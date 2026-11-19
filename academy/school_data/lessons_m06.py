"""Dasturchi 6-oy · QuizBot 1-qism (aiogram 3): TB01–TB12 "Dars kodi" (TB10 — ``lessons_dev.py``).

Bot kodi har dars uchun aiogram 3 bilan sinovdan o'tkazilgan (fayllar darsdan darsga ustma-ust yig'iladi).
SQL darslari (TB07, TB09) sqlite3 bilan ``run`` orqali testda ishga tushiriladi.
"""

from .lesson_kit import lesson, step

M = "6-oy · Telegram bot, 1-qism"

ECHO = r'''
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


@dp.message()
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

ROUTER_BOT = r'''
import asyncio
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    ism = message.from_user.first_name
    await message.answer(f"Salom, {ism}! 👋\nMen QuizBot — test ishlaydigan bot.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Buyruqlar:\n/start — boshlash\n/help — yordam")


@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Siz yozdingiz: {message.text}")


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

CONFIG = r'''
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "quizbot.db")
'''

START_V1 = r'''
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Salom, {message.from_user.first_name}! 👋\nMen QuizBot.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("/start — boshlash\n/help — yordam\n/register — ro'yxatdan o'tish")
'''

BOT_V1 = r'''
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import start


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

MENU_KB = r'''
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu():
    kb = ReplyKeyboardBuilder()
    for text in ("📝 Test", "📊 Reyting", "👤 Profil", "❓ Yordam"):
        kb.button(text=text)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
'''

START_V2 = r'''
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\nMenyudan tanlang:",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("/start — boshlash\n/help — yordam\n/register — ro'yxatdan o'tish")
'''

MENU_V1 = r'''
from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "❓ Yordam")
async def help_button(message: Message):
    await message.answer("Test ishlash uchun “📝 Test” tugmasini bosing.")


@router.message(F.text == "📊 Reyting")
async def rating_button(message: Message):
    await message.answer("Reyting tez orada! ⏳")
'''

BOT_V2 = r'''
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import menu, start


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.router, menu.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

SUBJECTS_KB = r'''
from aiogram.utils.keyboard import InlineKeyboardBuilder


def subjects_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔢 Matematika", callback_data="subject:math")
    kb.button(text="🇬🇧 Ingliz tili", callback_data="subject:english")
    kb.button(text="💻 Informatika", callback_data="subject:it")
    kb.adjust(1)
    return kb.as_markup()
'''

MENU_V2 = r'''
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from keyboards.subjects import subjects_kb

router = Router()


@router.message(F.text == "❓ Yordam")
async def help_button(message: Message):
    await message.answer("Test ishlash uchun “📝 Test” tugmasini bosing.")


@router.message(F.text == "📊 Reyting")
async def rating_button(message: Message):
    await message.answer("Reyting tez orada! ⏳")


@router.message(F.text == "📝 Test")
async def test_button(message: Message):
    await message.answer("Qaysi fandan test ishlaysiz?", reply_markup=subjects_kb())


@router.callback_query(F.data.startswith("subject:"))
async def subject_chosen(callback: CallbackQuery):
    fan = callback.data.split(":")[1]
    await callback.message.edit_text(f"Tanlandi: {fan}. Test 10-darsda tayyor bo'ladi!")
    await callback.answer()
'''

STATES_V1 = r'''
from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    phone = State()
    grade = State()
'''

REGISTER_KB = r'''
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def phone_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📱 Raqamni yuborish", request_contact=True)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
'''

REGISTER_V1 = r'''
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.register import phone_kb
from states import Register

router = Router()


@router.message(Command("register"))
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Ismingizni yozing:")


@router.message(Register.name, F.text)
async def get_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.answer("Ism kamida 2 harf bo'lsin")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(Register.phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_kb())


@router.message(Register.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.grade)
    await message.answer("Nechanchi sinfdasiz? (5–11)", reply_markup=ReplyKeyboardRemove())


@router.message(Register.grade, F.text.isdigit())
async def get_grade(message: Message, state: FSMContext):
    data = await state.update_data(grade=int(message.text))
    await state.clear()
    await message.answer(f"✅ Ro'yxatdan o'tdingiz!\n{data['name']}, {data['grade']}-sinf, {data['phone']}")
'''

BOT_V3 = r'''
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import menu, register, start


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.router, register.router, menu.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

SQL = r'''
import sqlite3

con = sqlite3.connect("quizbot.db")
cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "id INTEGER PRIMARY KEY, name TEXT, phone TEXT, grade INTEGER)"
)

cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (111, "Ali", "+998901112233", 7))
cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (222, "Laylo", "+998935556677", 9))
con.commit()

cur.execute("SELECT name, grade FROM users")
for name, grade in cur.fetchall():
    print(name, grade)

cur.execute("SELECT name FROM users WHERE grade > ?", (8,))
print("8-sinfdan yuqori:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM users")
print("Jami:", cur.fetchone()[0])
con.close()
'''

DB_V1 = r'''
import aiosqlite

from config import DB_PATH


async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, name TEXT, phone TEXT, grade INTEGER)"
        )
        await db.commit()


async def add_user(user_id: int, name: str, phone: str, grade: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)",
            (user_id, name, phone, grade),
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT name, phone, grade FROM users WHERE id = ?", (user_id,))
        return await cursor.fetchone()
'''

REGISTER_V2 = REGISTER_V1.replace(
    "from keyboards.register import phone_kb\n",
    "from database import add_user\nfrom keyboards.register import phone_kb\n",
).replace(
    "    await state.clear()\n    await message.answer(f\"✅ Ro'yxatdan o'tdingiz!",
    "    await state.clear()\n    await add_user(message.from_user.id, data[\"name\"], data[\"phone\"], data[\"grade\"])\n"
    "    await message.answer(f\"✅ Ro'yxatdan o'tdingiz!",
)

MENU_V3 = MENU_V2.replace(
    "from keyboards.subjects import subjects_kb\n",
    "from database import get_user\nfrom keyboards.subjects import subjects_kb\n",
) + r'''

@router.message(F.text == "👤 Profil")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("Avval ro'yxatdan o'ting: /register")
        return
    name, phone, grade = user
    await message.answer(f"👤 {name}\n📱 {phone}\n🏫 {grade}-sinf")
'''

BOT_V4 = BOT_V3.replace(
    "from config import BOT_TOKEN\n",
    "from config import BOT_TOKEN\nfrom database import create_tables\n",
).replace(
    "    logging.basicConfig(level=logging.INFO)\n",
    "    logging.basicConfig(level=logging.INFO)\n    await create_tables()\n",
)

SEED = r'''
import sqlite3

