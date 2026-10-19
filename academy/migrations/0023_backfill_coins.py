"""Avval yechilgan testlar uchun ham coin berish (har bir test uchun bir marta).

Qoidalar ``academy.coins`` bilan bir xil; qayta ishga tushirilsa takrorlanmaydi
(attempt + sabab bo'yicha takrorlanmas cheklov).
"""

from django.db import migrations


def forwards(apps, schema_editor):
    from academy.coins import PASS_PERCENT, PREVIEW_BONUS, RETAKE_BONUS, score_coins

    QuizAttempt = apps.get_model("academy", "QuizAttempt")
    CoinTransaction = apps.get_model("academy", "CoinTransaction")
    TestRequest = apps.get_model("academy", "TestRequest")
    kinds = dict(TestRequest.objects.exclude(attempt=None).values_list("attempt_id", "kind"))
    done = set(CoinTransaction.objects.values_list("attempt_id", "reason"))
    new = []
    for a in QuizAttempt.objects.filter(status="finished", total__gt=0).iterator():
        percent = round(100 * (a.correct or 0) / a.total)
        rows = [(score_coins(percent), f"Test: {percent}%")]
        if percent >= PASS_PERCENT and kinds.get(a.pk) == "preview":
            rows.append((PREVIEW_BONUS, "Yangi mavzuni oldindan o‘zlashtirdi"))
        if percent >= PASS_PERCENT and kinds.get(a.pk) == "retake":
            rows.append((RETAKE_BONUS, "Mustahkamlab, qayta topshirdi"))
        for amount, reason in rows:
            if (a.pk, reason) not in done:
                new.append(
                    CoinTransaction(
                        student_id=a.student_id, attempt_id=a.pk, amount=amount, reason=reason
                    )
                )
    CoinTransaction.objects.bulk_create(new)
    # Tarix testlar yakunlangan sanada ko'rinsin.
    for c in CoinTransaction.objects.filter(attempt__isnull=False).select_related("attempt"):
        if c.attempt.finished_at and c.created_at > c.attempt.finished_at:
            CoinTransaction.objects.filter(pk=c.pk).update(created_at=c.attempt.finished_at)


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0022_profile_auto_coins"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
