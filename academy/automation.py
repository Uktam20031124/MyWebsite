"""Fonda ishlaydigan vazifalar (systemd timer orqali), Telegram va email orqali.

- ``send_reminders``: yuborilgan, lekin hali ochilmagan test havolasi haqida o'quvchiga
  bitta eslatma — havola qaysi kanal(lar) orqali borgan bo'lsa, o'sha orqali, faqat kunduzi.
- ``send_scheduled``: rejalashtirilgan jo'natmalar (jo'natmada tanlangan kanallar orqali).
- ``daily_report``: kun yakuni — ustozning "Saqlangan xabarlar"iga va/yoki emailiga.
"""

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta

from django.conf import settings
from django.db.models import Count, Q
from django.utils import timezone

from . import delivery, mailer
from .contacts import has_contact
from .models import QuizAttempt, QuizBatch, Registration, Student
from .quiz_i18n import message_parts
from .services import percent


@dataclass
class ReminderResult:
    sent: int = 0
    failed: int = 0
    skipped: str = ""  # nima uchun umuman yuborilmadi (tun, sozlanmagan, ...)
    # Kanal umuman ishlamagan (ulanmagan, tarmoq): shu kanaldagilar keyingi safar qayta urinadi.
    errors: list = field(default_factory=list)


def is_daytime(now=None) -> bool:
    start, end = settings.QUIZ_REMINDER_HOURS
    return start <= timezone.localtime(now).hour < end


def due_reminders(now=None):
    """Eslatma vaqti kelgan havolalar: yuborilgan (Telegram yoki email), ochilmagan,
    hali eslatilmagan."""
    now = now or timezone.now()
    cutoff = now - timedelta(hours=settings.QUIZ_REMINDER_AFTER_HOURS)
    return (
        QuizAttempt.objects.filter(
            Q(sent_at__lte=cutoff) | Q(email_sent_at__lte=cutoff),
            status=QuizAttempt.Status.PENDING,
            reminded_at__isnull=True,
            batch__created_at__gte=now - timedelta(days=settings.QUIZ_REMINDER_MAX_AGE_DAYS),
        )
        .select_related("student", "quiz__topic", "batch")
        .order_by("sent_at")
    )


def reminder_text(attempt: QuizAttempt, link: str) -> str:
    m = message_parts(attempt)
    return f"{m['hello']}\n{m['rem_quiz']}\n\n{link}\n\n{m['rem_tail']}"


def reminder_mail(link: str, attempt: QuizAttempt) -> mailer.Mail:
    m = message_parts(attempt)
    return mailer.Mail(
        key=attempt.pk,
        to=attempt.student.email,
        subject=m["rem_subject"],
        text=reminder_text(attempt, link),
        html=mailer.button_html(
            m["rem_title"],
            [m["hello"], m["rem_quiz"], m["rem_tail"]],
            url=link,
            button=m["msg_button"],
        ),
    )


def send_reminders(now=None, dry_run: bool = False, sender=None, mail_sender=None) -> ReminderResult:
    """Har bir havolaga faqat bitta eslatma; muvaffaqiyatsiz bo'lsa ham qayta urinilmaydi
    (o'quvchini ortiqcha bezovta qilmaslik uchun) — sababi send_error/email_error'da saqlanadi.

    Eslatma havola borgan kanal(lar) orqali ketadi: Telegram'ga yuborilganga — Telegram'ga,
    emailga yuborilganga — emailga."""
    now = now or timezone.now()
    if not is_daytime(now):
        return ReminderResult(skipped="tungi vaqt — eslatmalar kunduzi yuboriladi")
    if not settings.SITE_URL:
        return ReminderResult(skipped="DARSXONA_SITE_URL sozlanmagan")
    attempts = list(due_reminders(now))
    if dry_run or not attempts:
        return ReminderResult(sent=len(attempts) if dry_run else 0)
    def link_of(a):
        return settings.SITE_URL + a.get_absolute_url()

    senders = {delivery.TELEGRAM: sender, delivery.EMAIL: mail_sender}
    outcome = ReminderResult()
    handled = set()  # kamida bitta kanal ishlagan (natijasi qanday bo'lmasin) urinishlar
    for channel in delivery.CHANNELS:
        sent_field, error_field = delivery.FIELDS[channel]
        group = [a for a in attempts if getattr(a, sent_field)]
        if not group:
            continue
        out = delivery.send_via(
            channel, group, link_of, reminder_text_for, reminder_mail, sender=senders[channel]
        )
        if out.error:
            outcome.errors.append(f"{out.label}: {out.error}")
            continue
        handled.update(a.pk for a in group)
        outcome.sent += len(out.sent)
        outcome.failed += len(out.failed)
        for a, error in out.failed:
            setattr(a, error_field, f"Eslatma: {error}"[:255])
            a.save(update_fields=[error_field])
    QuizAttempt.objects.filter(pk__in=handled).update(reminded_at=now)
    return outcome


def reminder_text_for(link: str, attempt: QuizAttempt) -> str:
    return reminder_text(attempt, link)


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
        lines.append(f"📵 Telegram/telefon/emaili yo‘q o‘quvchilar: {missing} ta")
    if settings.SITE_URL:
        lines.append(f"\n{settings.SITE_URL}/testlar/")
    return "\n".join(lines)


def send_scheduled(now=None, sender=None, mail_sender=None) -> ReminderResult:
    """Vaqti kelgan rejalashtirilgan jo'natmalar: hali yuborilmagan havolalarni
    jo'natmada tanlangan kanallar orqali yuboradi."""
    now = now or timezone.now()
    batches = list(
        QuizBatch.objects.filter(scheduled_at__lte=now, scheduled_sent_at__isnull=True)
    )
    if not batches:
        return ReminderResult()
    if not settings.SITE_URL:
        return ReminderResult(skipped="DARSXONA_SITE_URL sozlanmagan")

    def link_of(a):
        return settings.SITE_URL + a.get_absolute_url()

    senders = {delivery.TELEGRAM: sender, delivery.EMAIL: mail_sender}
    outcome = ReminderResult()
    done = []
    for batch in batches:
        retry = False
        for channel in delivery.parse_channels(batch.channels):
            sent_field = delivery.FIELDS[channel][0]
            attempts = list(
                batch.attempts.filter(
                    status=QuizAttempt.Status.PENDING, **{f"{sent_field}__isnull": True}
                ).select_related("student", "quiz__topic", "batch")
            )
            if not attempts:
                continue
            for out in delivery.deliver_links(attempts, [channel], link_of, now, senders):
                if out.error:
                    # Yuborilganlar takrorlanmaydi (sent_field), qolganlari keyingi safar.
                    retry = True
                    outcome.errors.append(f"{out.label}: {out.error}")
                outcome.sent += len(out.sent)
                outcome.failed += len(out.failed)
        if not retry:
            done.append(batch.pk)
    QuizBatch.objects.filter(pk__in=done).update(scheduled_sent_at=now)
    return outcome
