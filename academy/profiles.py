"""O'quvchi profili: kirish ruxsati, mavzular bo'yicha test so'rovlari, mustahkamlash.

Oqim:
1. Ustoz profil havolasini yuboradi (``/men/<kalit>/``). O'quvchi ism-familiyasini va
   "kirishga ruxsat so'rash" tugmasini ko'radi.
2. Ustoz 2 / 3 / 4 soatga ruxsat beradi — shu vaqt ichida profil ochiq.
3. Profilda guruhda o'tilgan mavzular (avtomatik) va ustoz qo'shimcha ruxsat etganlari. O'quvchi
   testni o'zi boshlaydi (10/12 savol, 5/10 daqiqa) — ustoz ruxsati shart emas.
   Bir mavzu bo'yicha kuniga ko'pi bilan ``TestRequest.DAILY_LIMIT`` ta.
4. Natija 60% dan past bo'lsa — "Darsni qayta mustahkamlash" o'zi ochiladi; material
   ochilgandan 20 daqiqa o'tib qayta topshirish mumkin.
5. Har bir yakunlangan test uchun quvvat ⚡️ (``academy.coins``).
6. Quvvat sarflab guruh dasturidagi navbatdagi mavzularni oldindan ochish (``unlock_topic``):
   material va test ochiladi, 70%+ natijada "oldindan o'zlashtirdi" bonusi.
"""

import logging
import threading
from dataclasses import dataclass
from datetime import datetime, time, timedelta

from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import telegram_sender as tg
from .coins import PASS_PERCENT
from .models import (
    CoinTransaction,
    QuizAttempt,
    QuizBatch,
    Student,
    StudySession,
    SyllabusItem,
    TestRequest,
    Topic,
    TopicUnlock,
)
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
    session: StudySession | None  # tegishli mustahkamlash/tayyorlanish
    now: datetime
    unlocked: bool = False  # quvvat bilan oldindan ochilgan (guruhda hali o'tilmagan)

    @property
    def left_today(self) -> int:
        return max(0, TestRequest.DAILY_LIMIT - self.used)

    @property
    def needs_review(self) -> bool:
        return bool(self.last and self.last.percent is not None and self.last.percent < PASS_PERCENT)

    @property
    def gate(self) -> str:
        """Test oldidan majburiy o'qish: "review" (past natija bo'lsa) yoki ""."""
        return StudySession.Kind.REVIEW if self.needs_review else ""

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
    """Guruhda o'tilgan mavzular (avtomatik) + ustoz ruxsat bergan + quvvat bilan ochilgan mavzular."""
    now = now or timezone.now()
    allowed = set(student.allowed_topics.values_list("pk", flat=True))
    taught = taught_topic_ids(student)
    unlocked = unlocked_topic_ids(student)
    topics = list(
        Topic.objects.filter(pk__in=allowed | taught | unlocked)
        .select_related("module", "quiz")
        .order_by("module__order", "module__title", "order", "title")
    )
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
            session=None,
            now=now,
            unlocked=t.pk in unlocked and t.pk not in taught,
        )
        if row.gate:
            s = sessions.get((t.pk, row.gate))
            # Mustahkamlash — faqat oxirgi past natijadan keyin boshlangani hisoblanadi.
            if s and s.started_at >= row.last.finished_at:
                row.session = s
        rows.append(row)
    return rows


def row_for(student: Student, topic: Topic) -> TopicRow | None:
    return next((r for r in topic_rows(student) if r.topic.pk == topic.pk), None)


def open_study(student: Student, topic: Topic) -> TopicRow | None:
    """Material sahifasi ochilganda: past natija bo'lsa mustahkamlash vaqtini boshlaydi."""
    row = row_for(student, topic)
    if row and row.gate and row.session is None and is_open(student):
        StudySession.objects.create(student=student, topic=topic, kind=row.gate)
        row = row_for(student, topic)
    return row


