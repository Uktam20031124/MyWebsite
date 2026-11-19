"""Dasturchi 7-oy · QuizBot 2-qism: reyting, admin, broadcast, middleware, eslatma, ikki til, statistika, testlar.

Fayllar 6-oy oxiridagi loyiha ustiga yig'iladi; har dars aiogram 3 bilan sinovdan o'tgan.
"""

from .lesson_kit import lesson, step
from .lessons_m06 import CONFIG, DB_V3, MENU_FINAL, QUIZ_V2, STATES_FULL

M = "7-oy · Telegram bot, 2-qism"

# --- database.py: 6-oy ustiga qo'shiladigan funksiyalar ---------------------------------------------------
TOP_USERS = r'''

async def top_users(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT u.name, SUM(a.score) AS ball, COUNT(a.id) AS testlar "
            "FROM attempts a JOIN users u ON u.id = a.user_id "
            "GROUP BY a.user_id ORDER BY ball DESC LIMIT ?",
            (limit,),
        )
        return await cursor.fetchall()
'''

ADD_QUESTION = r'''

async def add_question(subject, text, a, b, c, d, correct):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO questions (subject, text, a, b, c, d, correct) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (subject, text, a, b, c, d, correct),
        )
        await db.commit()
'''

QUESTIONS_PAGE = r'''

async def questions_page(offset: int, limit: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM questions")
        (total,) = await cursor.fetchone()
        cursor = await db.execute(
            "SELECT id, subject, text FROM questions ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        return total, await cursor.fetchall()


async def delete_question(question_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        await db.commit()
'''

ALL_USERS = r'''

async def all_user_ids() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM users")
        return [row[0] for row in await cursor.fetchall()]
'''

ADD_COLUMN = r'''

async def add_column(db, table: str, column: str, ddl: str):
    cursor = await db.execute(f"PRAGMA table_info({table})")
    if column not in [row[1] for row in await cursor.fetchall()]:
        await db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")
'''

REMINDERS = r'''

async def reminder_user_ids() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM users WHERE reminders = 1")
        return [row[0] for row in await cursor.fetchall()]


async def toggle_reminders(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET reminders = 1 - reminders WHERE id = ?", (user_id,))
        await db.commit()
        cursor = await db.execute("SELECT reminders FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
    return row[0] if row else 0
'''

LANG_DB = r'''

async def get_lang(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT lang FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
    return row[0] if row and row[0] else "uz"


async def set_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
        await db.execute("UPDATE users SET lang = ? WHERE id = ?", (lang, user_id))
        await db.commit()
'''

STATS_DB = r'''

async def stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT (SELECT COUNT(*) FROM users), COUNT(*), "
            "COALESCE(AVG(score * 100.0 / total), 0), "
            "COALESCE(SUM(DATE(created_at) = DATE('now')), 0) FROM attempts"
        )
        users, tests, avg, today = await cursor.fetchone()
    return {"users": users, "tests": tests, "avg": avg, "today": today}


async def attempts_rows():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT u.name, a.subject, a.score, a.total, a.created_at "
            "FROM attempts a JOIN users u ON u.id = a.user_id ORDER BY a.id"
        )
        return await cursor.fetchall()
'''

PHOTO_TABLES = '''        await add_column(db, "questions", "photo", "TEXT")
        await db.commit()'''
REMIND_TABLES = '''        await add_column(db, "users", "reminders", "INTEGER DEFAULT 1")
        await db.commit()'''
LANG_TABLES = '''        await add_column(db, "users", "lang", "TEXT DEFAULT 'uz'")
        await db.commit()'''

DB_13 = DB_V3 + TOP_USERS
DB_15 = DB_13 + ADD_QUESTION
DB_16 = DB_15 + QUESTIONS_PAGE
DB_17 = DB_16 + ALL_USERS
# 19-dars: questions.photo ustuni; get_questions photo'ni ham oladi.
DB_19 = (DB_17 + ADD_COLUMN).replace(
    '''            "score INTEGER, total INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        await db.commit()''',
    '''            "score INTEGER, total INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
''' + PHOTO_TABLES,
    1,
).replace('"SELECT id, text, a, b, c, d, correct FROM questions "', '"SELECT id, text, a, b, c, d, correct, photo FROM questions "')
DB_20 = DB_19.replace(PHOTO_TABLES, PHOTO_TABLES.replace("        await db.commit()", REMIND_TABLES), 1) + REMINDERS
DB_21 = DB_20.replace(REMIND_TABLES, REMIND_TABLES.replace("        await db.commit()", LANG_TABLES), 1) + LANG_DB
DB_22 = DB_21 + STATS_DB

CONFIG_14 = CONFIG.rstrip("\n") + '\nADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()}\n'

RATING = r'''
from aiogram import F, Router
from aiogram.types import Message

from database import top_users

router = Router()
MEDALS = ["🥇", "🥈", "🥉"]


@router.message(F.text == "📊 Reyting")
async def rating(message: Message):
    rows = await top_users()
    if not rows:
        await message.answer("Reyting hali bo'sh — birinchi bo'ling!")
        return
    lines = []
    for i, (name, ball, testlar) in enumerate(rows, start=1):
        belgi = MEDALS[i - 1] if i <= 3 else f"{i}."
        lines.append(f"{belgi} {name} — {ball} ball ({testlar} test)")
    await message.answer("📊 Top-10:\n" + "\n".join(lines))
'''

MENU_13 = MENU_FINAL.replace(
    r'''

@router.message(F.text == "📊 Reyting")
async def rating_button(message: Message):
    await message.answer("Reyting tez orada! ⏳")
''', "")

IS_ADMIN = r'''
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id in ADMIN_IDS
'''

ADMIN_KB = r'''
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="➕ Savol qo'shish", callback_data="adm:add")
    kb.button(text="📋 Savollar", callback_data="adm:list")
    kb.button(text="📣 Xabar yuborish", callback_data="adm:send")
    kb.button(text="📈 Statistika", callback_data="adm:stats")
    kb.adjust(2)
    return kb.as_markup()
'''

QUESTIONS_KB = r'''


def questions_kb(rows, page: int, pages: int):
    kb = InlineKeyboardBuilder()
    for qid, subject, text in rows:
        kb.button(text=f"🗑 {subject}: {text[:25]}", callback_data=f"qdel:{qid}:{page}")
    if page > 0:
        kb.button(text="◀", callback_data=f"qpage:{page - 1}")
    if page < pages - 1:
        kb.button(text="▶", callback_data=f"qpage:{page + 1}")
    kb.adjust(*([1] * len(rows)), 2)
    return kb.as_markup()
'''

ADMIN_14 = r'''
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.admin import IsAdmin
from keyboards.admin import admin_kb

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("🛠 Admin panel:", reply_markup=admin_kb())
'''

STATES_15 = STATES_FULL + r'''

class AddQuestion(StatesGroup):
    subject = State()
    text = State()
    options = State()
    correct = State()
'''

STATES_17 = STATES_15 + r'''

class Broadcast(StatesGroup):
    text = State()
'''

