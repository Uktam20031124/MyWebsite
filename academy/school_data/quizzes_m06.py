"""Dasturchi 6-oy (TB01–TB12, TB10 — ``quizzes_dev.py``) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "TB01": """
? Yangi Telegram bot qaysi bot orqali yaratiladi?
+ @BotFather
- @TelegramBot
- @NewBot
- @Admin

? Bot tokeni nima?
+ Botni boshqarish uchun maxfiy kalit (parol)
- Botning username'i
- Botning rasmi
- Telegram'dagi kanal

? Token qayerda saqlanadi?
+ .env faylida, kodda emas
- bot.py ichida ochiq
- README.md'da
- GitHub'da

? Dispatcher nima qiladi?
+ Kelgan xabarlarni kerakli handler'ga tarqatadi
- Xabar yuboradi
- Bot yaratadi
- Tokenni saqlaydi

? @dp.message() qanday xabarlarni ushlaydi?
+ Har qanday xabarni
- Faqat /start
- Faqat rasmlarni
- Hech qaysini

? Polling nima?
+ Bot Telegram'dan muntazam “yangi xabar bormi?” deb so'raydi
- Botni o'chirish
- Xabarni o'chirish
- Tokenni yangilash

? async / await nima uchun?
+ Javob kutayotganda bot boshqa xabarlarga ham ulgurishi uchun
- Kodni chiroyli qilish uchun
- Faqat xato chiqarish uchun
- Python shuni talab qiladi

? message.answer(message.text) nima qiladi?
+ Foydalanuvchi yozganini qaytarib yuboradi
- Xabarni o'chiradi
- Botni to'xtatadi
- Hech narsa

? load_dotenv() nima qiladi?
+ .env dagi qiymatlarni muhitga yuklaydi
- .env faylini o'chiradi
- Botni ishga tushiradi
- Token yaratadi

? aiogram qanday o'rnatiladi?
+ pip install aiogram
- python aiogram
- import install aiogram
- npm install aiogram
""",
    "TB02": """
? Router nima?
+ Handlerlar guruhi
- Botning tokeni
- Telegram serveri
- Tugma turi

? CommandStart() filtri qaysi xabarni ushlaydi?
+ /start
- /help
- Har qanday matnni
- Rasmlarni

? Command("help") qaysi buyruq uchun?
+ /help
- /start
- help so'zi bor har qanday matn
- Hech qaysi

? F.text filtri nimani bildiradi?
+ Matnli har qanday xabar
- Faqat /start
- Faqat rasm
- Bo'sh xabar

? message.from_user.first_name nima?
+ Yozgan foydalanuvchining ismi
- Botning nomi
- Chat nomi
- Token

? Handlerlar qaysi tartibda tekshiriladi?
+ Yuqoridan pastga — birinchi mos kelgani ishlaydi
- Pastdan yuqoriga
- Tasodifiy
- Hammasi birdan

? Nega F.text handler eng oxirida turadi?
+ Aks holda u /start va /help ni ham ushlab qoladi
- Tezroq ishlashi uchun
- Python talab qiladi
- Farqi yo'q

? dp.include_router(router) nima qiladi?
+ Router handlerlarini Dispatcher'ga ulaydi
- Routerni o'chiradi
- Bot yaratadi
- Xabar yuboradi

? Router'ning afzalligi?
+ Handlerlarni mavzu bo'yicha alohida fayllarga bo'lish mumkin
- Bot tezlashadi
- Token kerak bo'lmaydi
- Tugmalar o'zi paydo bo'ladi

? f"Salom, {ism}!" da ism = "Ali" bo'lsa bot nima yozadi?
+ Salom, Ali!
- Salom, {ism}!
- Salom, ism!
- Xato
""",
    "TB03": """
? config.py nima uchun?
+ Token va sozlamalarni bir joyda saqlash uchun
- Handlerlar uchun
- Tugmalar uchun
- Baza uchun

? handlers/ papkasida nima turadi?
+ Mavzular bo'yicha router fayllari
- Rasmlar
- .env fayli
- Baza fayli

