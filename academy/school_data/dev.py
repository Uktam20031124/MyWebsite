"""Minar Dasturchi — 3–11-oylar (Starter'dan keyin): Python, Telegram bot (QuizBot), 2 ta sayt (Portfolio, EduCenter).

9 oy × 12 dars = 108 dars, haftada 3 marta, 60 daqiqadan. Har oy — bitta loyiha ustida: kod darsdan darsga
o'sib boradi. Git 5-oyda o'rgatiladi va keyin har darsda ishlatiladi; bot 8-oyda, saytlar 9- va 11-oyda
serverga joylanadi. Kalitlar: DP — Python, TB — Telegram bot, WB — veb-saytlar.

Har bir darsning to'liq "Dars kodi" (reja, kod qadamlari, rasmlar) — ``lessons_dev.py``.
"""

from . import ModuleData as M
from . import TopicData as T

PLAN = (
    "Dars rejasi (60 daq.):\n"
    "1. Takrorlash: oldingi dars kodi — 5 daq.\n"
    "2. Yangi mavzu: tushuncha va misol — 15 daq.\n"
    "3. Birga kod yozamiz (Dars kodi rasmlari bo'yicha) — 25 daq.\n"
    "4. Mustaqil topshiriq va sinov — 10 daq.\n"
    "5. Test — 5 daq."
)


def topic(key: str, title: str, today: str, homework: str) -> T:
    return T(key, title, f"Maqsad: {title}.\n\nBugun yozamiz: {today}\n\n{PLAN}", homework, minutes=60)


MONTH3 = M(
    "Dasturchi 3-oy · Python asoslari",
    "O'zgaruvchi, shart va sikl bilan konsol dasturlari. Oy loyihasi — “Bank terminali”.",
    [
        topic("DP01", "Python va VS Code: birinchi dastur (print)", "hello.py — o'zi haqida 5 qator chiqaradigan “vizitka”.", "Vizitkaga sevimli fan va orzu kasbni qo'shing; sep va end bilan bezang."),
        topic("DP02", "O'zgaruvchilar va ma'lumot turlari", "profile.py — ism, yosh, bo'y; type() bilan tekshirish.", "Do'stingiz uchun profile2.py yozing: 5 ta o'zgaruvchi va ularning turlari."),
        topic("DP03", "input() va turlarni o'zgartirish", "age.py — tug'ilgan yildan yoshni hisoblash.", "Yil va oy bo'yicha yoshni oylarda hisoblaydigan dastur yozing."),
        topic("DP04", "Arifmetik amallar: kalkulyator", "calc.py v1 — ikki son va 4 amal.", "Kalkulyatorga // , % va ** amallarini qo'shing."),
        topic("DP05", "Satrlar, metodlar va f-string", "name_tool.py — ismni chiroyli formatlash, uzunlik, bosh harflar.", "Familiya va ismdan “Ali V.” ko'rinishidagi qisqa ism yasang."),
        topic("DP06", "Taqqoslash va mantiqiy amallar", "login.py — login va parolni tekshirish.", "Parol uzunligi 8+ va ichida raqam borligini tekshiring."),
        topic("DP07", "Shartlar: if, elif, else", "grade.py — balldan bahoni chiqarish.", "Haroratga qarab kiyim maslahatini beradigan dastur yozing."),
        topic("DP08", "Ichma-ich shart va match-case: menyuli kalkulyator", "calc.py v2 — menyuli kalkulyator.", "Menyuga “0 — chiqish” va nolga bo'lish tekshiruvini qo'shing."),
        topic("DP09", "while sikli va random: “Sonni top” o'yini", "guess.py v1 — kompyuter o'ylagan sonni topish.", "O'yinga “katta / kichik” maslahatini qo'shing."),
        topic("DP10", "for sikli va range()", "table.py — ko'paytirish jadvali va yig'indi.", "1 dan N gacha juft sonlar yig'indisini chiqaring."),
        topic("DP11", "break, continue va sikl amaliyoti", "guess.py v2 — urinishlar soni, qayta o'ynash.", "Eng yaxshi natijani (eng kam urinish) eslab qoling."),
        topic("DP12", "3-oy loyihasi: “Bank terminali” va nazorat", "bank.py — balans, kirim, chiqim, tarix.", "Terminalga PIN-kod bilan kirishni qo'shing (3 urinish)."),
    ],
)

