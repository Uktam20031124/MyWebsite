"""Minar AI Creator — 2 oylik sun'iy intellekt kursi (9–17 yosh).

8 hafta × 3 dars = 24 dars, har biri 60 daqiqa. Falsafa: 20% nazariya + 80% amaliyot —
"Bugun nimani o'rgandim?" emas, "Bugun nimani yaratdim?".

Dars formati (60 daq.): kirish 5 → ustoz demo 10 → yangi tushuncha 10 → amaliyot 25 →
challenge 5 → show & tell 5. Baholash — 100 ball (yo'qlamadagi "Ball" ustuniga).

Yosh bo'yicha: ko'p AI vositalari 13+ (ba'zilari 18+) yoshdan ruxsat beradi — 9–12 yoshdagilar
uchun vosita ustoz akkauntida namoyish qilinadi, o'quvchilar prompt va g'oyani o'zlari tuzadi.
"""

from . import ModuleData as M
from . import TopicData as T

AGE_NOTE = (
    "\n\nYosh bo'yicha:\n"
    "- 9–12 yosh: vosita ustoz akkauntida, o'quvchi prompt va g'oyani o'zi tuzadi; topshiriq soddaroq.\n"
    "- 13–17 yosh: o'z akkaunti (ota-ona ruxsati bilan), murakkabroq topshiriq va mustaqil ish."
)


def lesson(goal: str, tool: str, demo: str, concept: str, practice: str, challenge: str, grading: str) -> str:
    """Mavzu tavsifi — barcha darslarda bir xil tuzilma (60 daqiqa)."""
    return (
        f"Maqsad: {goal}\n\n"
        f"AI vositasi: {tool}\n\n"
        "Dars rejasi (60 daq.):\n"
        "1. Kirish va qiziqtirish: savol yoki qisqa misol — 5 daq.\n"
        f"2. Ustoz demo: {demo} — 10 daq.\n"
        f"3. Yangi tushuncha: {concept} — 10 daq.\n"
        f"4. O'quvchi amaliyoti: {practice} — 25 daq.\n"
        f"5. Challenge / mini musobaqa: {challenge} — 5 daq.\n"
        "6. Show & Tell: 2–3 o'quvchi natijasini ko'rsatadi — 5 daq.\n\n"
        f"Baholash (100 ball):\n{grading}"
        f"{AGE_NOTE}"
    )


