"""Tayyor test savollari bankini mavjud mavzularga yozish (har bir mavzuga 12 ta savol).

Ustoz to'ldirgan testlarga tegilmaydi (qarang: ``academy.quiz_bank.seed_quizzes``).
Bo'sh bazada hech narsa qilmaydi — mavzular keyin ``load_school`` bilan yuklanganda
o'sha buyruq testlarni ham yozadi.
"""

from django.db import migrations


def forwards(apps, schema_editor):
    from academy.quiz_bank import seed_quizzes

    seed_quizzes(
        apps.get_model("academy", "Topic"),
        apps.get_model("academy", "Quiz"),
        apps.get_model("academy", "Question"),
        apps.get_model("academy", "Choice"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_quiz_batches_finalize'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
