"""O'quvchi profili: kirish ruxsati, mavzular bo'yicha test so'rovlari, mustahkamlash.

Oqim:
1. Ustoz profil havolasini yuboradi (``/men/<kalit>/``). O'quvchi ism-familiyasini va
   "kirishga ruxsat so'rash" tugmasini ko'radi.
2. Ustoz 2 / 3 / 4 soatga ruxsat beradi — shu vaqt ichida profil ochiq.
3. Profilda ustoz ruxsat etgan mavzular va guruhdagi navbatdagi yangi mavzu. O'quvchi
   testni o'zi boshlaydi (10/12 savol, 5/10 daqiqa) — ustoz ruxsati shart emas.
   Bir mavzu bo'yicha kuniga ko'pi bilan ``TestRequest.DAILY_LIMIT`` ta.
4. Natija 60% dan past bo'lsa — "Darsni qayta mustahkamlash" o'zi ochiladi; material
   ochilgandan 20 daqiqa o'tib qayta topshirish mumkin. Yangi mavzu testi — 30 daqiqa
   tayyorlanishdan keyin.
5. Har bir yakunlangan test uchun coinlar (``academy.coins``).
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
from .coins import PASS_PERCENT
from .models import QuizAttempt, QuizBatch, Student, StudySession, SyllabusItem, TestRequest, Topic
from .services import create_quiz_batch

log = logging.getLogger(__name__)

ACCESS_HOURS = (2, 3, 4)


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


# --- Mavzular va testlar ---------------------------------------------------------


def taught_topic_ids(student: Student) -> set[int]:
    return set(
        SyllabusItem.objects.filter(
            group_id=student.group_id, status=SyllabusItem.Status.TAUGHT
        ).values_list("topic_id", flat=True)
    )


def next_topic(student: Student) -> Topic | None:
    """Guruh dasturida oxirgi o'tilgan mavzudan keyingi (hali o'tilmagan) mavzu."""
    items = list(
        SyllabusItem.objects.filter(group_id=student.group_id)
        .select_related("topic")
        .order_by("order", "id")
    )
    last_taught = max(
        (i for i, item in enumerate(items) if item.status == SyllabusItem.Status.TAUGHT), default=-1
    )
    return next(
        (item.topic for item in items[last_taught + 1 :] if item.status == SyllabusItem.Status.PLANNED),
        None,
    )


def day_start(now=None):
    tz = timezone.get_current_timezone()
    today = timezone.localtime(now or timezone.now(), tz).date()
    return timezone.make_aware(datetime.combine(today, time.min), tz)


def used_today(student: Student, topic: Topic, now=None) -> int:
    """Bugun shu mavzu bo'yicha boshlangan testlar (rad etilganlar hisoblanmaydi)."""
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
    request: TestRequest | None  # boshlangan, lekin hali test yaratilmagan
    used: int  # bugun
    preview: bool  # guruhdagi navbatdagi (yangi) mavzu
    session: StudySession | None  # tegishli mustahkamlash/tayyorlanish
    now: datetime

    @property
    def left_today(self) -> int:
        return max(0, TestRequest.DAILY_LIMIT - self.used)

    @property
    def needs_review(self) -> bool:
        return bool(self.last and self.last.percent is not None and self.last.percent < PASS_PERCENT)

    @property
    def gate(self) -> str:
        """Test oldidan majburiy o'qish: "review" (past natija), "preview" (yangi mavzu) yoki ""."""
        if self.needs_review:
            return StudySession.Kind.REVIEW
        if self.preview and self.last is None:
            return StudySession.Kind.PREVIEW
        return ""

    @property
    def unlocks_at(self):
        return self.session.unlocks_at if self.session else None

    @property
    def locked(self) -> bool:
        return bool(self.gate) and (self.session is None or self.now < self.session.unlocks_at)

    @property
    def seconds_left(self) -> int:
        if not self.locked or self.session is None:
            return 0
        return max(0, int((self.session.unlocks_at - self.now).total_seconds()))

    @property
    def can_start(self) -> bool:
        return self.bank > 0 and self.left_today > 0 and not self.locked


