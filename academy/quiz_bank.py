"""Tayyor test savollari banki: ``academy/school_data/quizzes_*.py`` → bazadagi mavzular.

``seed_quizzes`` model klasslarini parametr sifatida oladi: data migratsiyada tarixiy
modellar, ``load_school`` buyrug'ida esa haqiqiy modellar beriladi.
"""

from django.db.models import Max

from .quiz_format import Parsed, parse_quiz
from .school_data import all_modules

# Bank ustozning testini "to'ldirmaydigan" chegara: shuncha va undan ko'p savolli test
# ustoz tomonidan tayyorlangan deb hisoblanadi va unga tegilmaydi.
MIN_QUESTIONS = 10
DEFAULT_TIME_LIMIT = 10


def bank_texts() -> dict[str, str]:
    from .school_data.quizzes_python import QUIZZES as PYTHON
    from .school_data.quizzes_starter import QUIZZES as STARTER

    return {**STARTER, **PYTHON}


def bank_entries() -> list[tuple[str, str, str, Parsed]]:
    """[(mavzu kaliti, bo'lim nomi, mavzu nomi, savollar), ...] — katalog tartibida."""
    texts = bank_texts()
    entries = []
    for module in all_modules():
        for topic in module.topics:
            if topic.key in texts:
                parsed, errors = parse_quiz(texts[topic.key])
                if errors:
                    raise ValueError(f"Test banki, {topic.key}: " + "; ".join(errors))
                entries.append((topic.key, module.title, topic.title, parsed))
    return entries


def validate_bank() -> list[str]:
    """Bankdagi xatolar: noma'lum kalit, format xatosi, savollar kamligi, takror savol."""
    keys = {t.key for m in all_modules() for t in m.topics}
    errors = []
    for key, text in bank_texts().items():
        if key not in keys:
            errors.append(f"Test banki: noma'lum mavzu kaliti {key}")
            continue
        parsed, parse_errors = parse_quiz(text)
        errors += [f"Test banki, {key}: {e}" for e in parse_errors]
        if len(parsed) < MIN_QUESTIONS:
            errors.append(f"Test banki, {key}: {len(parsed)} ta savol (kamida {MIN_QUESTIONS})")
        titles = [q for q, _ in parsed]
        if len(set(titles)) != len(titles):
            errors.append(f"Test banki, {key}: savol takrorlangan")
    return errors


def seed_quizzes(Topic, Quiz, Question, Choice) -> tuple[int, int]:
    """Bankdagi savollarni mavzularga yozadi: (yaratilgan testlar, qo'shilgan savollar).

    Test yo'q bo'lsa — yaratiladi; savollari ``MIN_QUESTIONS`` dan kam bo'lsa — bankdagi
    yangi savollar qo'shiladi. Ustoz to'ldirgan testlar va mavjud savollarga tegilmaydi,
    shuning uchun qayta ishga tushirish xavfsiz.
    """
    created = added = 0
    for _key, module_title, topic_title, parsed in bank_entries():
        topic = Topic.objects.filter(
            module__title__iexact=module_title, title__iexact=topic_title
        ).first()
        if topic is None:
            continue
        quiz, is_new = Quiz.objects.get_or_create(
            topic=topic, defaults={"time_limit_minutes": DEFAULT_TIME_LIMIT}
        )
        created += is_new
        questions = Question.objects.filter(quiz=quiz)
        if not is_new and questions.count() >= MIN_QUESTIONS:
            continue
        have = set(questions.values_list("text", flat=True))
        order = questions.aggregate(m=Max("order"))["m"] or 0
        for text, choices in parsed:
            if text in have:
                continue
            order += 1
            question = Question.objects.create(quiz=quiz, text=text, order=order)
            Choice.objects.bulk_create(
                Choice(question=question, text=c, is_correct=ok, order=i)
                for i, (c, ok) in enumerate(choices, start=1)
            )
            added += 1
    return created, added
