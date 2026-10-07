import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

from django.db import transaction
from django.db.models import Avg, Count, Max, Q, Sum
from django.utils import timezone

from .models import (
    Attendance,
    Group,
    Lesson,
    Module,
    Quiz,
    QuizAttempt,
    QuizBatch,
    Student,
    SyllabusItem,
    Topic,
)

# Test formati modellarga bog'liq emas (data migratsiyada ham ishlatiladi); qayta eksport.
from .quiz_format import QUIZ_FORMAT_HELP, parse_quiz  # noqa: F401


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


# --- Jadval -----------------------------------------------------------------


@dataclass
class Session:
    """Jadval bo'yicha bitta dars vaqti. Bazada dars yozuvi bo'lmasligi ham mumkin."""

    group: Group
    day: date
    starts_at: time
    ends_at: time | None
    lesson: Lesson | None = None
    topic: Topic | None = None  # dars mavzusi yoki dastur bo'yicha navbatdagisi

    @property
    def is_today(self) -> bool:
        return self.day == timezone.localdate()

    @property
    def state(self) -> str:
        """done | cancelled | live | missed | upcoming."""
        if self.lesson and self.lesson.status == Lesson.Status.COMPLETED:
            return "done"
        if self.lesson and self.lesson.status == Lesson.Status.CANCELLED:
            return "cancelled"
        now = timezone.localtime()
        start = datetime.combine(self.day, self.starts_at, now.tzinfo)
        end = datetime.combine(self.day, self.ends_at or self.starts_at, now.tzinfo)
        if start <= now <= end:
            return "live"
        return "missed" if end < now else "upcoming"

    @property
    def duration_minutes(self) -> int:
        if not self.ends_at:
            return 60
        delta = datetime.combine(self.day, self.ends_at) - datetime.combine(
            self.day, self.starts_at
        )
        return max(15, int(delta.total_seconds() // 60))


def timetable_groups(qs=None) -> list[Group]:
    """Jadvali tuzilgan faol guruhlar (kunlar + boshlanish vaqti)."""
    qs = Group.objects.filter(status=Group.Status.ACTIVE) if qs is None else qs
    return [g for g in qs.exclude(days="").exclude(starts_at=None) if g.has_timetable]


def sessions_between(start: date, end: date, groups: list[Group] | None = None) -> list[Session]:
    """[start, end] oralig'idagi jadval darslari, sana va vaqt tartibida.

    Yozilgan dars bo'lsa — o'sha dars va uning mavzusi. Bugundan keyingi
    yozilmagan darslarga guruh dasturidagi navbatdagi mavzular ketma-ket
    taqsimlanadi (rejadagi darslarga biriktirilgan mavzular o'tkazib yuboriladi).
    Guruhlar sonidan qat'i nazar 2 ta so'rov.
    """
    groups = timetable_groups() if groups is None else groups
    if not groups or end < start:
        return []
    today = timezone.localdate()
    # Kelajakdagi oraliq uchun ham mavzular bugundan boshlab taqsimlanadi.
    walk_from = min(start, today) if start > today else start

    lessons: dict[tuple[int, date], Lesson] = {}
    for lesson in (
        Lesson.objects.filter(group__in=groups, held_on__range=(walk_from, end))
        .select_related("topic")
        .order_by("held_on", "starts_at", "pk")
    ):
        key = (lesson.group_id, lesson.held_on)
        # Bekor qilinmagan dars bekor qilinganidan ustun.
        if key not in lessons or lessons[key].status == Lesson.Status.CANCELLED:
            lessons[key] = lesson

    reserved = {
        (lesson.group_id, lesson.topic_id)
        for lesson in lessons.values()
        if lesson.held_on >= today and lesson.topic_id
    }
    queues: dict[int, deque[Topic]] = defaultdict(deque)
    for item in (
        SyllabusItem.objects.filter(group__in=groups, status=SyllabusItem.Status.PLANNED)
        .select_related("topic")
        .order_by("group_id", "order", "id")
    ):
        if (item.group_id, item.topic_id) not in reserved:
            queues[item.group_id].append(item.topic)

    ordered = sorted(groups, key=lambda g: (g.starts_at, g.name))
    sessions = []
    day = walk_from
    while day <= end:
        for group in ordered:
            if not group.meets_on(day):
                continue
            lesson = lessons.get((group.pk, day))
            topic = lesson.topic if lesson else None
            if lesson is None and day >= today and queues[group.pk]:
                topic = queues[group.pk].popleft()
            if day >= start:
                sessions.append(
                    Session(group, day, group.starts_at, group.ends_at, lesson, topic)
                )
        day += timedelta(days=1)
    return sessions


def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def week_timetable(monday: date) -> dict:
    """Haftalik kalendar: 7 ustun, soatlar shkalasi va har bir dars blokining o'rni (%)."""
    sessions = sessions_between(monday, monday + timedelta(days=6))
    if sessions:
        first = min(s.starts_at.hour for s in sessions) - 1
        ends = [s.ends_at or s.starts_at for s in sessions]
        last = max(t.hour + (1 if t.minute else 0) for t in ends) + 1
        first, last = max(0, first), min(24, max(last, first + 5))
    else:
        first, last = 9, 18
    span = (last - first) * 60

    def offset(t: time) -> float:
        return round((t.hour * 60 + t.minute - first * 60) / span * 100, 3)

    today = timezone.localdate()
    days = []
    for n in range(7):
        day = monday + timedelta(days=n)
        days.append(
            {
                "date": day,
                "is_today": day == today,
                "items": [
                    {
                        "session": s,
                        "top": offset(s.starts_at),
                        "height": round(s.duration_minutes / span * 100, 3),
                    }
                    for s in sessions
                    if s.day == day
                ],
            }
        )
    now = timezone.localtime()
    in_week = monday <= today <= monday + timedelta(days=6)
    return {
        "days": days,
        "hours": [time(h) for h in range(first, last)],
        "now_top": offset(now.time()) if in_week and first <= now.hour < last else None,
        "monday": monday,
        "prev": monday - timedelta(days=7),
        "next": monday + timedelta(days=7),
        "sessions": sessions,
    }


@transaction.atomic
def start_session(group: Group, day: date | None = None) -> tuple[Lesson, bool]:
    """Jadvaldagi darsni boshlash: shu kungi darsni topadi yoki dastur bo'yicha
    navbatdagi mavzu bilan yaratadi. Natija: (dars, yangi yaratildimi)."""
    day = day or timezone.localdate()
    lesson = (
        group.lessons.filter(held_on=day)
        .exclude(status=Lesson.Status.CANCELLED)
        .order_by("starts_at", "pk")
        .first()
    )
    if lesson:
        return lesson, False
    item = group.next_syllabus_item()
    topic = item.topic if item else None
    lesson = Lesson.objects.create(
        group=group,
        topic=topic,
        held_on=day,
        starts_at=group.starts_at,
        homework=topic.homework if topic else "",
    )
    return lesson, True


# --- Tahlil -----------------------------------------------------------------


def attendance_trend(weeks: int = 8) -> list[dict]:
    """Oxirgi N hafta davomati, eskisidan: [{"week", "total", "percent"}].

    Dars bo'lmagan haftada ``percent`` — None (grafikda uzilish, 0% emas).
    """
    today = timezone.localdate()
    first = week_start(today) - timedelta(weeks=weeks - 1)
    buckets = {first + timedelta(weeks=i): [0, 0] for i in range(weeks)}
    for held_on, status in Attendance.objects.filter(
        lesson__held_on__gte=first, lesson__held_on__lte=today
    ).values_list("lesson__held_on", "status"):
        bucket = buckets[week_start(held_on)]
        bucket[0] += 1
        bucket[1] += status in Attendance.ATTENDED
    return [
        {"week": week, "total": total, "percent": percent(present, total) if total else None}
        for week, (total, present) in buckets.items()
    ]


def rating(avg_score: float | None, attendance_pct: int) -> int | None:
    """Jurnaldagi reyting bilan bir xil formula."""
    if avg_score is None:
        return None
    w = RATING_SCORE_WEIGHT
    return round(avg_score * w + attendance_pct * (1 - w))


def student_insights(top: int = 5, risk: int = 6) -> dict:
    """Faol shogirdlar: reyting yetakchilari va e'tibor talab qiladiganlar (bitta so'rov)."""
    students = list(
        students_with_stats(Student.objects.filter(status=Student.Status.ACTIVE))
        .select_related("group")
        .annotate(score_avg=Avg("attendances__score"))
    )
    for s in students:
        s.att_pct = percent(s.att_present, s.att_total)
        s.rating = rating(s.score_avg, s.att_pct) if s.att_total else None
        s.score_avg = round(s.score_avg) if s.score_avg is not None else None
    leaders = sorted((s for s in students if s.rating is not None), key=lambda s: -s.rating)
    at_risk = sorted(
        (
            s
            for s in students
            if s.att_total >= 2
            and (s.att_pct < 70 or (s.score_avg is not None and s.score_avg < 60))
        ),
        key=lambda s: (s.att_pct, s.score_avg or 0),
    )
    return {"leaders": leaders[:top], "at_risk": at_risk[:risk]}


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

    trend = attendance_trend()
    this_week, last_week = trend[-1]["percent"], trend[-2]["percent"]
    scheduled = timetable_groups()
    week = sessions_between(today, today + timedelta(days=6), scheduled)
    today_sessions = [s for s in week if s.day == today]

    lessons = Lesson.objects.select_related("group", "topic")
    return {
        "today": today,
        "progress_rows": progress_rows,
        "today_sessions": today_sessions,
        "next_sessions": [s for s in week if s.day > today][:6],
        # Jadvaldan tashqari (qo'shimcha) bugungi darslar.
        "today_lessons": lessons.filter(held_on=today)
        .exclude(group__in=[s.group for s in today_sessions])
        .order_by("starts_at"),
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
            "attendance_delta": (
                this_week - last_week
                if this_week is not None and last_week is not None
                else None
            ),
            "sessions_week": len(week),
            "syllabus_pct": percent(
                sum(r["taught"] for r in progress_rows),
                sum(r["total"] for r in progress_rows),
            ),
        },
        "trend": trend,
        "trend_values": [t["percent"] for t in trend],
        "insights": student_insights(),
        "missing": missing,
        "has_timetable": bool(scheduled),
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


# --- Testlar ----------------------------------------------------------------


def create_quiz_batch(
    quiz: Quiz,
    students,
    question_count: int,
    time_limit_minutes: int,
    lesson: Lesson | None = None,
) -> QuizBatch:
    """Tanlangan shogirdlarga bir martalik havolalar bilan test jo'natmasi yaratadi.

    Savollar soni bankdagidan oshmaydi. Guruh — dars guruhi yoki (hamma shogird bitta
    guruhdan bo'lsa) o'sha guruh: jo'natmalarni guruh bo'yicha ko'rish uchun.
    """
    students = list(students)
    group_ids = {s.group_id for s in students}
    if lesson is not None:
        group_id = lesson.group_id
    else:
        group_id = group_ids.pop() if len(group_ids) == 1 else None
    with transaction.atomic():
        batch = QuizBatch.objects.create(
            quiz=quiz,
            lesson=lesson,
            group_id=group_id,
            question_count=min(question_count, quiz.questions.count()),
            time_limit_minutes=time_limit_minutes,
        )
        QuizAttempt.objects.bulk_create(
            QuizAttempt(batch=batch, quiz=quiz, student=s) for s in students
        )
    return batch


def annotate_batches(qs):
    """Jo'natmalarga havolalar soni, yechganlar soni va to'g'ri javoblar yig'indisi.

    Natija `QuizBatch.avg_percent` va `QuizBatch.progress` xossalarida ishlatiladi.
    """
    finished = Q(attempts__status=QuizAttempt.Status.FINISHED)
    return (
        qs.select_related("quiz__topic", "group", "lesson__group")
        .annotate(
            sent_n=Count("attempts", distinct=True),
            done_n=Count("attempts", filter=finished, distinct=True),
            correct_sum=Sum("attempts__correct", filter=finished),
            total_sum=Sum("attempts__total", filter=finished),
        )
        # GROUP BY so'rovida Meta.ordering qo'llanmaydi — tartib aniq ko'rsatiladi.
        .order_by("-created_at", "-pk")
    )
