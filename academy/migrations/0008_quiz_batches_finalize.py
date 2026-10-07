"""3-qadam: havola endi jo'natmaga tegishli; dars jo'natma orqali bog'lanadi."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0007_quiz_batches_data'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='quizattempt',
            name='uniq_quiz_attempt_lesson_student',
        ),
        migrations.RemoveField(
            model_name='quizattempt',
            name='lesson',
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='academy.quizbatch', verbose_name="Jo'natma"),
        ),
        migrations.AddConstraint(
            model_name='quizattempt',
            constraint=models.UniqueConstraint(fields=('batch', 'student'), name='uniq_quiz_attempt_batch_student'),
        ),
    ]