WEEK1 = M(
    "AI Creator 1 · AI bilan tanishuv",
    "Sun'iy intellekt nima, u qayerda ishlatiladi va undan xavfsiz, mas'uliyatli foydalanish qoidalari. "
    "Asosiy prinsip: “AI javob berdi” degani “bu haqiqat” degani emas.",
    [
        T(
            "AI01",
            "AI nima o‘zi? ChatGPT bilan birinchi muloqot",
            lesson(
                "sun'iy intellekt tushunchasi, qisqa tarixi va kundalik hayotdagi o'rnini tushunish; "
                "ChatGPT'ga aniq savol berishni o'rganish.",
                "ChatGPT",
                "AI qayerda ishlatiladi (tavsiyalar, tarjimon, ovozli yordamchi, navigator); ChatGPT'ga "
                "bir xil savolni noaniq va aniq shaklda berib, javoblarni solishtirish",
                "AI, mashinali o'rganish, til modeli (LLM), chatbot; AI “o'ylamaydi” — matnni bashorat qiladi",
                "ChatGPT bilan 10 ta savol-javob: o'zi haqida, sevimli fani, kelajak kasbi; har bir "
                "javobdan 1 ta yangi fakt yozib olish",
                "“Kim aniqroq so'raydi?” — bir mavzuda eng foydali javob olgan savol g'olib",
                "- AI tushunchasini o'z so'zi bilan tushuntiradi — 30\n"
                "- Kamida 10 ta aniq savol bergan — 40\n"
                "- Javoblardan yangi faktlarni yozib olgan — 30",
            ),
            "ChatGPT yordamida “Kelajakda AI kasblari” mavzusida 5 ta savoldan iborat intervyu "
            "tayyorlang: savol + AI javobi + o'zingizning fikringiz (1–2 gap).",
            "https://chatgpt.com\nhttps://openai.com/chatgpt/overview/",
            60,
        ),
        T(
            "AI02",
            "AI’dan foydalanish qoidalari: xatolar, plagiat va shaxsiy ma'lumot",
            lesson(
                "AI javoblaridagi xatolarni (hallucination) aniqlash, plagiatdan saqlanish va shaxsiy "
                "ma'lumotlarni himoya qilishni o'rganish.",
                "Microsoft Copilot",
                "Copilot'dan manbali javob olish; AI ataylab xato qilgan misolni topib, manba orqali tekshirish",
                "hallucination (AI “to'qib chiqargan” fakt), manba, plagiat; AI'ga berilmaydigan ma'lumotlar: "
                "parol, karta, pasport, uy manzili, boshqalarning shaxsiy ma'lumoti",
                "Copilot bilan 5 ta faktni so'rash va har birini 2 ta ishonchli manba bilan tekshirish; "
                "“berish mumkin / mumkin emas” ma'lumotlar jadvalini tuzish",
                "“Xatoni top” — ustoz bergan AI matnidagi 3 ta noto'g'ri faktni birinchi topgan g'olib",
                "- Faktlarni manba bilan tekshirgan — 40\n"
                "- Shaxsiy ma'lumotlar jadvali to'g'ri — 30\n"
                "- Plagiat va mualliflikni tushuntira oladi — 30",
            ),
            "Copilot bergan 3 ta faktdan iborat matnni tekshiring: har bir fakt yoniga “to'g'ri” yoki "
            "“xato” deb yozing va manba havolasini qo'shing.",
            "https://copilot.microsoft.com",
            60,
        ),
        T(
            "AI03",
            "AI xavfsizligi amaliyoti: deepfake, fishing va etika",
            lesson(
                "deepfake, fishing va qalbakilashtirish xavflarini tanish, AI botlarni xavfsiz sinash.",
                "Poe",
                "Poe'dagi turli botlarga bir xil savol berish; shaxsiy ma'lumot so'raydigan xavfli "
                "so'rovni tanib, rad etish",
                "deepfake (soxta video/ovoz), fishing (aldov xat/havola), ijtimoiy muhandislik, etika: "
                "boshqa odamning rasmi va ovozidan ruxsatsiz foydalanmaslik",
                "3 ta botni xavfsizlik nuqtai nazaridan sinash; har bir bot uchun “nimani so'radi, "
                "nimani bermaslik kerak” xulosasini yozish",
                "“Xavfli yoki xavfsiz?” — ustoz o'qigan 10 ta vaziyatni tez va to'g'ri ajratish",
                "- Deepfake va fishing belgilarini aytib bera oladi — 40\n"
                "- Botlarni sinash xulosasi — 30\n"
                "- Etika qoidalariga amal qiladi — 30",
            ),
            "Poe botlari uchun 5 ta “xavfsiz” va 5 ta “xavfli” (shaxsiy ma'lumot so'raydigan) prompt "
            "ro'yxatini tuzing; har bir xavfli prompt yoniga nima uchun xavfli ekanini yozing.",
            "https://poe.com",
            60,
        ),
    ],
)

