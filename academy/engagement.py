"""O'quvchini har kuni o'qishga undaydigan imkoniyatlar.

- **Xatolar ustida ishlash** — xato qilingan savollar yig'iladi; mashqda 3 marta ketma-ket
  to'g'ri yechilsa ro'yxatdan chiqadi (+coin). Keyingi testlarda ular ko'proq tushadi.
- **Streak** — ketma-ket faol kunlar (test yoki mashq); har 7 kunda bonus coin.
- **Quvvat reytingi** — guruhda joriy quvvat balansi bo'yicha (profildagi raqam bilan bir xil).
- **Coin do'koni** — sovg'a so'rovi; ustoz tasdiqlasa coin yechiladi.
"""

import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from django.db import transaction
from django.db.models import Count, F, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import coins
from .models import (
    CoinTransaction,
    DailyActivity,
    Mistake,
    Purchase,
    Question,
    QuizAttempt,
    Reward,
    Student,
)

STREAK_BONUS_EVERY = 7
STREAK_BONUS = 10
MISTAKE_FIXED_COINS = 2
LEADERBOARD_SIZE = 5


class EngagementError(Exception):
    """O'quvchiga ko'rsatiladigan sabab."""


def today(now=None) -> date:
    return timezone.localtime(now or timezone.now()).date()


# --- Test yakunlanganda ------------------------------------------------------------


def on_attempt_finished(attempt: QuizAttempt) -> None:
    """QuizAttempt.finish tranzaksiyasi ichida: coin, xatolar, faol kun."""
    coins.award_for_attempt(attempt)
    record_mistakes(attempt)
    record_activity(attempt.student, attempt.finished_at)


def record_mistakes(attempt: QuizAttempt) -> None:
    now = attempt.finished_at or timezone.now()
    items = [i for i in (attempt.snapshot or []) if not i.get("missing")]
    existing = Question.objects.filter(pk__in=[i["id"] for i in items]).values_list("pk", flat=True)
    existing = set(existing)
    for item in items:
        qid = item["id"]
        if qid not in existing:
            continue
        if item["is_correct"]:
            # Testda to'g'ri yechildi — mashqdagidek hisoblanadi.
            m = Mistake.objects.filter(
                student_id=attempt.student_id, question_id=qid, resolved_at__isnull=True
            ).first()
            if m:
                _count_correct(m, now)
            continue
        add_mistake(attempt.student_id, qid, now)


def add_mistake(student_id: int, question_id: int, now=None) -> None:
    """Xato javob: savol "Xatolar ustida ishlash"ga tushadi (o'zlashtirilgan bo'lsa — qayta ochiladi)."""
    now = now or timezone.now()
    m, created = Mistake.objects.get_or_create(
        student_id=student_id, question_id=question_id, defaults={"last_wrong_at": now}
    )
    if not created:
        m.streak, m.resolved_at, m.last_wrong_at = 0, None, now
        m.wrong_count += 1
        m.save(update_fields=["streak", "resolved_at", "last_wrong_at", "wrong_count"])


def _count_correct(m: Mistake, now) -> bool:
    """To'g'ri javob: ketma-ketlik +1; yetarli bo'lsa — o'zlashtirildi (+coin). True — yopildi."""
    m.streak += 1
    m.last_practiced_at = now
    fields = ["streak", "last_practiced_at"]
    fixed = m.streak >= Mistake.RESOLVE_AFTER
    if fixed:
        m.resolved_at = now
        fields.append("resolved_at")
    m.save(update_fields=fields)
    if fixed:
        CoinTransaction.objects.create(
            student_id=m.student_id,
            amount=MISTAKE_FIXED_COINS,
            reason=f"Xato tuzatildi: {m.question.quiz.topic.title}"[:120],
        )
    return fixed


# --- Streak ------------------------------------------------------------------------


def record_activity(student: Student, when=None) -> None:
    day = today(when)
    _day, created = DailyActivity.objects.get_or_create(student=student, day=day)
    if not created:
        return
    n = streak(student, day)
    if n and n % STREAK_BONUS_EVERY == 0:
        CoinTransaction.objects.create(
            student=student, amount=STREAK_BONUS, reason=f"🔥 {n} kun ketma-ket faol"
        )


