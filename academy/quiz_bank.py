"""Tayyor test savollari banki: ``academy/school_data/quizzes_*.py`` → bazadagi mavzular.

Ruscha tarjimalar: ``quizzes_*_ru.py`` (savollar) va ``titles_ru.py`` (mavzu nomlari);
``seed_translations`` ularni bazadagi o'zbekcha savollarga matni bo'yicha bog'laydi.

``seed_quizzes`` model klasslarini parametr sifatida oladi: data migratsiyada tarixiy
modellar, ``load_school`` buyrug'ida esa haqiqiy modellar beriladi.
"""

from django.db.models import Max

from .quiz_format import Parsed, parse_quiz, translation_errors
from .school_data import all_modules

# Bank ustozning testini "to'ldirmaydigan" chegara: shuncha va undan ko'p savolli test
# ustoz tomonidan tayyorlangan deb hisoblanadi va unga tegilmaydi.
MIN_QUESTIONS = 10
DEFAULT_TIME_LIMIT = 10


def bank_texts() -> dict[str, str]:
    from .school_data.quizzes_ai import QUIZZES as AI
    from .school_data.quizzes_python import QUIZZES as PYTHON
    from .school_data.quizzes_starter import QUIZZES as STARTER

    return {**STARTER, **PYTHON, **AI}


def bank_texts_ru() -> dict[str, str]:
    from .school_data.quizzes_ai_ru import QUIZZES as AI
    from .school_data.quizzes_python_ru import QUIZZES as PYTHON
    from .school_data.quizzes_starter_ru import QUIZZES as STARTER

    return {**STARTER, **PYTHON, **AI}


def bank_study() -> dict[str, str]:
    from .school_data.study_ai import STUDY as AI
    from .school_data.study_python import STUDY as PYTHON
    from .school_data.study_starter import STUDY as STARTER

    return {**STARTER, **PYTHON, **AI}


def bank_study_ru() -> dict[str, str]:
    from .school_data.study_ai_ru import STUDY as AI
    from .school_data.study_python_ru import STUDY as PYTHON
    from .school_data.study_starter_ru import STUDY as STARTER

    return {**STARTER, **PYTHON, **AI}


def bank_slides() -> dict[str, str]:
    from .school_data.slides_ai import SLIDES as AI

    return dict(AI)


def bank_titles_ru() -> dict[str, str]:
    from .school_data.titles_ru import TITLES

    return TITLES


def bank_entries(only=None) -> list[tuple[str, str, str, Parsed]]:
    """[(mavzu kaliti, bo'lim nomi, mavzu nomi, savollar), ...] — katalog tartibida.
    ``only`` — faqat shu mavzu kalitlari (bo'sh — hammasi)."""
    texts = bank_texts()
    entries = []
    for module in all_modules():
        for topic in module.topics:
            if topic.key in texts and (only is None or topic.key in only):
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
    for key, text in bank_texts_ru().items():
        if key not in bank_texts():
            errors.append(f"Ruscha bank: noma'lum mavzu kaliti {key}")
            continue
        translated, parse_errors = parse_quiz(text)
        errors += [f"Ruscha bank, {key}: {e}" for e in parse_errors]
        if not parse_errors:
            original = parse_quiz(bank_texts()[key])[0]
            errors += [f"Ruscha bank, {key}: {e}" for e in translation_errors(original, translated)]
    errors += [f"Ruscha nom: noma'lum mavzu kaliti {k}" for k in set(bank_titles_ru()) - keys]
    errors += [f"Mustahkamlash materiali: noma'lum mavzu kaliti {k}" for k in set(bank_study()) - keys]
    errors += [f"Ruscha material: o'zbekchasi yo'q — {k}" for k in set(bank_study_ru()) - set(bank_study())]
    return errors


def seed_quizzes(Topic, Quiz, Question, Choice, only=None) -> tuple[int, int]:
    """Bankdagi savollarni mavzularga yozadi: (yaratilgan testlar, qo'shilgan savollar).

    Test yo'q bo'lsa — yaratiladi; savollari ``MIN_QUESTIONS`` dan kam bo'lsa — bankdagi
    yangi savollar qo'shiladi. Ustoz to'ldirgan testlar va mavjud savollarga tegilmaydi,
    shuning uchun qayta ishga tushirish xavfsiz.
    """
    created = added = 0
    for _key, module_title, topic_title, parsed in bank_entries(only):
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


