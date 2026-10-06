"""Python kursi: noldan OOP va Telegram botgacha.

Bitta katalogdan ikki xil yo'nalish foydalanadi (dastur tartibi guruhda beriladi):
- Starter bitiruvchilari (S-009, S005) — PY01 dan boshlab ketma-ket;
- Python Pro (P-006) — o'tilganlaridan keyin tuzilmalar, shartlar, ..., OOP va loyihalar.

Har bir dars 90 daq.: ~25 daq. nazariya + jonli kod, ~50 daq. masalalar, ~15 daq. tekshirish.
Baholash (100 ball): darsdagi masalalar — 50, uy vazifasi — 40, kod tozaligi — 10.
"""

from . import ModuleData as M
from . import TopicData as T

DOCS = "https://docs.python.org/3/tutorial/"

BASICS = M(
    "Python 1 · Asoslar: o'zgaruvchilar, operatorlar, shartlar",
    "Muhitni sozlash, ma'lumot turlari, input/print, operatorlar va tarmoqlanuvchi algoritmlar.",
    [
        T(
            "PY01",
            "Pythonga kirish: o'rnatish, VS Code, print va birinchi dastur",
            """Maqsad: Python va VS Code'ni o'rnatish, .py fayl yaratib ishga tushirish.

Dars rejasi:
1. Python nima, qayerda ishlatiladi (veb, AI, avtomatlashtirish, botlar).
2. O'rnatish: python.org (Windows'da "Add to PATH" belgisi!), VS Code + Python kengaytmasi.
3. Terminalda: python --version, python fayl.py; REPL (>>>) bilan tajriba.
4. print(), izohlar (#), sintaksis xatolari va ularni o'qish.

Darsdagi masalalar:
1. "Hello, World!" va o'z ismingizni chiqaring.
2. print() bilan ASCII-rasm (uy yoki yurak) chizing.
3. sep= va end= parametrlari bilan "2026-10-06" sanasini chiqaring.""",
            """1. O'zingiz haqingizda 5 qatorli "vizitka"ni print bilan chiqaring.
2. print("A" * 20) dan foydalanib ramka chizing.
3. Ataylab 3 xil xato qiling (qavs, qo'shtirnoq, tab) va xato xabarini izohlab yozing.""",
            "https://www.python.org/downloads/\nhttps://code.visualstudio.com/docs/python/python-tutorial",
        ),
        T(
            "PY02",
            "O'zgaruvchilar va ma'lumot turlari: int, float, str, bool",
            """Maqsad: o'zgaruvchi yaratish, nomlash qoidalari va asosiy turlar.

Dars rejasi:
1. O'zgaruvchi = nom → qiymat; nomlash: snake_case, kalit so'zlar taqiqlangan.
2. int, float, str, bool; type() funksiyasi.
3. Bir nechta o'zgaruvchiga birdan qiymat berish, qiymatlarni almashtirish (a, b = b, a).
4. Konstantalar (KATTA_HARF) va izohlar.

Darsdagi masalalar:
1. Ism, yosh, bo'y (float), o'quvchimi (bool) o'zgaruvchilari va type() natijasi.
2. Ikki o'zgaruvchi qiymatini uchinchi o'zgaruvchisiz almashtiring.
3. Doira yuzi: PI = 3.14159, r = 5 → yuza va uzunlik.""",
            """1. Mahsulot: nomi, narxi, soni → umumiy summani chiqaring.
2. Sekundlarni soat:daqiqa:sekundga aylantiring (masalan, 3725 → 1:02:05).
3. 5 ta noto'g'ri o'zgaruvchi nomi yozib, nega noto'g'riligini izohlang.""",
            DOCS + "introduction.html",
        ),
        T(
            "PY03",
            "Tiplarni o'zgartirish (type conversion) va input()",
            """Maqsad: foydalanuvchidan ma'lumot olish va turlarni to'g'ri aylantirish.

Dars rejasi:
1. input() har doim str qaytaradi — nega "2" + "3" = "23".
2. int(), float(), str(), bool() — aylantirish va ValueError.
3. round(), abs() va f-string bilan chiroyli natija: f"{x:.2f}".

Darsdagi masalalar:
1. Ikki son kiritilsa, yig'indi, ayirma, ko'paytma va bo'linmani chiqaring.
2. Tug'ilgan yil → yosh.
3. Selsiy → Farengeyt (F = C × 9/5 + 32), 1 xona aniqlikda.""",
            """1. "Kalkulyator": 2 son va amal (+ - * /) so'rab, natijani chiqaring.
2. Narx va chegirma foizi → chegirmadan keyingi narx.
3. bool("0"), bool(""), bool(0), int("12.5") natijalarini tushuntiring.""",
            DOCS + "inputoutput.html",
        ),
        T(
            "PY04",
            "String metodlari, indekslash va f-string",
            """Maqsad: matn bilan ishlash — kesish, qidirish, almashtirish va formatlash.

Dars rejasi:
1. Indeks (0 dan) va manfiy indeks, slicing s[a:b:c], s[::-1].
2. Metodlar: upper, lower, title, strip, replace, split, join, find, count, startswith.
3. len(), in operatori; f-string va formatlash.

Darsdagi masalalar:
1. Ism-familiyani kiritib, bosh harflarni chiqaring ("Karimov Laziz" → "K.L.").
2. So'z palindrommi (katta-kichik harfni hisobga olmasdan)?
3. Gapdagi so'zlar soni va eng uzun so'z.""",
            """1. Telefon raqamini "+998 90 123 45 67" formatiga keltiring (kiritish: 901234567).
2. Matndagi unli harflar sonini toping.
3. Email'dan login va domenni ajrating ("ali@gmail.com" → "ali", "gmail.com").""",
            "https://docs.python.org/3/library/stdtypes.html#string-methods",
        ),
        T(
            "PY05",
            "Arifmetik operatorlar: + - * / // % **",
            """Maqsad: matematik amallar va ularning ustuvorligi.

Dars rejasi:
1. Barcha arifmetik operatorlar; // (butun bo'linma) va % (qoldiq) farqi.
2. Amallar ustuvorligi va qavslar; ** daraja va ildiz (x ** 0.5).
3. Qisqa yozuv: +=, -=, *=, /=.

Darsdagi masalalar:
1. Uch xonali sonning raqamlari yig'indisi (// va % bilan).
2. Minutni soat va minutga aylantiring.
3. Pifagor: katetlar → gipotenuza.""",
            """1. N kunni hafta va kunga aylantiring (17 → 2 hafta 3 kun).
2. Omonat: summa, yillik foiz, yil → murakkab foiz bilan yakuniy summa.
3. 4 xonali sonni teskari tartibda chiqaring (faqat arifmetika bilan).""",
            DOCS + "introduction.html#numbers",
        ),
        T(
            "PY06",
            "Taqqoslash va mantiqiy operatorlar: and, or, not",
            """Maqsad: rost/yolg'on ifodalar tuzish — shartlarga tayyorgarlik.

Dars rejasi:
1. ==, !=, <, >, <=, >=; zanjirli taqqoslash (0 < x < 10).
2. and, or, not; haqiqat jadvali.
3. is va == farqi (qisqacha), in operatori.

Darsdagi masalalar:
1. Son juft va musbatmi? (bitta bool ifoda)
2. Yil kabisa yilimi? ((y % 4 == 0 and y % 100 != 0) or y % 400 == 0)
3. Uchburchak tengsizligi bajariladimi?""",
            """1. Login uzunligi 5–15 va faqat harf/raqammi (isalnum) — True/False.
2. Yosh 7–18 orasida bo'lsa "o'quvchi" ekanini bool bilan chiqaring.
3. 6 ta ifoda yozib, natijasini oldindan taxmin qiling, keyin tekshiring.""",
            "https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not",
        ),
        T(
            "PY07",
            "Shart operatorlari: if, elif, else",
            """Maqsad: tarmoqlanuvchi algoritmlar yozish.

Dars rejasi:
1. if / elif / else sintaksisi, indentatsiya (4 bo'sh joy).
2. Shartlar tartibi nega muhim (avval eng aniq shart).
3. Qisqa if: x = "juft" if n % 2 == 0 else "toq".

Darsdagi masalalar:
1. Ball (0–100) → baho: 86+ "a'lo", 71+ "yaxshi", 56+ "qoniqarli", aks holda "qoniqarsiz".
2. Uch sonning eng kattasi (max() ishlatmasdan).
3. Yil fasli: oy raqami → "qish/bahor/yoz/kuz".""",
            """1. Tana massasi indeksi (BMI) va natija toifasi.
2. Kalkulyatorni yaxshilang: 0 ga bo'lishni tekshiring, noma'lum amal uchun xabar.
3. Taksi narxi: 3 km gacha 10 000 so'm, keyin har km 2 500 so'm; tunda (22–06) +20%.""",
            DOCS + "controlflow.html#if-statements",
        ),
        T(
            "PY08",
            "Ichma-ich shartlar, match-case va RegEx bilan tekshiruvlar",
            """Maqsad: murakkab shartlar va matnni andoza (RegEx) bilan tekshirish.

Dars rejasi:
1. Ichma-ich if va uni and/or bilan soddalashtirish.
2. match-case (Python 3.10+) — menyu tanlovi.
3. re.fullmatch bilan validatsiya: telefon, email, parol kuchi.

Darsdagi masalalar:
1. Parol kuchi: 8+ belgi, katta harf, raqam, maxsus belgi → "kuchsiz/o'rta/kuchli".
2. Telefon "+998XXXXXXXXX" formatidami (re.fullmatch)?
3. match-case bilan konsol menyu: 1 — salom, 2 — sana, 3 — chiqish.""",
            """1. Login validatori: 5–15 belgi, harf bilan boshlanadi, faqat harf/raqam/_ (RegEx).
2. Bankomat: PIN tekshirish, balans, yechish (balansdan oshmasin, 10 000 ga karrali).
3. Kiritilgan sana "KK.OO.YYYY" formatda va to'g'ri sanami (oy 1–12, kun 1–31).""",
            "https://docs.python.org/3/library/re.html\n" + DOCS + "controlflow.html#match-statements",
        ),
    ],
)

