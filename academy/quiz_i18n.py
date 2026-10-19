"""O'quvchi ko'radigan test sahifalari va xabarlar matnlari: o'zbekcha va ruscha.

Ustoz interfeysi o'zbekcha qoladi; bu yerda faqat o'quvchiga boradigan matnlar.
"""

from .models import QuizLanguage

UZ, RU = QuizLanguage.UZ, QuizLanguage.RU

_TEXTS = {
    UZ: {
        "kicker": "Darsxona · test",
        "hello": "Salom",
        "rule_questions": "{n} ta savol, har birida bitta to‘g‘ri javob.",
        "rule_time": "Vaqt: <strong>{m} daqiqa</strong>. Vaqt tugasa test avtomatik yakunlanadi.",
        "rule_once": "Havola <strong>faqat bir marta</strong> ishlaydi: boshlagandan keyin uni "
        "boshqa qurilmada ochib bo‘lmaydi.",
        "rule_leave": "Test paytida <strong>boshqa oyna yoki ilovaga o‘tish qayd qilinadi</strong> "
        "va ustozingizga ko‘rinadi.",
        "start": "Testni boshlash",
        "time_left": "Qolgan vaqt",
        "leave_notice": "<strong>Test oynasidan chiqdingiz</strong> — bu qayd qilindi va ustozingizga "
        "ko‘rinadi (jami: <span data-count>0</span> marta).",
        "image_alt": "Savol rasmi",
        "finish": "Testni yakunlash",
        "progress": "{answered} / {total} ta savolga javob berildi",
        "confirm_unanswered": "{left} ta savolga javob berilmagan. Testni yakunlaysizmi?",
        "time_up": "Vaqt tugadi",
        "sending": "Javoblaringiz yuborilmoqda…",
        "result": "Natija",
        "timed_out": "Vaqt tugadi — test avtomatik yakunlandi.",
        "score": "{correct} / {total} to‘g‘ri javob",
        "verdict_high": "Ajoyib! Mavzu yaxshi o‘zlashtirilgan.",
        "verdict_mid": "Yomon emas, lekin mavzuni yana bir bor takrorlang.",
        "verdict_low": "Mavzuni qayta o‘rganib chiqing va ustozingizdan yordam so‘rang.",
        "your_answers": "Javoblaringiz",
        "your_answer": "Javobingiz",
        "no_answer": "Javob berilmagan",
        "right": "to‘g‘ri",
        "wrong": "xato",
        "skipped": "javobsiz",
        "ask_teacher": "To‘g‘ri javoblarni ustozingizdan so‘rang — mavzuni birga takrorlaysiz.",
        "sent_to_teacher": "Natija ustozingizga yuborildi. Test qayta ochilmaydi.",
        "used_title": "Havola ishlatilgan",
        "used_text": "Bu test havolasi allaqachon ochilgan va qayta ishlamaydi.",
        "used_help": "Agar testni siz boshlamagan bo‘lsangiz yoki xato bo‘lsa, ustozingizga murojaat qiling.",
        # Telegram / email
        "msg_quiz": "“{topic}” mavzusi bo‘yicha test: {n} ta savol, {m} daqiqa.",
        "msg_once": "Havola faqat bir marta ishlaydi — testni tayyor bo‘lganingizda oching.",
        "msg_subject": "Test: {topic}",
        "msg_title": "“{topic}” bo‘yicha test",
        "msg_button": "Testni boshlash",
        "msg_counts": "{n} ta savol, {m} daqiqa.",
        "rem_quiz": "“{topic}” mavzusi bo‘yicha test hali ochilmagan: {n} ta savol, {m} daqiqa.",
        "rem_tail": "Vaqtingiz bo‘lganda yechib qo‘ying — natija ustozga boradi.",
        "rem_subject": "Eslatma: “{topic}” testi hali ochilmagan",
        "rem_title": "Test hali ochilmagan",
    },
    RU: {
        "kicker": "Darsxona · тест",
        "hello": "Здравствуйте",
        "rule_questions": "Вопросов: {n}, в каждом один правильный ответ.",
        "rule_time": "Время: <strong>{m} мин</strong>. Когда время закончится, тест завершится "
        "автоматически.",
        "rule_once": "Ссылка работает <strong>только один раз</strong>: после начала её нельзя "
        "открыть на другом устройстве.",
        "rule_leave": "Во время теста <strong>переход в другое окно или приложение фиксируется</strong> "
        "и виден учителю.",
        "start": "Начать тест",
        "time_left": "Осталось времени",
        "leave_notice": "<strong>Вы вышли из окна теста</strong> — это зафиксировано и видно учителю "
        "(всего: <span data-count>0</span> раз).",
        "image_alt": "Изображение к вопросу",
        "finish": "Завершить тест",
        "progress": "Отвечено: {answered} из {total}",
        "confirm_unanswered": "Без ответа вопросов: {left}. Завершить тест?",
        "time_up": "Время вышло",
        "sending": "Ваши ответы отправляются…",
        "result": "Результат",
        "timed_out": "Время вышло — тест завершён автоматически.",
        "score": "Правильных ответов: {correct} из {total}",
        "verdict_high": "Отлично! Тема хорошо усвоена.",
        "verdict_mid": "Неплохо, но повторите тему ещё раз.",
        "verdict_low": "Изучите тему заново и попросите помощи у учителя.",
        "your_answers": "Ваши ответы",
        "your_answer": "Ваш ответ",
        "no_answer": "Нет ответа",
        "right": "верно",
        "wrong": "неверно",
        "skipped": "без ответа",
        "ask_teacher": "Правильные ответы спросите у учителя — разберёте тему вместе.",
        "sent_to_teacher": "Результат отправлен учителю. Тест повторно не открывается.",
        "used_title": "Ссылка уже использована",
        "used_text": "Эта ссылка на тест уже была открыта и больше не работает.",
        "used_help": "Если тест начинали не вы или произошла ошибка, обратитесь к учителю.",
        "msg_quiz": "Тест по теме «{topic}»: вопросов — {n}, время — {m} мин.",
        "msg_once": "Ссылка работает только один раз — открывайте, когда будете готовы.",
        "msg_subject": "Тест: {topic}",
        "msg_title": "Тест по теме «{topic}»",
        "msg_button": "Начать тест",
        "msg_counts": "Вопросов: {n}, время: {m} мин.",
        "rem_quiz": "Тест по теме «{topic}» ещё не открыт: вопросов — {n}, время — {m} мин.",
        "rem_tail": "Решите, когда будет время, — результат придёт учителю.",
        "rem_subject": "Напоминание: тест «{topic}» ещё не открыт",
        "rem_title": "Тест ещё не открыт",
    },
}


def texts(lang: str) -> dict:
    return _TEXTS.get(lang, _TEXTS[UZ])


def attempt_texts(attempt) -> dict:
    """Shablon uchun: shu urinish tilidagi, son va nomlari qo'yilgan matnlar."""
    t = dict(texts(attempt.language))
    t["rule_questions"] = t["rule_questions"].format(n=attempt.question_count)
    t["rule_time"] = t["rule_time"].format(m=attempt.batch.time_limit_minutes)
    if attempt.total:
        t["score"] = t["score"].format(correct=attempt.correct or 0, total=attempt.total)
    t["lang"] = attempt.language
    t["topic"] = attempt.quiz.topic.title_in(attempt.language)
    return t


def message_parts(attempt) -> dict:
    """Telegram/email xabari uchun: shu urinish tilidagi tayyor qatorlar."""
    t = texts(attempt.language)
    values = {
        "topic": attempt.quiz.topic.title_in(attempt.language),
        "n": attempt.question_count,
        "m": attempt.batch.time_limit_minutes,
    }
    return {key: value.format(**values) for key, value in t.items() if key.startswith(("msg_", "rem_"))} | {
        "hello": f"{t['hello']}, {attempt.student.full_name}!"
    }