? Papkani import qilish uchun ichida qaysi fayl kerak?
+ __init__.py
- main.py
- config.py
- README.md

? bot.py'ning yangi vazifasi?
+ Faqat botni ishga tushirish va routerlarni ulash
- Hamma handlerlarni saqlash
- Tugmalarni chizish
- Bazani yaratish

? dp.include_routers(a, b) nima qiladi?
+ Bir nechta routerni birdan ulaydi
- Faqat birinchisini ulaydi
- Routerlarni o'chiradi
- Xato beradi

? logging.basicConfig(level=logging.INFO) nima beradi?
+ Terminalda bot nima qilayotganini ko'rsatadi
- Xatolarni yashiradi
- Botni tezlashtiradi
- Faylga yozadi

? os.getenv("DB_PATH", "quizbot.db") DB_PATH yo'q bo'lsa nima qaytaradi?
+ "quizbot.db"
- None
- Xato
- ""

? from handlers import start dan keyin router qanday olinadi?
+ start.router
- router.start
- handlers.router
- start()

? Kodni fayllarga bo'lishning foydasi?
+ O'qish, topish va jamoada ishlash oson
- Bot tezlashadi
- Token kerak emas
- Hech qanday

? keyboards/ papkasi nima uchun?
+ Tugmalarni yasovchi funksiyalar uchun
- Handlerlar uchun
- Baza uchun
- Rasmlar uchun
""",
    "TB04": """
? Reply tugmalar qayerda chiqadi?
+ Chat ostida, klaviatura o'rnida
- Xabar ichida
- Bot profilida
- Kanalda

? Reply tugma bosilganda botga nima keladi?
+ Tugmadagi matn oddiy xabar bo'lib
- callback_data
- Rasm
- Hech narsa

? ReplyKeyboardBuilder nima qiladi?
+ Pastki tugmalarni yig'adi
- Inline tugmalar yasaydi
- Xabar o'chiradi
- Bot yaratadi

? kb.adjust(2) nima qiladi?
+ Har qatorda 2 ta tugma joylaydi
- 2 ta tugma qoldiradi
- Tugmalarni 2 marta takrorlaydi
- Xato

? resize_keyboard=True nima beradi?
+ Tugmalar ixcham bo'ladi
- Tugmalar yo'qoladi
- Tugmalar katta bo'ladi
- Faqat bitta tugma

? Tugmani xabar bilan qanday yuboramiz?
+ message.answer(..., reply_markup=main_menu())
- message.button()
- send_keyboard()
- main_menu.send()

? F.text == "❓ Yordam" filtri qachon ishlaydi?
+ Matn aynan shu bo'lganda (emoji bilan)
- "yordam" so'zi bor har qanday matnda
- Har doim
- Hech qachon

? Menyuni yashirish uchun nima ishlatiladi?
+ ReplyKeyboardRemove()
- kb.delete()
- adjust(0)
- Hech narsa

? Reply va inline tugma farqi?
+ Reply — chat ostida, matn yuboradi; inline — xabar ostida, callback yuboradi
- Farqi yo'q
- Inline chat ostida
- Reply callback yuboradi

? main_menu() funksiyasi nima qaytaradi?
+ Tugmalar belgisini (markup)
- Matn
- Xabar
- None
""",
    "TB05": """
? Inline tugmalar qayerda chiqadi?
+ Xabarning ostida
- Chat ostida
- Profilda
- Menyu tugmasida

? callback_data nima?
+ Tugma bosilganda botga yashirin keladigan matn
- Tugmadagi ko'rinadigan matn
- Foydalanuvchi ismi
- Token

? Inline tugma bosilishini qaysi handler ushlaydi?
+ callback_query
- message
- command
- contact

? F.data.startswith("subject:") nimani ushlaydi?
+ callback_data subject: bilan boshlangan tugmalarni
- Hamma xabarlarni
- /subject buyrug'ini
- Rasmlarni

? callback.data = "subject:english". split(":")[1] nima?
+ "english"
- "subject"
- "subject:english"
- Xato