ADD_FLOW = r'''

@router.callback_query(F.data == "adm:add")
async def add_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddQuestion.subject)
    await callback.message.answer("Fan kodi (math / english / it):")
    await callback.answer()


@router.message(AddQuestion.subject, F.text.in_({"math", "english", "it"}))
async def add_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(AddQuestion.text)
    await message.answer("Savol matni:")


@router.message(AddQuestion.text, F.text)
async def add_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AddQuestion.options)
    await message.answer("4 ta variant, har biri yangi qatorda:")


@router.message(AddQuestion.options, F.text)
async def add_options(message: Message, state: FSMContext):
    variants = [v.strip() for v in message.text.split("\n") if v.strip()]
    if len(variants) != 4:
        await message.answer("Aynan 4 ta variant kerak")
        return
    await state.update_data(options=variants)
    await state.set_state(AddQuestion.correct)
    await message.answer("To'g'ri javob harfi (a, b, c yoki d):")


@router.message(AddQuestion.correct, F.text.lower().in_({"a", "b", "c", "d"}))
async def add_correct(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_question(data["subject"], data["text"], *data["options"], message.text.lower())
    await state.clear()
    await message.answer("✅ Savol qo'shildi")
'''

ADMIN_15 = ADMIN_14.replace(
    "from aiogram import Router\nfrom aiogram.filters import Command\nfrom aiogram.types import Message\n",
    "from aiogram import F, Router\nfrom aiogram.filters import Command\nfrom aiogram.fsm.context import FSMContext\n"
    "from aiogram.types import CallbackQuery, Message\n",
).replace(
    "from filters.admin import IsAdmin\n", "from database import add_question\nfrom filters.admin import IsAdmin\n"
).replace("from keyboards.admin import admin_kb\n", "from keyboards.admin import admin_kb\nfrom states import AddQuestion\n") + ADD_FLOW

PAGES_FLOW = r'''

PAGE = 5


async def show_page(message: Message, page: int, edit: bool = False):
    total, rows = await questions_page(page * PAGE, PAGE)
    pages = max(1, -(-total // PAGE))
    text = f"📋 Savollar: {total} ta · {page + 1}/{pages}-sahifa"
    markup = questions_kb(rows, page, pages)
    if edit:
        await message.edit_text(text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)


@router.callback_query(F.data == "adm:list")
async def list_questions(callback: CallbackQuery):
    await show_page(callback.message, 0)
    await callback.answer()


@router.callback_query(F.data.startswith("qpage:"))
async def turn_page(callback: CallbackQuery):
    await show_page(callback.message, int(callback.data.split(":")[1]), edit=True)
    await callback.answer()


@router.callback_query(F.data.startswith("qdel:"))
async def remove_question(callback: CallbackQuery):
    _, qid, page = callback.data.split(":")
    await delete_question(int(qid))
    await callback.answer("🗑 O'chirildi")
    await show_page(callback.message, int(page), edit=True)
'''

ADMIN_16 = ADMIN_15.replace(
    "from database import add_question\n", "from database import add_question, delete_question, questions_page\n"
).replace("from keyboards.admin import admin_kb\n", "from keyboards.admin import admin_kb, questions_kb\n") + PAGES_FLOW

SEND_FLOW = r'''

@router.callback_query(F.data == "adm:send")
async def send_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Broadcast.text)
    await callback.message.answer("Hammaga yuboriladigan xabarni yozing:")
    await callback.answer()


@router.message(Broadcast.text, F.text)
async def send_all(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    sent = failed = 0
    for user_id in await all_user_ids():
        try:
            await bot.send_message(user_id, message.text)
            sent += 1
        except TelegramForbiddenError:
            failed += 1
        await asyncio.sleep(0.05)
    await message.answer(f"📣 Yuborildi: {sent} · bloklagan: {failed}")
'''

ADMIN_17 = ("import asyncio\n\n" + ADMIN_16.lstrip("\n")).replace(
    "from aiogram import F, Router\n", "from aiogram import Bot, F, Router\nfrom aiogram.exceptions import TelegramForbiddenError\n"
).replace(
    "from database import add_question, delete_question, questions_page\n",
    "from database import add_question, all_user_ids, delete_question, questions_page\n",
).replace("from states import AddQuestion\n", "from states import AddQuestion, Broadcast\n") + SEND_FLOW

STATS_FLOW = r'''

@router.callback_query(F.data == "adm:stats")
async def show_stats(callback: CallbackQuery):
    s = await stats()
    await callback.message.answer(
        f"📈 Statistika\n👥 Foydalanuvchilar: {s['users']}\n"
        f"📝 Testlar: {s['tests']} (bugun {s['today']})\n🎯 O'rtacha natija: {s['avg']:.0f}%"
    )
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Ism", "Fan", "Ball", "Jami", "Vaqt"])
    writer.writerows(await attempts_rows())
    file = BufferedInputFile(buf.getvalue().encode("utf-8-sig"), filename="natijalar.csv")
    await callback.message.answer_document(file, caption="Barcha natijalar")
    await callback.answer()
'''

ADMIN_22 = ADMIN_17.replace("import asyncio\n", "import asyncio\nimport csv\nimport io\n", 1).replace(
    "from aiogram.types import CallbackQuery, Message\n", "from aiogram.types import BufferedInputFile, CallbackQuery, Message\n"
).replace(
    "from database import add_question, all_user_ids, delete_question, questions_page\n",
    "from database import add_question, all_user_ids, attempts_rows, delete_question, questions_page, stats\n",
) + STATS_FLOW

THROTTLE = r'''
import time

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 0.7):
        self.delay = delay
        self.last = {}

    async def __call__(self, handler, event: Message, data: dict):
        now = time.monotonic()
        user_id = event.from_user.id
        if now - self.last.get(user_id, 0) < self.delay:
            return None
        self.last[user_id] = now
        return await handler(event, data)
'''

LOG_MW = r'''
import logging

from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger("quizbot")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        logger.info("user=%s text=%r", event.from_user.id, event.text)
        return await handler(event, data)
'''

# --- handlers/quiz.py: 19-dars — rasmli savol va 30 soniya ------------------------------------------------
QUIZ_19 = QUIZ_V2.replace(
    "from aiogram import F, Router\n", "import time\n\nfrom aiogram import F, Router\n"
).replace(
    "router = Router()\n", "router = Router()\nLIMIT = 30  # soniya\n"
).replace(
    '''    await message.answer(
        f"❓ {index + 1}/{total}\\n\\n{question['text']}",
        reply_markup=answers_kb(question),
    )''',
    '''    caption = f"❓ {index + 1}/{total} · {LIMIT} soniya\\n\\n{question['text']}"
    if question.get("photo"):
        await message.answer_photo(question["photo"], caption=caption, reply_markup=answers_kb(question))
    else:
        await message.answer(caption, reply_markup=answers_kb(question))
    await state.update_data(asked_at=time.monotonic())''',
).replace(
    '''    if chosen == question["correct"]:
        score += 1''',
    '''    if time.monotonic() - data["asked_at"] > LIMIT:
        mark = f"⏰ Vaqt tugadi ({LIMIT} s)"
    elif chosen == question["correct"]:
        score += 1''',
)

SCHEDULER = r'''
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import reminder_user_ids


async def daily_reminder(bot: Bot):
    for user_id in await reminder_user_ids():
        try:
            await bot.send_message(user_id, "📝 Bugungi testni ishladingizmi? “📝 Test” tugmasini bosing!")
        except TelegramForbiddenError:
            continue


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    scheduler.add_job(daily_reminder, "cron", hour=19, minute=0, args=[bot])
    scheduler.start()
    return scheduler
'''