SAVOLLAR = [
    ("math", "7 × 8 = ?", "54", "56", "64", "48", "b"),
    ("math", "12 : 4 = ?", "2", "3", "4", "6", "b"),
    ("math", "15 + 27 = ?", "42", "32", "52", "41", "a"),
    ("english", "“Olma” inglizchasi?", "Pear", "Apple", "Plum", "Grape", "b"),
    ("english", "“Kitob” inglizchasi?", "Book", "Pen", "Desk", "Bag", "a"),
    ("it", "Python fayli kengaytmasi?", ".txt", ".exe", ".py", ".doc", "c"),
]

con = sqlite3.connect("quizbot.db")
con.execute(
    "CREATE TABLE IF NOT EXISTS questions ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, text TEXT, "
    "a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)"
)
con.executemany(
    "INSERT INTO questions (subject, text, a, b, c, d, correct) VALUES (?, ?, ?, ?, ?, ?, ?)",
    SAVOLLAR,
)
con.commit()

sql = "SELECT subject, COUNT(*) FROM questions GROUP BY subject ORDER BY subject"
for subject, soni in con.execute(sql):
    print(f"{subject}: {soni} ta savol")
con.close()
'''

DB_V3 = r'''
import aiosqlite

from config import DB_PATH


async def create_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, name TEXT, phone TEXT, grade INTEGER)"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS questions ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, text TEXT, "
            "a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS attempts ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, subject TEXT, "
            "score INTEGER, total INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        await db.commit()


async def add_user(user_id: int, name: str, phone: str, grade: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)",
            (user_id, name, phone, grade),
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT name, phone, grade FROM users WHERE id = ?", (user_id,))
        return await cursor.fetchone()


async def get_questions(subject: str, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, text, a, b, c, d, correct FROM questions "
            "WHERE subject = ? ORDER BY RANDOM() LIMIT ?",
            (subject, limit),
        )
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def save_attempt(user_id: int, subject: str, score: int, total: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO attempts (user_id, subject, score, total) VALUES (?, ?, ?, ?)",
            (user_id, subject, score, total),
        )
        await db.commit()


