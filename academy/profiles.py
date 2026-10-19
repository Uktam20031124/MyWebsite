"""O'quvchi profili: kirish ruxsati, mavzular bo'yicha test so'rovlari, mustahkamlash.

Oqim:
1. Ustoz profil havolasini yuboradi (``/men/<kalit>/``). O'quvchi ism-familiyasini va
   "kirishga ruxsat so'rash" tugmasini ko'radi.
2. Ustoz 2 / 3 / 4 soatga ruxsat beradi — shu vaqt ichida profil ochiq.
3. Profilda faqat ustoz shu o'quvchiga ruxsat etgan mavzular. O'quvchi test so'raydi,
   ustoz ruxsat bergach, o'zi 10/12 savol va 5/10 daqiqani tanlab, testni boshlaydi.
   Bir mavzu bo'yicha kuniga ko'pi bilan ``TestRequest.DAILY_LIMIT`` ta.
4. Natija past bo'lsa — "Darsni qayta mustahkamlash" (mavzu materiali, bajarilgan
   misollar), so'ng qayta topshirish so'rovi.
"""

import logging
import threading
from dataclasses import dataclass
from datetime import datetime, time, timedelta

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from . import telegram_sender as tg
from .models import QuizAttempt, QuizBatch, Student, SyllabusItem, TestRequest, Topic
from .services import create_quiz_batch

log = logging.getLogger(__name__)

ACCESS_HOURS = (2, 3, 4)
PASS_PERCENT = 50  # bundan past natija — mustahkamlash tavsiya etiladi


class ProfileError(Exception):
    """O'quvchiga ko'rsatiladigan sabab."""


# --- Kirish ruxsati ------------------------------------------------------------


def is_open(student: Student, now=None) -> bool:
    return bool(student.profile_until and student.profile_until > (now or timezone.now()))


def request_access(student: Student) -> bool:
    """Kirish so'rovi; profil ochiq bo'lsa yoki so'rov kutilayotgan bo'lsa — yo'q."""
    if is_open(student) or student.profile_requested_at:
        return False
    student.profile_requested_at = timezone.now()
    student.save(update_fields=["profile_requested_at"])
    notify(f"🔑 {student.full_name} ({student.group.code}) profiliga kirishga ruxsat so‘ramoqda.")
    return True


def grant_access(student: Student, hours: int) -> None:
    if hours not in ACCESS_HOURS:
        raise ValueError(hours)
    student.profile_until = timezone.now() + timedelta(hours=hours)
    student.profile_requested_at = None
    student.save(update_fields=["profile_until", "profile_requested_at"])


def close_access(student: Student) -> None:
    """Ruxsatni yopish yoki so'rovni rad etish."""
    student.profile_until = None
    student.profile_requested_at = None
    student.save(update_fields=["profile_until", "profile_requested_at"])


# --- Mavzular va so'rovlar -------------------------------------------------------


def taught_topic_ids(student: Student) -> set[int]:
    return set(
        SyllabusItem.objects.filter(
            group_id=student.group_id, status=SyllabusItem.Status.TAUGHT
        ).values_list("topic_id", flat=True)
    )


def day_start(now=None):
    tz = timezone.get_current_timezone()
    today = timezone.localtime(now or timezone.now(), tz).date()
    return timezone.make_aware(datetime.combine(today, time.min), tz)


def used_today(student: Student, topic: Topic, now=None) -> int:
    """Bugun shu mavzu bo'yicha so'rovlar (rad etilganlar hisoblanmaydi)."""
    return (
        TestRequest.objects.filter(student=student, topic=topic, created_at__gte=day_start(now))
        .exclude(status=TestRequest.Status.REJECTED)
        .count()
    )


@dataclass
class TopicRow:
    topic: Topic
    bank: int  # savollar banki hajmi
    last: QuizAttempt | None  # oxirgi yakunlangan test
    request: TestRequest | None  # kutilayotgan yoki ruxsat berilgan so'rov
    used: int  # bugun

    @property
    def left_today(self) -> int:
        return max(0, TestRequest.DAILY_LIMIT - self.used)

    @property
    def needs_review(self) -> bool:
        return bool(self.last and self.last.percent is not None and self.last.percent < PASS_PERCENT)

    @property
    def can_request(self) -> bool:
        return self.bank > 0 and self.request is None and self.left_today > 0