def topic_rows(student: Student, now=None) -> list[TopicRow]:
    """Ustoz ruxsat bergan mavzular + navbatdagi yangi mavzu (oldindan tayyorlanish)."""
    now = now or timezone.now()
    topics = list(
        student.allowed_topics.select_related("module", "quiz").order_by(
            "module__order", "module__title", "order", "title"
        )
    )
    upcoming = next_topic(student)
    if upcoming and upcoming.pk not in {t.pk for t in topics}:
        topics.append(upcoming)
    ids = [t.pk for t in topics]
    open_requests = {
        r.topic_id: r
        for r in TestRequest.objects.filter(
            student=student, topic_id__in=ids, status=TestRequest.Status.APPROVED
        )
    }
    last = {}
    for a in (
        QuizAttempt.objects.filter(
            student=student, quiz__topic_id__in=ids, status=QuizAttempt.Status.FINISHED
        )
        .select_related("quiz")
        .order_by("finished_at")
    ):
        last[a.quiz.topic_id] = a
    sessions = {}
    for s in StudySession.objects.filter(student=student, topic_id__in=ids).order_by("started_at"):
        sessions[(s.topic_id, s.kind)] = s  # eng oxirgisi qoladi
    used = {}
    for r in TestRequest.objects.filter(
        student=student, topic_id__in=ids, created_at__gte=day_start(now)
    ).exclude(status=TestRequest.Status.REJECTED):
        used[r.topic_id] = used.get(r.topic_id, 0) + 1
    rows = []
    for t in topics:
        quiz = getattr(t, "quiz", None)
        row = TopicRow(
            topic=t,
            bank=quiz.questions.count() if quiz else 0,
            last=last.get(t.pk),
            request=open_requests.get(t.pk),
            used=used.get(t.pk, 0),
            preview=bool(upcoming and t.pk == upcoming.pk),
            session=None,
            now=now,
        )
        if row.gate:
            s = sessions.get((t.pk, row.gate))
            # Mustahkamlash — faqat oxirgi past natijadan keyin boshlangani hisoblanadi.
            if s and (row.gate != StudySession.Kind.REVIEW or s.started_at >= row.last.finished_at):
                row.session = s
        rows.append(row)
    return rows


def row_for(student: Student, topic: Topic) -> TopicRow | None:
    return next((r for r in topic_rows(student) if r.topic.pk == topic.pk), None)


def open_study(student: Student, topic: Topic) -> TopicRow | None:
    """Material sahifasi ochilganda: kerak bo'lsa mustahkamlash/tayyorlanish vaqtini boshlaydi."""
    row = row_for(student, topic)
    if row and row.gate and row.session is None and is_open(student):
        StudySession.objects.create(student=student, topic=topic, kind=row.gate)
        row = row_for(student, topic)
    return row


def begin_test(student: Student, topic: Topic) -> TestRequest:
    """O'quvchi testni o'zi boshlaydi (ustoz ruxsati shart emas). Sabab bilan rad etilsa —
    ProfileError. Qaytgan so'rov bo'yicha o'quvchi savollar soni va vaqtni tanlaydi."""
    if not is_open(student):
        raise ProfileError("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang.")
    with transaction.atomic():
        row = row_for(student, topic)
        if row is None:
            raise ProfileError("Bu mavzudan test topshirishga ruxsat berilmagan.")
        if row.request is not None:
            return row.request  # boshlangan, lekin hali tanlanmagan — o'shani davom ettiramiz
        if not row.bank:
            raise ProfileError("Bu mavzuda hali test savollari yo‘q.")
        if not row.left_today:
            raise ProfileError(
                f"Bugun bu mavzudan {TestRequest.DAILY_LIMIT} ta test topshirdingiz — ertaga qayta urinib ko‘ring."
            )
        if row.locked:
            what = "Mustahkamlash" if row.gate == StudySession.Kind.REVIEW else "Yangi mavzuga tayyorlanish"
            if row.session is None:
                raise ProfileError(f"Avval materialni oching: {what.lower()} vaqti shundan boshlanadi.")
            at = timezone.localtime(row.unlocks_at)
            raise ProfileError(f"{what} {at:%H:%M} da tugaydi — keyin test ochiladi.")
        kind = (
            TestRequest.Kind.RETAKE
            if row.gate == StudySession.Kind.REVIEW
            else TestRequest.Kind.PREVIEW
            if row.gate == StudySession.Kind.PREVIEW
            else TestRequest.Kind.FIRST
        )
        return TestRequest.objects.create(
            student=student,
            topic=topic,
            kind=kind,
            status=TestRequest.Status.APPROVED,
            decided_at=timezone.now(),
        )


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
