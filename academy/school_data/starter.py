"""Starter kursi: kompyuter savodxonligi, dizayn va dasturlashga kirish.

Har bir mavzu — bitta dars (90 daq.). Tavsifda: maqsad, dars rejasi, darsdagi
amaliyot va baholash mezoni (jami 100 ball — yo'qlamadagi "Ball" ustuniga).
"""

from . import ModuleData as M
from . import TopicData as T

GOOGLE = M(
    "Starter 1 · Kompyuter savodxonligi va Google",
    "Klaviatura, elektron pochta va Google ofis dasturlari: hujjat, jadval, taqdimot, bulut.",
    [
        T(
            "ST01",
            "Monkeytype — klaviaturada tez yozish",
            """Maqsad: 10 barmoqli yozish texnikasini o'rganish, tezlik (WPM) va aniqlikni o'lchash.

Dars rejasi:
1. Barmoqlarning "uy qatori" (A S D F — J K L ;) va to'g'ri o'tirish holati — 15 daq.
2. Monkeytype interfeysi: rejimlar (time / words), WPM va accuracy nima — 10 daq.
3. Mashq: 15 s → 30 s → 60 s testlar, natijani daftarga yozish — 40 daq.
4. "Klaviatura poygasi": guruhda eng yuqori aniqlik (≥95%) bilan yozgan g'olib — 20 daq.
5. Yakun: shaxsiy maqsad qo'yish (masalan, +5 WPM bir haftada) — 5 daq.

Darsdagi amaliyot:
- Har bir o'quvchi 3 ta 60 soniyalik test topshiradi, eng yaxshi natijani skrinshot qiladi.

Baholash (100 ball):
- To'g'ri qo'l holati va uy qatori — 30
- Aniqlik ≥ 90% — 40
- Natijani qayd etish va shaxsiy maqsad — 30""",
            """1. Har kuni 10 daqiqa Monkeytype (time 60) — 5 kun natijasini jadvalga yozing.
2. Eng yaxshi natija skrinshotini guruhga yuboring.
3. Maqsad: aniqlik 95%+, tezlik +5 WPM.""",
            "https://monkeytype.com\nhttps://www.keybr.com",
        ),
        T(
            "ST02",
            "Gmail — elektron pochta bilan ishlash",
            """Maqsad: Gmail bilan ishonchli ishlash — xat yozish, javob berish,
ilova (attachment) yuborish va xatlarni tartiblash.

Dars rejasi:
1. Gmail interfeysi: Inbox, Sent, Drafts, Spam, Starred — 10 daq.
2. To'g'ri xat yozish: mavzu (Subject), salomlashish, asosiy matn, imzo — 15 daq.
3. To / Cc / Bcc farqi, Reply va Reply all, Forward — 15 daq.
4. Fayl ilova qilish, label (yorliq) va filtr yaratish — 20 daq.
5. Amaliyot va xavfsizlik: shubhali xatni qanday tanish mumkin — 30 daq.

Darsdagi amaliyot:
- Ustozga mavzusi "Uy vazifasi — Ism Familiya" bo'lgan, rasm ilova qilingan rasmiy xat yuborish.
- "O'qish" nomli label yaratib, 3 ta xatni unga o'tkazish.

Baholash (100 ball):
- Xat tuzilmasi (mavzu, salom, imzo) — 40
- Ilova va Cc to'g'ri ishlatilgan — 30
- Label/filtr yaratilgan — 30""",
            """1. Ustozga o'zingiz haqingizda 5–6 gapdan iborat rasmiy xat yozing (imzo bilan).
2. Xatga sevimli rasmingizni ilova qiling.
3. Gmail'da "Maktab" label'ini yarating va kamida 3 ta xatni joylang.""",
            "https://support.google.com/mail",
        ),
        T(
            "ST03",
            "Google Docs — hujjatlar bilan ishlash",
            """Maqsad: Google Docs'da formatlangan hujjat yaratish va boshqalar bilan ulashish.

Dars rejasi:
1. Yangi hujjat, nomlash, avtomatik saqlanish — 10 daq.
2. Formatlash: sarlavhalar (Heading 1/2), shrift, ro'yxatlar, hizalash — 20 daq.
3. Jadval, rasm va havola qo'shish — 20 daq.
4. Ulashish (Share): Viewer / Commenter / Editor; izoh va taklif rejimi — 15 daq.
5. Amaliyot: "Mening sevimli kasbim" referati — 25 daq.

Darsdagi amaliyot:
- Kamida 2 sarlavha, 1 jadval, 1 rasm va 1 havolali 1 sahifalik hujjat.
- Hujjatni ustozga "Commenter" huquqi bilan ulashish.

Baholash (100 ball):
- Tuzilma va sarlavhalar — 30
- Jadval, rasm, havola — 40
- To'g'ri ulashish — 30""",
            """1. "Mening sevimli kasbim" hujjatini yakunlang: kirish, 3 bo'lim, xulosa.
2. Mundarija (Table of contents) qo'shing.
3. Hujjatni ustozga "Commenter" huquqi bilan ulashing.""",
            "https://support.google.com/docs",
        ),
        T(
            "ST04",
            "Google Slides — prezentatsiya yaratish",
            """Maqsad: aniq va chiroyli prezentatsiya tayyorlash va uni taqdim etish.

Dars rejasi:
1. Slayd turlari (layout), mavzu (theme), ranglar — 10 daq.
2. Yaxshi slayd qoidalari: 1 slayd — 1 fikr, kam matn, katta shrift — 15 daq.
3. Rasm, shakl, ikonka va animatsiya/o'tish effektlari (me'yorida) — 20 daq.
4. Speaker notes va taqdimot rejimi — 10 daq.
5. Amaliyot va 1 daqiqalik taqdimot — 35 daq.

Darsdagi amaliyot:
- "Mening shahrim" mavzusida 5 slayd: titul, 3 ta asosiy, yakun.

Baholash (100 ball):
- Dizayn va o'qilishi — 40
- Mazmun (5 slayd, mantiqiy ketma-ketlik) — 30
- Taqdimot qilish (1 daqiqa) — 30""",
            """1. "Mening sevimli o'yinim/filmim" mavzusida 6 slaydli prezentatsiya.
2. Har slaydda ko'pi bilan 3 qator matn va kamida 1 rasm.
3. Havolani ustozga Gmail orqali yuboring.""",
            "https://support.google.com/docs",
        ),
        T(
            "ST05",
            "Google Drive — asoslar va hamkorlik",
            """Maqsad: fayllarni bulutda saqlash, tartiblash va jamoa bo'lib birga ishlash.

Dars rejasi:
1. Drive nima: bulutli xotira, 15 GB, My Drive va Shared with me — 10 daq.
2. Fayl/papka yuklash, papka yaratish, rang berish, qidiruv — 20 daq.
3. Ulashish: havola orqali va email orqali, huquqlar (Viewer/Commenter/Editor) — 20 daq.
4. Birgalikda tahrirlash: bitta Docs/Slides faylida 3–4 o'quvchi bir vaqtda — 25 daq.
5. Versiyalar tarixi (Version history) va fayl tiklash — 15 daq.

Darsdagi amaliyot:
- "Starter_Ism" papkasi va ichida Docs, Slides, Rasmlar kichik papkalari.
- Jamoa bilan bitta umumiy Slides — har bir o'quvchi bitta slayd tayyorlaydi.

Baholash (100 ball):
- Papkalar tuzilmasi — 30
- To'g'ri ulashish va huquqlar — 30
- Jamoaviy faylga hissa — 40""",
            """1. Drive'da o'quv papkangizni tartiblang: barcha uy vazifalari bitta papkada.
2. Papkani ustozga "Viewer" huquqi bilan ulashing.
3. Version history orqali hujjatning avvalgi holatini topib, skrinshot qiling.""",
            "https://support.google.com/drive",
        ),
        T(
            "ST06",
            "Google Sheets — asoslar va formulalar (SUM, AVERAGE, COUNT)",
            """Maqsad: elektron jadvalda ma'lumot kiritish, formatlash va oddiy formulalar bilan hisoblash.

Dars rejasi:
1. Yacheyka, qator, ustun, manzil (A1), varaqlar — 10 daq.
2. Ma'lumot turlari va formatlash: son, sana, foiz, valyuta — 15 daq.
3. Formulalar: =SUM, =AVERAGE, =COUNT, =MAX, =MIN; formulani pastga cho'zish — 25 daq.
4. Saralash va filtr — 15 daq.
5. Amaliyot: "Sinf baholari" jadvali — 25 daq.

Darsdagi amaliyot:
- 10 o'quvchi va 4 fan bo'yicha baholar jadvali; har bir o'quvchi uchun jami va o'rtacha,
  har bir fan uchun eng yuqori va eng past baho.

Baholash (100 ball):
- Jadval tuzilmasi va formatlash — 30
- Formulalar to'g'ri — 50
- Saralash/filtr — 20""",
            """1. "Haftalik xarajatlarim" jadvali: kun, nima, summa. Jami (SUM) va o'rtacha (AVERAGE) hisoblang.
2. Nechta xarid bo'lganini COUNT bilan toping.
3. Eng katta xarajatni MAX bilan toping va rang bilan ajrating.""",
            "https://support.google.com/docs",
        ),
        T(
            "ST07",
            "Google Sheets — diagrammalar va shartli formatlash",
            """Maqsad: ma'lumotni diagramma orqali ko'rsatish va xulosa chiqarish.

Dars rejasi:
1. Diagramma turlari: ustunli (column), chiziqli (line), doiraviy (pie) — qachon qaysi biri — 15 daq.
2. Diagramma yaratish va sozlash: sarlavha, o'qlar, ranglar, legenda — 25 daq.
3. Shartli formatlash (Conditional formatting): 60 dan pastini qizil qilish — 15 daq.
4. =IF bilan oddiy xulosa: "O'tdi" / "Qayta topshiradi" — 15 daq.
5. Amaliyot va natijani Slides'ga joylash — 20 daq.

Darsdagi amaliyot:
- Oldingi darsdagi "Sinf baholari" bo'yicha ustunli va doiraviy diagramma.

Baholash (100 ball):
- To'g'ri diagramma turi va sozlamalar — 40
- Shartli formatlash — 30
- IF bilan xulosa — 30""",
            """1. "Haftalik xarajatlarim" jadvali uchun doiraviy diagramma yarating.
2. 7 kunlik ob-havo (harorat) jadvali va chiziqli diagramma.
3. 20°C dan yuqori kunlarni shartli formatlash bilan yashil qiling.""",
            "https://support.google.com/docs",
        ),
        T(
            "ST08",
            "1-oy yakuniy amaliy dars: Gmail + Drive + Docs + Sheets + Slides",
            """Maqsad: oy davomida o'rganilgan Google vositalarini bitta yaxlit loyihada qo'llash.

Loyiha: "Sinfimiz sayohati" (3–4 kishilik jamoalarda)
1. Drive: jamoa papkasi va ulashish — 10 daq.
2. Docs: sayohat rejasi (manzil, kun tartibi, qoidalar) — 20 daq.
3. Sheets: xarajatlar smetasi (SUM, AVERAGE) va diagramma — 20 daq.
4. Slides: 5–6 slaydli taqdimot (Sheets diagrammasi bilan) — 20 daq.
5. Gmail: tayyor loyiha havolalarini ustozga rasmiy xat bilan yuborish — 5 daq.
6. Jamoalar taqdimoti (har biri 3 daqiqa) — 15 daq.

Baholash (100 ball):
- Har bir vosita to'g'ri ishlatilgan (5 × 12) — 60
- Jamoaviy ish va ulashish — 20
- Taqdimot — 20""",
            """1. Loyihaning o'zingizga tegishli qismini yakunlang.
2. Jamoa ishiga Docs'da izoh (comment) bilan 2 ta taklif yozing.
3. O'z hissangiz haqida 3–4 gaplik qisqa hisobotni Gmail orqali yuboring.""",
            "https://support.google.com/drive\nhttps://support.google.com/docs",
        ),
    ],
)