MONTH4 = M(
    "Dasturchi 4-oy · Python: tuzilmalar va funksiyalar",
    "list, tuple, set, dict va funksiyalar. Oy loyihasi — konsoldagi “Kundalik”.",
    [
        topic("DP13", "List: yaratish, indeks va kesish", "class_list.py — sinf ro'yxati bilan ishlash.", "Ro'yxatdan har ikkinchi o'quvchini va oxirgi 3 tasini chiqaring."),
        topic("DP14", "List metodlari: vazifalar ro'yxati", "todo.py v1 — vazifa qo'shish, o'chirish, ko'rsatish.", "Vazifani raqami bo'yicha o'chirishni qo'shing."),
        topic("DP15", "for bilan list: baholar statistikasi", "stats.py — yig'indi, eng kattasi, o'rtacha.", "5 dan past baholar sonini va foizini chiqaring."),
        topic("DP16", "Tuple va set", "subjects.py — takrorlarni olib tashlash, umumiy fanlar.", "Ikki do'stning umumiy va farqli sevimli fanlarini toping."),
        topic("DP17", "Dictionary: telefon kitobchasi", "phonebook.py v1 — ism → telefon.", "Har kontaktga email ham qo'shing (lug'at ichida lug'at)."),
        topic("DP18", "Dict metodlari va aylanish", "phonebook.py v2 — qidirish, tahrirlash, o'chirish.", "Ismning bir qismi bo'yicha qidirishni qo'shing."),
        topic("DP19", "Ichma-ich ma'lumot: o'quvchilar reytingi", "rating.py — o'quvchilar list[dict] va reyting.", "Har o'quvchiga 3 ta baho bering va o'rtachasi bo'yicha reyting tuzing."),
        topic("DP20", "Funksiyalar: def, parametr, return", "calc.py v3 — kalkulyator funksiyalarga bo'lingan.", "is_even(n) va max_of_three(a, b, c) funksiyalarini yozing."),
        topic("DP21", "Default qiymatlar, *args va scope", "todo.py v2 — funksiyalar bilan.", "add_tasks(*tasks) — bir nechta vazifani birdan qo'shadigan funksiya."),
        topic("DP22", "lambda, sorted, map va filter", "rating.py v2 — turli mezon bo'yicha saralash.", "O'quvchilarni ism uzunligi bo'yicha saralang."),
        topic("DP23", "List comprehension va matn tahlili", "text_stats.py — so'zlar soni, eng ko'p takrorlangan so'z.", "Matndagi unli harflar sonini comprehension bilan toping."),
        topic("DP24", "4-oy loyihasi: “Kundalik” va nazorat", "diary.py — menyuli “Kundalik”: qo'shish, bajarildi, o'chirish.", "Vazifaga muhimlik darajasini qo'shing va shu bo'yicha saralang."),
    ],
)

MONTH5 = M(
    "Dasturchi 5-oy · Python: fayl, xato, OOP va Git",
    "Modullar, xatolar, fayl va JSON, OOP, API; Git va GitHub. Oy loyihasi — GitHub'dagi “Kundalik”.",
    [
        topic("DP25", "Modullar: random va datetime", "tips.py — kunning maslahati va bugungi sana.", "Tug'ilgan kungacha necha kun qolganini hisoblang."),
        topic("DP26", "Xatolar bilan ishlash: try / except", "utils.py — xavfsiz input_int() funksiyasi.", "input_float() va oraliq tekshiruvchi input_range() yozing."),
        topic("DP27", "Txt fayllar: o'qish va yozish", "diary.py v2 — vazifalarni faylga saqlash.", "Dastur ochilganda vazifalar fayldan yuklansin."),
        topic("DP28", "JSON bilan ishlash", "diary.py v3 — tasks.json bilan.", "Har vazifaga yaratilgan sana qo'shing."),
        topic("DP29", "OOP: class, __init__ va metodlar", "models.py — Task klassi.", "Task'ga mark_done() va __str__ metodlarini qo'shing."),
        topic("DP30", "OOP: vorislik", "users.py — User va Admin.", "Admin'ga delete_user() metodini qo'shing."),
        topic("DP31", "OOP: property va maxsus metodlar", "diary.py v4 — TaskManager klassi.", "TaskManager'ga __len__ va search() qo'shing."),
        topic("DP32", "venv, pip va API: valyuta kursi", "currency.py — cbu.uz'dan valyuta kursini olish.", "So'mni dollar va yevroga o'tkazuvchi konvertor yozing."),
        topic("DP33", "Git: init, add, commit, log", "“Kundalik” loyihasi Git'da, 5 ta commit.", "Har bir o'zgarishni alohida commit qiling (kamida 3 ta)."),
        topic("DP34", "GitHub: repozitoriy, push, README, .gitignore", "Loyiha GitHub'da, README bilan.", "README'ga skrinshot va ishga tushirish yo'riqnomasini qo'shing."),
        topic("DP35", "Branch va Pull Request", "Juftlikda: do'stning repozitoriysiga Pull Request.", "Do'stingizning PR'iga sharh yozing va merge qiling."),
        topic("DP36", "Python yakuniy nazorat va loyiha himoyasi", "“Kundalik” himoyasi (GitHub havolasi bilan).", "Himoyadagi izohlar bo'yicha loyihani yaxshilang."),
    ],
)

