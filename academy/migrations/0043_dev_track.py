"""Minar Dasturchi (3–11-oylar): 9 bo'lim, 108 mavzu, testlar (UZ/RU) va "Dars kodi" (``Topic.lesson``).

Faqat shu yo'nalishga tegishli yozuvlar yaratiladi yoki yangilanadi; boshqa bo'lim va mavzularga tegilmaydi.
Bo'sh (yangi, test) bazada katalogni ``load_school`` yuklaydi — migratsiya faqat ish bazasini to'ldiradi.
Qayta ishga tushirish xavfsiz: testlar faqat bo'sh mavzuga yoziladi.
"""

from django.db import migrations, models

MODULE_ORDER_FROM = 300  # Starter, Python, AI va IQ bo'limlaridan keyin


def forwards(apps, schema_editor):
    from academy.lessons import seed_lessons
    from academy.quiz_bank import bank_titles_ru, seed_quizzes, seed_translations
    from academy.school_data.dev import MODULES, TRACK

    Module = apps.get_model("academy", "Module")
    Topic = apps.get_model("academy", "Topic")
    if not Module.objects.exists():
        return

    titles_ru = bank_titles_ru()
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
            topic.duration_minutes = t.minutes
            topic.order = t_index * 10
            topic.is_active = True
            if not topic.title_ru:
                topic.title_ru = titles_ru.get(t.key, "")
            topic.save()

    only = set(TRACK)
    Quiz = apps.get_model("academy", "Quiz")
    Question = apps.get_model("academy", "Question")
    Choice = apps.get_model("academy", "Choice")
    seed_quizzes(Topic, Quiz, Question, Choice, only=only)
    seed_translations(Topic, Question, Choice, only=only)
    seed_lessons(Topic, only=only)


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0042_topic_poster"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="lesson",
            field=models.JSONField(
                blank=True,
                default=dict,
                editable=False,
                help_text="Darsning bir nechta kadri: sxema, kod qadamlari, sinov va yakun.",
                verbose_name="Dars kodi",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