? edit_text nima qiladi?
+ Eski xabarni yangi matn bilan almashtiradi
- Yangi xabar yuboradi
- Xabarni o'chiradi
- Tugma qo'shadi

? callback.answer() chaqirilmasa nima bo'ladi?
+ Tugmada “soat” belgisi osilib qoladi
- Bot to'xtaydi
- Xabar o'chadi
- Hech narsa

? Nega callback_data'ga prefiks (subject:) qo'yamiz?
+ Boshqa tugmalardan ajratish oson bo'lsin
- Telegram talab qiladi
- Tezroq ishlashi uchun
- Shart emas

? InlineKeyboardBuilder'da tugma qanday qo'shiladi?
+ kb.button(text=..., callback_data=...)
- kb.add(text)
- kb.inline(text)
- kb.new(...)

? edit_text'dan keyin eski tugmalar bilan nima bo'ladi?
+ Yo'qoladi (reply_markup berilmasa)
- Qoladi
- Ikki baravar ko'payadi
- Xato chiqadi
""",
    "TB06": """
? FSM nima?
+ Holatlar mashinasi — foydalanuvchi qaysi bosqichda ekanini eslaydi
- Tugma turi
- Baza
- Token

? Holatlar qanday e'lon qilinadi?
+ class Register(StatesGroup): name = State() ...
- def Register(): ...
- Register = []
- import states

? state.set_state(Register.phone) nima qiladi?
+ Foydalanuvchini telefon bosqichiga o'tkazadi
- Telefonni saqlaydi
- Holatni o'chiradi
- Xabar yuboradi

? state.update_data(name="Ali") nima qiladi?
+ FSM xotirasiga ism yozadi
- Bazaga yozadi
- Xabar yuboradi
- Holatni o'zgartiradi

? @router.message(Register.name, F.text) handler qachon ishlaydi?
+ Foydalanuvchi ism bosqichida matn yozganda
- Har doim
- Faqat /start da
- Kontakt yuborilganda

? F.contact filtri nimani ushlaydi?
+ Kontakt (telefon raqam) yuborilganini
- Har qanday matnni
- Rasmlarni
- Buyruqlarni

? Kontakt tugmasi qanday yasaladi?
+ kb.button(text="📱 ...", request_contact=True)
- kb.contact()
- callback_data="phone"
- InlineKeyboardButton(phone=True)

? state.clear() nima qiladi?
+ Holat va FSM xotirasini tozalaydi
- Bazani tozalaydi
- Chatni o'chiradi
- Botni to'xtatadi

? Ism 1 harf bo'lsa nima qilamiz?
+ Ogohlantirib, holatni o'zgartirmaymiz — qayta so'raymiz
- Qabul qilamiz
- Botni to'xtatamiz
- Keyingi bosqichga o'tamiz

? state.update_data(...) nima qaytaradi?
+ Xotiradagi barcha ma'lumotlar lug'atini
- None
- Holat nomini
- Xato
""",
    "TB07": """
? SQLite nima?
+ Bitta faylda saqlanadigan ma'lumotlar bazasi
- Dasturlash tili
- Telegram kutubxonasi
- Server

? CREATE TABLE nima qiladi?
+ Ustunlari bilan yangi jadval yaratadi
- Qator qo'shadi
- Jadvalni o'chiradi
- Ma'lumot o'qiydi

? INSERT INTO nima qiladi?
+ Jadvalga yangi qator qo'shadi
- Jadval yaratadi
- Qatorni o'chiradi
- Qatorni o'qiydi

? SELECT name FROM users nima qaytaradi?
+ Hamma foydalanuvchilarning ismlarini
- Faqat birinchisini
- Jadval tuzilmasini
- Hech narsa

? WHERE grade > 8 nimani bildiradi?
+ Faqat sinfi 8 dan katta qatorlar
- 8 ta qator
- 8-qator
- Hammasi

? Nega qiymatlarni ? orqali beramiz?
+ SQL injection'dan himoya uchun
- Tezroq ishlashi uchun
- Majburiy emas, farqi yo'q
- Chiroyli ko'rinishi uchun