WEEK2 = M(
    "AI Creator 2 · Prompt engineering",
    "Yaxshi prompt tuzilmasi (Rol, Vazifa, Kontekst, Cheklovlar), promptlar musobaqasi va murakkab "
    "promptlar: few-shot va bosqichma-bosqich fikrlash (Chain-of-Thought).",
    [
        T(
            "AI04",
            "Yaxshi prompt nima? Rol, Vazifa, Kontekst, Cheklovlar",
            lesson(
                "prompt tuzilmasini o'rganish va Claude'dan sifatli, aniq natija olish.",
                "Claude",
                "“Hikoya yoz” va to'liq tuzilmali promptni solishtirish: rol, vazifa, kontekst, cheklov, format",
                "prompt formulasi: Rol + Vazifa + Kontekst + Cheklovlar (+ natija formati); iterativ yaxshilash",
                "bitta vazifa uchun 3 bosqichli prompt: oddiy → kontekstli → to'liq tuzilmali; natijalarni "
                "jadvalda solishtirish",
                "“Eng aniq prompt” — natijani birinchi urinishda kerakli formatda olgan o'quvchi",
                "- Promptda 4 ta qism ham bor — 40\n"
                "- 3 bosqichli taqqoslash qilingan — 30\n"
                "- Natija talab qilingan formatda — 30",
            ),
            "Claude uchun 3 bosqichli mukammal prompt tuzing (oddiy → yaxshilangan → mukammal) va har "
            "bosqich natijasini taqqoslab, qaysi qism eng ko'p ta'sir qilganini yozing.",
            "https://claude.ai\nhttps://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
            60,
        ),
        T(
            "AI05",
            "Prompt Battle: bir vazifa — eng yaxshi natija",
            lesson(
                "bir xil vazifaga turli promptlar berib, eng samarali usulni tajribada aniqlash.",
                "Google Gemini",
                "bitta reklama vazifasiga 3 xil prompt; natijalarni mezon bo'yicha baholash",
                "baholash mezonlari: aniqlik, ijodkorlik, auditoriyaga moslik, uzunlik; prompt variatsiyalari",
                "jamoalarda Prompt Battle: 3 raund, har raundda yangi cheklov (so'zlar soni, uslub, auditoriya)",
                "Final: sinf ovozi bilan eng yaxshi natija va uning prompti tahlili",
                "- Raundlarda faol qatnashgan — 30\n"
                "- Cheklovlarga amal qilgan — 40\n"
                "- O'z promptini tahlil qila oladi — 30",
            ),
            "Gemini yordamida maktab tadbiri uchun reklama matnini eng yaxshi ko'rinishga keltiradigan "
            "prompt yarating: kamida 3 ta versiya va nima uchun oxirgisi eng yaxshi ekanini yozing.",
            "https://gemini.google.com",
            60,
        ),
        T(
            "AI06",
            "Murakkab promptlar: few-shot va Chain-of-Thought",
            lesson(
                "namunalar (few-shot) va bosqichma-bosqich fikrlash (Chain-of-Thought) orqali murakkab "
                "topshiriqlarni hal qilish.",
                "Groq",
                "mantiqiy masalani avval “javobni ayt”, keyin “bosqichma-bosqich yech” deb so'rash va "
                "farqni ko'rsatish; Groq'ning tezligi",
                "zero-shot, few-shot (2–3 ta namuna berish), Chain-of-Thought; kontekst oynasi",
                "3 ta masala: few-shot bilan matn turini aniqlash, CoT bilan mantiqiy masala, natijani tekshirish",
                "“Kim tez va to'g'ri?” — CoT bilan masalani to'g'ri yechgan birinchi o'quvchi",
                "- Few-shot prompt to'g'ri tuzilgan — 30\n"
                "- CoT bilan masala to'g'ri yechilgan — 40\n"
                "- AI javobini o'zi tekshirgan — 30",
            ),
            "Groq interfeysida Chain-of-Thought usulidan foydalanib murakkab mantiqiy masalani "
            "bosqichma-bosqich yeching va har bir bosqich to'g'riligini o'zingiz tekshiring.",
            "https://groq.com\nhttps://console.groq.com/playground",
            60,
        ),
    ],
)

