"""Dasturchi 7-oy (TB13–TB24) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "TB13": """
? JOIN nima qiladi?
+ Ikki jadvalni umumiy ustun bo'yicha bog'laydi
- Jadvalni o'chiradi
- Qator qo'shadi
- Jadvalni nusxalaydi

? attempts va users qaysi ustunlar orqali bog'lanadi?
+ attempts.user_id = users.id
- attempts.id = users.id
- attempts.score = users.grade
- Bog'lanmaydi

? SUM(a.score) nima qaytaradi?
+ Ballar yig'indisini
- Ballar sonini
- Eng katta ballni
- O'rtacha ballni

? GROUP BY a.user_id nima uchun kerak?
+ Har o'quvchi uchun alohida yig'indi hisoblash uchun
- Saralash uchun
- O'chirish uchun
- Shart emas

? ORDER BY ball DESC nima qiladi?
+ Eng katta ballni birinchi qo'yadi
- Eng kichikni birinchi
- Tasodifiy tartib
- Saralamaydi

? LIMIT 10 nimani bildiradi?
+ Ko'pi bilan 10 qator
- Kamida 10 qator
- 10-qator
- 10 ta ustun

? "a" va "u" (FROM attempts a JOIN users u) nima?
+ Jadval taxalluslari
- Ustun nomlari
- O'zgaruvchilar
- Xato

? MEDALS[i - 1] if i <= 3 else f"{i}." nima qiladi?
+ Birinchi uchtaga medal, qolganlarga raqam qo'yadi
- Hammaga medal beradi
- Faqat birinchiga
- Xato beradi

? Test ishlamagan foydalanuvchi reytingda chiqadimi?
+ Yo'q — JOIN faqat attempts'dagilarni oladi
- Ha, 0 ball bilan
- Ha, oxirida
- Faqat admin ko'radi

? COUNT(a.id) AS testlar nimani hisoblaydi?
+ O'quvchi ishlagan testlar sonini
- Savollar sonini
- Foydalanuvchilar sonini
- Ballni
""",
    "TB14": """
? BaseFilter nima uchun?
+ O'z filtrimizni yozish uchun
- Tugma yaratish uchun
- Bazaga ulanish uchun
- Xabar yuborish uchun

? IsAdmin filtri qachon True qaytaradi?
+ Foydalanuvchi id'si ADMIN_IDS ichida bo'lsa
- Har doim
- Foydalanuvchi /admin yozsa
- Hech qachon

? ADMIN_IDS qayerdan o'qiladi?
+ .env faylidan
- Kod ichidan qattiq yozilgan
- Telegram'dan
- Bazadan

? router.message.filter(IsAdmin()) nima qiladi?
+ Routerdagi hamma xabar handlerlariga filtr qo'yadi
- Bitta handlerga
- Filtrni o'chiradi
- Adminni qo'shadi

? Nega callback_query.filter ham qo'yiladi?
+ Admin tugmalarini oddiy foydalanuvchi bosa olmasligi uchun
- Shart emas
- Tezlik uchun
- Xato chiqmasligi uchun

