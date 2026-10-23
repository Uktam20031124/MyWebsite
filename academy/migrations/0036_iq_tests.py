"""IQ — mantiqiy fikrlash: 1 bo'lim, 5 ta mavzu, testlar (15 savol, UZ/RU) va materiallar.

Mavzular hech bir guruh dasturiga qo'shilmaydi — ustoz testni istalgan guruhga yoki ochiq havola
orqali yuboradi. Faqat IQ kalitlariga tegiladi; qayta ishga tushirish xavfsiz.
"""

from django.db import migrations

MODULE_ORDER = 300  # AI kursidan (200–270) keyin


def forwards(apps, schema_editor):
    from academy.quiz_bank import bank_titles_ru, seed_quizzes, seed_study, seed_translations
    from academy.school_data.iq import MODULES, TIME_LIMIT, TRACK

    Module = apps.get_model("academy", "Module")
    Topic = apps.get_model("academy", "Topic")
    Quiz = apps.get_model("academy", "Quiz")
    Question = apps.get_model("academy", "Question")
    Choice = apps.get_model("academy", "Choice")
    Group = apps.get_model("academy", "Group")

    # Bo'sh (yangi) bazada — ``load_school`` vazifasi.
    if not Group.objects.exists():
        return

    titles_ru = bank_titles_ru()
    for data in MODULES:
        module = Module.objects.filter(title__iexact=data.title).first() or Module(title=data.title)
        module.description = data.description
        module.order = MODULE_ORDER
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
    seed_quizzes(Topic, Quiz, Question, Choice, only=only)
    seed_translations(Topic, Question, Choice, only=only)
    seed_study(Topic, only=only)
    Quiz.objects.filter(topic__module__title__iexact=MODULES[0].title, time_limit_minutes=10).update(
        time_limit_minutes=TIME_LIMIT
    )


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0035_test_warnings"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