WEEK3 = M(
    "AI Creator 3 · AI bilan o'qish va research",
    "Hujjatlardan o'rganish (NotebookLM), manbali qidiruv va fact-check (Perplexity), ma'lumotni "
    "taqdimotga aylantirish (Gamma).",
    [
        T(
            "AI07",
            "AI bilan o‘qish va o‘rganish: NotebookLM",
            lesson(
                "hujjat va PDF'lardan konspekt, savollar va qisqa xulosa tayyorlashni o'rganish.",
                "NotebookLM",
                "darslik bobini yuklab, undan konspekt, savollar va audio-xulosa olish; javoblar qaysi "
                "sahifadan olinganini ko'rsatish",
                "manbaga asoslangan AI (faqat yuklangan hujjatdan javob), iqtibos, konspekt va o'z-o'zini tekshirish",
                "o'z darsligidan 1 bobni yuklash: 5 ta asosiy fikr, 5 ta test savoli va lug'at",
                "“Kitob ichidan” — ustoz savoliga NotebookLM manbasi bilan birinchi javob bergan o'quvchi",
                "- Konspekt aniq va qisqa — 40\n"
                "- Test savollari hujjatga mos — 30\n"
                "- Javoblarni manba bilan tekshirgan — 30",
            ),
            "Maktab darsligining 1 ta bobini NotebookLM'ga yuklab, avtomatik test va qisqa konspekt "
            "yarating; 2 ta javobni kitobdan o'zingiz tekshiring.",
            "https://notebooklm.google.com",
            60,
        ),
        T(
            "AI08",
            "AI Research va fact-check: Perplexity AI",
            lesson(
                "internetdan manbalarga asoslangan ma'lumot qidirish va faktlarni tekshirishni o'rganish.",
                "Perplexity AI",
                "bitta savolga Perplexity javobi va manbalarini ochib tekshirish; ishonchli va "
                "ishonchsiz manbani ajratish",
                "ishonchli manba belgilari (rasmiy sayt, ilmiy jurnal, sana), fact-check bosqichlari, "
                "ikki manba qoidasi",
                "kichik izlanish: 1 savol → 3 ta manba → xulosa; har bir faktni ikkinchi manba bilan tasdiqlash",
                "“Fakt yoki feyk?” — 5 ta da'voni manbalar bilan eng tez tekshirgan jamoa",
                "- Kamida 3 ta ishonchli manba — 40\n"
                "- Faktlar ikkinchi manba bilan tasdiqlangan — 30\n"
                "- Xulosa o'z so'zlari bilan yozilgan — 30",
            ),
            "Perplexity AI orqali “Koinotni o'rganish” mavzusida manbalar havola qilingan kichik "
            "izlanish tayyorlang (5–7 gap + kamida 3 ta havola).",
            "https://www.perplexity.ai",
            60,
        ),
        T(
            "AI09",
            "Matn va ma'lumotni taqdimotga aylantirish: Gamma App",
            lesson(
                "matn va ma'lumotlarni tahlil qilib, AI yordamida chiroyli taqdimot yoki veb-sahifa yaratish.",
                "Gamma App",
                "bitta matndan Gamma'da taqdimot yaratish, keyin tuzilma, rasm va dizaynni qo'lda tahrirlash",
                "yaxshi slayd qoidalari: 1 slayd — 1 fikr, kam matn, vizual; AI qoralamasi → inson tahriri",
                "o'z mavzusidan 5 slaydli taqdimot: sarlavha, 3 ta asosiy fikr, xulosa; har slaydni tahrirlash",
                "“30 soniyalik pitch” — taqdimotni 30 soniyada eng aniq tushuntirgan o'quvchi",
                "- 5 slayd, har birida bitta fikr — 40\n"
                "- AI qoralamasi qo'lda tahrirlangan — 30\n"
                "- Taqdimotni ravon tushuntiradi — 30",
            ),
            "Gamma yordamida o'zingiz yoqtirgan sevimli mashg'ulot haqida 5 slaydli taqdimot yarating "
            "va havolasini ustozga yuboring.",
            "https://gamma.app",
            60,
        ),
    ],
)