SETTINGS_20 = r'''
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import toggle_reminders

router = Router()


@router.message(Command("remind"))
async def remind(message: Message):
    holat = await toggle_reminders(message.from_user.id)
    await message.answer("🔔 Eslatma yoqildi" if holat else "🔕 Eslatma o'chirildi")
'''

TEXTS = r'''
TEXTS = {
    "uz": {
        "menu": "Menyudan tanlang:",
        "choose_lang": "Tilni tanlang:",
        "saved": "✅ Til saqlandi",
        "no_tests": "Hali test ishlamadingiz",
    },
    "ru": {
        "menu": "Выберите в меню:",
        "choose_lang": "Выберите язык:",
        "saved": "✅ Язык сохранён",
        "no_tests": "Вы ещё не проходили тест",
    },
}


def t(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["uz"]).get(key, TEXTS["uz"][key])
'''

SETTINGS_21 = SETTINGS_20.replace(
    "from aiogram import Router\n", "from aiogram import F, Router\n"
).replace(
    "from aiogram.types import Message\n", "from aiogram.types import CallbackQuery, Message\nfrom aiogram.utils.keyboard import InlineKeyboardBuilder\n"
).replace(
    "from database import toggle_reminders\n", "from database import get_lang, set_lang, toggle_reminders\nfrom texts import t\n"
) + r'''

@router.message(Command("lang"))
async def choose_lang(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O'zbekcha", callback_data="lang:uz")
    kb.button(text="🇷🇺 Русский", callback_data="lang:ru")
    lang = await get_lang(message.from_user.id)
    await message.answer(t(lang, "choose_lang"), reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("lang:"))
async def lang_chosen(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await set_lang(callback.from_user.id, lang)
    await callback.message.edit_text(t(lang, "saved"))
    await callback.answer()
'''

START_21 = r'''
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database import get_lang
from keyboards.menu import main_menu
from texts import t

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n{t(lang, 'menu')}",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("/start · /register · /lang · /remind · /admin")
'''

UTILS = r'''
def percent(score: int, total: int) -> int:
    if total <= 0:
        return 0
    return round(score / total * 100)


def grade(score: int, total: int) -> int:
    p = percent(score, total)
    if p >= 90:
        return 5
    if p >= 70:
        return 4
    if p >= 50:
        return 3
    return 2


if __name__ == "__main__":
    print(percent(8, 10), grade(8, 10))
    print(percent(0, 0), grade(3, 10))
'''

TEST_UTILS = r'''
from utils import grade, percent


def test_percent():
    assert percent(8, 10) == 80
    assert percent(0, 0) == 0


def test_grade_boundaries():
    assert grade(9, 10) == 5
    assert grade(7, 10) == 4
    assert grade(5, 10) == 3
    assert grade(4, 10) == 2
'''

ERRORS = r'''
import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger("quizbot")


@router.errors()
async def on_error(event: ErrorEvent):
    logger.exception("Xato: %s", event.exception)
    message = event.update.message
    if message:
        await message.answer("⚠️ Kutilmagan xato. Birozdan keyin urinib ko'ring.")
    return True
'''


def bot_py(routers: list[str], middlewares: bool = False, scheduler: bool = False, file_log: bool = False) -> str:
    """bot.py ning shu darsdagi ko'rinishi (routerlar tartibi muhim)."""
    imports = ["import asyncio", "import logging", "", "from aiogram import Bot, Dispatcher", ""]
    imports += ["from config import BOT_TOKEN", "from database import create_tables"]
    imports.append("from handlers import " + ", ".join(sorted(routers)))
    if middlewares:
        imports.append("from middlewares.logging import LoggingMiddleware")
        imports.append("from middlewares.throttling import ThrottlingMiddleware")
    if scheduler:
        imports.append("from scheduler import setup_scheduler")
    body = ["", "", "async def main():"]
    if file_log:
        body += [
            "    logging.basicConfig(",
            "        level=logging.INFO,",
            '        format="%(asctime)s %(levelname)s %(name)s: %(message)s",',
            '        handlers=[logging.StreamHandler(), logging.FileHandler("bot.log", encoding="utf-8")],',
            "    )",
        ]
    else:
        body.append("    logging.basicConfig(level=logging.INFO)")
    body += ["    await create_tables()", "    bot = Bot(token=BOT_TOKEN)", "    dp = Dispatcher()"]
    if middlewares:
        body += ["    dp.message.middleware(LoggingMiddleware())", "    dp.message.middleware(ThrottlingMiddleware())"]
    body.append("    dp.include_routers(" + ", ".join(f"{r}.router" for r in routers) + ")")
    if scheduler:
        body.append("    setup_scheduler(bot)")
    body += ["    await dp.start_polling(bot)", "", "", 'if __name__ == "__main__":', "    asyncio.run(main())", ""]
    return "\n".join(imports + body)


R6 = ["start", "register", "menu", "quiz"]
BOT_13 = bot_py(["start", "register", "rating", "menu", "quiz"])
BOT_14 = bot_py(["admin", "start", "register", "rating", "menu", "quiz"])
BOT_18 = bot_py(["admin", "start", "register", "rating", "menu", "quiz"], middlewares=True, file_log=True)
BOT_20 = bot_py(["admin", "settings", "start", "register", "rating", "menu", "quiz"], True, True, True)
BOT_23 = bot_py(["errors", "admin", "settings", "start", "register", "rating", "menu", "quiz"], True, True, True)

ADMIN_CHAT = [("user", "/admin"), ("bot", "🛠 Admin panel:", ["➕ Savol qo'shish", "📋 Savollar", "📣 Xabar yuborish", "📈 Statistika"])]

