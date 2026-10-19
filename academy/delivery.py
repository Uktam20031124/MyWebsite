"""Test havolalarini o'quvchilarga yetkazish: Telegram va/yoki email (Gmail).

Har bir kanal mustaqil: biri ishlamasa (ulanmagan, xato), ikkinchisi baribir yuboradi.
Telegram natijasi ``sent_at``/``send_error``ga, email natijasi
``email_sent_at``/``email_error``ga yoziladi.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from django.utils import timezone

from . import mailer
from . import telegram_sender as tg
from .models import QuizAttempt
from .quiz_i18n import message_parts

TELEGRAM, EMAIL = "telegram", "email"
CHANNELS = (TELEGRAM, EMAIL)
CHANNEL_LABELS = {TELEGRAM: "Telegram", EMAIL: "Email"}
FIELDS = {TELEGRAM: ("sent_at", "send_error"), EMAIL: ("email_sent_at", "email_error")}


@dataclass
class Outcome:
    channel: str
    sent: list = field(default_factory=list)  # yetib borgan urinishlar
    failed: list = field(default_factory=list)  # (urinish, sabab)
    no_contact: list = field(default_factory=list)  # bu kanalda manzili yo'qlar
    error: str = ""  # kanal umuman ishlamadi (hech kimga yuborilmadi)

    @property
    def label(self) -> str:
        return CHANNEL_LABELS[self.channel]


def parse_channels(value) -> list[str]:
    """"telegram,email" yoki ro'yxat → tartiblangan, takrorsiz kanallar."""
    items = value.split(",") if isinstance(value, str) else (value or [])
    chosen = {str(v).strip() for v in items}
    return [c for c in CHANNELS if c in chosen]


def is_ready(channel: str) -> bool:
    return tg.is_configured() if channel == TELEGRAM else mailer.is_configured()


def setup_hint(channel: str) -> str:
    return tg.setup_hint() if channel == TELEGRAM else mailer.setup_hint()


def quiz_message(link: str, attempt: QuizAttempt) -> str:
    """Shogirdga boradigan xabar matni (Telegram va emailning oddiy matn qismi) —
    o'quvchining test tilida."""
    m = message_parts(attempt)
    return f"{m['hello']}\n{m['msg_quiz']}\n\n{link}\n\n{m['msg_once']}"


def quiz_mail(link: str, attempt: QuizAttempt) -> mailer.Mail:
    m = message_parts(attempt)
    return mailer.Mail(
        key=attempt.pk,
        to=attempt.student.email,
        subject=m["msg_subject"],
        text=quiz_message(link, attempt),
        html=mailer.button_html(
            m["msg_title"],
            [m["hello"], m["msg_counts"]],
            url=link,
            button=m["msg_button"],
            footer=m["msg_once"],
        ),
    )


def send_via(
    channel: str,
    attempts: list[QuizAttempt],
    link_of: Callable[[QuizAttempt], str],
    text_of: Callable[[str, QuizAttempt], str] = quiz_message,
    mail_of: Callable[[str, QuizAttempt], mailer.Mail] = quiz_mail,
    sender=None,
) -> Outcome:
    """Bitta kanal orqali yuboradi (bazaga yozmaydi)."""
    out = Outcome(channel)
    by_pk = {a.pk: a for a in attempts}
    try:
        if channel == TELEGRAM:
            items = []
            for a in attempts:
                username, phone = tg.recipient_of(a.student)
                items.append(
                    tg.Outgoing(a.pk, username, phone, a.student.full_name, text_of(link_of(a), a))
                )
            results = (sender or tg.send_messages)(items) if items else []
        else:
            out.no_contact = [a for a in attempts if not mailer.valid_email(a.student.email)]
            mails = [mail_of(link_of(a), a) for a in attempts if a not in out.no_contact]
            results = (sender or mailer.send_mails)(mails) if mails else []
    except (tg.TelegramError, mailer.MailError) as exc:
        out.error = str(exc)
        return out
    for r in results:
        if r.ok:
            out.sent.append(by_pk[r.key])
        else:
            out.failed.append((by_pk[r.key], r.error))
    return out


def deliver_links(
    attempts: list[QuizAttempt], channels, link_of, now=None, senders=None
) -> list[Outcome]:
    """Test havolalarini tanlangan kanallar orqali yuboradi va natijani saqlaydi."""
    now = now or timezone.now()
    outcomes = []
    for channel in parse_channels(channels):
        out = send_via(channel, attempts, link_of, sender=(senders or {}).get(channel))
        sent_field, error_field = FIELDS[channel]
        for a in out.sent:
            setattr(a, sent_field, now)
            setattr(a, error_field, "")
            a.save(update_fields=[sent_field, error_field])
        for a, error in out.failed:
            setattr(a, error_field, error[:255])
            a.save(update_fields=[error_field])
        outcomes.append(out)
    return outcomes
