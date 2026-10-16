from django.core.management.base import BaseCommand, CommandError

from academy import telegram_sender as tg


class Command(BaseCommand):
    help = "Ulangan akkaunt a'zo bo'lgan Telegram guruh/kanallari va ularning ID'lari."

    def handle(self, *args, **options):
        try:
            chats = tg.list_chats()
        except tg.TelegramError as exc:
            raise CommandError(str(exc)) from exc
        for c in chats:
            ref = f"@{c['username']}" if c["username"] else str(c["id"])
            self.stdout.write(f"{ref:<32} {c['title']}")
        if not chats:
            self.stdout.write("Guruh yoki kanal topilmadi.")