MONTH6 = M(
    "Dasturchi 6-oy · Telegram bot (QuizBot) 1-qism",
    "aiogram 3: menyu, tugmalar, ro'yxatdan o'tish, SQLite va test rejimi. Oy loyihasi — QuizBot.",
    [
        topic("TB01", "Bot qanday ishlaydi: BotFather, token, async", "bot.py — aytganini qaytaradigan (echo) bot.", "Botga matn uzunligini aytadigan javob qo'shing."),
        topic("TB02", "aiogram 3: Dispatcher, Router, handler", "/start va /help buyruqlari, ism bilan salomlashish.", "/about buyrug'ini qo'shing."),
        topic("TB03", "Bot loyihasi tuzilmasi: config, handlers, keyboards", "config.py, handlers/, keyboards/ papkalariga ajratish.", "Har bir buyruqni alohida faylga ajrating."),
        topic("TB04", "Reply tugmalar: asosiy menyu", "Asosiy menyu: Test · Reyting · Profil · Yordam.", "“Yordam” tugmasiga batafsil yo'riqnoma yozing."),
        topic("TB05", "Inline tugmalar va callback", "Fan tanlash tugmalari (Matematika, Ingliz tili, Informatika).", "To'rtinchi fan qo'shing va tugmalarni 2 ustunga joylang."),
        topic("TB06", "FSM: ro'yxatdan o'tish", "Ro'yxatdan o'tish: ism → telefon (kontakt tugmasi) → sinf.", "Ism kamida 2 harf ekanini tekshiring."),
        topic("TB07", "SQL asoslari: CREATE, INSERT, SELECT", "database.py — users jadvali.", "users jadvaliga created_at ustunini qo'shing."),
        topic("TB08", "aiosqlite: botni bazaga ulash", "Ro'yxatdan o'tganlarni saqlash, “Profil” tugmasi.", "Profilda ro'yxatdan o'tgan sanani ko'rsating."),
        topic("TB09", "Savollar jadvali va seed", "questions jadvali, seed.py bilan 30 ta savol.", "O'z faningizdan 10 ta savol qo'shing."),
        topic("TB10", "Test rejimi, 1-qism: savol va javob tugmalari", "Fan tugmasi → bazadan 10 ta savol → javob tugmalari → tekshirish.", "Test boshida “Tayyormisiz?” xabari va [Boshlash] tugmasini qo'shing."),
        topic("TB11", "Test rejimi, 2-qism: natija va attempts jadvali", "Ballni attempts jadvaliga saqlash, “Mening natijalarim”.", "Natijaga foiz va baho (5/4/3) qo'shing."),
        topic("TB12", "6-oy nazorati: QuizBot demosi", "Bot demosi va GitHub'da kod tahlili.", "Tahlildagi izohlar bo'yicha kodni tuzating."),
    ],
)

