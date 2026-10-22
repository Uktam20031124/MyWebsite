"""O'quvchi ko'radigan test sahifalari va xabarlar matnlari: o'zbekcha va ruscha.

Ustoz interfeysi o'zbekcha qoladi; bu yerda faqat o'quvchiga boradigan matnlar.
"""

from django.utils import timezone

from .models import QuizLanguage

UZ, RU = QuizLanguage.UZ, QuizLanguage.RU

_TEXTS = {
    UZ: {
        "kicker": "Minar Test · test",
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
        "ko‘rinadi (jami ogohlantirish: <span data-count>0</span>).",
        "copy_notice": "<strong>Nusxalash va qo‘yish taqiqlangan</strong> — urinish qayd qilindi va "
        "ustozingizga ko‘rinadi (jami ogohlantirish: <span data-count>0</span>).",
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
        "review_ask_hint": "Qaysi savolda to‘g‘ri, qaysida xato qilganingizni ko‘rish uchun "
        "ustozingizdan ruxsat so‘rang.",
        "review_ask": "Javoblarimni ko‘rish uchun ruxsat so‘rash",
        "review_wait": "So‘rov ustozingizga yuborildi. Ruxsat berilgach, javoblaringiz shu sahifada "
        "ko‘rinadi — sahifani keyinroq yangilang.",
        "review_rejected": "Ustozingiz hozircha javoblarni ko‘rsatmaslikka qaror qildi. Savollaringizni darsda bering.",
        "refresh": "Yangilash",
        "review_free_hint": "Javoblaringizni (qaysi savolda to‘g‘ri, qaysida xato) 1 daqiqa ko‘rishingiz mumkin — "
        "faqat bir marta. Keyin qayta ko‘rish uchun ustozingizdan ruxsat so‘raladi.",
        "review_free": "Javoblarimni ko‘rish (1 daqiqa)",
        "review_closes": "Javoblar yopilishiga:",
        "review_again_hint": "1 daqiqalik ko‘rish tugadi. Javoblarni yana ko‘rish uchun ustozingizdan ruxsat so‘rang.",
        "study_offer": "Natija 70% dan past. Mavzuni mustahkamlab oling: tushuntirish va bajarilgan "
        "misollar tayyor — 20 daqiqadan keyin testni qayta topshirasiz.",
        "study_button": "Mavzuni mustahkamlash",
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
        "msg_fallback": "Tugma ishlamasa:",
        "rem_quiz": "“{topic}” mavzusi bo‘yicha test hali ochilmagan: {n} ta savol, {m} daqiqa.",
        "rem_tail": "Vaqtingiz bo‘lganda yechib qo‘ying — natija ustozga boradi.",
        "rem_subject": "Eslatma: “{topic}” testi hali ochilmagan",
        "rem_title": "Test hali ochilmagan",
        # Umumiy havola (bitta havola — ko'p qatnashchi)
        "open_intro": "Testni boshlash uchun familiya, ism va sharifingizni kiriting.",
        "open_name": "F.I.Sh.",
        "open_name_ph": "Masalan: Aliyev Vali Karimovich",
        "open_name_error": "F.I.Sh.ni to‘liq kiriting — kamida familiya va ism.",
        "open_duplicate": "Bu F.I.Sh. bilan test allaqachon topshirilgan. Xato bo‘lsa, ustozingizga murojaat qiling.",
        "open_lang": "Test tili",
        "open_rule_once": "Testni <strong>bir marta</strong> topshirasiz: boshlagandan keyin uni boshqa "
        "qurilmada davom ettirib bo‘lmaydi.",
        "open_closes": "Test {date} gacha ochiq.",
        "open_closed_title": "Test yopilgan",
        "open_closed_text": "Bu test havolasi hozir faol emas yoki muddati tugagan.",
        "open_sent": "Natijangiz ustozga yuborildi. Rahmat!",
        "open_empty": "Bu testda hali savollar yo‘q. Ustozingizga murojaat qiling.",
        "msg_open_how": "Havolani oching, F.I.Sh.ingizni kiriting va “Testni boshlash” tugmasini bosing.",
        "msg_open_once": "Testni bir marta topshirish mumkin — tayyor bo‘lganingizda oching.",
        "msg_open_hello": "Assalomu alaykum!",
    },
    RU: {
        "kicker": "Minar Test · тест",
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
        "(всего предупреждений: <span data-count>0</span>).",
        "copy_notice": "<strong>Копирование и вставка запрещены</strong> — попытка зафиксирована и видна "
        "учителю (всего предупреждений: <span data-count>0</span>).",
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
        "review_ask_hint": "Чтобы увидеть, где вы ответили верно, а где ошиблись, попросите разрешение у учителя.",
        "review_ask": "Попросить разрешение посмотреть ответы",
        "review_wait": "Запрос отправлен учителю. Когда он разрешит, ваши ответы появятся на этой "
        "странице — обновите её позже.",
        "review_rejected": "Учитель решил пока не показывать ответы. Задайте вопросы на уроке.",
        "refresh": "Обновить",
        "review_free_hint": "Свои ответы (где верно, где ошибка) можно посмотреть 1 минуту — только один раз. "
        "Для повторного просмотра понадобится разрешение учителя.",
        "review_free": "Посмотреть мои ответы (1 минута)",
        "review_closes": "До закрытия ответов:",
        "review_again_hint": "Минута просмотра закончилась. Чтобы посмотреть ответы снова, "
        "попросите разрешение у учителя.",
        "study_offer": "Результат ниже 70%. Закрепите тему: объяснение и решённые примеры уже "
        "готовы — через 20 минут сможете пересдать тест.",
        "study_button": "Закрепить тему",
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
        "msg_fallback": "Если кнопка не работает:",
        "rem_quiz": "Тест по теме «{topic}» ещё не открыт: вопросов — {n}, время — {m} мин.",
        "rem_tail": "Решите, когда будет время, — результат придёт учителю.",
        "rem_subject": "Напоминание: тест «{topic}» ещё не открыт",
        "rem_title": "Тест ещё не открыт",
        "open_intro": "Чтобы начать тест, введите фамилию, имя и отчество.",
        "open_name": "Ф.И.О.",
        "open_name_ph": "Например: Алиев Вали Каримович",
        "open_name_error": "Введите Ф.И.О. полностью — как минимум фамилию и имя.",
        "open_duplicate": "Тест с таким Ф.И.О. уже сдан. Если это ошибка, обратитесь к учителю.",
        "open_lang": "Язык теста",
        "open_rule_once": "Тест сдаётся <strong>один раз</strong>: после начала продолжить его на другом "
        "устройстве нельзя.",
        "open_closes": "Тест открыт до {date}.",
        "open_closed_title": "Тест закрыт",
        "open_closed_text": "Эта ссылка на тест сейчас не активна или срок её действия истёк.",
        "open_sent": "Ваш результат отправлен учителю. Спасибо!",
        "open_empty": "В этом тесте пока нет вопросов. Обратитесь к учителю.",
        "msg_open_how": "Откройте ссылку, введите своё Ф.И.О. и нажмите «Начать тест».",
        "msg_open_once": "Тест можно сдать один раз — открывайте, когда будете готовы.",
        "msg_open_hello": "Здравствуйте!",
    },
}


