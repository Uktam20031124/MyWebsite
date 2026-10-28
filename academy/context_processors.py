from django.utils import timezone

from .models import Group, Lesson, Purchase, QuizAttempt, Registration, Student, TestRequest, Topic, warning_attempts
from .teachers import is_teacher, permissions_of, scope


def nav_counts(request):
    user = request.user
    if not user.is_authenticated:
        return {}
    teacher = is_teacher(user)
    sections = permissions_of(user)
    weekday = str(timezone.localdate().weekday())
    # O'qituvchi — faqat o'z guruhlari bo'yicha va faqat ruxsat etilgan bo'limlar hisoblanadi.
    groups = scope(user, Group.objects.filter(status=Group.Status.ACTIVE), "teacher")

    def count(key, qs, path="group__teacher"):
        return scope(user, qs, path).count() if key in sections else 0

    student_path = "student__group__teacher"
    return {
        "is_teacher": teacher,
        "teacher_sections": sections if teacher else set(),
        # "O'quv markazi" menyusidagi bo'limlar (Dars jadvali — o'qituvchi menyusida alohida).
        "teacher_center": sections - {"timetable"} if teacher else set(),
        "nav_groups": groups.count() if "groups" in sections else 0,
        "nav_students": count("students", Student.objects.filter(status=Student.Status.ACTIVE)),
        "nav_topics": Topic.objects.filter(is_active=True).count() if "topics" in sections else 0,
        "nav_lessons": count("lessons", Lesson.objects.filter(status=Lesson.Status.PLANNED)),
        # "days" — bir xonali raqamlar ro'yxati, shuning uchun __contains aniq ishlaydi.
        "nav_today": 0 if teacher else groups.filter(days__contains=weekday).exclude(starts_at=None).count(),
        "nav_quiz_open": count(
            "tests", QuizAttempt.objects.exclude(status=QuizAttempt.Status.FINISHED), student_path
        ),
        # Javoblarni ko'rish + profilga kirish + test so'rovlari + mukofot so'rovlari.
        "nav_review_requests": count(
            "requests", QuizAttempt.objects.filter(reveal=QuizAttempt.Reveal.REQUESTED), student_path
        )
        + count("requests", Student.objects.filter(profile_requested_at__isnull=False))
        + count("requests", TestRequest.objects.filter(status=TestRequest.Status.PENDING), student_path)
        + count("requests", Purchase.objects.filter(status=Purchase.Status.PENDING), student_path),
        # Ogohlantirishli (oynadan chiqqan / nusxalagan), ustoz hali ko'rib chiqmagan testlar.
        "nav_warnings": count("warnings", warning_attempts().filter(warning_checked_at__isnull=True), student_path),
        "nav_registrations": count(
            "registrations", Registration.objects.filter(status=Registration.Status.PENDING), "link__group__teacher"
        ),
    }
