"""Motivatsiya: haftalik reyting (guruh chatiga), o'quvchining shaxsiy sahifasi, sertifikat."""

import secrets
from dataclasses import dataclass
from datetime import timedelta
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .models import Group, QuizAttempt, Student
from .services import percent, quiz_stats, student_attendance_rate

# --- Haftalik reyting --------------------------------------------------------

LEADERBOARD_DAYS = 7
MEDALS = ["🥇", "🥈", "🥉"]


@dataclass
class LeaderRow:
    student: Student
    pct: int
    n: int


def weekly_leaderboard(group: Group, now=None, days: int = LEADERBOARD_DAYS) -> dict:
    """Guruhning oxirgi ``days`` kundagi test natijalari bo'yicha reytingi."""
    now = now or timezone.now()
    attempts = QuizAttempt.objects.filter(
        student__group=group,
        student__status=Student.Status.ACTIVE,
        status=QuizAttempt.Status.FINISHED,
        total__gt=0,
        finished_at__gte=now - timedelta(days=days),
    ).select_related("student")
    by_student: dict[int, list] = {}
    for a in attempts:
        by_student.setdefault(a.student_id, []).append(a)
    rows = [
        LeaderRow(
            items[0].student,
            percent(sum(a.correct for a in items), sum(a.total for a in items)),
            len(items),
        )
        for items in by_student.values()
    ]
    rows.sort(key=lambda r: (-r.pct, -r.n, r.student.full_name))
    all_attempts = [a for items in by_student.values() for a in items]
    return {
        "rows": rows,
        "tests_n": len(all_attempts),
        "avg": percent(sum(a.correct for a in all_attempts), sum(a.total for a in all_attempts))
        if all_attempts
        else None,
        "most_active": max(rows, key=lambda r: r.n) if rows else None,
    }


def leaderboard_text(group: Group, board: dict) -> str:
    if not board["rows"]:
        return ""
    lines = [f"🏆 {group.name} — haftaning eng yaxshilari", ""]
    for medal, row in zip(MEDALS, board["rows"][: len(MEDALS)], strict=False):
        lines.append(f"{medal} {row.student.full_name} — {row.pct}% ({row.n} ta test)")
    lines.append("")
    lines.append(f"Guruh bo‘yicha: {board['tests_n']} ta test, o‘rtacha {board['avg']}%.")
    active = board["most_active"]
    if active and active.n > 1:
        lines.append(f"🔥 Eng faol: {active.student.full_name} — {active.n} ta test.")
    lines.append("Barakalla! Keyingi hafta sizni ham shu ro‘yxatda ko‘rishni kutamiz 💪")
    return "\n".join(lines)


# --- Shaxsiy sahifa ----------------------------------------------------------


def portal_url(student: Student) -> str:
    """O'quvchining shaxsiy sahifasi havolasi (kalit kerak bo'lsa yaratiladi)."""
    from django.urls import reverse

    if not student.portal_token:
        student.portal_token = secrets.token_urlsafe(12)
        student.save(update_fields=["portal_token"])
    return reverse("student_portal", args=[student.portal_token])


def group_rank(student: Student) -> tuple[int | None, int]:
    """O'quvchining guruhdagi o'rni testlar foizi bo'yicha: (o'rin, test yechganlar soni)."""
    mates = list(
        student.group.students.filter(status=Student.Status.ACTIVE).values_list("pk", flat=True)
    )
    stats = quiz_stats(mates)
    ranked = sorted(stats.items(), key=lambda kv: -(kv[1].pct or 0))
    for i, (pk, _) in enumerate(ranked, start=1):
        if pk == student.pk:
            return i, len(ranked)
    return None, len(ranked)


# --- Sertifikat --------------------------------------------------------------

FONTS = Path(__file__).resolve().parent / "fonts"


def default_course(student: Student) -> str:
    """"S-009 · Starter" → "Starter"."""
    return student.group.name.split("·")[-1].strip() or student.group.name


