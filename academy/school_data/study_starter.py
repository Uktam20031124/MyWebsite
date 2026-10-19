"""Starter kursi: "Darsni qayta mustahkamlash" materiallari (mavzu kaliti bo'yicha).

O'quvchi testdan past natija olsa, profilida ko'radi. Format — ``ui.study_md``:
## sarlavha, ### kichik sarlavha, - / 1. ro'yxat, > eslatma, ``` kod ```, `kod`, **qalin**.
Python misollaridagi "Natija:" bloklari kodni ishga tushirib tekshirilgan.
"""

STUDY = {
    "ST01": """
## Mavzu nima haqida
10 barmoqli (ko'r) yozish — klaviaturaga qaramasdan, har bir tugmani "o'z" barmog'i bilan bosish usuli. Bu usulni o'rgangan odam 2–3 baravar tez va kam xato bilan yozadi. Monkeytype — tezlik va aniqlikni o'lchaydigan bepul sayt.

## Asosiy tushunchalar
- **Uy qatori** — barmoqlar doim qaytib keladigan qator: chap qo'l `A S D F`, o'ng qo'l `J K L ;`. Ko'rsatkich barmoqlar F va J da turadi.
- **Bo'rtiqlar** — F va J tugmalaridagi kichik do'mboqchalar. Qaramasdan, barmoq uchi bilan uy qatorini topish uchun.
- **WPM** (words per minute) — bir daqiqada yozilgan so'zlar soni. Hisoblashda 1 "so'z" = 5 ta belgi.
- **Accuracy (aniqlik)** — to'g'ri bosilgan belgilar foizi. 95% dan past bo'lsa, tezlikni oshirishga shoshilmang.
- **Bosh barmoq** — faqat probel (Space) uchun. Shift — harfni bosayotgan qo'lning **qarama-qarshi** qo'li jimjilog'i bilan.

## Bajarilgan misollar
### Misol 1. WPM ni hisoblash
60 soniyada 250 ta belgi to'g'ri yozildi. WPM = 250 ÷ 5 = **50 WPM**.
30 soniyada 150 ta belgi bo'lsa: 1 daqiqaga aylantiramiz → 300 belgi → 300 ÷ 5 = **60 WPM**.

### Misol 2. Aniqlikni hisoblash
Jami 200 ta bosish, shundan 190 tasi to'g'ri. Aniqlik = 190 ÷ 200 × 100 = **95%**. Bu yaxshi natija.
Agar 160 tasi to'g'ri bo'lsa → 80%. Demak, sekinroq, lekin xatosiz yozish kerak.

### Misol 3. Qaysi barmoq?
- "G" — chap ko'rsatkich barmoq (F dan o'ngga cho'ziladi).
- "H" — o'ng ko'rsatkich barmoq (J dan chapga).
- "Katta A" — o'ng qo'l jimjilog'i bilan o'ng Shift, chap jimjiloq bilan A.

### Misol 4. Haftalik reja
1-kun: 3 × 60 s test, natijalarni yozish (masalan 28, 30, 31 WPM, aniqlik 92%).
2–5-kun: har kuni 10 daqiqa. Maqsad: aniqlik 95%+, keyin tezlik +5 WPM.

## Ko'p uchraydigan xatolar
- Klaviaturaga qarab yozish — tezlik o'smaydi, chunki ko'z va qo'l doim almashadi.
- Faqat tezlikka intilish — xatolar odat bo'lib qoladi. **Avval aniqlik!**
- Bir qo'l bilan Shift va harfni birga bosish — barmoqlar charchaydi.
- Bukchayib o'tirish: tez charchaysiz, bilaklar og'riydi.

## Chuqurroq
- Muskul xotirasi takror bilan shakllanadi: har kuni 10 daqiqa, haftada bir marta 1 soatdan foydaliroq.
- Monkeytype'da "words" rejimida aniq so'zlar soni, "time" rejimida aniq vaqt beriladi. Natijani solishtirish uchun doim bir xil rejimdan foydalaning (masalan, time 60).
- keybr.com — yangi boshlovchilar uchun: harflarni bittadan qo'shib o'rgatadi.

## O'zingizni tekshiring
1. 45 soniyada 300 ta belgi yozildi. WPM qancha? (Javob: 300 × 60/45 = 400 belgi/daq → 80 WPM)
2. O'ng qo'l uy qatoridagi barmoqlar qaysi tugmalarda? (J K L ;)
3. Nega aniqlik 95% dan past bo'lsa tezlikni oshirmaslik kerak?
""",
    "ST02": """
## Mavzu nima haqida
Gmail — Google'ning elektron pochtasi. Ustozga vazifa yuborish, hujjat almashish, rasmiy yozishmalar uchun kerak. To'g'ri tuzilgan xat — madaniyat belgisi.

## Asosiy tushunchalar
- **Inbox** — kiruvchi xatlar; **Sent** — yuborilganlar; **Drafts** — yozilgan, lekin yuborilmagan; **Spam** — shubhali; **Trash** — o'chirilganlar (30 kun saqlanadi).
- **To** — asosiy qabul qiluvchi. **Cc** — nusxa: hamma ko'radi. **Bcc** — yashirin nusxa: boshqalar bu manzilni ko'rmaydi.
- **Reply** — faqat yuboruvchiga javob; **Reply all** — xatdagi hammaga; **Forward** — xatni boshqa odamga uzatish.
- **Label (yorliq)** — xatlarni mavzu bo'yicha guruhlash. **Filtr** — shartga mos xatlarga avtomatik label qo'yish.
- **Ilova** — qisqich 📎 belgisi orqali fayl qo'shish (25 MB gacha; kattasini Drive havolasi bilan).

## Bajarilgan misollar
### Misol 1. Ustozga to'g'ri xat
**Mavzu:** Uy vazifasi №3 — Aliyev Sardor
**Matn:**
Assalomu alaykum, ustoz!
3-uy vazifasini ilova qildim (Google Docs havolasi: ...).
Savolim: 2-topshiriqdagi jadvalni PDF qilib yuborsam bo'ladimi?
Hurmat bilan, Sardor (S-009 guruh)
Nega yaxshi: mavzudan nima haqidaligi tushunarli, salomlashish, aniq matn, imzo bor.

### Misol 2. Cc yoki Bcc?
Siz ota-onalarga umumiy e'lon yuboryapsiz. Har bir ota-onaning manzili boshqalarga ko'rinmasligi kerak → manzillarni **Bcc** ga yozasiz, To ga esa o'zingizni.

### Misol 3. Filtr yaratish
Ustozdan keladigan hamma xat "Darslar" yorlig'ini olsin:
1. Qidiruv qatoridagi ⚙ (filtr) belgisi → From: ustoz@gmail.com
2. "Create filter" → "Apply the label: Darslar" → Create.
Endi har bir yangi xat avtomatik shu yorliqqa tushadi.

### Misol 4. Fishingni aniqlash
"Hisobingiz bloklandi! 1 soat ichida parolni shu havolada kiriting: g00gle-security.com"
Belgilar: shoshiltiradi, parol so'raydi, manzil soxta (0 harfi o o'rniga). Javob: havolani bosmang, xatni Spam deb belgilang.

## Ko'p uchraydigan xatolar
- Mavzusiz xat — u spamga tushishi yoki o'qilmasligi mumkin.
- "Reply all" ni bilmasdan bosish — shaxsiy javob butun guruhga ketadi.
- Faylni ilova qilishni unutish. Gmail "ilova" so'zi bor, lekin fayl yo'q bo'lsa ogohlantiradi — e'tibor bering.
- Ko'p odamga To orqali yuborish — hammaning manzili hammaga ochiladi.

## Chuqurroq
- **Undo send** — yuborgandan keyin 5–30 soniya ichida bekor qilish mumkin (Settings → Undo Send).
- **Schedule send** — xatni belgilangan vaqtda yuborish.
- Qidiruv operatorlari: `from:ustoz has:attachment`, `subject:vazifa`, `older_than:7d`.

## O'zingizni tekshiring
1. Ota-onalarga xat yuborishda manzillar bir-biriga ko'rinmasligi uchun qaysi maydon? (Bcc)
2. Xat yuborildi, lekin Sent'da yo'q. Qayerni tekshirasiz? (Drafts yoki Outbox — internet uzilgan bo'lishi mumkin)
3. Ustozga yozgan xatingiz uchun to'g'ri mavzu o'ylab toping.
""",
    "ST03": """
## Mavzu nima haqida
Google Docs — brauzerda ishlaydigan matn muharriri. Hujjat bulutda saqlanadi, bir vaqtda bir necha kishi tahrirlay oladi, har bir o'zgarish tarixi qoladi.

## Asosiy tushunchalar
- **Avtosaqlash** — har bir o'zgarish darhol saqlanadi ("Saved to Drive").
- **Uslublar (Styles)** — Normal text, Title, Heading 1, Heading 2. Sarlavhani shu uslublar bilan qilsangiz, chap tomonda **outline** (tuzilma) chiqadi va **mundarija** (Insert → Table of contents) avtomatik yasaladi.
- **Huquqlar:** Viewer — faqat o'qiydi; Commenter — izoh/taklif qoldiradi; Editor — tahrirlaydi; Owner — egasi.
- **Suggesting rejimi** — o'zgarish "taklif" sifatida ko'rinadi, egasi qabul yoki rad etadi.
- **Izoh (Comment)** — matn bo'lagini belgilab, Ctrl+Alt+M.

## Bajarilgan misollar
### Misol 1. Referat tuzilmasi
1. Mavzu nomi → **Title** uslubi.
2. "Kirish", "Asosiy qism", "Xulosa" → **Heading 1**.
3. Asosiy qism ichidagi bo'limlar → **Heading 2**.
4. Boshiga Insert → Table of contents. Sarlavha o'zgarsa, mundarijadagi ↻ ni bosing.

### Misol 2. Ustozga izoh huquqi bilan ulashish
Share → ustozning emaili → rolni **Commenter** qiling → Send. Ustoz izoh qoldiradi, lekin matningizni o'zgartira olmaydi.

### Misol 3. Jadval qo'shish
Insert → Table → 3×4. Birinchi qatorga sarlavhalar: "Kun", "Mavzu", "Vaqt". Sarlavha qatorini qalin (Ctrl+B) va fonini rangli qiling.

### Misol 4. Tez tugmalar
- Ctrl+B — qalin, Ctrl+I — kursiv, Ctrl+U — tagiga chizish
- Ctrl+K — havola qo'shish
- Ctrl+Shift+E — markazga, Ctrl+Shift+L — chapga tekislash
- Ctrl+Z — bekor qilish, Ctrl+Y — qaytarish

## Ko'p uchraydigan xatolar
- Sarlavhani shunchaki kattalashtirish — mundarija ishlamaydi.
- Bo'sh joyni ko'p Enter/probel bilan to'ldirish — Line spacing va Page break ishlating.
- Hujjatni hammaga **Editor** qilib ulashish — kimdir tasodifan o'chirishi mumkin.

## Chuqurroq
- **Version history** (File → Version history): eski holatni ko'rish va tiklash; muhim versiyaga nom bering.
- **Voice typing** (Tools → Voice typing) — ovoz bilan yozish.
- File → Download → PDF/DOCX — boshqa formatga saqlash.

## O'zingizni tekshiring
1. Mundarija avtomatik bo'lishi uchun sarlavhalarga nima qilish kerak? (Heading uslubi)
2. Do'stingiz matningizni o'zgartirmasdan faqat taklif bersin desangiz, qaysi rol? (Commenter)
3. Kecha o'chirib yuborgan paragrafni qanday qaytarasiz? (Version history)
""",
    "ST04": """
## Mavzu nima haqida
Google Slides — taqdimot (prezentatsiya) yaratish dasturi. Yaxshi taqdimot — kam matn, aniq fikr, chiroyli va izchil dizayn.

## Asosiy tushunchalar
- **Theme** — ranglar va shriftlar to'plami; butun taqdimotga bir xil uslub beradi.
- **Layout (maket)** — slayddagi sarlavha, matn, rasm joylarining joylashuvi.
- **Transition** — slayddan slaydga o'tish effekti; **Animation** — slayd ichidagi bitta obyekt harakati.
- **Speaker notes** — ma'ruzachi eslatmalari, tomoshabin ko'rmaydi.
- **Qoida: 1 slayd — 1 fikr.** Ko'pi bilan 5–6 qator, shrift 24 pt dan katta.

## Bajarilgan misollar
### Misol 1. "Mening shahrim" taqdimoti rejasi
1. **Titul:** "Samarqand — Sharq durdonasi", ism-familiya.
2. **Tarix:** 3 ta qisqa fakt + rasm.
3. **Diqqatga sazovor joylar:** Registon, Shohi Zinda — rasmlar bilan.
4. **Taomlar:** non, plov — 2 ta rasm.
5. **Yakun:** "Rahmat! Savollar?"

### Misol 2. Yomon slaydni tuzatish
Yomon: 12 qator matn, 14 pt shrift, och sariq fonda oq yozuv.
Yaxshi: sarlavha + 3 ta qisqa band, 28 pt, to'q fonda oq yozuv yoki oq fonda qora yozuv, bitta rasm.

### Misol 3. Tez ishlash
- Ctrl+M — yangi slayd; Ctrl+D — slaydni nusxalash.
- Insert → Image → rasm qo'shish.
- Ctrl+F5 (yoki Slideshow) — to'liq ekranda ko'rsatish.

## Ko'p uchraydigan xatolar
- Slayddagi matnni so'zma-so'z o'qish — tomoshabin zerikadi.
- Har slaydga har xil shrift va rang — tartibsiz ko'rinadi.
- Juda ko'p animatsiya — diqqat mazmundan chalg'iydi.
- Kontrastsiz ranglar — matn o'qilmaydi.

## Chuqurroq
- **Kontrast** — fon va matn rangi orasidagi farq. To'q fon + och matn yoki aksincha.
- **Master slide** (Slide → Edit theme) — bitta joyda o'zgartirsangiz, hamma slayd yangilanadi.
- 1 daqiqalik nutq qoidasi: 1 asosiy fikr, 2–3 dalil, 1 xulosa.

## O'zingizni tekshiring
1. Transition va Animation farqi nima?
2. Tomoshabin ko'rmaydigan eslatmalar qayerga yoziladi? (Speaker notes)
3. Bitta slaydga 10 qator matn sig'dirdingiz. Qanday tuzatasiz?
""",
    "ST05": """
## Mavzu nima haqida
Google Drive — bulutli xotira: fayllarni saqlash, papkalarga ajratish, boshqalar bilan ulashish va birga ishlash. Kompyuter buzilsa ham fayllaringiz yo'qolmaydi.

## Asosiy tushunchalar
- Bepul hisobda **15 GB** joy (Gmail, Drive, Photos uchun umumiy).
- **My Drive** — o'z fayllaringiz; **Shared with me** — sizga ulashilganlar; **Trash** — o'chirilganlar (30 kun ichida tiklash mumkin).
- **Ulashish:** odam qo'shish (email) yoki havola (link). "Restricted" — faqat qo'shilganlar; "Anyone with the link" — havolasi bor har kim.
- **Rollar:** Viewer, Commenter, Editor.
- **Version history** — faylning oldingi holatlari.

## Bajarilgan misollar
### Misol 1. Papka tuzilmasi
```
Starter_Sardor/
    Docs/
    Slides/
    Rasmlar/
```
New → Folder → "Starter_Sardor". Ichida yana uchta papka. Fayllarni sudrab (drag & drop) kerakli papkaga tashlang.

### Misol 2. Jamoaviy taqdimot
1. Bitta o'quvchi Slides yaratadi, "Jamoa_loyiha" papkasiga qo'yadi.
2. Share → jamoa a'zolarining emaillari → **Editor**.
3. Ustozga → **Commenter**.
Endi hamma bir faylda bir vaqtda ishlaydi, o'zgarishlar darhol ko'rinadi.

### Misol 3. O'chirilgan faylni tiklash
Chap menyuda Trash → faylni o'ng tugma → Restore. 30 kundan o'tsa, butunlay o'chadi.

## Ko'p uchraydigan xatolar
- Hamma faylni bitta joyda "Untitled document" nomi bilan saqlash — keyin topib bo'lmaydi.
- Shaxsiy hujjatni "Anyone with the link" bilan ulashish — havola boshqa qo'lga tushsa, hamma ko'radi.
- Faylni yuklab olib, o'zgartirib, qayta yuklash — nusxalar ko'payib ketadi. Brauzerda to'g'ridan-to'g'ri ishlang.

## Chuqurroq
- **Starred** (yulduzcha) — tez-tez kerak bo'ladigan fayllar.
- Qidiruv: fayl turi (PDF, rasm), egasi, sana bo'yicha filtr.
- **Drive for desktop** — kompyuterdagi papkani bulut bilan sinxronlash.

## O'zingizni tekshiring
1. Ustoz izoh qoldirsin, lekin o'zgartirmasin — qaysi rol? (Commenter)
2. "Anyone with the link" xavfi nimada?
3. Kecha o'chirgan faylingiz qayerda? (Trash)
""",
    "ST06": """
## Mavzu nima haqida
Google Sheets — elektron jadval. Sonlarni saqlash, hisoblash, saralash va tahlil qilish uchun. Formulalar bilan qo'lda hisoblash shart emas — jadval o'zi hisoblaydi va ma'lumot o'zgarsa, natija ham yangilanadi.

## Asosiy tushunchalar
- **Yacheyka manzili:** ustun harfi + qator raqami. `B3` — B ustun, 3-qator.
- **Oraliq:** `B2:B10` — B2 dan B10 gacha.
- **Formula** doim `=` bilan boshlanadi: `=A1+A2`.
- **Asosiy funksiyalar:**
- `SUM(oraliq)` — yig'indi
- `AVERAGE(oraliq)` — o'rtacha
- `COUNT(oraliq)` — sonli yacheykalar soni
- `MIN` / `MAX` — eng kichik / eng katta
- **Avtoto'ldirish:** yacheyka burchagidagi kvadratchani pastga tortsangiz, formula nusxalanadi va manzillar o'zgaradi (A1 → A2).

## Bajarilgan misollar
### Misol 1. Baholar jadvali
A1: Ism, B1: Matematika, C1: Ingliz, D1: O'rtacha
A2: Ali, B2: 85, C2: 90
D2 ga: `=AVERAGE(B2:C2)` → **87.5**
Formulani D3, D4 ga cho'zsangiz: `=AVERAGE(B3:C3)`, `=AVERAGE(B4:C4)` bo'ladi.

### Misol 2. Guruh statistikasi
B2:B11 — 10 ta o'quvchining balli.
- Jami: `=SUM(B2:B11)`
- O'rtacha: `=AVERAGE(B2:B11)`
- Eng yuqori: `=MAX(B2:B11)`
- Nechta baho kiritilgan: `=COUNT(B2:B11)` (bo'sh yacheykalar hisoblanmaydi)

### Misol 3. Nisbiy va mutlaq manzil
Har bir narxni dollar kursiga ko'paytirish: kurs **F1** da.
`=B2*F1` ni pastga cho'zsangiz `=B3*F2` bo'ladi — xato! F2 bo'sh.
To'g'risi: `=B2*$F$1`. `$` belgisi manzilni "qotiradi".

### Misol 4. Foiz formati
0.85 → Format → Number → Percent → **85%**. Yoki formulada: `=B2/C2` va foiz formatini qo'yish.

## Ko'p uchraydigan xatolar
- `=` ni unutish: `SUM(B2:B5)` shunchaki matn bo'lib qoladi.
- Sonni matn sifatida kiritish ("85 ball") — formula uni hisoblamaydi.
- Oraliqni noto'g'ri belgilash: `=SUM(B2:B5)` jadval B10 gacha bo'lsa, qolganlari tushib qoladi.

## Chuqurroq
- `COUNTA` — bo'sh bo'lmagan hamma yacheykalar (matn ham).
- `ROUND(son; 1)` — yaxlitlash.
- **Saralash:** Data → Sort range (A→Z o'sish, Z→A kamayish). **Filtr:** shartga mos qatorlarni ko'rsatadi, qolganini vaqtincha yashiradi.

## O'zingizni tekshiring
1. `=A1*2` ni ikki qator pastga cho'zsangiz qanday formula bo'ladi? (`=A3*2`)
2. 5 ta bahodan 2 tasi bo'sh. `COUNT` nechani ko'rsatadi? (3)
3. Nega `$F$1` kerak bo'ladi?
""",
    "ST07": """
## Mavzu nima haqida
Diagramma — sonlarni ko'z bilan tez tushunish usuli. Shartli formatlash esa jadvaldagi muhim qiymatlarni avtomatik ranglab beradi. `IF` funksiyasi shartga qarab natija chiqaradi.

## Asosiy tushunchalar
- **Ustunli (column)** — bir nechta narsani solishtirish (o'quvchilar ballari).
- **Chiziqli (line)** — vaqt bo'yicha o'zgarish (oylar bo'yicha baho).
- **Doiraviy (pie)** — butunning qismlari (foiz ulushlar).
- **Legenda** — qaysi rang qaysi ma'lumotga tegishli.
- **Shartli formatlash** — Format → Conditional formatting: "60 dan kichik bo'lsa — qizil".
- **IF:** `=IF(shart; rost_bo'lsa; yolg'on_bo'lsa)`.

## Bajarilgan misollar
### Misol 1. Diagramma qurish
1. A1:B6 ni belgilang (ism va ball).
2. Insert → Chart. Sheets o'zi tur tanlaydi.
3. Chart editor → Setup → Chart type: Column.
4. Customize → Chart & axis titles: "Guruh ballari".

### Misol 2. Qaysi diagramma?
- 6 oy davomida o'rtacha baho → **line**.
- Guruhda a'lochi/yaxshi/qoniqarli ulushi → **pie**.
- 5 ta o'quvchining test natijasi → **column**.

### Misol 3. IF bilan baholash
B2 da ball. C2 ga: `=IF(B2>=60; "O'tdi"; "Qayta topshiradi")`
- B2 = 75 → O'tdi
- B2 = 60 → O'tdi (>= teng ham kiradi)
- B2 = 59 → Qayta topshiradi

### Misol 4. Ichma-ich IF
`=IF(B2>=86; "5"; IF(B2>=71; "4"; IF(B2>=56; "3"; "2")))`
B2 = 78 → "4". Avval birinchi shart tekshiriladi, mos kelmasa — keyingisi.

### Misol 5. Qizil va yashil
Belgilang B2:B20 → Format → Conditional formatting:
- "Less than" 60 → qizil fon.
- "Add another rule" → "Greater than or equal to" 86 → yashil fon.

## Ko'p uchraydigan xatolar
- Matnni qo'shtirnoqsiz yozish: `=IF(B2>60; O'tdi; ...)` → xato.
- Pie diagrammani vaqt bo'yicha ma'lumotga ishlatish — o'zgarish ko'rinmaydi.
- Sarlavhasiz diagramma — nima haqida ekani tushunarsiz.

## Chuqurroq
- Ba'zi tillarda vergul `,` o'rniga nuqtali vergul `;` ishlatiladi — bu jadval sozlamasiga (locale) bog'liq.
- `COUNTIF(B2:B20; "<60")` — 60 dan past nechta o'quvchi borligini sanaydi.
- Slides'ga **bog'langan** diagramma: Insert → Chart → From Sheets; jadval o'zgarsa "Update" bosiladi.

## O'zingizni tekshiring
1. `=IF(A1>10; "katta"; "kichik")`, A1 = 10 bo'lsa natija? ("kichik")
2. Butunning qismlarini ko'rsatish uchun qaysi diagramma? (pie)
3. 50 dan past baholarni qanday avtomatik qizil qilasiz?
""",
    "ST08": """
## Mavzu nima haqida
1-oy yakuniy amaliy dars — o'rgangan barcha vositalarni bitta jamoaviy loyihada birlashtirish: "Sayohat rejasi". Bu real ishga o'xshaydi: reja, hisob-kitob, taqdimot va hisobot.

## Asosiy tushunchalar
- **Drive** — umumiy jamoa papkasi (hamma fayl bir joyda).
- **Docs** — sayohat rejasi: manzil, kun tartibi, qoidalar.
- **Sheets** — xarajatlar smetasi: SUM, AVERAGE, diagramma.
- **Slides** — 5–6 slaydli taqdimot.
- **Gmail** — tayyor ishni ustozga rasmiy xat bilan yuborish.

## Bajarilgan misollar
### Misol 1. Ish taqsimoti (4 kishilik jamoa)
1. Ali — Drive papka, ulashish, Gmail xat.
2. Vali — Docs: reja.
3. Nigora — Sheets: smeta + diagramma.
4. Sardor — Slides: taqdimot.
Hammasi Editor; ustoz — Commenter.

### Misol 2. Smeta
Yo'l: 400 000, Mehmonxona: 600 000, Ovqat: 300 000, Muzey: 100 000
Jami: `=SUM(B2:B5)` → **1 400 000**
4 kishiga: `=B6/4` → **350 000** har biriga.
Eng katta xarajat: `=MAX(B2:B5)` → 600 000 (mehmonxona).

### Misol 3. Ustozga xat
**Mavzu:** 1-oy loyihasi — "Toshkent–Samarqand sayohati" (S-009, 2-jamoa)
Matn: salomlashish, papka havolasi, jamoa a'zolari, rahmat, imzo.

## Ko'p uchraydigan xatolar
- Har kim faylni o'z Drive'ida saqlaydi — keyin yig'ib bo'lmaydi.
- Smetada raqamni matn qilib yozish ("400 ming") — SUM hisoblamaydi.
- Taqdimotda smeta jadvalini rasm qilib qo'yish — o'zgarsa yangilanmaydi. From Sheets ishlating.

## Chuqurroq
- Jamoaviy ishda **Version history** kim nima o'zgartirganini ko'rsatadi — kelishmovchilikda foydali.
- Docs'da @ism yozsangiz, sherigingizga vazifa (assign) berasiz.
- Yaxshi loyiha: aniq maqsad, taqsimlangan vazifalar, muddat, yakunda tekshiruv.

## O'zingizni tekshiring
1. Jami xarajat 1 200 000, 3 kishi. Bir kishiga qancha? (400 000)
2. Ustozga loyihani qaysi huquq bilan ulashasiz? (Commenter)
3. Diagrammani taqdimotga qanday qo'yish to'g'ri? (Insert → Chart → From Sheets)
""",
    "ST09": """
## Mavzu nima haqida
Canva — brauzerda ishlaydigan oson dizayn dasturi. Tayyor shablonlardan foydalanib vizitka, post, plakat tayyorlash mumkin. Bu darsda dizaynning 4 asosiy qoidasi va vizitka yaratish.

## Asosiy tushunchalar
- **Kontrast** — elementlar orasidagi aniq farq (to'q fon + och matn).
- **Tekislash (alignment)** — elementlar bir chiziqda turadi, dizayn tartibli ko'rinadi.
- **Takrorlash (repetition)** — bir xil rang, shrift, uslub butun dizaynda.
- **Yaqinlik (proximity)** — bog'liq ma'lumotlar yonma-yon (telefon va email birga).
- **Bo'sh joy (white space)** — dizaynga "nafas" beradi.
- Shrift qoidasi: **2 ta shrift** (sarlavha + matn). Rang qoidasi: **3 ta asosiy rang**.

## Bajarilgan misollar
### Misol 1. Vizitka (90 × 50 mm)
1. Canva → "Business card" → bo'sh yoki shablon.
2. Old tomon: logo (Uploads), ism (katta, qalin), kasb (kichikroq).
3. Orqa tomon: telefon, email, Instagram — chapga tekislangan, bir ustunda.
4. Ranglar: to'q ko'k fon, oq matn, sariq aksent.

### Misol 2. Yomon → yaxshi
Yomon: 5 xil shrift, matn markazda ham, chapda ham; logo burchakka tiqilgan.
Yaxshi: 2 shrift, hamma matn chapga tekis, logo atrofida bo'sh joy.

### Misol 3. Eksport
- Chop etish uchun: Share → Download → **PDF Print** (sifatli).
- Ijtimoiy tarmoq uchun: **PNG** yoki JPG.
- Shaffof fonli logo: **PNG** (Canva Pro'da "transparent background").

## Ko'p uchraydigan xatolar
- Matnni vizitka chetiga juda yaqin qo'yish — chop etishda kesilib ketadi.
- Har bir so'zga boshqa rang — ko'z charchaydi.
- Kichik o'lchamli PNG ni chop etish — xira chiqadi.

## Chuqurroq
- Rang palitrasi uchun: coolors.co yoki Canva'ning "Color palette" generatori.
- Shriftlar juftligi: sarlavhaga dekorativ (Montserrat Bold), matnga oddiy (Open Sans).
- Ikki tomonli vizitkaning ikkala tomoni bir xil uslubda bo'lishi kerak — yagona brend hissi.

## O'zingizni tekshiring
1. Dizaynning 4 qoidasini ayting.
2. Chop etish uchun qaysi formatda yuklab olasiz? (PDF Print)
3. Nega 2 tadan ko'p shrift ishlatmaslik kerak?
""",
    "ST10": """
## Mavzu nima haqida
Ijtimoiy tarmoqlar uchun dizayn: post, story va taqdimot. Har bir platformaning o'lchami bor; bir brendning hamma materiallari bir xil uslubda bo'lishi kerak.

## Asosiy tushunchalar
- **Instagram post (kvadrat):** 1080 × 1080 px. **Story / Reels:** 1080 × 1920 px. **YouTube muqova:** 1280 × 720 px.
- **Ierarxiya** — eng muhim matn eng katta va ko'zga tashlanadigan.
- **Call to action (CTA)** — harakatga chaqiriq: "Hoziroq yoziling!", "Havolani bosing".
- **Brand kit** — logo, brend ranglari va shriftlari.
- **Xavfsiz zona** — story'da tepadagi va pastdagi ~250 px ga muhim matn qo'ymang (profil nomi va javob maydoni yopadi).

## Bajarilgan misollar
### Misol 1. Kurs reklamasi posti
1. Sarlavha (eng katta): "Python kursi — 0 dan"
2. Kichik matn: "3 oy · haftada 3 dars · sertifikat"
3. CTA tugma ko'rinishida: "Ro'yxatdan o'ting"
4. Pastda logo va telefon.
Ranglar: brend ranglari, 2 shrift.

### Misol 2. Postdan story'ga
Post dizaynini nusxalang → Resize → Instagram Story. Elementlarni vertikal joylashtiring, matnni xavfsiz zonaga oling.

### Misol 3. Feedback berish
"Yoqmadi" emas: "Sarlavha yaxshi ko'rinyapti. Pastdagi matn juda mayda — telefonda o'qilmaydi, 2 barobar kattalashtirsang yaxshi bo'ladi."

## Ko'p uchraydigan xatolar
- Post matni juda uzun — odamlar 2–3 soniyada o'tib ketadi.
- Telefonda tekshirmaslik — kompyuterda chiroyli, telefonda o'qilmaydi.
- Har postda boshqa uslub — brend tanilmaydi.

## Chuqurroq
- 3 soniya qoidasi: post nima haqida ekani 3 soniyada tushunarli bo'lishi kerak.
- Rasm sifati: kamida 1080 px kenglik.
- Ko'p sahifali taqdimotni yuborish — **PDF** eng qulay.

## O'zingizni tekshiring
1. Story o'lchami? (1080 × 1920)
2. CTA nima? 2 ta misol keltiring.
3. Nega postni telefonda ko'rib chiqish kerak?
""",
    "ST11": """
## Mavzu nima haqida
Figma — ilova va sayt interfeyslarini (UI) loyihalash vositasi. Dizaynerlar va dasturchilar bir faylda birga ishlaydi. Bu darsda Frame, asosiy shakllar, qatlamlar va Auto layout.

## Asosiy tushunchalar
- **Frame** — ekran chegarasi (telefon, planshet, sayt). Telefon uchun **375 × 812**.
- **Qatlamlar (Layers)** — chap panel: har bir element va ularning tartibi. Yuqoridagi qatlam ustida ko'rinadi.
- **Asboblar va tez tugmalar:** F/A — Frame, R — Rectangle, O — Ellipse, T — Text, L — Line, P — Pen.
- **O'ng panel:** o'lcham, rang (Fill), chegara (Stroke), **Corner radius** (burchak yumaloqligi), **Effects** (Drop shadow).
- **Auto layout** (Shift+A) — ichidagi elementlarni avtomatik joylashtiradi, matn o'zgarsa tugma o'lchami moslashadi.

## Bajarilgan misollar
### Misol 1. Tugma yasash
1. T bilan "Kirish" matnini yozing.
2. Matnni belgilab Shift+A — Auto layout. Padding: 16 (yon), 12 (tepa-past).
3. Fill: #2F80ED, matn oq, Corner radius: 10.
4. Matnni "Ro'yxatdan o'tish" ga o'zgartiring — tugma o'zi kengayadi.

### Misol 2. Login ekrani
Frame 375 × 812 ichida:
1. Logo (yuqorida, markazda).
2. Ikki input: "Email", "Parol" — 327 px kenglik, chapdan 24 px.
3. "Kirish" tugmasi (Misol 1).
4. "Parolni unutdingizmi?" — kichik matn havola.
Hammasini bitta Auto layout (vertikal, oraliq 16) ga solsangiz, tekislash avtomatik.

### Misol 3. Qatlamlarni nomlash
"Rectangle 12", "Frame 4" o'rniga: "btn/primary", "input/email", "screen/login". Katta loyihada kerakli elementni soniyalarda topasiz.

## Ko'p uchraydigan xatolar
- Elementlarni Frame tashqarisida qoldirish — eksport va prototipda chiqmaydi.
- Ko'z bilan tekislash — 1–2 px farq qoladi. Auto layout yoki Align tugmalarini ishlating.
- Nomlanmagan 100 ta qatlam — chalkashlik.

## Chuqurroq
- **Constraints** — ekran o'lchami o'zgarganda element qayerga "yopishadi" (chapga, markazga).
- **8 px grid** — oraliqlar 8, 16, 24, 32... bo'lsa, dizayn uyg'un ko'rinadi.
- Shift bosib chizsangiz — mukammal kvadrat/aylana.

## O'zingizni tekshiring
1. Telefon ekrani uchun Frame o'lchami? (375 × 812)
2. Auto layout qaysi tugmalar bilan qo'shiladi? (Shift+A)
3. Tugma burchagini yumaloq qilish uchun qaysi xususiyat? (Corner radius)
""",
    "ST12": """
## Mavzu nima haqida
Komponentlar — Figma'ning "qayta ishlatiladigan bloklari". Bitta tugmani komponent qilsangiz, uni 50 ta joyda ishlatib, hammasini bir joydan o'zgartirasiz. Rang va matn uslublari esa butun dizaynni izchil qiladi.

## Asosiy tushunchalar
- **Component (asosiy)** — yaratish: Ctrl+Alt+K. Belgisi: to'rt romb.
- **Instance** — komponent nusxasi. Asosiy o'zgarsa, hamma instance yangilanadi.
- **Override** — instance'da matn yoki rangni alohida o'zgartirish (bog'lanish saqlanadi).
- **Variants** — bitta komponentning holatlari: primary/secondary, default/hover/disabled.
- **Color styles** va **Text styles** — rang va shrift sozlamalarini nom bilan saqlash.

## Bajarilgan misollar
### Misol 1. Tugma komponenti
1. ST11 dagi tugmani belgilang → Ctrl+Alt+K → nom: "Button".
2. Assets panelidan 3 ta ekranga sudrab qo'ying (instance'lar).
3. Asosiy komponentda rangni o'zgartiring → uchala ekrandagi tugma ham o'zgaradi.

### Misol 2. Variants
Button'ni belgilang → "Add variant". Ikkinchisini: oq fon, ko'k chegara — "Type=Secondary". Instance'da o'ng paneldan Type ni almashtirasiz.

### Misol 3. Rang uslublari
Brend ko'k rangini #2F80ED → Fill yonidagi 4 nuqta → "+" → nom "Primary". Keyinchalik rangni #1E6FD9 ga almashtirsangiz — u ishlatilgan hamma joy yangilanadi.

### Misol 4. 3 ekranli ilova
Bosh sahifa, Ro'yxat, Profil. Pastki menyu (bottom navigation) — komponent: uchala ekranda bir xil, bir joydan o'zgaradi.

## Ko'p uchraydigan xatolar
- Instance'ni "Detach" qilib yuborish — bog'lanish uziladi, yangilanmaydi.
- Asosiy komponentni ekran ichida qoldirib, o'chirib yuborish. Komponentlarni alohida "Components" sahifasida saqlang.
- Har bir rangni qo'lda HEX bilan yozish — keyin o'zgartirish qiyin.

## Chuqurroq
- **Izchillik (consistency)** — foydalanuvchi bir xil elementni hamma joyda bir xil ko'radi va ishlatadi: bu ishonch beradi.
- Design system — komponentlar, uslublar va qoidalar to'plami (masalan, Material Design).

## O'zingizni tekshiring
1. Instance va Detach farqi nima?
2. Tugmaning "hover" holatini qanday saqlaysiz? (Variants)
3. Brend rangini bir joydan o'zgartirish uchun nima kerak? (Color style)
""",
    "ST13": """
## Mavzu nima haqida
Prototip — dizaynni "jonlantirish": tugmani bossangiz keyingi ekran ochiladi. Kod yozmasdan ilova qanday ishlashini ko'rsatish va tekshirish mumkin. Eksport esa dizayndan rasm/fayl olish.

## Asosiy tushunchalar
- **Prototype** rejimi (o'ng panel yuqorisida) — ekranlarni bog'lash.
- **Trigger:** On click (bosganda), On hover, After delay...
- **Action:** Navigate to (boshqa ekranga), Back (orqaga), Open overlay...
- **Animatsiya:** Instant (darhol), Dissolve (xiralashib), Smart animate (bir xil nomli qatlamlar silliq siljiydi).
- **Present (▶)** — prototipni ko'rish; telefonda Figma ilovasi yoki havola orqali.
- **Eksport formatlari:** PNG/JPG (rasm), SVG (vektor — sifatsiz kattalashadi), PDF (bir necha ekran bitta faylda). **@2x** — 2 baravar katta piksel (aniq ekranlar uchun).

## Bajarilgan misollar
### Misol 1. Login → Bosh sahifa
1. Prototype rejimi. Login ekranidagi "Kirish" tugmasini belgilang.
2. Paydo bo'lgan "+" doirachani Bosh sahifa frame'iga torting.
3. Interaction: On click → Navigate to → Bosh sahifa, Animation: Dissolve 300 ms.

### Misol 2. Orqaga qaytish
Bosh sahifadagi "←" ikonkasini → On click → **Back**. Foydalanuvchi har ekrandan qaytishi kerak.

### Misol 3. Smart animate
Ikki ekranda bir xil nomli "card" qatlami bor, lekin o'lchami har xil. Smart animate tanlasangiz, karta silliq kattalashadi.

### Misol 4. Eksport
Logo → o'ng panel Export → "+" → SVG. Ekran rasmini ijtimoiy tarmoq uchun → PNG @2x.

## Ko'p uchraydigan xatolar
- Ba'zi tugmalar bog'lanmagan — prototipda "o'lik" tugma chiqadi.
- Orqaga qaytish yo'q — foydalanuvchi "qamalib" qoladi.
- Logoni JPG qilish — fon oq bo'lib qoladi va kattalashtirganda xiralashadi.

## Chuqurroq
- **Flow starting point** — prototip qaysi ekrandan boshlanishi.
- **Overlay** — oyna ustida modal (masalan, "Tasdiqlaysizmi?").
- Foydalanuvchi testi: prototipni do'stingizga bering, hech narsa tushuntirmang — qayerda adashsa, o'sha joyni yaxshilang.

## O'zingizni tekshiring
1. Logo uchun qaysi format eng yaxshi? (SVG)
2. Bir xil nomli qatlamlarni silliq harakatlantiradigan animatsiya? (Smart animate)
3. Yaxshi prototipning 2 ta talabi?
""",
    "ST14": """
## Mavzu nima haqida
Terminal (buyruq satri) — kompyuterni sichqonchasiz, matnli buyruqlar bilan boshqarish. Dasturchilar har kuni ishlatadi: fayl yaratish, papkalar orasida yurish, dastur ishga tushirish.

## Asosiy tushunchalar
- `pwd` — hozir qaysi papkadasiz (print working directory).
- `ls` — papka ichidagi fayllar (Windows'da `dir`).
- `cd papka` — papkaga kirish; `cd ..` — bir daraja yuqoriga; `cd ~` — uy papkasiga.
- `mkdir nom` — yangi papka; `touch fayl.txt` — bo'sh fayl (Windows'da `type nul > fayl.txt`).
- `cp a b` — nusxalash; `mv a b` — ko'chirish yoki nomini o'zgartirish; `rm fayl` — o'chirish (**savatga tushmaydi!**).
- `cat fayl` — fayl ichini ekranga chiqarish; `clear` — ekranni tozalash.
- **Tab** — nomni avtomatik to'ldirish; **↑** — oldingi buyruqlar.

## Bajarilgan misollar
### Misol 1. Loyiha papkasi
```
mkdir loyiha
cd loyiha
mkdir rasmlar hujjatlar
touch README.txt
ls
```
Natija: `README.txt  hujjatlar  rasmlar`

### Misol 2. Fayl bilan ishlash
```
echo "Salom" > salom.txt
cat salom.txt
cp salom.txt nusxa.txt
mv nusxa.txt hujjatlar/
ls hujjatlar
```
`echo "Salom" > salom.txt` — faylga matn yozadi. Oxirida hujjatlar papkasida `nusxa.txt` bor.

### Misol 3. Yo'l (path)
`/home/ali/loyiha/rasmlar` — mutlaq yo'l (ildizdan). `rasmlar/logo.png` — nisbiy yo'l (hozirgi papkadan).
Agar `pwd` → `/home/ali/loyiha` bo'lsa, `cd ..` dan keyin `/home/ali`.

## Ko'p uchraydigan xatolar
- Bo'sh joyli nomlar: `cd Mening papkam` ishlamaydi → `cd "Mening papkam"`.
- `rm` bilan shoshilish — fayl qaytmaydi. Avval `ls` bilan tekshiring.
- Katta-kichik harf: Linux'da `Rasmlar` va `rasmlar` — ikki xil papka.

## Chuqurroq
- `rm -r papka` — papkani ichidagilari bilan o'chiradi (juda ehtiyot bo'ling).
- `ls -la` — yashirin fayllar va batafsil ma'lumot.
- `history` — hamma kiritilgan buyruqlar ro'yxati.
- Terminal Python, Git, serverlar bilan ishlashning asosi.

## O'zingizni tekshiring
1. Hozirgi papkani qaysi buyruq ko'rsatadi? (pwd)
2. `a.txt` ni `b.txt` deb qayta nomlash? (`mv a.txt b.txt`)
3. Nega `rm` xavfli?
""",
    "ST15": """
## Mavzu nima haqida
Scratch — bloklarni yig'ib dastur tuzish muhiti. Kod yozmasdan dasturlash mantiqini (algoritm, ketma-ketlik, hodisa) o'rganasiz. Bu darsda sprite, sahna, koordinatalar va asosiy bloklar.

## Asosiy tushunchalar
- **Algoritm** — masalani yechishning aniq, ketma-ket qadamlari.
- **Sprite** — sahnadagi qahramon/obyekt. **Kostyum** — sprite'ning tashqi ko'rinishi varianti (animatsiya uchun almashtiriladi).
- **Sahna (Stage)** — 480 × 360; markaz **x: 0, y: 0**. x o'ngga oshadi (−240...240), y yuqoriga oshadi (−180...180).
- **Bo'limlar:** Events (hodisalar — "yashil bayroq bosilganda"), Motion (harakat), Looks (ko'rinish, gapirish), Sound (ovoz), Control (takrorlash, shartlar).
- **Yo'nalish:** 90° — o'ngga, −90° — chapga, 0° — yuqoriga, 180° — pastga.

## Bajarilgan misollar
### Misol 1. Salomlashuvchi mushuk
```
yashil bayroq bosilganda
  x: 0 y: 0 ga bor
  "Salom!" ni 2 soniya ayt
  10 qadam yur
```
Mushuk markazdan "Salom!" deydi va biroz o'ngga siljiydi.

### Misol 2. Yurish animatsiyasi
```
yashil bayroq bosilganda
  10 marta takrorla
    10 qadam yur
    keyingi kostyum
    0.1 soniya kut
```
Kostyum almashgani uchun mushuk "yurayotgandek" ko'rinadi.

### Misol 3. "Choy damlash" algoritmi
1. Choynakka suv quyish. 2. Qaynatish. 3. Choynakka choy solish. 4. Qaynoq suv quyish. 5. 5 daqiqa kutish. 6. Piyolaga quyish.
Tartib buzilsa (avval piyolaga quyish) — natija noto'g'ri. Dasturda ham shunday.

### Misol 4. Koordinata masalasi
Sprite (100, 50) da. "x ni 30 ga o'zgartir" → (130, 50). "y ni −80 ga o'zgartir" → (130, −30).

## Ko'p uchraydigan xatolar
- Hodisa blokisiz yozish — dastur ishga tushmaydi.
- "Kut" bloksiz animatsiya — juda tez o'tib ketadi, ko'z ilg'amaydi.
- Boshlang'ich holatni belgilamaslik — har ishga tushirishda sprite boshqa joydan boshlaydi.

## Chuqurroq
- Har bir sprite'ning o'z skripti bor; bir nechta sprite parallel ishlaydi.
- **Broadcast (xabar yuborish)** — bir sprite boshqasiga "hozir boshla" deydi.
- Sahna (backdrop) almashtirish — o'yin bosqichlari uchun.

## O'zingizni tekshiring
1. Sahna markazining koordinatasi? (0, 0)
2. Sprite (0, 0) da, 90° yo'nalishda, 50 qadam yurdi. Yangi x? (50)
3. Kostyum nima uchun kerak?
""",
    "ST16": """
## Mavzu nima haqida
Shartlar va sikllar — har qanday o'yin va dasturning yuragi. Bu darsda "repeat", "forever", "if", o'zgaruvchilar va ular yordamida mini-o'yin (to'siqdan qochish) yasaymiz.

## Asosiy tushunchalar
- **repeat N** — ichidagi bloklarni N marta takrorlaydi.
- **forever** — dastur to'xtatilmaguncha takrorlaydi (o'yin sikli).
- **if … then** — shart rost bo'lsa bajariladi. **if … then … else** — rost/yolg'on uchun ikki yo'l.
- **Sensing (sezish):** "touching …?" (tegdimi), "key … pressed?" (tugma bosildimi).
- **O'zgaruvchi (Variable)** — qiymat saqlaydigan "quti": score, lives. "set … to" — qiymat beradi, "change … by" — oshiradi/kamaytiradi.

## Bajarilgan misollar
### Misol 1. Strelkalar bilan boshqarish
```
yashil bayroq bosilganda
  forever
    if <o'ng strelka bosilganmi?> then
      x ni 10 ga o'zgartir
    if <chap strelka bosilganmi?> then
      x ni -10 ga o'zgartir
```
Nega forever ichida? Tugma har lahzada tekshirilishi kerak.

### Misol 2. Ball yig'ish
```
yashil bayroq bosilganda
  score ni 0 ga o'rnat
  forever
    if <Yulduz ga tegyaptimi?> then
      score ni 1 ga o'zgartir
      Yulduz ni tasodifiy joyga ko'chir
```

### Misol 3. Hayotlar va Game Over
```
yashil bayroq bosilganda
  lives ni 3 ga o'rnat
  forever
    if <To'siq ga tegyaptimi?> then
      lives ni -1 ga o'zgartir
      1 soniya kut
    if <lives = 0> then
      "Game Over" ayt
      hammasini to'xtat
```
"1 soniya kut" bo'lmasa, bitta tegishda hayot bir necha marta birdan kamayadi (sikl soniyasiga ~30 marta aylanadi).

### Misol 4. repeat bilan kvadrat chizish (Pen)
```
4 marta takrorla
  100 qadam yur
  90 daraja buril
```

## Ko'p uchraydigan xatolar
- Shartni sikldan tashqarida bir marta tekshirish — o'yin "sezmaydi".
- O'zgaruvchini boshida qayta o'rnatmaslik — ikkinchi o'yinda ball eski qiymatdan boshlanadi.
- "change lives by 3" va "set lives to 3" ni adashtirish.

## Chuqurroq
- **repeat until <shart>** — shart rost bo'lguncha takrorlash.
- "Klonlar" (create clone) — bir xil to'siqlardan ko'p yaratish.
- O'yin dizayni: avval qoidalarni qog'ozga yozing (maqsad, yutish, yutqazish), keyin bloklarni yig'ing.

## O'zingizni tekshiring
1. "repeat 5" ichida "10 qadam yur". Sprite jami necha qadam yuradi? (50)
2. score = 4. "change score by 2" dan keyin? (6)
3. Nega to'qnashuvni "forever" ichida tekshirish kerak?
""",
    "ST17": """
## Mavzu nima haqida
Google Meet — video uchrashuvlar, Google Calendar — vaqtni rejalashtirish. Onlayn darslar, jamoaviy uchrashuvlar va eslatmalar uchun.

## Asosiy tushunchalar
- **Meet havolasi** — meet.google.com/abc-defg-hij. Taklif qilish = havolani yuborish.
- **Mikrofon odobi** — gapirmayotganda o'chiq (M tugmasi / Ctrl+D).
- **Raise hand** — gapirish navbatini so'rash. **Chat** — matnli xabar va havolalar.
- **Present now** — ekranni ulashish (butun ekran, oyna yoki tab).
- **Captions** — nutqni subtitr qilib ko'rsatish.
- **Calendar tadbiri:** nom, vaqt, takrorlanish (Weekly), mehmonlar (Add guests), eslatma (Notification), Meet havolasi.

## Bajarilgan misollar
### Misol 1. Takrorlanuvchi dars
1. Calendar → Create → "Python darsi".
2. Dush 15:00–16:30 → "Does not repeat" o'rniga "Custom": Dush, Chor, Juma.
3. "Add Google Meet video conferencing".
4. Notification: 30 daqiqa oldin.
5. Add guests: o'quvchilar emaillari → Save → "Send".

### Misol 2. Ekranni xavfsiz ulashish
Butun ekran o'rniga faqat kerakli **tab**ni ulashing: shaxsiy xabarlar, parollar ko'rinmaydi.

### Misol 3. Darsdan oldin tekshiruv ro'yxati
- Internet ishlayaptimi?
- Mikrofon va kamera (Meet'da "Check your audio and video").
- Quloqchin, jim joy, zaryadlangan qurilma.

## Ko'p uchraydigan xatolar
- Mikrofonni yoqiq qoldirish — shovqin hammani chalg'itadi.
- Butun ekranni ulashib, shaxsiy chatni ochib qo'yish.
- Vaqt zonasini noto'g'ri qo'yish — dars 1 soat farq bilan chiqadi.

## Chuqurroq
- Meet **breakout rooms** — guruhni kichik xonalarga bo'lish (ba'zi hisoblarda).
- Calendar'da "Find a time" — hammaga qulay vaqtni topish.
- Tadbir rangi — dars, uy vazifasi, shaxsiy ishlar ajralib turishi uchun.

## O'zingizni tekshiring
1. Haftada 3 marta takrorlanadigan darsni qanday yaratasiz?
2. Gapirish navbatini qanday so'raysiz? (Raise hand)
3. Ekran ulashishda nimaga e'tibor berish kerak?
""",
    "ST18": """
## Mavzu nima haqida
Onlayn xavfsizlik — hisoblaringiz, pulingiz va shaxsiy ma'lumotlaringizni himoya qilish. Eng ko'p uchraydigan xavflar: zaif parol, fishing va ehtiyotsizlik.

## Asosiy tushunchalar
- **Kuchli parol:** 12+ belgi, so'zlar birikmasi, raqam va belgi: `Tog'dagi-Olma-Daraxti!2026`. Har saytga **boshqa** parol.
- **2FA** — paroldan tashqari ikkinchi tasdiq (SMS kod, Google Authenticator). Parol o'g'irlansa ham hisob himoyalangan.
- **Parol menejeri** — murakkab parollarni xavfsiz saqlaydi (Google Password Manager, Bitwarden).
- **Fishing** — soxta xat/sayt orqali parol yoki karta raqamini so'rash. Belgilari: shoshiltirish, qo'rqitish, soxta manzil (`gooogle-login.com`).
- **Raqamli gigiyena:** kam ulashish, ilova ruxsatlarini tekshirish, yangilanishlarni o'rnatish.

## Bajarilgan misollar
### Misol 1. Parolni baholash
- `123456` — bir soniyada topiladi.
- `ali2010` — ism + yil, ijtimoiy tarmoqdan taxmin qilinadi.
- `Qizil-Choynak-Uchadi-77!` — uzun, eslab qolish oson, buzish juda qiyin. ✅

### Misol 2. Fishing xatni tahlil qilish
"Hurmatli mijoz! Kartangiz bloklandi. 24 soat ichida tasdiqlang: click-bank-uz.top"
1. Shoshiltiradi ✔ 2. Manzil rasmiy emas ✔ 3. Karta ma'lumotini so'raydi ✔ → **Fishing.** Havolani bosmang, bankning rasmiy ilovasiga o'zingiz kiring.

### Misol 3. SMS kod so'rashdi
"Bank xodimi" qo'ng'iroq qilib, SMS kodni so'rayapti → **Hech kimga aytmang.** Bank hech qachon kodni so'ramaydi. Qo'ng'iroqni tugating va bankning rasmiy raqamiga o'zingiz qo'ng'iroq qiling.

### Misol 4. Google hisobni tekshirish
myaccount.google.com → Security → **Security Checkup**: noma'lum qurilmalar, 2FA, parol holati.

## Ko'p uchraydigan xatolar
- Hamma joyda bitta parol — bitta sayt buzilsa, hammasi ochiladi.
- Ommaviy Wi-Fi'da bank ilovasiga kirish.
- Ilovalarga keraksiz ruxsat berish (fonarik ilovasi kontaktlarni so'raydi — nega?).
- Uy manzili, maktab, telefonni ochiq profilga yozish.

## Chuqurroq
- **HTTPS va qulf** belgisi aloqa shifrlanganini bildiradi, lekin saytning halolligini kafolatlamaydi — manzilni o'qing.
- haveibeenpwned.com — emailingiz ma'lumot sizib chiqishida bo'lganmi.
- Zaxira kodlar (backup codes) — telefon yo'qolsa 2FA'dan kirish uchun.

## O'zingizni tekshiring
1. Kuchli parolning 3 ta belgisini ayting.
2. 2FA qanday himoya qiladi?
3. "Hisobingiz bloklanadi" degan xat keldi. Nima qilasiz?
""",
    "ST19": """
## Mavzu nima haqida
Starter kursining yakuniy loyihasi — "Mening kichik biznesim / ijtimoiy loyiham". O'rgangan hamma vositani bitta real loyihada qo'llaysiz va himoya qilasiz.

## Asosiy tushunchalar
- **Canva** — logo va ijtimoiy tarmoq posti.
- **Figma** — 3 ekranli ilova prototipi.
- **Sheets** — xarajat va daromad jadvali + diagramma.
- **Slides** — 6–8 slaydli taqdimot.
- **Drive** — hamma fayl bitta papkada, ustozga Commenter huquqi bilan ulashilgan.
- **Scratch** — ixtiyoriy: reklama mini-animatsiyasi.
- **Himoya** — 4–5 daqiqa taqdimot + savollar.

## Bajarilgan misollar
### Misol 1. Loyiha g'oyasi: "Uyda pishirilgan pishiriqlar"
- Logo: "Shirin Uy", 3 rang (krem, jigarrang, pushti).
- Post: "Har shanba — yangi pishiriq! Buyurtma: @shirin_uy".
- Figma: Bosh sahifa (mahsulotlar), Mahsulot sahifasi, Buyurtma ekrani.
- Sheets: xarajat (un, shakar, qadoq) va daromad, foyda = daromad − xarajat.

### Misol 2. Foyda hisobi
Daromad: 30 ta tort × 50 000 = 1 500 000
Xarajat: `=SUM(B2:B6)` → 900 000
Foyda: `=B7-B8` → **600 000**
Diagramma: xarajat tarkibi (pie).

### Misol 3. Taqdimot tuzilmasi (7 slayd)
1. Titul 2. Muammo/ehtiyoj 3. Yechim (g'oya) 4. Brend (logo, post) 5. Ilova prototipi 6. Hisob-kitob (diagramma) 7. Xulosa va rahmat.

## Ko'p uchraydigan xatolar
- Fayllar turli joyda — ustoz topa olmaydi.
- Taqdimotda slayddagi matnni o'qish.
- Hisob-kitobni qo'lda yozish, formulasiz.
- Savollarga tayyorgarlik ko'rmaslik.

## Chuqurroq
- Baholashda eng ko'p ball — **vositalarni to'g'ri qo'llash** (50). Har birini kamida bir marta mazmunli ishlating.
- Himoyadan oldin 2 marta ovoz chiqarib mashq qiling, vaqtni o'lchang.
- Starter'dan keyin — **Python** kursi.

## O'zingizni tekshiring
1. Loyihada qaysi qism ixtiyoriy? (Scratch animatsiyasi)
2. Foyda qanday hisoblanadi?
3. Himoyaga qancha vaqt beriladi? (4–5 daqiqa + savollar)
""",
}
