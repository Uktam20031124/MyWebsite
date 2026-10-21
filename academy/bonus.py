"""Qo'shimcha savollar: guruhda o'tilgan mavzulardan savollar — profilda, QR kod orqali.

- Har savolga **bir marta** javob beriladi; to'g'ri bo'lsa — test uchun ustoz belgilagan
  quvvat (``Quiz.bonus_quvvat``, 1–5 ⚡️).
- To'g'ri javob ko'rsatilmaydi (asosiy testlar banki ochilib qolmasin); xato savol
  "Xatolar ustida ishlash"ga tushadi.
- Kuniga ``DAILY_LIMIT`` ta savol — bankni bir o'tirishda "yig'ib olish" emas, har kungi odat.
- Navbatdagi savol barqaror: sahifani yangilab, qiyin savolni almashtirib bo'lmaydi.
"""

import random
from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from . import engagement, profiles
from .models import BonusAnswer, Choice, CoinTransaction, Question, QuizLanguage, Student

DAILY_LIMIT = 10
REASON = "➕ Qo‘shimcha savol: {topic}"


class BonusError(Exception):
    """O'quvchiga ko'rsatiladigan sabab."""


def questions(student: Student, topic_id: int | None = None):
    """O'tilgan mavzulardagi hali javob berilmagan savollar."""
    qs = Question.objects.filter(quiz__topic_id__in=profiles.taught_topic_ids(student)).exclude(
        bonus_answers__student=student
    )
    return qs.filter(quiz__topic_id=topic_id) if topic_id else qs


def answered_today(student: Student) -> int:
    return student.bonus_answers.filter(answered_at__gte=profiles.day_start()).count()


def next_question(student: Student, topic_id: int | None = None) -> Question | None:
    ids = sorted(questions(student, topic_id).values_list("pk", flat=True))
    if not ids:
        return None
    seed = f"{student.portal_token}:{student.bonus_answers.count()}:{topic_id or 0}"
    pk = random.Random(seed).choice(ids)
    return Question.objects.select_related("quiz__topic").prefetch_related("choices").get(pk=pk)


def shuffled_choices(student: Student, question: Question) -> list[Choice]:
    choices = list(question.choices.all())
    random.Random(f"{student.portal_token}:{question.pk}").shuffle(choices)
    return choices


@dataclass
class BonusResult:
    correct: bool
    coins: int
    topic: str


def answer(student: Student, question_id: int, choice_id: int) -> BonusResult:
    with transaction.atomic():
        if answered_today(student) >= DAILY_LIMIT:
            raise BonusError(_("Bugungi limit tugadi ({n} ta savol). Ertaga davom eting!").format(n=DAILY_LIMIT))
        question = questions(student).select_related("quiz__topic").filter(pk=question_id).first()
        if question is None:
            raise BonusError(_("Bu savolga javob berib bo‘lmaydi — keyingisiga o‘ting."))
        choice = question.choices.filter(pk=choice_id).first()
        if choice is None:
            raise BonusError(_("Javobni tanlang."))
        topic = question.quiz.topic.title
        amount = question.quiz.bonus_quvvat if choice.is_correct else 0
        try:
            with transaction.atomic():
                BonusAnswer.objects.create(
                    student=student, question=question, is_correct=choice.is_correct, coins=amount
                )
        except IntegrityError:
            raise BonusError(_("Bu savolga allaqachon javob bergansiz.")) from None
        now = timezone.now()
        if amount:
            CoinTransaction.objects.create(student=student, amount=amount, reason=REASON.format(topic=topic)[:120])
        else:
            engagement.add_mistake(student.pk, question.pk, now)
        engagement.record_activity(student, now)
    return BonusResult(correct=choice.is_correct, coins=amount, topic=topic)


def summary(student: Student) -> dict:
    """Profil uchun: bugun, qolgan savollar, jami to'g'ri va yig'ilgan quvvat."""
    done = student.bonus_answers.aggregate(
        n=Count("pk"), correct=Count("pk", filter=Q(is_correct=True)), coins=Sum("coins")
    )
    today = answered_today(student)
    return {
        "today": today,
        "limit": DAILY_LIMIT,
        "left_today": max(0, DAILY_LIMIT - today),
        "remaining": questions(student).count(),
        "answered": done["n"],
        "correct": done["correct"],
        "coins": done["coins"] or 0,
    }


def topics(student: Student) -> list[dict]:
    """Javob berilmagan savollari bor o'tilgan mavzular (savollar soni va mukofoti bilan)."""
    rows = (
        questions(student)
        .values("quiz__topic_id", "quiz__topic__title", "quiz__topic__title_ru", "quiz__bonus_quvvat")
        .annotate(n=Count("pk"))
        .order_by("quiz__topic__module__order", "quiz__topic__order")
    )
    ru = get_language() == QuizLanguage.RU
    return [
        {
            "topic_id": r["quiz__topic_id"],
            "title": (ru and r["quiz__topic__title_ru"]) or r["quiz__topic__title"],
            "bonus": r["quiz__bonus_quvvat"],
            "n": r["n"],
        }
        for r in rows
    ]