MONTH7 = M(
    "Dasturchi 7-oy · Telegram bot 2-qism: imkoniyatlar",
    "Reyting, admin panel, broadcast, middleware, eslatmalar, ikki til va testlar.",
    [
        topic("TB13", "SQL: ORDER BY, LIMIT, JOIN — reyting", "“Reyting” — top-10 o'quvchi.", "Reytingda foydalanuvchining o'z o'rnini ham ko'rsating."),
        topic("TB14", "Filtrlar va admin huquqi", "/admin paneli, faqat admin ID uchun.", "Bir nechta admin ID'ni .env'dan o'qing."),
        topic("TB15", "Admin: FSM bilan savol qo'shish", "Yangi savol va 4 ta variant kiritish.", "Savol qo'shishdan oldin tasdiqlash tugmasini qo'shing."),
        topic("TB16", "Admin: savollarni boshqarish va sahifalash", "Inline sahifalash, savolni tahrirlash va o'chirish.", "Savollarni fan bo'yicha filtrlash tugmasini qo'shing."),
        topic("TB17", "Hammaga xabar (broadcast)", "Xabar yuborish, botni bloklaganlarni ushlash.", "Broadcast oxirida “yuborildi / xato” statistikasini chiqaring."),
        topic("TB18", "Middleware va logging", "Har so'rovni log qilish, spamdan himoya (throttling).", "Faylga log yozishni qo'shing."),
        topic("TB19", "Media va vaqt chegarasi", "Rasmli savollar, har savolga 30 soniya.", "Vaqt tugaganda savolni avtomatik o'tkazib yuboring."),
        topic("TB20", "Rejalashtirilgan vazifalar: APScheduler", "Har kuni 19:00 da “Bugungi test” eslatmasi.", "Foydalanuvchi eslatmani o'chira oladigan sozlama qo'shing."),
        topic("TB21", "Ikki tilli bot: o'zbek va rus", "Til tanlash, matnlar lug'ati (texts.py).", "Profilda tilni almashtirish tugmasini qo'shing."),
        topic("TB22", "Admin statistikasi va CSV hisobot", "Kunlik hisobot va natijalarni CSV fayl qilib yuborish.", "Hisobotga eng faol 3 foydalanuvchini qo'shing."),
        topic("TB23", "Xatolarni ushlash va pytest", "Umumiy error handler, pytest bilan funksiyalar testi.", "Ball hisoblash funksiyasiga 3 ta test yozing."),
        topic("TB24", "7-oy nazorati: bot demosi", "Bot demosi va kod tahlili.", "Tahlildagi izohlar bo'yicha kodni tuzating."),
    ],
)

MONTH8 = M(
    "Dasturchi 8-oy · Telegram bot 3-qism: server",
    "Linux, VPS, systemd, deploy, zaxira, monitoring, Docker va bot himoyasi.",
    [
        topic("TB25", "Linux asoslari va SSH", "Serverga kirish, papka va fayllar, nano.", "Serverda o'z papkangizni yarating va README yozing."),
        topic("TB26", "VPS sozlash: foydalanuvchi, firewall, Python", "Yangi foydalanuvchi, ufw, Python o'rnatish.", "SSH kalit bilan parolsiz kirishni sozlang."),
        topic("TB27", "Botni serverga joylash", "git clone, venv, .env, qo'lda ishga tushirish.", "Bot ishlayotganini skrinshot bilan ko'rsating."),
        topic("TB28", "systemd xizmati: bot 24/7", "quizbot.service va journalctl bilan loglar.", "Xizmat to'xtasa avtomatik qayta ishga tushishini tekshiring."),
        topic("TB29", "Yangilash jarayoni: deploy.sh", "deploy.sh: git pull + restart.", "deploy.sh'ga pip install -r requirements.txt qo'shing."),
        topic("TB30", "Zaxira: cron bilan bazani saqlash", "Har kuni bazani zaxiralash.", "7 kundan eski zaxiralarni o'chiradigan qator qo'shing."),
        topic("TB31", "Monitoring: xatolar admin'ga", "Xato bo'lsa admin'ga Telegram'da xabar.", "Kunlik “bot ishlayapti” hisobotini qo'shing."),
        topic("TB32", "Docker asoslari", "Dockerfile va docker compose bilan botni ishga tushirish.", "docker compose'ga restart: always qo'shing."),
        topic("TB33", "Kod sifati: refaktoring, type hint, ruff", "Kodni tozalash va ruff tekshiruvi.", "ruff topgan barcha ogohlantirishlarni tuzating."),
        topic("TB34", "GitHub'da loyiha: README va requirements", "README, skrinshotlar, requirements.txt.", "README'ga “Qanday ishga tushirish” bo'limini yozing."),
        topic("TB35", "Bot himoyasiga tayyorgarlik", "Demo ssenariysi va savollarga javoblar.", "3 daqiqalik demo ssenariysini yozing."),
        topic("TB36", "QuizBot himoyasi: demo kun", "Har o'quvchi o'z botini ko'rsatadi.", "Himoyadagi izohlar bo'yicha botni yaxshilang."),
    ],
)