DESIGN = M(
    "Starter 2 · Grafik dizayn: Canva va Figma",
    "Vizual kompozitsiya, rang va shrift; Canva'da tez dizayn, Figma'da interfeys va prototip.",
    [
        T(
            "ST09",
            "Canva — kirish va vizitka dizayni",
            """Maqsad: Canva interfeysini o'rganish va dizaynning asosiy qoidalari bilan vizitka yaratish.

Dars rejasi:
1. Canva: shablonlar, elementlar, matn, yuklash (Uploads) — 15 daq.
2. Dizayn asoslari: kontrast, tekislash (alignment), bo'sh joy, 2 ta shrift qoidasi — 20 daq.
3. Rang palitrasi tanlash (3 ta rang) — 10 daq.
4. Vizitka yaratish (90×50 mm) — 35 daq.
5. PNG va PDF formatida yuklab olish — 10 daq.

Darsdagi amaliyot:
- O'zingiz yoki xayoliy kompaniya uchun ikki tomonli vizitka.

Baholash (100 ball):
- Tekislash va o'qilishi — 40
- Rang va shrift uyg'unligi — 30
- To'g'ri eksport — 30""",
            """1. Oila a'zolaringizdan biri uchun vizitka yarating (2 xil variant).
2. Qaysi variant yaxshiroq va nima uchun — 2–3 gap bilan izohlang.""",
            "https://www.canva.com/designschool/",
        ),
        T(
            "ST10",
            "Canva — social media post va prezentatsiya dizayni",
            """Maqsad: ijtimoiy tarmoq uchun post/story va Canva'da taqdimot tayyorlash.

Dars rejasi:
1. O'lchamlar: Instagram post 1080×1080, story 1080×1920 — 10 daq.
2. Sarlavha ierarxiyasi va "call to action" (chaqiriq) — 15 daq.
3. Brend to'plami: logo, ranglar, shriftlarni bir xil ishlatish — 15 daq.
4. Canva Presentations: 5 slayd, bir xil uslub — 30 daq.
5. Jamoada ko'rib chiqish va fikr bildirish — 20 daq.

Darsdagi amaliyot:
- O'quv markazi kursi uchun 1 ta post + 1 ta story (bir xil uslubda).

Baholash (100 ball):
- To'g'ri o'lcham va kompozitsiya — 30
- Uslub izchilligi (post + story + slaydlar) — 40
- Matnning qisqa va aniqligi — 30""",
            """1. Sevimli kitobingiz yoki filmingiz uchun 3 ta postdan iborat seriya yarating.
2. Bitta story qo'shing.
3. Canva havolasini "view only" qilib ustozga yuboring.""",
            "https://www.canva.com/designschool/",
        ),
        T(
            "ST11",
            "Figma — interfeys, frame va asosiy shakllar",
            """Maqsad: Figma interfeysi bilan tanishish va oddiy mobil ekran maketini chizish.

Dars rejasi:
1. Figma'da hisob, fayl, sahifa; Frame (Phone 375×812) — 15 daq.
2. Asboblar: Rectangle, Ellipse, Text, Line; Layers paneli — 20 daq.
3. Auto layout'ga kirish: tugma (button) yasash — 15 daq.
4. Rang, radius, soya (drop shadow), shrift sozlamalari — 15 daq.
5. Amaliyot: ilovaning "Kirish" (Login) ekrani — 25 daq.

Darsdagi amaliyot:
- Logo, 2 ta input, "Kirish" tugmasi va "Parolni unutdingizmi?" havolasi bo'lgan Login ekrani.

Baholash (100 ball):
- Frame va qatlamlar tartibi (nomlangan layer'lar) — 30
- Tekislash va bo'sh joylar — 40
- Tugma auto layout bilan — 30""",
            """1. Shu ilova uchun "Ro'yxatdan o'tish" ekranini chizing.
2. Layer'larni ma'noli nomlang (masalan, "btn/primary").""",
            "https://help.figma.com",
        ),
        T(
            "ST12",
            "Figma — komponentlar, ranglar va to'liq dizayn",
            """Maqsad: qayta ishlatiladigan komponentlar bilan izchil interfeys yaratish.

Dars rejasi:
1. Component va Instance; asosiy komponentni o'zgartirish — 20 daq.
2. Variants: tugmaning primary/secondary holatlari — 15 daq.
3. Rang va matn uslublari (Color/Text styles) — 15 daq.
4. Amaliyot: 3 ekranli ilova (Bosh sahifa, Ro'yxat, Profil) — 40 daq.

Darsdagi amaliyot:
- Kamida 3 ta komponent: tugma, kartochka, pastki menyu; barcha ekranlarda instance sifatida.

Baholash (100 ball):
- Komponentlar to'g'ri ishlatilgan — 40
- Rang/matn uslublari — 30
- 3 ekran izchilligi — 30""",
            """1. Ilovangizga 4-ekran qo'shing (Sozlamalar).
2. Kartochka komponentiga "tanlangan" varianti qo'shing.""",
            "https://help.figma.com",
        ),
        T(
            "ST13",
            "Figma — prototip yaratish va eksport",
            """Maqsad: ekranlarni bog'lab interaktiv prototip yaratish va dizaynni eksport qilish.

Dars rejasi:
1. Prototype rejimi: bog'lanishlar (On click → Navigate to) — 20 daq.
2. Animatsiyalar: Instant, Dissolve, Smart animate — 15 daq.
3. Prototipni telefonda/brauzerda ko'rish, havola ulashish — 15 daq.
4. Eksport: PNG/JPG/SVG/PDF, @2x — 15 daq.
5. Taqdimot: har bir o'quvchi prototipini ko'rsatadi — 25 daq.

Darsdagi amaliyot:
- 3–4 ekranli ilovani to'liq bog'langan prototipga aylantirish.

Baholash (100 ball):
- Barcha tugmalar ishlaydi — 40
- To'g'ri eksport — 20
- Taqdimot — 40""",
            """1. Prototip havolasini ustozga yuboring.
2. Asosiy ekranni PNG (@2x) formatida eksport qilib, Drive papkangizga joylang.""",
            "https://help.figma.com",
        ),
    ],
)