LESSONS = {
    "TB13": lesson(
        M, 1, "SQL: ORDER BY, LIMIT, JOIN — reyting",
        "Eng ko'p ball to'plagan 10 o'quvchini medallar bilan ko'rsatamiz.",
        "6-oyda: users, questions, attempts jadvallari.",
        "attempts jadvalida qanday ustunlar bor?",
        "JOIN — ikki jadvalni bog'lash; GROUP BY + SUM; ORDER BY ... DESC; LIMIT; alias (a, u).",
        "Reyting ostida foydalanuvchining o'z o'rnini ko'rsating.",
        [("📝", "attempts", "score, user_id", ""),
         ("🔗", "JOIN users", "ismni olish", "mem"),
         ("➕", "SUM + GROUP BY", "har o'quvchi", ""),
         ("⬇", "ORDER BY DESC", "kattadan", ""),
         ("🥇", "Top-10", "medallar", "")],
        [
            step("database.py", "JOIN bilan reyting so'rovi", TOP_USERS,
                 [("JOIN ... ON", "attempts.user_id = users.id — ismni boshqa jadvaldan olamiz."),
                  ("SUM(a.score)", "har o'quvchining jami bali; GROUP BY a.user_id bilan."),
                  ("a, u", "jadval taxalluslari — so'rov qisqaroq.")],
                 "[('Laylo', 47, 5), ('Ali', 38, 4), ...]"),
            step("handlers/rating.py", "Medallar bilan chiqarish", RATING,
                 [("MEDALS[i - 1]", "birinchi uchtaga medal, qolganlarga raqam."),
                  ("enumerate(..., start=1)", "o'rin raqami."),
                  ("bo'sh reyting", "hali test bo'lmasa — chiroyli xabar.")],
                 "📊 Top-10:\n🥇 Laylo — 47 ball (5 test)\n🥈 Ali — 38 ball (4 test)"),
            step("bot.py", "Routerni ulaymiz", r'''
from handlers import menu, quiz, rating, register, start
...
    dp.include_routers(start.router, register.router, rating.router, menu.router, quiz.router)''',
                 [("rating.router", "yangi fayl — yangi router."),
                  ("menu.py", "eski “tez orada” javobini olib tashlaymiz.")],
                 "📊 Reyting tugmasi endi haqiqiy reytingni ko'rsatadi", new=[1, 3]),
        ],
        {"database.py": DB_13, "handlers/rating.py": RATING, "handlers/menu.py": MENU_13, "bot.py": BOT_13},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── database.py", "o‘zgardi"), ("└── handlers/", ""), ("    ├── rating.py", "yangi"), ("    └── menu.py", "o‘zgardi")],
        ["JOIN", "GROUP BY va SUM", "ORDER BY DESC, LIMIT", "Jadval taxalluslari"],
        ["Majburiy: reyting ostida foydalanuvchining o'z o'rnini ko'rsating.",
         "Qo'shimcha: fan bo'yicha reyting (WHERE a.subject = ?)."],
        "7.2 · Filtrlar va admin huquqi.",
        chat=[("user", "📊 Reyting"), ("bot", "📊 Top-10:\n🥇 Laylo — 47 ball (5 test)\n🥈 Ali — 38 ball (4 test)\n🥉 Vali — 30 ball (4 test)\n4. Sardor — 21 ball (3 test)")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="📊 Reyting",
        checks=["Reyting ball bo'yicha kamayish tartibidami?", "Birinchi uchtada medal bormi?"],
    ),
    "TB14": lesson(
        M, 2, "Filtrlar va admin huquqi",
        "/admin paneli faqat admin uchun ochiladi — o'z filtrimizni yozamiz.",
        "O'tgan darsda: JOIN va reyting.",
        "F.text == \"...\" filtri qanday ishlaydi?",
        "BaseFilter — o'z filtrimiz; ADMIN_IDS .env'dan; router.message.filter(...) — butun routerga filtr.",
        "Bir nechta admin ID'ni .env'dan o'qing va sinab ko'ring.",
        [("⚙", ".env", "ADMIN_IDS=111,222", ""),
         ("🛡", "IsAdmin", "BaseFilter", "mem"),
         ("📂", "admin router", "filter(IsAdmin())", ""),
         ("🛠", "/admin", "panel tugmalari", "")],
        [
            step("config.py", "Adminlar ro'yxati", r'''
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()}''',
                 [("set", "tez tekshirish: user_id in ADMIN_IDS."),
                  (".env", "ADMIN_IDS=111,222 — kodni o'zgartirmasdan admin qo'shish.")],
                 "ADMIN_IDS = {111, 222}"),
            step("filters/admin.py", "O'z filtrimiz", IS_ADMIN,
                 [("BaseFilter", "__call__ True qaytarsa — handler ishlaydi."),
                  ("Message | CallbackQuery", "xabar va tugma uchun ham ishlaydi.")],
                 "IsAdmin()(xabar) → True / False"),
            step("handlers/admin.py", "Admin router va panel", ADMIN_14,
                 [("router.message.filter", "routerdagi hamma handlerlarga bitta filtr."),
                  ("callback_query.filter", "admin tugmalari ham faqat adminga."),
                  ("oddiy foydalanuvchi", "/admin yozsa — hech narsa bo'lmaydi.")],
                 "🛠 Admin panel:\n[➕ Savol qo'shish] [📋 Savollar] ..."),
        ],
        {"config.py": CONFIG_14, "filters/__init__.py": "", "filters/admin.py": IS_ADMIN, "keyboards/admin.py": ADMIN_KB, "handlers/admin.py": ADMIN_14, "bot.py": BOT_14},
        [("quizbot/", ""), ("├── config.py", "o‘zgardi"), ("├── filters/", "yangi"), ("│   └── admin.py", "yangi"), ("├── handlers/", ""), ("│   └── admin.py", "yangi"), ("└── keyboards/", ""), ("    └── admin.py", "yangi")],
        ["BaseFilter", "ADMIN_IDS .env'dan", "Routerga umumiy filtr", "Admin paneli"],
        ["Majburiy: 2 ta admin ID bilan sinab ko'ring.",
         "Qo'shimcha: /whoami — foydalanuvchiga o'z ID'sini ko'rsatish."],
        "7.3 · Admin: FSM bilan savol qo'shish.",
        chat=ADMIN_CHAT,
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="admin va oddiy foydalanuvchi",
        checks=["Admin /admin'da panelni ko'rdimi?", "Oddiy foydalanuvchiga panel chiqmadimi?"],
    ),
    "TB15": lesson(
        M, 3, "Admin: FSM bilan savol qo'shish",
        "Admin bot ichidan yangi savol qo'shadi: fan → matn → 4 variant → to'g'ri javob.",
        "O'tgan darsda: IsAdmin filtri, admin panel.",
        "router.message.filter(IsAdmin()) nima qiladi?",
        "FSM takrorlash (AddQuestion), F.text.in_ va lower(), ko'p qatorli kiritish, *data[\"options\"] bilan ochish.",
        "Savol qo'shishdan oldin “Tasdiqlaysizmi?” tugmasini qo'shing.",
        [("➕", "adm:add", "boshlash", ""),
         ("📚", "Fan", "math / english / it", "loop"),
         ("❓", "Matn", "savol", "loop"),
         ("🔤", "4 variant", "har qatorda", "loop"),
         ("✅", "To'g'ri harf", "add_question()", "mem")],
        [
            step("handlers/admin.py", "Fan va matn", r'''
@router.callback_query(F.data == "adm:add")
async def add_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddQuestion.subject)
    await callback.message.answer("Fan kodi (math / english / it):")
    await callback.answer()


@router.message(AddQuestion.subject, F.text.in_({"math", "english", "it"}))
async def add_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(AddQuestion.text)
    await message.answer("Savol matni:")''',
                 [("F.text.in_({...})", "faqat ruxsat etilgan fan kodlari qabul qilinadi."),
                  ("AddQuestion.subject", "4 bosqichli yangi FSM.")],
                 "Fan kodi: math\nSavol matni:"),
            step("handlers/admin.py", "4 ta variant", r'''
@router.message(AddQuestion.options, F.text)
async def add_options(message: Message, state: FSMContext):
    variants = [v.strip() for v in message.text.split("\n") if v.strip()]
    if len(variants) != 4:
        await message.answer("Aynan 4 ta variant kerak")
        return
    await state.update_data(options=variants)
    await state.set_state(AddQuestion.correct)
    await message.answer("To'g'ri javob harfi (a, b, c yoki d):")''',
                 [("split(\"\\n\")", "har qator — bitta variant."),
                  ("len != 4", "noto'g'ri bo'lsa holat o'zgarmaydi — qayta so'raymiz.")],
                 "54\n56\n64\n48 → To'g'ri javob harfi:"),
            step("handlers/admin.py", "Saqlash", r'''
@router.message(AddQuestion.correct, F.text.lower().in_({"a", "b", "c", "d"}))
async def add_correct(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_question(data["subject"], data["text"], *data["options"], message.text.lower())
    await state.clear()
    await message.answer("✅ Savol qo'shildi")''',
                 [("F.text.lower()", "“B” ham, “b” ham qabul qilinadi."),
                  ("*data[\"options\"]", "4 ta variant 4 ta argument bo'lib uzatiladi.")],
                 "✅ Savol qo'shildi"),
        ],
        {"database.py": DB_15, "states.py": STATES_15, "handlers/admin.py": ADMIN_15},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("├── states.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── admin.py", "o‘zgardi")],
        ["Ko'p bosqichli FSM", "F.text.in_ va lower()", "Ko'p qatorli kiritish", "*args bilan ochish"],
        ["Majburiy: saqlashdan oldin “Tasdiqlaysizmi?” tugmasini qo'shing.",
         "Qo'shimcha: /cancel bilan qo'shishni bekor qilish."],
        "7.4 · Admin: savollarni boshqarish va sahifalash.",
        chat=[("bot", "Fan kodi (math / english / it):"), ("user", "math"), ("bot", "Savol matni:"), ("user", "9 × 6 = ?"), ("bot", "4 ta variant, har biri yangi qatorda:"), ("user", "54\n56\n63\n45"), ("bot", "To'g'ri javob harfi (a, b, c yoki d):"), ("user", "A"), ("bot", "✅ Savol qo'shildi")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="➕ Savol qo'shish",
        checks=["3 ta variant rad etildimi?", "Katta “A” ham qabul qilindimi?", "Savol testda chiqdimi?"],
    ),
    "TB16": lesson(
        M, 4, "Admin: savollarni boshqarish va sahifalash",
        "Savollar ko'p — ularni 5 tadan sahifalab ko'rsatamiz va o'chiramiz.",
        "O'tgan darsda: FSM bilan savol qo'shish.",
        "F.text.lower().in_({...}) nimaga kerak edi?",
        "LIMIT ... OFFSET — sahifalash; sahifalar soni (yuqoriga yaxlitlash); callback_data'da bir nechta qiymat; edit_text bilan sahifani almashtirish.",
        "Savollarni fan bo'yicha filtrlash tugmalarini qo'shing.",
        [("📋", "adm:list", "1-sahifa", ""),
         ("🔢", "LIMIT · OFFSET", "5 tadan", "mem"),
         ("◀ ▶", "qpage:N", "sahifa almashtirish", "loop"),
         ("🗑", "qdel:id:sahifa", "o'chirish", ""),
         ("🔄", "edit_text", "o'sha sahifa", "")],
        [
            step("database.py", "Sahifa so'rovi", QUESTIONS_PAGE,
                 [("LIMIT ? OFFSET ?", "5 ta qator, oldingi sahifalarni o'tkazib."),
                  ("(total,) = ...", "bitta qiymatli qatorni ochish."),
                  ("DELETE ... WHERE id = ?", "bitta savolni o'chirish.")],
                 "questions_page(5) → (23, [(18, 'math', '9 × 6 = ?'), ...])"),
            step("keyboards/admin.py", "Sahifa tugmalari", QUESTIONS_KB,
                 [("qdel:{qid}:{page}", "o'chirgach o'sha sahifaga qaytish uchun sahifa ham saqlanadi."),
                  ("◀ / ▶", "faqat kerak bo'lganda chiqadi."),
                  ("adjust(1, 1, ..., 2)", "savollar ustma-ust, strelkalar yonma-yon.")],
                 "[🗑 math: 9 × 6 = ?] ... [◀] [▶]"),
            step("handlers/admin.py", "Sahifani ko'rsatuvchi funksiya", PAGES_FLOW.split("\n\n\n@router")[0],
                 [("-(-total // PAGE)", "yuqoriga yaxlitlash: 23 ta → 5 sahifa."),
                  ("edit=True", "yangi xabar emas — o'sha xabar yangilanadi."),
                  ("bitta funksiya", "ro'yxat, varaqlash va o'chirishdan keyin — 3 joyda ishlatiladi.")],
                 "📋 Savollar: 23 ta · 2/5-sahifa"),
            step("handlers/admin.py", "Varaqlash va o'chirish", "@router" + PAGES_FLOW.split("\n\n\n@router", 1)[1],
                 [("qpage:N", "sahifa raqami callback'da keladi."),
                  ("_, qid, page = split", "qdel:18:2 → id va qaytish sahifasi."),
                  ("callback.answer(\"🗑 ...\")", "qisqa bildirishnoma oynasi.")],
                 "🗑 O'chirildi → 📋 Savollar: 22 ta · 2/5-sahifa"),
        ],
        {"database.py": DB_16, "keyboards/admin.py": ADMIN_KB + QUESTIONS_KB, "handlers/admin.py": ADMIN_16},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("├── handlers/", ""), ("│   └── admin.py", "o‘zgardi"), ("└── keyboards/", ""), ("    └── admin.py", "o‘zgardi")],
        ["LIMIT va OFFSET", "Sahifalar sonini hisoblash", "callback_data'da bir nechta qiymat", "edit_text bilan sahifalash"],
        ["Majburiy: fan bo'yicha filtr tugmalari (math / english / it).",
         "Qo'shimcha: o'chirishdan oldin “Rostdan ham?” tasdig'i."],
        "7.5 · Hammaga xabar (broadcast).",
        chat=[("user", "📋 Savollar"), ("bot", "📋 Savollar: 23 ta · 1/5-sahifa", ["🗑 math: 9 × 6 = ?", "🗑 it: Python fayli kengaytmasi?", "▶"]), ("bot", "🗑 O'chirildi → 📋 Savollar: 22 ta · 1/5-sahifa")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="📋 Savollar → ▶ → 🗑",
        checks=["▶ bosilganda xabar o'zgardimi (yangisi kelmadimi)?", "O'chirgach o'sha sahifada qoldimi?"],
    ),
    "TB17": lesson(
        M, 5, "Hammaga xabar (broadcast)",
        "Admin bitta xabarni barcha foydalanuvchilarga yuboradi — botni bloklaganlarni hisobga olib.",
        "O'tgan darsda: sahifalash va o'chirish.",
        "OFFSET nima qiladi?",
        "bot.send_message(user_id, ...), handler'da bot parametri, TelegramForbiddenError, asyncio.sleep — Telegram limitlari.",
        "Yuborishdan oldin xabar ko'rinishini ko'rsatib, tasdiq so'rang.",
        [("📣", "adm:send", "Broadcast.text", ""),
         ("👥", "all_user_ids()", "hamma id", "mem"),
         ("✉", "send_message", "har biriga", "loop"),
         ("🚫", "Forbidden", "bloklagan", ""),
         ("📊", "Hisobot", "yuborildi / xato", "")],
        [
            step("database.py", "Barcha foydalanuvchilar", ALL_USERS,
                 [("list comprehension", "qatorlardan faqat id'larni olamiz.")],
                 "[111, 222, 333, ...]"),
            step("handlers/admin.py", "Yuborish va xatolarni ushlash", SEND_FLOW,
                 [("bot: Bot", "aiogram botni handler'ga o'zi uzatadi."),
                  ("TelegramForbiddenError", "foydalanuvchi botni bloklagan — dastur to'xtamaydi."),
                  ("sleep(0.05)", "sekundiga ~20 ta — Telegram limitidan oshmaymiz.")],
                 "📣 Yuborildi: 41 · bloklagan: 3"),
        ],
        {"database.py": DB_17, "states.py": STATES_17, "handlers/admin.py": ADMIN_17},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("├── states.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── admin.py", "o‘zgardi")],
        ["bot.send_message", "TelegramForbiddenError", "Telegram limitlari va sleep", "Hisobot"],
        ["Majburiy: yuborishdan oldin ko'rinish va [Yuborish] [Bekor] tugmalari.",
         "Qo'shimcha: rasmli xabar yuborish (message.photo)."],
        "7.6 · Middleware va logging.",
        chat=ADMIN_CHAT + [("bot", "Hammaga yuboriladigan xabarni yozing:"), ("user", "Ertaga test 10:00 da!"), ("bot", "📣 Yuborildi: 41 · bloklagan: 3")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="📣 Xabar yuborish",
        checks=["Bot bloklangan foydalanuvchida to'xtab qolmadimi?", "Hisobot sonlari to'g'rimi?"],
    ),
    "TB18": lesson(
        M, 6, "Middleware va logging",
        "Har xabar handler'dan oldin tekshiriladi: log yoziladi va spam to'xtatiladi.",
        "O'tgan darsda: broadcast va xatolarni ushlash.",
        "TelegramForbiddenError qachon chiqadi?",
        "Middleware — handler oldidan ishlovchi qatlam; BaseMiddleware.__call__(handler, event, data); logging faylga; throttling.",
        "Log'ga foydalanuvchi ismini ham qo'shing.",
        [("💬", "Xabar", "Telegram'dan", ""),
         ("📝", "LoggingMiddleware", "bot.log", "mem"),
         ("⏱", "Throttling", "0.7 s", ""),
         ("🎯", "Handler", "odatdagidek", "")],
        [
            step("middlewares/logging.py", "Har xabarni yozamiz", LOG_MW,
                 [("BaseMiddleware", "__call__ — har xabar uchun chaqiriladi."),
                  ("await handler(event, data)", "keyingi qatlamga (handler'ga) uzatish."),
                  ("%r", "matnni qo'shtirnoq bilan — bo'sh xabar ham ko'rinadi.")],
                 "2026-11-19 15:42:10 INFO quizbot: user=111 text='📝 Test'"),
            step("middlewares/throttling.py", "Spamdan himoya", THROTTLE,
                 [("self.last", "har foydalanuvchining oxirgi xabar vaqti."),
                  ("return None", "handler chaqirilmaydi — xabar e'tiborsiz qoladi."),
                  ("monotonic()", "soat o'zgarsa ham to'g'ri o'lchaydigan vaqt.")],
                 "0.3 s ichida 5 ta xabar → faqat 1 tasi ishlanadi"),
            step("bot.py", "Ulash va faylga log", r'''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("bot.log", encoding="utf-8")],
    )''',
                 [("FileHandler", "log terminalga ham, bot.log fayliga ham yoziladi."),
                  ("dp.message.middleware(...)", "faqat xabarlar uchun; tartib — yozilgan tartibda.")],
                 "bot.log fayli paydo bo'ldi"),
        ],
        {"middlewares/__init__.py": "", "middlewares/logging.py": LOG_MW, "middlewares/throttling.py": THROTTLE, "bot.py": BOT_18},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── bot.log", "yangi"), ("└── middlewares/", "yangi"), ("    ├── logging.py", "yangi"), ("    └── throttling.py", "yangi")],
        ["Middleware tushunchasi", "BaseMiddleware", "Faylga logging", "Throttling"],
        ["Majburiy: log'ga foydalanuvchi ismini qo'shing.",
         "Qo'shimcha: throttling'da “Sekinroq 🙂” deb bir marta javob bering."],
        "7.7 · Media va vaqt chegarasi.",
    ),
    "TB19": lesson(
        M, 7, "Media va vaqt chegarasi",
        "Savollarga rasm qo'shamiz va har savolga 30 soniya beramiz.",
        "O'tgan darsda: middleware, logging, throttling.",
        "Middleware handler'dan oldin yoki keyin ishlaydimi?",
        "ALTER TABLE bilan yangi ustun (PRAGMA table_info); answer_photo va file_id; time.monotonic bilan vaqtni o'lchash.",
        "Vaqt tugaganda qolgan soniyalarni savol matnida ko'rsating.",
        [("🖼", "photo ustuni", "file_id", ""),
         ("🛠", "add_column()", "ALTER TABLE", "mem"),
         ("📸", "answer_photo", "rasm + tugmalar", ""),
         ("⏱", "asked_at", "monotonic()", "loop"),
         ("⏰", "> 30 s", "javob hisoblanmaydi", "")],
        [
            step("database.py", "Ustunni xavfsiz qo'shish", ADD_COLUMN,
                 [("PRAGMA table_info", "jadvaldagi ustunlar ro'yxati."),
                  ("ALTER TABLE ... ADD COLUMN", "eski ma'lumot saqlangan holda yangi ustun."),
                  ("create_tables ichida", "har ishga tushishda tekshiriladi — ikkinchi marta qo'shilmaydi.")],
                 "questions: ... correct, photo"),
            step("handlers/quiz.py", "Rasm yoki matn", r'''
    caption = f"❓ {index + 1}/{total} · {LIMIT} soniya\n\n{question['text']}"
    if question.get("photo"):
        await message.answer_photo(question["photo"], caption=caption, reply_markup=answers_kb(question))
    else:
        await message.answer(caption, reply_markup=answers_kb(question))
    await state.update_data(asked_at=time.monotonic())''',
                 [("file_id", "Telegram serveridagi rasm — qayta yuklash shart emas."),
                  ("caption", "rasm ostidagi matn."),
                  ("asked_at", "savol yuborilgan vaqt FSM'da.")],
                 "🖼 + ❓ 3/10 · 30 soniya"),
            step("handlers/quiz.py", "Vaqtni tekshirish", r'''
    if time.monotonic() - data["asked_at"] > LIMIT:
        mark = f"⏰ Vaqt tugadi ({LIMIT} s)"
    elif chosen == question["correct"]:
        score += 1''',
                 [("farq > LIMIT", "kechikkan javob ball bermaydi."),
                  ("elif", "vaqt tugamagan bo'lsagina to'g'riligi tekshiriladi.")],
                 "7 × 8 = ?\n\n⏰ Vaqt tugadi (30 s)"),
        ],
        {"database.py": DB_19, "handlers/quiz.py": QUIZ_19},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── quiz.py", "o‘zgardi")],
        ["ALTER TABLE va PRAGMA", "answer_photo, file_id", "time.monotonic()", "Vaqt chegarasi"],
        ["Majburiy: savolda qolgan vaqtni ko'rsating.",
         "Qo'shimcha: admin savol qo'shishda rasm ham yubora olsin."],
        "7.8 · Rejalashtirilgan vazifalar: APScheduler.",
        chat=[("bot", "🖼 ❓ 3/10 · 30 soniya\n\nRasmda nechta uchburchak bor?", ["4", "5", "6", "8"]), ("bot", "Rasmda nechta uchburchak bor?\n\n⏰ Vaqt tugadi (30 s)")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="rasmli savol va vaqt",
        checks=["Rasm tugmalar bilan birga chiqdimi?", "30 soniyadan keyingi javob ball bermadimi?"],
    ),
    "TB20": lesson(
        M, 8, "Rejalashtirilgan vazifalar: APScheduler",
        "Bot har kuni 19:00 da eslatma yuboradi; foydalanuvchi /remind bilan o'chirib-yoqadi.",
        "O'tgan darsda: rasmli savollar va vaqt chegarasi.",
        "add_column() nima uchun kerak?",
        "AsyncIOScheduler, cron trigger, vaqt zonasi Asia/Tashkent; reminders ustuni; 1 - reminders bilan almashtirish.",
        "Foydalanuvchi eslatma vaqtini o'zi tanlay olsin (18:00 / 19:00 / 20:00).",
        [("⏰", "cron 19:00", "Asia/Tashkent", "mem"),
         ("👥", "reminders = 1", "kimga", ""),
         ("✉", "daily_reminder", "xabar", "loop"),
         ("🔔", "/remind", "yoqish / o'chirish", "")],
        [
            step("scheduler.py", "Kunlik vazifa", SCHEDULER,
                 [("AsyncIOScheduler", "aiogram bilan bir event loop'da ishlaydi."),
                  ("\"cron\", hour=19", "har kuni 19:00 da."),
                  ("timezone", "server boshqa mamlakatda bo'lsa ham Toshkent vaqti.")],
                 "19:00 → 📝 Bugungi testni ishladingizmi?"),
            step("database.py", "Eslatma sozlamasi", REMINDERS,
                 [("1 - reminders", "1 → 0, 0 → 1: bitta so'rov bilan almashtirish."),
                  ("WHERE reminders = 1", "faqat yoqqanlarga yuboramiz.")],
                 "toggle_reminders(111) → 0"),
            step("handlers/settings.py", "/remind buyrug'i", SETTINGS_20,
                 [("yangi router", "sozlamalar alohida faylda."),
                  ("javob", "holatga qarab 🔔 yoki 🔕.")],
                 "/remind → 🔕 Eslatma o'chirildi"),
        ],
        {"database.py": DB_20, "scheduler.py": SCHEDULER, "handlers/settings.py": SETTINGS_20, "bot.py": BOT_20,
         "requirements.txt": "aiogram==3.31.0\naiosqlite==0.21.0\npython-dotenv==1.0.1\napscheduler==3.10.4\n"},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── scheduler.py", "yangi"), ("├── database.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── settings.py", "yangi")],
        ["APScheduler va cron", "Vaqt zonasi", "Sozlamani almashtirish", "Rejalashtirilgan xabar"],
        ["Majburiy: eslatma vaqtini tanlash (18/19/20).",
         "Qo'shimcha: dushanba kuni haftalik natija xulosasini yuboring."],
        "7.9 · Ikki tilli bot: o'zbek va rus.",
        chat=[("bot", "📝 Bugungi testni ishladingizmi? “📝 Test” tugmasini bosing!"), ("user", "/remind"), ("bot", "🔕 Eslatma o'chirildi"), ("user", "/remind"), ("bot", "🔔 Eslatma yoqildi")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="eslatma va /remind",
        checks=["Eslatma belgilangan vaqtda keldimi (sinov uchun 1 daqiqadan keyin)?", "/remind holatni almashtirdimi?"],
    ),
    "TB21": lesson(
        M, 9, "Ikki tilli bot: o'zbek va rus",
        "Foydalanuvchi tilni tanlaydi, bot matnlari shu tilda chiqadi.",
        "O'tgan darsda: APScheduler va /remind.",
        "1 - reminders qanday ishlaydi?",
        "Matnlar lug'ati (TEXTS), t(lang, key) yordamchisi; lang ustuni; INSERT OR IGNORE + UPDATE; tilni callback bilan tanlash.",
        "Profilda tilni almashtirish tugmasini qo'shing.",
        [("🌐", "/lang", "🇺🇿 / 🇷🇺", ""),
         ("💾", "set_lang()", "users.lang", "mem"),
         ("📖", "TEXTS", "uz · ru", ""),
         ("🔤", "t(lang, key)", "kerakli matn", ""),
         ("👋", "/start", "tanlangan tilda", "")],
        [
            step("texts.py", "Matnlar lug'ati", TEXTS,
                 [("TEXTS[lang][key]", "har til uchun bir xil kalitlar."),
                  ("t()", "til yoki kalit yo'q bo'lsa — o'zbekcha."),
                  ("kodda matn yo'q", "yangi til qo'shish — faqat lug'atga.")],
                 "t(\"ru\", \"menu\") → Выберите в меню:"),
            step("database.py", "Tilni saqlash", LANG_DB,
                 [("INSERT OR IGNORE", "ro'yxatdan o'tmagan bo'lsa ham qator yaratiladi."),
                  ("standart \"uz\"", "til tanlanmagan bo'lsa.")],
                 "set_lang(111, \"ru\") → users.lang = 'ru'"),
            step("handlers/settings.py", "Til tanlash tugmalari", r'''
@router.message(Command("lang"))
async def choose_lang(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O'zbekcha", callback_data="lang:uz")
    kb.button(text="🇷🇺 Русский", callback_data="lang:ru")
    lang = await get_lang(message.from_user.id)
    await message.answer(t(lang, "choose_lang"), reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith("lang:"))
async def lang_chosen(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await set_lang(callback.from_user.id, lang)
    await callback.message.edit_text(t(lang, "saved"))
    await callback.answer()''',
                 [("lang:uz / lang:ru", "callback'da til kodi."),
                  ("edit_text(t(lang, ...))", "javob darhol yangi tilda.")],
                 "🇷🇺 → ✅ Язык сохранён"),
        ],
        {"texts.py": TEXTS, "database.py": DB_21, "handlers/settings.py": SETTINGS_21, "handlers/start.py": START_21},
        [("quizbot/", ""), ("├── texts.py", "yangi"), ("├── database.py", "o‘zgardi"), ("└── handlers/", ""), ("    ├── settings.py", "o‘zgardi"), ("    └── start.py", "o‘zgardi")],
        ["Matnlar lug'ati", "t(lang, key)", "Tilni bazada saqlash", "Callback bilan sozlama"],
        ["Majburiy: profilda tilni almashtirish tugmasi.",
         "Qo'shimcha: menyu tugmalarini ham ikki tilda qiling."],
        "7.10 · Admin statistikasi va CSV hisobot.",
        chat=[("user", "/lang"), ("bot", "Tilni tanlang:", ["🇺🇿 O'zbekcha", "🇷🇺 Русский"]), ("bot", "✅ Язык сохранён"), ("user", "/start"), ("bot", "Salom, Ali! 👋\nВыберите в меню:")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="/lang → 🇷🇺 → /start",
        checks=["Til tanlangach javob o'sha tilda keldimi?", "Bot qayta ishga tushganda til saqlandimi?"],
    ),
    "TB22": lesson(
        M, 10, "Admin statistikasi va CSV hisobot",
        "Admin bir tugma bilan statistika va barcha natijalar faylini oladi.",
        "O'tgan darsda: ikki tilli bot.",
        "t(\"ru\", \"menu\") nima qaytaradi?",
        "Agregat so'rovlar (COUNT, AVG, ichki SELECT), COALESCE; csv moduli; StringIO; BufferedInputFile va answer_document.",
        "Hisobotga eng faol 3 foydalanuvchini qo'shing.",
        [("📈", "adm:stats", "tugma", ""),
         ("🔢", "stats()", "COUNT, AVG", "mem"),
         ("📄", "csv.writer", "StringIO", ""),
         ("📎", "answer_document", "natijalar.csv", "")],
        [
            step("database.py", "Statistika so'rovi", STATS_DB,
                 [("(SELECT COUNT(*) FROM users)", "ichki so'rov — boshqa jadvaldan son."),
                  ("COALESCE(x, 0)", "test bo'lmasa NULL o'rniga 0."),
                  ("DATE('now')", "bugungi testlar.")],
                 "{'users': 44, 'tests': 128, 'avg': 71.4, 'today': 9}"),
            step("handlers/admin.py", "Xabar va CSV fayl", STATS_FLOW,
                 [("io.StringIO()", "faylni diskka yozmasdan xotirada yig'amiz."),
                  ("utf-8-sig", "Excel o'zbekcha/ruscha harflarni to'g'ri ochadi."),
                  ("BufferedInputFile", "baytlarni Telegram'ga fayl qilib yuborish.")],
                 "📈 Statistika\n👥 Foydalanuvchilar: 44\n📝 Testlar: 128 (bugun 9)\n🎯 O'rtacha natija: 71%\n📎 natijalar.csv"),
        ],
        {"database.py": DB_22, "handlers/admin.py": ADMIN_22},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── admin.py", "o‘zgardi")],
        ["Agregat so'rovlar", "COALESCE", "csv va StringIO", "Fayl yuborish"],
        ["Majburiy: eng faol 3 foydalanuvchini hisobotga qo'shing.",
         "Qo'shimcha: CSV'ga foiz ustunini qo'shing."],
        "7.11 · Xatolarni ushlash va pytest.",
        chat=ADMIN_CHAT + [("bot", "📈 Statistika\n👥 Foydalanuvchilar: 44\n📝 Testlar: 128 (bugun 9)\n🎯 O'rtacha natija: 71%"), ("bot", "📎 natijalar.csv — Barcha natijalar")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="📈 Statistika",
        checks=["Sonlar bazadagi ma'lumotga mosmi?", "CSV Excel'da harflar buzilmay ochildimi?"],
    ),
    "TB23": lesson(
        M, 11, "Xatolarni ushlash va pytest",
        "Kutilmagan xato botni to'xtatmasin; muhim funksiyalarni avtomatik testlar bilan tekshiramiz.",
        "O'tgan darsda: statistika va CSV.",
        "COALESCE nima uchun kerak?",
        "@router.errors() — umumiy xato handleri; logger.exception; sof funksiyalar (utils.py); pytest: assert, test_ funksiyalar.",
        "grade() ga 3 ta yangi chegaraviy test yozing.",
        [("💥", "Xato", "handler ichida", ""),
         ("🛡", "@router.errors()", "ushlaydi", "mem"),
         ("📝", "logger.exception", "bot.log", ""),
         ("🧪", "pytest", "utils testlari", "")],
        [
            step("handlers/errors.py", "Umumiy xato handleri", ERRORS,
                 [("@router.errors()", "har qanday handler'dagi xato shu yerga keladi."),
                  ("logger.exception", "to'liq traceback log'ga yoziladi."),
                  ("return True", "xato hal qilindi — bot ishlashda davom etadi.")],
                 "⚠️ Kutilmagan xato. Birozdan keyin urinib ko'ring."),
            step("utils.py", "Sof funksiyalar", UTILS,
                 [("sof funksiya", "faqat argumentga bog'liq — test qilish oson."),
                  ("total <= 0", "nolga bo'lishdan himoya.")],
                 "80 4\n0 2"),
            step("tests/test_utils.py", "pytest testlari", TEST_UTILS,
                 [("test_ bilan boshlanadi", "pytest shunday funksiyalarni o'zi topadi."),
                  ("assert", "noto'g'ri bo'lsa test yiqiladi."),
                  ("$ pytest", "loyiha papkasida ishga tushiriladi.")],
                 "tests/test_utils.py ..  [100%]\n2 passed"),
        ],
        {"handlers/errors.py": ERRORS, "utils.py": UTILS, "tests/test_utils.py": TEST_UTILS, "bot.py": BOT_23},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── utils.py", "yangi"), ("├── handlers/", ""), ("│   └── errors.py", "yangi"), ("└── tests/", "yangi"), ("    └── test_utils.py", "yangi")],
        ["Umumiy xato handleri", "logger.exception", "Sof funksiyalar", "pytest va assert"],
        ["Majburiy: grade() ga 3 ta chegaraviy test qo'shing.",
         "Qo'shimcha: quiz natijasida percent() va grade() dan foydalaning."],
        "7.12 · 7-oy nazorati: bot demosi.",
        run={"file": "utils.py", "input": "", "expect": ["80 4", "0 2"]},
    ),
    "TB24": lesson(
        M, 12, "7-oy nazorati: bot demosi",
        "Admin panelli, ikki tilli, eslatmali botni yig'amiz va demo qilamiz.",
        "7-oyda: reyting, admin, broadcast, middleware, media, eslatma, til, statistika, testlar.",
        "Middleware va error handler farqi nima?",
        "Loyiha tuzilmasi va routerlar tartibi (errors → admin → settings → ...). Demo: foydalanuvchi va admin ko'zi bilan.",
        "Kod tahlilidagi izohlarni tuzatib, GitHub'ga push qiling.",
        [("🛡", "errors", "birinchi", ""),
         ("🛠", "admin", "IsAdmin", ""),
         ("⚙", "settings", "/lang, /remind", ""),
         ("👤", "foydalanuvchi", "start → quiz", "mem"),
         ("⏰", "scheduler", "19:00", "")],
        [
            step("bot.py", "To'liq bot.py", BOT_23,
                 [("routerlar tartibi", "xatolar va admin birinchi, umumiy matn handlerlari oxirida."),
                  ("middleware + scheduler", "polling'dan oldin ulanadi.")],
                 "INFO quizbot: Start polling"),
            step("Terminal", "Demo ssenariysi", r'''
$ pytest
$ python bot.py
Foydalanuvchi: /lang → /start → 📝 Test → 📊 Reyting
Admin: /admin → ➕ Savol → 📋 Savollar → 📣 Xabar → 📈 Statistika''',
                 [("avval pytest", "testlar o'tmasa — demo qilmaymiz."),
                  ("ikki rol", "foydalanuvchi va admin ko'zi bilan ko'rsating.")],
                 "2 passed · Bot ishga tushdi"),
        ],
        {"bot.py": BOT_23},
        [("quizbot/", ""), ("├── bot.py", ""), ("├── filters/", ""), ("├── handlers/", ""), ("├── middlewares/", ""), ("├── scheduler.py", ""), ("├── texts.py", ""), ("├── utils.py", ""), ("└── tests/", "")],
        ["Katta loyiha tuzilmasi", "Routerlar tartibi", "Ikki rol bilan demo", "Testdan keyin demo"],
        ["Majburiy: tahlil izohlarini tuzatib, push qiling.",
         "Qo'shimcha: README'ga admin buyruqlari bo'limini yozing."],
        "8.1 · Linux asoslari va SSH.",
        chat=ADMIN_CHAT + [("user", "📊 Reyting"), ("bot", "📊 Top-10:\n🥇 Laylo — 47 ball (5 test)")],
        chat_title="Demo", chat_sub="foydalanuvchi va admin",
        checks=["pytest o'tdimi?", "Admin va oddiy foydalanuvchi farqi ko'rindimi?", "Eslatma va til ishladimi?"],
    ),
}