STRUCTURES = M(
    "Python 2 · Ma'lumotlar tuzilmalari: list, tuple, set, dict",
    "To'plamlar bilan ishlash, ularning farqi va murakkab (ichma-ich) ma'lumotlar.",
    [
        T(
            "PY09",
            "List: yaratish, indekslash va slicing",
            """Maqsad: ro'yxat tushunchasi, elementlarga murojaat va o'zgartirish.

Dars rejasi:
1. [] va list(); indeks, manfiy indeks, slicing.
2. Element o'zgartirish, len(), in, min/max/sum.
3. list o'zgaruvchan (mutable) — nusxa olish: copy() va [:].

Darsdagi masalalar:
1. 7 kunlik harorat ro'yxati: o'rtacha, eng issiq, eng sovuq kun.
2. Ro'yxatning birinchi va oxirgi 3 elementi (slicing).
3. Ro'yxatni teskari tartibda chiqaring (2 xil usulda).""",
            """1. Guruhingizdagi 5 ta o'quvchi ismi: alifbo tartibida va eng uzun ism.
2. Baholar ro'yxati → o'rtacha va o'rtachadan yuqori baholar soni.
3. a = [1, 2]; b = a; b.append(3) — nima uchun a ham o'zgardi? Tushuntiring.""",
            DOCS + "introduction.html#lists",
        ),
        T(
            "PY10",
            "List metodlari va list comprehension",
            """Maqsad: ro'yxatni boshqarish metodlari va qisqa yozuv.

Dars rejasi:
1. append, insert, extend, remove, pop, index, count, sort, reverse, clear.
2. sorted() va sort() farqi, key= parametri.
3. List comprehension: [x * 2 for x in nums if x > 0].

Darsdagi masalalar:
1. "Xarid ro'yxati": qo'shish, o'chirish, tartiblash.
2. 1–50 orasidagi juft sonlar kvadratlari (comprehension).
3. Ro'yxatdan takrorlanuvchilarni tartibni saqlagan holda olib tashlash.""",
            """1. To-do ro'yxat: 5 ta vazifa qo'shing, 2 tasini bajarilgan deb o'chiring, qolganini chiqaring.
2. So'zlar ro'yxatini uzunligi bo'yicha saralang (key=len).
3. Ikki ro'yxatning umumiy elementlari (comprehension bilan).""",
            DOCS + "datastructures.html#more-on-lists",
        ),
        T(
            "PY11",
            "Tuple va Set: o'zgarmas ro'yxat va to'plamlar",
            """Maqsad: tuple va set farqi, qachon qaysi birini ishlatish.

Dars rejasi:
1. tuple: o'zgarmas, unpacking (x, y = point), funksiyadan bir nechta qiymat.
2. set: takrorlanmas elementlar, add/remove/discard.
3. To'plam amallari: | (birlashma), & (kesishma), - (ayirma), ^ (simmetrik ayirma).
4. list vs tuple vs set — tezlik va xususiyatlar jadvali.

Darsdagi masalalar:
1. Ikki guruhda ham o'qiydigan o'quvchilar (set kesishmasi).
2. Matndagi noyob so'zlar soni.
3. Koordinatalar tuple'lari ro'yxati: boshlang'ich nuqtaga eng yaqini.""",
            """1. Ikki sinf sevimli fanlari: umumiy, faqat 1-sinfda, hammasi (set amallari).
2. Ro'yxatda takrorlangan elementlar bormi (set yordamida bir qatorda)?
3. Hafta kunlari tuple'i — nima uchun bu yerda list emas, tuple to'g'riroq?""",
            DOCS + "datastructures.html#tuples-and-sequences",
        ),
        T(
            "PY12",
            "Dictionary (lug'at): kalit-qiymat va metodlar",
            """Maqsad: lug'at bilan ma'lumotni nom bo'yicha saqlash va qidirish.

Dars rejasi:
1. {} va dict(); kalit orqali o'qish/yozish; get() bilan xavfsiz o'qish.
2. keys, values, items, update, pop, setdefault.
3. Lug'at bo'ylab for bilan yurish; dict comprehension.

Darsdagi masalalar:
1. Inglizcha–o'zbekcha lug'at: so'z kiritilsa tarjimasi yoki "topilmadi".
2. Matndagi har bir so'z necha marta uchragani.
3. Mahsulot narxlari lug'ati: eng qimmat mahsulot.""",
            """1. Telefon kitobchasi: qo'shish, qidirish, o'chirish (konsol menyu).
2. O'quvchi → baholar ro'yxati lug'ati: har birining o'rtachasi.
3. Ikki lug'atni birlashtiring (bir xil kalitlarda qiymatlarni qo'shib).""",
            DOCS + "datastructures.html#dictionaries",
        ),
        T(
            "PY13",
            "Murakkab ma'lumotlar: ichma-ich list va dict",
            """Maqsad: real hayotiy ma'lumotlarni (JSON'ga o'xshash) tuzilma bilan ifodalash.

Dars rejasi:
1. Lug'atlar ro'yxati: [{"ism": ..., "ball": ...}, ...].
2. Lug'at ichida ro'yxat va lug'at; chuqur murojaat data["guruh"]["oquvchilar"][0].
3. sorted(..., key=lambda x: x["ball"]) bilan saralash (lambda — oldindan tanishuv).

Darsdagi masalalar:
1. O'quvchilar ro'yxati: ball bo'yicha reyting va eng yaxshi 3 talik.
2. Do'kon ombori: mahsulot → {narx, soni}; umumiy qiymat.
3. Guruhlar lug'ati: har bir guruhdagi o'quvchilar soni.""",
            """1. Kutubxona: kitoblar ro'yxati (nomi, muallif, yili) — muallif bo'yicha guruhlang.
2. Haftalik dars jadvali: kun → [darslar] lug'ati; eng ko'p darsli kun.
3. Ichma-ich ma'lumotdan barcha telefon raqamlarini bitta ro'yxatga yig'ing.""",
            DOCS + "datastructures.html#looping-techniques",
        ),
    ],
)

