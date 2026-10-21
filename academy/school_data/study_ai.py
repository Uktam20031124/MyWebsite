"""Minar AI Creator: mavzu materiallari (mavzu kaliti bo'yicha).

O'quvchi profilida "📘 Material" (quvvat bilan ochilgan mavzu) va testdan past natijada
"Mustahkamlash" sifatida ko'rinadi. Format — ``ui.study_md``:
## sarlavha, ### kichik sarlavha, - / 1. ro'yxat, > eslatma, ``` kod ```, `kod`, **qalin**.
"""

STUDY = {
    "AI01": """
## Mavzu nima haqida
Sun'iy intellekt (AI) — odatda inson aqlini talab qiladigan ishlarni bajaradigan kompyuter tizimlari: matnni tushunish, rasmni tanish, tarjima qilish, tavsiya berish. ChatGPT — matn bilan muloqot qiladigan AI yordamchi.

## Asosiy tushunchalar
- **AI** — o'rganadigan va qaror qabul qilishga yordam beradigan dasturlar oilasi.
- **Mashinali o'rganish** — kompyuter ko'p misollardan qonuniyatni o'zi topadi (masalan, minglab mushuk rasmidan “mushuk”ni tanishni o'rganadi).
- **Til modeli (LLM)** — juda ko'p matnlardan o'rgangan model. U “o'ylamaydi”, keyingi so'zlarni ehtimollik bo'yicha bashorat qiladi.
- **Prompt** — AI'ga beriladigan topshiriq yoki savol.
- **Kontekst** — suhbatdagi avvalgi xabarlar; AI keyingi javobda ularni hisobga oladi.

## Bajarilgan misollar
### Misol 1. Noaniq va aniq savol
- Noaniq: `Fotosintez` → AI uzun, umumiy matn beradi.
- Aniq: `5-sinf o'quvchisiga fotosintezni 3 ta qisqa gapda tushuntir` → qisqa, tushunarli javob.

### Misol 2. Kundalik hayotdagi AI
- Video platformadagi tavsiyalar, telefon yuz bilan ochilishi, ovozli yordamchi, avtomatik tarjimon — barchasi AI.
- Oddiy kalkulyator esa AI emas: u har doim bir xil qoida bilan ishlaydi.

### Misol 3. Intervyu tayyorlash
`Sen kasblar bo'yicha maslahatchisan. “Kelajakda AI kasblari” mavzusida 12 yoshli o'quvchi uchun 5 ta intervyu savoli tuz.`
Keyin har bir savolga AI javobini o'qib, yoniga o'z fikringizni 1–2 gapda yozing.

## Ko'p uchraydigan xatolar
- AI javobini tekshirmasdan haqiqat deb qabul qilish.
- Bir so'zli, noaniq savol berish.
- AI'ni “hamma narsani biladigan inson” deb o'ylash — u xato qilishi mumkin.

## Chuqurroq
> AI — yordamchi. G'oya va qoralama beradi, lekin fikrlash, tekshirish va yakuniy qaror sizda.

## O'zingizni tekshiring
1. AI va oddiy dastur (kalkulyator) farqi nimada?
2. Til modeli javobni qanday tuzadi?
3. “Aniq savol”ga o'zingiz 2 ta misol yozing.
""",
    "AI02": """
## Mavzu nima haqida
AI juda foydali, lekin xato qiladi, ba'zan esa faktlarni “to'qib chiqaradi”. Bu darsda AI javobini tekshirish, plagiatdan saqlanish va shaxsiy ma'lumotni himoya qilishni o'rganamiz.

## Asosiy tushunchalar
- **Hallucination** — AI ishonch bilan noto'g'ri yoki mavjud bo'lmagan ma'lumot berishi.
- **Manba** — ma'lumot olingan joy: rasmiy sayt, darslik, ilmiy maqola.
- **Ikki manba qoidasi** — muhim faktni kamida 2 ta ishonchli manbada tekshiring.
- **Plagiat** — birovning ishini o'zingizniki qilib ko'rsatish.
- **Shaxsiy ma'lumot** — parol, karta, pasport, uy manzili, telefon raqami: AI'ga **berilmaydi**.

## Bajarilgan misollar
### Misol 1. Faktni tekshirish
AI: “Eyfel minorasi 1999-yilda qurilgan.” → Rasmiy saytda: 1889-yil. Demak, AI xato qildi.

### Misol 2. To'g'ri foydalanish
AI yozgan matnni o'qing, faktlarini tekshiring, o'z so'zlaringiz bilan qayta yozing va “AI yordamida tayyorlandi” deb belgilang.

### Misol 3. “Berish mumkin / mumkin emas”
- Mumkin: “Quyosh tizimidagi sayyoralar ro'yxati”, o'zingiz yozgan hikoya (ismsiz, manzilsiz).
- Mumkin emas: parol, karta raqami, uy manzili, do'stingizning rasmi (ruxsatsiz).

## Ko'p uchraydigan xatolar
- Bitta savolni AI'ga qayta berib, “tekshirdim” deb o'ylash.
- AI matnini o'zgartirmasdan topshirish.
- Raqam va sanalarni tekshirmaslik — AI ularda ko'p adashadi.

## Chuqurroq
> “AI javob berdi” degani “bu haqiqat” degani emas.

Copilot javobidagi havolalarni oching: ba'zan manba javobdagi gapni umuman aytmaydi.

## O'zingizni tekshiring
1. Hallucination nima? Misol keltiring.
2. AI'ga qaysi 4 xil ma'lumotni bermaslik kerak?
3. AI matnidan halol foydalanishning 3 qadamini ayting.
""",
    "AI03": """
## Mavzu nima haqida
AI yordamida soxta video va ovoz (deepfake) yaratish, aldov xatlar (fishing) yozish oson bo'ldi. Bu darsda xavflarni tanish va o'zingizni himoya qilishni o'rganamiz.

## Asosiy tushunchalar
- **Deepfake** — AI bilan yaratilgan, haqiqiyga o'xshash soxta video, rasm yoki ovoz.
- **Fishing** — aldov xat yoki havola orqali parol va ma'lumotlarni o'g'irlash.
- **Ijtimoiy muhandislik** — odamni aldab, ishonchiga kirib, sir oldirish.
- **2FA** — paroldan tashqari ikkinchi tekshiruv (SMS yoki ilovadagi kod).
- **Etika** — boshqa odamning rasmi, ovozi va ma'lumotidan faqat ruxsat bilan foydalanish.

## Bajarilgan misollar
### Misol 1. Fishing xatini tanish
“Akkauntingiz bloklanadi! 24 soat ichida parolni shu havolada kiriting: g00gle-login.com”
Belgilar: shoshiltiradi, parol so'raydi, domen shubhali (`g00gle` — nol bilan). **Ochmang!**

### Misol 2. Deepfake belgilari
G'ayritabiiy ko'z qisish, lab harakati ovozga mos emas, yuz chetlari xira, yorug'lik notekis.

### Misol 3. Xavfsiz va xavfli prompt
- Xavfsiz: `Menga 10 yoshli bolalar uchun xavfsiz parol tuzish qoidalarini ayt.`
- Xavfli (bot so'rasa — bermang): `Ismingiz, maktabingiz va uy manzilingizni yozing.`

## Ko'p uchraydigan xatolar
- Qiziq havolani tekshirmasdan ochish.
- “Do'stim yubordi” deb ishonish — do'stning akkaunti buzilgan bo'lishi mumkin.
- Bitta parolni hamma joyda ishlatish.

## Chuqurroq
Kuchli parol: uzun (12+ belgi), harf, raqam va belgi aralash, masalan `Kitob7!Daryo#Oy`. Har bir sayt uchun alohida parol va 2FA.

## O'zingizni tekshiring
1. Fishing xatining 3 ta belgisini ayting.
2. Deepfake'ni qanday tanish mumkin?
3. Bot karta raqamini so'rasa, nima qilasiz?
""",
    "AI04": """
## Mavzu nima haqida
Prompt — AI'ga beriladigan topshiriq. Prompt qanchalik aniq bo'lsa, natija shunchalik yaxshi. Bu darsda prompt formulasini o'rganamiz.

## Asosiy tushunchalar
- **Rol** — AI kim sifatida javob beradi: “Sen bolalar yozuvchisisan”.
- **Vazifa** — nima qilish kerak: “hikoya yoz”.
- **Kontekst** — kim uchun, qanday vaziyatda: “9 yoshlilar uchun, do'stlik haqida”.
- **Cheklovlar** — uzunlik, format, uslub: “150 so'z, oxirida xulosa”.
- **Iteratsiya** — natijaga qarab promptni bosqichma-bosqich yaxshilash.

## Bajarilgan misollar
### Misol 1. Uch bosqich
1. Oddiy: `Hikoya yoz.`
2. Yaxshilangan: `Do'stlik haqida hikoya yoz.`
3. Mukammal: `Sen bolalar yozuvchisisan. 9 yoshli o'quvchilar uchun do'stlik haqida 150 so'zli hikoya yoz. Oddiy so'zlar ishlat, oxirida 1 gapli xulosa bo'lsin.`

### Misol 2. Formatni so'rash
`Sen matematika ustozisan. Kasrlarni qo'shishni 3 qadamli ro'yxat va 1 ta misol bilan tushuntir.`

### Misol 3. Iteratsiya
Javob uzun chiqdi → `Javobni 2 baravar qisqartir va 2-qadamni misol bilan tushuntir.`

## Ko'p uchraydigan xatolar
- Kontekst bermaslik: AI kimga yozayotganini bilmaydi.
- Bitta promptda 5 xil vazifa so'rash.
- Natijani tekshirmasdan qabul qilish.

## Chuqurroq
> Formula: **Rol + Vazifa + Kontekst + Cheklovlar (+ format)**.

Namuna berish (“mana shunday uslubda”) — eng kuchli usullardan biri.

## O'zingizni tekshiring
1. Promptning 4 qismini ayting va har biriga misol keltiring.
2. “Rasm haqida yoz” promptini mukammal qiling.
3. Birinchi javob yoqmasa, nima qilasiz?
""",
    "AI05": """
## Mavzu nima haqida
Prompt Battle — bir xil vazifaga turli promptlar yozib, qaysi biri eng yaxshi natija berishini aniqlaydigan musobaqa. Bu tajriba orqali qaysi so'zlar natijaga ta'sir qilishini ko'rasiz.

## Asosiy tushunchalar
- **Baholash mezonlari** — g'olibni aniqlash uchun oldindan kelishilgan qoidalar: aniqlik, ijodkorlik, auditoriyaga moslik, uzunlik.
- **Auditoriya** — matn kim uchun yozilmoqda.
- **Ohang (tone)** — rasmiy, quvnoq, jiddiy.
- **Harakatga chaqiriq (CTA)** — “Bugun ro'yxatdan o'ting!”

## Bajarilgan misollar
### Misol 1. Maktab tadbiri reklamasi
- Zaif: `Tadbir haqida reklama yoz.`
- Kuchli: `Sen marketologsan. 12–15 yoshli o'quvchilar uchun “Ilm-fan kuni” tadbiriga 40 so'zli quvnoq reklama yoz. Sana: 20-noyabr. Oxirida harakatga chaqiriq bo'lsin.`

### Misol 2. Cheklov raundi
Xuddi shu vazifa, lekin `20 so'zdan oshmasin` → AI faqat eng muhim ma'lumotni qoldiradi.

### Misol 3. Fikr bildirish
Yomon: `Yomon.` Yaxshi: `Ohangni quvnoqroq qil, sanani boshiga ko'chir, 2-gapni qisqartir.`

## Ko'p uchraydigan xatolar
- Mezonlarsiz baholash — g'olib tasodifiy bo'ladi.
- Bir xil promptni o'zgartirmay qayta-qayta yuborish.
- Boshqa jamoaning promptini o'zinikidek ko'rsatish.

## Chuqurroq
AI javoblarida tasodifiylik bor: bir xil prompt ikki marta biroz farqli javob beradi. Shuning uchun natijani bir necha marta sinab ko'ring.

## O'zingizni tekshiring
1. Reklama promptiga qaysi 3 narsani qo'shish kerak?
2. Cheklov natijaga qanday ta'sir qiladi?
3. Musobaqadan keyin nimani yozib qo'yish foydali?
""",
    "AI06": """
## Mavzu nima haqida
Murakkab vazifalar uchun ikki kuchli usul bor: **few-shot** (namuna berish) va **Chain-of-Thought** (bosqichma-bosqich fikrlash). Groq — modellarni juda tez ishlatadigan platforma, tajriba uchun qulay.

## Asosiy tushunchalar
- **Zero-shot** — namunasiz, faqat vazifa.
- **Few-shot** — vazifadan oldin 2–3 ta tayyor namuna.
- **Chain-of-Thought (CoT)** — “bosqichma-bosqich o'ylab, keyin javob ber”.
- **Kontekst oynasi** — model bir vaqtda ko'ra oladigan matn hajmi.

## Bajarilgan misollar
### Misol 1. Few-shot
```
Kayfiyatni aniqla.
"Zo'r kun!" -> ijobiy
"Yomg'ir, zerikarli" -> salbiy
"Kino ajoyib edi" -> ?
```
AI: `ijobiy` — namunalardan qolipni o'rgandi.

### Misol 2. Chain-of-Thought
Masala: “Do'konda 3 ta daftar 6000 so'm. 7 ta daftar necha so'm?”
Prompt: `Bosqichma-bosqich yech.` → 1) 1 ta daftar = 6000 ÷ 3 = 2000 so'm. 2) 7 × 2000 = **14 000 so'm**.

### Misol 3. Tuzoqli masala
“3 ta olma 3 daqiqada yeyilsa (har kishi bittadan), 100 ta olma 100 kishi bilan qancha vaqtda yeyiladi?” CoT bilan: har kishi 1 olmani 3 daqiqada yeydi → javob **3 daqiqa**, 100 emas.

## Ko'p uchraydigan xatolar
- CoT javobini tekshirmaslik: bitta bosqichdagi xato yakuniy javobni buzadi.
- Few-shot namunalarini har xil formatda berish.

## Chuqurroq
> Murakkab vazifani kichik qismlarga bo'ling va har birini alohida so'rang.

## O'zingizni tekshiring
1. Few-shot va zero-shot farqi nima?
2. CoT qaysi vazifalarda foydali?
3. O'zingiz few-shot prompt yozing (3 ta namuna bilan).
""",
    "AI07": """
## Mavzu nima haqida
NotebookLM — siz yuklagan hujjatlar (PDF, darslik, maqola) asosida ishlaydigan AI. U konspekt, savollar va audio-xulosa tayyorlaydi va javob hujjatning qaysi joyidan olinganini ko'rsatadi.

## Asosiy tushunchalar
- **Manbaga asoslangan AI** — javoblar faqat yuklangan hujjatlardan olinadi.
- **Iqtibos (citation)** — javob manbaning qaysi joyidan olinganini ko'rsatadi.
- **Konspekt** — asosiy fikrlarning qisqa, tartibli yozuvi.
- **Glossariy** — yangi atamalar va ularning ma'nosi.

## Bajarilgan misollar
### Misol 1. Bobdan konspekt
Prompt: `Shu bobning 5 ta asosiy fikrini 1 gapdan yoz va har biriga sahifa raqamini ko'rsat.`

### Misol 2. Test tuzish
`Shu bob bo'yicha 5 ta test savoli tuz: 4 ta variant, to'g'ri javob alohida.` Keyin har bir javobni kitobdan tekshiring.

### Misol 3. O'zini tekshirish
AI savollariga avval **o'zingiz** javob bering, keyin AI javobi bilan solishtiring — shunda bilim mustahkamlanadi.

## Ko'p uchraydigan xatolar
- Shaxsiy hujjatlarni (pasport, parollar) yuklash.
- Faqat AI xulosasini o'qib, kitobni ochmaslik.
- Avtomatik testni tekshirmasdan ishlatish.

## Chuqurroq
Audio-xulosa (podkast) materialni yo'lda tinglab takrorlashga yordam beradi. Konspektni o'z so'zlaringiz bilan qayta yozish — eslab qolishning eng yaxshi usuli.

## O'zingizni tekshiring
1. NotebookLM oddiy chatbotdan nimasi bilan farq qiladi?
2. Iqtibos nima uchun kerak?
3. AI tuzgan testni qanday tekshirasiz?
""",
    "AI08": """
## Mavzu nima haqida
Perplexity AI internetdan qidiradi va javobga manba havolalarini qo'shadi. Bu research (izlanish) va fact-check (faktni tekshirish) uchun qulay vosita.

## Asosiy tushunchalar
- **Research tartibi**: savol → manbalar → tekshirish → xulosa.
- **Fact-check** — faktni ishonchli manbalar orqali tekshirish.
- **Ishonchli manba**: rasmiy tashkilot, ilmiy jurnal, aniq muallif va sana.
- **Ikki manba qoidasi** — muhim faktni 2 ta mustaqil manbada tasdiqlash.

## Bajarilgan misollar
### Misol 1. Yaxshi research savoli
`Quyosh tizimida nechta sayyora bor va Pluton nega sayyora hisoblanmaydi? Manbalar bilan.`
Javob: 8 ta sayyora; Pluton 2006-yilda “mitti sayyora” deb tasniflangan. Manbalarni ochib tekshiring (masalan, NASA).

### Misol 2. Ziddiyatli manbalar
Ikki sayt turli raqam bersa → uchinchi ishonchli manbani toping va sanasini solishtiring.

### Misol 3. Feyk yangilikni tanish
Hayajonli sarlavha, manba yo'q, boshqa saytlarda tasdig'i yo'q → ishonmang.

## Ko'p uchraydigan xatolar
- Havolalarni ochmasdan “manba bor” deb ishonish.
- Eski ma'lumotdan foydalanish (sanaga qaramaslik).
- Xulosani manbadan to'liq ko'chirish.

## Chuqurroq
> Xulosani o'z so'zlaringiz bilan yozing va oxirida manbalar ro'yxatini bering.

## O'zingizni tekshiring
1. Research'ning 4 bosqichini ayting.
2. Manba ishonchliligini qanday baholaysiz?
3. Ikki manba bir-biriga zid bo'lsa nima qilasiz?
""",
    "AI09": """
## Mavzu nima haqida
Gamma App matndan avtomatik taqdimot, hujjat yoki veb-sahifa yaratadi. AI qoralama beradi — siz uni tahrirlab, mukammal qilasiz.

## Asosiy tushunchalar
- **1 slayd — 1 fikr**: kam matn, ko'proq vizual.
- **Tuzilma**: sarlavha → asosiy fikrlar → xulosa.
- **Kontrast** — matn fonda yaxshi o'qilishi.
- **Pitch** — g'oyani qisqa va ishonarli taqdim qilish.

## Bajarilgan misollar
### Misol 1. Prompt
`“Shaxmat — mening sevimli mashg'ulotim” mavzusida 5 slaydli taqdimot: 1-sarlavha, 2–4 asosiy fikrlar (har biri 3 ta qisqa band), 5-xulosa. Ohang — quvnoq, auditoriya — sinfdoshlar.`

### Misol 2. Tahrirlash
AI slaydiga 8 qator matn yozdi → 3 ta kalit so'zga qisqartiring va mos rasm qo'shing.

### Misol 3. 30 soniyalik pitch
“Shaxmat fikrlashni o'rgatadi. Men 3 yildan beri o'ynayman. Taqdimotda — boshlash uchun 3 maslahat.”

## Ko'p uchraydigan xatolar
- Slaydni matnga to'ldirish.
- Slayddagi matnni so'zma-so'z o'qish.
- Fon va matn rangi bir-biriga yaqin.

## Chuqurroq
> AI taqdimotidagi faktlarni ham tekshiring — AI xato qilishi mumkin.

## O'zingizni tekshiring
1. Yaxshi slaydning asosiy qoidasi qaysi?
2. 5 slaydli taqdimot rejasini ayting.
3. Nima uchun AI qoralamasini qo'lda tahrirlash kerak?
""",
    "AI10": """
## Mavzu nima haqida
AI rasm generatori matnli tavsifdan (prompt) yangi rasm yaratadi. Midjourney — sifatli, badiiy rasmlar uchun mashhur vosita.

## Asosiy tushunchalar
- **Rasm prompti tuzilmasi**: obyekt + harakat + muhit + uslub + yorug'lik + kamera burchagi + parametrlar.
- **Uslub**: akvarel, piksel-art, kiberpank, 3D, multfilm.
- **Yorug'lik**: “quyosh botishidagi iliq yorug'lik”, “neon yorug'lik”.
- **Kompozitsiya**: obyektlarning joylashuvi va kamera burchagi (tepadan, yaqin plan).
- **--ar** — tomonlar nisbati (16:9 — keng, 1:1 — kvadrat, 9:16 — tik).

## Bajarilgan misollar
### Misol 1. Bosqichma-bosqich
1. `kelajak shahri`
2. `kelajak shahri, uchuvchi mashinalar, osmono'par binolar`
3. `kelajak shahri, uchuvchi mashinalar, yashil bog'li osmono'par binolar, kiberpank uslubi, kechki neon yorug'lik, tepadan ko'rinish --ar 16:9`

### Misol 2. Uch xil uslub
Bitta g'oya: akvarel, piksel-art, 3D render — natijalarni solishtiring.

## Ko'p uchraydigan xatolar
- Bir so'zli prompt — natija tasodifiy.
- Mashhur rassom asarini yoki brend logotipini nusxalash.
- Rasmdagi xatolarni (barmoqlar, matn) e'tiborsiz qoldirish.

## Chuqurroq
> Iteratsiya: har safar promptga bitta aniqlik qo'shing va natijani solishtiring.

## O'zingizni tekshiring
1. Rasm promptining 5 ta qismini ayting.
2. --ar 16:9 qaysi format uchun mos?
3. “Mushuk” promptini mukammal qiling.
""",
    "AI11": """
## Mavzu nima haqida
O'yin qahramoni dizayni: g'oya → konsept-art → variantlar → izchil qiyofa. Leonardo AI'da Image-to-Image yordamida bir qahramonni turli pozalarda olish mumkin.

## Asosiy tushunchalar
- **Konsept-art** — qahramonning dastlabki vizual g'oyasi.
- **Izchillik** — barcha rasmlarda qahramon bir xil: yuz, kiyim, ranglar.
- **Image-to-Image** — mavjud rasmni asos qilib, yangi variant yaratish.
- **Negative prompt** — rasmda bo'lmasligi kerak narsalar: “xira, ortiqcha barmoqlar”.
- **Turnaround** — old, yon va orqa ko'rinish (3D uchun).

## Bajarilgan misollar
### Misol 1. Qahramon tavsifi
`Kosmik kashfiyotchi qiz, ko'k skafandr, yelkasida kichik robot, jasur va qiziquvchan, multfilm uslubi, toza fon.`

### Misol 2. Poza o'zgartirish
Eng yaxshi rasmni Image-to-Image'ga qo'ying: `xuddi shu qahramon, yugurayotgan holatda`.

### Misol 3. Qahramon tarixi
“Lola — Mars stansiyasida tug'ilgan. Uning robot do'sti Bip yo'qolgan kemani qidirishga yordam beradi.”

## Ko'p uchraydigan xatolar
- Har rasmda qahramon boshqacha chiqishi (izchillik yo'q).
- Mashhur qahramonni aynan nusxalash — mualliflik huquqi buziladi.
- Xarakter va tarixsiz faqat rasm.

## Chuqurroq
> Yaxshi qahramon — esda qoladigan silueti, aniq xarakteri va o'ziga xos ranglari bor qahramon.

## O'zingizni tekshiring
1. Izchillik nima va u nega muhim?
2. Negative prompt'ga misol yozing.
3. O'z qahramoningiz tavsifini yozing.
""",
    "AI12": """
## Mavzu nima haqida
Brend — nom, logotip, ranglar va uslubdan iborat qiyofa. Ideogram AI rasm ichida matnni aniq yozadi — logotip va poster uchun qulay.

## Asosiy tushunchalar
- **Logotip qoidalari**: oddiy, esda qoladigan, kichik o'lchamda ham o'qiladi.
- **Rang palitrasi**: 2–3 ta asosiy rang.
- **Tipografika**: shrift tanlash va matnni chiroyli joylashtirish.
- **Ierarxiya**: eng muhim ma'lumot eng ko'zga tashlanadi.
- **UI / UX**: interfeys ko'rinishi / foydalanish qulayligi.

## Bajarilgan misollar
### Misol 1. Logotip prompti
`“Minar Kids” o'quv markazi uchun minimalistik logotip: minora shakli, ko'k va oltin ranglar, oq fon, matn aniq yozilsin.`

### Misol 2. Poster
`“Robototexnika kuni” posteri: katta sarlavha, robot rasmi, sana 25-noyabr, joy — Minar Academy, pastda “Ro'yxatdan o'ting!”`

### Misol 3. 5 soniya testi
Do'stingizga logotipni 5 soniya ko'rsating va nima eslab qolganini so'rang.

## Ko'p uchraydigan xatolar
- Logotipda juda ko'p mayda detal.
- 10 xil rang va 5 xil shrift.
- Boshqa brend logotipiga o'xshatish.

## Chuqurroq
> Kontrast: matn fondan yaqqol ajralib tursin.

## O'zingizni tekshiring
1. Yaxshi logotipning 3 xususiyati?
2. Posterdagi ierarxiya nima?
3. UI va UX farqi nima?
""",
    "AI13": """
## Mavzu nima haqida
AI matndan (Text-to-Video) yoki rasmdan (Image-to-Video) qisqa video yaratadi. Runway — shu ishni bajaradigan mashhur vosita.

## Asosiy tushunchalar
- **Video prompti**: sahna + harakat + kamera harakati + kayfiyat.
- **Kamera harakatlari**: zoom in (yaqinlashish), pan (gorizontal burilish), orbit (atrofida aylanish).
- **Loop** — oxiri boshiga uzluksiz ulanadigan video.
- AI videolar odatda **bir necha soniyalik** bo'ladi.

## Bajarilgan misollar
### Misol 1. Rasmdan video
Rasm: tog' ustidagi qal'a. Prompt: `kamera sekin yaqinlashadi, bulutlar suzadi, quyosh botishi, sirli kayfiyat`.

### Misol 2. Bitta aniq harakat
Yomon: `qush uchadi, yugaradi, suvga sho'ng'iydi, qo'shiq aytadi`.
Yaxshi: `ko'k qush qanot qoqib shoxdan uchadi, kamera uni kuzatadi`.

## Ko'p uchraydigan xatolar
- Qisqa videoda juda ko'p harakat so'rash.
- Kamera harakatini yozmaslik — video “qotib” qoladi.
- Haqiqiy odamlarning soxta videosini yaratish — etikaga zid.

## Chuqurroq
> Bir nechta variant yarating va eng tabiiysini tanlang: AI videoda obyekt shakli kadrdan kadrga o'zgarishi mumkin.

## O'zingizni tekshiring
1. Text-to-Video va Image-to-Video farqi?
2. 3 ta kamera harakatini ayting.
3. 5 soniyalik video uchun prompt yozing.
""",
    "AI14": """
## Mavzu nima haqida
Kinematografik mini-treyler: bir nechta AI kliplarni reja asosida yaratib, montajda birlashtirish. Luma Dream Machine — kino uslubidagi kliplar uchun vosita.

## Asosiy tushunchalar
- **Storyboard** — sahnalarning ketma-ket rejasi.
- **Treyler tuzilmasi**: qiziqtiruvchi boshlanish → asosiy sahnalar → sarlavha.
- **Montaj** — kliplarni bitta videoga birlashtirish (masalan, CapCut).
- **O'tish (transition)** — sahnalar orasidagi ravon effekt.

## Bajarilgan misollar
### Misol 1. Storyboard (3 sahna)
1. Tungi o'rmon, tuman, kamera sekin oldinga — sirli boshlanish.
2. Yorug' darvoza ochiladi, qahramon ichkariga kiradi — orbit kamera.
3. Sarlavha: “SIRLI DARVOZA” — qora fon, oltin harflar.

### Misol 2. Izchillik
Har sahnada qahramonni bir xil tasvirlang: “ko'k plashli qiz, qo'lida fonar”.

## Ko'p uchraydigan xatolar
- Storyboardsiz boshlash — vaqt behuda ketadi.
- Har sahnada qahramon boshqacha.
- 2 daqiqalik treyler — juda uzun; 15–20 soniya yetarli.

## Chuqurroq
> Sahna kutilgandek chiqmasa, promptni aniqlashtirib yangi variant yarating.

## O'zingizni tekshiring
1. Storyboard nima uchun kerak?
2. Treyler tuzilmasini ayting.
3. 3 sahnali treyler rejasini yozing.
""",
    "AI15": """
## Mavzu nima haqida
ElevenLabs matnni tabiiy ovoz bilan o'qib beradi (Text-to-Speech). Ovozlashtirish (voice-over) videolarni jonlantiradi. Ovoz klonlash esa faqat ruxsat bilan mumkin.

## Asosiy tushunchalar
- **Text-to-Speech** — matnni sun'iy ovoz bilan o'qish.
- **Voice-over** — video ustidan diktor ovozi.
- **Voice cloning** — ovozni nusxalash: faqat o'z ovozingiz yoki aniq ruxsat bilan.
- **Tinish belgilari** — pauza va intonatsiyani boshqaradi.

## Bajarilgan misollar
### Misol 1. Matnni tayyorlash
Yomon: `bir kuni lola o'rmonga bordi va u yerda katta daraxt ko'rdi va u juda hayron qoldi`
Yaxshi: `Bir kuni Lola o'rmonga bordi. U yerda ulkan daraxt turardi... Lola hayron qoldi!`

### Misol 2. Qahramonlar ovozi
Hikoyachi — vazmin ovoz, Lola — quvnoq yosh ovoz, robot Bip — metall ohang.

## Ko'p uchraydigan xatolar
- Juda uzun gaplar — ovoz nafas olmaydigandek eshitiladi.
- Natijani tinglab tekshirmaslik — AI ba'zi so'zlarni noto'g'ri talaffuz qiladi.
- Birovning ovozini ruxsatsiz klonlash.

## Chuqurroq
> AI ovoz bilan firibgarlik qo'ng'iroqlari ko'paymoqda: oilada “maxfiy so'z” kelishib qo'ying.

## O'zingizni tekshiring
1. Tinish belgilari ovozga qanday ta'sir qiladi?
2. Ovoz klonlashning etik qoidasi?
3. Ovozlashtirish rejasining 4 qadamini ayting.
""",
    "AI16": """
## Mavzu nima haqida
Veb-sahifa uch qismdan iborat: **HTML** — tuzilma, **CSS** — ko'rinish, **JavaScript** — harakat. Replit — brauzerda kod yozib, darhol natijani ko'rish mumkin bo'lgan muhit, AI yordamchisi bilan.

## Asosiy tushunchalar
- `<h1>` — eng katta sarlavha, `<p>` — matn, `<img src="...">` — rasm, `<a href="...">` — havola.
- CSS: `color` — matn rangi, `font-size` — shrift o'lchami, `background` — fon.
- JS: tugma bosilganda nimadir bo'lishi.

## Bajarilgan misollar
### Misol 1. Oddiy vizitka
```
<h1>Salom, men Ali!</h1>
<p>Men robototexnika va o'yinlarni yaxshi ko'raman.</p>
<button onclick="alert('Rahmat!')">Bog'lanish</button>
```

### Misol 2. CSS
```
h1 { color: navy; text-align: center; }
button { background: teal; color: white; padding: 10px 20px; }
```

### Misol 3. AI'dan so'rash
`HTML va CSS'da ko'k rangli, markazlashgan 'Salom' tugmasi bo'lgan sahifa yoz va har qismini izohla.`

## Ko'p uchraydigan xatolar
- AI kodini tushunmasdan nusxalash.
- Tegni yopishni unutish: `<p>` ... `</p>`.
- O'zgarishdan keyin natijani tekshirmaslik.

## Chuqurroq
> AI'dan har qatorni tushuntirishni so'rang va kamida 2 ta o'zgarishni o'zingiz kiriting.

## O'zingizni tekshiring
1. HTML, CSS va JS vazifalari nima?
2. Rasm qaysi teg bilan qo'shiladi?
3. Matn rangini CSS'da qanday o'zgartirasiz?
""",
    "AI17": """
## Mavzu nima haqida
v0.dev prompt asosida tayyor interfeys (UI) yaratadi. Birinchi mini ilova: Kalkulyator yoki To-do list.

## Asosiy tushunchalar
- **Komponent** — qayta ishlatiladigan qism: tugma, karta, forma.
- **Holat (state)** — ilovaning hozirgi ma'lumoti (ro'yxatdagi vazifalar).
- **Foydalanuvchi oqimi** — maqsadga yetish qadamlari.
- **MVP** — eng oddiy ishlaydigan versiya.

## Bajarilgan misollar
### Misol 1. To-do list prompti
`To-do list ilovasi: yuqorida kiritish maydoni va "Qo'shish" tugmasi; ro'yxatda har bir vazifa yonida belgilash va o'chirish tugmasi; ro'yxat bo'sh bo'lsa "Hali vazifa yo'q" yozuvi; zamonaviy, toza dizayn.`

### Misol 2. Takomillashtirish
`Tugmalarni kattalashtir va tungi rejim qo'sh.`

### Misol 3. Sinov
Kalkulyatorda: `2 + 2 = 4`, `10 / 4 = 2.5`, `7 × 0 = 0` — natijalarni tekshiring.

## Ko'p uchraydigan xatolar
- “Yaxshiroq qil” kabi noaniq so'rov.
- Ilovani sinamasdan ko'rsatish.
- Birdaniga 20 ta funksiya qo'shishga urinish.

## Chuqurroq
> Avval asosiy funksiya ishlasin, keyin bitta qo'shimcha imkoniyat.

## O'zingizni tekshiring
1. Komponent nima?
2. To-do list'ning 3 asosiy funksiyasi?
3. Bo'sh ro'yxat holatida nima ko'rsatish kerak?
""",
    "AI18": """
## Mavzu nima haqida
Debugging — xatolarni topish va tuzatish. Cursor — ichiga AI o'rnatilgan kod muharriri: xatoni tushuntiradi va tuzatishni taklif qiladi.

## Asosiy tushunchalar
- **Sintaksis xatosi** — til qoidasi buzilgan: dastur umuman ishlamaydi.
- **Mantiqiy xato** — dastur ishlaydi, lekin natija noto'g'ri.
- **Xato xabari** — xato turi va qator raqamini ko'rsatadi.
- **Refaktoring** — ishlashini o'zgartirmasdan kodni tartibli qilish.

## Bajarilgan misollar
### Misol 1. Sintaksis xatosi
```
print("Salom"
```
Xato: qavs yopilmagan → `print("Salom")`.

### Misol 2. Mantiqiy xato
```
narx = 5000
soni = 3
jami = narx + soni
print(jami)
```
Natija: `5003` — noto'g'ri. To'g'risi: `jami = narx * soni` → `15000`.

### Misol 3. AI'dan so'rash
`Mana kod va xato xabari. Xato nima uchun chiqyapti? Tuzatishni va sababini tushuntir.`

## Ko'p uchraydigan xatolar
- Xato xabarini o'qimaslik.
- AI tuzatishini tekshirmasdan qabul qilish.
- O'zgaruvchilarga `a`, `x` kabi tushunarsiz nom berish (`total_score` yaxshiroq).

## Chuqurroq
> Muammoni kichik qismlarga bo'ling va har birini alohida tekshiring.

## O'zingizni tekshiring
1. Sintaksis va mantiqiy xato farqi?
2. Xato xabaridan qanday foydalanasiz?
3. Refaktoring nima?
""",
    "AI19": """
## Mavzu nima haqida
AI qanday ishlaydi: model ma'lumotlardan o'rgatiladi, dasturlar esa unga **API** orqali so'rov yuborib javob oladi. Hugging Face — ochiq modellar va demo ilovalar (Spaces) platformasi.

## Asosiy tushunchalar
- **Model** — ma'lumotlardan o'rgatilgan, bashorat qila oladigan dastur.
- **API** — dasturlar ma'lumot almashadigan “eshik”.
- **Request → Response** — so'rov yuboriladi, javob olinadi.
- **JSON** — “kalit: qiymat” formati.
- **API kaliti** — maxfiy “parol”: hech kimga berilmaydi.

## Bajarilgan misollar
### Misol 1. JSON o'qish
```
{"ism": "Ali", "yosh": 12, "fanlar": ["matematika", "ingliz tili"]}
```
`yosh` → `12`, `fanlar` → ro'yxat (kvadrat qavsda).

### Misol 2. API javobi
Rasm tanish modeli: so'rov — rasm; javob — `{"label": "mushuk", "score": 0.97}` (97% ishonch).

### Misol 3. Model sinovi yozuvi
Har bir model uchun yozing:
- Vazifa: rasmdagi hayvonni tanish.
- Kirish: it rasmi.
- Natija: `{"label": "it", "score": 0.91}`.
- Xato bo'ldimi: bo'rini ham “it” dedi.

## Ko'p uchraydigan xatolar
- API kalitini kodga yoki chatga yozib qo'yish.
- Model natijasini tekshirmasdan ishonish.
- JSON'da qavslarni chalkashtirish.

## Chuqurroq
> Xato kodi kelsa — xabarni o'qing: ko'pincha kalit yoki format noto'g'ri bo'ladi.

## O'zingizni tekshiring
1. API nima? O'z so'zlaringiz bilan.
2. JSON'da ro'yxat qanday yoziladi?
3. API kalitini qayerda saqlash kerak?
""",
    "AI20": """
## Mavzu nima haqida
Make.com — kod yozmasdan avtomatlashtirish platformasi. Modullarni ulab, masalan, Telegram botga AI javob beradigan sxema yaratish mumkin.

## Asosiy tushunchalar
- **Scenario** — ulangan modullardan iborat sxema.
- **Trigger** — sxemani ishga tushiradigan hodisa (botga yangi xabar).
- **Modul** — bitta qadam (AI javob yaratish, xabar yuborish).
- **Ma'lumot oqimi** — ma'lumot moduldan modulga o'tishi.

## Bajarilgan misollar
### Misol 1. Bot sxemasi
`Telegram: yangi xabar` → `AI: javob yarat (“Sen 10 yoshli bolalar uchun yordamchisan. Faqat fan haqida javob ber.”)` → `Telegram: javob yuborish`.

### Misol 2. Kunlik avtomatlashtirish
`Har kuni 08:00` → `Ob-havo` → `Telegram'ga xabar`.

### Misol 3. Xatoni topish
Sxema ishlamasa — har modulning tarixini (log) oching: qaysi qadam qizil bo'lsa, xato o'sha yerda.

## Ko'p uchraydigan xatolar
- API kalitini bot tavsifida yoki chatda ochiq qoldirish.
- Botga cheklov qo'ymaslik — u har qanday savolga javob beradi.
- Sxemani sinamasdan ishga tushirish.

## Chuqurroq
> Avtomatlashtirish vaqtni tejaydi va takroriy ishdagi xatolarni kamaytiradi.

## O'zingizni tekshiring
1. Trigger nima? Misol keltiring.
2. Bot uchun qanday cheklovlar kerak?
3. Sxema ishlamasa nima qilasiz?
""",
    "AI21": """
## Mavzu nima haqida
Deployment — ilovani internetga joylab, havola orqali hammaga ochish. Netlify Drop'da sayt papkasini sudrab tashlashning o'zi yetarli.

## Asosiy tushunchalar
- **Hosting** — sayt fayllari saqlanadigan server.
- **Domen** — sayt manzili.
- **Statik sayt** — faqat HTML, CSS, JS fayllar.
- **index.html** — saytning asosiy fayli (papka ildizida bo'lishi shart).
- **HTTPS** — xavfsiz, shifrlangan ulanish.

## Bajarilgan misollar
### Misol 1. Papka tuzilmasi
```
mening-saytim/
  index.html
  style.css
  rasm.png
```
Papkani app.netlify.com/drop sahifasiga tashlang → bir necha soniyada havola tayyor.

### Misol 2. Yangilash
Faylni o'zgartirdingiz → papkani qayta joylang (redeploy) → telefonda tekshiring.

## Ko'p uchraydigan xatolar
- `index.html` ichki papkada qolishi — sayt ochilmaydi.
- Kodda parol yoki API kaliti qoldirish.
- Telefonda tekshirmaslik.

## Chuqurroq
> Ommaviy havolani joylashdan oldin saytda shaxsiy ma'lumot yo'qligiga ishonch hosil qiling.

## O'zingizni tekshiring
1. Hosting va domen farqi?
2. Sayt ochilmasa birinchi nimani tekshirasiz?
3. Joylashdan oldin koddan nimani olib tashlash kerak?
""",
    "AI22": """
## Mavzu nima haqida
Final loyiha boshlanadi: g'oya tanlash va tuzilmani loyihalash. Whimsical AI mindmap va blok-sxemalarni tez chizadi.

## Asosiy tushunchalar
- **Loyiha formulasi**: Muammo → Yechim → AI qayerda → Demo → Kelajak.
- **MVP** — asosiy muammoni hal qiladigan eng oddiy versiya.
- **Maqsadli foydalanuvchi** — loyiha kim uchun.
- **Mindmap** va **flowchart** — g'oya xaritasi va jarayon sxemasi.

## Bajarilgan misollar
### Misol 1. “AI Tutor”
- Muammo: o'quvchi uy vazifasidagi mavzuni tushunmaydi.
- Yechim: savolga o'quvchi darajasida tushuntiradigan yordamchi.
- AI: tushuntirish va misollar yaratish.
- MVP: 1 fan, 1 sahifa, savol-javob.
- Kelajak: ovozli javob, testlar.

### Misol 2. 3 ta asosiy funksiya
1. Savol kiritish. 2. Oddiy tushuntirish. 3. “Yana misol” tugmasi.

## Ko'p uchraydigan xatolar
- Juda katta g'oya — 2 haftada tugamaydi.
- Muammosiz loyiha — “nima uchun kerak?” savoliga javob yo'q.
- Barcha vaqtni dizaynga sarflash.

## Chuqurroq
> Elevator pitch: g'oyani 30 soniyada tushuntira olsangiz — u aniq.

## O'zingizni tekshiring
1. Loyiha formulasining 5 qismini ayting.
2. MVP nima?
3. O'z loyihangiz uchun 3 ta asosiy funksiyani yozing.
""",
    "AI23": """
## Mavzu nima haqida
Prototip — sinab ko'rish mumkin bo'lgan birinchi versiya. Uni sinfdoshlarda testlab, fikrlar asosida yaxshilaymiz. Suno AI loyiha uchun musiqa yaratadi.

## Asosiy tushunchalar
- **Prototip** — ishlaydigan dastlabki versiya.
- **Feedback** — foydalanuvchi fikri.
- **Bug list** — topilgan xatolar ro'yxati.
- **Sound-design** — loyiha tovush muhiti.
- **Musiqa prompti**: janr + temp + kayfiyat + cholg'u.

## Bajarilgan misollar
### Misol 1. Testlash
Sinfdoshingizga vazifa bering: “Bitta savol yozib, javob oling.” Gapirmasdan kuzating, qayerda qiynalganini yozing.

### Misol 2. Eng foydali savol
“Qayerda qiynaldingiz va nimani tushunmadingiz?”

### Misol 3. Musiqa prompti
`kosmik sarguzasht o'yini uchun fon musiqasi, elektron, o'rtacha temp, sirli va quvnoq, sintezator, so'zsiz`

## Ko'p uchraydigan xatolar
- Faqat o'zingiz sinash.
- Feedback bilan bahslashish.
- Musiqa juda baland va diqqatni chalg'itadi.

## Chuqurroq
> Platformaning foydalanish shartlarini o'qing: AI musiqasini qayerda ishlatish mumkinligi.

## O'zingizni tekshiring
1. Prototip va yakuniy mahsulot farqi?
2. Feedback'dan keyin nima qilasiz?
3. Loyihangiz uchun musiqa prompti yozing.
""",
    "AI24": """
## Mavzu nima haqida
Demo Day — loyihani hakamlar va ota-onalar oldida 3–5 daqiqada taqdim qilish. Bu kursning yakuniy bosqichi: loyiha, taqdimot, sertifikat.

## Asosiy tushunchalar
- **Taqdimot tuzilmasi**: Muammo → Yechim → AI → Jonli demo → Kelajak.
- **Jonli demo** — loyiha haqiqatan ishlashini ko'rsatish.
- **Zaxira** — demo ishlamasa video yoki skrinshotlar.
- **Portfolio** — barcha ishlaringiz to'plami.

## Bajarilgan misollar
### Misol 1. 3 daqiqalik pitch
1. (30 s) “Siz ham uy vazifasida qiynalganmisiz?” — muammo.
2. (30 s) “AI Tutor — savolingizga darajangizda tushuntiradi.” — yechim.
3. (30 s) “AI'dan tushuntirish va misollar uchun foydalandim.”
4. (60 s) Jonli demo.
5. (30 s) “Keyingi versiyada — ovozli javob.”

### Misol 2. Bilmagan savol
“Yaxshi savol! Buni keyingi versiyada o'rganib chiqaman.”

## Ko'p uchraydigan xatolar
- Slayddan o'qish va tinglovchilarga qaramaslik.
- Vaqtdan oshib ketish.
- Zaxirasiz jonli demo.

## Chuqurroq
> Shior: “AI bilan gaplashma — AI yordamida yarat.”

## O'zingizni tekshiring
1. Taqdimot tuzilmasining 5 qismi?
2. Demo ishlamasa nima qilasiz?
3. Portfolioga nimalarni qo'shasiz?
""",
}
