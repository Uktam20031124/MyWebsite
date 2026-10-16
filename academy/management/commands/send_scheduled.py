from django.core.management.base import BaseCommand, CommandError

from academy import telegram_sender as tg
from academy.automation import send_scheduled


class Command(BaseCommand):
    help = "Vaqti kelgan rejalashtirilgan test havolalarini Telegram orqali yuboradi (har 5 daqiqa)."

    def handle(self, *args, **options):
        try:
            result = send_scheduled()
        except tg.TelegramError as exc:
            raise CommandError(f"Rejalashtirilgan havolalar yuborilmadi: {exc}") from exc
        if result.skipped:
            self.stdout.write(f"O'tkazib yuborildi: {result.skipped}.")
        elif result.sent or result.failed:
            self.stdout.write(f"Rejalashtirilgan: {result.sent} ta yuborildi, {result.failed} ta xato.")
