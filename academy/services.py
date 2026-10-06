import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import timedelta

from django.db import transaction
from django.db.models import Avg, Count, Max, Q
from django.utils import timezone

from .models import Attendance, Group, Lesson, Module, Student, SyllabusItem, Topic


def percent(part: int, total: int) -> int:
    return int(round(part / total * 100)) if total else 0


# --- Statistika -------------------------------------------------------------


def groups_with_stats(qs=None):
    """Guruhlar + faol shogirdlar soni va dastur progressi (bitta so'rov)."""
    qs = Group.objects.all() if qs is None else qs
    qs = qs.order_by(*Group._meta.ordering)
    return qs.annotate(
        student_n=Count(
            "students",
            filter=Q(students__status=Student.Status.ACTIVE),
            distinct=True,
        ),
        syllabus_total=Count("syllabus", distinct=True),
        syllabus_taught=Count(
            "syllabus",
            filter=Q(syllabus__status=SyllabusItem.Status.TAUGHT),
            distinct=True,
        ),
    )


def students_with_stats(qs=None):
    """Shogirdlar + davomat hisoblari (N+1 so'rovsiz)."""
    qs = Student.objects.all() if qs is None else qs
    qs = qs.order_by(*Student._meta.ordering)
    return qs.annotate(
        att_total=Count("attendances", distinct=True),
        att_present=Count(
            "attendances",
            filter=Q(attendances__status__in=Attendance.ATTENDED),
            distinct=True,
        ),
    )


def group_progress(group: Group) -> dict:
    counts = group.syllabus.aggregate(
        total=Count("id"),
        taught=Count("id", filter=Q(status=SyllabusItem.Status.TAUGHT)),
    )
    return {**counts, "percent": percent(counts["taught"], counts["total"])}


def student_attendance_rate(student: Student) -> dict:
    counts = student.attendances.aggregate(
        total=Count("id"),
        present=Count("id", filter=Q(status__in=Attendance.ATTENDED)),
        avg_score=Avg("score"),
    )
    avg = counts["avg_score"]
    return {
        **counts,
        "percent": percent(counts["present"], counts["total"]),
        "avg_score": round(avg) if avg is not None else None,
    }


def lesson_attendance_summary(lesson: Lesson) -> dict:
    counts = defaultdict(int)
    for status in lesson.attendances.values_list("status", flat=True):
        counts[status] += 1
    return {
        "present": counts[Attendance.Status.PRESENT],
        "late": counts[Attendance.Status.LATE],
        "absent": counts[Attendance.Status.ABSENT],
        "excused": counts[Attendance.Status.EXCUSED],
        "marked": sum(counts.values()),
    }


def filter_students(params, qs=None):
    """Shogirdlar ro'yxati va CSV eksport uchun umumiy filtr (?group, ?status, ?q)."""
    qs = Student.objects.select_related("group") if qs is None else qs
    try:
        group = int(params.get("group", ""))
    except ValueError:
        group = None
    status = params.get("status", "")
    q = params.get("q", "").strip()
    if group:
        qs = qs.filter(group_id=group)
    if status in Student.Status.values:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q)
            | Q(phone__icontains=q)
            | Q(telegram__icontains=q.lstrip("@"))
        )
    return qs


# Reyting = o'rtacha ball × 0.7 + davomat foizi × 0.3 (ikkalasi ham 0–100).
RATING_SCORE_WEIGHT = 0.7


@dataclass
class JournalCell:
    status: str = ""  # Attendance.Status qiymati; "" — belgilanmagan
    score: int | None = None


@dataclass
class JournalRow:
    student: Student
    cells: list[JournalCell]
    rank: int | None = None

    @property
    def marked(self) -> int:
        return sum(bool(c.status) for c in self.cells)

    @property
    def attended(self) -> int:
        return sum(c.status in Attendance.ATTENDED for c in self.cells)

    @property
    def percent(self) -> int:
        return percent(self.attended, self.marked)

    @property
    def avg_score(self) -> int | None:
        scores = [c.score for c in self.cells if c.score is not None]
        return round(sum(scores) / len(scores)) if scores else None

    @property
    def rating(self) -> int | None:
        if self.avg_score is None:
            return None
        w = RATING_SCORE_WEIGHT
        return round(self.avg_score * w + self.percent * (1 - w))


