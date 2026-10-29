"""O'qituvchilar faoliyati va maoshi: oy bo'yicha darslar, testlar, natijalar, davomat va hisoblangan summa.

Darslar ``Lesson.teacher`` bo'yicha (darsni o'tgan o'qituvchi), test natijalari va davomat —
o'qituvchining hozirgi guruhlari bo'yicha. Maosh = o'tilgan darslar × dars narxi + oylik qat'iy qism.
"""

from dataclasses import dataclass, field
from datetime import date

from django.db.models import Count, Q, Sum
from django.utils import timezone

from .models import Attendance, Group, Lesson, QuizAttempt, QuizBatch, Student, TeacherAccount, TeacherPayout
from .services import percent


def month_start(value: str = "", today: date | None = None) -> date:
    """"2026-10" → 2026-10-01; noto'g'ri yoki bo'sh — joriy oy."""
    today = today or timezone.localdate()
    try:
        year, month = (int(x) for x in value.split("-")[:2])
        return date(year, month, 1)
    except (ValueError, TypeError):
        return today.replace(day=1)


def next_month(day: date) -> date:
    return date(day.year + day.month // 12, day.month % 12 + 1, 1)


def prev_month(day: date) -> date:
    return date(day.year - (day.month == 1), (day.month - 2) % 12 + 1, 1)


@dataclass
class TeacherRow:
    account: TeacherAccount
    groups: list = field(default_factory=list)
    students: int = 0
    lessons: int = 0
    cancelled: int = 0
    planned: int = 0
    tests: int = 0
    results: int = 0  # yakunlangan testlar
    avg_percent: int | None = None
    attendance: int | None = None
    salary: int = 0
    payout: TeacherPayout | None = None

    @property
    def user(self):
        return self.account.user


def teacher_row(account: TeacherAccount, month: date) -> TeacherRow:
    user, end = account.user, next_month(month)
    row = TeacherRow(account, groups=list(Group.objects.filter(teacher=user).exclude(status=Group.Status.ARCHIVED)))
    row.students = Student.objects.filter(group__teacher=user, status=Student.Status.ACTIVE).count()
    lessons = Lesson.objects.filter(teacher=user, held_on__gte=month, held_on__lt=end).aggregate(
        done=Count("pk", filter=Q(status=Lesson.Status.COMPLETED)),
        cancelled=Count("pk", filter=Q(status=Lesson.Status.CANCELLED)),
        planned=Count("pk", filter=Q(status=Lesson.Status.PLANNED)),
    )
    row.lessons, row.cancelled, row.planned = lessons["done"], lessons["cancelled"], lessons["planned"]
    row.tests = QuizBatch.objects.filter(
        sent_by=user, from_profile=False, created_at__date__gte=month, created_at__date__lt=end
    ).count()
    attempts = QuizAttempt.objects.filter(
        student__group__teacher=user,
        status=QuizAttempt.Status.FINISHED,
        finished_at__date__gte=month,
        finished_at__date__lt=end,
        total__gt=0,
    ).aggregate(n=Count("pk"), correct=Sum("correct"), total=Sum("total"))
    row.results = attempts["n"]
    if attempts["total"]:
        row.avg_percent = percent(attempts["correct"] or 0, attempts["total"])
    marks = Attendance.objects.filter(
        lesson__teacher=user, lesson__held_on__gte=month, lesson__held_on__lt=end
    ).aggregate(total=Count("pk"), present=Count("pk", filter=Q(status__in=Attendance.ATTENDED)))
    if marks["total"]:
        row.attendance = percent(marks["present"], marks["total"])
    row.salary = row.lessons * account.lesson_rate + account.monthly_fixed
    row.payout = TeacherPayout.objects.filter(teacher=user, month=month).first()
    return row


def month_report(month: date) -> list[TeacherRow]:
    accounts = (
        TeacherAccount.objects.select_related("user")
        .filter(user__is_superuser=False)
        .order_by("user__first_name", "user__username")
    )
    return [teacher_row(a, month) for a in accounts]


def mark_paid(account: TeacherAccount, month: date) -> TeacherPayout:
    """Shu oy uchun hisoblangan summa to'landi deb belgilanadi (summa — o'sha paytdagi nusxa)."""
    row = teacher_row(account, month)
    payout, _created = TeacherPayout.objects.update_or_create(
        teacher=account.user,
        month=month,
        defaults={"lessons": row.lessons, "amount": row.salary, "paid_at": timezone.now()},
    )
    return payout