def topic_rows(student: Student, now=None) -> list[TopicRow]:
    topics = list(student.allowed_topics.select_related("module", "quiz").order_by(
        "module__order", "module__title", "order", "title"
    ))
    open_requests = {
        r.topic_id: r
        for r in TestRequest.objects.filter(
            student=student,
            topic__in=topics,
            status__in=[TestRequest.Status.PENDING, TestRequest.Status.APPROVED],
        )
    }
    last = {}
    for a in (
        QuizAttempt.objects.filter(
            student=student, quiz__topic__in=topics, status=QuizAttempt.Status.FINISHED
        )
        .select_related("quiz")
        .order_by("finished_at")
    ):
        last[a.quiz.topic_id] = a
    start = day_start(now)
    used = {}
    for r in TestRequest.objects.filter(
        student=student, topic__in=topics, created_at__gte=start
    ).exclude(status=TestRequest.Status.REJECTED):
        used[r.topic_id] = used.get(r.topic_id, 0) + 1
    rows = []
    for t in topics:
        quiz = getattr(t, "quiz", None)
        rows.append(
            TopicRow(
                topic=t,
                bank=quiz.questions.count() if quiz else 0,
                last=last.get(t.pk),
                request=open_requests.get(t.pk),
                used=used.get(t.pk, 0),
            )
        )
    return rows


def request_test(student: Student, topic: Topic, kind: str = TestRequest.Kind.FIRST) -> TestRequest:
    """Test so'rovi. Sabab bilan rad etilsa — ProfileError."""
    if not is_open(student):
        raise ProfileError("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang.")
    with transaction.atomic():
        if not student.allowed_topics.filter(pk=topic.pk).exists():
            raise ProfileError("Bu mavzudan test topshirishga ruxsat berilmagan.")
        quiz = getattr(topic, "quiz", None)
        if quiz is None or not quiz.questions.exists():
            raise ProfileError("Bu mavzuda hali test savollari yo‘q.")
        if TestRequest.objects.filter(
            student=student,
            topic=topic,
            status__in=[TestRequest.Status.PENDING, TestRequest.Status.APPROVED],
        ).exists():
            raise ProfileError("Bu mavzu bo‘yicha so‘rovingiz allaqachon bor.")
        if used_today(student, topic) >= TestRequest.DAILY_LIMIT:
            raise ProfileError(
                f"Bugun bu mavzudan {TestRequest.DAILY_LIMIT} ta test topshirdingiz — ertaga qayta urinib ko‘ring."
            )
        req = TestRequest.objects.create(student=student, topic=topic, kind=kind)
    label = "qayta topshirmoqchi" if kind == TestRequest.Kind.RETAKE else "test topshirmoqchi"
    notify(f"📝 {student.full_name} ({student.group.code}) “{topic.title}” mavzusidan {label}.")
    return req


def decide_test(req: TestRequest, approve: bool) -> None:
    if req.status != TestRequest.Status.PENDING:
        return
    req.status = TestRequest.Status.APPROVED if approve else TestRequest.Status.REJECTED
    req.decided_at = timezone.now()
    req.save(update_fields=["status", "decided_at"])


def start_test(req: TestRequest, questions: int, minutes: int) -> QuizAttempt:
    """Ruxsat berilgan so'rovdan testni yaratadi; o'quvchi keyin boshlash sahifasiga o'tadi."""
    if questions not in TestRequest.QUESTION_CHOICES or minutes not in TestRequest.MINUTE_CHOICES:
        raise ProfileError("Savollar soni 10 yoki 12, vaqt 5 yoki 10 daqiqa bo‘lishi kerak.")
    if not is_open(req.student):
        raise ProfileError("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang.")
    with transaction.atomic():
        req = TestRequest.objects.select_for_update().get(pk=req.pk)
        if req.status != TestRequest.Status.APPROVED:
            raise ProfileError("Bu so‘rovga ruxsat berilmagan yoki u allaqachon ishlatilgan.")
        batch = create_quiz_batch(req.topic.quiz, [req.student], questions, minutes)
        QuizBatch.objects.filter(pk=batch.pk).update(from_profile=True, channels="")
        attempt = batch.attempts.get()
        req.status, req.attempt = TestRequest.Status.USED, attempt
        req.save(update_fields=["status", "attempt"])
    return attempt


# --- Ustozga ---------------------------------------------------------------------


def pending_access():
    return Student.objects.filter(profile_requested_at__isnull=False).select_related("group").order_by(
        "profile_requested_at"
    )


def pending_tests():
    return (
        TestRequest.objects.filter(status=TestRequest.Status.PENDING)
        .select_related("student__group", "topic")
        .order_by("created_at")
    )


def notify(text: str) -> None:
    """Ustozning Telegram "Saqlangan xabarlar"iga — fonda (o'quvchi kutib qolmaydi)."""
    if not tg.is_configured():
        return
    if settings.SITE_URL:
        text += "\n" + settings.SITE_URL + reverse("quiz_review_requests")

    def run():
        try:
            tg.send_text_to_self(text)
        except Exception:  # noqa: BLE001 — bildirishnoma ixtiyoriy
            log.warning("Profil so'rovi bildirishnomasi yuborilmadi", exc_info=True)

    threading.Thread(target=run, daemon=True).start()
