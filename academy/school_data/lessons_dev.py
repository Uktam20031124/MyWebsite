"""Minar Dasturchi darslarining "Dars kodi": reja, kod qadamlari va rasmlar uchun ma'lumot (kalit — ``dev.py``).

Kod qadamlaridagi har bir qator ``files`` dagi tayyor fayllarda bor (``tests/test_lessons.py``);
bot kodi aiogram 3 bilan sinovdan o'tgan.
"""

LESSONS = {
    "TB10": {'month': '6-oy · Telegram bot, 1-qism',
     'number': 10,
     'title': 'Test rejimi, 1-qism: savol va javob tugmalari',
     'goal': 'Fan tugmasi bosilganda bot bazadan 10 ta savol oladi, ularni birma-bir tugmalar bilan yuboradi va '
             'javobni tekshiradi.',
     'before': 'Oldingi darslarda: fan tanlash tugmalari (6.5), FSM (6.6), aiosqlite (6.8), questions jadvali va 30 ta '
               'savol (6.9).',
     'plan': [('0–5',
               'Takrorlash',
               'Fan tugmalari qanday callback yuboradi? FSM nima uchun kerak edi? 2 ta savol bilan eslatamiz.'),
              ('5–15',
               'Yangi g‘oya',
               'Test oqimini doskada chizamiz (1-rasm): savollar ro‘yxati, index va score FSM xotirasida turadi.'),
              ('15–40',
               'Birga kod yozamiz',
               '6 qadam: bazadan savol olish → holat → javob tugmalari → savol yuborish → testni boshlash → javobni '
               'tekshirish.'),
              ('40–50', 'Sinov', 'Har kim o‘z botida 1 ta testni oxirigacha ishlaydi, xatolarni birga tuzatamiz.'),
              ('50–60', 'Mustaqil ish va test', 'Qo‘shimcha topshiriq + saytdagi 10 savollik test.')],
     'steps': [{'file': 'database.py',
                'title': 'Bazadan tasodifiy 10 ta savol olamiz',
                'code': 'async def get_questions(subject: str, limit: int = 10) -> list[dict]:\n'
                        '    async with aiosqlite.connect(DB_PATH) as db:\n'
                        '        db.row_factory = aiosqlite.Row\n'
                        '        cursor = await db.execute(\n'
                        '            "SELECT id, text, a, b, c, d, correct FROM questions "\n'
                        '            "WHERE subject = ? ORDER BY RANDOM() LIMIT ?",\n'
                        '            (subject, limit),\n'
                        '        )\n'
                        '        rows = await cursor.fetchall()\n'
                        '    return [dict(row) for row in rows]',
                'new': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'notes': [('WHERE subject = ?',
                           "faqat tanlangan fan savollari; <b>?</b> — xavfsiz parametr, matnni SQL'ga qo‘shib "
                           'yozmaymiz.'),
                          ('ORDER BY RANDOM() LIMIT ?', 'har safar boshqa 10 ta savol, boshqa tartibda.'),
                          ('row_factory = Row', "qatorni <code>row['text']</code> kabi nom bilan o‘qish uchun."),
                          ('dict(row)', 'FSM xotirasiga oddiy lug‘at saqlanadi — Row obyekti emas.')],
                'result': 'get_questions("math") → [{\'id\': 4, \'text\': \'7 × 8 = ?\', \'a\': \'54\', \'b\': \'56\', '
                          "..., 'correct': 'b'}, ...]"},
               {'file': 'states.py  ·  keyboards/quiz.py',
                'title': 'Holat va javob tugmalari',
                'code': '# states.py\n'
                        'class Quiz(StatesGroup):\n'
                        '    answering = State()\n'
                        '\n'
                        '\n'
                        '# keyboards/quiz.py\n'
                        'def answers_kb(question: dict):\n'
                        '    kb = InlineKeyboardBuilder()\n'
                        '    for key in ("a", "b", "c", "d"):\n'
                        '        kb.button(text=question[key], callback_data=f"ans:{key}")\n'
                        '    kb.adjust(1)\n'
                        '    return kb.as_markup()',
                'new': [2, 3, 7, 8, 9, 10, 11, 12],
                'notes': [('Quiz.answering',
                           '“foydalanuvchi hozir test yechyapti” holati. Javob tugmalari faqat shu holatda ishlaydi.'),
                          ('callback_data="ans:b"',
                           'tugma bosilganda botga keladigan yashirin matn: qaysi variant tanlangani.'),
                          ('kb.adjust(1)', 'har qatorda 1 ta tugma — uzun javoblar sig‘adi.')],
                'result': '4 ta tugma: [54] [56] [64] [48] — har biri ans:a … ans:d yuboradi'},
               {'file': 'handlers/quiz.py',
                'title': 'Navbatdagi savolni yuboruvchi funksiya',
                'code': 'router = Router()\n'
                        '\n'
                        '\n'
                        'async def send_question(message: Message, state: FSMContext):\n'
                        '    data = await state.get_data()\n'
                        '    index = data["index"]\n'
                        '    question = data["questions"][index]\n'
                        '    total = len(data["questions"])\n'
                        '    await message.answer(\n'
                        '        f"❓ {index + 1}/{total}\\n\\n{question[\'text\']}",\n'
                        '        reply_markup=answers_kb(question),\n'
                        '    )',
                'new': [4, 5, 6, 7, 8, 9, 10, 11, 12],
                'notes': [('state.get_data()', 'FSM xotirasidan lug‘at: questions, index, score.'),
                          ('index', 'nechanchi savoldamiz (0 dan). Ekranda <b>index + 1</b> ko‘rsatamiz.'),
                          ('alohida funksiya',
                           'savol yuborish 2 joyda kerak: test boshida va har javobdan keyin — kodni takrorlamaymiz.')],
                'result': '❓ 1/10\n\n7 × 8 = ?\n[54] [56] [64] [48]'},
               {'file': 'handlers/quiz.py',
                'title': 'Fan tugmasi bosilganda testni boshlaymiz',
                'code': '@router.callback_query(F.data.startswith("subject:"))\n'
                        'async def start_quiz(callback: CallbackQuery, state: FSMContext):\n'
                        '    subject = callback.data.split(":")[1]\n'
                        '    questions = await get_questions(subject)\n'
                        '    if not questions:\n'
                        '        await callback.answer("Bu fanda hali savol yo\'q", show_alert=True)\n'
                        '        return\n'
                        '    await state.set_state(Quiz.answering)\n'
                        '    await state.update_data(questions=questions, index=0, score=0)\n'
                        '    await callback.message.edit_text(f"📚 Test boshlandi: {len(questions)} ta savol")\n'
                        '    await send_question(callback.message, state)\n'
                        '    await callback.answer()',
                'new': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'notes': [('F.data.startswith', 'faqat <code>subject:math</code> kabi tugmalarni ushlaydi.'),
                          ('split(":")[1]', '"subject:math" → "math".'),
                          ('if not questions', 'savol yo‘q bo‘lsa — ogohlantirish oynasi va to‘xtash.'),
                          ('set_state + update_data', 'holatni yoqamiz va 3 ta qiymatni xotiraga yozamiz.'),
                          ('callback.answer()', 'tugmadagi “soat” belgisini o‘chiradi — har doim oxirida.')],
                'result': '📚 Test boshlandi: 10 ta savol\n❓ 1/10 …'},
               {'file': 'handlers/quiz.py',
                'title': 'Javobni tekshiramiz va keyingi savolga o‘tamiz',
                'code': '@router.callback_query(Quiz.answering, F.data.startswith("ans:"))\n'
                        'async def check_answer(callback: CallbackQuery, state: FSMContext):\n'
                        '    chosen = callback.data.split(":")[1]\n'
                        '    data = await state.get_data()\n'
                        '    question = data["questions"][data["index"]]\n'
                        '    score = data["score"]\n'
                        '    if chosen == question["correct"]:\n'
                        '        score += 1\n'
                        '        mark = "✅ To\'g\'ri!"\n'
                        '    else:\n'
                        '        mark = f"❌ Noto\'g\'ri. Javob: {question[question[\'correct\']]}"\n'
                        '    await callback.message.edit_text(f"{question[\'text\']}\\n\\n{mark}")\n'
                        '    index = data["index"] + 1\n'
                        '    await state.update_data(index=index, score=score)\n'
                        '    if index < len(data["questions"]):\n'
                        '        await send_question(callback.message, state)\n'
                        '    else:\n'
                        '        await state.clear()\n'
                        '        await callback.message.answer(f"🏁 Test tugadi! To\'g\'ri javoblar: {score}/{index}")\n'
                        '    await callback.answer()',
                'new': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'notes': [('Quiz.answering', 'filtr: test tugagach eski tugmalar ishlamaydi.'),
                          ('edit_text', 'savol xabaridan tugmalar olib tashlanadi — ikki marta bosib bo‘lmaydi.'),
                          ('index + 1', 'keyingi savol; oxirgisi bo‘lsa — natija va <code>state.clear()</code>.'),
                          ("question[question['correct']]", '"b" → variant matni "56".')],
                'result': "7 × 8 = ?\n\n❌ Noto'g'ri. Javob: 56\n❓ 2/10 …"},
               {'file': 'bot.py',
                'title': 'Routerni ulaymiz va ishga tushiramiz',
                'code': 'from handlers import quiz, start\n'
                        '\n'
                        '\n'
                        'async def main():\n'
                        '    logging.basicConfig(level=logging.INFO)\n'
                        '    await create_tables()\n'
                        '    bot = Bot(token=BOT_TOKEN)\n'
                        '    dp = Dispatcher()\n'
                        '    dp.include_routers(start.router, quiz.router)\n'
                        '    await dp.start_polling(bot)',
                'new': [1, 9],
                'notes': [('include_routers',
                           'yangi <code>quiz.router</code> ni qo‘shmasak, tugmalar hech narsa qilmaydi.'),
                          ('python bot.py', "terminalda ishga tushiramiz va Telegram'da /start bosamiz.")],
                'result': 'INFO:aiogram.dispatcher:Start polling\n'
                          'INFO:aiogram.dispatcher:Run polling for bot @minar_quiz_bot'}],
     'flow': [('🔘', 'Fan tugmasi', 'subject:math callback keladi', ''),
              ('🗄', '10 ta savol', 'bazadan tasodifiy: get_questions()', ''),
              ('🧠', 'FSM xotirasi', 'questions · index · score', 'mem'),
              ('❓', 'Savol + 4 tugma', 'send_question()', 'loop'),
              ('✔', 'Javobni tekshirish', 'to‘g‘ri bo‘lsa score + 1', 'loop'),
              ('🏁', 'Natija', '8/10 · state.clear()', '')],
     'loop': '↺ index < 10 bo‘lsa — keyingi savol',
     'chat_title': 'Telegram’da sinab ko‘ramiz',
     'chat_sub': 'python bot.py → /start → fan → 10 ta savol',
     'checks': ['Fan tugmasidan keyin “Test boshlandi” chiqdimi?',
                'Javob bosilgach eski tugmalar yo‘qoldimi?',
                'Noto‘g‘ri javobda to‘g‘ri variant ko‘rsatildimi?',
                '10-savoldan keyin natija chiqib, holat tozalandimi?'],
     'chat': [('user', '/start'),
              ('bot', 'Qaysi fandan test ishlaysiz?', ['🔢 Matematika', '🇬🇧 Ingliz tili', '💻 Informatika']),
              ('bot', '📚 Test boshlandi: 10 ta savol'),
              ('bot', "7 × 8 = ?\n\n✅ To'g'ri!"),
              ('bot', '❓ 2/10\n\n12 : 4 = ?', ['2', '3', '4', '6']),
              ('bot', "🏁 Test tugadi! To'g'ri javoblar: 8/10")],
     'tree': [('quizbot/', ''),
              ('├── bot.py', 'o‘zgardi'),
              ('├── config.py', ''),
              ('├── database.py', 'o‘zgardi'),
              ('├── states.py', 'yangi'),
              ('├── handlers/', ''),
              ('│   ├── start.py', ''),
              ('│   └── quiz.py', 'yangi'),
              ('└── keyboards/', ''),
              ('    ├── subjects.py', ''),
              ('    └── quiz.py', 'yangi')],
     'learned': ['SQL: WHERE, ORDER BY RANDOM(), LIMIT',
                 'FSM xotirasida ro‘yxat va hisoblagich saqlash',
                 'callback_data bilan tugmani aniqlash',
                 'edit_text bilan xabarni yangilash'],
     'homework': ['Majburiy: test boshida “Tayyormisiz?” xabari va [Boshlash] tugmasi qo‘shing.',
                  'Qo‘shimcha: savol matniga fan nomini qo‘shing: “🔢 Matematika · 3/10”.'],
     'files': {'database.py': 'import aiosqlite\n'
                              '\n'
                              'from config import DB_PATH\n'
                              '\n'
                              '\n'
                              'async def create_tables():\n'
                              '    async with aiosqlite.connect(DB_PATH) as db:\n'
                              '        await db.execute(\n'
                              '            "CREATE TABLE IF NOT EXISTS questions ("\n'
                              '            "id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, text TEXT, "\n'
                              '            "a TEXT, b TEXT, c TEXT, d TEXT, correct TEXT)"\n'
                              '        )\n'
                              '        await db.commit()\n'
                              '\n'
                              '\n'
                              'async def get_questions(subject: str, limit: int = 10) -> list[dict]:\n'
                              '    async with aiosqlite.connect(DB_PATH) as db:\n'
                              '        db.row_factory = aiosqlite.Row\n'
                              '        cursor = await db.execute(\n'
                              '            "SELECT id, text, a, b, c, d, correct FROM questions "\n'
                              '            "WHERE subject = ? ORDER BY RANDOM() LIMIT ?",\n'
                              '            (subject, limit),\n'
                              '        )\n'
                              '        rows = await cursor.fetchall()\n'
                              '    return [dict(row) for row in rows]\n',
               'states.py': 'from aiogram.fsm.state import State, StatesGroup\n'
                            '\n'
                            '\n'
                            'class Quiz(StatesGroup):\n'
                            '    answering = State()\n',
               'keyboards/quiz.py': 'from aiogram.utils.keyboard import InlineKeyboardBuilder\n'
                                    '\n'
                                    '\n'
                                    'def answers_kb(question: dict):\n'
                                    '    kb = InlineKeyboardBuilder()\n'
                                    '    for key in ("a", "b", "c", "d"):\n'
                                    '        kb.button(text=question[key], callback_data=f"ans:{key}")\n'
                                    '    kb.adjust(1)\n'
                                    '    return kb.as_markup()\n',
               'handlers/quiz.py': 'from aiogram import F, Router\n'
                                   'from aiogram.fsm.context import FSMContext\n'
                                   'from aiogram.types import CallbackQuery, Message\n'
                                   '\n'
                                   'from database import get_questions\n'
                                   'from keyboards.quiz import answers_kb\n'
                                   'from states import Quiz\n'
                                   '\n'
                                   'router = Router()\n'
                                   '\n'
                                   '\n'
                                   'async def send_question(message: Message, state: FSMContext):\n'
                                   '    data = await state.get_data()\n'
                                   '    index = data["index"]\n'
                                   '    question = data["questions"][index]\n'
                                   '    total = len(data["questions"])\n'
                                   '    await message.answer(\n'
                                   '        f"❓ {index + 1}/{total}\\n\\n{question[\'text\']}",\n'
                                   '        reply_markup=answers_kb(question),\n'
                                   '    )\n'
                                   '\n'
                                   '\n'
                                   '@router.callback_query(F.data.startswith("subject:"))\n'
                                   'async def start_quiz(callback: CallbackQuery, state: FSMContext):\n'
                                   '    subject = callback.data.split(":")[1]\n'
                                   '    questions = await get_questions(subject)\n'
                                   '    if not questions:\n'
                                   '        await callback.answer("Bu fanda hali savol yo\'q", show_alert=True)\n'
                                   '        return\n'
                                   '    await state.set_state(Quiz.answering)\n'
                                   '    await state.update_data(questions=questions, index=0, score=0)\n'
                                   '    await callback.message.edit_text(f"📚 Test boshlandi: {len(questions)} ta '
                                   'savol")\n'
                                   '    await send_question(callback.message, state)\n'
                                   '    await callback.answer()\n'
                                   '\n'
                                   '\n'
                                   '@router.callback_query(Quiz.answering, F.data.startswith("ans:"))\n'
                                   'async def check_answer(callback: CallbackQuery, state: FSMContext):\n'
                                   '    chosen = callback.data.split(":")[1]\n'
                                   '    data = await state.get_data()\n'
                                   '    question = data["questions"][data["index"]]\n'
                                   '    score = data["score"]\n'
                                   '    if chosen == question["correct"]:\n'
                                   '        score += 1\n'
                                   '        mark = "✅ To\'g\'ri!"\n'
                                   '    else:\n'
                                   '        mark = f"❌ Noto\'g\'ri. Javob: {question[question[\'correct\']]}"\n'
                                   '    await callback.message.edit_text(f"{question[\'text\']}\\n\\n{mark}")\n'
                                   '    index = data["index"] + 1\n'
                                   '    await state.update_data(index=index, score=score)\n'
                                   '    if index < len(data["questions"]):\n'
                                   '        await send_question(callback.message, state)\n'
                                   '    else:\n'
                                   '        await state.clear()\n'
                                   '        await callback.message.answer(f"🏁 Test tugadi! To\'g\'ri javoblar: '
                                   '{score}/{index}")\n'
                                   '    await callback.answer()\n',
               'bot.py': 'import asyncio\n'
                         'import logging\n'
                         '\n'
                         'from aiogram import Bot, Dispatcher\n'
                         '\n'
                         'from config import BOT_TOKEN\n'
                         'from database import create_tables\n'
                         'from handlers import quiz, start\n'
                         '\n'
                         '\n'
                         'async def main():\n'
                         '    logging.basicConfig(level=logging.INFO)\n'
                         '    await create_tables()\n'
                         '    bot = Bot(token=BOT_TOKEN)\n'
                         '    dp = Dispatcher()\n'
                         '    dp.include_routers(start.router, quiz.router)\n'
                         '    await dp.start_polling(bot)\n'
                         '\n'
                         '\n'
                         'if __name__ == "__main__":\n'
                         '    asyncio.run(main())\n'},
     'next': '6.11 · Test rejimi, 2-qism: natijani attempts jadvaliga saqlash va “Mening natijalarim”.'},
}



def _tb10_full_project():
    """TB10 fayllari 6-oy loyihasining shu darsdagi to'liq holati (oldingi darslar ustiga yoziladi)."""
    from .lessons_m06 import BOT_FINAL, DB_TB10, MENU_FINAL, STATES_FULL

    lesson = LESSONS["TB10"]
    lesson["files"].update(
        {"database.py": DB_TB10, "states.py": STATES_FULL, "handlers/menu.py": MENU_FINAL, "bot.py": BOT_FINAL}
    )
    last = lesson["steps"][-1]
    last["code"] = last["code"].replace("from handlers import quiz, start", "from handlers import menu, quiz, register, start")
    last["code"] = last["code"].replace(
        "dp.include_routers(start.router, quiz.router)",
        "dp.include_routers(start.router, register.router, menu.router, quiz.router)",
    )
    last["notes"] = last["notes"] + [
        ("menu.py", "5-darsdagi “Tanlandi” callback'ini o'chiramiz — endi fan tugmasini quiz.router ushlaydi."),
    ]


_tb10_full_project()