WEEK4 = M(
    "AI Creator 4 · AI dizayn",
    "AI bilan rasm yaratish (Midjourney), o'yin qahramonlari dizayni (Leonardo AI), logotip, poster va "
    "brending (Ideogram).",
    [
        T(
            "AI10",
            "AI bilan rasm yaratish: Midjourney",
            lesson(
                "AI image generation asoslarini o'rganish: uslub, yorug'lik, kompozitsiya va parametrlar.",
                "Midjourney",
                "bitta g'oyani uslub, yorug'lik va kompozitsiya qo'shib bosqichma-bosqich yaxshilash; "
                "--ar (tomonlar nisbati) va --v (versiya) parametrlari",
                "rasm prompti tuzilmasi: obyekt + harakat + muhit + uslub + yorug'lik + kamera burchagi + parametrlar",
                "“Fantastik shahar” mavzusida 3 xil uslubda rasm (masalan, kiberpank, akvarel, piksel-art)",
                "“Eng ko'p ovoz” — sinf eng yoqtirgan rasm va uning prompti",
                "- Promptda uslub, yorug'lik va kompozitsiya bor — 40\n"
                "- Parametrlardan to'g'ri foydalangan — 30\n"
                "- 3 xil uslubdagi natija — 30",
            ),
            "Midjourney orqali fantastik uslubdagi shahar arxitekturasining 3 xil rasmini yarating va "
            "har birining promptini yozib qo'ying.",
            "https://www.midjourney.com\nhttps://docs.midjourney.com",
            60,
        ),
        T(
            "AI11",
            "AI + Design: o'yin qahramoni dizayni (Leonardo AI)",
            lesson(
                "Image-to-Image va prompt generatsiyasi orqali izchil o'yin qahramoni dizaynini ishlash.",
                "Leonardo AI",
                "qahramon g'oyasidan konsept-art, keyin Image-to-Image bilan turli pozalar va kiyimlar",
                "konsept-art, izchillik (bir qahramon — bir xil ko'rinish), Image-to-Image, negative prompt",
                "o'z qahramoni: ism, xarakter, kuchi; 3 ta varianti va eng yaxshisining 2 ta pozasi",
                "“Qahramonlar paradi” — eng izchil va o'ziga xos qahramon",
                "- Qahramon g'oyasi va tavsifi aniq — 30\n"
                "- Izchil dizayn (bir xil qiyofa) — 40\n"
                "- Image-to-Image'dan foydalangan — 30",
            ),
            "Leonardo AI orqali o'zingiz o'ylab topgan kompyuter o'yini qahramonining konseptual "
            "rasmini yarating; qahramonning qisqa tarixini (3–4 gap) yozing.",
            "https://leonardo.ai",
            60,
        ),
        T(
            "AI12",
            "Brending va UI/UX asoslari: logotip va poster (Ideogram)",
            lesson(
                "grafik dizayn va tipografika asoslari; AI yordamida matnli logotip va poster yaratish.",
                "Ideogram",
                "brend uchun 3 ta logotip varianti, keyin shu uslubdagi poster; matnning to'g'ri yozilishini tekshirish",
                "brend: nom, rang palitrasi, shrift, uslub; logotip qoidalari (oddiy, esda qoladigan, kichikda ham "
                "o'qiladi); poster ierarxiyasi",
                "o'z brendi yoki o'quv markazi uchun logotip va 1 ta poster; ranglar va shrift tanlovini asoslash",
                "“5 soniya testi” — 5 soniya ko'rib eslab qolingan logotip",
                "- Logotip oddiy va o'qiladi — 40\n"
                "- Poster ierarxiyasi aniq — 30\n"
                "- Rang va shrift tanlovi asoslangan — 30",
            ),
            "Ideogram yordamida o'z brendingiz yoki o'quv markazingiz uchun logotip hamda poster "
            "tayyorlang; brend ranglarini (2–3 ta) yozing.",
            "https://ideogram.ai",
            60,
        ),
    ],
)

WEEK5 = M(
    "AI Creator 5 · AI video va ovoz",
    "Text-to-Video va Image-to-Video (Runway), kinematografik kliplar (Luma Dream Machine), AI ovoz va "
    "ovozlashtirish (ElevenLabs).",
    [
        T(
            "AI13",
            "AI Video: Runway bilan harakatdagi kadrlar",
            lesson(
                "Text-to-Video va Image-to-Video texnologiyalari bilan qisqa dinamik video yaratish.",
                "Runway (Gen-3)",
                "tayyor rasmni 5 soniyalik videoga aylantirish; harakat va kamera yo'nalishini promptda berish",
                "video prompti: sahna + harakat + kamera (zoom, pan, orbit) + kayfiyat; kadr, sekund, loop",
                "o'z rasmidan (4-haftadagi) 5 soniyalik animatsiya: 2 ta variant, harakatni o'zgartirib",
                "“Eng jonli kadr” — eng tabiiy harakatli video",
                "- Promptda harakat va kamera bor — 40\n"
                "- 5 soniyalik video tayyor — 30\n"
                "- Variantlarni solishtirgan — 30",
            ),
            "Runway yordamida tayyor rasmdan 5 soniyalik dinamik animatsion video yarating.",
            "https://runwayml.com",
            60,
        ),
        T(
            "AI14",
            "AI Content Creator: Luma Dream Machine bilan mini-treyler",
            lesson(
                "kinematografik video kliplar yaratish va kamera harakatlarini boshqarish.",
                "Luma Dream Machine",
                "3 ta sahnadan iborat mini-treyler rejasi (storyboard) va har sahnani generatsiya qilish",
                "storyboard, sahna ketma-ketligi, kamera harakatlari, kinematografik uslub; montajda birlashtirish",
                "15–20 soniyalik mini-treyler: 3 ta sahna + sarlavha; oddiy montaj (CapCut yoki boshqa)",
                "“Premyera” — sinfda eng qiziqarli treyler",
                "- Storyboard tuzilgan — 30\n"
                "- 3 ta sahna izchil — 40\n"
                "- Montaj va sarlavha — 30",
            ),
            "Luma Dream Machine yordamida qisqa kinematografik mini-treyler yarating (3 ta sahna, 15–20 soniya).",
            "https://lumalabs.ai/dream-machine",
            60,
        ),
        T(
            "AI15",
            "Ovoz va animatsiya: ElevenLabs bilan ovozlashtirish",
            lesson(
                "AI Text-to-Speech bilan professional ovozlashtirish; ovozdan etik foydalanish.",
                "ElevenLabs",
                "bitta matnni turli ovoz, tezlik va hissiyot bilan o'qitish; tinish belgilarining ta'siri",
                "Text-to-Speech, ovoz parametrlari (barqarorlik, hissiyot), voice cloning va uning etikasi: "
                "faqat o'z ovozi yoki ruxsat bilan",
                "o'z hikoyasini (5–6 gap) ovozlashtirish va 5-haftadagi videoga voice-over sifatida qo'shish",
                "“Ovoz aktyori” — hissiyotni eng yaxshi bergan audio",
                "- Matn ovozlashtirish uchun tayyorlangan — 30\n"
                "- Ovoz va hissiyot to'g'ri tanlangan — 40\n"
                "- Etika qoidalariga amal qilgan — 30",
            ),
            "O'zingiz yozgan hikoya matnini ElevenLabs platformasida audio shaklga keltiring.",
            "https://elevenlabs.io",
            60,
        ),
    ],
)

