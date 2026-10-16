"""Test havolalarini ustozning Telegram akkaunti orqali yuborish (Telethon, MTProto).

Xabarlar faqat ``TELEGRAM_SENDER_ID`` akkauntidan ketadi: sessiya boshqa akkauntga
tegishli bo'lsa, hech narsa yuborilmaydi. Sessiya ``manage.py telegram_login`` bilan
bir marta yaratiladi va ``TELEGRAM_SESSION_FILE`` faylida saqlanadi (repozitoriyga kirmaydi).
"""

import asyncio
import contextlib
import os
import random
import re
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings

# Ketma-ket xabarlar orasidagi pauza: Telegram spam-filtrini qo'zg'atmaslik uchun.
SEND_DELAY_SECONDS = 1.0
# Shundan qisqa FloodWait'ni kutib, qayta urinamiz; uzunrog'ida to'xtaymiz.
MAX_FLOOD_WAIT = 15


class TelegramError(Exception):
    """Foydalanuvchiga ko'rsatiladigan xato (o'zbekcha matn)."""


@dataclass
class Outgoing:
    key: object  # natijani qaytarish uchun (masalan, QuizAttempt.pk)
    username: str
    phone: str
    first_name: str
    text: str


@dataclass
class Result:
    key: object
    ok: bool
    error: str = ""


def sender_id() -> int:
    return settings.TELEGRAM_SENDER_ID


def session_path() -> Path:
    return Path(settings.TELEGRAM_SESSION_FILE)


def load_session() -> str:
    try:
        return session_path().read_text().strip()
    except FileNotFoundError:
        return ""


def save_session(value: str) -> None:
    path = session_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sessiya — akkauntga to'liq kirish kaliti: faqat egasi o'qiy oladi.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(value)


def is_configured() -> bool:
    return bool(settings.TELEGRAM_API_ID and settings.TELEGRAM_API_HASH and load_session())


def setup_hint() -> str:
    if not (settings.TELEGRAM_API_ID and settings.TELEGRAM_API_HASH):
        return (
            ".env faylga TELEGRAM_API_ID va TELEGRAM_API_HASH yozing (my.telegram.org → "
            "API development tools), so‘ng `python manage.py telegram_login`."
        )
    return "`python manage.py telegram_login` buyrug‘i bilan akkauntga ulaning."


def normalize_username(value: str) -> str:
    """"@ali", "ali", "https://t.me/ali" → "ali"; noto'g'ri bo'lsa — ""."""
    value = (value or "").strip()
    value = re.sub(r"^(https?://)?(www\.)?(t|telegram)\.me/", "", value, flags=re.I)
    value = value.lstrip("@").split("?")[0].strip("/")
    return value if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{3,31}", value) else ""


def normalize_phone(value: str) -> str:
    """Telefonni xalqaro ko'rinishga keltiradi: "90 123 45 67" → "+998901234567"."""
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 9:  # mahalliy raqam (O'zbekiston)
        digits = "998" + digits
    return f"+{digits}" if 11 <= len(digits) <= 15 else ""


def recipient_of(student) -> tuple[str, str]:
    """(username, telefon) — ikkalasi bo'sh bo'lsa, shogirdga yuborib bo'lmaydi."""
    return normalize_username(student.telegram), normalize_phone(student.phone)


def make_client(session: str = ""):
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    return TelegramClient(
        StringSession(session), settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH
    )


@contextlib.asynccontextmanager
async def connected(client):
    """Faqat ulanadi (kirish so'ramaydi); sessiya tekshiruvi — `check_account`."""
    await client.connect()
    try:
        yield client
    finally:
        await client.disconnect()


async def check_account(client) -> object:
    """Ulangan akkaunt aynan ruxsat etilgan akkauntmi — aks holda TelegramError."""
    if not await client.is_user_authorized():
        raise TelegramError("Telegram sessiyasi eskirgan. " + setup_hint())
    me = await client.get_me()
    if me.id != sender_id():
        raise TelegramError(
            f"Ulangan akkaunt ({me.id}) ruxsat etilganidan ({sender_id()}) farq qiladi — "
            "xabar yuborilmadi."
        )
    return me


async def _resolve(client, item: Outgoing):
    from telethon.tl.functions.contacts import ImportContactsRequest
    from telethon.tl.types import InputPhoneContact

    if item.username:
        return await client.get_input_entity(item.username)
    # Username bo'lmasa — telefon raqami orqali (kontaktga qo'shib) topamiz.
    result = await client(
        ImportContactsRequest(
            [InputPhoneContact(random.randrange(2**31), item.phone, item.first_name, "")]
        )
    )
    if not result.users:
        raise TelegramError("bu raqamda Telegram yo‘q yoki raqam yashirilgan")
    return result.users[0]


def _error_text(exc: Exception) -> str:
    from telethon import errors

    if isinstance(exc, TelegramError):
        return str(exc)
    if isinstance(exc, (errors.UsernameNotOccupiedError, errors.UsernameInvalidError, ValueError)):
        return "Telegram username topilmadi"
    if isinstance(exc, (errors.UserPrivacyRestrictedError, errors.PrivacyPremiumRequiredError)):
        return "shogird maxfiylik sozlamalari xabar yuborishga ruxsat bermaydi"
    if isinstance(exc, errors.PeerFloodError):
        return "Telegram vaqtincha cheklov qo‘ydi (ko‘p xabar) — keyinroq urinib ko‘ring"
    if isinstance(exc, errors.UserIsBlockedError):
        return "shogird akkauntingizni bloklagan"
    return f"Telegram xatosi: {type(exc).__name__}"


