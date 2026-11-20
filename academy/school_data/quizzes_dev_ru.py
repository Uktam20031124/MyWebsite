"""Ruscha tarjima: ``quizzes_dev.py`` bilan bir xil kalitlar, savollar tartibi va to'g'ri javob o'rni."""

from .quizzes_m03_ru import QUIZZES as M03
from .quizzes_m04_ru import QUIZZES as M04
from .quizzes_m05_ru import QUIZZES as M05
from .quizzes_m06_ru import QUIZZES as M06
from .quizzes_m07_ru import QUIZZES as M07
from .quizzes_m08_ru import QUIZZES as M08
from .quizzes_m09_ru import QUIZZES as M09
from .quizzes_m10_ru import QUIZZES as M10

QUIZZES = {
    "TB10": """
? Что делает ORDER BY RANDOM() LIMIT 10?
+ Берёт 10 случайных строк
- Берёт первые 10 строк
- Удаляет 10 строк
- Сортирует и сохраняет таблицу

? Почему название предмета передаётся в SQL через ?, а не через f-строку?
+ Для защиты от SQL-инъекций
- Чтобы работало быстрее
- f-строка не работает в async-функции
- Разницы нет

? Какое поле приходит боту при нажатии inline-кнопки?
+ callback_data
- text
- reply_markup
- message_id

? Если callback.data = "subject:math", что вернёт callback.data.split(":")[1]?
+ "math"
- "subject"
- "subject:math"
- Ошибку

? Что делает state.update_data(index=0, score=0)?
+ Записывает значения в память FSM
- Записывает в базу данных
- Сбрасывает состояние
- Отправляет сообщение

? Зачем после ответа менять сообщение с вопросом через edit_text?
+ Кнопки исчезают, и нажать повторно нельзя
- Сообщение удаляется
- Бот работает быстрее
- Балл сохраняется в базу

? Что обеспечивает фильтр Quiz.answering в обработчике check_answer?
+ После окончания теста старые кнопки не работают
- Нажать может только админ
- Ответ всегда будет верным
- Вопросы идут в случайном порядке

? Что будет, если не вызвать callback.answer()?
+ На кнопке останется значок «часов»
- Бот остановится
- Сообщение удалится
- Ничего не изменится

? Что делает state.clear() в конце теста?
+ Сбрасывает состояние и данные в памяти FSM
- Очищает базу данных
- Удаляет чат
- Перезапускает бота

? Что будет, если не добавить quiz.router в dp.include_routers?
+ Кнопки предметов и ответов не будут работать
- Не будет работать /start
- Бот вообще не запустится
- Ничего не изменится
""",
}
QUIZZES = {**M03, **M04, **M05, **M06, **M07, **M08, **M09, **M10, **QUIZZES}
