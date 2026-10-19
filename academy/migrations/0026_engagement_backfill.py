"""Boshlang'ich sovg'alar; eski testlardan faol kunlar (streak) va xatolar ro'yxatini tiklash.

O'tmish uchun coin berilmaydi (faqat ro'yxatlar to'ldiriladi).
"""

from django.db import migrations
from django.utils import timezone

REWARDS = [
    ("Uyga vazifadan bir marta ozod bo‘lish", "Ustoz bilan kelishilgan bitta uyga vazifa", 50, 1),
    ("Sertifikatga «A’lochi» belgisi", "Kurs yakunidagi sertifikatda", 300, 2),
]


def forwards(apps, schema_editor):
    Reward = apps.get_model("academy", "Reward")
    QuizAttempt = apps.get_model("academy", "QuizAttempt")
    Question = apps.get_model("academy", "Question")
    Mistake = apps.get_model("academy", "Mistake")
    DailyActivity = apps.get_model("academy", "DailyActivity")

    if not Reward.objects.exists():
        Reward.objects.bulk_create(
            Reward(title=t, description=d, cost=c, order=o) for t, d, c, o in REWARDS
        )

    questions = set(Question.objects.values_list("pk", flat=True))
    days, state = set(), {}  # (o'quvchi, savol) -> [streak, xato soni, oxirgi xato, yopilgan]
    attempts = QuizAttempt.objects.filter(status="finished").exclude(finished_at=None).order_by("finished_at")
    for a in attempts.iterator():
        days.add((a.student_id, timezone.localtime(a.finished_at).date()))
        for item in a.snapshot or []:
            qid = item.get("id")
            if item.get("missing") or qid not in questions:
                continue
            key = (a.student_id, qid)
            if not item.get("is_correct"):
                prev = state.get(key)
                state[key] = [0, (prev[1] + 1) if prev else 1, a.finished_at, None]
            elif key in state and state[key][3] is None:
                state[key][0] += 1
                if state[key][0] >= 3:
                    state[key][3] = a.finished_at
    DailyActivity.objects.bulk_create(
        [DailyActivity(student_id=s, day=d) for s, d in days], ignore_conflicts=True
    )
    Mistake.objects.bulk_create(
        [
            Mistake(
                student_id=s,
                question_id=q,
                streak=v[0],
                wrong_count=v[1],
                last_wrong_at=v[2],
                resolved_at=v[3],
            )
            for (s, q), v in state.items()
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0025_engagement"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
