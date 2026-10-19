"""Mavzularga "Darsni qayta mustahkamlash" materialini yozish (faqat bo'shlariga).

Qarang: ``academy.quiz_bank.seed_study``.
"""

from django.db import migrations


def forwards(apps, schema_editor):
    from academy.quiz_bank import seed_study

    seed_study(apps.get_model("academy", "Topic"))


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0020_student_profile"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