async def last_attempts(user_id: int, limit: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT subject, score, total, created_at FROM attempts "
            "WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        )
        return await cursor.fetchall()
'''

QUIZ_V2 = r'''
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import get_questions, last_attempts, save_attempt
from keyboards.quiz import answers_kb
from states import Quiz

router = Router()


async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    question = data["questions"][index]
    total = len(data["questions"])
    await message.answer(
        f"❓ {index + 1}/{total}\n\n{question['text']}",
        reply_markup=answers_kb(question),
    )


@router.callback_query(F.data.startswith("subject:"))
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.split(":")[1]
    questions = await get_questions(subject)
    if not questions:
        await callback.answer("Bu fanda hali savol yo'q", show_alert=True)
        return
    await state.set_state(Quiz.answering)
    await state.update_data(subject=subject, questions=questions, index=0, score=0)
    await callback.message.edit_text(f"📚 Test boshlandi: {len(questions)} ta savol")
    await send_question(callback.message, state)
    await callback.answer()


@router.callback_query(Quiz.answering, F.data.startswith("ans:"))
async def check_answer(callback: CallbackQuery, state: FSMContext):
    chosen = callback.data.split(":")[1]
    data = await state.get_data()
    question = data["questions"][data["index"]]
    score = data["score"]
    if chosen == question["correct"]:
        score += 1
        mark = "✅ To'g'ri!"
    else:
        mark = f"❌ Noto'g'ri. Javob: {question[question['correct']]}"
    await callback.message.edit_text(f"{question['text']}\n\n{mark}")
    index = data["index"] + 1
    await state.update_data(index=index, score=score)
    if index < len(data["questions"]):
        await send_question(callback.message, state)
    else:
        await state.clear()
        await save_attempt(callback.from_user.id, data["subject"], score, index)
        foiz = round(score / index * 100)
        await callback.message.answer(f"🏁 Test tugadi!\nTo'g'ri: {score}/{index} ({foiz}%)")
    await callback.answer()


@router.message(F.text == "📈 Natijalarim")
async def my_results(message: Message):
    rows = await last_attempts(message.from_user.id)
    if not rows:
        await message.answer("Hali test ishlamadingiz")
        return
    lines = [f"{fan}: {score}/{total} · {vaqt[:16]}" for fan, score, total, vaqt in rows]
    await message.answer("📈 Oxirgi natijalar:\n" + "\n".join(lines))
'''

MENU_KB_V2 = r'''
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu():
    kb = ReplyKeyboardBuilder()
    for text in ("📝 Test", "📈 Natijalarim", "📊 Reyting", "👤 Profil", "❓ Yordam"):
        kb.button(text=text)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
'''

BOT_FINAL = r'''
import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_tables
from handlers import menu, quiz, register, start


async def main():
    logging.basicConfig(level=logging.INFO)
    await create_tables()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.router, register.router, menu.router, quiz.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
'''

README = r'''
# QuizBot

Telegram'da test ishlaydigan bot: ro'yxatdan o'tish, fan tanlash, 10 ta savol,
natija va tarix. aiogram 3 + SQLite.

## Ishga tushirish

```
python -m venv .venv
pip install -r requirements.txt
python seed.py
python bot.py
```

`.env` faylida: `BOT_TOKEN=...`
'''

REQUIREMENTS = r'''
aiogram==3.31.0
aiosqlite==0.21.0
python-dotenv==1.0.1
'''

# Menyudagi "Test" tugmasi 10-darsdan boshlab quiz.router'ga o'tadi — menu.py'dagi eski callback olib tashlanadi.
MENU_FINAL = MENU_V3.replace(
    r'''

@router.callback_query(F.data.startswith("subject:"))
async def subject_chosen(callback: CallbackQuery):
    fan = callback.data.split(":")[1]
    await callback.message.edit_text(f"Tanlandi: {fan}. Test 10-darsda tayyor bo'ladi!")
    await callback.answer()
''', "").replace("from aiogram.types import CallbackQuery, Message", "from aiogram.types import Message")

CHAT_START = [("user", "/start"), ("bot", "Salom, Ali! 👋\nMenyudan tanlang:", ["📝 Test", "📊 Reyting", "👤 Profil", "❓ Yordam"])]

LESSONS = {
    "TB01": lesson(
        M, 1, "Bot qanday ishlaydi: BotFather, token, async",
        "Birinchi Telegram botimizni yaratamiz: u yozilgan har bir xabarni qaytaradi.",
        "3–5-oylarda: Python, funksiyalar, modullar, venv va pip.",
        "pip install nima qiladi? .env fayli GitHub'ga yuklanadimi?",
        "Bot = Telegram serveri ↔ bizning dastur (polling); token — bot paroli; async/await — kutish paytida boshqa ish.",
        "Bot javobiga xabar uzunligini qo'shing: “5 ta belgi”.",
        [("👤", "Foydalanuvchi", "xabar yozadi", ""),
         ("☁", "Telegram", "server", ""),
         ("🔄", "Polling", "yangi xabar bormi?", "mem"),
         ("🐍", "bot.py", "handler", ""),
         ("💬", "Javob", "message.answer", "")],
        [
            step("Telegram · Terminal", "BotFather, token va o'rnatish", r'''
@BotFather → /newbot
Nom: Minar QuizBot
Username: minar_quiz_bot
Token: 7412345678:AAH...xyz

$ pip install aiogram python-dotenv
.env:  BOT_TOKEN=7412345678:AAH...xyz''',
                 [("@BotFather", "Telegram'ning rasmiy boti — yangi bot yaratadi."),
                  ("token", "bot paroli: kim bilsa, botni boshqaradi."),
                  (".env", "token kodda emas, alohida faylda — .gitignore'da.")],
                 "Successfully installed aiogram-3.31.0"),
            step("bot.py", "Bot va Dispatcher", r'''
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()''',
                 [("load_dotenv()", ".env dagi qiymatlarni muhitga yuklaydi."),
                  ("Bot", "Telegram bilan gaplashadigan obyekt."),
                  ("Dispatcher", "kelgan xabarlarni kerakli handler'ga tarqatadi.")],
                 "(bot tayyor, hali xabar tinglamaydi)"),
            step("bot.py", "Handler va polling", r'''
@dp.message()
async def echo(message: Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())''',
                 [("@dp.message()", "har qanday matnli xabar uchun handler."),
                  ("async / await", "Telegram javobini kutayotganda bot boshqa xabarlarga ham ulguradi."),
                  ("start_polling", "Telegram'dan muntazam “yangi xabar bormi?” deb so'raydi.")],
                 "INFO: Start polling\nBot: Salom → Salom"),
        ],
        {"bot.py": ECHO, ".env": "BOT_TOKEN=7412345678:AAH...xyz\n"},
        [("quizbot/", ""), ("├── bot.py", "yangi"), ("└── .env", "yangi")],
        ["BotFather va token", "Bot, Dispatcher, handler", "async / await", "Polling"],
        ["Majburiy: javobga xabar uzunligini qo'shing.",
         "Qo'shimcha: bot javobni katta harflarda qaytarsin (upper())."],
        "6.2 · aiogram 3: Dispatcher, Router, handler.",
        chat=[("user", "Salom!"), ("bot", "Salom!"), ("user", "Qalaysan?"), ("bot", "Qalaysan?")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="python bot.py → botga yozing",
        checks=["Terminalda “Start polling” chiqdimi?", "Bot xabarni qaytardimi?", ".env .gitignore'ga yozildimi?"],
    ),
    "TB02": lesson(
        M, 2, "aiogram 3: Dispatcher, Router, handler",
        "Buyruqlarga javob beramiz: /start ism bilan salomlashadi, /help yordam beradi.",
        "O'tgan darsda: BotFather, token, echo bot.",
        "Dispatcher nima qiladi? start_polling nimani so'raydi?",
        "Router — handlerlar guruhi; filtrlar: CommandStart, Command(\"help\"), F.text; message.from_user.",
        "/about buyrug'ini qo'shing: bot nima qila oladi.",
        [("💬", "Xabar", "/start", ""),
         ("🧭", "Dispatcher", "routerlarga", ""),
         ("📂", "Router", "handlerlar", "mem"),
         ("🔍", "Filtr", "CommandStart, F.text", ""),
         ("👋", "Javob", "Salom, Ali!", "")],
        [
            step("bot.py", "Router va /start", r'''
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    ism = message.from_user.first_name
    await message.answer(f"Salom, {ism}! 👋\nMen QuizBot — test ishlaydigan bot.")''',
                 [("Router()", "handlerlarni guruhlaydi — keyin alohida fayllarga bo'lamiz."),
                  ("CommandStart()", "faqat /start buyrug'i uchun filtr."),
                  ("from_user.first_name", "yozgan odamning ismi.")],
                 "/start → Salom, Ali! 👋"),
            step("bot.py", "/help va matn filtri", r'''
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Buyruqlar:\n/start — boshlash\n/help — yordam")


@router.message(F.text)
async def echo(message: Message):
    await message.answer(f"Siz yozdingiz: {message.text}")''',
                 [("Command(\"help\")", "/help buyrug'i."),
                  ("F.text", "har qanday matn — eng oxirida turadi."),
                  ("tartib", "handlerlar yuqoridan pastga tekshiriladi: birinchi mos kelgani ishlaydi.")],
                 "/help → Buyruqlar: ...\nSalom → Siz yozdingiz: Salom"),
            step("bot.py", "Routerni ulash", r'''
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)''',
                 [("include_router", "Dispatcher routerdagi handlerlarni biladi."),
                  ("bot main() ichida", "obyektlar dastur ishga tushganda yaratiladi.")],
                 "INFO: Start polling"),
        ],
        {"bot.py": ROUTER_BOT},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("└── .env", "")],
        ["Router", "CommandStart, Command, F.text", "Handlerlar tartibi", "message.from_user"],
        ["Majburiy: /about buyrug'ini qo'shing.",
         "Qo'shimcha: “salom” so'zi bor xabarga alohida javob (F.text.lower().contains)."],
        "6.3 · Bot loyihasi tuzilmasi: config, handlers, keyboards.",
        chat=[("user", "/start"), ("bot", "Salom, Ali! 👋\nMen QuizBot — test ishlaydigan bot."), ("user", "/help"), ("bot", "Buyruqlar:\n/start — boshlash\n/help — yordam"), ("user", "Salom"), ("bot", "Siz yozdingiz: Salom")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="/start, /help va oddiy matn",
        checks=["/start ismingiz bilan salomlashdimi?", "/help buyruqlarni ko'rsatdimi?", "Oddiy matnga “Siz yozdingiz” chiqdimi?"],
    ),
    "TB03": lesson(
        M, 3, "Bot loyihasi tuzilmasi: config, handlers, keyboards",
        "Bot kattalashadi — kodni papkalarga bo'lamiz: sozlamalar, handlerlar, tugmalar.",
        "O'tgan darsda: Router, filtrlar, /start va /help.",
        "Router nima uchun kerak edi?",
        "config.py — sozlamalar; handlers/ — har mavzu alohida router; bot.py — faqat ishga tushirish; logging.",
        "/about'ni handlers/about.py ga alohida router qilib chiqaring.",
        [("⚙", "config.py", "BOT_TOKEN", ""),
         ("📂", "handlers/", "start.py ...", "mem"),
         ("⌨", "keyboards/", "tugmalar", ""),
         ("🚀", "bot.py", "include_routers", "")],
        [
            step("config.py", "Sozlamalar bir joyda", CONFIG,
                 [("BOT_TOKEN", "boshqa fayllar config'dan oladi — .env faqat shu yerda o'qiladi."),
                  ("DB_PATH", "keyinchalik baza fayli uchun."),
                  ("os.getenv(k, standart)", "qiymat yo'q bo'lsa standart.")],
                 "from config import BOT_TOKEN"),
            step("handlers/start.py", "Handlerlar alohida faylda", START_V1,
                 [("router = Router()", "har faylning o'z routeri."),
                  ("faqat start/help", "bitta fayl — bitta mavzu.")],
                 "/start → Salom, Ali! 👋 Men QuizBot."),
            step("bot.py", "Faqat ishga tushirish", BOT_V1,
                 [("from handlers import start", "papkadagi modulni import qilamiz (handlers/__init__.py bo'lishi kerak)."),
                  ("include_routers(...)", "bir nechta routerni birdan ulash."),
                  ("logging", "terminalda nima bo'layotganini ko'rsatadi.")],
                 "INFO:aiogram.dispatcher:Start polling"),
        ],
        {"config.py": CONFIG, "handlers/__init__.py": "", "handlers/start.py": START_V1, "keyboards/__init__.py": "", "bot.py": BOT_V1},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── config.py", "yangi"), ("├── handlers/", "yangi"), ("│   └── start.py", "yangi"), ("└── keyboards/", "yangi")],
        ["Loyiha tuzilmasi", "config.py", "Har mavzu — alohida router", "logging"],
        ["Majburiy: /about'ni handlers/about.py ga chiqaring.",
         "Qo'shimcha: README.md'ga papkalar tuzilmasini yozing."],
        "6.4 · Reply tugmalar: asosiy menyu.",
    ),
    "TB04": lesson(
        M, 4, "Reply tugmalar: asosiy menyu",
        "Foydalanuvchi buyruq yozmasin — pastda menyu tugmalari bo'lsin.",
        "O'tgan darsda: config, handlers, keyboards papkalari.",
        "Nega har mavzu alohida routerda?",
        "ReplyKeyboardBuilder, button, adjust, resize_keyboard; tugma bosilganda matn keladi → F.text == \"...\".",
        "“❓ Yordam” tugmasiga batafsil yo'riqnoma yozing.",
        [("⌨", "main_menu()", "4 ta tugma", "mem"),
         ("👋", "/start", "menyuni ko'rsatadi", ""),
         ("👆", "Bosish", "matn yuboriladi", ""),
         ("🔍", "F.text == ...", "handler", "")],
        [
            step("keyboards/menu.py", "Menyu tugmalari", MENU_KB,
                 [("ReplyKeyboardBuilder", "pastki tugmalarni yig'uvchi."),
                  ("adjust(2)", "har qatorda 2 ta tugma."),
                  ("resize_keyboard=True", "tugmalar ixcham bo'ladi.")],
                 "[📝 Test] [📊 Reyting]\n[👤 Profil] [❓ Yordam]"),
            step("handlers/start.py", "Menyuni ko'rsatamiz", r'''
