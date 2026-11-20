"""Dasturchi 11-oy (WB25–WB36, EduCenter: server, integratsiya, yakuniy loyiha): "Dars kodi" va testlar (UZ/RU). Mavzular 0043 da yaratilgan; testlar faqat bo'sh mavzuga."""

from django.db import migrations

# WB24: seed_demo tavsiflari qisqartirildi (ruff E501); WB25–WB36 — yangi darslar.
KEYS = {f"WB{n:02}" for n in range(24, 37)}


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
        ("academy", "0051_dev_month10"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
