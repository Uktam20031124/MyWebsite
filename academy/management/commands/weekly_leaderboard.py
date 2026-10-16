from django.core.management.base import BaseCommand

from academy import telegram_sender as tg
from academy.models import Group
from academy.motivation import leaderboard_text, weekly_leaderboard


class Command(BaseCommand):
    help = (
        "Haftalik reyting (oxirgi 7 kun testlari) har bir guruhning Telegram chatiga "
        "(Group.telegram_chat). systemd timer: yakshanba 18:00."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Yubormasdan, matnni ko'rsatish")
        parser.add_argument("--group", help="Faqat shu guruh kodi")

    def handle(self, *args, dry_run, group, **options):
        groups = Group.objects.filter(status=Group.Status.ACTIVE).order_by("name")
        if group:
            groups = groups.filter(code__iexact=group)
        for g in groups:
            text = leaderboard_text(g, weekly_leaderboard(g))
            if not text:
                self.stdout.write(f"{g.code}: oxirgi 7 kunda test yo'q — o'tkazildi.")
                continue
            if dry_run:
                self.stdout.write(f"--- {g.code} → {g.telegram_chat or '(chat yo‘q)'}\n{text}\n")
                continue
            if not g.telegram_chat:
                self.stdout.write(f"{g.code}: Telegram chat tanlanmagan — o'tkazildi.")
                continue
            try:
                tg.send_to_chat(g.telegram_chat, text)
            except tg.TelegramError as exc:
                self.stderr.write(f"{g.code}: yuborilmadi — {exc}")
            else:
                self.stdout.write(f"{g.code}: reyting {g.telegram_chat} ga yuborildi.")