LOOPS_FUNCS = M(
    "Python 3 · Sikllar va funksiyalar",
    "for/while, boshqaruv operatorlari, funksiyalar, *args/**kwargs, lambda va standart funksiyalar.",
    [
        T(
            "PY14",
            "for sikli va range()",
            """Maqsad: takrorlanuvchi amallarni for bilan yozish.

Dars rejasi:
1. for x in ketma-ketlik; range(start, stop, step).
2. enumerate() va zip().
3. Hisoblagich va yig'uvchi andozalari (counter / accumulator).

Darsdagi masalalar:
1. 1 dan N gacha yig'indi va faktorial.
2. Ko'paytirish jadvali (ichma-ich for).
3. Ro'yxatdagi juft sonlar yig'indisi va soni.""",
            """1. Yulduzchalardan uchburchak va archa chizing (N kiritiladi).
2. Sonning barcha bo'luvchilari; tub sonmi?
3. 1–100 FizzBuzz.""",
            DOCS + "controlflow.html#for-statements",
        ),
        T(
            "PY15",
            "while sikli va break, continue, pass",
            """Maqsad: shartga bog'liq sikllar va sikl oqimini boshqarish.

Dars rejasi:
1. while shart; cheksiz sikldan qochish.
2. break, continue, pass; for/while ... else.
3. Foydalanuvchi kiritishini tekshirish sikli (to'g'ri kiritguncha so'rash).

Darsdagi masalalar:
1. "Sonni top" o'yini: kompyuter 1–100 son o'ylaydi, "katta/kichik" maslahat.
2. Raqamlar yig'indisi (while bilan, 1234 → 10).
3. Musbat son kiritilguncha qayta so'rash.""",
            """1. Bankomat menyusi: "chiqish" tanlanmaguncha ishlaydi.
2. Kollats ketma-ketligi: n → 1 gacha qadamlar soni.
3. Parolni 3 marta noto'g'ri kiritsa bloklansin.""",
            DOCS + "controlflow.html#break-and-continue-statements",
        ),
        T(
            "PY16",
            "Sikllar bilan list va dict ustida ishlash",
            """Maqsad: to'plamlarni qayta ishlashning amaliy andozalari.

Dars rejasi:
1. Filtrlash, o'zgartirish, guruhlash, qidirish andozalari.
2. dict.items() bo'ylab sikl; ichma-ich tuzilmalar bo'ylab sikl.
3. Sikl ichida ro'yxatni o'zgartirish xavfi.

Darsdagi masalalar:
1. Baholar lug'atidan "a'lochilar" ro'yxati.
2. So'zlarni birinchi harfi bo'yicha guruhlash.
3. Matritsa (ro'yxatlar ro'yxati) qatorlari va ustunlari yig'indisi.""",
            """1. Do'kon cheki: savatdagi mahsulotlar (nomi, narxi, soni) — chiroyli chek chiqaring.
2. Eng ko'p takrorlangan 3 ta so'z.
3. Ikki o'lchamli ro'yxatdan eng katta element va uning o'rni.""",
            DOCS + "datastructures.html#looping-techniques",
        ),
        T(
            "PY17",
            "Funksiyalar: def, parametrlar, return",
            """Maqsad: kodni qayta ishlatiladigan bo'laklarga ajratish.

Dars rejasi:
1. def, chaqirish, parametr va argument.
2. return va print farqi; bir nechta qiymat qaytarish (tuple).
3. Docstring; funksiya nomlash qoidalari; bitta funksiya — bitta vazifa.

Darsdagi masalalar:
1. is_even(n), is_prime(n) funksiyalari.
2. area(shakl, ...) — kvadrat, doira, uchburchak.
3. min_max(nums) → (eng kichik, eng katta).""",
            """1. Kalkulyatorni funksiyalarga ajrating: add, sub, mul, div va menyu.
2. grade(score) → baho matni (PY07 masalasi funksiya ko'rinishida).
3. count_vowels(text) va reverse_words(text).""",
            DOCS + "controlflow.html#defining-functions",
        ),
        T(
            "PY18",
            "Funksiyalar: default qiymatlar, *args, **kwargs va scope",
            """Maqsad: moslashuvchan funksiyalar yozish.

Dars rejasi:
1. Default qiymatlar va nomli argumentlar; o'zgaruvchan default xavfi (def f(x=[])).
2. *args va **kwargs; argumentlarni ochish (*list, **dict).
3. Ko'rinish sohasi (local/global), global'dan qochish.

Darsdagi masalalar:
1. total(*nums) — istalgan miqdordagi sonlar yig'indisi.
2. make_profile(name, **info) — profil matni.
3. greet(name, lang="uz") — 3 tilda salomlashish.""",
            """1. order(*items, discount=0) — buyurtma summasi chegirma bilan.
2. build_url(base, **params) → "https://site.uz/?q=python&page=2".
3. Nima uchun def add(item, box=[]) xavfli? Misol bilan ko'rsating va tuzating.""",
            DOCS + "controlflow.html#more-on-defining-functions",
        ),
        T(
            "PY19",
            "Lambda va standart funksiyalar: map, filter, sorted, sum, min, max",
            """Maqsad: qisqa funksiyalar va tayyor funksiyalardan samarali foydalanish.

Dars rejasi:
1. lambda sintaksisi va qachon kerak (key= uchun).
2. map, filter, sorted(key=), min/max(key=), sum, any, all.
3. Comprehension vs map/filter — qaysi biri o'qishga osonroq.

Darsdagi masalalar:
1. O'quvchilarni ball bo'yicha kamayish tartibida saralang.
2. Narxlar ro'yxatiga 12% QQS qo'shing (map).
3. Ro'yxatda manfiy son bormi (any)? Hammasi musbatmi (all)?""",
            """1. Mahsulotlar lug'atlari ro'yxati: eng arzon va eng qimmat (min/max key=).
2. So'zlarni oxirgi harfi bo'yicha saralang.
3. Faqat "a" bilan boshlanadigan ismlar (filter va comprehension — ikki usulda).""",
            "https://docs.python.org/3/library/functions.html",
        ),
    ],
)