WEEK6 = M(
    "AI Creator 6 · AI + Coding",
    "AI yordamida kod yozish (Replit AI), prompt orqali interfeys yaratish (v0.dev) va AI muharriri "
    "bilan xatolarni tuzatish (Cursor).",
    [
        T(
            "AI16",
            "AI bilan kod yozish: Replit AI va HTML/CSS/JS",
            lesson(
                "brauzerda kod yozish va AI yordamchi bilan oddiy veb-sahifa strukturasini yaratish.",
                "Replit AI",
                "AI'dan vizitka sahifa so'rash, kodni qatorma-qator tushuntirish, keyin o'zgartirish",
                "HTML (tuzilma), CSS (ko'rinish), JS (harakat); AI kodini tushunmasdan nusxalamaslik",
                "shaxsiy vizitka sayt: ism, rasm, qiziqishlar, aloqa tugmasi; 2 ta o'zgarishni o'zi kiritish",
                "“Tugmani jonlantir” — JS bilan tugmaga eng qiziq harakat qo'shgan o'quvchi",
                "- Sahifa ishlaydi va tuzilmasi to'g'ri — 40\n"
                "- Kodni tushuntira oladi — 30\n"
                "- O'zi kiritgan o'zgarishlar — 30",
            ),
            "Replit AI orqali shaxsiy vizitka saytingizning kodini tayyorlang va havolasini yuboring.",
            "https://replit.com",
            60,
        ),
        T(
            "AI17",
            "Birinchi Mini App: v0.dev bilan interfeys",
            lesson(
                "prompt orqali interaktiv foydalanuvchi interfeysi va komponentlarni yaratish.",
                "v0.dev",
                "“To-do list” interfeysini prompt bilan yaratish va bosqichma-bosqich takomillashtirish",
                "UI/UX asoslari: komponent, holat (state), foydalanuvchi oqimi; mini ilova rejasi",
                "Kalkulyator yoki To-do list: asosiy funksiya + 1 ta qo'shimcha imkoniyat (masalan, tungi rejim)",
                "“Demo 60 soniya” — ilovasini eng ravon ko'rsatgan o'quvchi",
                "- Interfeys ishlaydi — 40\n"
                "- Qo'shimcha imkoniyat qo'shilgan — 30\n"
                "- Foydalanuvchi oqimi tushuntirilgan — 30",
            ),
            "v0.dev yordamida “Kalkulyator” yoki “To-do list” interfeysini yarating.",
            "https://v0.dev",
            60,
        ),
        T(
            "AI18",
            "Kodni tuzatish (debugging) va optimallashtirish: Cursor",
            lesson(
                "AI muharriri yordamida koddagi xatolarni topish, tushuntirish va refaktoring qilish.",
                "Cursor",
                "xatoli koddan xato xabarini o'qish, AI'dan sababini so'rash va tuzatishni tekshirish",
                "xato turlari (sintaksis, mantiqiy), xato xabarini o'qish, debugging bosqichlari, refaktoring",
                "ustoz bergan 3 ta xatoli dasturni tuzatish va har biriga “xato nima edi” izohini yozish",
                "“Bug hunter” — eng ko'p xatoni to'g'ri topgan o'quvchi",
                "- Xatolar tuzatilgan va kod ishlaydi — 40\n"
                "- Har bir xato sababi tushuntirilgan — 40\n"
                "- Kod tartibli (refaktoring) — 20",
            ),
            "Cursor yordamida berilgan xatoli kodni tuzating, to'g'ri ishlashini ta'minlang va qaysi "
            "xatolar bo'lganini yozing.",
            "https://cursor.com",
            60,
        ),
    ],
)