PROGRAMMING = M(
    "Starter 3 · Dasturlashga kirish: Terminal va Scratch",
    "Buyruqlar qatori, algoritm va mantiqiy fikrlash; Scratch'da o'yinlar.",
    [
        T(
            "ST14",
            "Terminal — asosiy buyruqlar",
            """Maqsad: kompyuterni buyruqlar qatori orqali boshqarish asoslari.

Dars rejasi:
1. Terminal/PowerShell nima, nega dasturchilarga kerak — 10 daq.
2. Navigatsiya: pwd, ls (dir), cd, cd .. — 20 daq.
3. Fayl va papkalar: mkdir, touch (ni), cp, mv, rm — ehtiyot choralari — 25 daq.
4. Foydali: echo, cat, clear, Tab bilan avtoto'ldirish, ↑ tarix — 15 daq.
5. Amaliyot: topshiriqli "xazina ovi" — 20 daq.

Darsdagi amaliyot:
- Terminal orqali loyiha/{docs,images,code} tuzilmasini yaratish va fayllarni ko'chirish.

Baholash (100 ball):
- Navigatsiya — 30
- Fayl/papka amallari — 50
- Xavfsiz ishlash (rm'dan oldin tekshirish) — 20""",
            """1. Terminal orqali "maktab" papkasini va ichida 5 ta fan papkasini yarating.
2. Har biriga bitta matnli fayl qo'shing va ls/dir natijasini skrinshot qiling.""",
            "https://ss64.com",
        ),
        T(
            "ST15",
            "Scratch — dasturlash asoslari: sprite, sahna, bloklar",
            """Maqsad: algoritm tushunchasi va Scratch'da birinchi animatsiya.

Dars rejasi:
1. Algoritm nima: kundalik misollar (choy damlash) — 10 daq.
2. Scratch interfeysi: sahna, sprite, kostyum, fon — 15 daq.
3. Bloklar: Motion (harakat), Looks (ko'rinish), Sound (ovoz), Events (hodisalar) — 25 daq.
4. Koordinatalar (x, y) va burilish — 15 daq.
5. Amaliyot: qisqa animatsion hikoya — 25 daq.

Darsdagi amaliyot:
- 2 ta qahramon gaplashadigan, fon almashadigan 30 soniyalik animatsiya.

Baholash (100 ball):
- Hodisalar (yashil bayroq, tugma bosilganda) — 30
- Harakat va ko'rinish bloklari — 40
- Ijodkorlik — 30""",
            """1. "Mening kunim" animatsiyasi: kamida 3 sahna va 2 ta sprite.
2. Loyihani Scratch'da Share qilib, havolani yuboring.""",
            "https://scratch.mit.edu/ideas",
        ),
        T(
            "ST16",
            "Scratch — shartlar, sikllar va mini-o'yin",
            """Maqsad: if/else, repeat, forever va o'zgaruvchi bilan o'yin yaratish.

Dars rejasi:
1. Sikllar: repeat N, forever — 15 daq.
2. Shartlar: if, if/else, "touching", "key pressed" — 20 daq.
3. O'zgaruvchi: ball (score) va hayotlar (lives) hisoblagichi — 15 daq.
4. Amaliyot: "To'siqdan qoch" o'yini — 40 daq.

Darsdagi amaliyot:
- O'yinchi strelkalar bilan boshqariladi, to'siqqa tegsa hayot kamayadi, yulduz yig'sa ball oshadi,
  hayot 0 bo'lsa "Game Over".

Baholash (100 ball):
- Boshqaruv va sikllar — 30
- Shartlar to'g'ri — 40
- Ball/hayot hisoblagichi — 30""",
            """1. O'yiningizga 2-daraja (tezroq to'siqlar) qo'shing.
2. Eng yuqori natija (high score) o'zgaruvchisini qo'shing.""",
            "https://scratch.mit.edu/ideas",
        ),
    ],
)

