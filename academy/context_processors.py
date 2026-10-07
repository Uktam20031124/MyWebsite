from django.utils import timezone

from .models import Group, Lesson, QuizAttempt, Student, Topic


def nav_counts(request):
    if not request.user.is_authenticated:
        return {}
    weekday = str(timezone.localdate().weekday())
    today_groups = Group.objects.filter(
        status=Group.Status.ACTIVE, days__contains=weekday
    ).exclude(starts_at=None)
    return {
        "nav_groups": Group.objects.filter(status=Group.Status.ACTIVE).count(),
        "nav_students": Student.objects.filter(status=Student.Status.ACTIVE).count(),
        "nav_topics": Topic.objects.filter(is_active=True).count(),
        "nav_lessons": Lesson.objects.filter(status=Lesson.Status.PLANNED).count(),
        # "days" — bir xonali raqamlar ro'yxati, shuning uchun __contains aniq ishlaydi.
        "nav_today": today_groups.count(),
        "nav_quiz_open": QuizAttempt.objects.exclude(
            status=QuizAttempt.Status.FINISHED
        ).count(),
    }