WEEK7 = M(
    "AI Creator 7 · AI integratsiya",
    "AI qanday ishlaydi: model, API, request/response va JSON (Hugging Face); no-code integratsiya "
    "(Make.com); veb-ilovani internetga joylash (Netlify).",
    [
        T(
            "AI19",
            "AI qanday ishlaydi? Model, API va JSON (Hugging Face)",
            lesson(
                "ochiq modellar, API, request, response va JSON tushunchalarini amaliy darajada tushunish.",
                "Hugging Face",
                "Hugging Face Spaces'da 2–3 ta demo modelni sinash (rasm tanish, matn tahlili); "
                "API so'rov va JSON javob namunasi",
                "model va ma'lumotlar to'plami, API, request → response, JSON (kalit: qiymat), API kaliti xavfsizligi",
                "3 ta model sinovi jadvali: vazifa, kiruvchi ma'lumot, natija, xato holatlari; JSON namunasini o'qish",
                "“JSON detektiv” — JSON javobdan kerakli qiymatni birinchi topgan o'quvchi",
                "- 3 ta model sinovi jadvali — 40\n"
                "- API va JSON'ni tushuntira oladi — 40\n"
                "- API kaliti xavfsizligini biladi — 20",
            ),
            "Hugging Face platformasida o'zingizga yoqqan 1 ta ochiq AI modelni sinab ko'ring va u "
            "haqida sharh yozing (nima qiladi, qayerda foydali, qayerda xato qildi).",
            "https://huggingface.co\nhttps://huggingface.co/spaces",
            60,
        ),
        T(
            "AI20",
            "AI API bilan mini loyiha: Make.com avtomatlashtirish",
            lesson(
                "no-code integratsiya: trigger → harakat sxemasi bilan AI bot yaratish.",
                "Make.com",
                "Telegram bot → AI modul → javob sxemasi; API kalitini xavfsiz saqlash",
                "avtomatlashtirish (scenario), trigger, modul, ma'lumot oqimi; xatolarni kuzatish",
                "oddiy Telegram bot: savolga AI javobi yoki kunning iqtibosi; sxemani chizib, ishga tushirish",
                "“Botimga savol ber” — sinfdoshlar sinab ko'radi, eng foydali bot",
                "- Sxema ishlaydi — 40\n"
                "- Trigger va modullarni tushuntira oladi — 30\n"
                "- API kaliti xavfsiz saqlangan — 30",
            ),
            "Make.com orqali Telegram botga avtomatik AI javob berish integratsiyasini ulang.",
            "https://www.make.com",
            60,
        ),
        T(
            "AI21",
            "Veb-ilovani joylashtirish (Deployment): Netlify",
            lesson(
                "yaratilgan veb-ilovani internetga nashr qilish va ommaviy havola olish.",
                "Netlify",
                "papkani Netlify Drop'ga tashlab sayt yaratish; sayt nomini o'zgartirish va yangilash",
                "hosting, deploy, domen va havola, statik sayt; xavfsizlik: kodda parol yoki API kaliti qoldirmaslik",
                "6-haftadagi vizitka yoki mini ilovani joylash, havolani telefonda tekshirish",
                "“Birinchi bo'lib onlayn” — saytini birinchi ishga tushirgan o'quvchi",
                "- Sayt internetda ochiladi — 50\n"
                "- Telefonda tekshirilgan — 20\n"
                "- Kodda maxfiy ma'lumot yo'q — 30",
            ),
            "Oldingi darsda tayyorlangan mini veb-ilovani Netlify'ga joylang va havolasini yuboring.",
            "https://www.netlify.com\nhttps://app.netlify.com/drop",
            60,
        ),
    ],
)