def streak(student: Student, on: date | None = None) -> int:
    """Ketma-ket faol kunlar. Bugun hali faol bo'lmasa — kechagacha hisoblanadi (yo'qolmagan)."""
    on = on or today()
    days = set(
        DailyActivity.objects.filter(student=student, day__lte=on, day__gte=on - timedelta(days=400))
        .values_list("day", flat=True)
    )
    cur = on if on in days else on - timedelta(days=1)
    n = 0
    while cur in days:
        n += 1
        cur -= timedelta(days=1)
    return n


@dataclass
class StreakInfo:
    days: int
    active_today: bool
    week: list  # [(sana, faolmi)] — oxirgi 7 kun

    @property
    def to_bonus(self) -> int:
        return STREAK_BONUS_EVERY - self.days % STREAK_BONUS_EVERY


def streak_info(student: Student) -> StreakInfo:
    d = today()
    days = set(
        DailyActivity.objects.filter(student=student, day__gte=d - timedelta(days=6)).values_list("day", flat=True)
    )
    week = [(d - timedelta(days=i), d - timedelta(days=i) in days) for i in range(6, -1, -1)]
    return StreakInfo(days=streak(student, d), active_today=d in days, week=week)


# --- Xatolar ustida ishlash --------------------------------------------------------


def open_mistakes(student: Student):
    return Mistake.objects.filter(student=student, resolved_at__isnull=True)


def mistakes_by_topic(student: Student) -> list[dict]:
    rows = (
        open_mistakes(student)
        .values("question__quiz__topic_id", "question__quiz__topic__title")
        .annotate(n=Count("pk"))
        .order_by("-n", "question__quiz__topic__title")
    )
    return [
        {"topic_id": r["question__quiz__topic_id"], "title": r["question__quiz__topic__title"], "n": r["n"]}
        for r in rows
    ]


def next_mistake(student: Student, topic_id: int | None = None, exclude: int | None = None) -> Mistake | None:
    """Eng uzoq mashq qilinmagani (yangi xatolar birinchi); ketma-ket bir xil savol chiqmasin."""
    qs = open_mistakes(student).select_related("question__quiz__topic")
    if topic_id:
        qs = qs.filter(question__quiz__topic_id=topic_id)
    if exclude and qs.exclude(pk=exclude).exists():
        qs = qs.exclude(pk=exclude)
    return qs.order_by(F("last_practiced_at").asc(nulls_first=True), "last_wrong_at").first()


def shuffled_choices(m: Mistake, seed: str) -> list:
    choices = list(m.question.choices.all())
    random.Random(f"{seed}:{m.pk}:{m.streak}").shuffle(choices)
    return choices


@dataclass
class PracticeResult:
    correct: bool
    fixed: bool  # 3 marta to'g'ri — ro'yxatdan chiqdi
    left: int  # chiqishi uchun yana nechta to'g'ri javob kerak


def answer_mistake(student: Student, mistake_id: int, choice_id: int) -> PracticeResult:
    with transaction.atomic():
        m = (
            Mistake.objects.select_for_update()
            .select_related("question__quiz__topic")
            .filter(pk=mistake_id, student=student, resolved_at__isnull=True)
            .first()
        )
        if m is None:
            raise EngagementError(_("Bu savol allaqachon o‘zlashtirilgan yoki topilmadi."))
        choice = m.question.choices.filter(pk=choice_id).first()
        if choice is None:
            raise EngagementError(_("Javobni tanlang."))
        now = timezone.now()
        if choice.is_correct:
            fixed = _count_correct(m, now)
        else:
            m.streak, m.last_practiced_at = 0, now
            m.wrong_count += 1
            m.save(update_fields=["streak", "last_practiced_at", "wrong_count"])
            fixed = False
        record_activity(student, now)
    return PracticeResult(choice.is_correct, fixed, max(0, Mistake.RESOLVE_AFTER - m.streak))