MONTH9 = M(
    "Dasturchi 9-oy · 1-sayt: Portfolio (HTML, CSS, JS)",
    "HTML, CSS (Flexbox, Grid, media query) va JavaScript. Oy loyihasi — GitHub Pages'dagi shaxsiy sayt.",
    [
        topic("WB01", "Veb qanday ishlaydi va HTML skelet", "index.html — sahifa skeleti.", "Sahifaga title va o'zingiz haqingizda 1 abzats qo'shing."),
        topic("WB02", "HTML teglar: matn, rasm, havola, ro'yxat", "“Men haqimda”: sarlavha, matn, rasm, havolalar, ro'yxat.", "Sevimli 5 ta kitob/film ro'yxatini qo'shing."),
        topic("WB03", "Semantik HTML va forma", "header, main, section, footer va aloqa formasi.", "Formaga “Mavzu” tanlash maydonini (select) qo'shing."),
        topic("WB04", "CSS asoslari va box model", "style.css — ranglar, shriftlar, oraliqlar.", "Sahifaga o'z rang palitrangizni bering (3 rang)."),
        topic("WB05", "Flexbox: navigatsiya va hero", "Navigatsiya paneli va bosh blok (hero).", "Hero'ga ikkita tugma qo'shing va yonma-yon joylang."),
        topic("WB06", "Grid: loyihalar kartalari", "Loyihalar kartalari to'ri.", "Kartaga rasm va “Ko'rish” havolasini qo'shing."),
        topic("WB07", "Responsive dizayn: media query", "Media query, telefon uchun menyu.", "Planshet (768 px) uchun alohida ko'rinish qo'shing."),
        topic("WB08", "CSS o'zgaruvchilari va animatsiya", "Rang tokenlari, hover effektlar, tungi rejim ranglari.", "Kartalarga yumshoq paydo bo'lish animatsiyasini qo'shing."),
        topic("WB09", "JavaScript asoslari va DOM", "script.js — elementni topish va o'zgartirish.", "Sahifada bugungi sanani JS bilan chiqaring."),
        topic("WB10", "JS hodisalar: tungi rejim, menyu, forma", "Tungi rejim tugmasi, mobil menyu, forma tekshiruvi.", "Forma yuborilganda “Rahmat!” xabarini ko'rsating."),
        topic("WB11", "JS massivlar va localStorage", "Loyihalar kartalarini JS ma'lumotidan chiqarish, rejimni eslab qolish.", "Loyihalarni texnologiya bo'yicha filtrlash tugmalarini qo'shing."),
        topic("WB12", "GitHub Pages'ga joylash va himoya", "Sayt username.github.io manzilida.", "Saytga favicon va meta description qo'shing."),
    ],
)