? con.commit() nima uchun?
+ O'zgarishlarni faylga yozish uchun
- Jadvalni o'chirish uchun
- Ulanishni ochish uchun
- O'qish uchun

? PRIMARY KEY nima?
+ Har qatorni aniqlovchi takrorlanmas ustun
- Birinchi ustun har doim
- Parol
- Jadval nomi

? SELECT COUNT(*) FROM users nima qaytaradi?
+ Qatorlar sonini
- Ustunlar sonini
- Birinchi qatorni
- Hammasini

? fetchone() va fetchall() farqi?
+ fetchone — bitta qator, fetchall — hamma qatorlar
- Farqi yo'q
- fetchall bitta qator
- fetchone hammasini
""",
    "TB08": """
? Nega botda sqlite3 emas, aiosqlite ishlatamiz?
+ Async — baza kutayotganda bot boshqa xabarlarga ulguradi
- sqlite3 ishlamaydi
- aiosqlite tezroq yozadi
- Farqi yo'q

? async with aiosqlite.connect(DB_PATH) as db: nima qiladi?
+ Bazaga ulanadi va blok tugagach yopadi
- Bazani o'chiradi
- Jadval yaratadi
- Xabar yuboradi

? INSERT OR REPLACE nima qiladi?
+ Bunday id bo'lsa yangilaydi, yo'q bo'lsa qo'shadi
- Har doim xato beradi
- Faqat qo'shadi
- Faqat o'chiradi

? Foydalanuvchini bazada qanday aniqlaymiz?
+ message.from_user.id — Telegram'dagi takrorlanmas id
- Ismi bo'yicha
- Telefon bo'yicha
- Tasodifiy son

? get_user() foydalanuvchi bo'lmasa nima qaytaradi?
+ None
- Bo'sh lug'at
- Xato
- 0

? create_tables() qachon chaqiriladi?
+ Bot ishga tushganda, polling'dan oldin
- Har xabarda
- Hech qachon
- Ro'yxatdan o'tganda

? Profil tugmasi ro'yxatdan o'tmagan foydalanuvchiga nima deydi?
+ Avval ro'yxatdan o'ting: /register
- Xato
- Hech narsa
- Bo'sh profil

? name, phone, grade = user nima qiladi?
+ Qatorni uchta o'zgaruvchiga ochadi
- Uch marta so'raydi
- Xato beradi
- Bazaga yozadi

? Bot qayta ishga tushganda profil saqlanadimi?
+ Ha — ma'lumot bazada
- Yo'q — xotirada edi
- Faqat admin uchun
- Faqat bir kun

? Baza funksiyalarini chaqirishda nima kerak?
+ await
- yield
- return
- Hech narsa
""",
    "TB09": """
? Seed skripti nima?
+ Bazani boshlang'ich ma'lumot bilan to'ldiradigan skript
- Bot handleri
- Tugma
- Test

? Nega to'g'ri javobni harf (b) bilan saqlaymiz?
+ Variantlar tugmasi qaysi harf bosilganini yuboradi — solishtirish oson
- Joy tejash uchun
- Telegram talab qiladi
- Farqi yo'q

? executemany nima qiladi?
+ Ro'yxatdagi har bir tuple uchun so'rovni bajaradi
- Bitta qator qo'shadi
- Jadvalni o'chiradi
- Hammasini o'qiydi

? AUTOINCREMENT nima?
+ id o'zi oshib boradi
- id har doim 1
- Tasodifiy id
- id kerak emas

? GROUP BY subject nima qiladi?
+ Bir xil fanlarni guruhlab, har biriga hisob chiqaradi
- Fanlarni o'chiradi
- Saralaydi
- Birlashtiradi

? ORDER BY subject nima qiladi?
+ Natijani fan nomi bo'yicha saralaydi
- Guruhlaydi
- O'chiradi
- Sanaydi

? Savol jadvalida nechta variant ustuni bor?
+ 4 ta: a, b, c, d
- 2 ta
- 3 ta
- 5 ta

? Seed ikki marta ishga tushsa nima bo'ladi (DELETE'siz)?
+ Savollar takrorlanib qoladi
- Xato chiqadi
- Hech narsa
- Eskilari o'chadi