WEEK8 = M(
    "AI Creator 8 · Final loyiha va Demo Day",
    "Final loyiha: g'oya va arxitektura (Whimsical), prototip va sound-design (Suno), Demo Day — "
    "loyiha taqdimoti (Muammo → Yechim → AI → Demo → Kelajak) va sertifikat.",
    [
        T(
            "AI22",
            "Final loyiha: g‘oya va arxitektura (Whimsical)",
            lesson(
                "final loyiha g'oyasini tanlash va uning tuzilmasini mindmap/flowchart ko'rinishida loyihalash.",
                "Whimsical AI",
                "“AI Tutor” g'oyasidan mindmap va foydalanuvchi oqimi (flowchart) yaratish",
                "loyiha formulasi: Muammo → Yechim → AI qayerda → Demo → Kelajak; MVP (eng kichik ishlaydigan versiya)",
                "o'z final loyihasi: muammo, maqsadli foydalanuvchi, 3 ta asosiy funksiya, mindmap",
                "“Elevator pitch” — g'oyani 30 soniyada eng aniq tushuntirgan o'quvchi",
                "- Muammo va yechim aniq — 40\n"
                "- Mindmap va funksiyalar ro'yxati — 40\n"
                "- MVP realistik — 20",
            ),
            "Whimsical AI orqali final loyihangizning mindmap sxemasini chizib keling.",
            "https://whimsical.com",
            60,
        ),
        T(
            "AI23",
            "Final loyiha: prototip, testlash va sound-design (Suno)",
            lesson(
                "prototipni yig'ish, sinfdoshlarda testlash va loyiha uchun mualliflik musiqasini yaratish.",
                "Suno AI",
                "loyiha kayfiyatiga mos musiqa prompti (janr, temp, kayfiyat, cholg'u)",
                "prototip va testlash: foydalanuvchi fikri (feedback), xatolar ro'yxati, takomillashtirish",
                "prototipni yig'ish, 2 ta sinfdoshda sinash, 3 ta yaxshilashni kiritish; fon musiqasi",
                "“Feedback raundi” — eng foydali fikr bergan va olgan juftlik",
                "- Prototip ishlaydi — 40\n"
                "- Feedback asosida yaxshilangan — 30\n"
                "- Musiqa loyihaga mos — 30",
            ),
            "Suno AI platformasida final loyihangiz uchun fon musiqasi yoki saundtrek yarating.",
            "https://suno.com",
            60,
        ),
        T(
            "AI24",
            "DEMO DAY: loyiha taqdimoti va sertifikat",
            lesson(
                "final loyihani 3–5 daqiqada hakamlar va ota-onalar oldida taqdim qilish.",
                "Pitch (AI taqdimot)",
                "namunaviy 3 daqiqalik pitch: muammo → yechim → AI → jonli demo → kelajak rejasi",
                "yaxshi taqdimot: hikoya, jonli demo, vaqtga rioya, savollarga javob; portfolio",
                "taqdimot slaydlari va jonli demo; har bir o'quvchi 3–5 daqiqa + 1–2 savol",
                "hakamlar baholashi va sinf mukofotlari (eng foydali, eng ijodiy, eng yaxshi demo)",
                "- Loyiha ishlaydi (jonli demo) — 40\n"
                "- Taqdimot tuzilmasi va vaqt — 30\n"
                "- Savollarga javob — 30",
            ),
            "Loyiha natijalarini jamlab portfolioga joylang: havola, skrinshotlar, qisqa tavsif va "
            "“keyingi versiyada nima qo'shaman” bo'limi.",
            "https://pitch.com",
            60,
        ),
    ],
)

MODULES = [WEEK1, WEEK2, WEEK3, WEEK4, WEEK5, WEEK6, WEEK7, WEEK8]
TRACK = [t.key for m in MODULES for t in m.topics]  # AI guruhi dasturi — 24 dars tartibda