from keyboards.menu import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\nMenyudan tanlang:",
        reply_markup=main_menu(),
    )''',
                 [("reply_markup=", "xabar bilan birga tugmalar yuboriladi."),
                  ("doim turadi", "reply tugmalar chat ostida qoladi.")],
                 "Salom, Ali! 👋\nMenyudan tanlang:"),
            step("handlers/menu.py", "Tugmalarga javob", MENU_V1,
                 [("F.text == \"❓ Yordam\"", "tugma bosilganda aynan shu matn keladi."),
                  ("emoji ham", "matn bilan to'liq bir xil bo'lishi kerak.")],
                 "❓ Yordam → Test ishlash uchun “📝 Test” tugmasini bosing."),
        ],
        {"keyboards/menu.py": MENU_KB, "handlers/start.py": START_V2, "handlers/menu.py": MENU_V1, "bot.py": BOT_V2},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── handlers/", ""), ("│   ├── start.py", "o‘zgardi"), ("│   └── menu.py", "yangi"), ("└── keyboards/", ""), ("    └── menu.py", "yangi")],
        ["Reply tugmalar", "adjust va resize_keyboard", "F.text == \"...\" filtri", "reply_markup"],
        ["Majburiy: “❓ Yordam”ga batafsil yo'riqnoma yozing.",
         "Qo'shimcha: /hide — ReplyKeyboardRemove() bilan menyuni yashirish."],
        "6.5 · Inline tugmalar va callback.",
        chat=CHAT_START + [("user", "❓ Yordam"), ("bot", "Test ishlash uchun “📝 Test” tugmasini bosing.")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="/start → menyu tugmalari",
        checks=["/start'dan keyin pastda 4 ta tugma chiqdimi?", "Tugma bosilganda javob keldimi?"],
    ),
    "TB05": lesson(
        M, 5, "Inline tugmalar va callback",
        "Xabar ostidagi tugmalar bilan fan tanlaymiz — callback_data orqali.",
        "O'tgan darsda: reply tugmalar, F.text filtri.",
        "Reply tugma bosilganda botga nima keladi?",
        "InlineKeyboardBuilder, callback_data, callback_query handler, edit_text, callback.answer().",
        "To'rtinchi fan qo'shing va tugmalarni 2 ustunga joylang.",
        [("📝", "“Test” tugmasi", "reply", ""),
         ("🔘", "Inline tugmalar", "fanlar", "mem"),
         ("📦", "callback_data", "subject:math", ""),
         ("🔍", "callback_query", "F.data.startswith", ""),
         ("✏", "edit_text", "xabarni yangilash", "")],
        [
            step("keyboards/subjects.py", "Inline tugmalar", SUBJECTS_KB,
                 [("InlineKeyboardBuilder", "xabar ostidagi tugmalar."),
                  ("callback_data", "botga yashirin keladigan matn: subject:math."),
                  ("prefiks", "subject: — keyin boshqa tugmalardan ajratish oson.")],
                 "[🔢 Matematika]\n[🇬🇧 Ingliz tili]\n[💻 Informatika]"),
            step("handlers/menu.py", "Fanlarni ko'rsatamiz", r'''