def certificate_number(student: Student) -> str:
    return f"DX-{timezone.localdate():%Y}-{student.pk:04d}"


def certificate_pdf(student: Student, course: str, teacher: str) -> bytes:
    """A4 (yotiq) sertifikat. O'zbek harflari uchun DejaVu shrifti (loyiha ichida)."""
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    for name, file in (
        ("DX", "DejaVuSans.ttf"),
        ("DX-Bold", "DejaVuSans-Bold.ttf"),
        ("DX-Serif", "DejaVuSerif-Bold.ttf"),
    ):
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))

    quiz = quiz_stats([student.pk]).get(student.pk)
    attendance = student_attendance_rate(student)
    width, height = landscape(A4)
    brand, gold, ink, muted = (HexColor(c) for c in ("#1e3a2f", "#b08948", "#1c1a16", "#6b6358"))

    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=(width, height))
    pdf.setTitle(f"Sertifikat — {student.full_name}")
    pdf.setAuthor(teacher)
    # Ramka
    pdf.setFillColor(HexColor("#fffdf8"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setStrokeColor(brand)
    pdf.setLineWidth(6)
    pdf.rect(24, 24, width - 48, height - 48)
    pdf.setStrokeColor(gold)
    pdf.setLineWidth(1.5)
    pdf.rect(38, 38, width - 76, height - 76)

    cx = width / 2
    pdf.setFillColor(gold)
    pdf.setFont("DX-Bold", 13)
    pdf.drawCentredString(cx, height - 92, "DARSXONA")
    pdf.setFillColor(brand)
    pdf.setFont("DX-Serif", 46)
    pdf.drawCentredString(cx, height - 150, "SERTIFIKAT")
    pdf.setFillColor(muted)
    pdf.setFont("DX", 14)
    pdf.drawCentredString(cx, height - 185, "Ushbu sertifikat")
    pdf.setFillColor(ink)
    pdf.setFont("DX-Serif", 32)
    pdf.drawCentredString(cx, height - 232, student.full_name)
    pdf.setStrokeColor(gold)
    pdf.setLineWidth(1)
    pdf.line(cx - 220, height - 245, cx + 220, height - 245)
    pdf.setFillColor(muted)
    pdf.setFont("DX", 14)
    pdf.drawCentredString(cx, height - 275, "ga quyidagi kursni muvaffaqiyatli yakunlagani uchun berildi:")
    pdf.setFillColor(brand)
    pdf.setFont("DX-Bold", 22)
    pdf.drawCentredString(cx, height - 310, course)

    stats = []
    if quiz and quiz.n:
        stats.append(f"Testlar: {quiz.n} ta, o‘rtacha {quiz.pct}%")
    if attendance["total"]:
        stats.append(f"Davomat: {attendance['percent']}%")
    if stats:
        pdf.setFillColor(muted)
        pdf.setFont("DX", 12)
        pdf.drawCentredString(cx, height - 340, "  ·  ".join(stats))

    pdf.setFillColor(ink)
    pdf.setFont("DX", 12)
    pdf.drawString(90, 92, f"Sana: {timezone.localdate():%d.%m.%Y}")
    pdf.drawString(90, 74, f"№ {certificate_number(student)}")
    pdf.line(width - 300, 100, width - 90, 100)
    pdf.drawCentredString(width - 195, 84, teacher)
    pdf.setFillColor(muted)
    pdf.setFont("DX", 10)
    pdf.drawCentredString(width - 195, 70, "Ustoz")
    pdf.showPage()
    pdf.save()
    return buf.getvalue()


def certificate_filename(student: Student) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in student.full_name).strip("-")
    return f"sertifikat-{safe or student.pk}.pdf"


def site_url(request=None) -> str:
    if settings.SITE_URL:
        return settings.SITE_URL
    return request.build_absolute_uri("/").rstrip("/") if request else ""
