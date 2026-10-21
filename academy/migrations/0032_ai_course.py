"""Minar AI Creator kursi: 8 bo'lim, 24 mavzu, testlar (UZ/RU), materiallar va "AI 00-1" guruhi dasturi.

Faqat AI kursiga tegishli yozuvlar yaratiladi; boshqa bo'lim, mavzu va guruhlarga tegilmaydi.
Qayta ishga tushirish xavfsiz: mavjud mavzular yangilanadi, testlar va materiallar faqat bo'sh
joyga yoziladi, guruh dasturidagi mavjud mavzularning holati o'zgarmaydi.
"""

from django.db import migrations
from django.db.models import Max

GROUP_CODE = "AI 00-1"
MODULE_ORDER_FROM = 200  # Starter (10–40) va Python (50–100) bo'limlaridan keyin


def forwards(apps, schema_editor):
    from academy.quiz_bank import bank_titles_ru, seed_quizzes, seed_study, seed_translations
    from academy.school_data.ai import MODULES, TRACK

    Module = apps.get_model("academy", "Module")
    Topic = apps.get_model("academy", "Topic")
    Quiz = apps.get_model("academy", "Quiz")
    Question = apps.get_model("academy", "Question")
    Choice = apps.get_model("academy", "Choice")
    Group = apps.get_model("academy", "Group")
    SyllabusItem = apps.get_model("academy", "SyllabusItem")

    # Kurs mavjud "AI 00-1" guruhi uchun yuklanadi. Yangi (bo'sh) bazada — ``load_school`` vazifasi.
    group = Group.objects.filter(code__iexact=GROUP_CODE).first()
    if group is None:
        return

    titles_ru = bank_titles_ru()
    topics = {}
    for m_index, data in enumerate(MODULES):
        module = Module.objects.filter(title__iexact=data.title).first() or Module(title=data.title)
        module.description = data.description
        module.order = MODULE_ORDER_FROM + m_index * 10
        module.save()
        for t_index, t in enumerate(data.topics, start=1):
            topic = Topic.objects.filter(module=module, title__iexact=t.title).first() or Topic(
                module=module, title=t.title
            )
            topic.description = t.description
            topic.homework = t.homework
            topic.resources = t.resources
            topic.duration_minutes = t.minutes
            topic.order = t_index * 10
            topic.is_active = True
            if not topic.title_ru:
                topic.title_ru = titles_ru.get(t.key, "")
            topic.save()
            topics[t.key] = topic

    only = set(TRACK)
    seed_quizzes(Topic, Quiz, Question, Choice, only=only)
    seed_translations(Topic, Question, Choice, only=only)
    seed_study(Topic, only=only)

    order = SyllabusItem.objects.filter(group=group).aggregate(m=Max("order"))["m"] or 0
    for key in TRACK:
        _item, created = SyllabusItem.objects.get_or_create(
            group=group, topic=topics[key], defaults={"order": order + 1, "status": "planned"}
        )
        order += created


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0031_topic_unlock"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
