"""Coinlar: o'quvchi yechgan testlari uchun mukofot.

Har bir yakunlangan test uchun natijaga qarab coin (bir marta), qo'shimcha:
- mustahkamlab, qayta topshirib o'tgani — bonus.
"""

from django.db import IntegrityError, transaction
from django.db.models import Sum

from .models import CoinTransaction, QuizAttempt, Student

PASS_PERCENT = 60
# (natija chegarasi, coin) — kattasidan boshlab birinchi mos keladigani.
SCORE_COINS = ((90, 10), (75, 7), (60, 5), (0, 1))
PREVIEW_BONUS = 5
RETAKE_BONUS = 3

RULES = [
    "90% va undan yuqori — 10 coin",
    "75–89% — 7 coin",
    "60–74% — 5 coin",
    "60% dan past — 1 coin (urinish uchun)",
    f"Mustahkamlab, qayta topshirib o‘tsangiz (60%+) — yana +{RETAKE_BONUS}",
    "Xatolar mashqida savolni 3 marta ketma-ket to‘g‘ri yechsangiz — +2",
    "Har 7 kun ketma-ket faol bo‘lsangiz (🔥 streak) — +10",
]


def score_coins(percent: int) -> int:
    return next(c for limit, c in SCORE_COINS if percent >= limit)


def _give(attempt, amount, reason) -> None:
    try:
        with transaction.atomic():
            CoinTransaction.objects.create(
                student_id=attempt.student_id, attempt=attempt, amount=amount, reason=reason
            )
    except IntegrityError:
        pass  # shu test uchun shu sabab bilan allaqachon berilgan


def award_for_attempt(attempt: QuizAttempt) -> None:
    if attempt.status != QuizAttempt.Status.FINISHED or not attempt.total:
        return
    percent = attempt.percent
    _give(attempt, score_coins(percent), f"Test: {percent}%")
    if percent < PASS_PERCENT:
        return
    request = getattr(attempt, "test_request", None)
    kind = request.kind if request else ""
    if kind == "preview":
        _give(attempt, PREVIEW_BONUS, "Yangi mavzuni oldindan o‘zlashtirdi")
    elif kind == "retake":
        _give(attempt, RETAKE_BONUS, "Mustahkamlab, qayta topshirdi")


def balance(student: Student) -> int:
    return student.coins.aggregate(s=Sum("amount"))["s"] or 0


def balances(student_ids) -> dict[int, int]:
    rows = (
        CoinTransaction.objects.filter(student_id__in=list(student_ids))
        .values("student_id")
        .annotate(s=Sum("amount"))
    )
    return {r["student_id"]: r["s"] for r in rows}