def rank_rows(rows: list[JournalRow]) -> None:
    """Reyting bo'yicha o'rin (teng reytingga bir xil o'rin: 1, 2, 2, 4)."""
    rated = sorted((r for r in rows if r.rating is not None), key=lambda r: -r.rating)
    for i, row in enumerate(rated):
        same_as_prev = i and row.rating == rated[i - 1].rating
        row.rank = rated[i - 1].rank if same_as_prev else i + 1


def group_journal(group: Group, limit: int | None = None):
    """Guruh jurnali: shogirdlar × darslar (bekor qilinmagan, sana bo'yicha).

    Faqat o'tilgan yoki yo'qlama olingan darslar kiradi. ``limit`` — oxirgi N dars.
    Jami 3 ta so'rov, shogird/dars soniga bog'liq emas. Reyting har doim
    ko'rsatilgan darslar bo'yicha hisoblanadi.
    """
    lessons = list(
        group.lessons.exclude(status=Lesson.Status.CANCELLED)
        .filter(Q(status=Lesson.Status.COMPLETED) | Q(attendances__isnull=False))
        .distinct()
        .select_related("topic")
        .order_by("held_on", "starts_at", "pk")
    )
    if limit:
        lessons = lessons[-limit:]
    marks = {
        (a.student_id, a.lesson_id): JournalCell(a.status, a.score)
        for a in Attendance.objects.filter(lesson__in=lessons).only(
            "student_id", "lesson_id", "status", "score"
        )
    }
    marked_ids = {student_id for student_id, _ in marks}
    students = group.students.filter(
        Q(status=Student.Status.ACTIVE) | Q(pk__in=marked_ids)
    )
    empty = JournalCell()
    rows = [
        JournalRow(
            student=student,
            cells=[marks.get((student.pk, lesson.pk), empty) for lesson in lessons],
        )
        for student in students
    ]
    rank_rows(rows)
    return lessons, rows


def dashboard_payload():
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)
    past_week = Q(held_on__gt=week_ago, held_on__lte=today)

    groups = groups_with_stats(Group.objects.filter(status=Group.Status.ACTIVE))
    progress_rows = [
        {
            "group": g,
            "student_count": g.student_n,
            "total": g.syllabus_total,
            "taught": g.syllabus_taught,
            "percent": percent(g.syllabus_taught, g.syllabus_total),
        }
        for g in groups
    ]

    week_att = Attendance.objects.filter(
        lesson__held_on__gt=week_ago, lesson__held_on__lte=today
    ).aggregate(
        total=Count("id"),
        present=Count("id", filter=Q(status__in=Attendance.ATTENDED)),
    )

    missing = (
        Student.objects.filter(status=Student.Status.ACTIVE)
        .annotate(
            absents=Count(
                "attendances",
                filter=Q(
                    attendances__status=Attendance.Status.ABSENT,
                    attendances__lesson__held_on__gt=week_ago,
                ),
            )
        )
        .filter(absents__gte=2)
        .select_related("group")
        .order_by("-absents")[:8]
    )

    lessons = Lesson.objects.select_related("group", "topic")
    return {
        "today": today,
        "progress_rows": progress_rows,
        "today_lessons": lessons.filter(held_on=today).order_by("starts_at"),
        "upcoming": lessons.filter(
            held_on__gt=today, status=Lesson.Status.PLANNED
        ).order_by("held_on", "starts_at")[:6],
        "recent": lessons.filter(status=Lesson.Status.COMPLETED)[:6],
        "overdue": lessons.filter(
            held_on__lt=today, status=Lesson.Status.PLANNED
        ).order_by("held_on")[:6],
        "stats": {
            "groups": len(progress_rows),
            "students": Student.objects.filter(status=Student.Status.ACTIVE).count(),
            "lessons_week": Lesson.objects.filter(past_week).count(),
            "attendance_pct": percent(week_att["present"], week_att["total"]),
        },
        "missing": missing,
    }


# --- Mavzular importi -------------------------------------------------------
#
# Format (oddiy matn, bevosita nusxa olib qo'yish uchun):
#
#   # Python asoslari                <- bo'lim (heading)
#   1. Kirish va muhit — VS Code     <- mavzu — tavsif
#   - Sikllar | for, while | 120     <- mavzu | tavsif | daqiqa
#       qo'shimcha izoh              <- surilgan qator tavsifga qo'shiladi
#
# Raqam/belgi (1. 1) - * •) avtomatik olib tashlanadi.

_BULLET = re.compile(r"^\s*(?:\d+[.)]|[-*•–])\s+")
_DASH_SPLIT = re.compile(r"\s+[—–-]\s+")