? ADMIN_IDS nega set (to'plam)?
+ in bilan tez tekshirish va takrorlanmaslik uchun
- Faqat set ishlaydi
- Tartib uchun
- Xato bermasligi uchun

? Oddiy foydalanuvchi /admin yozsa nima bo'ladi?
+ Admin handleri ishlamaydi
- Panel ochiladi
- Bot to'xtaydi
- Xato chiqadi

? __call__ metodi filtrda nimani bildiradi?
+ Filtr obyektini funksiya kabi chaqirish mumkin
- Konstruktor
- Destruktor
- Hech narsa

? "111,222".split(",") natijasi?
+ ["111", "222"]
- [111, 222]
- "111222"
- Xato

? Admin panel tugmalari qanday turdagi?
+ Inline tugmalar (callback_data bilan)
- Reply tugmalar
- Havolalar
- Kontakt tugmasi
""",
    "TB15": """
? AddQuestion holatlari nechta?
+ 4: subject, text, options, correct
- 2
- 3
- 5

? F.text.in_({"math", "english", "it"}) nima qiladi?
+ Faqat shu fan kodlarini qabul qiladi
- Har qanday matnni
- Faqat raqamni
- Hech narsani

? Variantlar qanday kiritiladi?
+ Har biri yangi qatorda, bitta xabarda
- 4 ta alohida xabarda
- Vergul bilan
- Tugma bilan

? message.text.split("\\n") nima qaytaradi?
+ Qatorlar ro'yxatini
- So'zlar ro'yxatini
- Harflar ro'yxatini
- Bitta satr

? 3 ta variant kiritilsa nima bo'ladi?
+ “Aynan 4 ta variant kerak” deb, holat o'zgarmaydi
- Qabul qilinadi
- Bot to'xtaydi
- Keyingi bosqichga o'tadi

? F.text.lower().in_({"a","b","c","d"}) nimani ta'minlaydi?
+ Katta va kichik harf ikkalasi qabul qilinadi
- Faqat katta harf
- Faqat kichik harf
- Hech narsa

? *data["options"] nima qiladi?
+ 4 ta variantni alohida argument qilib uzatadi
- Ro'yxatni o'chiradi
- Ikki marta ko'paytiradi
- Xato beradi

? Savol saqlangach state bilan nima qilinadi?
+ state.clear()
- Hech narsa
- set_state(AddQuestion.subject)
- Bazaga yoziladi

? Savol qaysi funksiya bilan bazaga yoziladi?
+ add_question()
- add_user()
- save_attempt()
- get_questions()

? Nega to'g'ri javob harf bilan saqlanadi?
+ Test tugmalari harf yuboradi — solishtirish oson
- Joy tejaladi
- Telegram talab qiladi
- Farqi yo'q
""",
    "TB16": """
? LIMIT 5 OFFSET 10 nimani qaytaradi?
+ 11–15-qatorlarni
- 1–5-qatorlarni
- 10 ta qatorni
- 5–10-qatorlarni

? 23 ta savol, sahifada 5 ta. Nechta sahifa?
+ 5
- 4
- 4.6
- 23

? -(-total // PAGE) nima qiladi?
+ Yuqoriga yaxlitlab bo'ladi
- Pastga yaxlitlaydi
- Manfiy son qaytaradi
- Xato

? callback_data "qdel:18:2" da 2 nima?
+ O'chirgandan keyin qaytiladigan sahifa raqami
- Savol id'si
- Savollar soni
- Fan

? edit=True bo'lsa nima bo'ladi?
+ Yangi xabar emas, eski xabar yangilanadi
- Yangi xabar yuboriladi
- Xabar o'chadi
- Hech narsa

? ◀ tugmasi qachon chiqmaydi?
+ Birinchi sahifada
- Oxirgi sahifada
- Har doim chiqadi
- Hech qachon chiqmaydi

? callback.answer("🗑 O'chirildi") nima ko'rsatadi?
+ Qisqa bildirishnoma oynasi
- Yangi xabar
- Hech narsa
- Xato

? DELETE FROM questions WHERE id = ? nima qiladi?
+ Bitta savolni o'chiradi
- Hamma savollarni o'chiradi
- Savolni o'zgartiradi
- Jadvalni o'chiradi

? (total,) = await cursor.fetchone() nima qiladi?
+ Bitta qiymatli qatorni o'zgaruvchiga ochadi
- Xato beradi
- Ro'yxat yaratadi
- Hamma qatorlarni oladi

? Sahifalash nima uchun kerak?
+ Ko'p ma'lumotni bitta xabarga sig'dirmasdan qismlab ko'rsatish uchun
- Bazani tezlashtirish uchun
- Savollarni o'chirish uchun
- Shart emas
""",
    "TB17": """
? Broadcast nima?
+ Bitta xabarni hamma foydalanuvchilarga yuborish
- Bitta foydalanuvchiga xabar
- Xabarni o'chirish
- Botni to'xtatish

? Handler'ga bot obyekti qanday keladi?
+ Parametr sifatida (bot: Bot) — aiogram o'zi uzatadi
- Global o'zgaruvchidan
- Import qilib
- Kelmaydi

? TelegramForbiddenError qachon chiqadi?
+ Foydalanuvchi botni bloklaganda
- Internet yo'q bo'lganda
- Xabar bo'sh bo'lganda
- Hech qachon

? Nega har xabardan keyin asyncio.sleep(0.05)?
+ Telegram yuborish limitidan oshmaslik uchun
- Kodni chiroyli qilish uchun
- Xatoni yashirish uchun
- Shart emas

? Bloklagan foydalanuvchida sikl to'xtaydimi?
+ Yo'q — xato ushlanadi va keyingisiga o'tiladi
- Ha
- Faqat admin uchun
- Bot o'chadi

? sent = failed = 0 nima qiladi?
+ Ikki o'zgaruvchiga 0 beradi
- Ularni solishtiradi
- Xato beradi
- Faqat sent'ga beradi

? all_user_ids() nima qaytaradi?
+ Barcha foydalanuvchilar id'lari ro'yxatini
- Faqat adminlarni
- Foydalanuvchilar sonini
- Ismlarni

? Broadcast oxirida admin nimani ko'radi?
+ Nechta yuborildi va nechta bloklagan
- Hech narsa
- Faqat “Tayyor”
- Xatolar ro'yxati

? Broadcast matni qayerdan olinadi?
+ Broadcast.text holatida admin yozgan xabardan
- Bazadan
- .env dan
- Tugmadan

? bot.send_message(user_id, text) nima qiladi?
+ Ko'rsatilgan foydalanuvchiga xabar yuboradi
- Hammaga yuboradi
- Xabarni o'chiradi
- Xabarni tahrirlaydi
""",
    "TB18": """
? Middleware nima?
+ Handler'dan oldin har xabar uchun ishlaydigan qatlam
- Tugma turi
- Baza jadvali
- Holat

? await handler(event, data) middleware'da nima qiladi?
+ Xabarni keyingi qatlamga — handler'ga uzatadi
- Xabarni o'chiradi
- Botni to'xtatadi
- Hech narsa

? Middleware None qaytarib, handler'ni chaqirmasa nima bo'ladi?
+ Xabar e'tiborsiz qoladi
- Xato chiqadi
- Xabar ikki marta ishlanadi
- Bot to'xtaydi

? Throttling nima?
+ Juda tez-tez xabarlarni cheklash (spamdan himoya)
- Xabarni shifrlash
- Botni tezlashtirish
- Log yozish

? time.monotonic() nega time.time() o'rnida?
+ Soat o'zgarsa ham to'g'ri o'lchaydi
- Tezroq
- Aniqroq sana beradi
- Farqi yo'q

? FileHandler("bot.log") nima qiladi?
+ Loglarni faylga ham yozadi
- Faylni o'chiradi
- Faylni o'qiydi
- Hech narsa

? dp.message.middleware(...) qaysi hodisalarga qo'llanadi?
+ Faqat xabarlarga
- Faqat callback'larga
- Hammasiga
- Hech qaysiga

? logger.info("user=%s", uid) da %s nima?
+ Qiymat qo'yiladigan joy
- Xato
- Izoh
- Matn tugashi

? Log nima uchun kerak?
+ Bot nima qilganini keyin ko'rish va xatolarni topish uchun
- Botni tezlashtirish uchun
- Foydalanuvchilarga ko'rsatish uchun
- Shart emas

? self.last lug'atida nima saqlanadi?
+ Har foydalanuvchining oxirgi xabar vaqti
- Xabarlar matni
- Foydalanuvchi ismlari
- Ballar
""",
    "TB19": """
? Mavjud jadvalga yangi ustun qanday qo'shiladi?
+ ALTER TABLE ... ADD COLUMN
- CREATE TABLE qaytadan
- INSERT COLUMN
- DROP TABLE

? PRAGMA table_info(questions) nima beradi?
+ Jadvaldagi ustunlar ro'yxatini
- Qatorlar sonini
- Jadvalni o'chiradi
- Savollarni

? Nega add_column avval ustun borligini tekshiradi?
+ Ikkinchi marta qo'shishda xato bo'lmasligi uchun
- Tezlik uchun
- Ustunni o'chirish uchun
- Shart emas

? file_id nima?
+ Telegram serveridagi faylning identifikatori
- Fayl nomi
- Fayl hajmi
- Diskdagi yo'l

? Rasm tugmalar bilan qanday yuboriladi?
+ answer_photo(file_id, caption=..., reply_markup=...)
- answer(photo=...)
- send_file()
- Rasmga tugma qo'shib bo'lmaydi

? asked_at nima saqlaydi?
+ Savol yuborilgan vaqtni
- Javob vaqtini
- Savol id'sini
- Ballni

? 40 soniyadan keyin to'g'ri javob bosilsa ball beriladimi (LIMIT = 30)?
+ Yo'q — “Vaqt tugadi”
- Ha
- Yarim ball
- Xato chiqadi

? question.get("photo") nega question["photo"] o'rnida?
+ Kalit yo'q bo'lsa ham xato bermasligi uchun
- Tezroq
- Farqi yo'q
- Rasmni yuklash uchun

? Eski ma'lumotlar ALTER TABLE'dan keyin nima bo'ladi?
+ Saqlanib qoladi
- O'chadi
- Ikki baravar ko'payadi
- Xato

? caption nima?
+ Rasm ostidagi matn
- Rasm nomi
- Tugma matni
- Fayl turi
""",
    "TB20": """
? APScheduler nima uchun?
+ Vazifalarni belgilangan vaqtda avtomatik bajarish uchun
- Bazaga ulanish uchun
- Tugmalar uchun
- Log uchun

? Nega AsyncIOScheduler?
+ aiogram bilan bitta asinxron event loop'da ishlaydi
- Yagona mavjud scheduler
- Tezroq
- Farqi yo'q

? add_job(..., "cron", hour=19, minute=0) nimani bildiradi?
+ Har kuni 19:00 da bajarish
- 19 soatdan keyin bir marta
- Har 19 daqiqada
- 19-kuni

? timezone="Asia/Tashkent" nega kerak?
+ Server boshqa vaqt zonasida bo'lsa ham Toshkent vaqti ishlatilsin
- Shart emas
- Tezlik uchun
- Telegram talab qiladi

? UPDATE users SET reminders = 1 - reminders nima qiladi?
+ 1 ni 0 ga, 0 ni 1 ga almashtiradi
- Har doim 1 qiladi
- Har doim 0 qiladi
- Xato beradi

? Eslatma kimlarga yuboriladi?
+ reminders = 1 bo'lgan foydalanuvchilarga
- Hammaga
- Faqat adminlarga
- Hech kimga

? /remind buyrug'i nima qiladi?
+ Eslatmani yoqadi yoki o'chiradi
- Darhol eslatma yuboradi
- Testni boshlaydi
- Botni to'xtatadi

? daily_reminder ichida TelegramForbiddenError ushlansa?
+ Keyingi foydalanuvchiga o'tiladi
- Vazifa to'xtaydi
- Bot to'xtaydi
- Hamma qayta yuboriladi

? scheduler qachon ishga tushiriladi?
+ bot.py'da polling'dan oldin setup_scheduler(bot)
- Har xabarda
- Faqat admin buyrug'ida
- Hech qachon

? requirements.txt ga nima qo'shildi?
+ apscheduler
- django
- requests
- flask
""",
    "TB21": """
? TEXTS lug'ati nima saqlaydi?
+ Har til uchun bir xil kalitli matnlar
- Foydalanuvchilarni
- Savollarni
- Tugmalarni

? t("ru", "menu") nima qaytaradi?
+ “Выберите в меню:”
- “Menyudan tanlang:”
- "menu"
- Xato

? t("xx", "menu") (noma'lum til) nima qaytaradi?
+ O'zbekcha matnni
- Xato
- None
- Bo'sh satr

? Til qayerda saqlanadi?
+ users jadvalidagi lang ustunida
- .env da
- FSM'da
- Telegram'da

? INSERT OR IGNORE INTO users (id) nima uchun?
+ Ro'yxatdan o'tmagan foydalanuvchi uchun ham qator yaratish
- Foydalanuvchini o'chirish
- Takroriy qator yaratish
- Xatoni yashirish

? Til qaysi callback bilan tanlanadi?
+ lang:uz yoki lang:ru
- subject:uz
- adm:lang
- /uz

? Matnlarni kodga emas, lug'atga yozishning foydasi?
+ Yangi til qo'shish faqat lug'atni to'ldirish bilan bo'ladi
- Kod tezlashadi
- Xato bo'lmaydi
- Shart emas

? get_lang() til tanlanmagan bo'lsa nima qaytaradi?
+ "uz"
- None
- "ru"
- Xato

? Til tanlangach javob qaysi tilda chiqadi?
+ Yangi tanlangan tilda
- Har doim o'zbekcha
- Har doim ruscha
- Inglizcha

? /start tilni qayerdan biladi?
+ get_lang(message.from_user.id) orqali bazadan
- Telegram sozlamasidan avtomatik
- FSM'dan
- Bilmaydi
""",
    "TB22": """
? COALESCE(x, 0) nima qiladi?
+ x NULL bo'lsa 0 qaytaradi
- x ni o'chiradi
- 0 ni NULL qiladi
- Xato

? (SELECT COUNT(*) FROM users) so'rov ichida nima?
+ Ichki so'rov — boshqa jadvaldan son oladi
- Xato
- Izoh
- Jadval nomi

? AVG(score * 100.0 / total) nimani hisoblaydi?
+ O'rtacha natija foizini
- Yig'indini
- Testlar sonini
- Eng katta ballni

? Nega CSV faylni io.StringIO'da yig'amiz?
+ Diskka yozmasdan xotirada tayyorlash uchun
- Tezroq yuklash uchun
- Telegram talab qiladi
- Shart emas

? "utf-8-sig" nega kerak?
+ Excel o'zbekcha va ruscha harflarni to'g'ri ochishi uchun
- Fayl kichrayadi
- Shifrlash uchun
- Farqi yo'q

? BufferedInputFile nima?
+ Baytlarni Telegram'ga fayl qilib yuborish obyekti
- Rasm
- Tugma
- Baza ulanishi

? Fayl qaysi metod bilan yuboriladi?
+ answer_document
- answer_photo
- answer
- send_csv

? csv.writer(...).writerows(rows) nima qiladi?
+ Ko'p qatorni CSV'ga yozadi
- Bitta qatorni
- Faylni o'qiydi
- Faylni o'chiradi

? DATE(created_at) = DATE('now') nimani tekshiradi?
+ Bugun ishlangan testlarni
- Hamma testlarni
- Kechagi testlarni
- Hech narsani

? f"{71.43:.0f}%" natijasi?
+ "71%"
- "71.43%"
- "71.4%"
- "72%"
""",
    "TB23": """
? @router.errors() nima qiladi?
+ Handlerlardagi kutilmagan xatolarni ushlaydi
- Xatolarni yaratadi
- Botni to'xtatadi
- Hech narsa

? logger.exception nima yozadi?
+ Xato xabari va to'liq traceback
- Faqat “xato”
- Hech narsa
- Foydalanuvchi ismi

? Error handler True qaytarsa nima bo'ladi?
+ Xato hal qilindi deb hisoblanadi, bot ishlashda davom etadi
- Bot to'xtaydi
- Xato takrorlanadi
- Hech narsa

? Sof funksiya nima?
+ Natijasi faqat argumentlarga bog'liq, tashqi holatni o'zgartirmaydi
- Bazaga yozadigan funksiya
- Xabar yuboradigan funksiya
- Bo'sh funksiya

? percent(0, 0) nima qaytaradi?
+ 0
- Xato
- 100
- None

? grade(8, 10) nima qaytaradi?
+ 4
- 5
- 3
- 80

? pytest test funksiyalarini qanday topadi?
+ test_ bilan boshlangan funksiyalar va fayllar orqali
- Hammasini
- main() orqali
- Topmaydi

? assert percent(8, 10) == 80 noto'g'ri bo'lsa?
+ Test yiqiladi (AssertionError)
- Hech narsa
- Bot to'xtaydi
- Ogohlantirish

? Testlar qanday ishga tushiriladi?
+ Loyiha papkasida: pytest
- python test.py har doim
- Telegram orqali
- Avtomatik

? Nega mantiqni handler'dan sof funksiyaga ajratamiz?
+ Telegram'siz test qilish oson bo'lishi uchun
- Kod uzunroq bo'lishi uchun
- Telegram talab qiladi
- Shart emas
""",
    "TB24": """
? Routerlar tartibida nega errors birinchi?
+ Xatolarni ushlash hamma uchun umumiy
- Alifbo tartibi
- Tasodifiy
- Shart emas

? Admin router nega oddiy routerlardan oldin?
+ Admin buyruqlari boshqa umumiy handlerlarga tushib qolmasligi uchun
- Tezlik uchun
- Telegram talab qiladi
- Farqi yo'q

? Demo oldidan nimani ishga tushiramiz?
+ pytest — testlar o'tishi kerak
- Faqat bot
- Hech narsa
- Bazani o'chiramiz

? 7-oyda qaysi papkalar qo'shildi?
+ filters/, middlewares/, tests/
- static/, templates/
- css/, js/
- api/, web/

? Bot middleware'lari nimalar?
+ LoggingMiddleware va ThrottlingMiddleware
- AdminMiddleware
- QuizMiddleware
- Yo'q

? Eslatma qaysi modulda?
+ scheduler.py
- texts.py
- utils.py
- config.py

? Ikki tillilik qaysi faylga asoslanadi?
+ texts.py
- states.py
- database.py
- filters/admin.py

? Admin funksiyalariga nimalar kiradi?
+ Savol qo'shish, savollarni boshqarish, xabar yuborish, statistika
- Faqat statistika
- Faqat savol qo'shish
- Test ishlash

? 8-oyda nima o'rganiladi?
+ Botni serverga joylash (Linux, systemd, Docker)
- Django
- HTML
- Scratch

? Demo kim ko'zi bilan ko'rsatiladi?
+ Oddiy foydalanuvchi va admin
- Faqat admin
- Faqat foydalanuvchi
- Hech kim
""",
}