# --- Haftalik reyting --------------------------------------------------------------


def week_start(now=None):
    d = today(now)
    monday = d - timedelta(days=d.weekday())
    return timezone.make_aware(datetime.combine(monday, time.min), timezone.get_current_timezone())


def quvvat_board(group_id: int) -> list[dict]:
    """Guruh reytingi joriy quvvat ⚡️ balansi bo'yicha — profildagi raqam bilan bir xil
    (yig'ilgani − sarflangani va jarimalar)."""
    rows = (
        Student.objects.filter(group_id=group_id, status=Student.Status.ACTIVE)
        .annotate(balance=Sum("coins__amount"))
        .order_by(F("balance").desc(nulls_last=True), "full_name")
    )
    board, place, prev = [], 0, None
    for i, s in enumerate(rows, start=1):
        b = s.balance or 0
        if b != prev:
            place, prev = i, b
        board.append({"student": s, "coins": b, "place": place})
    return board


# --- Coin do'koni ------------------------------------------------------------------


def available(student: Student) -> int:
    """Sarflash mumkin bo'lgan coin: balans − kutilayotgan so'rovlar."""
    pending = student.purchases.filter(status=Purchase.Status.PENDING).aggregate(s=Sum("cost"))["s"] or 0
    return coins.balance(student) - pending


def buy(student: Student, reward_id: int) -> Purchase:
    with transaction.atomic():
        Student.objects.select_for_update().filter(pk=student.pk).first()  # bir vaqtda ikki so'rov bo'lmasin
        reward = Reward.objects.filter(pk=reward_id, is_active=True).first()
        if reward is None:
            raise EngagementError(_("Bu sovg'a hozir do‘konda yo‘q."))
        if student.purchases.filter(reward=reward, status=Purchase.Status.PENDING).exists():
            raise EngagementError(_("Bu sovg'a uchun so‘rovingiz ustozda kutilmoqda."))
        if reward.perk == Reward.Perk.HONOR and student.honor_since:
            raise EngagementError(_("Sizda “A’lochi” unvoni allaqachon bor."))
        if available(student) < reward.cost:
            raise EngagementError(
                _("Quvvat yetmaydi: kerak {cost} ⚡️, sizda {available} ⚡️.").format(
                    cost=reward.cost, available=available(student)
                )
            )
        return Purchase.objects.create(student=student, reward=reward, title=reward.title, cost=reward.cost)


def decide_purchase(purchase: Purchase, approve: bool) -> None:
    with transaction.atomic():
        p = Purchase.objects.select_for_update().get(pk=purchase.pk)
        if p.status != Purchase.Status.PENDING:
            return
        if approve and coins.balance(p.student) < p.cost:
            approve = False  # balans yetmay qolgan (masalan, ustoz coin olib tashlagan)
        if approve:
            p.transaction = CoinTransaction.objects.create(
                student=p.student, amount=-p.cost, reason=f"Do‘kon: {p.title}"[:120]
            )
        p.status = Purchase.Status.APPROVED if approve else Purchase.Status.REJECTED
        p.decided_at = timezone.now()
        p.save(update_fields=["status", "decided_at", "transaction"])
        if approve and p.reward and p.reward.perk == Reward.Perk.HONOR:
            grant_honor(p.student, when=p.decided_at)


def grant_honor(student: Student, when=None) -> bool:
    """"A'lochi" unvonini berish (bor bo'lsa — o'zgarmaydi). Yangi berilgan bo'lsa True."""
    when = when or timezone.now()
    granted = Student.objects.filter(pk=student.pk, honor_since__isnull=True).update(honor_since=when)
    if granted:
        student.honor_since = when
    return bool(granted)


def revoke_honor(student: Student) -> None:
    Student.objects.filter(pk=student.pk).update(honor_since=None)
    student.honor_since = None


def pending_purchases():
    return Purchase.objects.filter(status=Purchase.Status.PENDING).select_related("student__group").order_by(
        "created_at"
    )