async def _send_all(client, items: list[Outgoing], delay: float) -> list[Result]:
    from telethon import errors

    await check_account(client)
    results = []
    stopped = ""
    for n, item in enumerate(items):
        if stopped:
            results.append(Result(item.key, False, stopped))
            continue
        if not (item.username or item.phone):
            results.append(Result(item.key, False, "shogirdda Telegram username ham, telefon ham yo‘q"))
            continue
        if n and delay:
            await asyncio.sleep(delay)
        for attempt in range(2):
            try:
                entity = await _resolve(client, item)
                await client.send_message(entity, item.text, link_preview=False)
                results.append(Result(item.key, True))
            except errors.FloodWaitError as exc:
                if attempt == 0 and exc.seconds <= MAX_FLOOD_WAIT:
                    await asyncio.sleep(exc.seconds)
                    continue
                stopped = f"Telegram cheklovi: {exc.seconds} soniyadan keyin qayta yuboring"
                results.append(Result(item.key, False, stopped))
            except Exception as exc:  # noqa: BLE001 — har bir shogird uchun alohida natija
                results.append(Result(item.key, False, _error_text(exc)))
                if isinstance(exc, errors.PeerFloodError):
                    stopped = _error_text(exc)
            break
    return results


def send_file_to_self(path, caption: str = "", client_factory=None) -> None:
    """Faylni ruxsat etilgan akkauntning "Saqlangan xabarlar"iga yuboradi (zaxira uchun)."""

    async def action(client):
        await client.send_file("me", str(path), caption=caption, force_document=True)

    _run_on_self(action, client_factory)


def send_text_to_self(text: str, client_factory=None) -> None:
    """Ustozning o'ziga ("Saqlangan xabarlar") qisqa xabar — bildirishnoma uchun."""

    async def action(client):
        await client.send_message("me", text, link_preview=False)

    _run_on_self(action, client_factory)


def chat_ref(value: str) -> str | int:
    """Guruh chati: "@guruh", "t.me/guruh" → "guruh"; "-100123…" → int; aks holda ""."""
    value = (value or "").strip()
    if re.fullmatch(r"-?\d{5,20}", value):
        return int(value)
    return normalize_username(value)


async def _chat_entity(client, chat: str):
    ref = chat_ref(chat)
    try:
        if isinstance(ref, int):
            # Raqamli ID — sessiyada saqlanmaydi, dialoglar ichidan topamiz.
            async for dialog in client.iter_dialogs():
                if dialog.id == ref:
                    return dialog.entity
            raise ValueError(ref)
        if ref:
            return await client.get_input_entity(ref)
    except (ValueError, TypeError) as exc:
        raise TelegramError(
            "Telegram chat topilmadi — akkauntingiz shu guruhda a’zo ekanini va nom/ID to‘g‘riligini "
            "tekshiring."
        ) from exc
    raise TelegramError("Guruhning Telegram chati ko‘rsatilmagan.")


def send_to_chat(chat: str, text: str, client_factory=None) -> None:
    """Guruh chatiga xabar (masalan, haftalik reyting) — ustozning akkauntidan."""

    async def action(client):
        await client.send_message(await _chat_entity(client, chat), text, link_preview=False)

    _run_on_self(action, client_factory)


def send_file_to(item: Outgoing, path, caption: str = "", client_factory=None) -> None:
    """O'quvchiga fayl (masalan, sertifikat PDF) — username yoki telefon orqali."""

    async def action(client):
        if not (item.username or item.phone):
            raise TelegramError("O‘quvchida Telegram username ham, telefon ham yo‘q.")
        try:
            entity = await _resolve(client, item)
            await client.send_file(entity, str(path), caption=caption, force_document=True)
        except TelegramError:
            raise
        except Exception as exc:  # noqa: BLE001 — foydalanuvchiga tushunarli matn
            raise TelegramError(_error_text(exc)) from exc

    _run_on_self(action, client_factory)


def list_chats(client_factory=None) -> list[dict]:
    """Akkaunt a'zo bo'lgan guruh va kanallar: [{id, title, username}] — chatni tanlash uchun."""

    async def action(client):
        chats = []
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                username = getattr(dialog.entity, "username", None) or ""
                chats.append({"id": dialog.id, "title": dialog.name, "username": username})
        return chats

    return _run_on_self(action, client_factory)


def _run_on_self(action, client_factory=None):
    if client_factory is None:
        if not is_configured():
            raise TelegramError("Telegram ulanmagan. " + setup_hint())
        session = load_session()

        def client_factory():
            return make_client(session)

    async def run():
        async with connected(client_factory()) as client:
            await check_account(client)
            return await action(client)

    try:
        return asyncio.run(run())
    except TelegramError:
        raise
    except (OSError, ConnectionError) as exc:
        raise TelegramError("Telegram serveriga ulanib bo‘lmadi — internetni tekshiring.") from exc


def send_messages(
    items: list[Outgoing], client_factory=None, delay: float = SEND_DELAY_SECONDS
) -> list[Result]:
    """Xabarlarni ruxsat etilgan akkauntdan yuboradi. Sozlanmagan bo'lsa — TelegramError."""
    if client_factory is None:
        if not is_configured():
            raise TelegramError("Telegram ulanmagan. " + setup_hint())
        session = load_session()

        def client_factory():
            return make_client(session)

    async def run():
        # Client o'zi ishlaydigan event loop ichida yaratiladi. `async with client` emas:
        # u sessiya yaroqsiz bo'lsa telefon raqamini so'rab, serverni osib qo'yadi.
        async with connected(client_factory()) as client:
            return await _send_all(client, items, delay)

    try:
        return asyncio.run(run())
    except TelegramError:
        raise
    except (OSError, ConnectionError) as exc:
        raise TelegramError("Telegram serveriga ulanib bo‘lmadi — internetni tekshiring.") from exc
