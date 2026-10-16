"""Fonda ishlaydigan Telegram vazifalari (systemd timer orqali).

- ``send_reminders``: Telegram'da yuborilgan, lekin hali ochilmagan test havolasi haqida
  o'quvchiga bitta eslatma — faqat kunduzi.
- ``daily_report``: kun yakuni — ustozning "Saqlangan xabarlar"iga qisqa hisobot.
"""

from dataclasses import dataclass
from datetime import datetime, time, timedelta

from django.conf import settings
from django.db.models import Count, Q
from django.utils import timezone

from . import telegram_sender as tg
from .contacts import has_contact
from .models import QuizAttempt, Registration, Student
from .services import percent


@dataclass
class ReminderResult:
    sent: int = 0
    failed: int = 0
    skipped: str = ""  # nima uchun umuman yuborilmadi (tun, sozlanmagan, ...)


def is_daytime(now=None) -> bool:
    start, end = settings.QUIZ_REMINDER_HOURS
    return start <= timezone.localtime(now).hour < end


def due_reminders(now=None):
    """Eslatma vaqti kelgan havolalar: yuborilgan, ochilmagan, hali eslatilmagan."""
    now = now or timezone.now()
    return (
        QuizAttempt.objects.filter(
            status=QuizAttempt.Status.PENDING,
            reminded_at__isnull=True,
            sent_at__lte=now - timedelta(hours=settings.QUIZ_REMINDER_AFTER_HOURS),
            batch__created_at__gte=now - timedelta(days=settings.QUIZ_REMINDER_MAX_AGE_DAYS),
        )
        .select_related("student", "quiz__topic", "batch")
        .order_by("sent_at")
    )


def reminder_text(attempt: QuizAttempt, link: str) -> str:
    return (
        f"Salom, {attempt.student.full_name}!\n"
        f"“{attempt.quiz.topic.title}” mavzusi bo‘yicha test hali ochilmagan: "
        f"{attempt.question_count} ta savol, {attempt.batch.time_limit_minutes} daqiqa.\n\n"
        f"{link}\n\nVaqtingiz bo‘lganda yechib qo‘ying — natija ustozga boradi."
    )


def send_reminders(now=None, dry_run: bool = False, sender=None) -> ReminderResult:
    """Har bir havolaga faqat bitta eslatma; muvaffaqiyatsiz bo'lsa ham qayta urinilmaydi
    (o'quvchini ortiqcha bezovta qilmaslik uchun) — sababi send_error'da saqlanadi."""
    now = now or timezone.now()
    if not is_daytime(now):
        return ReminderResult(skipped="tungi vaqt — eslatmalar kunduzi yuboriladi")
    if not settings.SITE_URL:
        return ReminderResult(skipped="DARSXONA_SITE_URL sozlanmagan")
    attempts = list(due_reminders(now))
    if dry_run or not attempts:
        return ReminderResult(sent=len(attempts) if dry_run else 0)
    items = []
    for a in attempts:
        username, phone = tg.recipient_of(a.student)
        link = settings.SITE_URL + a.get_absolute_url()
        items.append(tg.Outgoing(a.pk, username, phone, a.student.full_name, reminder_text(a, link)))
    results = (sender or tg.send_messages)(items)
    by_pk = {a.pk: a for a in attempts}
    outcome = ReminderResult()
    for r in results:
        attempt = by_pk[r.key]
        attempt.reminded_at = now
        if r.ok:
            outcome.sent += 1
        else:
            outcome.failed += 1
            attempt.send_error = f"Eslatma: {r.error}"[:255]
        attempt.save(update_fields=["reminded_at", "send_error"])
    return outcome


def daily_report(day=None) -> str:
    """Kun yakuni hisoboti (mahalliy sana bo'yicha)."""
    day = day or timezone.localdate()
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.combine(day, time.min), tz)
    end = start + timedelta(days=1)
    finished = list(
        QuizAttempt.objects.filter(
            status=QuizAttempt.Status.FINISHED, finished_at__gte=start, finished_at__lt=end
        ).select_related("student__group", "quiz__topic")
    )
    lines = [f"📊 Darsxona · {day:%d.%m.%Y} kun yakuni"]
    if finished:
        avg = percent(sum(a.correct for a in finished), sum(a.total for a in finished))
        timed_out = sum(a.timed_out for a in finished)
        lines.append(
            f"\n✅ Test yechildi: {len(finished)} ta · o‘rtacha {avg}%"
            + (f" · vaqti tugagan: {timed_out}" if timed_out else "")
        )
        by_topic: dict[str, list] = {}
        for a in finished:
            by_topic.setdefault(a.quiz.topic.title, []).append(a)
        for title, items in sorted(by_topic.items(), key=lambda kv: -len(kv[1]))[:5]:
            pct = percent(sum(a.correct for a in items), sum(a.total for a in items))
            lines.append(f"• {title[:60]} — {len(items)} kishi, {pct}%")
        low = sorted((a for a in finished if a.percent < 50), key=lambda a: a.percent)
        if low:
            lines.append("\n⚠️ 50% dan past:")
            lines += [f"• {a.student.full_name} ({a.student.group.code}) — {a.percent}%" for a in low[:8]]
            if len(low) > 8:
                lines.append(f"  … yana {len(low) - 8} kishi")
    else:
        lines.append("\nBugun test yechilmadi.")

    open_counts = QuizAttempt.objects.filter(status=QuizAttempt.Status.PENDING).aggregate(
        total=Count("pk"), sent=Count("pk", filter=Q(sent_at__isnull=False))
    )
    if open_counts["total"]:
        lines.append(f"\n⏳ Ochilmagan havolalar: {open_counts['total']} ta")
    pending = Registration.objects.filter(status=Registration.Status.PENDING).count()
    if pending:
        lines.append(f"📝 Tekshirilmagan arizalar: {pending} ta")
    missing = sum(
        not has_contact(s) for s in Student.objects.filter(status=Student.Status.ACTIVE)
    )
    if missing:
        lines.append(f"📵 Telegram/telefoni yo‘q o‘quvchilar: {missing} ta")
    if settings.SITE_URL:
        lines.append(f"\n{settings.SITE_URL}/testlar/")
    return "\n".join(lines)
