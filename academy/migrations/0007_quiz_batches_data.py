"""2-qadam: mavjud test havolalarini jo'natmalarga ko'chirish.

Har bir (dars, test) juftligi — bitta jo'natma; savollar soni — testdagi barcha savollar,
vaqt — testning vaqti (avvalgi xatti-harakat saqlanadi).
"""

from django.db import migrations


def forwards(apps, schema_editor):
    QuizAttempt = apps.get_model("academy", "QuizAttempt")
    QuizBatch = apps.get_model("academy", "QuizBatch")
    Question = apps.get_model("academy", "Question")
    batches = {}
    for attempt in QuizAttempt.objects.select_related("quiz", "lesson").order_by("created_at"):
        key = (attempt.lesson_id, attempt.quiz_id)
        if key not in batches:
            batch = QuizBatch.objects.create(
                quiz_id=attempt.quiz_id,
                lesson_id=attempt.lesson_id,
                group_id=attempt.lesson.group_id,
                question_count=max(1, Question.objects.filter(quiz_id=attempt.quiz_id).count()),
                time_limit_minutes=attempt.quiz.time_limit_minutes,
            )
            # auto_now_add — jo'natma sanasi havolalar yaratilgan sana bo'lsin.
            QuizBatch.objects.filter(pk=batch.pk).update(created_at=attempt.created_at)
            batches[key] = batch.pk
        QuizAttempt.objects.filter(pk=attempt.pk).update(batch_id=batches[key])


def backwards(apps, schema_editor):
    QuizAttempt = apps.get_model("academy", "QuizAttempt")
    for attempt in QuizAttempt.objects.select_related("batch"):
        if attempt.batch and attempt.batch.lesson_id:
            QuizAttempt.objects.filter(pk=attempt.pk).update(lesson_id=attempt.batch.lesson_id)
        else:
            attempt.delete()  # darssiz jo'natmani eski sxemada ifodalab bo'lmaydi


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0006_quiz_batches'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
