"""Minar AI Creator kursi mavzulari bo'yicha test savollari (har bir mavzuga 12 ta).

Format — mavzu testi formasidagi bilan bir xil:
"?" — savol, "+" — to'g'ri javob, "-" — noto'g'ri javob. Kalit — ``ai.py`` dagi mavzu kaliti.
Savollar vositalarning tez o'zgaradigan tafsilotlariga emas, asosiy tushunchalarga tayanadi.
"""

QUIZZES = {
    "AI01": """
? Sun'iy intellekt (AI) nima?
+ Odatda inson aqlini talab qiladigan vazifalarni bajaradigan kompyuter tizimlari
- Faqat robotlar ichidagi maxsus mikrosxema
- Internetdagi barcha saytlar yig'indisi
- Kompyuterning tezroq ishlashi uchun dastur

? ChatGPT qanday turdagi AI vositasi?
+ Matn bilan muloqot qiladigan til modeli (chatbot)
- Rasm chizadigan dastur
- Antivirus dasturi
- Video montaj dasturi

? Quyidagilardan qaysi biri kundalik hayotda AI ishlatilishiga misol?
+ Video platformalardagi “sizga yoqishi mumkin” tavsiyalari
- Oddiy kalkulyatorda 2 + 2 ni hisoblash
- Qog'ozga qalam bilan yozish
- Chiroqni kalit bilan yoqish

? Til modeli (LLM) javobni qanday tuzadi?
+ O'rgangan matnlari asosida keyingi so'zlarni ehtimollik bo'yicha bashorat qiladi
- Har bir savolga javobni internetdagi bitta saytdan nusxalaydi
- Javobni oldindan yozib qo'ygan odam yuboradi
- Javobni tasodifiy harflardan yig'adi

? “Prompt” nima?
+ AI'ga beriladigan topshiriq yoki savol matni
- AI'ning javobi
- Kompyuterning paroli
- AI'ni o'chirish tugmasi

? Qaysi savol ChatGPT'dan foydaliroq javob olishga yordam beradi?
+ “5-sinf o'quvchisiga fotosintezni 3 ta qisqa gapda tushuntir”
- “Fotosintez”
- “Biror narsa ayt”
- “?”

? Mashinali o'rganish (machine learning) nima?
+ Kompyuter ko'p misollardan qonuniyatlarni o'zi o'rganishi
- Kompyuterni mashinaga o'rnatish
- Kompyuterni qo'lda yig'ish
- Klaviaturada tez yozishni o'rganish

? AI javobi har doim to'g'ri bo'ladimi?
+ Yo'q, AI xato qilishi mumkin, muhim ma'lumotni tekshirish kerak
- Ha, AI hech qachon xato qilmaydi
- Faqat matematikada xato qiladi
- Faqat ingliz tilida to'g'ri javob beradi

? Chatbot bilan suhbatda keyingi savol berganda u nimani hisobga oladi?
+ Shu suhbatdagi avvalgi xabarlarni (kontekstni)
- Faqat oxirgi so'zni
- Kompyuteringizdagi barcha fayllarni
- Telefoningizdagi rasmlarni

? AI kasblar bilan bog'liq to'g'ri fikr qaysi?
+ AI ko'p ishlarni o'zgartiradi, AI bilan ishlay oladigan odamlarga talab ortadi
- AI tufayli hech kim ishlamay qo'yadi
- AI faqat o'yinlarda ishlatiladi
- AI kelajakda butunlay yo'qoladi

? Quyidagilardan qaysi biri AI emas, oddiy dastur?
+ Har doim bir xil qoida bo'yicha ishlaydigan oddiy kalkulyator
- Yuzni tanib telefonni ochish
- Ovozli yordamchi (masalan, “Hey Siri”)
- Avtomatik tarjimon

? AI bilan ishlashda eng to'g'ri munosabat qaysi?
+ AI — yordamchi: g'oya beradi, lekin fikrlash va tekshirish o'quvchining o'zida
- AI hamma uy vazifasini o'zi bajarishi kerak
- AI javobini hech o'qimasdan topshirish mumkin
- AI'ga hech qachon savol bermaslik kerak
""",
    "AI02": """
? AI'dagi “hallucination” nima?
+ AI ishonch bilan noto'g'ri yoki to'qib chiqarilgan ma'lumot berishi
- AI'ning juda tez ishlashi
- AI'ning rasm chizishi
- Kompyuterning qizib ketishi

? AI bergan muhim faktni qanday tekshirish kerak?
+ Kamida 2 ta ishonchli manbada (rasmiy sayt, darslik, ilmiy maqola) solishtirib
- Shu savolni AI'ga yana bir marta berib
- Do'stingizdan “to'g'rimi?” deb so'rab
- Tekshirish shart emas, AI har doim to'g'ri

? Quyidagilardan qaysi birini AI'ga yozish MUMKIN EMAS?
+ Akkaunt parolingizni
- “Quyosh tizimidagi sayyoralar ro'yxati”
- O'zingiz yozgan hikoya matnini (shaxsiy ma'lumotsiz)
- Matematikadan misol

? Plagiat nima?
+ Birovning matni yoki ishini o'zingizniki qilib ko'rsatish
- Matnni ovozli o'qish
- Uy vazifasini o'z vaqtida topshirish
- Manbaga havola berish

? AI yozgan matndan foydalansangiz, to'g'ri yo'l qaysi?
+ O'qib, tekshirib, o'z so'zlaringiz bilan qayta yozish va AI'dan foydalanganingizni aytish
- Hech narsani o'zgartirmasdan “men yozdim” deb topshirish
- Matnni boshqa tilga tarjima qilib, o'zingizniki deb aytish
- Matnni do'stingizga berib, uning nomidan topshirish

? Qaysi ma'lumot shaxsiy va AI'ga berilmasligi kerak?
+ Uy manzilingiz va telefon raqamingiz
- Sevimli rangingiz
- Fanlar ro'yxati
- Kitob nomi

? Copilot javobi ostidagi manba havolalari nima uchun kerak?
+ Ma'lumot qayerdan olinganini ko'rib, uni tekshirish uchun
- Javobni chiroyli ko'rsatish uchun
- Reklama uchun
- Ular hech narsani bildirmaydi

? Ishonchli manbaga eng yaxshi misol qaysi?
+ Rasmiy tashkilot yoki ilmiy jurnal sayti
- Noma'lum muallifning ijtimoiy tarmoqdagi posti
- Sharhlardagi anonim fikr
- Reklama banneri

? Boshqa odamning rasmini AI'ga yuklash haqida to'g'ri fikr qaysi?
+ Faqat o'sha odamning ruxsati bilan mumkin
- Har doim mumkin, rasm internetda bo'lsa
- Faqat tunda mumkin
- Faqat rangli rasm bo'lsa mumkin

? AI javobida sana yoki raqam bo'lsa, nimaga e'tibor berish kerak?
+ Uni manbadan tekshirish — AI raqam va sanalarda ko'p xato qiladi
- Raqamlar doim to'g'ri bo'ladi
- Raqamlarni yaxlitlash kerak
- Raqamlar muhim emas

? Imtihonda AI'dan yashirincha foydalanish qanday baholanadi?
+ Aldash (akademik halollikni buzish)
- Aqlli usul
- Ruxsat etilgan yordam
- Uy vazifasi

? Mualliflik huquqi (copyright) nimani himoya qiladi?
+ Asar (matn, rasm, musiqa) muallifining unga bo'lgan huquqlarini
- Kompyuterni viruslardan
- Internet tezligini
- Telefon batareyasini
""",
    "AI03": """
? Deepfake nima?
+ AI yordamida yaratilgan, haqiqiyga o'xshash soxta video, rasm yoki ovoz
- Juda chuqur suv havzasi haqidagi video
- Kompyuter o'yinining nomi
- Antivirus dasturi

? Fishing (phishing) hujumi nima?
+ Aldov xat yoki havola orqali parol va shaxsiy ma'lumotlarni o'g'irlashga urinish
- Baliq ovlash haqidagi o'yin
- Internet tezligini oshirish usuli
- Kompyuterni tozalash dasturi

? Fishing xatining belgisi qaysi?
+ Shoshiltiradi (“24 soat ichida parolni kiriting!”) va shubhali havola yuboradi
- Do'stingiz bilan oldindan kelishgan uchrashuv haqida
- Maktab jadvali haqida rasmiy e'lon
- Hech qanday havola yoki so'rov yo'q

? Chatbot sizdan bank kartangiz raqamini so'rasa, nima qilish kerak?
+ Bermaslik, suhbatni to'xtatish va kattalarga aytish
- Darhol yozib berish
- Faqat oxirgi 4 ta raqamni emas, hammasini berish
- Bir necha kundan keyin berish

? Videodagi odam deepfake bo'lishi mumkinligining belgisi qaysi?
+ G'ayritabiiy ko'z qisish, lab harakati ovozga mos kelmasligi, yuz chetlari xira
- Video yuqori sifatda
- Videoda tabiat ko'rinadi
- Video qisqa

? Ijtimoiy muhandislik (social engineering) nima?
+ Odamni aldab, ishonchiga kirib, maxfiy ma'lumot oldirish usuli
- Ijtimoiy tarmoq yaratish kasbi
- Ko'prik qurish muhandisligi
- Ijtimoiy fanlar darsligi

? Kimdir ruxsatsiz sizning ovozingizni AI bilan nusxalab ishlatsa, bu...
+ Etikaga zid va zararli bo'lishi mumkin — ota-ona yoki ustozga aytish kerak
- Normal holat, hamma shunday qiladi
- Sizga sovg'a
- Faqat kulgili bo'lsa mumkin

? Poe kabi bir nechta bot bor platformada xavfsizlik uchun nima muhim?
+ Har qanday botga shaxsiy ma'lumot bermaslik va javoblarni tekshirish
- Eng ko'p obunachisi bor botga hamma narsani aytish
- Botlarga parollarni saqlatish
- Faqat bitta botdan foydalanish shart

? Shubhali havolani ochishdan oldin nima qilish kerak?
+ Manzilni (domen) diqqat bilan tekshirish va ishonmasangiz ochmaslik
- Darhol ochib ko'rish
- Havolani hamma do'stlarga yuborish
- Havolaga parol yozish

? AI bilan soxta yangilik yaratib tarqatish haqida to'g'ri fikr qaysi?
+ Bu mas'uliyatsiz va zararli — odamlarni chalg'itadi
- Agar qiziq bo'lsa, mumkin
- Faqat o'qituvchiga yuborsa mumkin
- Bu oddiy hazil, hech qanday zarari yo'q

? Kuchli parolga misol qaysi?
+ “Kitob7!Daryo#Oy” — uzun, harf, raqam va belgilar aralash
- “123456”
- “parol”
- Tug'ilgan sanangiz

? Ikki bosqichli tasdiqlash (2FA) nima beradi?
+ Paroldan tashqari ikkinchi tekshiruv (masalan, kod) — akkaunt xavfsizroq bo'ladi
- Internetni tezlashtiradi
- Parolni keraksiz qiladi
- Akkauntni ikkiga bo'ladi
""",
    "AI04": """
? Yaxshi promptning to'rt asosiy qismi qaysi?
+ Rol, Vazifa, Kontekst, Cheklovlar
- Salom, Rahmat, Xayr, Kechirasiz
- Sarlavha, Rasm, Video, Musiqa
- Savol, Javob, Baho, Imzo

? Promptdagi “Rol” nimani bildiradi?
+ AI kim sifatida javob berishi kerakligini (masalan, “Sen tajribali ustozsan”)
- Javob qaysi tilda bo'lishini
- Kompyuter modelini
- Javobning rangini

? “Kontekst” qismiga misol qaysi?
+ “Matn 10 yoshli bolalar uchun, ular mavzuni birinchi marta o'rganmoqda”
- “Javob ber”
- “Tez”
- “Rahmat”

? “Cheklovlar”ga misol qaysi?
+ “100 so'zdan oshmasin, 3 ta band ko'rinishida”
- “Sen o'qituvchisan”
- “Hikoya yoz”
- “Salom”

? Quyidagi promptlardan qaysi biri eng yaxshi?
+ “Sen bolalar yozuvchisisan. 9 yoshlilar uchun do'stlik haqida 150 so'zli hikoya yoz, oxirida xulosa bo'lsin.”
- “Hikoya yoz”
- “Do'stlik”
- “Menga nimadir ber”

? Birinchi javob yoqmasa, eng to'g'ri harakat qaysi?
+ Promptni aniqlashtirib, nima o'zgarishi kerakligini aytish (iteratsiya)
- Hech narsa qilmaslik
- AI'ni boshqa savollar bilan chalg'itish
- Kompyuterni o'chirish

? Javob formatini so'rash nimaga yordam beradi?
+ Natijani kerakli ko'rinishda (jadval, ro'yxat, reja) olishga
- AI'ni tezroq ishlatishga
- Internet sarfini kamaytirishga
- Rasm sifatini oshirishga

? “Sen matematika ustozisan” — bu promptning qaysi qismi?
+ Rol
- Cheklov
- Format
- Kontekst

? Noaniq prompt nimaga olib keladi?
+ Umumiy, kerakka yaramaydigan javobga
- Har doim mukammal javobga
- AI'ning ishlamay qolishiga
- Javobning rasmga aylanishiga

? Prompt yozishda namuna (misol) berish nima uchun foydali?
+ AI qanday javob kutilayotganini aniqroq tushunadi
- Prompt qisqaroq bo'ladi
- Namuna berish taqiqlangan
- AI namunani o'chirib tashlaydi

? Uzun ish uchun eng yaxshi yondashuv qaysi?
+ Ishni bosqichlarga bo'lib, har birini alohida so'rash
- Hammasini bitta so'z bilan so'rash
- Hech qanday tafsilot bermaslik
- Faqat “davom et” deb yozish

? Claude yoki boshqa AI javobini qabul qilishdan oldin nima qilish kerak?
+ Javobni o'qib, talablarga mosligini va xatolarini tekshirish
- Darhol nusxalab topshirish
- Javobning faqat birinchi gapini o'qish
- Javobni o'chirib tashlash
""",
    "AI05": """
? Prompt Battle'da g'olibni aniqlash uchun eng muhim narsa nima?
+ Oldindan kelishilgan aniq baholash mezonlari
- Kim birinchi yozgani
- Promptning eng uzun bo'lishi
- Kompyuterning narxi

? Bir xil vazifaga turli promptlar berishdan maqsad nima?
+ Qaysi so'zlar va tuzilma eng yaxshi natija berishini tajribada aniqlash
- AI'ni charchatish
- Vaqtni o'tkazish
- Internet sarfini oshirish

? Reklama matni uchun promptga nimani qo'shish foydali?
+ Maqsadli auditoriya, uslub va harakatga chaqiriq (masalan, “ro'yxatdan o'ting”)
- Faqat “reklama” so'zini
- Tasodifiy raqamlarni
- Hech narsa qo'shmaslik

? “Auditoriya” nima?
+ Matn yoki mahsulot mo'ljallangan odamlar guruhi
- Musiqa turi
- Kompyuter qismi
- Rasm formati

? Cheklov qo'shilganda (masalan, “20 so'zdan oshmasin”) natija qanday o'zgaradi?
+ Qisqaroq va aniqroq bo'ladi — muhim narsalarni tanlashga majbur qiladi
- Har doim uzunroq bo'ladi
- O'zgarmaydi
- AI javob bermay qo'yadi

? Gemini javobini yaxshilashning to'g'ri usuli qaysi?
+ Aniq fikr bildirish: “ohangni quvnoqroq qil, 2-gapni qisqartir”
- “Yomon” deb yozib qo'yish
- Yangi suhbat boshlab, hech narsa tushuntirmaslik
- Bir xil promptni o'zgartirmay 10 marta yuborish

? Jamoada prompt yozishning foydasi nima?
+ Turli g'oyalarni birlashtirib, kuchliroq prompt yaratish
- Har kim faqat o'z promptini yashiradi
- Bitta odam ishlaydi, qolganlar kutadi
- Foydasi yo'q

? Musobaqada boshqa jamoaning promptini tahlil qilishdan maqsad nima?
+ Undan o'rganish va o'z promptini yaxshilash
- Uni ko'chirib olib, o'zingizniki deb aytish
- Uni masxara qilish
- Uni o'chirish

? Reklama uchun “harakatga chaqiriq” (call to action) qaysi?
+ “Bugun ro'yxatdan o'ting!”
- “Bizning maktab”
- “Rangli rasm”
- “Shrift”

? Bir xil promptga AI ikki marta biroz farqli javob berishi mumkinmi?
+ Ha, AI javoblarida tasodifiylik bor
- Yo'q, javob har doim bir xil
- Faqat kechqurun farq qiladi
- Faqat rus tilida farq qiladi

? “Ohang” (tone) nimani bildiradi?
+ Matnning kayfiyati va uslubi (rasmiy, quvnoq, jiddiy)
- Matnning uzunligi
- Shrift o'lchami
- Ovoz balandligi

? Prompt Battle'dan keyin eng foydali xulosa qaysi?
+ Qaysi prompt qismlari natijani yaxshilaganini yozib qo'yish
- Faqat g'olib nomini eslab qolish
- Hamma promptlarni o'chirish
- Hech narsa yozmaslik
""",
    "AI06": """
? “Few-shot” prompt nima?
+ AI'ga vazifadan oldin bir nechta tayyor namuna (misol) berish
- Faqat bitta so'zli prompt
- Rasm bilan prompt
- Juda tez yoziladigan prompt

? “Zero-shot” prompt nima?
+ Hech qanday namunasiz, faqat vazifani aytish
- Nol ballik javob
- Bo'sh prompt
- Faqat raqamlardan iborat prompt

? Chain-of-Thought (CoT) usuli nima?
+ AI'dan masalani bosqichma-bosqich, fikrlash zanjiri bilan yechishni so'rash
- AI'ga zanjir rasmini chizdirish
- Bir nechta chatbotni ketma-ket ulash
- Javobni qisqartirish

? CoT qaysi vazifalarda ayniqsa foydali?
+ Mantiqiy va matematik masalalarda
- Rasm chizishda
- Musiqa tinglashda
- Shrift tanlashda

? Few-shot promptga misol qaysi?
+ “Kayfiyatni aniqla. ‘Zo'r kun!’ → ijobiy. ‘Yomg'ir, zerikarli’ → salbiy. ‘Kino ajoyib edi’ → ?”
- “Kayfiyat”
- “Menga yordam ber”
- “Javob ber”

? Groq platformasining asosiy xususiyati nima?
+ Til modellarini juda tez ishga tushiradi (javob tez keladi)
- Faqat rasm yaratadi
- Faqat video tahrirlaydi
- Internetsiz ishlaydi

? “Kontekst oynasi” (context window) nima?
+ Model bir vaqtda “eslab” ko'ra oladigan matn hajmi
- Brauzer oynasi
- Kompyuter ekrani o'lchami
- Chat oynasining rangi

? CoT bilan olingan javobni nega o'zingiz ham tekshirish kerak?
+ Bosqichlarning birida xato bo'lsa, yakuniy javob ham noto'g'ri bo'ladi
- Tekshirish shart emas
- CoT hech qachon xato qilmaydi
- Faqat ustoz tekshiradi

? “Bosqichma-bosqich o'ylab, keyin javob ber” — bu qaysi usul?
+ Chain-of-Thought
- Few-shot
- Rol berish
- Cheklov qo'yish

? Murakkab vazifani AI'ga berishda eng yaxshi yo'l qaysi?
+ Uni kichik qismlarga bo'lib, ketma-ket so'rash
- Hammasini bitta qisqa so'z bilan so'rash
- Hech qanday ma'lumot bermaslik
- Faqat oxirgi qismini so'rash

? Few-shot namunalari qanday bo'lishi kerak?
+ Bir xil formatda va aniq — AI ulardan qoliplarni o'rganadi
- Har xil formatda va chalkash
- Faqat bitta harfdan iborat
- Vazifaga umuman aloqasiz

? “Agar 3 ta olma 3 daqiqada yeyilsa, 100 ta olma 100 daqiqada yeyiladimi?” kabi masalada CoT nima beradi?
+ Shartni diqqat bilan tahlil qilib, shoshilinch xatoni oldini oladi
- Javobni tasodifiy tanlaydi
- Masalani rasmga aylantiradi
- Masalani o'chiradi
""",
    "AI07": """
? NotebookLM asosan nima uchun ishlatiladi?
+ Yuklangan hujjatlar (PDF, matn) asosida o'rganish, konspekt va savollar tayyorlash
- Video montaj qilish
- O'yin yaratish
- Musiqa yozish

? NotebookLM javoblarining asosiy afzalligi nima?
+ Javoblar siz yuklagan manbalarga asoslanadi va iqtibos ko'rsatiladi
- Javoblar har doim internetdan olinadi
- Javoblar faqat ingliz tilida
- Javoblar faqat rasm ko'rinishida

? Konspekt nima?
+ Matnning asosiy fikrlari qisqa va tartibli yozilgan ko'rinishi
- Matnning to'liq nusxasi
- Kitobning muqovasi
- Test javoblari

? “Iqtibos” (citation) nima uchun kerak?
+ Javob manbaning qaysi joyidan olinganini ko'rsatish va tekshirish uchun
- Matnni chiroyli qilish uchun
- Reklama uchun
- Javobni uzaytirish uchun

? NotebookLM'ga qanday hujjatni yuklamaslik kerak?
+ Shaxsiy yoki maxfiy ma'lumotlar bor hujjatni (pasport, parollar)
- Darslik bobini
- O'z konspektingizni
- Ochiq maqolani

? AI bilan o'qishning eng foydali usuli qaysi?
+ AI tuzgan savollarga o'zingiz javob berib, bilimingizni tekshirish
- Faqat AI xulosasini o'qib, kitobni ochmaslik
- Javoblarni yodlab olish
- Hujjatni yuklab, hech narsa qilmaslik

? Hujjatdan avtomatik test yaratilgandan keyin nima qilish kerak?
+ Savol va javoblarni kitob bilan solishtirib, xatolarini tuzatish
- Hech tekshirmasdan ishlatish
- Testni o'chirish
- Faqat birinchi savolni o'qish

? “Manbaga asoslangan AI” deganda nima tushuniladi?
+ AI faqat berilgan hujjatlardagi ma'lumotlardan foydalanadi
- AI har qanday saytdan ma'lumot oladi
- AI manba yaratadi
- AI manbalarni o'chiradi

? Konspektda qaysi narsa bo'lishi shart emas?
+ Asosiy fikrga aloqasi yo'q mayda tafsilotlar
- Asosiy tushunchalar
- Muhim ta'riflar
- Qisqa xulosa

? NotebookLM'dagi audio-xulosa (podkast) nima uchun qulay?
+ Materialni yo'lda yoki dam olayotganda tinglab takrorlash mumkin
- Matnni o'chiradi
- Faqat musiqa qo'yadi
- Hujjatni tarjima qilmaydi

? Lug'at (glossariy) tuzishdan maqsad nima?
+ Yangi atamalar va ularning ma'nosini bir joyda to'plash
- Kitobni qisqartirish
- Rasm qo'shish
- Sahifalarni raqamlash

? AI tuzgan konspektni o'z so'zlaringiz bilan qayta yozish nima beradi?
+ Mavzuni chuqurroq tushunasiz va eslab qolasiz
- Hech qanday foyda bermaydi
- Vaqtni behuda sarflash
- Faqat ustoz uchun kerak
""",
    "AI08": """
? Perplexity AI'ning oddiy chatbotdan asosiy farqi nima?
+ Internetdan qidiradi va javobga manbalar havolasini qo'shadi
- Faqat rasm chizadi
- Internetsiz ishlaydi
- Faqat she'r yozadi

? Fact-check nima?
+ Ma'lumot to'g'ri ekanini ishonchli manbalar orqali tekshirish
- Matnni chiroyli yozish
- Faktlarni yodlash
- Rasmni tahrirlash

? “Ikki manba qoidasi” nima?
+ Muhim faktni kamida ikkita mustaqil ishonchli manbada tasdiqlash
- Faqat ikkita sayt ochish mumkin
- Ikki marta savol berish
- Ikki kishidan so'rash

? Manbaning ishonchliligini qanday baholash mumkin?
+ Muallif/tashkilot kimligi, nashr sanasi va boshqa manbalarga mosligi orqali
- Saytning rangi bo'yicha
- Reklamalar soni bo'yicha
- Sarlavhaning uzunligi bo'yicha

? Qaysi manba odatda eng ishonchli?
+ Ilmiy tashkilot yoki rasmiy agentlik sayti (masalan, NASA)
- Noma'lum blog
- Anonim forum xabari
- Reklama sahifasi

? Perplexity havola qilgan manbani ochib ko'rish nega kerak?
+ AI manbani noto'g'ri tushungan yoki xato iqtibos keltirgan bo'lishi mumkin
- Ochish shart emas
- Havola faqat bezak
- Manbalar har doim bir xil

? Ma'lumotning sanasi nega muhim?
+ Eski ma'lumot hozirgi holatga mos kelmasligi mumkin
- Sana hech qanday rol o'ynamaydi
- Faqat tug'ilgan kun uchun muhim
- Yangi ma'lumot har doim noto'g'ri

? Research (izlanish) qaysi tartibda o'tkaziladi?
+ Savol qo'yish → manbalarni topish → tekshirish → xulosa yozish
- Xulosa yozish → savol qo'yish
- Faqat bitta sayt ochish
- Do'stdan javobni ko'chirish

? “Feyk” yangilikning belgisi qaysi?
+ Hayajonli sarlavha, manba yo'q, boshqa ishonchli saytlarda tasdig'i yo'q
- Rasmiy saytda e'lon qilingan
- Ko'p manbalar tasdiqlagan
- Muallif va sana ko'rsatilgan

? Izlanish xulosasini qanday yozish to'g'ri?
+ O'z so'zlaringiz bilan, manbalar havolasi bilan
- Manbadan to'liq ko'chirib, havolasiz
- AI javobini o'zgartirmasdan
- Xulosasiz

? Agar ikki manba bir-biriga zid ma'lumot bersa, nima qilish kerak?
+ Uchinchi ishonchli manbani topib, qaysi biri to'g'riligini aniqlash
- Birinchisiga ishonish
- Ikkalasini ham tashlab yuborish
- Tangani tashlab tanlash

? Perplexity'ga yaxshi research savoliga misol qaysi?
+ “Quyosh tizimida nechta sayyora bor va Pluton nega sayyora hisoblanmaydi? Manbalar bilan.”
- “Koinot”
- “Ayt”
- “Qiziq narsa”
""",
    "AI09": """
? Gamma App nima uchun ishlatiladi?
+ AI yordamida taqdimot, hujjat va veb-sahifa yaratish uchun
- Faqat video montaj uchun
- O'yin yaratish uchun
- Musiqa yozish uchun

? Yaxshi slaydning asosiy qoidasi qaysi?
+ Bitta slayd — bitta asosiy fikr, kam matn
- Har slaydga imkon qadar ko'p matn
- Har slaydda 10 xil shrift
- Rasmsiz va sarlavhasiz slayd

? AI yaratgan taqdimotni nima uchun qo'lda tahrirlash kerak?
+ Xatolarni tuzatish, mazmunni aniqlashtirish va o'z uslubingizni qo'shish uchun
- Tahrirlash shart emas
- Faqat rangini o'zgartirish uchun
- AI tahrirlashni taqiqlaydi

? Taqdimot tuzilmasining to'g'ri tartibi qaysi?
+ Sarlavha → asosiy fikrlar → xulosa
- Xulosa → sarlavha → hech narsa
- Faqat rasmlar
- Faqat xulosa

? Slayddagi matn qanday bo'lishi kerak?
+ Qisqa: kalit so'zlar va qisqa jumlalar
- Butun maqola
- Juda kichik shriftda uzun matn
- Faqat bosh harflarda

? Taqdimotda vizual (rasm, diagramma) nima uchun kerak?
+ Fikrni tezroq va tushunarliroq yetkazish uchun
- Faqat joyni to'ldirish uchun
- Matnni yashirish uchun
- Kerak emas

? “Pitch” nima?
+ G'oya yoki loyihani qisqa va ishonarli taqdim qilish
- Futbol maydoni
- Rasm formati
- Kompyuter dasturi

? Taqdimotni ko'rsatayotganda eng to'g'ri usul qaysi?
+ Slayddan o'qimasdan, tinglovchilarga qarab, o'z so'zlaringiz bilan gapirish
- Slayddagi matnni so'zma-so'z o'qish
- Orqa o'girib gapirish
- Juda tez gapirib tugatish

? Ranglarni tanlashda nimaga e'tibor berish kerak?
+ Matn fonda yaxshi o'qilishiga (kontrast)
- Imkon qadar ko'p rang ishlatishga
- Matn va fonni bir xil rangda qilishga
- Faqat qora va qora

? Ma'lumotni diagrammaga aylantirish qachon foydali?
+ Raqamlar va taqqoslashlarni ko'rsatishda
- Faqat she'r yozishda
- Hech qachon
- Faqat sarlavhada

? AI taqdimotidagi faktlar haqida to'g'ri fikr qaysi?
+ Ularni ham tekshirish kerak — AI xato qilishi mumkin
- Ular har doim to'g'ri
- Faktlar taqdimotda muhim emas
- Faqat raqamlarni tekshirish kerak

? 5 slaydli taqdimot uchun eng mos reja qaysi?
+ 1-sarlavha, 2–4 asosiy fikrlar, 5-xulosa
- 5 ta bir xil slayd
- Faqat bitta slayd
- 5 ta bo'sh slayd
""",
    "AI10": """
? AI rasm generatori nima qiladi?
+ Matnli tavsif (prompt) asosida yangi rasm yaratadi
- Mavjud rasmni faqat qirqadi
- Rasmni matnga aylantiradi
- Kamerani yoqadi

? Yaxshi rasm promptida nimalar bo'lishi foydali?
+ Obyekt, muhit, uslub, yorug'lik va kompozitsiya
- Faqat bitta so'z
- Faqat raqamlar
- Faqat “chiroyli rasm”

? Midjourney'dagi --ar parametri nimani belgilaydi?
+ Rasm tomonlarining nisbatini (masalan, 16:9 yoki 1:1)
- Rasm rangini
- Rassom ismini
- Rasm narxini

? “Uslub” (style) promptga qanday qo'shiladi?
+ “akvarel uslubida”, “piksel-art”, “kiberpank” kabi so'zlar bilan
- Rasm hajmini yozib
- Kompyuter nomini yozib
- Uslub qo'shib bo'lmaydi

? Yorug'likni tasvirlashga misol qaysi?
+ “quyosh botishidagi iliq yorug'lik”
- “kvadrat shakl”
- “uchta odam”
- “katta shahar”

? Kompozitsiya nima?
+ Rasm ichidagi obyektlarning joylashuvi va kamera burchagi
- Rasm fayli nomi
- Rasm narxi
- Rasm yuklangan sana

? AI rasm yaratishda mualliflik bo'yicha to'g'ri fikr qaysi?
+ Mashhur rassomning asarini nusxalash yoki taniqli brend logotipini soxtalashtirish noto'g'ri
- Hamma narsani nusxalash mumkin
- Mualliflik AI'ga tegishli emas, shuning uchun qoidalar yo'q
- Faqat qora-oq rasmda qoidalar bor

? Rasmni yaxshilash uchun eng yaxshi usul qaysi?
+ Natijaga qarab promptga bitta-bitta aniqlik kiritish (iteratsiya)
- Har safar butunlay boshqa mavzu yozish
- Promptni qisqartirib bitta so'z qoldirish
- Natijani ko'rmasdan yuborish

? 16:9 nisbati qaysi format uchun mos?
+ Kompyuter ekrani va YouTube videosi kabi keng format
- Kvadrat avatar
- Tik telefon hikoyasi (story)
- Pasport rasmi

? Rasm uchun kamera burchagiga misol qaysi?
+ “tepadan ko'rinish” (bird's-eye view)
- “qizil rang”
- “baxtli kayfiyat”
- “yozgi kun”

? Bir xil promptdan bir nechta variant olish nima uchun foydali?
+ Eng yaxshisini tanlash va g'oyani rivojlantirish uchun
- Hech qanday foyda yo'q
- Faqat xotirani to'ldiradi
- Variantlar bir xil bo'ladi

? AI rasmidagi tipik xato qaysi?
+ Qo'llardagi barmoqlar soni noto'g'ri yoki matn buzilgan bo'lishi
- Rasm har doim mukammal
- Rasm faqat qora rangda
- Rasm umuman ochilmaydi
""",
    "AI11": """
? Konsept-art nima?
+ Qahramon yoki olamning dastlabki vizual g'oyasi (eskizi)
- Tayyor o'yinning kodi
- Musiqa trek
- O'yin narxi

? Image-to-Image nima?
+ Mavjud rasmni asos qilib, uning yangi variantini yaratish
- Rasmni matnga aylantirish
- Rasmni o'chirish
- Rasmni chop etish

? Qahramon dizaynida “izchillik” nimani bildiradi?
+ Turli rasmlarda qahramon bir xil qiyofada (yuz, kiyim, ranglar) ko'rinishi
- Har rasmda butunlay boshqa qahramon
- Faqat bitta rasm chizish
- Qahramonni rangsiz chizish

? Negative prompt nima?
+ Rasmda bo'lmasligi kerak bo'lgan narsalar ro'yxati (masalan, “xira, ortiqcha barmoqlar”)
- Salbiy kayfiyatli rasm
- Promptni o'chirish
- Qora-oq rasm

? Yaxshi o'yin qahramoni uchun nima muhim?
+ Esda qoladigan silueti, aniq xarakteri va o'ziga xos ranglari
- Imkon qadar ko'p detallar, hech qanday g'oyasiz
- Boshqa mashhur qahramonning aniq nusxasi
- Faqat matn

? Leonardo AI'da qahramonni turli pozalarda olish uchun qaysi usul qulay?
+ Asosiy rasmni Image-to-Image bilan ishlatib, pozani promptda o'zgartirish
- Har safar butunlay yangi qahramon tasvirlash
- Rasmni qo'lda qirqish
- Faqat sarlavhani o'zgartirish

? Qahramonning “xarakteri” deganda nima tushuniladi?
+ Uning fe'l-atvori, maqsadi va kuchli tomonlari
- Faqat ismi
- Faqat bo'yi
- Kompyuter xotirasi

? Mashhur o'yin qahramonini aynan nusxalab, o'zinikidek sotish haqida to'g'ri fikr qaysi?
+ Bu mualliflik huquqini buzadi
- Bu mutlaqo normal
- AI bilan qilinsa ruxsat
- Faqat rangini o'zgartirsa ruxsat

? Konsept-art jarayonining to'g'ri tartibi qaysi?
+ G'oya va tavsif → bir nechta variant → eng yaxshisini tanlash → takomillashtirish
- Tayyor rasm → g'oya
- Faqat bitta urinish
- Variantlarsiz darhol yakunlash

? Qahramon tavsifiga misol qaysi?
+ “Kosmik kashfiyotchi qiz, ko'k skafandr, yelkasida kichik robot, jasur va qiziquvchan”
- “Qahramon”
- “Rasm chiz”
- “Yaxshi”

? 3D modelga mos illustratsiya uchun qaysi ko'rinish foydali?
+ Old, yon va orqa tomondan ko'rinish (turnaround)
- Faqat bitta xira rasm
- Faqat yuzning yaqin plani
- Faqat soya

? AI bilan yaratilgan qahramon rasmidan keyin nima qilish foydali?
+ Xatolarni (qo'l, ko'z) tuzatish va qahramonning qisqa tarixini yozish
- Hech narsa qilmaslik
- Rasmni darhol o'chirish
- Boshqa odamning ismi bilan e'lon qilish
""",
    "AI12": """
? Brend nima?
+ Kompaniya yoki loyihaning nomi, logotipi, ranglari va uslubidan iborat qiyofasi
- Faqat mahsulot narxi
- Do'kon manzili
- Kompyuter dasturi

? Yaxshi logotipning xususiyati qaysi?
+ Oddiy, esda qoladigan va kichik o'lchamda ham o'qiladigan
- Juda ko'p mayda detallarga ega
- 10 xil rangli
- Faqat katta plakatda ko'rinadigan

? Tipografika nima?
+ Shrift tanlash va matnni chiroyli, o'qiladigan joylashtirish san'ati
- Rasm chizish usuli
- Musiqa janri
- Printer turi

? Ideogram AI'ning boshqa rasm generatorlardan kuchli tomoni nima?
+ Rasm ichida matnni (logotip, poster yozuvi) aniq yoza oladi
- Video montaj qiladi
- Musiqa yaratadi
- Faqat 3D modellar yaratadi

? Posterda “ierarxiya” nimani bildiradi?
+ Eng muhim ma'lumot eng ko'zga tashlanadigan bo'lishi (katta sarlavha → tafsilot)
- Hamma matn bir xil o'lchamda
- Faqat rasm, matnsiz
- Ma'lumotlar tasodifiy joylashgan

? Brend uchun rang palitrasi nechta asosiy rangdan iborat bo'lgani yaxshi?
+ 2–3 ta asosiy rang
- 15–20 ta rang
- Faqat bitta oq rang
- Rang muhim emas

? UI nima?
+ Foydalanuvchi interfeysi — ekrandagi tugmalar, menyular va ko'rinish
- Kompyuter ichidagi qism
- Internet tezligi
- Fayl formati

? UX nima?
+ Foydalanuvchi tajribasi — mahsulotdan foydalanish qanchalik qulay va yoqimli ekani
- Rasm formati
- Kompyuter brendi
- Dasturlash tili

? “5 soniya testi” nimani tekshiradi?
+ Odam 5 soniya ko'rgandan keyin dizaynning asosiy g'oyasini eslab qolishini
- Kompyuter tezligini
- Matnni 5 marta o'qishni
- Rasmning 5 ta rangini

? Logotip yaratishda boshqa kompaniyaning logotipiga juda o'xshatish haqida to'g'ri fikr qaysi?
+ Bu chalkashlik va huquqiy muammoga olib keladi
- Bu yaxshi g'oya
- Bu majburiy
- Hech qanday muammo yo'q

? Kontrast nima uchun muhim?
+ Matn va elementlar fondan yaqqol ajralib, oson o'qiladi
- Rasmni xira qiladi
- Faylni kichraytiradi
- Hech qanday ahamiyati yo'q

? Poster uchun eng to'g'ri tartib qaysi?
+ Katta sarlavha, aniq tasvir, qisqa ma'lumot (sana, joy) va harakatga chaqiriq
- Faqat uzun matn
- Ko'p kichik rasmlar, sarlavhasiz
- Bo'sh varaq
""",
    "AI13": """
? Text-to-Video nima?
+ Matnli tavsif asosida video yaratish
- Videoni matnga aylantirish
- Videoni o'chirish
- Video uchun subtitr yozish

? Image-to-Video nima?
+ Tayyor rasmni harakatlanuvchi videoga aylantirish
- Videodan rasm qirqib olish
- Rasmni chop etish
- Rasmni o'chirish

? Video promptida nimani albatta yozish kerak?
+ Sahna, harakat va kamera harakati
- Faqat videoning nomini
- Faqat rang nomini
- Hech narsa

? Kamera harakatiga misol qaysi?
+ “kamera sekin yaqinlashadi (zoom in)”
- “qizil olma”
- “quvnoq kayfiyat”
- “katta shrift”

? “Pan” kamera harakati nima?
+ Kameraning chapdan o'ngga (yoki aksincha) gorizontal burilishi
- Kameraning yaqinlashishi
- Videoni to'xtatish
- Rangni o'zgartirish

? Video sifati va harakat tabiiyligini oshirishning yaxshi usuli qaysi?
+ Bitta oddiy harakatni aniq tasvirlash va bir nechta variant yaratib tanlash
- Bitta qisqa videoda 10 ta turli harakat so'rash
- Promptni bo'sh qoldirish
- Faqat bitta urinish qilish

? Runway kabi vositalarda video uzunligi odatda qanday?
+ Bir necha soniyalik qisqa kliplar
- Bir necha soatlik film
- Faqat 1 kadr
- Cheksiz

? “Loop” video nima?
+ Oxiri boshiga uzluksiz ulanib, takrorlanadigan video
- Ovozsiz video
- Teskari o'ynaydigan video
- Juda uzun video

? AI video yaratishda etik qoida qaysi?
+ Haqiqiy odamlar ishtirokidagi soxta videolarni ruxsatsiz yaratmaslik
- Istalgan odamning soxta videosini yaratish mumkin
- Faqat do'stlar haqida soxta video mumkin
- Etika videoga taalluqli emas

? Video kayfiyatini qanday berish mumkin?
+ “sirli, tuman, kechqurun” kabi kayfiyat va muhitni tasvirlab
- Video hajmini yozib
- Fayl nomini o'zgartirib
- Kayfiyat berib bo'lmaydi

? AI videodagi tipik nuqson qaysi?
+ Obyekt shakli yoki yuzning kadrdan kadrga o'zgarib ketishi
- Video doim mukammal
- Video faqat qora-oq
- Video ovozsiz ochilmaydi

? 5 soniyalik video uchun eng mos sahna qaysi?
+ Bitta asosiy harakat (masalan, qushning qanot qoqib uchishi)
- To'liq kino syujeti
- 20 ta sahna almashinuvi
- Uzun dialog
""",
    "AI14": """
? Storyboard nima?
+ Video sahnalarining ketma-ket chizilgan yoki yozilgan rejasi
- Videoning nomi
- Musiqa ro'yxati
- Kompyuter klaviaturasi

? Treyler nima?
+ Film yoki loyihaga qiziqtiruvchi qisqa reklama videosi
- To'liq film
- Kino chiptasi
- Kamera turi

? Kinematografik uslub deganda nima tushuniladi?
+ Kino kabi: chiroyli yorug'lik, kamera harakati va kompozitsiya
- Faqat qora ekran
- Telefon ekrani skrinshoti
- Matnli slayd

? Bir nechta AI kliplarni bitta videoga qanday birlashtirish mumkin?
+ Video muharrirda (masalan, CapCut) montaj qilib
- Ular o'zi birlashadi
- Birlashtirib bo'lmaydi
- Faqat chop etib

? Treylerning odatiy tuzilmasi qaysi?
+ Qiziqtiruvchi boshlanish → asosiy sahnalar → sarlavha va yakun
- Faqat sarlavha
- Faqat titrlar
- Tasodifiy kadrlar

? Sahnalar orasidagi izchillik nima uchun muhim?
+ Tomoshabin hikoyani tushunishi va qahramonni tanishi uchun
- Muhim emas
- Faqat ovoz uchun
- Faqat fayl hajmi uchun

? “Orbit” kamera harakati nima?
+ Kamera obyekt atrofida aylanib harakatlanadi
- Kamera to'xtab turadi
- Kamera faqat yuqoriga qaraydi
- Kamera o'chadi

? Mini-treyler uchun eng mos davomiylik qaysi?
+ 15–20 soniya
- 2 soat
- 1 soniya
- 30 daqiqa

? Montajda “o'tish” (transition) nima?
+ Bir sahnadan ikkinchisiga ravon o'tish effekti
- Videoni o'chirish
- Videoni sotish
- Kamerani almashtirish

? Treylerga sarlavha qo'shishdan maqsad nima?
+ Loyiha nomini eslab qolarli qilib ko'rsatish
- Videoni uzaytirish
- Ovozni o'chirish
- Hech qanday maqsad yo'q

? AI video sahnasi rejadagidek chiqmasa, nima qilish kerak?
+ Promptni aniqlashtirib, yangi variant yaratish
- Butun loyihani tashlab ketish
- Rejani o'chirish
- Shunday qoldirish

? Storyboard tuzishning foydasi nima?
+ Vaqtni tejaydi: qaysi sahnalar kerakligini oldindan bilasiz
- Hech qanday foyda yo'q
- Faqat ustoz uchun
- Videoni uzaytiradi
""",
    "AI15": """
? Text-to-Speech (TTS) nima?
+ Matnni sun'iy ovoz bilan o'qib berish texnologiyasi
- Ovozni matnga aylantirish
- Musiqa yozish
- Video montaj

? Voice cloning nima?
+ Kimningdir ovozini AI yordamida nusxalash
- Ovozni o'chirish
- Ovozni balandlatish
- Mikrofon turi

? Boshqa odamning ovozini klonlash haqida to'g'ri qoida qaysi?
+ Faqat o'sha odamning aniq ruxsati bilan mumkin
- Har doim mumkin
- Faqat mashhur odamlarniki mumkin
- Faqat tunda mumkin

? Tinish belgilari AI ovozlashtirishga qanday ta'sir qiladi?
+ Pauza va intonatsiyani belgilaydi (vergul — qisqa pauza, nuqta — to'xtash)
- Hech qanday ta'sir qilmaydi
- Ovozni o'chiradi
- Faqat rangni o'zgartiradi

? Voice-over nima?
+ Video ustidan qo'yilgan diktor ovozi
- Videoning nomi
- Musiqa effekti
- Kamera turi

? Ovozlashtirish uchun matnni qanday tayyorlash yaxshi?
+ Qisqa gaplar, aniq tinish belgilari, qiyin so'zlarning to'g'ri yozilishi
- Juda uzun gaplar, tinish belgilarisiz
- Faqat bosh harflar
- Raqamlar va belgilar aralashmasi

? Ovozda hissiyotni berish uchun nima qilish mumkin?
+ Mos ovozni tanlash va hissiyot/barqarorlik sozlamalarini o'zgartirish
- Matnni o'chirish
- Faylni qayta nomlash
- Ovozni butunlay o'chirish

? Hikoyani ovozlashtirishda turli qahramonlar uchun nima qilinadi?
+ Har bir qahramonga alohida ovoz tanlanadi
- Barchasi bitta ovozda, pauzasiz
- Ovoz ishlatilmaydi
- Faqat musiqa qo'yiladi

? AI ovozi bilan aldash (masalan, ota-onaga soxta qo'ng'iroq) haqida to'g'ri fikr qaysi?
+ Bu xavfli firibgarlik usuli — bunday qo'ng'iroqlarga ehtiyot bo'lish kerak
- Bu oddiy hazil
- Bu foydali texnologiya, cheklov yo'q
- Bu mumkin emas

? Audio faylni videoga qo'shishda nimaga e'tibor berish kerak?
+ Ovoz va tasvir vaqtga mos (sinxron) bo'lishiga
- Faqat fayl nomiga
- Faqat rangiga
- Hech narsaga

? Ovozlashtirilgan matnni nega tinglab tekshirish kerak?
+ AI ba'zi so'zlarni noto'g'ri talaffuz qilishi mumkin
- Tekshirish shart emas
- AI hech qachon xato qilmaydi
- Faqat uzunligini bilish uchun

? Qisqa hikoya uchun yaxshi ovozlashtirish rejasi qaysi?
+ Matn yozish → ovoz tanlash → generatsiya → tinglab tuzatish
- Ovoz tanlash → matnsiz generatsiya
- Faqat musiqa qo'yish
- Hech narsa tekshirmaslik
""",
    "AI16": """
? HTML nima uchun ishlatiladi?
+ Veb-sahifa tuzilmasini (sarlavha, matn, rasm, tugma) yaratish uchun
- Sahifani bezash (rang, shrift) uchun
- Kompyuterni yoqish uchun
- Rasm chizish uchun

? CSS nima uchun ishlatiladi?
+ Veb-sahifaning ko'rinishini (rang, shrift, joylashuv) bezash uchun
- Ma'lumotlar bazasi uchun
- Musiqa yozish uchun
- Fayl o'chirish uchun

? JavaScript nima uchun ishlatiladi?
+ Sahifaga harakat va interaktivlik (tugma bosilganda nimadir bo'lishi) qo'shish uchun
- Faqat matn yozish uchun
- Faqat rang tanlash uchun
- Kompyuterni tozalash uchun

? HTML'da eng katta sarlavha qaysi teg bilan yoziladi?
+ <h1>
- <p>
- <img>
- <a>

? Havola (link) qaysi teg bilan yaratiladi?
+ <a href="...">
- <h1>
- <div>
- <br>

? Replit nima?
+ Brauzerda kod yozish va ishga tushirish muhiti
- Rasm muharriri
- Video player
- Antivirus

? AI yozgan kodni nusxalashdan oldin nima qilish kerak?
+ Kodni o'qib, har qism nima qilishini tushunish
- Hech o'qimasdan ishlatish
- Kodni o'chirish
- Faqat birinchi qatorni o'qish

? CSS'da matn rangini o'zgartirish qaysi xususiyat bilan qilinadi?
+ color
- font-size
- margin
- border

? Rasm qo'shish uchun qaysi HTML tegi ishlatiladi?
+ <img src="...">
- <a>
- <p>
- <h2>

? Vizitka sayt uchun eng kerakli bo'limlar qaysi?
+ Ism, qisqa tanishtiruv, qiziqishlar va aloqa
- Faqat bo'sh sahifa
- Faqat reklama
- Faqat parol

? Kodda o'zgarish qilgandan keyin nima qilish kerak?
+ Natijani ishga tushirib tekshirish
- Hech narsa
- Kodni darhol o'chirish
- Kompyuterni o'chirish

? AI'dan kod so'rashda yaxshi prompt qaysi?
+ “HTML va CSS'da ko'k rangli, markazlashgan 'Salom' tugmasi bo'lgan sahifa yoz va har qismini izohla”
- “Kod”
- “Sayt”
- “Nimadir yasa”
""",
    "AI17": """
? v0.dev nima qiladi?
+ Prompt asosida veb-interfeys (UI) komponentlarini yaratadi
- Video montaj qiladi
- Musiqa yaratadi
- Fotosuratlarni tahrirlaydi

? Komponent nima?
+ Interfeysning qayta ishlatiladigan qismi (tugma, karta, forma)
- Kompyuter ehtiyot qismi
- Rasm formati
- Internet provayderi

? “Holat” (state) nima?
+ Ilovaning ayni paytdagi ma'lumoti (masalan, ro'yxatdagi vazifalar)
- Ilovaning rangi
- Kompyuter manzili
- Ekran o'lchami

? To-do list ilovasining asosiy funksiyalari qaysi?
+ Vazifa qo'shish, bajarildi deb belgilash va o'chirish
- Faqat rasm ko'rsatish
- Musiqa ijro etish
- Video yozish

? Kalkulyator ilovasida eng muhim tekshiruv qaysi?
+ Hisob-kitob natijalari to'g'ri ekanini sinab ko'rish (masalan, 2 + 2 = 4)
- Faqat rangini tekshirish
- Faqat nomini tekshirish
- Hech narsa tekshirmaslik

? “Foydalanuvchi oqimi” (user flow) nima?
+ Foydalanuvchi maqsadga erishish uchun bosadigan qadamlar ketma-ketligi
- Internet trafigi
- Kompyuterning issiqligi
- Ma'lumotlar bazasi

? Interfeysni promptda yaxshilashning to'g'ri usuli qaysi?
+ Aniq o'zgarishni so'rash: “tugmalarni kattalashtir, tungi rejim qo'sh”
- “Yaxshiroq qil” deb yozish
- Promptni o'chirish
- Hech narsa yozmaslik

? MVP (minimal ishlaydigan mahsulot) nima?
+ Asosiy vazifani bajaradigan eng oddiy ishlaydigan versiya
- Eng qimmat versiya
- Tugallanmagan rasm
- Faqat reklama

? Yaxshi UI uchun qaysi qoida to'g'ri?
+ Tugmalar aniq yozilgan va bosish uchun yetarlicha katta
- Tugmalar yashirilgan
- Matn juda kichik
- Har bir tugma bir xil, yozuvsiz

? Ilovani boshqalarga ko'rsatishdan oldin nima qilish kerak?
+ O'zingiz to'liq sinab, xatolarni tuzatish
- Hech qanday sinovsiz ko'rsatish
- Ilovani o'chirish
- Faqat skrinshot yuborish

? Bo'sh ro'yxat holatida (empty state) ilova nima ko'rsatgani yaxshi?
+ “Hali vazifa yo'q — birinchisini qo'shing” kabi yo'riqnoma
- Bo'sh oq ekran
- Xato xabari
- Hech narsa

? Mini ilovaga qo'shimcha imkoniyat sifatida nima mos keladi?
+ Tungi rejim yoki vazifalarni saralash
- Ilovani o'chirib qo'yish
- Barcha tugmalarni olib tashlash
- Ekranni qora qilish
""",
    "AI18": """
? Debugging nima?
+ Dasturdagi xatolarni topish va tuzatish jarayoni
- Dastur yozishni boshlash
- Kompyuterni tozalash
- Dasturni o'chirish

? Sintaksis xatosi nima?
+ Til qoidalari buzilgan xato (masalan, yopilmagan qavs)
- Dastur ishlaydi, lekin noto'g'ri natija beradi
- Kompyuter sekin ishlashi
- Internet uzilishi

? Mantiqiy xato nima?
+ Dastur ishlaydi, lekin noto'g'ri natija beradi
- Dastur umuman ishga tushmaydi
- Klaviatura buzilishi
- Faylning nomi noto'g'ri

? Xato xabari (error message) nima uchun foydali?
+ Xato turi va qaysi qatorda ekanini ko'rsatadi
- Hech qanday foydasi yo'q
- Kompyuterni tezlashtiradi
- Kodni avtomatik o'chiradi

? Cursor nima?
+ Ichiga AI yordamchi o'rnatilgan kod muharriri
- Sichqoncha ko'rsatkichi o'yini
- Rasm muharriri
- Brauzer

? Refaktoring nima?
+ Kodning ishlashini o'zgartirmasdan, uni tushunarli va tartibli qilish
- Kodni o'chirib tashlash
- Yangi xato qo'shish
- Kodni boshqa tilga tarjima qilish

? AI xatoni tuzatib bergandan keyin nima qilish kerak?
+ Dasturni qayta ishga tushirib tekshirish va xato sababini tushunish
- Hech tekshirmasdan qabul qilish
- Kodni o'chirish
- Faylni yashirish

? Python'da print("Salom" — bu qanday xato?
+ Sintaksis xatosi: qavs yopilmagan
- Mantiqiy xato
- Xato yo'q
- Internet xatosi

? Xatoni topishning yaxshi usuli qaysi?
+ Muammoni kichik qismlarga bo'lib, har birini alohida tekshirish
- Hamma kodni birdan o'chirish
- Kompyuterni qayta yoqish
- Xatoni e'tiborsiz qoldirish

? O'zgaruvchiga yaxshi nom berishga misol qaysi?
+ total_score
- a
- x1y2z3
- qwerty

? AI'dan xato haqida so'rashda yaxshi prompt qaysi?
+ “Mana kod va xato xabari. Xato nima uchun chiqyapti? Tuzatishni va sababini tushuntir.”
- “Ishlamayapti”
- “Yordam”
- “Kod yomon”

? Izoh (comment) koddagi nima uchun kerak?
+ Kodning nima qilishini o'quvchiga tushuntirish uchun
- Kodni tezlashtirish uchun
- Kodni yashirish uchun
- Xato chiqarish uchun
""",
    "AI19": """
? API nima?
+ Dasturlar bir-biri bilan ma'lumot almashishi uchun kelishilgan interfeys
- Kompyuter ekrani
- Rasm formati
- Ovozli xabar

? Request (so'rov) va response (javob) nima?
+ Dastur API'ga so'rov yuboradi va undan javob oladi
- Ikkita kompyuter o'yini
- Ikki xil shrift
- Rasm va video

? JSON nima?
+ Ma'lumotni “kalit: qiymat” ko'rinishida saqlash va almashish formati
- Rasm muharriri
- Dasturlash tili kompilyatori
- Musiqa fayli

? {"ism": "Ali", "yosh": 12} — bu JSON'da "yosh" kalitining qiymati qanday?
+ 12
- "Ali"
- "yosh"
- ism

? Hugging Face nima?
+ Ochiq AI modellari, ma'lumotlar to'plami va demo ilovalar (Spaces) platformasi
- Ijtimoiy tarmoq o'yini
- Video muharrir
- Antivirus

? API kaliti (API key) bilan qanday ishlash kerak?
+ Uni maxfiy saqlash, hech kimga va ochiq kodga bermaslik
- Hammaga ulashish
- Saytga ochiq joylash
- Ijtimoiy tarmoqqa post qilish

? Ochiq (open-source) model nima?
+ Kodi yoki modeli hamma uchun ochiq bo'lgan, foydalanish va o'rganish mumkin bo'lgan model
- Faqat bir kompaniya ishlatadigan yopiq model
- Internetsiz ishlamaydigan dastur
- Pullik o'yin

? Rasmni taniydigan model qanday vazifani bajaradi?
+ Rasmdagi narsalarni aniqlaydi (masalan, “mushuk”)
- Rasmni chizadi
- Rasmni o'chiradi
- Rasmni chop etadi

? JSON'da ro'yxat (massiv) qanday yoziladi?
+ Kvadrat qavslarda: ["olma", "nok"]
- Doira qavslarda: ("olma", "nok")
- Burchak qavslarda: <olma, nok>
- Qavssiz: olma nok

? AI modelni sinashda nimani yozib borish foydali?
+ Kiruvchi ma'lumot, natija va xato qilgan holatlarni
- Faqat model nomini
- Hech narsani
- Faqat sanani

? “Model” deganda AI'da nima tushuniladi?
+ Ma'lumotlardan o'rgatilgan va bashorat qila oladigan dastur
- Kiyim ko'rsatuvchi odam
- Kompyuter korpusi
- Rasm ramkasi

? Agar API xato kodi qaytarsa, nima qilish kerak?
+ Xato xabarini o'qib, so'rovdagi muammoni (kalit, format) tekshirish
- Kompyuterni sindirish
- Hech narsa qilmaslik
- API'ni abadiy tashlab ketish
""",
    "AI20": """
? Avtomatlashtirish (automation) nima?
+ Takrorlanadigan ishni dastur o'zi bajaradigan qilib sozlash
- Ishni qo'lda bajarish
- Kompyuterni o'chirish
- Rasm chizish

? Make.com'da “scenario” nima?
+ Bir-biriga ulangan modullardan iborat avtomatlashtirish sxemasi
- Kino ssenariysi
- Rasm albomi
- Matn muharriri

? Trigger nima?
+ Sxemani ishga tushiradigan hodisa (masalan, botga yangi xabar kelishi)
- Sxemaning yakuni
- Xato xabari
- Rasm formati

? “Telegram xabar → AI → javob” sxemasida AI moduli nima qiladi?
+ Kelgan xabarni qayta ishlab, javob matnini yaratadi
- Xabarni o'chiradi
- Telegram'ni yopadi
- Rasm chizadi

? Bot uchun API kalitini qayerda saqlash kerak?
+ Platformaning maxfiy sozlamalarida (ulanish/connection), ochiq matnda emas
- Botning ommaviy tavsifida
- Guruh chatida
- Sayt bosh sahifasida

? No-code nima?
+ Kod yozmasdan, vizual bloklar bilan dastur yoki avtomatlashtirish yaratish
- Kodni o'chirish
- Kompyuter yo'qligi
- Parolsiz kirish

? Sxema ishlamasa, birinchi navbatda nima qilinadi?
+ Har bir modul natijasini (log/tarix) ko'rib, qaysi qadamda xato borligini topish
- Hamma narsani o'chirish
- Kompyuterni almashtirish
- Kutib turish

? Avtomatlashtirishga yaxshi misol qaysi?
+ Har kuni ertalab Telegram'ga ob-havo xabarini avtomatik yuborish
- Har kuni qo'lda bir xil xabar yozish
- Rasmni qo'lda chizish
- Kitob o'qish

? Telegram bot javob berishida qanday cheklov qo'yish foydali?
+ Faqat ma'lum mavzuda javob berish va shaxsiy ma'lumot so'ramaslik
- Hech qanday cheklov qo'ymaslik
- Foydalanuvchidan parol so'rash
- Javobni yashirish

? Ma'lumot oqimi (data flow) nima?
+ Ma'lumot bir moduldan keyingisiga qanday o'tishi
- Daryodagi suv
- Internet tezligi
- Kompyuter kabeli

? Bot javobini sinab ko'rish uchun eng yaxshi usul qaysi?
+ Turli savollar yuborib, javoblarni tekshirish
- Faqat bitta savol yuborish
- Hech qachon sinamaslik
- Botni darhol o'chirish

? Avtomatlashtirishning asosiy foydasi nima?
+ Vaqtni tejaydi va takroriy ishdagi xatolarni kamaytiradi
- Har doim ko'proq ish yaratadi
- Kompyuterni sekinlashtiradi
- Hech qanday foydasi yo'q
""",
    "AI21": """
? Deployment (joylashtirish) nima?
+ Ilovani internetga joylab, boshqalar ocha oladigan qilish
- Ilovani o'chirish
- Kod yozishni boshlash
- Kompyuterni yangilash

? Hosting nima?
+ Sayt fayllari saqlanadigan va internetga uzatiladigan server xizmati
- Mehmon kutish
- Rasm muharriri
- Klaviatura turi

? Domen nima?
+ Sayt manzili (masalan, minartest.uz)
- Sayt rangi
- Kompyuter nomi
- Parol

? Netlify Drop orqali saytni qanday joylash mumkin?
+ Sayt papkasini sahifaga sudrab tashlash orqali
- Saytni qog'ozga chop etib
- Faqat telefon qo'ng'irog'i orqali
- Joylab bo'lmaydi

? Statik sayt nima?
+ Faqat HTML, CSS, JS fayllaridan iborat, server tomonda kod ishlamaydigan sayt
- Harakatsiz rasm
- Internetsiz ishlaydigan o'yin
- Ma'lumotlar bazasi

? Saytni joylashdan oldin kodda nima qolmasligi kerak?
+ Parollar va API kalitlari
- Sarlavhalar
- Rasmlar
- Tugmalar

? Sayt asosiy fayli odatda qanday nomlanadi?
+ index.html
- start.doc
- main.png
- home.mp3

? Joylashtirilgan saytni telefonda tekshirish nima uchun kerak?
+ Ko'p foydalanuvchilar telefondan kiradi — ko'rinish to'g'riligini tekshirish uchun
- Kerak emas
- Faqat telefon zaryadini bilish uchun
- Saytni o'chirish uchun

? HTTPS nima beradi?
+ Sayt bilan ma'lumot almashinuvini shifrlab, xavfsiz qiladi
- Saytni tezroq bo'yaydi
- Saytni yashiradi
- Faylni kattalashtiradi

? Saytga o'zgarish kiritgandan keyin nima qilish kerak?
+ Yangilangan fayllarni qayta joylash (redeploy) va natijani tekshirish
- Hech narsa, o'zi yangilanadi doim
- Saytni o'chirish
- Domenni sotish

? Ommaviy havola (public link) nima?
+ Har kim ocha oladigan sayt manzili
- Faqat sizga ko'rinadigan fayl
- Parol
- Xato xabari

? Sayt ochilmasa, birinchi navbatda nimani tekshirish kerak?
+ index.html fayli papka ildizida (asosiy joyida) ekanini
- Kompyuter rangini
- Klaviatura tilini
- Sichqoncha batareyasini
""",
    "AI22": """
? Final loyihaning to'g'ri tuzilmasi qaysi?
+ Muammo → Yechim → AI qayerda ishlatilgan → Demo → Kelajak rejasi
- Faqat demo
- Faqat musiqa
- Faqat logotip

? Mindmap nima?
+ Markaziy g'oyadan tarmoqlanuvchi fikrlar xaritasi
- Shahar xaritasi
- Kompyuter sxemasi
- Kitob mundarijasi

? Flowchart (blok-sxema) nima?
+ Jarayon qadamlarini va qarorlarni ko'rsatuvchi sxema
- Gul rasmi
- Musiqa notasi
- Rasm ramkasi

? MVP nima?
+ Asosiy muammoni hal qiladigan eng oddiy ishlaydigan versiya
- Eng ko'p funksiyali versiya
- Loyiha nomi
- Mukofot

? Yaxshi loyiha g'oyasi qanday bo'ladi?
+ Real muammoni hal qiladi va 2 haftada amalga oshirsa bo'ladi
- Juda ulkan va bajarib bo'lmaydi
- Hech qanday muammoni hal qilmaydi
- Faqat boshqa loyihaning nusxasi

? “Maqsadli foydalanuvchi” nima?
+ Loyiha kim uchun mo'ljallanganini bildiradi
- Loyiha muallifi
- Kompyuter
- Ustoz

? Whimsical AI nimaga yordam beradi?
+ Mindmap, flowchart va sxemalarni tez yaratishga
- Video montajga
- Musiqa yozishga
- Kod kompilyatsiyasiga

? Loyiha funksiyalarini tanlashda to'g'ri yo'l qaysi?
+ Eng muhim 3 ta funksiyani tanlab, avval ularni qilish
- Bir vaqtda 20 ta funksiya boshlash
- Funksiyasiz loyiha
- Faqat dizaynga e'tibor berish

? Elevator pitch nima?
+ G'oyani 30–60 soniyada qisqa va aniq tushuntirish
- Lift ta'mirlash
- Uzun ma'ruza
- Reklama banneri

? Loyihada AI qayerda ishlatilganini ko'rsatish nima uchun muhim?
+ Bu kursning asosiy maqsadi — AI yordamida yaratishni ko'rsatish
- Muhim emas
- Faqat reklama uchun
- Faqat ustoz bilishi kerak

? Loyiha rejasini tuzishda vaqtni qanday taqsimlash kerak?
+ Asosiy funksiyalar va sinovga yetarli vaqt qoldirib
- Hamma vaqtni dizaynga sarflab
- Oxirgi kunga qoldirib
- Rejasiz

? “AI Tutor” loyihasi qanday muammoni hal qiladi?
+ O'quvchiga savollariga uning darajasida tushuntirib beradi
- Kompyuterni tozalaydi
- Musiqa ijro etadi
- Rasm chop etadi
""",
    "AI23": """
? Prototip nima?
+ G'oyaning sinab ko'rish mumkin bo'lgan dastlabki ishlaydigan versiyasi
- Yakuniy mukammal mahsulot
- Loyiha nomi
- Faqat rasm

? Feedback (fikr-mulohaza) nima uchun kerak?
+ Foydalanuvchilar fikri asosida loyihani yaxshilash uchun
- Loyihani maqtash uchun
- Vaqtni o'tkazish uchun
- Kerak emas

? Prototipni sinashning to'g'ri usuli qaysi?
+ Boshqa odamga vazifa berib, uning ishlatishini kuzatish
- Faqat o'zingiz sinash
- Hech kimga ko'rsatmaslik
- Faqat ta'rifini o'qish

? Suno AI nima yaratadi?
+ Matnli tavsif bo'yicha qo'shiq va musiqa
- Video
- Rasm
- Taqdimot

? Musiqa promptida nimani ko'rsatish foydali?
+ Janr, temp, kayfiyat va cholg'u asboblari
- Faqat “musiqa”
- Faqat fayl hajmi
- Faqat sana

? Sound-design nima?
+ Loyiha uchun tovush va musiqa muhitini yaratish
- Rasm chizish
- Matn yozish
- Kod tuzatish

? Feedback'dan keyin nima qilish kerak?
+ Eng muhim kamchiliklarni ro'yxatlab, ularni tuzatish
- Barcha fikrlarni e'tiborsiz qoldirish
- Loyihani tashlab ketish
- Fikr bergan odam bilan bahslashish

? Loyiha fon musiqasi qanday bo'lishi kerak?
+ Loyiha kayfiyatiga mos va diqqatni chalg'itmaydigan
- Juda baland va shovqinli
- Loyihaga umuman aloqasiz
- Doim jim

? AI musiqasidan foydalanishda nimaga e'tibor berish kerak?
+ Platforma foydalanish shartlari (qayerda ishlatish mumkinligi)
- Hech narsaga
- Faqat fayl nomiga
- Faqat davomiyligiga

? Xatolar ro'yxati (bug list) nima uchun kerak?
+ Topilgan muammolarni unutmasdan tartib bilan tuzatish uchun
- Loyihani yomonlash uchun
- Ustozga shikoyat uchun
- Kerak emas

? Testlash davomida eng foydali savol qaysi?
+ “Qayerda qiynaldingiz va nimani tushunmadingiz?”
- “Loyiham zo'rmi?”
- “Menga baho berasizmi?”
- “Hech narsa so'ramaslik”

? Prototipdan yakuniy versiyaga o'tishda nima o'zgaradi?
+ Feedback asosida xatolar tuzatiladi va foydalanish qulayligi yaxshilanadi
- Hech narsa o'zgarmaydi
- Loyiha butunlay o'chiriladi
- Faqat nomi o'zgaradi
""",
    "AI24": """
? Demo Day nima?
+ O'quvchilar o'z loyihalarini hakamlar va ota-onalar oldida taqdim qiladigan kun
- Dam olish kuni
- Imtihon kuni
- Sport musobaqasi

? Yaxshi taqdimotda “jonli demo” nima uchun muhim?
+ Loyiha haqiqatan ishlashini ko'rsatadi
- Vaqtni cho'zish uchun
- Kerak emas
- Faqat musiqa uchun

? Taqdimot uchun ajratilgan vaqtga qanday munosabatda bo'lish kerak?
+ Belgilangan vaqtga (3–5 daqiqa) sig'ish
- Iloji boricha uzoq gapirish
- 30 soniyada tugatish
- Vaqtga e'tibor bermaslik

? Taqdimotni boshlashning yaxshi usuli qaysi?
+ Muammoni qiziqarli savol yoki hikoya bilan ko'rsatish
- “Bilmayman, nima deyishni”
- Darhol oxirgi slayddan boshlash
- Indamay turish

? Hakam savoliga javobni bilmasangiz, eng to'g'ri javob qaysi?
+ “Yaxshi savol, buni keyingi versiyada o'rganib chiqaman”
- Javobni to'qib chiqarish
- Savolni e'tiborsiz qoldirish
- Xafa bo'lish

? Portfolio nima?
+ O'z ishlaringiz (loyihalar, havolalar, natijalar) to'plami
- Sumka turi
- Imtihon varaqasi
- Kompyuter papkasi nomi

? Taqdimotning “Kelajak” qismida nima aytiladi?
+ Keyingi versiyada qo'shiladigan imkoniyatlar
- Kelajak haqida fantastik hikoya
- Ob-havo ma'lumoti
- Hech narsa

? Jonli demo ishlamay qolsa, oldindan qanday tayyorgarlik foydali?
+ Zaxira sifatida demo videosi yoki skrinshotlarni tayyorlab qo'yish
- Hech qanday tayyorgarlik qilmaslik
- Taqdimotni bekor qilish
- Kompyuterni almashtirish

? Taqdimot paytida tinglovchilar bilan qanday aloqa qilish kerak?
+ Ko'zlariga qarab, aniq va ishonch bilan gapirish
- Ekranga qarab, pichirlab gapirish
- Orqa o'girib turish
- Tez-tez telefonga qarash

? Demo Day'da baholashning asosiy mezonlari qaysi?
+ Loyiha ishlashi, taqdimot tuzilmasi va savollarga javob
- Faqat kiyim
- Faqat kompyuter narxi
- Faqat slaydlar soni

? Kurs yakunidagi asosiy natija qaysi?
+ 10+ mini loyiha, 1 ta final loyiha, Demo Day va sertifikat
- Faqat bitta rasm
- Faqat test bahosi
- Hech narsa

? “AI bilan gaplashma — AI yordamida yarat” shiori nimani anglatadi?
+ AI'dan faqat savol-javob uchun emas, real mahsulot yaratish uchun foydalanish
- AI bilan umuman gaplashmaslik
- Faqat rasm chizish
- AI'dan foydalanmaslik
""",
}
