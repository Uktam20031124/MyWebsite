from .models import Group, Lesson, Student, Topic


def nav_counts(request):
    if not request.user.is_authenticated:
        return {}
    return {
        "nav_groups": Group.objects.filter(status=Group.Status.ACTIVE).count(),
        "nav_students": Student.objects.filter(status=Student.Status.ACTIVE).count(),
        "nav_topics": Topic.objects.filter(is_active=True).count(),
        "nav_lessons": Lesson.objects.filter(status=Lesson.Status.PLANNED).count(),
    }
