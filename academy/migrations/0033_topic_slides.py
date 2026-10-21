"""Mavzuga dars taqdimoti (``Topic.slides``) va Minar AI Creator kursi uchun tayyor slaydlar.

Slaydlar faqat bo'sh maydonga yoziladi — ustoz tahrirlagan taqdimotga tegilmaydi."""

from django.db import migrations, models


def forwards(apps, schema_editor):
    from academy.quiz_bank import seed_slides
    from academy.school_data.ai import TRACK

    seed_slides(apps.get_model("academy", "Topic"), only=set(TRACK))


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0032_ai_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="slides",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Dars paytida ekranga chiqariladi. Slaydlar orasida --- qatori; # sarlavha slaydi; "
                    "!! katta ibora; :: timer 25 — 25 daqiqalik taymer; qolgani — material formati."
                ),
                verbose_name="Taqdimot slaydlari",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
