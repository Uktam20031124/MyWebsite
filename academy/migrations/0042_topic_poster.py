"""Mavzuga dars rasmi (``Topic.poster``) — proyektor uchun 16:9 poster ma'lumoti, katalogdagi hamma mavzu uchun."""

from django.db import migrations, models


def forwards(apps, schema_editor):
    from academy.posters import seed_posters

    seed_posters(apps.get_model("academy", "Topic"))


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0041_homework"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="poster",
            field=models.JSONField(
                blank=True,
                default=dict,
                editable=False,
                help_text="Proyektor uchun 16:9 dars rasmi: ko'rgazma, formulalar va test oldidan savollar.",
                verbose_name="Dars rasmi",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