? SELECT subject, COUNT(*) ... GROUP BY subject natijasi?
+ Har fan va undagi savollar soni
- Faqat jami son
- Faqat fanlar nomi
- Barcha savollar

? Seed skripti qanday ishga tushiriladi?
+ python seed.py — bir marta
- Bot ichida har xabarda
- Telegram orqali
- Avtomatik har kuni
""",
    "TB11": """
? attempts jadvali nima saqlaydi?
+ Har bir test urinishi: kim, fan, ball, jami, vaqt
- Savollarni
- Foydalanuvchilarni
- Tugmalarni

? DEFAULT CURRENT_TIMESTAMP nima beradi?
+ Qator qo'shilgan vaqt o'zi yoziladi
- Vaqtni o'chiradi
- Har doim 0
- Xato

? ORDER BY id DESC nima qiladi?
+ Eng yangi qatorlar birinchi chiqadi
- Eng eskisi birinchi
- Tasodifiy tartib
- Saralamaydi

? LIMIT 5 nimani bildiradi?
+ Ko'pi bilan 5 ta qator
- Kamida 5 ta
- 5-qator
- 5 ta ustun

? Fan nomi test oxirida qayerdan olinadi?
+ start_quiz'da FSM xotirasiga yozilgan subject'dan
- Bazadan
- Tugmadan qayta
- Foydalanuvchidan so'rab

? 8 ta to'g'ri 10 tadan. foiz = round(8 / 10 * 100) nechaga teng?
+ 80
- 8
- 0.8
- 800

? save_attempt qachon chaqiriladi?
+ Oxirgi savolga javob berilgach
- Har savolda
- Test boshida
- Hech qachon

? vaqt[:16] nima qiladi?
+ Sanadan soniyalarni olib tashlaydi
- Sanani o'chiradi
- 16 kun qo'shadi
- Xato

? “📈 Natijalarim” hali test ishlamaganga nima deydi?
+ Hali test ishlamadingiz
- Xato
- 0/0
- Hech narsa

? INSERT'da nega id va created_at ko'rsatilmaydi?
+ Ular o'zi to'ldiriladi
- Ular kerak emas
- Xato chiqmasligi uchun shart emas
- Telegram to'ldiradi
""",
    "TB12": """
? Routerlar nega start → register → menu → quiz tartibida?
+ Umumiy F.text handlerlar oxirida bo'lishi kerak
- Alifbo tartibi
- Tasodifiy
- Telegram talab qiladi

? QuizBot'da nechta jadval bor?
+ 3: users, questions, attempts
- 1
- 2
- 5

? requirements.txt nima uchun?
+ Boshqa kompyuterda kerakli kutubxonalarni bir xil versiyada o'rnatish uchun
- Token saqlash uchun
- Savollar uchun
- Shart emas

? README'da nimalar bo'lishi kerak?
+ Bot nima qiladi va qanday ishga tushiriladi
- Token
- Parollar
- Hech narsa

? Demo oldidan nima tayyor bo'lishi kerak?
+ .env, token va savollar (seed)
- Faqat README
- Hech narsa
- Yangi bot

? Nega menu.py dan eski “Tanlandi” callback olib tashlandi?
+ Aks holda u fan tugmasini quiz routeridan oldin ushlaydi
- Xato bergani uchun
- Kod uzun bo'lgani uchun
- Telegram taqiqlagani uchun

? Bot ma'lumotlari qayerda saqlanadi?
+ quizbot.db (SQLite) faylida
- Telegram'da
- .env da
- README'da

? FSM qaysi bosqichlarda ishlatildi?
+ Ro'yxatdan o'tish va test rejimi
- Faqat /start
- Faqat profil
- Hech qayerda

? .env GitHub'ga yuklanadimi?
+ Yo'q — .gitignore'da
- Ha
- Faqat token
- Faqat bir marta

? 6-oyda o'rganilmagan mavzu qaysi?
+ Admin panel va broadcast (7-oyda)
- FSM
- Inline tugmalar
- SQLite
""",
}
