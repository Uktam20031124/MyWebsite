from collections import defaultdict
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from .models import Attendance, Group, Lesson, Student, SyllabusItem


def group_progress(group: Group) -> dict:
    items = list(group.syllabus.all())
    total = len(items)
    taught = sum(1 for i in items if i.status == SyllabusItem.Status.TAUGHT)
    pct = int(round((taught / total) * 100)) if total else 0
    return {"total": total, "taught": taught, "percent": pct}


def student_attendance_rate(student: Student) -> dict:
    qs = student.attendances.select_related("lesson")
    total = qs.count()
    if not total:
        return {"total": 0, "present": 0, "percent": 0}
    present = qs.filter(
        status__in=[Attendance.Status.PRESENT, Attendance.Status.LATE]
    ).count()
    return {
        "total": total,
        "present": present,
        "percent": int(round((present / total) * 100)),
    }


def lesson_attendance_summary(lesson: Lesson) -> dict:
    rows = lesson.attendances.all()
    counts = defaultdict(int)
    for row in rows:
        counts[row.status] += 1
    return {
        "present": counts[Attendance.Status.PRESENT],
        "late": counts[Attendance.Status.LATE],
        "absent": counts[Attendance.Status.ABSENT],
        "excused": counts[Attendance.Status.EXCUSED],
        "marked": rows.count(),
    }


def dashboard_payload():
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)

    groups = Group.objects.filter(status=Group.Status.ACTIVE).prefetch_related(
        "syllabus", "students"
    )
    progress_rows = []
    for g in groups:
        p = group_progress(g)
        p["group"] = g
        p["student_count"] = g.students.filter(status=Student.Status.ACTIVE).count()
        progress_rows.append(p)

    today_lessons = (
        Lesson.objects.filter(held_on=today)
        .select_related("group", "topic")
        .prefetch_related("attendances")
    )
    upcoming = (
        Lesson.objects.filter(held_on__gt=today, status=Lesson.Status.PLANNED)
        .select_related("group", "topic")[:6]
    )
    recent = (
        Lesson.objects.filter(status=Lesson.Status.COMPLETED)
        .select_related("group", "topic")[:6]
    )

    week_att = Attendance.objects.filter(lesson__held_on__gte=week_ago)
    week_total = week_att.count()
    week_present = week_att.filter(
        status__in=[Attendance.Status.PRESENT, Attendance.Status.LATE]
    ).count()

    missing = (
        Student.objects.filter(status=Student.Status.ACTIVE)
        .annotate(
            absents=Count(
                "attendances",
                filter=Q(
                    attendances__status=Attendance.Status.ABSENT,
                    attendances__lesson__held_on__gte=week_ago,
                ),
            )
        )
        .filter(absents__gte=2)
        .select_related("group")[:8]
    )

    return {
        "today": today,
        "progress_rows": progress_rows,
        "today_lessons": today_lessons,
        "upcoming": upcoming,
        "recent": recent,
        "stats": {
            "groups": groups.count(),
            "students": Student.objects.filter(status=Student.Status.ACTIVE).count(),
            "lessons_week": Lesson.objects.filter(held_on__gte=week_ago).count(),
            "attendance_pct": int(round((week_present / week_total) * 100))
            if week_total
            else 0,
        },
        "missing": missing,
    }