@router.message(F.text == "📝 Test")
async def test_button(message: Message):
    await message.answer("Qaysi fandan test ishlaysiz?", reply_markup=subjects_kb())''',
                 [("reply → inline", "menyudagi tugma inline tanlovni ochadi.")],
                 "Qaysi fandan test ishlaysiz?\n[🔢 Matematika] ..."),
            step("handlers/menu.py", "Callback'ni ushlaymiz", r'''
@router.callback_query(F.data.startswith("subject:"))
async def subject_chosen(callback: CallbackQuery):
    fan = callback.data.split(":")[1]
    await callback.message.edit_text(f"Tanlandi: {fan}. Test 10-darsda tayyor bo'ladi!")
    await callback.answer()''',
                 [("callback_query", "inline tugma bosilishi — message emas."),
                  ("edit_text", "eski xabarni yangilaydi (tugmalar yo'qoladi)."),
                  ("callback.answer()", "tugmadagi “soat” belgisini o'chiradi.")],
                 "Tanlandi: math. Test 10-darsda tayyor bo'ladi!"),
        ],
        {"keyboards/subjects.py": SUBJECTS_KB, "handlers/menu.py": MENU_V2},
        [("quizbot/", ""), ("├── handlers/", ""), ("│   └── menu.py", "o‘zgardi"), ("└── keyboards/", ""), ("    └── subjects.py", "yangi")],
        ["Inline tugmalar", "callback_data", "callback_query handler", "edit_text va callback.answer()"],
        ["Majburiy: 4-fan qo'shing va adjust(2) bilan 2 ustunga joylang.",
         "Qo'shimcha: “🔙 Orqaga” tugmasi — menyuga qaytish."],
        "6.6 · FSM: ro'yxatdan o'tish.",
        chat=[("user", "📝 Test"), ("bot", "Qaysi fandan test ishlaysiz?", ["🔢 Matematika", "🇬🇧 Ingliz tili", "💻 Informatika"]), ("bot", "Tanlandi: math. Test 10-darsda tayyor bo'ladi!")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="📝 Test → fan tanlash",
        checks=["Inline tugmalar xabar ostida chiqdimi?", "Bosilganda xabar o'zgardimi?", "Tugmada “soat” qolmadimi?"],
    ),
    "TB06": lesson(
        M, 6, "FSM: ro'yxatdan o'tish",
        "Bot ketma-ket savol beradi: ism → telefon → sinf. Har bosqichni FSM eslab qoladi.",
        "O'tgan darsda: inline tugmalar va callback.",
        "edit_text va callback.answer() nima qiladi?",
        "FSM — holatlar mashinasi: StatesGroup, State, set_state, update_data, clear; kontakt tugmasi (request_contact).",
        "Ism kamida 2 harf, sinf 5–11 oralig'ida ekanini tekshiring.",
        [("📝", "/register", "Register.name", ""),
         ("👤", "Ism", "Register.phone", "loop"),
         ("📱", "Kontakt", "Register.grade", "loop"),
         ("🏫", "Sinf", "clear()", ""),
         ("✅", "Tayyor", "ma'lumot jamlandi", "mem")],
        [
            step("states.py", "Holatlar", STATES_V1,
                 [("StatesGroup", "bir jarayonning holatlari to'plami."),
                  ("State()", "har bir bosqich: ism, telefon, sinf.")],
                 "Register.name → Register.phone → Register.grade"),
            step("handlers/register.py", "Ism va telefon", r'''
@router.message(Command("register"))
async def start_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Ismingizni yozing:")


@router.message(Register.name, F.text)
async def get_name(message: Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.answer("Ism kamida 2 harf bo'lsin")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(Register.phone)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=phone_kb())''',
                 [("set_state", "foydalanuvchini keyingi bosqichga o'tkazadi."),
                  ("Register.name filtri", "handler faqat shu holatda ishlaydi."),
                  ("update_data", "javobni FSM xotirasiga yozadi.")],
                 "/register → Ismingizni yozing:\nAli → Telefon raqamingizni yuboring:"),
            step("handlers/register.py", "Kontakt va sinf", r'''
@router.message(Register.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.grade)
    await message.answer("Nechanchi sinfdasiz? (5–11)", reply_markup=ReplyKeyboardRemove())


@router.message(Register.grade, F.text.isdigit())
async def get_grade(message: Message, state: FSMContext):
    data = await state.update_data(grade=int(message.text))
    await state.clear()''',
                 [("F.contact", "“📱 Raqamni yuborish” tugmasi bosilganda keladi."),
                  ("ReplyKeyboardRemove", "kontakt tugmasini yashiradi."),
                  ("clear()", "jarayon tugadi — holat va xotira tozalanadi.")],
                 "✅ Ro'yxatdan o'tdingiz!\nAli, 7-sinf, +998901112233"),
        ],
        {"states.py": STATES_V1, "keyboards/register.py": REGISTER_KB, "handlers/register.py": REGISTER_V1, "bot.py": BOT_V3},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── states.py", "yangi"), ("├── handlers/", ""), ("│   └── register.py", "yangi"), ("└── keyboards/", ""), ("    └── register.py", "yangi")],
        ["FSM: StatesGroup va State", "set_state, update_data, clear", "Holat filtri", "Kontakt tugmasi"],
        ["Majburiy: sinf 5–11 oralig'ida ekanini tekshiring.",
         "Qo'shimcha: /cancel — ro'yxatdan o'tishni bekor qilish."],
        "6.7 · SQL asoslari: CREATE, INSERT, SELECT.",
        chat=[("user", "/register"), ("bot", "Ismingizni yozing:"), ("user", "Ali"), ("bot", "Telefon raqamingizni yuboring:", ["📱 Raqamni yuborish"]), ("user", "📱 +998901112233"), ("bot", "Nechanchi sinfdasiz? (5–11)"), ("user", "7"), ("bot", "✅ Ro'yxatdan o'tdingiz!\nAli, 7-sinf, +998901112233")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="/register → 3 bosqich",
        checks=["Bitta harfli ism rad etildimi?", "Kontakt tugmasi chiqdimi?", "Oxirida hammasi jamlab ko'rsatildimi?"],
    ),
    "TB07": lesson(
        M, 7, "SQL asoslari: CREATE, INSERT, SELECT",
        "Bot ma'lumotni unutmasin — SQLite bazasi va SQL tilining asosiy buyruqlari.",
        "O'tgan darsda: FSM bilan ro'yxatdan o'tish (ma'lumot faqat xotirada).",
        "state.clear() dan keyin ism qayerda qoladi?",
        "Baza = jadvallar; ustun va qator; CREATE TABLE, INSERT, SELECT, WHERE, COUNT; ? — xavfsiz parametr.",
        "users jadvaliga created_at ustunini qo'shing.",
        [("🗄", "quizbot.db", "SQLite fayli", ""),
         ("📐", "CREATE TABLE", "users", "mem"),
         ("➕", "INSERT", "qator qo'shish", ""),
         ("🔍", "SELECT", "o'qish, WHERE", ""),
         ("🔢", "COUNT(*)", "nechta?", "")],
        [
            step("sql_practice.py", "Jadval yaratamiz", r'''
