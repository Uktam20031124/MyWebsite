from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from academy import mailer
from academy import telegram_sender as tg
from academy.automation import daily_report


class Command(BaseCommand):
    help = (
        "Kun yakuni hisoboti ustozga: Telegram 'Saqlangan xabarlar' va/yoki email "
        "(DARSXONA_REPORT_EMAIL) — qaysi biri ulangan bo'lsa (systemd timer: 20:00)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Faqat ekranga chiqarish")

    def handle(self, *args, dry_run, **options):
        text = daily_report()
        if dry_run:
            self.stdout.write(text)
            return
        sent, errors = [], []
        email_on = bool(settings.REPORT_EMAIL) and mailer.is_configured()
        # Email ulanmagan bo'lsa — Telegram har doim sinab ko'riladi (xatosi ko'rinsin).
        if tg.is_configured() or not email_on:
            try:
                tg.send_text_to_self(text)
                sent.append("Telegram")
            except tg.TelegramError as exc:
                errors.append(f"Telegram: {exc}")
        if email_on:
            try:
                mailer.send_one(settings.REPORT_EMAIL, text.splitlines()[0].lstrip("📊 "), text)
                sent.append("email")
            except mailer.MailError as exc:
                errors.append(f"Email: {exc}")
        if sent:
            self.stdout.write(f"Kun yakuni hisoboti yuborildi: {', '.join(sent)}.")
        if errors:
            raise CommandError("Hisobot yuborilmadi — " + "; ".join(errors))
