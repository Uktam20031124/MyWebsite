from django.core.management.base import BaseCommand, CommandError

from academy.automation import send_reminders


class Command(BaseCommand):
    help = (
        "Telegram yoki emailga yuborilgan, lekin ochilmagan test havolalari haqida o'quvchilarga bitta "
        "eslatma (faqat kunduzi). systemd timer har soatda ishga tushiradi."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="Yubormasdan, nechta ekanini ko'rsatish"
        )

    def handle(self, *args, dry_run, **options):
        result = send_reminders(dry_run=dry_run)
        if result.skipped:
            self.stdout.write(f"O'tkazib yuborildi: {result.skipped}.")
        elif dry_run:
            self.stdout.write(f"Eslatma vaqti kelgan havolalar: {result.sent} ta (yuborilmadi).")
        else:
            self.stdout.write(f"Eslatmalar: {result.sent} ta yuborildi, {result.failed} ta xato.")
        if result.errors:
            raise CommandError("Eslatmalar: kanal ishlamadi — " + "; ".join(result.errors))
