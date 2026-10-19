"""Email (Gmail SMTP) orqali yuborish — Telegram'ga muqobil kanal.

Hamma xatlar bitta SMTP ulanishi orqali ketadi. Har bir o'quvchi uchun alohida natija
(``telegram_sender.Result`` bilan bir xil shakl) qaytadi; butun kanal ishlamasa
(login/parol, tarmoq) — ``MailError``.
"""

import smtplib
from dataclasses import dataclass, field
from html import escape

from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .telegram_sender import Result


class MailError(Exception):
    """Foydalanuvchiga ko'rsatiladigan xato (o'zbekcha)."""


@dataclass
class Mail:
    key: object
    to: str
    subject: str
    text: str
    html: str = ""
    attachments: list = field(default_factory=list)  # [(fayl nomi, bytes, mime)]


def is_configured() -> bool:
    if not settings.EMAIL_BACKEND.endswith("smtp.EmailBackend"):
        return True  # testlar va dev (locmem/console)
    return bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)


def setup_hint() -> str:
    return gettext(
        ".env faylga DARSXONA_GMAIL_USER (Gmail manzil) va DARSXONA_GMAIL_APP_PASSWORD "
        "(Google → Xavfsizlik → App passwords, 16 belgi) yozing."
    )


def valid_email(value: str) -> str:
    value = (value or "").strip()
    try:
        validate_email(value)
    except ValidationError:
        return ""
    return value


def button_html(title: str, lines: list[str], url: str = "", button: str = "", footer: str = "") -> str:
    """Oddiy, hamma pochta dasturlarida to'g'ri ko'rinadigan HTML xat."""
    body = "".join(f'<p style="margin:0 0 12px">{escape(line)}</p>' for line in lines)
    cta = (
        f'<p style="margin:20px 0"><a href="{escape(url)}" style="background:#c2572a;color:#fff;'
        f'padding:12px 22px;border-radius:10px;text-decoration:none;font-weight:600;display:inline-block">'
        f"{escape(button)}</a></p>"
        f'<p style="margin:0 0 12px;font-size:13px;color:#8a8275">Tugma ishlamasa: '
        f'<a href="{escape(url)}" style="color:#2c6688">{escape(url)}</a></p>'
        if url
        else ""
    )
    foot = f'<p style="margin:18px 0 0;font-size:13px;color:#8a8275">{escape(footer)}</p>' if footer else ""
    return (
        '<div style="background:#f5f2ea;padding:24px 12px;font-family:Arial,Helvetica,sans-serif">'
        '<div style="max-width:520px;margin:0 auto;background:#fffdf8;border:1px solid #e5ddcf;'
        'border-radius:16px;padding:24px;color:#1c1a16;font-size:15px;line-height:1.5">'
        '<p style="margin:0 0 6px;font-size:12px;letter-spacing:.08em;color:#b08948;font-weight:700">MINAR TEST</p>'
        f'<h1 style="margin:0 0 14px;font-size:20px;color:#1e3a2f">{escape(title)}</h1>'
        f"{body}{cta}{foot}</div></div>"
    )


def _error_text(exc: Exception) -> str:
    if isinstance(exc, smtplib.SMTPRecipientsRefused):
        return "email manzil qabul qilinmadi"
    if isinstance(exc, smtplib.SMTPDataError):
        return "Gmail xatni rad etdi (kunlik limit yoki spam filtri)"
    return f"email xatosi: {type(exc).__name__}"


def send_mails(mails: list[Mail]) -> list[Result]:
    """Xatlarni yuboradi. Kanal umuman ishlamasa — MailError (hech biri yuborilmagan)."""
    if not is_configured():
        raise MailError(_("Gmail ulanmagan. ") + setup_hint())
    results = []
    try:
        with mail.get_connection(fail_silently=False) as connection:
            for m in mails:
                if not valid_email(m.to):
                    results.append(Result(m.key, False, "shogirdda email yo‘q yoki noto‘g‘ri"))
                    continue
                msg = mail.EmailMultiAlternatives(
                    m.subject, m.text, settings.DEFAULT_FROM_EMAIL, [m.to], connection=connection
                )
                if m.html:
                    msg.attach_alternative(m.html, "text/html")
                for name, content, mime in m.attachments:
                    msg.attach(name, content, mime)
                try:
                    msg.send()
                    results.append(Result(m.key, True))
                except (smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError) as exc:
                    results.append(Result(m.key, False, _error_text(exc)))
    except smtplib.SMTPAuthenticationError as exc:
        raise MailError(
            _("Gmail login yoki App Password noto‘g‘ri (oddiy parol ishlamaydi). ") + setup_hint()
        ) from exc
    except (smtplib.SMTPException, OSError) as exc:
        raise MailError(_("Gmail serveriga ulanib bo‘lmadi: {name}").format(name=type(exc).__name__)) from exc
    return results


def send_one(to: str, subject: str, text: str, html: str = "", attachments=None) -> None:
    """Bitta xat; muvaffaqiyatsiz bo'lsa — MailError."""
    result = send_mails([Mail(0, to, subject, text, html, attachments or [])])[0]
    if not result.ok:
        raise MailError(result.error)
