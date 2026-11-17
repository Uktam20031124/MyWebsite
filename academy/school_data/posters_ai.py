"""AI Creator kursi: dars rasmlari (mavzu kaliti bo'yicha). Shakl — ``poster_kit``; manba — ``study_ai``."""

from .poster_kit import card, code, poster

POSTERS = {
    "AI01": poster(
        "AI — sehr emas: u <b>misollardan o'rganadi</b> va keyingi so'zni bashorat qiladi. Birinchi suhbatni quramiz.",
        ("flow", [
            ("Ma'lumot", "Millionlab matn, rasm va misollar."),
            ("O'rganish", "Model ulardan qonuniyatlarni topadi."),
            ("Prompt", "Siz topshiriq yoki savol yozasiz."),
            ("Bashorat", "Model eng ehtimolli keyingi so'zlarni tanlaydi."),
            ("Javob", "Tekshiring va kontekst bilan aniqlashtiring."),
        ]),
        [
            card("LLM", text="Til modeli <b>o'ylamaydi</b> — keyingi so'zni ehtimollik bo'yicha bashorat qiladi."),
            card("Noaniq → aniq", text="“Kosmos haqida yoz” emas — “<b>10 yoshli bolaga</b> Oy haqida <b>5 ta qiziq fakt</b> ayt”."),
            card("Kontekst", text="AI suhbatdagi avvalgi xabarlarni eslaydi — “yana qisqaroq qil” deb davom ettiring."),
        ],
        ("Aniq savol — aniq javob", "Kim uchun, nima kerak, qanday shaklda — hammasini yozing."),
        [
            ("Til modeli javobni qanday hosil qiladi?", "Keyingi so'zni ehtimollik bo'yicha bashorat qiladi."),
            ("Prompt nima?", "AI'ga beriladigan topshiriq yoki savol."),
            ("“Kosmos haqida yoz” promptini qanday yaxshilash mumkin?", "Auditoriya, mavzu va hajmni qo'shib: “10 yoshliga Oy haqida 5 fakt”."),
        ],
        title="AI qanday javob beradi?",
        badge=("AI", "1-dars"),
    ),
    "AI02": poster(
        "AI ham xato qiladi. Faktni <b>tekshiramiz</b>, halol ishlatamiz va shaxsiy ma'lumotni himoya qilamiz.",
        ("compare", {
            "bad": ("Mumkin emas", [
                "AI javobini tekshirmasdan ko'chirish",
                "Insho'ni AI'ga yozdirib, “o'zim yozdim” deyish",
                "Parol, karta, pasport raqamini yozish",
                "Uy manzili va telefonni aytish",
                "Bitta manbaga ishonish",
            ]),
            "good": ("To'g'ri foydalanish", [
                "Reja, g'oya va tushuntirish so'rash",
                "Matnni o'zingiz yozib, AI'dan fikr so'rash",
                "Faktni <b>2 ta ishonchli manbada</b> tekshirish",
                "AI yordam berganini ochiq aytish",
                "Shaxsiy ma'lumot o'rniga misol ishlatish",
            ]),
        }),
        [
            card("Hallucination", text="AI <b>ishonch bilan</b> noto'g'ri yoki mavjud bo'lmagan ma'lumot berishi mumkin."),
            card("Ikki manba qoidasi", formula="AI javobi + 2 manba = [fakt]", text="Rasmiy sayt, darslik, ilmiy maqola."),
            card("Plagiat", text="Birovning — jumladan AI'ning — ishini o'zingizniki qilib ko'rsatish."),
        ],
        ("AI — yordamchi, muallif — siz", "Javob uchun mas'uliyat sizda."),
        [
            ("Hallucination nima?", "AI ishonch bilan noto'g'ri ma'lumot berishi."),
            ("Muhim faktni nechta manbada tekshiramiz?", "Kamida 2 ta ishonchli manbada."),
            ("AI'ga qaysi ma'lumotni bermaymiz?", "Parol, karta, pasport, manzil, telefon."),
        ],
        title="Mumkin va mumkin emas",
        badge=("✓✕", "qoidalar"),
    ),
    "AI03": poster(
        "Soxta video, aldov xatlar va firibgarlarni <b>tanib olamiz</b> — AI davrida xavfsiz qolamiz.",
        ("tiles", [
            ("🎭", "Deepfake", "AI yasagan soxta video, rasm yoki ovoz."),
            ("🎣", "Fishing", "Aldov xat yoki havola orqali parol o'g'irlash."),
            ("🗣", "Ijtimoiy muhandislik", "Ishonchga kirib, sir oldirish."),
            ("🔐", "2FA", "Paroldan tashqari ikkinchi kod."),
            ("⚖", "Etika", "Birovning rasmi va ovozi — faqat ruxsat bilan."),
            ("✋", "To'xta", "Shoshiltirsa — to'xtab, tekshiring."),
        ]),
        [
            card("Deepfake belgilari", text="G'alati ko'z qisish, lab va ovoz mos emas, yuz chegarasi xira, soya noto'g'ri."),
            card("Fishing belgilari", text="“Tezda!”, “Bloklanadi!”, soxta manzil, parol yoki kod so'rash."),
            card("Tekshirish", text="Odamga <b>boshqa yo'l</b> bilan qo'ng'iroq qiling — xabardagi raqamga emas."),
        ],
        ("Shoshiltirish — xavf belgisi", "Haqiqiy tashkilot hech qachon parol yoki SMS kod so'ramaydi."),
        [
            ("Deepfake nima?", "AI yaratgan, haqiqiyga o'xshash soxta video, rasm yoki ovoz."),
            ("“Akkauntingiz 1 soatda o'chadi, kodni yuboring” — bu nima?", "Fishing."),
            ("Do'stingiz rasmidan AI bilan video yasash uchun nima kerak?", "Uning ruxsati."),
        ],
        title="Xavflar va himoya",
        badge=("🛡", "xavfsizlik"),
    ),
    "AI04": poster(
        "Yaxshi prompt <b>4 qismdan</b> iborat: rol, vazifa, kontekst va cheklovlar.",
        ("anatomy", [
            ("Rol — kim bo'lib javob beradi", "Sen bolalar yozuvchisisan."),
            ("Vazifa — nima qilish kerak", "Qisqa hikoya yoz"),
            ("Kontekst — kim uchun, qanday vaziyat", "9 yoshli bolalar uchun, do'stlik haqida,"),
            ("Cheklovlar — hajm, format, uslub", "150 so'z, sodda tilda, oxirida xulosa bilan."),
        ]),
        [
            card("Formula", formula="Rol + Vazifa + Kontekst + Cheklov = [prompt]"),
            card("Format so'rash", text="“Jadval qilib ber”, “3 ta band”, “avval reja, keyin matn” — natija shakli aniq bo'ladi."),
            card("Iteratsiya", text="Birinchi javob — qoralama. “Qisqaroq”, “quvnoqroq”, “misol qo'sh” deb yaxshilang."),
        ],
        ("Qancha aniq — shuncha yaxshi", "AI fikringizni o'qiy olmaydi — hammasini yozing."),
        [
            ("Yaxshi promptning 4 qismi?", "Rol, Vazifa, Kontekst, Cheklovlar."),
            ("“150 so'z, jadval ko'rinishida” — qaysi qism?", "Cheklovlar."),
            ("Iteratsiya nima?", "Natijaga qarab promptni bosqichma-bosqich yaxshilash."),
        ],
        title="Prompt anatomiyasi",
        badge=("4", "qism"),
    ),
    "AI05": poster(
        "Bir vazifa — har xil promptlar. <b>Mezon bo'yicha baholab</b>, eng yaxshisini tanlaymiz.",
        ("flow", [
            ("Vazifa", "Hamma uchun bir xil: maktab tadbiri reklamasi."),
            ("Prompt yozish", "5 daqiqa: rol, auditoriya, ohang, CTA."),
            ("Natija", "Har jamoa AI javobini ekranga chiqaradi."),
            ("Baholash", "Mezonlar bo'yicha 1–5 ball."),
            ("Tahlil", "G'olib prompt nimasi bilan yaxshi?"),
        ]),
        [
            card("Mezonlar", text="<b>Aniqlik</b>, <b>ijodkorlik</b>, <b>auditoriyaga moslik</b>, <b>uzunlik</b> — oldindan kelishiladi."),
            card("Ohang va auditoriya", text="Rasmiy, quvnoq yoki jiddiy — kimga yozayotganingizga qarab."),
            card("CTA", text="Harakatga chaqiriq: “Bugun ro'yxatdan o'ting!” — reklama shu bilan tugaydi."),
        ],
        ("Tanqid — promptga, odamga emas", "“Auditoriya ko'rsatilmagan” — foydali fikr."),
        [
            ("Prompt Battle'da g'olib qanday aniqlanadi?", "Oldindan kelishilgan mezonlar bo'yicha."),
            ("CTA nima?", "Harakatga chaqiriq: “Ro'yxatdan o'ting!”"),
            ("Bolalar uchun reklamada qanday ohang mos?", "Quvnoq, sodda."),
        ],
        title="Battle bosqichlari",
        badge=("⚔", "battle"),
    ),
    "AI06": poster(
        "Murakkab vazifalar uchun: <b>namunalar bilan o'rgatish</b> va bosqichma-bosqich o'ylatish.",
        ("tiles", [
            ("0", "Zero-shot", "Namunasiz, faqat vazifa: “Bu sharhni baholab ber”."),
            ("1·2·3", "Few-shot", "Vazifadan oldin 2–3 ta tayyor namuna."),
            ("→→", "Chain-of-Thought", "“Bosqichma-bosqich o'ylab, keyin javob ber”."),
            ("📄", "Kontekst oynasi", "Model bir vaqtda ko'ra oladigan matn hajmi."),
        ]),
        [
            card("Few-shot namuna", code="“Zo'r kino!” → ijobiy\n“Zerikarli.” → salbiy\n“Juda yoqdi!” → ?", text=""),
            card("CoT", text="Masala va mantiq savollarida AI kamroq adashadi: har qadamni yozadi va tekshiradi."),
            card("Tuzoqli masala", formula="raketka + to'p = 1100, farq 1000 → to'p = [50]", text=""),
        ],
        ("Murakkab masala — “bosqichma-bosqich”", "Formatni ko'rsatmoqchi bo'lsangiz — namuna bering."),
        [
            ("Few-shot va zero-shot farqi?", "Few-shot'da oldin namunalar beriladi, zero-shot'da yo'q."),
            ("Chain-of-Thought qachon foydali?", "Masala, mantiq va ko'p qadamli savollarda."),
            ("Kontekst oynasi nima?", "Model bir vaqtda ko'ra oladigan matn hajmi."),
        ],
        title="3 ta usul",
        badge=("CoT", "o'ylash"),
    ),
    "AI07": poster(
        "NotebookLM — <b>faqat sizning manbalaringiz</b> asosida javob beradigan o'quv yordamchi.",
        ("flow", [
            ("Manba yuklash", "Darslik bobi, PDF, maqola yoki havola."),
            ("Savol berish", "“Asosiy 5 fikrni ayt”."),
            ("Iqtibos", "Har javob manbaning qaysi joyidan olingani ko'rsatiladi."),
            ("Konspekt", "Qisqa tartibli yozuv va glossariy."),
            ("O'zini tekshirish", "AI tuzgan test bilan."),
        ]),
        [
            card("Manbaga asoslangan", text="Javoblar <b>faqat yuklangan hujjatlardan</b> — internetdan to'qib chiqarmaydi."),
            card("Iqtibos (citation)", text="Raqamni bosing — manbadagi aynan o'sha joy ochiladi. Tekshirish oson."),
            card("Glossariy", text="Yangi atamalar va ularning ma'nosi — imtihon oldidan takrorlash uchun."),
        ],
        ("AI konspekt yozadi — tushunish sizning ishingiz", "Konspektni o'z so'zlaringiz bilan qayta aytib bering."),
        [
            ("NotebookLM javoblari qayerdan olinadi?", "Faqat yuklangan manbalardan."),
            ("Iqtibos nima uchun kerak?", "Javob manbaning qaysi joyidan olinganini tekshirish uchun."),
            ("Glossariy nima?", "Yangi atamalar va ularning ma'nosi ro'yxati."),
        ],
        title="Manbadan bilimgacha",
        badge=("📓", "o'qish"),
    ),
    "AI08": poster(
        "Internetdagi ma'lumotni <b>tekshiramiz</b>: yaxshi savol, ishonchli manba va fact-check.",
        ("flow", [
            ("Savol", "Aniq: “O'zbekistonda 2024-yilda nechta universitet bor?”"),
            ("Manbalar", "Perplexity havolalarini oching."),
            ("Tekshirish", "Muallif, sana, tashkilot — ishonchlimi?"),
            ("Solishtirish", "2 ta mustaqil manba bir xil deydimi?"),
            ("Xulosa", "Manbalarni ko'rsatib, o'z so'zingiz bilan."),
        ]),
        [
            card("Ishonchli manba", text="Rasmiy tashkilot, ilmiy jurnal, <b>aniq muallif va sana</b>."),
            card("Feyk belgilari", text="Shov-shuvli sarlavha, manbasiz raqamlar, eski sana, faqat bitta sayt yozgan."),
            card("Ziddiyat", text="Manbalar har xil desa — sanasi yangi va rasmiyrog'iga ishoning, farqni ham yozing."),
        ],
        ("Ikki mustaqil manba — keyin ishoning", "Havolani ochmasdan AI xulosasiga tayanmang."),
        [
            ("Research tartibi qanday?", "Savol → manbalar → tekshirish → xulosa."),
            ("Ishonchli manbaning 3 belgisi?", "Rasmiy tashkilot, aniq muallif, sana."),
            ("Feyk yangilikning bir belgisi?", "Shov-shuvli sarlavha / manbasiz raqam / faqat bitta sayt."),
        ],
        title="Research tartibi",
        badge=("🔎", "fact-check"),
    ),
    "AI09": poster(
        "Gamma bilan matnni <b>bir necha daqiqada taqdimotga</b> aylantiramiz va qisqa pitch qilamiz.",
        ("compare", {
            "bad": ("AI qoralamasi", [
                "Har slaydda 10 qator matn",
                "Umumiy, kimga ekani noma'lum gaplar",
                "Rasmlar mavzuga mos emas",
                "Xulosa slaydi yo'q",
            ]),
            "good": ("Tahrirdan keyin", [
                "<b>1 slayd — 1 fikr</b>, ko'proq vizual",
                "Sarlavha → asosiy fikrlar → xulosa",
                "Kontrast: matn fonda yaxshi o'qiladi",
                "Oxirida aniq xulosa va savol",
            ]),
        }),
        [
            card("Gamma prompti", text="“<b>7–8 yoshlilar uchun</b>, suvni tejash haqida, <b>6 slayd</b>, quvnoq uslubda”."),
            card("Tahrirlash", text="AI natijasi — qoralama: ortiqcha matnni o'chiring, rasmlarni almashtiring."),
            card("30 soniyalik pitch", formula="muammo + yechim + chaqiriq = [pitch]", text=""),
        ],
        ("AI tez yasaydi — sifatni siz berasiz", "Har slaydni o'qib, keraksizini olib tashlang."),
        [
            ("Yaxshi slayd qoidasi?", "1 slayd — 1 fikr, kam matn."),
            ("Pitch nima?", "G'oyani qisqa va ishonarli taqdim qilish."),
            ("Gamma promptiga nimalarni yozish kerak?", "Auditoriya, mavzu, slaydlar soni, uslub."),
        ],
        title="Qoralamadan taqdimotgacha",
        badge=("▦", "slayd"),
    ),
    "AI10": poster(
        "Midjourney'da rasm prompti <b>qismlardan yig'iladi</b>: kim, nima, qayerda, qanday uslubda.",
        ("anatomy", [
            ("Obyekt", "qizil tulki"),
            ("Harakat", "kitob o'qiyapti"),
            ("Muhit", "qishki o'rmondagi kulbada,"),
            ("Uslub", "akvarel uslubida,"),
            ("Yorug'lik", "kamin iliq yorug'ligi,"),
            ("Kamera va parametr", "yaqin plan --ar 16:9"),
        ]),
        [
            card("Uslublar", text="Akvarel, piksel-art, kiberpank, 3D, multfilm — bitta so'z rasmni butunlay o'zgartiradi."),
            card("--ar", text="Tomonlar nisbati: <b>16:9</b> keng, <b>1:1</b> kvadrat, <b>9:16</b> tik (story)."),
            card("Kompozitsiya", text="Kamera burchagi: tepadan, yaqin plan, keng plan, pastdan."),
        ],
        ("Bittasini o'zgartiring — farqni ko'ring", "Uslub yoki yorug'likni almashtirib, 3 variant solishtiring."),
        [
            ("Rasm promptining asosiy qismlari?", "Obyekt, harakat, muhit, uslub, yorug'lik, kamera."),
            ("Instagram story uchun qaysi --ar?", "9:16"),
            ("“neon yorug'lik” — promptning qaysi qismi?", "Yorug'lik."),
        ],
        title="Rasm prompti qismlari",
        badge=("🎨", "rasm"),
    ),
    "AI11": poster(
        "O'yin qahramonini yaratamiz va uni <b>hamma rasmda bir xil</b> saqlaymiz.",
        ("flow", [
            ("Tavsif", "Yosh, kiyim, ranglar, xarakter — aniq yozing."),
            ("Konsept-art", "Birinchi variantlardan eng yaxshisini tanlang."),
            ("Image-to-Image", "Tanlangan rasmni asos qilib, yangi pozalar."),
            ("Negative prompt", "Bo'lmasligi kerak: xira, ortiqcha barmoq."),
            ("Turnaround", "Old, yon va orqa ko'rinish."),
        ]),
        [
            card("Izchillik", text="Yuz, kiyim va ranglar <b>har rasmda bir xil</b> — aks holda qahramon tanilmaydi."),
            card("Negative prompt", code="blurry, extra fingers,\ntext, watermark", text=""),
            card("Qahramon tarixi", text="Ismi, kuchi, zaif tomoni, orzusi — AI'dan 5 jumlada yozib berishni so'rang."),
        ],
        ("Bir xil tavsifni har safar takrorlang", "“qizil sharf, ko'k ko'zlar” kabi detallar o'zgarmasin."),
        [
            ("Negative prompt nima?", "Rasmda bo'lmasligi kerak narsalar ro'yxati."),
            ("Turnaround nima?", "Qahramonning old, yon va orqa ko'rinishi."),
            ("Qahramon har rasmda bir xil chiqishi uchun nima qilamiz?", "Image-to-Image va bir xil tavsif."),
        ],
        title="Qahramon yaratish yo'li",
        badge=("🧙", "qahramon"),
    ),
    "AI12": poster(
        "Brend yaratamiz: <b>logotip, ranglar va poster</b> — dizayn qoidalari va Ideogram bilan.",
        ("tiles", [
            ("◯", "Oddiy", "Logotip kichik o'lchamda ham o'qilsin."),
            ("★", "Esda qoladigan", "Bitta aniq g'oya va shakl."),
            ("3", "Rang palitrasi", "2–3 ta asosiy rang."),
            ("Aa", "Tipografika", "Shrift brend xarakteriga mos."),
            ("1→3", "Ierarxiya", "Eng muhim ma'lumot — eng ko'zga tashlanadigan."),
            ("UX", "UI / UX", "Ko'rinish va foydalanish qulayligi."),
        ]),
        [
            card("Logotip prompti", text="“<b>Minimalist</b> logotip, kitob va lampochka, ko'k va oltin, oq fon, matnsiz”."),
            card("Poster", text="Ideogram matnni yaxshi yozadi: sarlavha, sana va joyni qo'shtirnoqda bering."),
            card("5 soniya testi", text="Posterni 5 soniya ko'rsating: nima, qachon, qayerda — eslab qolishdimi?"),
        ],
        ("Kam rang, kam shrift — kuchli brend", "Har joyda bir xil logotip va ranglar."),
        [
            ("Logotipning 3 asosiy qoidasi?", "Oddiy, esda qoladigan, kichikda ham o'qiladi."),
            ("Brend uchun nechta asosiy rang yetarli?", "2–3 ta."),
            ("UI va UX farqi?", "UI — ko'rinish, UX — foydalanish qulayligi."),
        ],
        title="Brend dizayni qoidalari",
        badge=("◆", "brend"),
    ),
    "AI13": poster(
        "Rasmni jonlantiramiz: Runway'da <b>harakat va kamera</b> bilan qisqa video kadr yaratamiz.",
        ("anatomy", [
            ("Sahna", "Tog' ko'li bo'yida yolg'iz qayiq,"),
            ("Harakat", "suv sekin to'lqinlanadi, tuman suzadi,"),
            ("Kamera harakati", "kamera sekin yaqinlashadi (zoom in),"),
            ("Kayfiyat", "tinch, sirli tong."),
        ]),
        [
            card("Kamera harakatlari", text="<b>Zoom in</b> — yaqinlashish, <b>pan</b> — gorizontal burilish, <b>orbit</b> — atrofida aylanish."),
            card("Bitta aniq harakat", text="Bir kadrda bitta asosiy harakat — ko'p narsa so'ralsa video buziladi."),
            card("Loop", text="Oxiri boshiga uzluksiz ulanadigan video — fon va post uchun qulay."),
        ],
        ("AI video — bir necha soniya", "Uzun video kerak bo'lsa — kadrlarni montajda ulang."),
        [
            ("Video promptining 4 qismi?", "Sahna, harakat, kamera harakati, kayfiyat."),
            ("Kamera obyekt atrofida aylansa — bu qaysi harakat?", "Orbit."),
            ("Loop video nima?", "Oxiri boshiga uzluksiz ulanadigan video."),
        ],
        title="Video prompti qismlari",
        badge=("🎬", "video"),
    ),
    "AI14": poster(
        "Bir necha AI kliplardan <b>mini-treyler</b> yig'amiz: storyboard, izchillik va montaj.",
        ("flow", [
            ("Storyboard", "Sahnalar rejasi: 3–5 kadr qog'ozda."),
            ("Boshlanish", "Qiziqtiruvchi birinchi kadr."),
            ("Asosiy sahnalar", "Luma'da har sahna — alohida klip."),
            ("Montaj", "CapCut'da kliplar, o'tishlar va musiqa."),
            ("Sarlavha", "Oxirida nom va sana."),
        ]),
        [
            card("Treyler formulasi", formula="qiziqtirish + sahnalar + sarlavha = [treyler]", text=""),
            card("Izchillik", text="Har klipda qahramon va uslub bir xil: <b>bir xil tavsif</b> va asosiy rasm."),
            card("O'tish (transition)", text="Sahnalar orasidagi ravon effekt — ortiqcha bo'lmasin."),
        ],
        ("Avval storyboard — keyin generatsiya", "Reja bo'lmasa, kliplar bir-biriga ulanmaydi."),
        [
            ("Storyboard nima?", "Sahnalarning ketma-ket rejasi."),
            ("Kliplarni bitta videoga qayerda birlashtiramiz?", "Montaj dasturida (CapCut)."),
            ("Treyler qanday tugaydi?", "Sarlavha — nom va sana bilan."),
        ],
        title="Treyler yo'li",
        badge=("🎞", "treyler"),
    ),
    "AI15": poster(
        "ElevenLabs bilan matnni <b>jonli ovozga</b> aylantiramiz va qahramonlarni ovozlashtiramiz.",
        ("compare", {
            "bad": ("Robot kabi o'qiydi", [
                "Uzun jumlalar, tinish belgisiz",
                "Raqamlar: “2026”",
                "Qisqartmalar: “va h.k.”",
                "Hamma qahramon bir xil ovozda",
            ]),
            "good": ("Jonli eshitiladi", [
                "Qisqa jumlalar, vergul va nuqta — <b>pauza</b>",
                "So'z bilan: “ikki ming yigirma oltinchi”",
                "To'liq yozilgan so'zlar",
                "Har qahramonga alohida ovoz va ohang",
            ]),
        }),
        [
            card("Text-to-Speech", text="Matnni sun'iy ovoz bilan o'qish. <b>Voice-over</b> — video ustidan diktor ovozi."),
            card("Tinish belgilari", text="Vergul — qisqa pauza, nuqta — uzun pauza, “!” va “?” — intonatsiya."),
            card("Voice cloning", text="Ovozni nusxalash — <b>faqat o'z ovozingiz</b> yoki aniq ruxsat bilan."),
        ],
        ("Birovning ovozini ruxsatsiz nusxalamang", "Bu aldov va qonunbuzarlik bo'lishi mumkin."),
        [
            ("Ovozda pauza qilish uchun matnga nima qo'shamiz?", "Tinish belgilari: vergul, nuqta."),
            ("Voice-over nima?", "Video ustidan diktor ovozi."),
            ("Kimning ovozini klonlash mumkin?", "O'zingizniki yoki aniq ruxsat berganniki."),
        ],
        title="Matnni ovozga tayyorlash",
        badge=("🎙", "ovoz"),
    ),
    "AI16": poster(
        "AI yordamida <b>HTML, CSS va JS</b> bilan birinchi veb-sahifa — vizitkani yasaymiz.",
        code('''
<h1>Laylo Karimova</h1>
<p>Dizayner · 14 yosh</p>
<img src="foto.jpg">
<a href="https://t.me/laylo">
  Telegram</a>
<button onclick="alert('Salom!')">
  Salom ayt</button>
<style>
  h1 { color: navy; }
  p { font-size: 20px; }
</style>
''', '''
Laylo Karimova   ← katta sarlavha
Dizayner · 14 yosh
[ rasm ]
Telegram          ← havola
[ Salom ayt ]     ← tugma
''', lang="text", run=False),
        [
            card("HTML — tuzilma", text="<code>&lt;h1&gt;</code> sarlavha, <code>&lt;p&gt;</code> matn, <code>&lt;img&gt;</code> rasm, <code>&lt;a href&gt;</code> havola."),
            card("CSS — ko'rinish", text="<code>color</code> — rang, <code>font-size</code> — o'lcham, <code>background</code> — fon."),
            card("JS — harakat", text="Tugma bosilganda nimadir bo'lishi: <code>onclick</code>."),
        ],
        ("AI kodini o'qing va tushuning", "“Har qatorni izohlab ber” deb so'rang."),
        [
            ("Eng katta sarlavha qaysi teg?", "<h1>"),
            ("Matn rangini qaysi CSS xususiyati o'zgartiradi?", "color"),
            ("Havola qaysi teg bilan yoziladi?", "<a href=\"...\">"),
        ],
        title="Vizitka sahifasi",
        badge=("</>", "HTML"),
    ),
    "AI17": poster(
        "v0.dev'da so'z bilan <b>ilova interfeysini</b> yasaymiz: To-do list MVP.",
        ("window", {"app": "To-do list — MVP", "parts": [
            ("Sarlavha", "ilova nomi va bugungi sana", "field", "Bugungi vazifalar · 17-noyabr"),
            ("Kiritish maydoni", "yangi vazifa yozish", "field", "Uy vazifasini qilish…"),
            ("Qo'shish tugmasi", "komponent — qayta ishlatiladi", "button", "+ Qo'shish"),
            ("Vazifalar ro'yxati", "holat (state) — hozirgi ma'lumot", "list", "☐ Kitob o'qish"),
            ("Filtr", "keyingi versiya uchun", "tabs", ["Hammasi", "Bajarilgan", "Qolgan"]),
        ]}),
        [
            card("MVP", text="Eng oddiy <b>ishlaydigan</b> versiya: qo'shish, belgilash, o'chirish — qolgani keyin."),
            card("Komponent va holat", text="<b>Komponent</b> — tugma, karta, forma. <b>Holat</b> — ro'yxatdagi vazifalar."),
            card("Foydalanuvchi oqimi", formula="yoz → qo'sh → belgila → [bajarildi]", text=""),
        ],
        ("Avval MVP — keyin bezak", "Har yangi funksiyadan keyin sinab ko'ring."),
        [
            ("MVP nima?", "Eng oddiy ishlaydigan versiya."),
            ("To-do ilovada “holat” nima?", "Hozirgi vazifalar ro'yxati."),
            ("Komponentga misol?", "Tugma, karta yoki forma."),
        ],
        title="Ilova interfeysi",
        badge=("MVP", "ilova"),
    ),
    "AI18": poster(
        "Xatoni topamiz va tuzatamiz: <b>xato xabarini o'qish</b>, AI bilan debugging va refaktoring.",
        code('''
# Mantiqiy xato: o'rtacha noto'g'ri
ball = [80, 90, 70]
jami = 0
for b in ball:
    jami += b
print(jami / 2)        # ← xato
print(jami / len(ball))  # ← to'g'ri
''', '''
120.0
80.0
'''),
        [
            card("Sintaksis xatosi", text="Til qoidasi buzilgan — dastur <b>umuman ishlamaydi</b>: ikki nuqta, qavs, chekinish."),
            card("Mantiqiy xato", text="Dastur ishlaydi, lekin <b>natija noto'g'ri</b> — eng qiyini, test bilan topiladi."),
            card("Xato xabari", formula="turi + [qator raqami]", text="<code>SyntaxError: line 4</code> — qayerga qarashni aytadi."),
        ],
        ("AI'ga kod + xato xabari + kutgan natijani bering", "“Ishlamayapti” deyish yetmaydi."),
        [
            ("Dastur ishlaydi, lekin javob noto'g'ri. Bu qanday xato?", "Mantiqiy xato."),
            ("Refaktoring nima?", "Ishlashini o'zgartirmay, kodni tartibli qilish."),
            ("AI'dan yordam so'rashda nimalarni beramiz?", "Kod, xato xabari va kutilgan natija."),
        ],
        title="Xatoni topish",
        badge=("🐞", "debug"),
    ),
    "AI19": poster(
        "AI ilovalar ichida qanday ishlaydi: <b>model, API va JSON</b> — so'rov va javob.",
        code('''
POST /models/sentiment
{
  "inputs": "Bu kino juda zo'r!"
}
''', '''
[
  {"label": "POSITIVE",
   "score": 0.98}
]
''', lang="text", run=False),
        [
            card("API", formula="Request → [Response]", text="Dasturlar ma'lumot almashadigan “eshik”."),
            card("JSON", text="“Kalit: qiymat” formati: <code>\"label\": \"POSITIVE\"</code>, <code>\"score\": 0.98</code>."),
            card("API kaliti", text="Maxfiy “parol” — <b>hech kimga berilmaydi</b>, kodga ochiq yozilmaydi."),
        ],
        ("Model — o'rgatilgan dastur, API — unga yo'l", "Hugging Face'da modelni brauzerda sinab ko'ring."),
        [
            ("API nima?", "Dasturlar ma'lumot almashadigan “eshik”."),
            ("JSON'da score 0.98 nimani bildiradi?", "Model 98% ishonch bilan javob berdi."),
            ("API kalitini nega yashiramiz?", "Kim bilsa, sizning nomingizdan foydalanadi."),
        ],
        title="So'rov va javob",
        badge=("API", "JSON"),
    ),
    "AI20": poster(
        "Make.com'da modullarni ulab, <b>ishni avtomatlashtiramiz</b>: Telegram bot + AI javob.",
        ("flow", [
            ("Trigger", "Telegram botga yangi xabar keldi."),
            ("Modul: AI", "Xabar matnidan javob yaratish."),
            ("Modul: filtr", "Faqat savol bo'lsa davom etish."),
            ("Modul: yuborish", "Javobni foydalanuvchiga qaytarish."),
            ("Sinov", "Run once — har qadamni tekshirish."),
        ]),
        [
            card("Scenario", text="Ulangan modullardan iborat sxema — har biri bitta ish."),
            card("Ma'lumot oqimi", formula="xabar → AI → [javob]", text="Oldingi modul natijasi keyingisiga o'tadi."),
            card("Xatoni topish", text="Har modul ustidagi pufakchani bosing — qayerda to'xtaganini ko'rasiz."),
        ],
        ("Avval qo'lda bajaring — keyin avtomatlashtiring", "Jarayonni qadamlarga bo'lib yozib oling."),
        [
            ("Trigger nima?", "Sxemani ishga tushiradigan hodisa."),
            ("Scenario nimadan iborat?", "Ulangan modullardan."),
            ("Har kuni 8:00 da xabar yuborish uchun trigger qanday?", "Vaqt bo'yicha (Schedule)."),
        ],
        title="Avtomatlashtirish sxemasi",
        badge=("⚙", "avto"),
    ),
    "AI21": poster(
        "Saytni internetga chiqaramiz: Netlify'da <b>bir necha daqiqada</b> joylashtirish.",
        ("flow", [
            ("Papka", "index.html, style.css, script.js — bitta joyda."),
            ("Tekshirish", "index.html papka ildizida."),
            ("Netlify", "Papkani sudrab tashlang (Deploy)."),
            ("Manzil", "nom.netlify.app — HTTPS bilan."),
            ("Yangilash", "O'zgargan papkani qayta yuklang."),
        ]),
        [
            card("Hosting va domen", text="<b>Hosting</b> — fayllar turadigan server, <b>domen</b> — sayt manzili."),
            card("Statik sayt", text="Faqat HTML, CSS, JS fayllar — Netlify bepul joylashtiradi."),
            card("HTTPS", text="Xavfsiz, shifrlangan ulanish — manzil oldida qulf belgisi."),
        ],
        ("index.html — papka ildizida bo'lishi shart", "Aks holda sayt “Page not found” ko'rsatadi."),
        [
            ("Saytning asosiy fayli qanday nomlanadi?", "index.html"),
            ("Hosting va domen farqi?", "Hosting — server, domen — manzil."),
            ("HTTPS nima beradi?", "Xavfsiz, shifrlangan ulanish."),
        ],
        title="Deploy qadamlari",
        badge=("🌐", "deploy"),
    ),
    "AI22": poster(
        "Final loyiha g'oyasini tuzamiz: <b>muammodan yechimgacha</b> va Whimsical'da sxema.",
        ("flow", [
            ("Muammo", "Kimning qanday muammosi bor?"),
            ("Yechim", "Loyiha uni qanday hal qiladi?"),
            ("AI qayerda", "Qaysi qismda AI ishlaydi?"),
            ("Demo", "MVP: 3 ta asosiy funksiya."),
            ("Kelajak", "Keyingi versiyada nima qo'shiladi?"),
        ]),
        [
            card("Misol: AI Tutor", text="Muammo — uy vazifasida yordam yo'q. Yechim — savolga bosqichma-bosqich tushuntiradigan bot."),
            card("Maqsadli foydalanuvchi", text="Loyiha <b>kim uchun</b>: “5–7-sinf o'quvchilari”, “hamma” emas."),
            card("Mindmap va flowchart", text="<b>Mindmap</b> — g'oyalar xaritasi, <b>flowchart</b> — jarayon sxemasi."),
        ],
        ("Kichik, lekin ishlaydigan — katta, lekin chala emas", "MVP'ga 3 ta asosiy funksiya yetarli."),
        [
            ("Loyiha formulasining 5 qismi?", "Muammo, Yechim, AI qayerda, Demo, Kelajak."),
            ("MVP'da nechta asosiy funksiya bo'lgani ma'qul?", "3 ta."),
            ("Flowchart nima?", "Jarayonning qadamma-qadam sxemasi."),
        ],
        title="Loyiha formulasi",
        badge=("💡", "g'oya"),
    ),
    "AI23": poster(
        "Prototipni <b>sinab, tuzatib</b>, Suno bilan loyihaga musiqa va tovush beramiz.",
        ("anatomy", [
            ("Janr", "Yengil elektron"),
            ("Temp", "o'rtacha tezlikda,"),
            ("Kayfiyat", "quvnoq va ilhomlantiruvchi,"),
            ("Cholg'u", "sintezator va qo'ng'iroqchalar, so'zsiz."),
        ]),
        [
            card("Testlash", text="3 ta do'stga ilovani bering — <b>yordam bermang</b>, faqat kuzating va yozib oling."),
            card("Eng foydali savol", text="“Qayerda qiynaldingiz?” — “Yoqdimi?” dan ko'ra ko'proq foyda beradi."),
            card("Bug list", text="Topilgan xatolar ro'yxati: nima, qayerda, qanchalik muhim."),
        ],
        ("Feedback — sovg'a, tanqid emas", "Har bir fikrni yozing, keyin eng muhimini tuzating."),
        [
            ("Musiqa promptining 4 qismi?", "Janr, temp, kayfiyat, cholg'u."),
            ("Bug list nima?", "Topilgan xatolar ro'yxati."),
            ("Test paytida foydalanuvchiga yordam beramizmi?", "Yo'q — kuzatamiz va yozib olamiz."),
        ],
        title="Musiqa prompti",
        badge=("♪", "sound"),
    ),
    "AI24": poster(
        "DEMO DAY: loyihani <b>3 daqiqada ishonarli</b> taqdim qilamiz va savollarga javob beramiz.",
        ("flow", [
            ("Muammo", "30 s: hikoya yoki raqam bilan boshlang."),
            ("Yechim", "30 s: loyiha nima qiladi."),
            ("AI", "30 s: qayerda va qanday ishlatilgan."),
            ("Jonli demo", "60 s: ishlashini ko'rsating."),
            ("Kelajak", "30 s: keyingi qadamlar va rahmat."),
        ]),
        [
            card("Vaqt", formula="30 + 30 + 30 + 60 + 30 = [180 s]", text="Uyda soat bilan 2 marta mashq qiling."),
            card("Zaxira", text="Internet yoki demo ishlamasa — <b>video yoki skrinshotlar</b> tayyor tursin."),
            card("Bilmagan savol", text="“Yaxshi savol — buni hali sinamadim, keyingi versiyada tekshiraman” — halol javob."),
        ],
        ("Jonli demo — eng kuchli dalil", "Loyiha haqiqatan ishlashini ko'rsating."),
        [
            ("Taqdimot tuzilmasining 5 qismi?", "Muammo, Yechim, AI, Jonli demo, Kelajak."),
            ("Demo ishlamay qolsa nima qilamiz?", "Zaxira video yoki skrinshotlarni ko'rsatamiz."),
            ("Portfolio nima?", "Barcha ishlaringiz to'plami."),
        ],
        title="3 daqiqalik pitch",
        badge=("🏆", "demo day"),
    ),
}
