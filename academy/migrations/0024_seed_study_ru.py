"""Mustahkamlash materialining ruscha tarjimasini mavzularga yozish (faqat bo'shlariga)."""

from django.db import migrations


def forwards(apps, schema_editor):
    from academy.quiz_bank import seed_study

    seed_study(apps.get_model("academy", "Topic"))


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0023_backfill_coins"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
