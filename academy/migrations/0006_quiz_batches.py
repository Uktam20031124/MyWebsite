"""Test jo'natmalari (QuizBatch): savollar soni va vaqt har bir jo'natmada belgilanadi.

1-qadam: yangi jadval va maydonlar (batch hozircha bo'sh bo'lishi mumkin).
"""

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0005_quizzes'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_count', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Savollar soni')),
                ('time_limit_minutes', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(180)], verbose_name='Vaqt (daq.)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Jo'natilgan")),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz_batches', to='academy.group', verbose_name='Guruh')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quiz_batches', to='academy.lesson', verbose_name='Dars')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='academy.quiz', verbose_name='Test')),
            ],
            options={
                'verbose_name': "Test jo'natmasi",
                'verbose_name_plural': "Test jo'natmalari",
                'ordering': ['-created_at', '-pk'],
            },
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='academy.quizbatch', verbose_name="Jo'natma"),
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='question_ids',
            field=models.JSONField(blank=True, default=list, editable=False, verbose_name='Savollar'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time_limit_minutes',
            field=models.PositiveSmallIntegerField(default=10, help_text="Jo'natishda taklif qilinadigan vaqt. Har bir jo'natmada o'zgartirish mumkin.", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(180)], verbose_name='Vaqt (daq.)'),
        ),
    ]