import sqlite3

con = sqlite3.connect("quizbot.db")
cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "id INTEGER PRIMARY KEY, name TEXT, phone TEXT, grade INTEGER)"
)''',
                 [("sqlite3", "Python bilan birga keladi — o'rnatish shart emas."),
                  ("CREATE TABLE", "jadval va ustunlar turi: INTEGER, TEXT."),
                  ("PRIMARY KEY", "takrorlanmas id — Telegram user_id.")],
                 "quizbot.db fayli paydo bo'ldi"),
            step("sql_practice.py", "Qator qo'shamiz", r'''
cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (111, "Ali", "+998901112233", 7))
cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (222, "Laylo", "+998935556677", 9))
con.commit()''',
                 [("INSERT", "jadvalga yangi qator."),
                  ("?", "qiymatlar alohida beriladi — SQL injection'dan himoya."),
                  ("commit()", "o'zgarishni faylga yozish.")],
                 "users: 2 qator"),
            step("sql_practice.py", "O'qiymiz va sanaymiz", r'''
cur.execute("SELECT name, grade FROM users")
for name, grade in cur.fetchall():
    print(name, grade)

cur.execute("SELECT name FROM users WHERE grade > ?", (8,))
print("8-sinfdan yuqori:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM users")
print("Jami:", cur.fetchone()[0])
con.close()''',
                 [("SELECT ... FROM", "qaysi ustunlar, qaysi jadvaldan."),
                  ("WHERE", "shart bo'yicha filtr."),
                  ("fetchall / fetchone", "hamma qatorlar / bitta qator.")],
                 "Ali 7\nLaylo 9\n8-sinfdan yuqori: Laylo\nJami: 2"),
        ],
        {"sql_practice.py": SQL},
        [("quizbot/", ""), ("├── sql_practice.py", "yangi"), ("└── quizbot.db", "yangi")],
        ["Jadval, ustun, qator", "CREATE TABLE, INSERT", "SELECT, WHERE, COUNT", "? parametrlar va commit"],
        ["Majburiy: created_at ustunini qo'shing (DEFAULT CURRENT_TIMESTAMP).",
         "Qo'shimcha: UPDATE bilan Ali sinfini 8 qiling, DELETE bilan Laylo'ni o'chiring."],
        "6.8 · aiosqlite: botni bazaga ulash.",
        run={"file": "sql_practice.py", "input": "", "expect": ["Ali 7", "Laylo 9", "8-sinfdan yuqori: Laylo", "Jami: 2"]},
    ),
    "TB08": lesson(
        M, 8, "aiosqlite: botni bazaga ulash",
        "Ro'yxatdan o'tganlarni bazaga saqlaymiz va “👤 Profil” tugmasida ko'rsatamiz.",
        "O'tgan darsda: SQL — CREATE, INSERT, SELECT (sqlite3).",
        "INSERT dan keyin nega commit() kerak?",
        "aiosqlite — async baza; async with connect; INSERT OR REPLACE; fetchone; bot ishga tushganda create_tables().",
        "Profilda ro'yxatdan o'tgan sanani ko'rsating.",
        [("📝", "Ro'yxatdan o'tish", "FSM", ""),
         ("💾", "add_user()", "INSERT", "mem"),
         ("🗄", "users", "quizbot.db", ""),
         ("👤", "Profil", "get_user()", ""),
         ("🚀", "create_tables()", "ishga tushganda", "")],
        [
            step("database.py", "Async baza funksiyalari", DB_V1,
                 [("aiosqlite", "bot kutib qolmasligi uchun async versiya."),
                  ("INSERT OR REPLACE", "qayta ro'yxatdan o'tsa — yangilaydi."),
                  ("fetchone()", "bitta qator yoki None.")],
                 "users: (111, 'Ali', '+998901112233', 7)"),
            step("handlers/register.py", "Ro'yxatdan o'tganda saqlaymiz", r'''
from database import add_user
...
    data = await state.update_data(grade=int(message.text))
    await state.clear()
    await add_user(message.from_user.id, data["name"], data["phone"], data["grade"])''',
                 [("message.from_user.id", "Telegram'dagi takrorlanmas id — PRIMARY KEY."),
                  ("await", "baza bilan ishlash ham async.")],
                 "✅ Ro'yxatdan o'tdingiz! → bazada saqlandi", new=[1, 5]),
            step("handlers/menu.py", "Profil tugmasi", r'''
@router.message(F.text == "👤 Profil")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer("Avval ro'yxatdan o'ting: /register")
        return
    name, phone, grade = user
    await message.answer(f"👤 {name}\n📱 {phone}\n🏫 {grade}-sinf")''',
                 [("None", "bazada yo'q — ro'yxatdan o'tishga yo'naltiramiz."),
                  ("name, phone, grade = user", "qatorni o'zgaruvchilarga ochish.")],
                 "👤 Ali\n📱 +998901112233\n🏫 7-sinf"),
        ],
        {"database.py": DB_V1, "handlers/register.py": REGISTER_V2, "handlers/menu.py": MENU_V3, "bot.py": BOT_V4},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── database.py", "yangi"), ("└── handlers/", ""), ("    ├── register.py", "o‘zgardi"), ("    └── menu.py", "o‘zgardi")],
        ["aiosqlite", "async with connect", "INSERT OR REPLACE", "Bot ishga tushganda jadvallar"],
        ["Majburiy: profilda ro'yxatdan o'tgan sanani ko'rsating.",
         "Qo'shimcha: /users — admin uchun foydalanuvchilar soni."],
        "6.9 · Savollar jadvali va seed.",
        chat=[("user", "👤 Profil"), ("bot", "Avval ro'yxatdan o'ting: /register"), ("user", "/register … 7"), ("bot", "✅ Ro'yxatdan o'tdingiz!\nAli, 7-sinf, +998901112233"), ("user", "👤 Profil"), ("bot", "👤 Ali\n📱 +998901112233\n🏫 7-sinf")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="Profil → ro'yxatdan o'tish → Profil",
        checks=["Ro'yxatdan o'tmaganga ogohlantirish chiqdimi?", "Bot qayta ishga tushganda ham profil saqlandimi?"],
    ),
    "TB09": lesson(
        M, 9, "Savollar jadvali va seed",
        "Test uchun savollar bazasini yaratamiz va bir buyruq bilan to'ldiramiz.",
        "O'tgan darsda: aiosqlite, users jadvali, profil.",
        "INSERT OR REPLACE nima qiladi?",
        "Savol jadvali tuzilmasi (variantlar a–d, to'g'ri javob), seed skripti, executemany, GROUP BY.",
        "O'z faningizdan 10 ta savol qo'shing.",
        [("📋", "SAVOLLAR", "Python ro'yxati", ""),
         ("📐", "questions", "jadval", "mem"),
         ("➕", "executemany", "hammasini birdan", ""),
         ("📊", "GROUP BY", "fan bo'yicha soni", "")],
        [
            step("seed.py", "Savollar ro'yxati", r'''
