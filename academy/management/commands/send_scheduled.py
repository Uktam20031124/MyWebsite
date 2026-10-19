from django.core.management.base import BaseCommand, CommandError

from academy.automation import send_scheduled


class Command(BaseCommand):
    help = (
        "Vaqti kelgan rejalashtirilgan test havolalarini tanlangan kanallar (Telegram/email) "
        "orqali yuboradi (har 5 daqiqa)."
    )

    def handle(self, *args, **options):
        result = send_scheduled()
        if result.skipped:
            self.stdout.write(f"O'tkazib yuborildi: {result.skipped}.")
        elif result.sent or result.failed:
            self.stdout.write(f"Rejalashtirilgan: {result.sent} ta yuborildi, {result.failed} ta xato.")
        if result.errors:
            raise CommandError("Rejalashtirilgan havolalar: kanal ishlamadi — " + "; ".join(result.errors))