def begin_test(student: Student, topic: Topic) -> TestRequest:
    """O'quvchi testni o'zi boshlaydi (ustoz ruxsati shart emas). Sabab bilan rad etilsa —
    ProfileError. Qaytgan so'rov bo'yicha o'quvchi savollar soni va vaqtni tanlaydi."""
    if not is_open(student):
        raise ProfileError(_("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang."))
    with transaction.atomic():
        row = row_for(student, topic)
        if row is None:
            raise ProfileError(_("Bu mavzudan test topshirishga ruxsat berilmagan."))
        if row.request is not None:
            return row.request  # boshlangan, lekin hali tanlanmagan — o'shani davom ettiramiz
        if not row.bank:
            raise ProfileError(_("Bu mavzuda hali test savollari yo‘q."))
        if not row.left_today:
            raise ProfileError(
                _("Bugun bu mavzudan {DAILY_LIMIT} ta test topshirdingiz — ertaga qayta urinib ko‘ring.").format(
                    DAILY_LIMIT=TestRequest.DAILY_LIMIT
                )
            )
        if row.locked:
            if row.session is None:
                raise ProfileError(_("Avval materialni oching: mustahkamlash vaqti shundan boshlanadi."))
            at = timezone.localtime(row.unlocks_at)
            raise ProfileError(_("Mustahkamlash {at:%H:%M} da tugaydi — keyin test ochiladi.").format(at=at))
        if row.gate:
            kind = TestRequest.Kind.RETAKE
        elif row.unlocked and not row.last:
            kind = TestRequest.Kind.PREVIEW  # 70%+ bo'lsa — "oldindan o'zlashtirdi" bonusi
        else:
            kind = TestRequest.Kind.FIRST
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
        raise ProfileError(_("Savollar soni 10 yoki 12, vaqt 5 yoki 10 daqiqa bo‘lishi kerak."))
    if not is_open(req.student):
        raise ProfileError(_("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang."))
    with transaction.atomic():
        req = TestRequest.objects.select_for_update().get(pk=req.pk)
        if req.status != TestRequest.Status.APPROVED:
            raise ProfileError(_("Bu so‘rovga ruxsat berilmagan yoki u allaqachon ishlatilgan."))
        batch = create_quiz_batch(req.topic.quiz, [req.student], questions, minutes)
        QuizBatch.objects.filter(pk=batch.pk).update(from_profile=True, channels="")
        attempt = batch.attempts.get()
        req.status, req.attempt = TestRequest.Status.USED, attempt
        req.save(update_fields=["status", "attempt"])
    return attempt


# --- Quvvat bilan mavzu ochish ------------------------------------------------------

UNLOCK_COST = 30  # ⚡️ — bitta mavzu
UNLOCK_AHEAD = 3  # guruh dasturida navbatdagi nechta mavzu ochishga taklif qilinadi
UNLOCK_REASON = "🔓 Mavzu ochildi: {title}"


def unlocked_topic_ids(student: Student) -> set[int]:
    return set(student.topic_unlocks.values_list("topic_id", flat=True))


def unlock_offers(student: Student) -> list[Topic]:
    """Guruh dasturidagi navbatdagi (hali o'tilmagan va profilda yo'q) mavzular — material yoki
    test savollari bori."""
    available = (
        set(student.allowed_topics.values_list("pk", flat=True))
        | taught_topic_ids(student)
        | unlocked_topic_ids(student)
    )
    items = (
        SyllabusItem.objects.filter(group_id=student.group_id, status=SyllabusItem.Status.PLANNED)
        .exclude(topic_id__in=available)
        .select_related("topic__module", "topic__quiz")
        .order_by("order", "pk")
    )
    offers = []
    for item in items:
        topic = item.topic
        quiz = getattr(topic, "quiz", None)
        if topic.study or (quiz and quiz.questions.exists()):
            offers.append(topic)
        if len(offers) == UNLOCK_AHEAD:
            break
    return offers


def unlock_topic(student: Student, topic: Topic) -> TopicUnlock:
    """Quvvat sarflab mavzuni ochish. Sabab bilan rad etilsa — ProfileError."""
    from .engagement import available

    if not is_open(student):
        raise ProfileError(_("Profilga kirish vaqti tugagan — ustozdan qayta ruxsat so‘rang."))
    with transaction.atomic():
        Student.objects.select_for_update().filter(pk=student.pk).first()  # bir vaqtda ikki so'rov bo'lmasin
        if TopicUnlock.objects.filter(student=student, topic=topic).exists():
            raise ProfileError(_("Bu mavzu allaqachon ochilgan."))
        if topic.pk not in {t.pk for t in unlock_offers(student)}:
            raise ProfileError(_("Bu mavzuni hozir ochib bo‘lmaydi — navbatdagi mavzulardan birini tanlang."))
        have = available(student)
        if have < UNLOCK_COST:
            raise ProfileError(
                _("Quvvat yetmaydi: kerak {cost} ⚡️, sizda {available} ⚡️.").format(cost=UNLOCK_COST, available=have)
            )
        tx = CoinTransaction.objects.create(
            student=student, amount=-UNLOCK_COST, reason=UNLOCK_REASON.format(title=topic.title)[:120]
        )
        unlock = TopicUnlock.objects.create(student=student, topic=topic, cost=UNLOCK_COST, transaction=tx)
    notify(f"🔓 {student.full_name} ({student.group.code}): “{topic.title}” mavzusini {UNLOCK_COST} ⚡️ ga ochdi.")
    return unlock


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