@dataclass
class ParsedTopic:
    title: str
    description: str = ""
    duration: int | None = None


@dataclass
class ParsedModule:
    title: str  # "" = bo'limsiz
    topics: list[ParsedTopic] = field(default_factory=list)


def parse_topics(text: str) -> list[ParsedModule]:
    modules: list[ParsedModule] = []
    current: ParsedModule | None = None

    for raw in text.splitlines():
        if not raw.strip():
            continue
        line = raw.rstrip()

        if line.lstrip().startswith("#"):
            current = ParsedModule(title=line.lstrip("# \t").strip()[:160])
            modules.append(current)
            continue

        is_continuation = raw[:1] in (" ", "\t") and not _BULLET.match(raw)
        if is_continuation and current and current.topics:
            last = current.topics[-1]
            extra = line.strip()
            last.description = f"{last.description}\n{extra}".strip()
            continue

        if current is None:
            current = ParsedModule(title="")
            modules.append(current)
        current.topics.append(_parse_topic_line(_BULLET.sub("", line).strip()))

    return [m for m in modules if m.topics or m.title]


def _parse_topic_line(line: str) -> ParsedTopic:
    duration = None
    if "|" in line:
        parts = [p.strip() for p in line.split("|")]
        title, desc = parts[0], parts[1] if len(parts) > 1 else ""
        if len(parts) > 2 and parts[2].isdigit():
            duration = int(parts[2])
    else:
        parts = _DASH_SPLIT.split(line, maxsplit=1)
        title, desc = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""
    return ParsedTopic(title=title[:200], description=desc, duration=duration)


@dataclass
class ImportResult:
    modules_created: int = 0
    topics_created: int = 0
    topics_updated: int = 0
    added_to_groups: int = 0
    topics: list[Topic] = field(default_factory=list)


@transaction.atomic
def import_topics(
    modules: list[ParsedModule],
    groups=(),
    default_duration: int = 90,
    update_existing: bool = True,
) -> ImportResult:
    """Parse qilingan mavzularni bazaga yozadi (idempotent: qayta import xavfsiz)."""
    result = ImportResult()
    module_order = (Module.objects.aggregate(m=Max("order"))["m"] or 0)

    for pm in modules:
        module = None
        if pm.title:
            module = Module.objects.filter(title__iexact=pm.title).first()
            if module is None:
                module_order += 10
                module = Module.objects.create(title=pm.title, order=module_order)
                result.modules_created += 1

        siblings = Topic.objects.filter(module=module)
        order = siblings.aggregate(m=Max("order"))["m"] or 0
        for pt in pm.topics:
            topic = siblings.filter(title__iexact=pt.title).first()
            if topic is None:
                order += 10
                topic = Topic.objects.create(
                    module=module,
                    title=pt.title,
                    description=pt.description,
                    duration_minutes=pt.duration or default_duration,
                    order=order,
                )
                result.topics_created += 1
            elif update_existing:
                changed = []
                if pt.description and pt.description != topic.description:
                    topic.description = pt.description
                    changed.append("description")
                if pt.duration and pt.duration != topic.duration_minutes:
                    topic.duration_minutes = pt.duration
                    changed.append("duration_minutes")
                if changed:
                    topic.save(update_fields=changed)
                    result.topics_updated += 1
            result.topics.append(topic)

    for group in groups:
        result.added_to_groups += group.add_topics(result.topics)
    return result


def export_topics() -> str:
    """Katalogni import formatidagi matnga aylantiradi (zaxira / ko'chirish uchun)."""
    # Bo'limsiz mavzular boshida, sarlavhasiz turadi — aks holda qayta importda
    # ular "Bo'limsiz" nomli yangi bo'limga tushib qolardi.
    by_module: dict[Module | None, list[Topic]] = defaultdict(list)
    for t in Topic.objects.select_related("module").order_by("order", "title"):
        by_module[t.module].append(t)
    ordered = sorted(
        by_module, key=lambda m: (m is not None, m.order if m else 0, str(m or ""))
    )

    def field_text(value: str) -> str:
        # "|" import formatida ustun ajratuvchisi — matn ichida qolsa, qayta
        # importda tavsif/davomiylik siljib ketadi.
        return " ".join(value.replace("|", "/").split())

    blocks = []
    for module in ordered:
        lines = [f"# {module.title}"] if module else []
        for n, t in enumerate(by_module[module], start=1):
            lines.append(
                f"{n}. {field_text(t.title)} | {field_text(t.description)} | {t.duration_minutes}"
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n" if blocks else ""
