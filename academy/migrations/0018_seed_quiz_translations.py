"""Test banki savollari va mavzu nomlarining ruscha tarjimasini bazaga yozish.

Faqat bankdagi bilan aynan bir xil (ustoz o'zgartirmagan) savollarga yoziladi
(qarang: ``academy.quiz_bank.seed_translations``).
"""

from django.db import migrations


def forwards(apps, schema_editor):
    from academy.quiz_bank import seed_translations

    seed_translations(
        apps.get_model("academy", "Topic"),
        apps.get_model("academy", "Question"),
        apps.get_model("academy", "Choice"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0017_quiz_languages"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
