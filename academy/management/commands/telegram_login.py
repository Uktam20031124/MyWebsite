import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from academy import telegram_sender as tg


class Command(BaseCommand):
    help = (
        "Test havolalarini yuboradigan Telegram akkauntiga ulanish (bir marta). Telefon, "
        "SMS kod va (bo'lsa) 2 bosqichli parol so'raladi. Faqat TELEGRAM_SENDER_ID "
        "akkauntiga ruxsat beriladi."
    )

    def add_arguments(self, parser):
        parser.add_argument("--check", action="store_true", help="Saqlangan sessiyani tekshirish")
        parser.add_argument("--logout", action="store_true", help="Sessiyani o'chirish")

    def handle(self, *args, check, logout, **options):
        if not (settings.TELEGRAM_API_ID and settings.TELEGRAM_API_HASH):
            raise CommandError(
                ".env faylga TELEGRAM_API_ID va TELEGRAM_API_HASH yozing "
                "(my.telegram.org → API development tools)."
            )
        try:
            if logout:
                asyncio.run(self.logout())
            elif check:
                asyncio.run(self.check())
            else:
                asyncio.run(self.login())
        except tg.TelegramError as exc:
            raise CommandError(str(exc)) from exc

    async def check(self):
        if not tg.load_session():
            raise tg.TelegramError("Sessiya yo'q. `python manage.py telegram_login` bilan ulaning.")
        async with tg.connected(tg.make_client(tg.load_session())) as client:
            me = await tg.check_account(client)
        self.stdout.write(self.style.SUCCESS(f"Ulangan: {self.describe(me)}"))

    async def logout(self):
        session = tg.load_session()
        if session:
            async with tg.connected(tg.make_client(session)) as client:
                await client.log_out()
        tg.session_path().unlink(missing_ok=True)
        self.stdout.write("Sessiya o'chirildi.")

    async def login(self):
        allowed = tg.sender_id()
        self.stdout.write(f"Ruxsat etilgan akkaunt ID: {allowed}")
        client = tg.make_client()
        await client.start(
            phone=lambda: input("Telefon raqami (+998...): ").strip(),
            code_callback=lambda: input("Telegram'ga kelgan kod: ").strip(),
            password=lambda: input("2 bosqichli parol (bo'lmasa Enter): "),
        )
        try:
            me = await client.get_me()
            if me.id != allowed:
                await client.log_out()
                raise tg.TelegramError(
                    f"Bu akkaunt ({me.id}) ruxsat etilmagan — faqat {allowed}. Sessiya saqlanmadi."
                )
            tg.save_session(client.session.save())
        finally:
            await client.disconnect()
        self.stdout.write(
            self.style.SUCCESS(
                f"Ulandi: {self.describe(me)}. Sessiya: {tg.session_path()} (maxfiy saqlang)."
            )
        )

    @staticmethod
    def describe(me) -> str:
        name = " ".join(filter(None, [me.first_name, me.last_name]))
        username = f" @{me.username}" if me.username else ""
        return f"{name}{username} (ID {me.id})"
