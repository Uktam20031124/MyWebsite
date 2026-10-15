import asyncio
import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from academy import telegram_sender as tg


class Command(BaseCommand):
    help = (
        "Test havolalarini yuboradigan Telegram akkauntiga ulanish (bir marta). Faqat "
        "TELEGRAM_SENDER_ID akkauntiga ruxsat beriladi. Interaktiv: argumentsiz. "
        "Ikki bosqichli (terminal so'roviga javob berib bo'lmaganda): avval --phone, "
        "Telegram'ga kelgan kod bilan --code (2FA bo'lsa --password ham)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--phone", help="1-bosqich: shu raqamga kirish kodini yuborish")
        parser.add_argument("--code", help="2-bosqich: Telegram'ga kelgan kod")
        parser.add_argument("--password", help="2 bosqichli tasdiqlash paroli (yoqilgan bo'lsa)")
        parser.add_argument("--check", action="store_true", help="Saqlangan sessiyani tekshirish")
        parser.add_argument("--logout", action="store_true", help="Sessiyani o'chirish")

    def handle(self, *args, phone, code, password, check, logout, **options):
        if not (settings.TELEGRAM_API_ID and settings.TELEGRAM_API_HASH):
            raise CommandError(
                ".env faylga TELEGRAM_API_ID va TELEGRAM_API_HASH yozing "
                "(my.telegram.org → API development tools)."
            )
        if logout:
            action = self.logout()
        elif check:
            action = self.check()
        elif phone:
            action = self.send_code(phone)
        elif code or password:
            action = self.finish(code, password)
        else:
            action = self.interactive()
        try:
            asyncio.run(action)
        except tg.TelegramError as exc:
            raise CommandError(str(exc)) from exc

    # --- Saqlangan sessiya ---------------------------------------------------

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
        self.pending_path().unlink(missing_ok=True)
        self.stdout.write("Sessiya o'chirildi.")

    # --- Ikki bosqichli kirish (--phone, so'ng --code) --------------------------

    @staticmethod
    def pending_path():
        return tg.session_path().with_name(tg.session_path().name + ".pending")

    def save_pending(self, **data) -> None:
        path = self.pending_path()
        tg.session_path().parent.mkdir(parents=True, exist_ok=True)
        path.touch(mode=0o600, exist_ok=True)
        path.write_text(json.dumps(data))

    def load_pending(self) -> dict:
        try:
            return json.loads(self.pending_path().read_text())
        except (FileNotFoundError, ValueError) as exc:
            raise tg.TelegramError(
                "Avval kod so'rang: python manage.py telegram_login --phone +998XXXXXXXXX"
            ) from exc

    async def send_code(self, phone: str):
        phone = tg.normalize_phone(phone) or phone.strip()
        async with tg.connected(tg.make_client()) as client:
            sent = await client.send_code_request(phone)
            # Kod shu sessiyaga (auth key) bog'langan — 2-bosqichda aynan u kerak.
            self.save_pending(session=client.session.save(), phone=phone, hash=sent.phone_code_hash)
        self.stdout.write(
            self.style.SUCCESS(f"Kod {phone} akkauntining Telegram ilovasiga yuborildi.")
        )
        self.stdout.write("Endi: python manage.py telegram_login --code KOD")

    async def finish(self, code: str | None, password: str | None):
        from telethon import errors

        pending = self.load_pending()
        async with tg.connected(tg.make_client(pending["session"])) as client:
            try:
                if code and not pending.get("need_password"):
                    await client.sign_in(
                        pending["phone"], code.strip(), phone_code_hash=pending["hash"]
                    )
                elif password:
                    await client.sign_in(password=password)
                else:
                    raise tg.TelegramError("2 bosqichli parol kerak: --password PAROL")
            except errors.SessionPasswordNeededError:
                self.save_pending(**{**pending, "need_password": True})
                if not password:
                    raise tg.TelegramError(
                        "Akkauntda 2 bosqichli parol yoqilgan: "
                        "python manage.py telegram_login --password PAROL"
                    ) from None
                await client.sign_in(password=password)
            except (errors.PhoneCodeInvalidError, errors.PhoneCodeExpiredError) as exc:
                raise tg.TelegramError(
                    "Kod noto'g'ri yoki eskirgan. Qaytadan: telegram_login --phone ..."
                ) from exc
            except errors.PasswordHashInvalidError as exc:
                raise tg.TelegramError("2 bosqichli parol noto'g'ri.") from exc
            me = await self.accept(client)
        self.pending_path().unlink(missing_ok=True)
        self.stdout.write(self.style.SUCCESS(f"Ulandi: {self.describe(me)}."))

    # --- Interaktiv kirish -----------------------------------------------------

    async def interactive(self):
        self.stdout.write(f"Ruxsat etilgan akkaunt ID: {tg.sender_id()}")
        client = tg.make_client()
        await client.start(
            phone=lambda: input("Telefon raqami (+998...): ").strip(),
            code_callback=lambda: input("Telegram'ga kelgan kod: ").strip(),
            password=lambda: input("2 bosqichli parol (bo'lmasa Enter): "),
        )
        try:
            me = await self.accept(client)
        finally:
            await client.disconnect()
        self.stdout.write(self.style.SUCCESS(f"Ulandi: {self.describe(me)}."))

    async def accept(self, client):
        """Faqat ruxsat etilgan akkauntning sessiyasini saqlaydi; boshqasidan chiqadi."""
        me = await client.get_me()
        if me.id != tg.sender_id():
            await client.log_out()
            raise tg.TelegramError(
                f"Bu akkaunt ({me.id}) ruxsat etilmagan — faqat {tg.sender_id()}. "
                "Sessiya saqlanmadi."
            )
        tg.save_session(client.session.save())
        self.stdout.write(f"Sessiya: {tg.session_path()} (maxfiy — hech kimga bermang).")
        return me

    @staticmethod
    def describe(me) -> str:
        name = " ".join(filter(None, [me.first_name, me.last_name]))
        username = f" @{me.username}" if me.username else ""
        return f"{name}{username} (ID {me.id})"