SAVOLLAR = [
    ("math", "7 × 8 = ?", "54", "56", "64", "48", "b"),
    ("math", "12 : 4 = ?", "2", "3", "4", "6", "b"),
    ("math", "15 + 27 = ?", "42", "32", "52", "41", "a"),
    ("english", "“Olma” inglizchasi?", "Pear", "Apple", "Plum", "Grape", "b"),
    ("english", "“Kitob” inglizchasi?", "Book", "Pen", "Desk", "Bag", "a"),
    ("it", "Python fayli kengaytmasi?", ".txt", ".exe", ".py", ".doc", "c"),
]''',
                 [("tuple", "fan, savol, 4 variant, to'g'ri javob harfi."),
                  ("correct = \"b\"", "javob matnini emas, harfini saqlaymiz.")],
                 "6 ta savol (darsda 30 tagacha)"),
            step("seed.py", "Jadval va executemany", r'''
con = sqlite3.connect("quizbot.db")
con.execute(
    "CREATE TABLE IF NOT EXISTS questions ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, text TEXT, "
    "a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)"
)
con.executemany(
    "INSERT INTO questions (subject, text, a, b, c, d, correct) VALUES (?, ?, ?, ?, ?, ?, ?)",
    SAVOLLAR,
)
con.commit()''',
                 [("AUTOINCREMENT", "id o'zi oshib boradi."),
                  ("executemany", "ro'yxatdagi har bir tuple uchun INSERT."),
                  ("seed", "bir marta ishga tushiriladigan to'ldirish skripti.")],
                 "questions: 6 qator"),
            step("seed.py", "Fan bo'yicha sanaymiz", r'''
sql = "SELECT subject, COUNT(*) FROM questions GROUP BY subject ORDER BY subject"
for subject, soni in con.execute(sql):
    print(f"{subject}: {soni} ta savol")
