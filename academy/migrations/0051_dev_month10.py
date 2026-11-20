"""Dasturchi 10-oy (WB13–WB24, EduCenter Django sayti): "Dars kodi" va testlar (UZ/RU). Mavzular 0043 da yaratilgan; testlar faqat bo'sh mavzuga."""

from django.db import migrations

KEYS = {f"WB{n:02}" for n in range(13, 25)}


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
        ("academy", "0050_dev_month9"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
