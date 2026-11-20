"""Minar Dasturchi darslari bo'yicha test savollari (har darsga 10 ta). Format va kalitlar — ``quizzes_ai.py`` kabi."""

from .quizzes_m03 import QUIZZES as M03
from .quizzes_m04 import QUIZZES as M04
from .quizzes_m05 import QUIZZES as M05
from .quizzes_m06 import QUIZZES as M06
from .quizzes_m07 import QUIZZES as M07
from .quizzes_m08 import QUIZZES as M08
from .quizzes_m09 import QUIZZES as M09

QUIZZES = {
    "TB10": """
? ORDER BY RANDOM() LIMIT 10 nima qiladi?
+ Tasodifiy 10 ta qatorni oladi
- Birinchi 10 ta qatorni oladi
- 10 ta qatorni o'chiradi
- Jadvalni saralab saqlaydi

? Nega SQL so'roviga fan nomini f-string bilan emas, ? orqali beramiz?
+ SQL injection'dan himoya uchun
- Tezroq ishlashi uchun
- f-string async funksiyada ishlamaydi
- Farqi yo'q

? Inline tugma bosilganda botga qaysi maydon keladi?
+ callback_data
- text
- reply_markup
- message_id

? callback.data = "subject:math" bo'lsa, callback.data.split(":")[1] nima beradi?
+ "math"
- "subject"
- "subject:math"
- Xato beradi

? state.update_data(index=0, score=0) nima qiladi?
+ FSM xotirasiga qiymatlarni yozadi
- Bazaga yozadi
- Holatni o'chiradi
- Xabar yuboradi

? Javob berilgach savol xabarini edit_text bilan o'zgartirish nimaga kerak?
+ Tugmalar yo'qoladi va qayta bosib bo'lmaydi
- Xabar o'chib ketadi
- Bot tezlashadi
- Ball bazaga saqlanadi

? check_answer handleridagi Quiz.answering filtri nimani ta'minlaydi?
+ Test tugagach eski tugmalar ishlamaydi
- Faqat admin bosa oladi
- Javob har doim to'g'ri bo'ladi
- Savollar tasodifiy chiqadi

? callback.answer() chaqirilmasa nima bo'ladi?
+ Tugmada “soat” belgisi osilib qoladi
- Bot to'xtab qoladi
- Xabar o'chib ketadi
- Hech narsa o'zgarmaydi

? Test tugaganda state.clear() nima qiladi?
+ Holat va FSM xotirasidagi ma'lumotni tozalaydi
- Bazani tozalaydi
- Chatni o'chiradi
- Botni qayta ishga tushiradi

? quiz.router ni dp.include_routers ga qo'shmasak nima bo'ladi?
+ Fan va javob tugmalari ishlamaydi
- /start ishlamaydi
- Bot umuman ishga tushmaydi
- Hech narsa o'zgarmaydi
""",
}
QUIZZES = {**M03, **M04, **M05, **M06, **M07, **M08, **M09, **QUIZZES}