con.close()''',
                 [("GROUP BY", "bir xil fanlarni guruhlab, har biri uchun COUNT."),
                  ("ORDER BY", "natija tartibli chiqadi.")],
                 "english: 2 ta savol\nit: 1 ta savol\nmath: 3 ta savol"),
        ],
        {"seed.py": SEED},
        [("quizbot/", ""), ("├── seed.py", "yangi"), ("└── quizbot.db", "o‘zgardi")],
        ["Savollar jadvali", "Seed skripti", "executemany", "GROUP BY va COUNT"],
        ["Majburiy: o'z faningizdan 10 ta savol qo'shing.",
         "Qo'shimcha: seed qayta ishga tushganda takrorlanmasin (avval DELETE FROM questions)."],
        "6.10 · Test rejimi, 1-qism.",
        run={"file": "seed.py", "input": "", "expect": ["english: 2 ta savol", "it: 1 ta savol", "math: 3 ta savol"]},
    ),
    "TB11": lesson(
        M, 11, "Test rejimi, 2-qism: natija va attempts jadvali",
        "Test natijasini bazaga saqlaymiz va “📈 Natijalarim” tugmasida oxirgi 5 tasini ko'rsatamiz.",
        "O'tgan darsda: test rejimi — savollar, tugmalar, tekshirish.",
        "state.clear() test oxirida nima qiladi?",
        "attempts jadvali (DEFAULT CURRENT_TIMESTAMP), save_attempt, ORDER BY id DESC LIMIT, foiz hisoblash.",
        "Natijaga baho qo'shing: 90%+ — 5, 70%+ — 4, 50%+ — 3.",
        [("❓", "Test", "10 savol", ""),
         ("🏁", "Oxirgi javob", "score/total", ""),
         ("💾", "save_attempt", "attempts", "mem"),
         ("📈", "Natijalarim", "last_attempts", ""),
         ("🖥", "Javob", "oxirgi 5 ta", "")],
        [
            step("database.py", "attempts jadvali", r'''
        await db.execute(
            "CREATE TABLE IF NOT EXISTS attempts ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, subject TEXT, "
            "score INTEGER, total INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )''',
                 [("create_tables ichida", "bot ishga tushganda jadval tayyor bo'ladi."),
                  ("DEFAULT CURRENT_TIMESTAMP", "vaqt o'zi yoziladi.")],
                 "attempts: user_id, subject, score, total, created_at"),
            step("database.py", "Saqlash va o'qish", r'''
async def save_attempt(user_id: int, subject: str, score: int, total: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO attempts (user_id, subject, score, total) VALUES (?, ?, ?, ?)",
            (user_id, subject, score, total),
        )
        await db.commit()


async def last_attempts(user_id: int, limit: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT subject, score, total, created_at FROM attempts "
            "WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        )
        return await cursor.fetchall()''',
                 [("ORDER BY id DESC", "eng yangisi birinchi."),
                  ("LIMIT ?", "faqat oxirgi 5 ta."),
                  ("ustunlar ro'yxati", "INSERT'da id va created_at ko'rsatilmaydi — o'zi to'ladi.")],
                 "[('math', 8, 10, '2026-11-19 15:42:10'), ...]"),
            step("handlers/quiz.py", "Test oxirida saqlash va Natijalarim", r'''
        await state.clear()
        await save_attempt(callback.from_user.id, data["subject"], score, index)
        foiz = round(score / index * 100)
        await callback.message.answer(f"🏁 Test tugadi!\nTo'g'ri: {score}/{index} ({foiz}%)")
    await callback.answer()


@router.message(F.text == "📈 Natijalarim")
async def my_results(message: Message):
    rows = await last_attempts(message.from_user.id)
    if not rows:
        await message.answer("Hali test ishlamadingiz")
        return
    lines = [f"{fan}: {score}/{total} · {vaqt[:16]}" for fan, score, total, vaqt in rows]
    await message.answer("📈 Oxirgi natijalar:\n" + "\n".join(lines))''',
                 [("data[\"subject\"]", "start_quiz'da fan ham xotiraga yoziladi."),
                  ("foiz", "score ÷ jami × 100."),
                  ("vaqt[:16]", "soniyasiz: 2026-11-19 15:42.")],
                 "🏁 Test tugadi!\nTo'g'ri: 8/10 (80%)"),
        ],
        {"database.py": DB_V3, "handlers/quiz.py": QUIZ_V2, "keyboards/menu.py": MENU_KB_V2},
        [("quizbot/", ""), ("├── database.py", "o‘zgardi"), ("├── handlers/", ""), ("│   └── quiz.py", "o‘zgardi"), ("└── keyboards/", ""), ("    └── menu.py", "o‘zgardi")],
        ["attempts jadvali", "DEFAULT CURRENT_TIMESTAMP", "ORDER BY DESC LIMIT", "Natijalar tarixi"],
        ["Majburiy: natijaga baho qo'shing (5/4/3/2).",
         "Qo'shimcha: “📈 Natijalarim”da o'rtacha foizni ham ko'rsating."],
        "6.12 · 6-oy nazorati: QuizBot demosi.",
        chat=[("bot", "7 × 8 = ?\n\n✅ To'g'ri!"), ("bot", "🏁 Test tugadi!\nTo'g'ri: 8/10 (80%)"), ("user", "📈 Natijalarim"), ("bot", "📈 Oxirgi natijalar:\nmath: 8/10 · 2026-11-19 15:42\nenglish: 6/10 · 2026-11-18 16:05")],
        chat_title="Telegram'da sinab ko'ramiz", chat_sub="Test → natija → Natijalarim",
        checks=["Test oxirida foiz chiqdimi?", "“📈 Natijalarim” oxirgi testni ko'rsatdimi?", "Bot qayta ishga tushganda natijalar saqlandimi?"],
    ),
    "TB12": lesson(
        M, 12, "6-oy nazorati: QuizBot demosi",
        "Bir oyda yasalgan botni yig'amiz, README yozamiz va demo qilamiz.",
        "6-oyda: aiogram 3, tugmalar, FSM, SQLite, test rejimi.",
        "Router, FSM, callback — oyni 5 savol bilan takrorlaymiz.",
        "Loyiha tuzilmasi va oqim: /start → menyu → ro'yxatdan o'tish → test → natija. Demo ssenariysi.",
        "Kod tahlilidagi izohlar bo'yicha botni tuzatib, GitHub'ga push qiling.",
        [("👋", "/start", "menyu", ""),
         ("📝", "/register", "FSM + users", ""),
         ("❓", "Test", "questions", "mem"),
         ("💾", "Natija", "attempts", ""),
         ("📈", "Natijalarim", "tarix", "")],
        [
            step("bot.py", "Hamma routerlarni yig'amiz", BOT_FINAL,
                 [("tartib", "start → register → menu → quiz: umumiy F.text handlerlar oxirida."),
                  ("create_tables()", "uchala jadval bot ishga tushganda tayyor.")],
                 "INFO: Start polling\nINFO: Run polling for bot @minar_quiz_bot"),
            step("README.md", "Loyiha tavsifi", r'''
# QuizBot

Telegram'da test ishlaydigan bot: ro'yxatdan o'tish, fan tanlash, 10 ta savol,
natija va tarix. aiogram 3 + SQLite.

## Ishga tushirish''',
                 [("README", "GitHub'da birinchi ko'rinadi: nima qiladi va qanday ishga tushadi."),
                  ("requirements.txt", "aniq versiyalar — boshqa kompyuterda ham bir xil ishlaydi.")],
                 "github.com/ali/quizbot"),
            step("Terminal", "Demo ssenariysi", r'''
$ python seed.py
$ python bot.py
1. /start → menyu
2. /register → ism, kontakt, sinf
3. 📝 Test → Matematika → 10 savol
4. 📈 Natijalarim → oxirgi natijalar''',
                 [("3 daqiqa", "har bosqichni ko'rsatib, qisqa tushuntiring."),
                  ("tayyorgarlik", "token, .env va savollar oldindan tayyor bo'lsin.")],
                 "Demo: 4 bosqich, 3 daqiqa"),
        ],
        {"bot.py": BOT_FINAL, "handlers/menu.py": MENU_FINAL, "README.md": README, "requirements.txt": REQUIREMENTS},
        [("quizbot/", ""), ("├── bot.py", "o‘zgardi"), ("├── config.py", ""), ("├── database.py", ""), ("├── seed.py", ""), ("├── states.py", ""), ("├── handlers/", ""), ("├── keyboards/", ""), ("├── README.md", "yangi"), ("└── requirements.txt", "yangi")],
        ["Botning to'liq oqimi", "Routerlar tartibi", "README va requirements", "Demo ssenariysi"],
        ["Majburiy: tahlil izohlari bo'yicha tuzatib, GitHub'ga push qiling.",
         "Qo'shimcha: README'ga bot skrinshotlarini qo'shing."],
        "7.1 · SQL: ORDER BY, LIMIT, JOIN — reyting.",
        chat=CHAT_START + [("user", "📝 Test"), ("bot", "Qaysi fandan test ishlaysiz?", ["🔢 Matematika", "🇬🇧 Ingliz tili", "💻 Informatika"]), ("bot", "🏁 Test tugadi!\nTo'g'ri: 9/10 (90%)")],
        chat_title="Demo", chat_sub="/start → Test → natija",
        checks=["Hamma tugmalar ishladimi?", "Ma'lumotlar bazada saqlandimi?", "README va requirements GitHub'dami?"],
    ),
}


# 10-dars (lessons_dev.py) uchun to'liq fayllar: oldingi darslar ustiga yig'iladi.
STATES_FULL = STATES_V1 + r'''

class Quiz(StatesGroup):
    answering = State()
'''

DB_TB10 = DB_V1.replace(
    '''        await db.commit()


async def add_user''',
    '''        await db.execute(
            "CREATE TABLE IF NOT EXISTS questions ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, text TEXT, "
            "a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)"
        )
        await db.commit()


async def add_user''',
    1,
) + r'''

async def get_questions(subject: str, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, text, a, b, c, d, correct FROM questions "
            "WHERE subject = ? ORDER BY RANDOM() LIMIT ?",
            (subject, limit),
        )
        rows = await cursor.fetchall()
    return [dict(row) for row in rows]
'''
