"""Dasturchi 5-oy (DP25–DP36): "Dars kodi" va testlar (UZ/RU). Mavzular 0043 da yaratilgan; testlar faqat bo'sh mavzuga."""

from django.db import migrations

KEYS = {f"DP{n:02}" for n in range(25, 37)}


def forwards(apps, schema_editor):
    from academy.lessons import seed_lessons
    from academy.quiz_bank import seed_quizzes, seed_translations

    Topic = apps.get_model("academy", "Topic")
    Quiz = apps.get_model("academy", "Quiz")
    Question = apps.get_model("academy", "Question")
    Choice = apps.get_model("academy", "Choice")
    seed_quizzes(Topic, Quiz, Question, Choice, only=KEYS)
    seed_translations(Topic, Question, Choice, only=KEYS)
    seed_lessons(Topic, only=KEYS)


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0045_dev_month4"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