MODULES_FILES = M(
    "Python 4 · Modullar, fayllar va xatoliklar",
    "Standart kutubxona (random, math, datetime, re, os), try/except, txt va JSON fayllar.",
    [
        T(
            "PY20",
            "Modullar va import; random kutubxonasi",
            """Maqsad: tayyor kutubxonalardan foydalanish.

Dars rejasi:
1. import, from ... import, as; modul qidirish yo'li.
2. random: randint, choice, shuffle, sample, random.
3. Standart kutubxona hujjatlarini o'qishni o'rganish.

Darsdagi masalalar:
1. Zar tashlash simulyatori (1000 marta) — har bir son chastotasi.
2. Tasodifiy parol generatori (uzunlik kiritiladi).
3. Guruhni tasodifiy 2 jamoaga bo'lish.""",
            """1. "Tosh-qog'oz-qaychi" (kompyuterga qarshi, 3 raund).
2. Lotereya: 1–49 dan 6 ta takrorlanmas son (sample).
3. Viktorina: 5 ta savoldan tasodifiy 3 tasi.""",
            "https://docs.python.org/3/library/random.html",
        ),
        T(
            "PY21",
            "math va datetime kutubxonalari",
            """Maqsad: matematik funksiyalar va sana/vaqt bilan ishlash.

Dars rejasi:
1. math: sqrt, pow, ceil, floor, pi, gcd, factorial.
2. datetime: date.today(), datetime.now(), timedelta, strftime/strptime.
3. Sanalar orasidagi farq va formatlash ("%d.%m.%Y").

Darsdagi masalalar:
1. Tug'ilgan kungacha necha kun qoldi?
2. Kvadrat tenglama ildizlari (math.sqrt, diskriminant).
3. Bugundan 100 kun keyin qaysi sana va hafta kuni?""",
            """1. Yoshni yil, oy, kunda hisoblang.
2. Dars jadvali: boshlanish vaqti + 90 daqiqa → tugash vaqti.
3. EKUB va EKUK kalkulyatori (math.gcd).""",
            "https://docs.python.org/3/library/math.html\nhttps://docs.python.org/3/library/datetime.html",
        ),
        T(
            "PY22",
            "re (RegEx): matndan andoza bo'yicha qidirish",
            """Maqsad: muntazam ifodalar bilan matnni tekshirish va ajratib olish.

Dars rejasi:
1. re.search, re.match, re.fullmatch, re.findall, re.sub.
2. Belgilar: \\d \\w \\s . ^ $ [] + * ? {n,m} va guruhlar ().
3. Raw string r"..." va regex101.com bilan sinash.

Darsdagi masalalar:
1. Matndagi barcha telefon raqamlarini toping.
2. Matndagi barcha email manzillarni ajrating.
3. Sanani "2026-10-06" → "06.10.2026" ga o'zgartiring (re.sub va guruhlar).""",
            """1. Matndan barcha #hashtag'larni toping.
2. Parol validatori (PY08) ni bitta murakkab regex bilan qayta yozing.
3. Avtomobil raqami "01 A 123 BC" formatini tekshiring.""",
            "https://docs.python.org/3/library/re.html\nhttps://regex101.com",
        ),
        T(
            "PY23",
            "os moduli va o'z modulingizni yaratish",
            """Maqsad: fayl tizimi bilan ishlash va kodni bir nechta faylga ajratish.

Dars rejasi:
1. os: getcwd, listdir, mkdir, path.join, path.exists; pathlib.Path — zamonaviy usul.
2. O'z modulingiz: utils.py va undan import; if __name__ == "__main__".
3. pip va virtual muhit (venv) bilan tanishuv.

Darsdagi masalalar:
1. Papkadagi fayllarni kengaytmasi bo'yicha sanash.
2. utils.py'ga PY17 funksiyalarini ko'chirib, main.py'dan foydalaning.
3. "Hisobotlar/2026-10" papkasini mavjud bo'lmasa yaratish.""",
            """1. "Yuklamalar tozalovchisi": fayllarni turiga qarab (rasm, hujjat, boshqa) papkalarga ajratish
   (avval nusxa papkada sinang!).
2. Kalkulyator loyihangizni 2 modulga ajrating.""",
            "https://docs.python.org/3/library/os.html\nhttps://docs.python.org/3/library/pathlib.html",
        ),
        T(
            "PY24",
            "Xatoliklar bilan ishlash: try, except, else, finally",
            """Maqsad: dastur xatoda "qulamasligi" va foydalanuvchiga tushunarli xabar berish.

Dars rejasi:
1. Traceback'ni o'qish; ValueError, ZeroDivisionError, KeyError, IndexError, FileNotFoundError.
2. try / except (aniq xato turi!) / else / finally.
3. raise va o'z xato xabaringiz; "barcha xatoni yutib yuborish" nega yomon.

Darsdagi masalalar:
1. Xavfsiz son kiritish funksiyasi: to'g'ri kiritilguncha so'raydi.
2. Kalkulyatorga xatolarni ushlash qo'shing.
3. Lug'atdan kalitni o'qish: KeyError'ni ushlash va get() bilan solishtirish.""",
            """1. ask_int(prompt, min_value, max_value) — chegaradan tashqarida bo'lsa qayta so'raydi.
2. Bankomat: yetarli mablag' bo'lmasa raise ValueError va uni menyuda ushlash.
3. 5 ta xato turi uchun bittadan misol va ularni ushlash.""",
            DOCS + "errors.html",
        ),
        T(
            "PY25",
            "Fayllar bilan ishlash: txt o'qish va yozish",
            """Maqsad: ma'lumotni faylda saqlash va qayta o'qish.

Dars rejasi:
1. open() rejimlari: r, w, a; encoding="utf-8".
2. with ... as f — fayl avtomatik yopiladi.
3. read, readline, readlines, qatorma-qator for bilan o'qish; write.

Darsdagi masalalar:
1. Kundalik: kiritilgan matnni sana bilan faylga qo'shish (a rejimi).
2. Fayldagi qatorlar, so'zlar va belgilar soni.
3. ismlar.txt'dan ismlarni o'qib, alifbo tartibida yangi faylga yozish.""",
            """1. To-do ro'yxat: vazifalar todo.txt'da saqlanadi (qo'shish/ko'rish/o'chirish).
2. Baholar fayli (ism;ball) → o'rtacha ball va eng yuqori natija.
3. Fayl topilmasa dastur qulamasin (try/except).""",
            DOCS + "inputoutput.html#reading-and-writing-files",
        ),
        T(
            "PY26",
            "JSON bilan ishlash: ma'lumotni saqlash va yuklash",
            """Maqsad: murakkab tuzilmalarni (list/dict) JSON faylda saqlash.

Dars rejasi:
1. JSON formati va Python turlari mosligi.
2. json.dump/json.load (fayl), json.dumps/json.loads (matn); ensure_ascii=False, indent=2.
3. "Ma'lumotlar ombori" andozasi: yuklash → o'zgartirish → saqlash.

Darsdagi masalalar:
1. Telefon kitobchasini (PY12) contacts.json'da saqlang.
2. O'quvchilar ro'yxatini JSON'dan o'qib, reyting tuzing.
3. Sozlamalar fayli (settings.json) bo'lmasa — standart qiymatlar bilan yaratish.""",
            """1. To-do ilovangizni JSON'ga o'tkazing (vazifa: matn, bajarildi, sana).
2. Kichik "kutubxona" dasturi: kitob qo'shish, qidirish, ro'yxat — books.json.
3. Noto'g'ri JSON faylda json.JSONDecodeError'ni ushlang.""",
            "https://docs.python.org/3/library/json.html",
        ),
    ],
)

