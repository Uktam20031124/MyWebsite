"""Coinlar: o'quvchi yechgan testlari uchun mukofot.

Har bir yakunlangan test uchun natijaga qarab coin (bir marta), qo'shimcha:
- mustahkamlab, qayta topshirib o'tgani — bonus.
"""

from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import CoinTransaction, QuizAttempt, Student

PASS_PERCENT = 70  # bundan past natijada mustahkamlash taklif qilinadi
# (natija chegarasi, coin) — kattasidan boshlab birinchi mos keladigani.
SCORE_COINS = ((90, 10), (75, 7), (60, 5), (0, 1))
PREVIEW_BONUS = 5
RETAKE_BONUS = 3
# Profildan bitta testni shuncha marta topshirgandan keyin — takroriy urinish: faqat
# REPEAT_PERCENT% va undan yuqori natijaga REPEAT_COINS, past natijaga — hech narsa.
REPEAT_AFTER = 2
REPEAT_PERCENT = 90
REPEAT_COINS = 1

RULES = [
    _("90% va undan yuqori — 10 ⚡️"),
    _("75–89% — 7 ⚡️"),
    _("60–74% — 5 ⚡️"),
    _("60% dan past — 1 ⚡️ (urinish uchun)"),
    _("Mustahkamlab, qayta topshirib o‘tsangiz ({PASS_PERCENT}%+) — yana +{RETAKE_BONUS}").format(
        PASS_PERCENT=PASS_PERCENT, RETAKE_BONUS=RETAKE_BONUS
    ),
    _("Profildan bitta testni {n} martadan ko‘p topshirsangiz — faqat {p}%+ natijaga {c} ⚡️").format(
        n=REPEAT_AFTER, p=REPEAT_PERCENT, c=REPEAT_COINS
    ),
    _("Xatolar mashqida savolni 3 marta ketma-ket to‘g‘ri yechsangiz — +2"),
    _("Har 7 kun ketma-ket faol bo‘lsangiz (🔥 streak) — +10"),
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


def is_repeat(attempt: QuizAttempt) -> bool:
    """Profildan shu testni avval ``REPEAT_AFTER`` marta (yoki ko'proq) yakunlagan bo'lsa."""
    if not attempt.batch.from_profile:
        return False
    earlier = QuizAttempt.objects.filter(
        student_id=attempt.student_id,
        quiz_id=attempt.quiz_id,
        status=QuizAttempt.Status.FINISHED,
        batch__from_profile=True,
    ).exclude(pk=attempt.pk)
    if attempt.finished_at:
        earlier = earlier.filter(finished_at__lt=attempt.finished_at)
    return earlier.count() >= REPEAT_AFTER


def repeat_info(student: Student, quiz_id: int) -> dict | None:
    """Profil testini boshlashdan oldin: takroriy urinish bo'lsa — qoida (o'quvchiga ko'rsatish uchun)."""
    done = QuizAttempt.objects.filter(
        student=student, quiz_id=quiz_id, status=QuizAttempt.Status.FINISHED, batch__from_profile=True
    ).count()
    if done < REPEAT_AFTER:
        return None
    return {"done": done, "after": REPEAT_AFTER, "percent": REPEAT_PERCENT, "coins": REPEAT_COINS}


def award_for_attempt(attempt: QuizAttempt) -> None:
    if attempt.status != QuizAttempt.Status.FINISHED or not attempt.total:
        return
    percent = attempt.percent
    if is_repeat(attempt):
        # Takroriy urinish: bonuslar yo'q, faqat a'lo natijaga ramziy quvvat.
        if percent >= REPEAT_PERCENT:
            _give(attempt, REPEAT_COINS, f"Takroriy test: {percent}%")
        return
    _give(attempt, score_coins(percent), f"Test: {percent}%")
    if percent < PASS_PERCENT:
        return
    request = getattr(attempt, "test_request", None)
    kind = request.kind if request else ""
    if kind == "preview":
        _give(attempt, PREVIEW_BONUS, "Yangi mavzuni oldindan o‘zlashtirdi")
    elif kind == "retake":
        _give(attempt, RETAKE_BONUS, "Mustahkamlab, qayta topshirdi")


# --- Ustozdan sovg'a -----------------------------------------------------------------
GIFT_REASON = "🎁 Ustozdan sovg‘a"
GIFT_MAX = 1000
GIFT_PRESETS = (10, 50, 100, 300)
GIFT_UNDO_HOURS = 24  # adashib berilgan sovg'ani shu vaqt ichida bekor qilish mumkin


def gift(student: Student, amount: int, note: str = "") -> CoinTransaction:
    """Ustoz o'quvchiga coin sovg'a qiladi (izoh — ixtiyoriy, coin tarixida ko'rinadi)."""
    if not 1 <= amount <= GIFT_MAX:
        raise ValueError(amount)
    note = " ".join(note.split())[:80]
    reason = f"{GIFT_REASON}: {note}" if note else GIFT_REASON
    return CoinTransaction.objects.create(student=student, amount=amount, reason=reason)


def undo_gift(tx: CoinTransaction) -> bool:
    """Yaqinda berilgan sovg'ani bekor qilish (yozuv o'chiriladi — tarixda qolmaydi)."""
    if not tx.can_undo:
        return False
    tx.delete()
    return True


# --- Test qoidasini buzish (oynadan chiqish, nusxalash) uchun jarima ----------------------
PENALTY_PREFIX = "⚠️ Test qoidasi buzildi"
PENALTY_MAX = 5


def penalize(attempt: QuizAttempt, amount: int) -> int:
    """Ustoz ogohlantirishlarni ko'rib chiqadi: 1–5 ⚡️ ayiradi yoki 0 — kechiradi.

    Qayta qaror avvalgisini almashtiradi (jarima ikki marta olinmaydi); balansdan ko'p
    ayirilmaydi. Natija: haqiqatda ayirilgan quvvat."""
    if not 0 <= amount <= PENALTY_MAX:
        raise ValueError(amount)
    with transaction.atomic():
        CoinTransaction.objects.filter(attempt=attempt, reason__startswith=PENALTY_PREFIX).delete()
        taken = min(amount, max(0, balance(attempt.student)))
        if taken:
            CoinTransaction.objects.create(
                student_id=attempt.student_id,
                attempt=attempt,
                amount=-taken,
                reason=f"{PENALTY_PREFIX}: {attempt.quiz.topic.title}"[:120],
            )
        attempt.penalty = taken
        attempt.warning_checked_at = timezone.now()
        attempt.save(update_fields=["penalty", "warning_checked_at"])
    return taken


def balance(student: Student) -> int:
    return student.coins.aggregate(s=Sum("amount"))["s"] or 0


def balances(student_ids) -> dict[int, int]:
    rows = (
        CoinTransaction.objects.filter(student_id__in=list(student_ids))
        .values("student_id")
        .annotate(s=Sum("amount"))
    )
    return {r["student_id"]: r["s"] for r in rows}
