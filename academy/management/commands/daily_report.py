from django.core.management.base import BaseCommand, CommandError

from academy import telegram_sender as tg
from academy.automation import daily_report


class Command(BaseCommand):
    help = "Kun yakuni hisoboti ustozning Telegram 'Saqlangan xabarlar'iga (systemd timer: 20:00)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Faqat ekranga chiqarish")

    def handle(self, *args, dry_run, **options):
        text = daily_report()
        if dry_run:
            self.stdout.write(text)
            return
        try:
            tg.send_text_to_self(text)
        except tg.TelegramError as exc:
            raise CommandError(f"Hisobot yuborilmadi: {exc}") from exc
        self.stdout.write("Kun yakuni hisoboti Telegram'ga yuborildi.")