OOP = M(
    "Python 5 · OOP asoslari",
    "Class, obyekt, vorislik, inkapsulyatsiya va maxsus metodlar.",
    [
        T(
            "PY27",
            "OOP: class va obyekt, __init__, metodlar",
            """Maqsad: real dunyo narsalarini class sifatida modellashtirish.

Dars rejasi:
1. Class — chizma, obyekt — nusxa; self nima.
2. __init__, atributlar, metodlar; class atributi va obyekt atributi.
3. __str__ bilan chiroyli chiqarish.

Darsdagi masalalar:
1. Student class: ism, baholar; add_grade(), average().
2. BankAccount: deposit(), withdraw() (yetarli mablag' tekshiruvi), balance.
3. Rectangle: area(), perimeter(), is_square().""",
            """1. Book class va Library class (kitoblar ro'yxati, qo'shish, qidirish).
2. Timer class: start(), stop(), elapsed() (datetime bilan).
3. Student obyektlari ro'yxatidan eng yaxshi o'quvchini toping.""",
            DOCS + "classes.html",
        ),
        T(
            "PY28",
            "OOP: vorislik (inheritance) va polimorfizm",
            """Maqsad: umumiy xususiyatlarni ota class'ga chiqarish.

Dars rejasi:
1. class Child(Parent); super().__init__().
2. Metodni qayta aniqlash (override) va polimorfizm.
3. isinstance, issubclass; "is-a" va "has-a" (kompozitsiya) farqi.

Darsdagi masalalar:
1. Animal → Dog, Cat: speak() har biri o'zicha.
2. Employee → Teacher, Driver: salary() har xil hisoblanadi.
3. Shape → Circle, Square: area(); shakllar ro'yxati umumiy yuzasi.""",
            """1. Vehicle → Car, Bike, Bus: tavsif va yo'l narxi hisoblash.
2. Account → SavingsAccount (foiz qo'shadi), CreditAccount (minusga kirish mumkin).""",
            DOCS + "classes.html#inheritance",
        ),
        T(
            "PY29",
            "OOP: inkapsulyatsiya, property va maxsus metodlar",
            """Maqsad: obyekt holatini himoya qilish va Python'ga xos qulayliklar.

Dars rejasi:
1. _protected va __private nomlash qoidalari.
2. @property va setter — qiymatni tekshirib o'rnatish.
3. Maxsus metodlar: __str__, __repr__, __len__, __eq__, __lt__ (saralash uchun).

Darsdagi masalalar:
1. Product: narx manfiy bo'lishi mumkin emas (property setter).
2. Cart: __len__ (mahsulotlar soni), total property.
3. Student'larni __lt__ orqali o'rtacha ball bo'yicha saralash.""",
            """1. BankAccount'da balance'ni faqat o'qiladigan (read-only) property qiling.
2. Temperature class: celsius va fahrenheit property'lari (biri o'zgarsa, ikkinchisi ham).""",
            "https://docs.python.org/3/library/functions.html#property",
        ),
    ],
)