DIGITAL_LIFE = M(
    "Starter 4 · Raqamli hayot va yakuniy loyiha",
    "Onlayn muloqot, vaqtni rejalashtirish, xavfsizlik va kurs yakuni.",
    [
        T(
            "ST17",
            "Google Meet va Calendar — video muloqot va rejalashtirish",
            """Maqsad: onlayn darsda qatnashish va o'z vaqtini rejalashtirish.

Dars rejasi:
1. Meet: uchrashuv yaratish, havola, mikrofon/kamera odobi — 15 daq.
2. Ekranni ulashish, chat, qo'l ko'tarish, subtitrlar — 20 daq.
3. Calendar: tadbir yaratish, takrorlanuvchi dars jadvali, eslatma — 20 daq.
4. Tadbirga Meet havolasi va mehmonlar qo'shish — 10 daq.
5. Amaliyot: guruhda 10 daqiqalik onlayn "mini-dars" — 25 daq.

Darsdagi amaliyot:
- Har bir o'quvchi haftalik dars jadvalini Calendar'da takrorlanuvchi tadbir sifatida yaratadi.

Baholash (100 ball):
- Meet'da ekran ulashish — 40
- Takrorlanuvchi tadbir va eslatma — 40
- Onlayn odob — 20""",
            """1. Kelgusi haftadagi barcha darslar va uy vazifalari vaqtini Calendar'ga kiriting.
2. Do'stingiz bilan 5 daqiqalik Meet qilib, ekran ulashishni mashq qiling (skrinshot).""",
            "https://support.google.com/meet\nhttps://support.google.com/calendar",
        ),
        T(
            "ST18",
            "Onlayn xavfsizlik: kuchli parol, 2FA, fishing, raqamli gigiyena",
            """Maqsad: o'z hisoblarini himoya qilish va onlayn firibgarlikni tanish.

Dars rejasi:
1. Kuchli parol: uzunlik (12+), parol-ibora, har saytda boshqa parol, parol menejeri — 15 daq.
2. 2FA (ikki bosqichli tasdiqlash): Google hisobida yoqish — 15 daq.
3. Fishing: soxta xat/sayt belgilari (manzil, shoshiltirish, imlo xatolari) — 20 daq.
4. Raqamli gigiyena: shaxsiy ma'lumot, kamera/mikrofon ruxsatlari, ekran vaqti — 15 daq.
5. Viktorina: "Haqiqiymi yoki fishingmi?" (10 misol) — 25 daq.

Darsdagi amaliyot:
- Google hisobida Security Checkup'dan o'tish va 2FA'ni yoqish (ota-ona ruxsati bilan).

Baholash (100 ball):
- Viktorina natijasi — 50
- 2FA / Security Checkup bajarilgan — 30
- Shaxsiy xavfsizlik rejasi — 20""",
            """1. Oilangiz uchun "5 ta xavfsizlik qoidasi" plakatini Canva'da tayyorlang.
2. Telefoningizdagi ilovalar ruxsatlarini tekshirib, keraksizlarini o'chiring (ro'yxat yozing).""",
            "https://myaccount.google.com/security-checkup\nhttps://haveibeenpwned.com",
        ),
        T(
            "ST19",
            "Yakuniy loyiha va sertifikat topshirish",
            """Maqsad: Starter kursidagi barcha vositalarni bitta loyihada ko'rsatish va himoya qilish.

Loyiha talablari (individual yoki 2 kishilik):
- Mavzu: "Mening kichik biznesim / ijtimoiy loyiham".
- Canva: logo + 1 ta post; Figma: 3 ekranli ilova prototipi;
  Sheets: xarajat/daromad jadvali va diagramma; Slides: 6–8 slaydli taqdimot;
  Scratch (ixtiyoriy): loyiha reklamasi uchun mini-animatsiya.
- Hammasi bitta Drive papkasida, ustozga ulashilgan.

Dars rejasi:
1. Yakuniy tayyorgarlik — 20 daq.
2. Himoya: har bir o'quvchi 4–5 daqiqa + savollar — 60 daq.
3. Sertifikatlar topshirish va Python kursiga o'tish haqida — 10 daq.

Baholash (100 ball):
- Vositalarni qo'llash (Canva, Figma, Sheets, Slides) — 50
- Taqdimot va savollarga javob — 30
- Tartib va o'z vaqtida topshirish — 20""",
            """Python kursiga tayyorgarlik: kompyuteringizga Python 3 va VS Code o'rnating
(https://www.python.org/downloads/) va "python --version" natijasini skrinshot qiling.""",
            "https://www.python.org/downloads/\nhttps://code.visualstudio.com",
        ),
    ],
)

MODULES = [GOOGLE, DESIGN, PROGRAMMING, DIGITAL_LIFE]