MONTH10 = M(
    "Dasturchi 10-oy · 2-sayt: EduCenter (Django) 1-qism",
    "Django: modellar, admin, sahifalar, shablonlar, formalar va login. Oy loyihasi — o'quv markazi sayti.",
    [
        topic("WB13", "Django nima: MVT va birinchi loyiha", "venv, startproject, runserver — birinchi ishga tushirish.", "Loyiha sozlamalarida tilni uz va vaqt zonasini Asia/Tashkent qiling."),
        topic("WB14", "App, URL, view va shablon", "courses app, base.html, Portfolio CSS'ini qayta ishlatish.", "“Biz haqimizda” sahifasini qo'shing."),
        topic("WB15", "Modellar va migratsiya", "Course modeli, makemigrations, migrate.", "Course'ga price va duration_months maydonlarini qo'shing."),
        topic("WB16", "Django admin", "superuser, list_display, kurslarni admin orqali qo'shish.", "Admin'da kurslarni narx bo'yicha filtrlash qo'shing."),
        topic("WB17", "ORM va QuerySet: kurslar ro'yxati", "“Kurslar” sahifasi — bazadan ro'yxat.", "Faqat faol kurslarni narx bo'yicha saralab chiqaring."),
        topic("WB18", "Detal sahifa: slug va get_object_or_404", "Kurs sahifasi.", "Kurs sahifasiga “Boshqa kurslar” blokini qo'shing."),
        topic("WB19", "Bog'lanishlar: ForeignKey va ManyToMany", "Category va Teacher modellari.", "Ustoz sahifasida u dars beradigan kurslarni chiqaring."),
        topic("WB20", "Rasm yuklash: ImageField va media", "Kurs va ustoz rasmlari.", "Rasm bo'lmasa standart rasm ko'rsating."),
        topic("WB21", "Formalar: kursga yozilish", "Enrollment va “Kursga yozilish” formasi, CSRF, messages.", "Telefon raqami +998 bilan boshlanishini tekshiring."),
        topic("WB22", "Ro'yxatdan o'tish va login", "UserCreationForm, login, logout.", "Login'dan keyin bosh sahifada “Salom, ism!” chiqsin."),
        topic("WB23", "Shaxsiy kabinet va qidiruv", "login_required, “Mening arizalarim”, kurs qidirish.", "Qidiruvga kategoriya bo'yicha filtr qo'shing."),
        topic("WB24", "10-oy nazorati: EduCenter demosi", "Sayt demosi va kod tahlili.", "Tahlildagi izohlar bo'yicha kodni tuzating."),
    ],
)

MONTH11 = M(
    "Dasturchi 11-oy · Django 2-qism, server va himoya",
    "Yangiliklar, testlar, serverga joylash (gunicorn, nginx, HTTPS), API, bot bilan integratsiya va yakuniy himoya.",
    [
        topic("WB25", "Yangiliklar, sahifalash va class-based views", "Post modeli, ListView, Paginator.", "Yangilik sahifasiga “Oldingi / keyingi” havolalarini qo'shing."),
        topic("WB26", "Testlar va sozlamalar (.env)", "TestCase, .env, DEBUG, ALLOWED_HOSTS, collectstatic.", "Kurs sahifasi uchun 2 ta test yozing."),
        topic("WB27", "Gunicorn va systemd", "Saytni serverda educenter.service sifatida ishga tushirish.", "Xizmat loglarini journalctl bilan ko'rib, skrinshot qiling."),
        topic("WB28", "Nginx, domen va HTTPS", "static fayllar, proxy, certbot.", "Saytni telefoningizdan HTTPS bilan oching."),
        topic("WB29", "API: JSON qaytarish", "/api/courses/ — JsonResponse.", "API'ga ?category= filtri qo'shing."),
        topic("WB30", "Integratsiya: sayt → bot", "Yangi ariza tushsa, admin'ga Telegram xabar.", "Xabarga kurs narxi va ariza vaqtini qo'shing."),
        topic("WB31", "Integratsiya: bot → sayt", "QuizBot'da /kurslar — saytdagi kurslar ro'yxati.", "Har kurs ostiga “Saytda ochish” tugmasini qo'shing."),
        topic("WB32", "Yakuniy loyiha: g'oya va reja", "Har o'quvchi o'z loyihasini tanlaydi va rejasini yozadi.", "Loyiha rejasini README'ga yozing."),
        topic("WB33", "Yakuniy loyiha: ishlash kuni", "Asosiy funksiyalar.", "Asosiy funksiyalardan birini tugating."),
        topic("WB34", "Yakuniy loyiha: kod tahlili va joylash", "Tuzatishlar va serverga joylash.", "Loyihani serverga joylab, havolasini yuboring."),
        topic("WB35", "Taqdimotga tayyorgarlik: portfolio va rezyume", "Portfolio'ni yangilash, README, rezyume.", "Portfolio saytingizga bot va EduCenter havolalarini qo'shing."),
        topic("WB36", "DEMO DAY: himoya va sertifikat", "Yakuniy loyiha himoyasi.", "Tabriklaymiz! Loyihangizni rivojlantirishda davom eting."),
    ],
)

MODULES = [MONTH3, MONTH4, MONTH5, MONTH6, MONTH7, MONTH8, MONTH9, MONTH10, MONTH11]
TRACK = [t.key for m in MODULES for t in m.topics]