def texts(lang: str) -> dict:
    return _TEXTS.get(lang, _TEXTS[UZ])


def attempt_texts(attempt) -> dict:
    """Shablon uchun: shu urinish tilidagi, son va nomlari qo'yilgan matnlar."""
    t = dict(texts(attempt.language))
    t["rule_questions"] = t["rule_questions"].format(n=attempt.question_count)
    t["rule_time"] = t["rule_time"].format(m=attempt.time_limit_minutes)
    if attempt.total:
        t["score"] = t["score"].format(correct=attempt.correct or 0, total=attempt.total)
    t["lang"] = attempt.language
    open_quiz = getattr(attempt, "open_quiz", None)
    t["topic"] = (open_quiz and open_quiz.title) or attempt.quiz.topic.title_in(attempt.language)
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


def open_quiz_texts(open_quiz, lang: str) -> dict:
    """Umumiy havola kirish sahifasi uchun matnlar (``lang`` — qatnashchi tanlagan til)."""
    t = dict(texts(lang))
    n = open_quiz.question_total
    t["rule_questions"] = t["rule_questions"].format(n=n)
    t["rule_time"] = t["rule_time"].format(m=open_quiz.time_limit_minutes)
    if open_quiz.closes_at:
        closes = timezone.localtime(open_quiz.closes_at)
        t["open_closes"] = t["open_closes"].format(date=closes.strftime("%d.%m.%Y %H:%M"))
    t["lang"] = lang
    t["topic"] = open_quiz.title or open_quiz.quiz.topic.title_in(lang)
    return t


def open_message_parts(open_quiz, lang: str) -> dict:
    """Umumiy havola xati: shu tildagi tayyor qatorlar."""
    t = texts(lang)
    values = {
        "topic": open_quiz.title or open_quiz.quiz.topic.title_in(lang),
        "n": open_quiz.question_total,
        "m": open_quiz.time_limit_minutes,
    }
    keys = (
        "msg_quiz", "msg_subject", "msg_title", "msg_button", "msg_fallback",
        "msg_open_how", "msg_open_once", "msg_open_hello",
    )
    return {key: t[key].format(**values) for key in keys}