PROJECTS = M(
    "Python 6 · Yakuniy loyihalar",
    "Konsol o'yinlari, ma'lumotlar bilan ishlaydigan konsol tizimi va Telegram bot.",
    [
        T(
            "PY30",
            "Loyiha: konsol o'yinlari (Tosh-qog'oz-qaychi, Sonni top)",
            """Maqsad: o'rganilganlarni (shart, sikl, funksiya, random) bitta o'yinda birlashtirish.

Talablar:
- Menyu: 1 — Tosh-qog'oz-qaychi, 2 — Sonni top, 3 — Natijalar, 0 — Chiqish.
- Har bir o'yin alohida funksiya; noto'g'ri kiritish ushlanadi.
- Natijalar (g'alaba/mag'lubiyat, eng kam urinish) scores.json'da saqlanadi.

Dars rejasi:
1. Loyiha tuzilmasini rejalashtirish (funksiyalar ro'yxati) — 15 daq.
2. Kod yozish (juftlikda) — 55 daq.
3. Bir-birining o'yinini sinash va fikr — 20 daq.

Baholash (100 ball): ishlashi — 50, kod tuzilmasi (funksiyalar) — 30, xatolarni ushlash — 20.""",
            """1. O'yinga qiyinlik darajasi qo'shing (Sonni top: 1–50 / 1–100 / 1–1000).
2. README.txt: o'yin qoidalari va qanday ishga tushirish.""",
            "https://docs.python.org/3/library/random.html",
        ),
        T(
            "PY31",
            "Loyiha: konsol boshqaruv tizimi (JSON ma'lumotlar ombori, CRUD)",
            """Maqsad: real tizim — qo'shish, ko'rish, tahrirlash, o'chirish (CRUD) va qidirish.

Mavzulardan birini tanlang: "O'quv markazi o'quvchilari", "Do'kon ombori", "Kutubxona".
Talablar:
- Ma'lumot JSON faylda; dastur qayta ochilganda saqlanib qoladi.
- Qidiruv va saralash; noto'g'ri kiritishga chidamli (try/except).
- Kod modullarga ajratilgan (storage.py, models.py, main.py); OOP o'tilgan bo'lsa — class'lar bilan.

Dars rejasi:
1. Ma'lumot tuzilmasi va menyuni loyihalash — 20 daq.
2. Kod yozish — 55 daq.
3. Ko'rgazma — 15 daq.

Baholash (100 ball): CRUD to'liq — 40, saqlash/yuklash — 20, tuzilma va modullar — 25, xatolar — 15.""",
            """1. Statistikani qo'shing (masalan, ombordagi umumiy qiymat, o'rtacha ball).
2. Ma'lumotni CSV'ga eksport qiling (csv moduli).""",
            "https://docs.python.org/3/library/json.html\nhttps://docs.python.org/3/library/csv.html",
        ),
        T(
            "PY32",
            "Telegram bot (1): BotFather, token va birinchi bot",
            """Maqsad: Telegram bot yaratish va oddiy buyruqlarga javob berish.

Dars rejasi:
1. BotFather'da bot yaratish; token — maxfiy (kodga emas, muhit o'zgaruvchisiga!).
2. pip install pyTelegramBotAPI; birinchi /start va /help.
3. Matnli xabarlarga javob (echo), tugmalar (ReplyKeyboardMarkup).
4. Bot qanday ishlaydi: polling, handler'lar.

Darsdagi masalalar:
1. /start — salomlashish va menyu tugmalari.
2. "Sana" tugmasi — bugungi sana (datetime).
3. "Tasodifiy fakt" tugmasi — ro'yxatdan random.choice.""",
            """1. Botga /about buyrug'ini qo'shing (o'zingiz haqingizda).
2. Kalkulyator: foydalanuvchi "12 * 7" yozsa, natija qaytadi (eval ishlatmang!).
3. Token'ni .env yoki muhit o'zgaruvchisida saqlang.""",
            "https://core.telegram.org/bots/tutorial\nhttps://pytba.readthedocs.io/en/latest/",
        ),
        T(
            "PY33",
            "Telegram bot (2): holat, ma'lumot saqlash va yakuniy bot",
            """Maqsad: foydalanuvchi ma'lumotini saqlaydigan foydali bot yaratish.

Mavzulardan birini tanlang: "Lug'at boti", "Vazifalar (to-do) boti", "Viktorina boti",
"O'quv markaziga ro'yxatdan o'tish boti".
Talablar:
- Inline tugmalar (InlineKeyboardMarkup) va callback'lar.
- Foydalanuvchi ma'lumotlari JSON faylda (user_id bo'yicha).
- Xatolar ushlanadi, token kodda emas.

Dars rejasi:
1. Bot g'oyasi va buyruqlar ro'yxati — 15 daq.
2. Kod yozish — 60 daq.
3. Sinov: guruhdoshlar botdan foydalanib ko'radi — 15 daq.

Baholash (100 ball): ishlashi — 40, saqlash — 20, foydalanish qulayligi — 20, kod sifati — 20.""",
            """Yakuniy loyiha himoyasiga tayyorlaning: botingiz (yoki konsol tizimingiz) haqida
3–5 slaydli taqdimot va kodni GitHub'ga joylang.""",
            "https://pytba.readthedocs.io/en/latest/",
        ),
        T(
            "PY34",
            "Yakuniy loyiha himoyasi va sertifikat",
            """Maqsad: loyihani taqdim etish, kod haqida savollarga javob berish.

Talablar:
- Loyiha: Telegram bot yoki konsol boshqaruv tizimi (PY31/PY33 asosida yoki yangi g'oya).
- Kod GitHub'da, README bilan (nima qiladi, qanday ishga tushadi).
- Taqdimot: 5 daqiqa demo + 3 daqiqa savol-javob.

Baholash (100 ball):
- Loyiha ishlaydi va foydali — 40
- Kod sifati (funksiya/class, nomlash, xatolar) — 30
- Taqdimot va savollarga javob — 20
- GitHub va README — 10""",
            """Keyingi qadam: loyihangizga 1 ta yangi imkoniyat qo'shing va 2 haftadan keyin
ustozga ko'rsating.""",
            "https://docs.github.com/en/get-started/start-your-journey/hello-world",
        ),
    ],
)

MODULES = [BASICS, STRUCTURES, LOOPS_FUNCS, MODULES_FILES, OOP, PROJECTS]