def seed_translations(Topic, Question, Choice, only=None) -> tuple[int, int]:
    """Ruscha tarjimalarni bazaga yozadi: (nomi tarjima qilingan mavzular, savollar).

    Savol o'zbekcha matni va variantlari bankdagisi bilan aynan bir xil bo'lsa — tarjima
    yoziladi (variantlar matni bo'yicha moslanadi). Ustoz tahrirlagan savollarga va
    ustoz kiritgan tarjimalarga tegilmaydi, shuning uchun qayta ishga tushirish xavfsiz.
    """
    texts_ru, titles_ru = bank_texts_ru(), bank_titles_ru()
    # (o'zbekcha savol, variantlar to'plami) -> (ruscha matn, {o'zbekcha variant: ruscha})
    # Variantlar ham kalitda: turli mavzularda bir xil savol matni uchrashi mumkin.
    by_text = {}
    for key, text in bank_texts().items():
        if key not in texts_ru or (only is not None and key not in only):
            continue
        original, translated = parse_quiz(text)[0], parse_quiz(texts_ru[key])[0]
        for (uz_q, uz_choices), (ru_q, ru_choices) in zip(original, translated, strict=True):
            by_text[(uz_q, frozenset(c for c, _ in uz_choices))] = (
                ru_q,
                {uz: ru for (uz, _), (ru, _) in zip(uz_choices, ru_choices, strict=True)},
            )

    topics = 0
    for _key, module_title, topic_title, _parsed in bank_entries(only):
        title_ru = titles_ru.get(_key)
        if title_ru:
            topics += Topic.objects.filter(
                module__title__iexact=module_title, title__iexact=topic_title, title_ru=""
            ).update(title_ru=title_ru)

    questions = 0
    for q in Question.objects.filter(text_ru="", text__in={text for text, _ in by_text}):
        choices = list(Choice.objects.filter(question=q))
        found = by_text.get((q.text, frozenset(c.text for c in choices)))
        if found is None:
            continue  # ustoz variantlarni o'zgartirgan — tarjima mos emas
        ru_text, choice_map = found
        q.text_ru = "" if ru_text == q.text else ru_text
        q.save(update_fields=["text_ru"])
        for c in choices:
            ru = choice_map[c.text]
            if not c.text_ru and ru != c.text:
                c.text_ru = ru
                c.save(update_fields=["text_ru"])
        questions += bool(q.text_ru)
    return topics, questions


def seed_study(Topic, only=None) -> int:
    """"Darsni qayta mustahkamlash" materialini (o'zbekcha va ruscha) mavzularga yozadi —
    faqat bo'shlariga (ustoz yozgan yoki tahrirlagan materialga tegilmaydi).
    Natija: o'zbekcha material yozilgan mavzular soni."""
    texts, texts_ru = bank_study(), bank_study_ru()
    # Eski migratsiyalardagi (tarixiy) modelda study_ru maydoni hali yo'q.
    if not any(f.name == "study_ru" for f in Topic._meta.get_fields()):
        texts_ru = {}
    filled = 0
    for module in all_modules():
        for t in module.topics:
            if only is not None and t.key not in only:
                continue
            same = {"module__title__iexact": module.title, "title__iexact": t.title}
            if texts.get(t.key):
                filled += Topic.objects.filter(study="", **same).update(study=texts[t.key].strip())
            if texts_ru.get(t.key):
                Topic.objects.filter(study_ru="", **same).update(study_ru=texts_ru[t.key].strip())
    return filled


def seed_slides(Topic, only=None) -> int:
    """Dars taqdimotlarini mavzularga yozadi — faqat bo'shlariga (ustoz tahrirlagan slaydlarga
    tegilmaydi). Natija: taqdimot yozilgan mavzular soni."""
    if not any(f.name == "slides" for f in Topic._meta.get_fields()):
        return 0
    texts = bank_slides()
    filled = 0
    for module in all_modules():
        for t in module.topics:
            if t.key not in texts or (only is not None and t.key not in only):
                continue
            same = {"module__title__iexact": module.title, "title__iexact": t.title}
            filled += Topic.objects.filter(slides="", **same).update(slides=texts[t.key])
    return filled
