"""Dasturchi 4-oy · Python: tuzilmalar va funksiyalar — 12 dars "Dars kodi" (kalit — ``dev.py``)."""

from .lesson_kit import lesson, step

M = "4-oy · Tuzilmalar va funksiyalar"

CLASS_LIST = r'''
sinf = ["Ali", "Laylo", "Vali", "Sardor", "Madina"]

print("Birinchi:", sinf[0])
print("Oxirgi:", sinf[-1])
print("Dastlabki uchtasi:", sinf[:3])
print("Har ikkinchisi:", sinf[::2])

sinf[2] = "Valijon"
print("O'zgartirildi:", sinf)
print("O'quvchilar soni:", len(sinf))
print("Laylo bormi?", "Laylo" in sinf)
'''

TODO1 = r'''
vazifalar = []

while True:
    buyruq = input("+ qo'shish, - o'chirish, ? ro'yxat, q chiqish: ")
    if buyruq == "+":
        vazifa = input("Vazifa: ")
        vazifalar.append(vazifa)
        print("✅ Qo'shildi")
    elif buyruq == "-":
        vazifa = input("Qaysi vazifa? ")
        if vazifa in vazifalar:
            vazifalar.remove(vazifa)
            print("🗑 O'chirildi")
        else:
            print("Bunday vazifa yo'q")
    elif buyruq == "?":
        if not vazifalar:
            print("Ro'yxat bo'sh")
        n = 1
        for v in vazifalar:
            print(f"{n}. {v}")
            n += 1
    elif buyruq == "q":
        break
'''

STATS = r'''
baholar = [5, 4, 3, 5, 2, 4, 5]

jami = 0
eng_katta = baholar[0]
for b in baholar:
    jami += b
    if b > eng_katta:
        eng_katta = b

orta = jami / len(baholar)
print("Yig'indi:", jami)
print("Eng katta:", eng_katta)
print("O'rtacha:", round(orta, 2))
print("Tayyor funksiyalar:", sum(baholar), max(baholar), min(baholar))

past = 0
for b in baholar:
    if b < 4:
        past += 1
print("4 dan past baholar:", past)
'''

SUBJECTS = r'''
nuqta = (41.3, 69.2)
x, y = nuqta
print("Toshkent:", x, y)

fanlar = ["matematika", "fizika", "matematika", "ingliz", "fizika"]
noyob = set(fanlar)
print("Noyob fanlar:", sorted(noyob))
print("Nechta fan:", len(noyob))

ali = {"matematika", "fizika", "ingliz"}
vali = {"fizika", "tarix", "ingliz"}
print("Umumiy:", sorted(ali & vali))
print("Hammasi:", sorted(ali | vali))
print("Faqat Alida:", sorted(ali - vali))
'''

PHONE1 = r'''
kitob = {"Ali": "+998901112233", "Laylo": "+998935556677"}

print("Ali:", kitob["Ali"])
kitob["Vali"] = "+998977778899"
print("Kontaktlar soni:", len(kitob))

ism = input("Kimni qidiramiz? ")
print(kitob.get(ism, "Topilmadi"))

for ism, tel in kitob.items():
    print(f"{ism}: {tel}")
'''

PHONE2 = r'''
kitob = {"Ali": "+998901112233", "Laylo": "+998935556677"}

while True:
    tanlov = input("1-qidir 2-saqla 3-o'chir 4-hammasi 0-chiqish: ")
    if tanlov == "1":
        qism = input("Ism (qismi): ").lower()
        topildi = False
        for ism, tel in kitob.items():
            if qism in ism.lower():
                print(f"{ism}: {tel}")
                topildi = True
        if not topildi:
            print("Topilmadi")
    elif tanlov == "2":
        ism = input("Ism: ").title()
        kitob[ism] = input("Telefon: ")
        print("✅ Saqlandi")
    elif tanlov == "3":
        ism = input("Ism: ").title()
        print("🗑 O'chirildi" if kitob.pop(ism, None) else "Bunday kontakt yo'q")
    elif tanlov == "4":
        for ism in sorted(kitob):
            print(f"{ism}: {kitob[ism]}")
    elif tanlov == "0":
        break
'''

RATING1 = r'''
oquvchilar = [
    {"ism": "Ali", "baholar": [5, 4, 5]},
    {"ism": "Laylo", "baholar": [5, 5, 5]},
    {"ism": "Vali", "baholar": [3, 4, 4]},
]

for o in oquvchilar:
    o["orta"] = round(sum(o["baholar"]) / len(o["baholar"]), 2)

eng_yaxshi = oquvchilar[0]
for o in oquvchilar:
    if o["orta"] > eng_yaxshi["orta"]:
        eng_yaxshi = o

for o in oquvchilar:
    print(f"{o['ism']}: {o['orta']}")
print("🏆 Eng yaxshi:", eng_yaxshi["ism"])
print("Layloning 2-bahosi:", oquvchilar[1]["baholar"][1])
'''

CALC3 = r'''
def qosh(a, b):
    return a + b


def bol(a, b):
    if b == 0:
        return None
    return a / b


def hisobla(a, amal, b):
    if amal == "+":
        return qosh(a, b)
    if amal == "-":
        return a - b
    if amal == "*":
        return a * b
    if amal == "/":
        return bol(a, b)
    return None


ifoda = input("Ifoda (masalan 12 * 3): ").split()
a, amal, b = float(ifoda[0]), ifoda[1], float(ifoda[2])
natija = hisobla(a, amal, b)
print("Natija:", natija if natija is not None else "xato")
'''

TODO2 = r'''
vazifalar = []


def qosh(*yangilar):
    for v in yangilar:
        vazifalar.append(v)
    return len(yangilar)


def korsat(sarlavha="Vazifalar"):
    print(f"--- {sarlavha} ({len(vazifalar)}) ---")
    for n, v in enumerate(vazifalar, start=1):
        print(f"{n}. {v}")


def ochir(raqam):
    if 1 <= raqam <= len(vazifalar):
        return vazifalar.pop(raqam - 1)
    return None


soni = qosh("Kitob o'qish", "Sport", "Ingliz tili")
print("Qo'shildi:", soni)
korsat()
print("O'chirildi:", ochir(2))
korsat("Bugun")
'''

RATING2 = r'''
oquvchilar = [("Ali", 87), ("Laylo", 95), ("Vali", 72), ("Sardor", 64)]

by_ball = sorted(oquvchilar, key=lambda o: o[1], reverse=True)
print("Reyting:", by_ball)

by_name = sorted(oquvchilar, key=lambda o: o[0])
print("Alifbo:", list(map(lambda o: o[0], by_name)))

otganlar = list(filter(lambda o: o[1] >= 70, oquvchilar))
print("O'tganlar:", len(otganlar))

print("Eng yuqori:", max(oquvchilar, key=lambda o: o[1])[0])
'''

TEXT = r'''
matn = input("Matn: ")

sozlar = [s.strip(".,!?").lower() for s in matn.split()]
print("So'zlar soni:", len(sozlar))

uzunlar = [s for s in sozlar if len(s) > 4]
print("Uzun so'zlar:", uzunlar)

sanoq = {}
for s in sozlar:
    sanoq[s] = sanoq.get(s, 0) + 1
eng_kop = max(sanoq, key=sanoq.get)
print(f"Eng ko'p: {eng_kop} ({sanoq[eng_kop]} marta)")

unlilar = [h for h in matn.lower() if h in "aeiou"]
print("Unli harflar:", len(unlilar))
'''

DIARY = r'''
vazifalar = []


def menyu():
    print("\n1) Qo'shish  2) Ro'yxat  3) Bajarildi  4) O'chirish  0) Chiqish")
    return input("Tanlang: ")


def qosh():
    matn = input("Vazifa: ").strip()
    if matn:
        vazifalar.append({"matn": matn, "bajarildi": False})
        print("✅ Qo'shildi")


def royxat():
    if not vazifalar:
        print("Ro'yxat bo'sh")
    for n, v in enumerate(vazifalar, start=1):
        belgi = "✔" if v["bajarildi"] else "☐"
        print(f"{n}. {belgi} {v['matn']}")


def raqam_sora():
    javob = input("Raqam: ")
    if javob.isdigit() and 1 <= int(javob) <= len(vazifalar):
        return int(javob) - 1
    print("Noto'g'ri raqam")
    return None


while True:
    tanlov = menyu()
    if tanlov == "1":
        qosh()
    elif tanlov == "2":
        royxat()
    elif tanlov == "3":
        i = raqam_sora()
        if i is not None:
            vazifalar[i]["bajarildi"] = True
    elif tanlov == "4":
        i = raqam_sora()
        if i is not None:
            print("🗑", vazifalar.pop(i)["matn"])
    elif tanlov == "0":
        bajarilgan = len([v for v in vazifalar if v["bajarildi"]])
        print(f"Xayr! Bajarildi: {bajarilgan}/{len(vazifalar)}")
        break
'''

LESSONS = {
    "DP13": lesson(
        M, 1, "List: yaratish, indeks va kesish",
        "Ko'p qiymatni bitta ro'yxatda saqlaymiz va indeks bilan ishlaymiz.",
        "3-oyda: o'zgaruvchilar, satr indekslari va kesish, sikllar.",
        "\"Python\"[0] va \"Python\"[::-1] — satr indeksini eslaymiz.",
        "List — tartiblangan ro'yxat: [...], indeks 0 dan, manfiy indeks, kesish, len, in, o'zgartirish.",
        "Ro'yxatdan oxirgi 3 ta o'quvchini va teskari tartibni chiqaring.",
        [("📋", "Ro'yxat", "[\"Ali\", ...]", "mem"),
         ("🔢", "Indeks", "[0] · [-1]", ""),
         ("✂", "Kesish", "[:3] · [::2]", ""),
         ("✏", "O'zgartirish", "sinf[2] = ...", ""),
         ("🔍", "in · len", "bormi? nechta?", "")],
        [
            step("class_list.py", "Ro'yxat va indekslar", r'''
sinf = ["Ali", "Laylo", "Vali", "Sardor", "Madina"]

print("Birinchi:", sinf[0])
print("Oxirgi:", sinf[-1])''',
                 [("[ ... ]", "kvadrat qavs ichida, vergul bilan."),
                  ("sinf[0]", "indeks 0 dan — birinchi element."),
                  ("sinf[-1]", "manfiy indeks oxiridan sanaydi.")],
                 "Birinchi: Ali\nOxirgi: Madina"),
            step("class_list.py", "Kesish", r'''
print("Dastlabki uchtasi:", sinf[:3])
print("Har ikkinchisi:", sinf[::2])''',
                 [("[:3]", "0, 1, 2-indekslar — oxiri kirmaydi."),
                  ("[::2]", "qadam 2 — har ikkinchisi."),
                  ("yangi ro'yxat", "kesish asl ro'yxatni o'zgartirmaydi.")],
                 "Dastlabki uchtasi: ['Ali', 'Laylo', 'Vali']\nHar ikkinchisi: ['Ali', 'Vali', 'Madina']"),
            step("class_list.py", "O'zgartirish, len va in", r'''
sinf[2] = "Valijon"
print("O'zgartirildi:", sinf)
print("O'quvchilar soni:", len(sinf))
print("Laylo bormi?", "Laylo" in sinf)''',
                 [("sinf[2] = ...", "list o'zgaruvchan — satrdan farqli."),
                  ("len()", "elementlar soni."),
                  ("in", "ro'yxatda bormi — True/False.")],
                 "O'zgartirildi: ['Ali', 'Laylo', 'Valijon', 'Sardor', 'Madina']\nO'quvchilar soni: 5\nLaylo bormi? True"),
        ],
        {"class_list.py": CLASS_LIST},
        [("python/", ""), ("└── class_list.py", "yangi")],
        ["List yaratish", "Indeks va manfiy indeks", "Kesish (slicing)", "len() va in"],
        ["Majburiy: oxirgi 3 o'quvchi va teskari ro'yxatni chiqaring.",
         "Qo'shimcha: mavjud bo'lmagan indeks (sinf[10]) qanday xato berishini sinang."],
        "4.2 · List metodlari: vazifalar ro'yxati.",
        run={"file": "class_list.py", "input": "", "expect": ["Oxirgi: Madina", "Har ikkinchisi: ['Ali', 'Vali', 'Madina']", "Laylo bormi? True"]},
    ),
    "DP14": lesson(
        M, 2, "List metodlari: vazifalar ro'yxati",
        "Ro'yxatga element qo'shamiz, o'chiramiz va chiqaramiz — birinchi “To-do”.",
        "O'tgan darsda: list, indeks, kesish, in.",
        "sinf[-1] va sinf[:2] nima beradi?",
        "append, remove, pop, insert; bo'sh ro'yxat []; for bilan ro'yxatni aylanish.",
        "Vazifani raqami bo'yicha o'chirishni qo'shing (pop).",
        [("📋", "Bo'sh ro'yxat", "vazifalar = []", "mem"),
         ("➕", "append", "oxiriga qo'shish", ""),
         ("🗑", "remove", "qiymat bo'yicha", ""),
         ("🔁", "for", "raqamlab chiqarish", "")],
        [
            step("todo.py", "Bo'sh ro'yxat va append", r'''
vazifalar = []

while True:
    buyruq = input("+ qo'shish, - o'chirish, ? ro'yxat, q chiqish: ")
    if buyruq == "+":
        vazifa = input("Vazifa: ")
        vazifalar.append(vazifa)
        print("✅ Qo'shildi")''',
                 [("[]", "bo'sh ro'yxat — keyin to'ldiramiz."),
                  (".append(x)", "oxiriga bitta element qo'shadi."),
                  ("while True", "foydalanuvchi q bosmaguncha.")],
                 "+ qo'shish, ...: +\nVazifa: Kitob o'qish\n✅ Qo'shildi"),
            step("todo.py", "remove bilan o'chirish", r'''
    elif buyruq == "-":
        vazifa = input("Qaysi vazifa? ")
        if vazifa in vazifalar:
            vazifalar.remove(vazifa)
            print("🗑 O'chirildi")
        else:
            print("Bunday vazifa yo'q")''',
                 [(".remove(x)", "qiymat bo'yicha birinchisini o'chiradi."),
                  ("in bilan tekshirish", "yo'q qiymatni remove qilsak — ValueError."),
                  (".pop(i)", "indeks bo'yicha olib tashlaydi (uyga vazifa).")],
                 "Qaysi vazifa? Kitob o'qish\n🗑 O'chirildi"),
            step("todo.py", "Ro'yxatni raqamlab chiqarish", r'''
    elif buyruq == "?":
        if not vazifalar:
            print("Ro'yxat bo'sh")
        n = 1
        for v in vazifalar:
            print(f"{n}. {v}")
            n += 1
    elif buyruq == "q":
        break''',
                 [("not vazifalar", "bo'sh ro'yxat shartda False."),
                  ("for v in vazifalar", "har element navbat bilan v ga tushadi."),
                  ("n += 1", "o'zimiz raqamlaymiz (keyinroq enumerate).")],
                 "1. Uy vazifa\n2. Sport"),
        ],
        {"todo.py": TODO1},
        [("python/", ""), ("├── class_list.py", ""), ("└── todo.py", "yangi")],
        ["append, remove, pop", "Bo'sh ro'yxat va not", "for bilan aylanish", "Menyu sikli + list"],
        ["Majburiy: vazifani raqami bo'yicha o'chiring (pop).",
         "Qo'shimcha: “!” buyrug'i — vazifani ro'yxat boshiga qo'shish (insert(0, x))."],
        "4.3 · for bilan list: baholar statistikasi.",
        run={"file": "todo.py", "input": "+\nKitob o'qish\n+\nUy vazifa\n?\n-\nKitob o'qish\n?\nq\n", "expect": ["1. Kitob o'qish", "🗑 O'chirildi", "1. Uy vazifa"]},
    ),
    "DP15": lesson(
        M, 3, "for bilan list: baholar statistikasi",
        "Ro'yxatni aylanib yig'indi, eng katta va o'rtacha qiymatni topamiz.",
        "O'tgan darsda: append, remove, for bilan aylanish.",
        "Bo'sh ro'yxat shartda nima hisoblanadi?",
        "Yig'uvchi va eng kattasini qo'lda topish; tayyor sum, max, min, len; sanash.",
        "5 dan past baholar foizini chiqaring.",
        [("📋", "Baholar", "[5, 4, 3, ...]", ""),
         ("🔁", "for b", "har bir baho", "loop"),
         ("➕", "jami +=", "yig'indi", "mem"),
         ("🏔", "eng_katta", "solishtirish", ""),
         ("📊", "Natija", "o'rtacha 4.0", "")],
        [
            step("stats.py", "Yig'indi va eng kattasi", r'''
baholar = [5, 4, 3, 5, 2, 4, 5]

jami = 0
eng_katta = baholar[0]
for b in baholar:
    jami += b
    if b > eng_katta:
        eng_katta = b''',
                 [("jami = 0", "yig'uvchi — sikldan oldin."),
                  ("eng_katta = baholar[0]", "birinchi elementdan boshlaymiz."),
                  ("if b > eng_katta", "kattarog'i chiqsa — almashtiramiz.")],
                 "jami = 28, eng_katta = 5"),
            step("stats.py", "O'rtacha va tayyor funksiyalar", r'''
orta = jami / len(baholar)
print("Yig'indi:", jami)
print("Eng katta:", eng_katta)
print("O'rtacha:", round(orta, 2))
print("Tayyor funksiyalar:", sum(baholar), max(baholar), min(baholar))''',
                 [("jami / len", "o'rtacha = yig'indi ÷ soni."),
                  ("sum, max, min", "Python'da tayyor — lekin qanday ishlashini bilish muhim.")],
                 "Yig'indi: 28\nEng katta: 5\nO'rtacha: 4.0\nTayyor funksiyalar: 28 5 2"),
            step("stats.py", "Shart bo'yicha sanash", r'''
past = 0
for b in baholar:
    if b < 4:
        past += 1
print("4 dan past baholar:", past)''',
                 [("past += 1", "shart rost bo'lgandagina sanaymiz."),
                  ("ikkinchi sikl", "har savol uchun alohida sikl — tushunarli kod.")],
                 "4 dan past baholar: 2"),
        ],
        {"stats.py": STATS},
        [("python/", ""), ("├── todo.py", ""), ("└── stats.py", "yangi")],
        ["Yig'uvchi o'zgaruvchi", "Eng kattasini qo'lda topish", "sum, max, min, len", "Shart bo'yicha sanash"],
        ["Majburiy: 4 dan past baholar foizini chiqaring.",
         "Qo'shimcha: eng kichik bahoni qo'lda (min'siz) toping."],
        "4.4 · Tuple va set.",
        run={"file": "stats.py", "input": "", "expect": ["Yig'indi: 28", "O'rtacha: 4.0", "Tayyor funksiyalar: 28 5 2", "4 dan past baholar: 2"]},
    ),
    "DP16": lesson(
        M, 4, "Tuple va set",
        "O'zgarmas tuple va takrorlanmas set: takrorlarni olib tashlaymiz, umumiy fanlarni topamiz.",
        "O'tgan darsda: for bilan list, sum, max, min.",
        "sum([5, 4, 3]) va max([5, 4, 3]) nima beradi?",
        "Tuple (...) — o'zgarmas, ochish x, y = t; set {...} — takror yo'q, tartib yo'q; & | − amallari.",
        "Ikki do'stning faqat bittasida bor fanlarni toping (^).",
        [("📍", "Tuple", "(41.3, 69.2)", ""),
         ("📤", "Ochish", "x, y = nuqta", ""),
         ("🧺", "set()", "takrorsiz", "mem"),
         ("∩", "&  |  −", "umumiy, hammasi, farq", "")],
        [
            step("subjects.py", "Tuple va ochish", r'''
nuqta = (41.3, 69.2)
x, y = nuqta
print("Toshkent:", x, y)''',
                 [("( ... )", "tuple — o'zgartirib bo'lmaydi: nuqta[0] = 1 → TypeError."),
                  ("x, y = nuqta", "ochish: elementlar o'zgaruvchilarga taqsimlanadi.")],
                 "Toshkent: 41.3 69.2"),
            step("subjects.py", "set bilan takrorlarni olib tashlash", r'''
fanlar = ["matematika", "fizika", "matematika", "ingliz", "fizika"]
noyob = set(fanlar)
print("Noyob fanlar:", sorted(noyob))
print("Nechta fan:", len(noyob))''',
                 [("set(ro'yxat)", "takrorlar o'chadi."),
                  ("sorted()", "set'da tartib yo'q — chiqarishda saralaymiz."),
                  ("bo'sh set", "set() — {} esa bo'sh lug'at!")],
                 "Noyob fanlar: ['fizika', 'ingliz', 'matematika']\nNechta fan: 3"),
            step("subjects.py", "To'plam amallari", r'''
ali = {"matematika", "fizika", "ingliz"}
vali = {"fizika", "tarix", "ingliz"}
print("Umumiy:", sorted(ali & vali))
print("Hammasi:", sorted(ali | vali))
print("Faqat Alida:", sorted(ali - vali))''',
                 [("&", "kesishma — ikkalasida bor."),
                  ("|", "birlashma — hech bo'lmasa bittasida."),
                  ("−", "ayirma — birinchisida bor, ikkinchisida yo'q.")],
                 "Umumiy: ['fizika', 'ingliz']\nHammasi: ['fizika', 'ingliz', 'matematika', 'tarix']\nFaqat Alida: ['matematika']"),
        ],
        {"subjects.py": SUBJECTS},
        [("python/", ""), ("├── stats.py", ""), ("└── subjects.py", "yangi")],
        ["Tuple va ochish", "set va takrorlarni olib tashlash", "& | − amallari", "set() va {} farqi"],
        ["Majburiy: faqat bittasida bor fanlarni toping (ali ^ vali).",
         "Qo'shimcha: matndagi noyob harflar sonini set bilan toping."],
        "4.5 · Dictionary: telefon kitobchasi.",
        run={"file": "subjects.py", "input": "", "expect": ["Toshkent: 41.3 69.2", "Nechta fan: 3", "Umumiy: ['fizika', 'ingliz']", "Faqat Alida: ['matematika']"]},
    ),
    "DP17": lesson(
        M, 5, "Dictionary: telefon kitobchasi",
        "Ma'lumotni kalit bo'yicha saqlaymiz: ism → telefon.",
        "O'tgan darsda: tuple, set, to'plam amallari.",
        "set() va {} farqi nima?",
        "dict {kalit: qiymat}, d[kalit], qo'shish d[k] = v, get(k, standart), items().",
        "Har kontaktga email ham qo'shing.",
        [("📒", "Lug'at", "{\"Ali\": \"+998...\"}", "mem"),
         ("🔑", "d[\"Ali\"]", "kalit bo'yicha", ""),
         ("➕", "d[\"Vali\"] = ...", "qo'shish", ""),
         ("🛟", "get()", "xatosiz qidirish", ""),
         ("🔁", "items()", "hammasi", "")],
        [
            step("phonebook.py", "Lug'at yaratish va qo'shish", r'''
kitob = {"Ali": "+998901112233", "Laylo": "+998935556677"}

print("Ali:", kitob["Ali"])
kitob["Vali"] = "+998977778899"
print("Kontaktlar soni:", len(kitob))''',
                 [("{kalit: qiymat}", "jingalak qavs, juftliklar vergul bilan."),
                  ("kitob[\"Ali\"]", "kalit bo'yicha qiymat (indeks emas!)."),
                  ("kitob[\"Vali\"] = ...", "yangi kalit bo'lsa qo'shiladi, bor bo'lsa almashtiriladi.")],
                 "Ali: +998901112233\nKontaktlar soni: 3"),
            step("phonebook.py", "get bilan xavfsiz qidirish", r'''
ism = input("Kimni qidiramiz? ")
print(kitob.get(ism, "Topilmadi"))''',
                 [("kitob[\"Sardor\"]", "yo'q kalit — KeyError xatosi."),
                  (".get(k, \"Topilmadi\")", "yo'q bo'lsa — ikkinchi qiymat qaytadi.")],
                 "Kimni qidiramiz? Sardor\nTopilmadi"),
            step("phonebook.py", "Hammasini chiqarish", r'''
for ism, tel in kitob.items():
    print(f"{ism}: {tel}")''',
                 [(".items()", "kalit va qiymat juftliklari."),
                  ("ism, tel", "har juftlik ikki o'zgaruvchiga ochiladi.")],
                 "Ali: +998901112233\nLaylo: +998935556677\nVali: +998977778899"),
        ],
        {"phonebook.py": PHONE1},
        [("python/", ""), ("├── subjects.py", ""), ("└── phonebook.py", "yangi")],
        ["Lug'at: kalit → qiymat", "Qo'shish va almashtirish", "get() bilan xavfsiz qidirish", "items() bilan aylanish"],
        ["Majburiy: har kontaktga email qo'shing (qiymat — lug'at).",
         "Qo'shimcha: keys() va values() ni chiqarib ko'ring."],
        "4.6 · Dict metodlari va aylanish.",
        run={"file": "phonebook.py", "input": "Sardor\n", "expect": ["Kontaktlar soni: 3", "Topilmadi", "Vali: +998977778899"]},
    ),
    "DP18": lesson(
        M, 6, "Dict metodlari va aylanish",
        "Telefon kitobchasini menyuli dasturga aylantiramiz: qidirish, saqlash, o'chirish.",
        "O'tgan darsda: dict, get(), items().",
        "kitob.get(\"X\", 0) X yo'q bo'lsa nima qaytaradi?",
        "Qism bo'yicha qidirish (in), pop(k, None), sorted(lug'at) — kalitlar bo'yicha.",
        "Telefon raqami +998 bilan boshlanishini tekshiring.",
        [("📋", "Menyu", "1–4, 0", "loop"),
         ("🔍", "Qidirish", "qism in ism", ""),
         ("💾", "Saqlash", "kitob[ism] = tel", "mem"),
         ("🗑", "pop()", "o'chirish", ""),
         ("🔤", "sorted", "alifbo bo'yicha", "")],
        [
            step("phonebook.py", "Ism qismi bo'yicha qidirish", r'''
kitob = {"Ali": "+998901112233", "Laylo": "+998935556677"}

while True:
    tanlov = input("1-qidir 2-saqla 3-o'chir 4-hammasi 0-chiqish: ")
    if tanlov == "1":
        qism = input("Ism (qismi): ").lower()
        topildi = False
        for ism, tel in kitob.items():
            if qism in ism.lower():
                print(f"{ism}: {tel}")
                topildi = True
        if not topildi:
            print("Topilmadi")''',
                 [("qism in ism", "satr ichida bo'lakni qidiradi: \"la\" in \"laylo\"."),
                  (".lower()", "katta-kichik harfga qaramay qidirish."),
                  ("topildi", "bayroq: birorta topilmasa xabar beramiz.")],
                 "Ism (qismi): la\nLaylo: +998935556677"),
            step("phonebook.py", "Saqlash va o'chirish", r'''
    elif tanlov == "2":
        ism = input("Ism: ").title()
        kitob[ism] = input("Telefon: ")
        print("✅ Saqlandi")
    elif tanlov == "3":
        ism = input("Ism: ").title()
        print("🗑 O'chirildi" if kitob.pop(ism, None) else "Bunday kontakt yo'q")''',
                 [(".title()", "\"vali\" → \"Vali\" — kalitlar bir xil ko'rinishda."),
                  ("kitob[ism] = ...", "yangi bo'lsa qo'shiladi, bor bo'lsa tahrirlanadi."),
                  (".pop(k, None)", "o'chiradi va qiymatni qaytaradi; yo'q bo'lsa None.")],
                 "Ism: vali\nTelefon: +998977778899\n✅ Saqlandi\nIsm: ali\n🗑 O'chirildi"),
            step("phonebook.py", "Alifbo bo'yicha ro'yxat", r'''
    elif tanlov == "4":
        for ism in sorted(kitob):
            print(f"{ism}: {kitob[ism]}")
    elif tanlov == "0":
        break''',
                 [("sorted(kitob)", "lug'atni aylanganda kalitlar keladi — alifbo bo'yicha saralaymiz."),
                  ("kitob[ism]", "har kalit bo'yicha qiymat.")],
                 "Laylo: +998935556677\nVali: +998977778899"),
        ],
        {"phonebook.py": PHONE2},
        [("python/", ""), ("├── subjects.py", ""), ("└── phonebook.py", "o‘zgardi")],
        ["Qism bo'yicha qidirish", "Tahrirlash = qayta yozish", "pop(k, None)", "sorted(lug'at)"],
        ["Majburiy: telefon +998 bilan boshlanishini tekshiring (startswith).",
         "Qo'shimcha: kontaktlar sonini menyuning tepasida ko'rsating."],
        "4.7 · Ichma-ich ma'lumot: o'quvchilar reytingi.",
        run={"file": "phonebook.py", "input": "1\nla\n2\nvali\n+998977778899\n3\nali\n4\n0\n", "expect": ["Laylo: +998935556677", "✅ Saqlandi", "🗑 O'chirildi", "Vali: +998977778899"]},
    ),
    "DP19": lesson(
        M, 7, "Ichma-ich ma'lumot: o'quvchilar reytingi",
        "Haqiqiy ma'lumot ichma-ich bo'ladi: lug'atlar ro'yxati bilan reyting tuzamiz.",
        "O'tgan darsda: dict metodlari, menyuli telefon kitobchasi.",
        "kitob.pop(\"X\", None) X yo'q bo'lsa nima qaytaradi?",
        "list[dict] — har o'quvchi bitta lug'at; qadam-baqadam murojaat d[\"k\"][i]; lug'atga yangi kalit qo'shish.",
        "Har o'quvchiga “sinf” kalitini qo'shib, sinf bo'yicha guruhlang.",
        [("📋", "Ro'yxat", "o'quvchilar", ""),
         ("📒", "Lug'at", "ism, baholar", "mem"),
         ("➗", "o'rtacha", "har biriga qo'shamiz", ""),
         ("🏆", "Eng yaxshi", "solishtirish", ""),
         ("🎯", "[1][\"baholar\"][1]", "chuqur murojaat", "")],
        [
            step("rating.py", "Lug'atlar ro'yxati", r'''
oquvchilar = [
    {"ism": "Ali", "baholar": [5, 4, 5]},
    {"ism": "Laylo", "baholar": [5, 5, 5]},
    {"ism": "Vali", "baholar": [3, 4, 4]},
]''',
                 [("har qator", "bitta o'quvchi — bitta lug'at."),
                  ("\"baholar\": [...]", "lug'at ichida ro'yxat."),
                  ("ko'p qatorli", "o'qish oson bo'lishi uchun har element alohida qatorda.")],
                 "3 ta o'quvchi xotirada"),
            step("rating.py", "O'rtachani qo'shamiz va eng yaxshisini topamiz", r'''
for o in oquvchilar:
    o["orta"] = round(sum(o["baholar"]) / len(o["baholar"]), 2)

eng_yaxshi = oquvchilar[0]
for o in oquvchilar:
    if o["orta"] > eng_yaxshi["orta"]:
        eng_yaxshi = o''',
                 [("o[\"orta\"] = ...", "har lug'atga yangi kalit qo'shiladi."),
                  ("o", "sikldagi o — ro'yxatdagi lug'atning o'zi, nusxa emas."),
                  ("eng_yaxshi", "o'rtachasi kattarog'ini saqlaymiz.")],
                 "Ali 4.67 · Laylo 5.0 · Vali 3.67"),
            step("rating.py", "Natija va chuqur murojaat", r'''
for o in oquvchilar:
    print(f"{o['ism']}: {o['orta']}")
print("🏆 Eng yaxshi:", eng_yaxshi["ism"])
print("Layloning 2-bahosi:", oquvchilar[1]["baholar"][1])''',
                 [("f\"{o['ism']}\"", "f-string ichida boshqa turdagi qo'shtirnoq."),
                  ("[1][\"baholar\"][1]", "qadam-baqadam: 2-o'quvchi → baholar → 2-baho.")],
                 "Ali: 4.67\nLaylo: 5.0\nVali: 3.67\n🏆 Eng yaxshi: Laylo\nLayloning 2-bahosi: 5"),
        ],
        {"rating.py": RATING1},
        [("python/", ""), ("├── phonebook.py", ""), ("└── rating.py", "yangi")],
        ["list[dict] tuzilmasi", "Lug'atga yangi kalit qo'shish", "Chuqur murojaat", "Eng yaxshisini topish"],
        ["Majburiy: “sinf” kalitini qo'shib, har sinfning o'rtachasini chiqaring.",
         "Qo'shimcha: 2 o'lchamli ro'yxat — 3×3 jadvalning diagonalini chiqaring."],
        "4.8 · Funksiyalar: def, parametr, return.",
        run={"file": "rating.py", "input": "", "expect": ["Ali: 4.67", "Laylo: 5.0", "🏆 Eng yaxshi: Laylo", "Layloning 2-bahosi: 5"]},
    ),
    "DP20": lesson(
        M, 8, "Funksiyalar: def, parametr, return",
        "Kalkulyatorni funksiyalarga bo'lamiz: har funksiya bitta ishni bajaradi.",
        "O'tgan darsda: ichma-ich ma'lumot, reyting.",
        "oquvchilar[1][\"baholar\"][1] qanday o'qiladi?",
        "def nom(parametrlar):, return — natijani qaytaradi; parametr va argument; funksiya funksiyani chaqiradi.",
        "is_even(n) va max_of_three(a, b, c) funksiyalarini yozing.",
        [("⌨", "\"12 * 3\"", "split()", ""),
         ("📞", "hisobla()", "amalga qarab", "mem"),
         ("➕", "qosh() · bol()", "kichik funksiyalar", ""),
         ("↩", "return", "natija", ""),
         ("🖥", "Natija", "36.0", "")],
        [
            step("calc.py", "Kichik funksiyalar", r'''
def qosh(a, b):
    return a + b


def bol(a, b):
    if b == 0:
        return None
    return a / b''',
                 [("def qosh(a, b):", "e'lon: nom va parametrlar."),
                  ("return", "natijani qaytaradi va funksiyani <b>darhol tugatadi</b>."),
                  ("None", "“natija yo'q” — nolga bo'lishda.")],
                 "qosh(2, 3) → 5\nbol(1, 0) → None"),
            step("calc.py", "Funksiya funksiyani chaqiradi", r'''
def hisobla(a, amal, b):
    if amal == "+":
        return qosh(a, b)
    if amal == "-":
        return a - b
    if amal == "*":
        return a * b
    if amal == "/":
        return bol(a, b)
    return None''',
                 [("return erta", "mos amal topilgach qolgan if'lar tekshirilmaydi."),
                  ("qosh(a, b)", "oldin yozilgan funksiyani qayta ishlatamiz."),
                  ("oxirgi return", "noma'lum amal uchun.")],
                 "hisobla(12, \"*\", 3) → 36"),
            step("calc.py", "Ifodani o'qib hisoblaymiz", r'''
ifoda = input("Ifoda (masalan 12 * 3): ").split()
a, amal, b = float(ifoda[0]), ifoda[1], float(ifoda[2])
natija = hisobla(a, amal, b)
print("Natija:", natija if natija is not None else "xato")''',
                 [(".split()", "\"12 * 3\" → [\"12\", \"*\", \"3\"]."),
                  ("argument", "chaqirishda beriladigan qiymat (a, amal, b)."),
                  ("is not None", "None'ni tekshirishning to'g'ri usuli.")],
                 "Ifoda (masalan 12 * 3): 12 * 3\nNatija: 36.0"),
        ],
        {"calc.py": CALC3},
        [("python/", ""), ("├── rating.py", ""), ("└── calc.py", "o‘zgardi")],
        ["def va return", "Parametr va argument", "Funksiyadan funksiyani chaqirish", "None qiymati"],
        ["Majburiy: is_even(n) va max_of_three(a, b, c) funksiyalari.",
         "Qo'shimcha: kalkulyatorga “^” — daraja amalini funksiya bilan qo'shing."],
        "4.9 · Default qiymatlar, *args va scope.",
        run={"file": "calc.py", "input": "12 * 3\n", "expect": ["Natija: 36.0"]},
    ),
    "DP21": lesson(
        M, 9, "Default qiymatlar, *args va scope",
        "Vazifalar ro'yxatini funksiyalar bilan qayta yozamiz: moslashuvchan parametrlar.",
        "O'tgan darsda: def, return, funksiya ichida funksiya chaqirish.",
        "return yozilmagan funksiya nima qaytaradi?",
        "Default qiymat (x=\"...\"), *args — istalgancha argument (tuple), enumerate, lokal va global o'zgaruvchi.",
        "add_tasks(*tasks) dan foydalanib 5 ta vazifani birdan qo'shing va 3-sini o'chiring.",
        [("📋", "vazifalar", "global ro'yxat", "mem"),
         ("➕", "qosh(*yangilar)", "istalgancha", ""),
         ("👁", "korsat(sarlavha=...)", "default", ""),
         ("🗑", "ochir(raqam)", "pop", ""),
         ("🖥", "Natija", "2 ta qoldi", "")],
        [
            step("todo.py", "*args bilan qo'shish", r'''
vazifalar = []


def qosh(*yangilar):
    for v in yangilar:
        vazifalar.append(v)
    return len(yangilar)''',
                 [("*yangilar", "nechta argument berilsa ham — tuple bo'lib keladi."),
                  ("vazifalar", "funksiyadan tashqarida — global; append bilan o'zgartirish mumkin."),
                  ("return len", "nechtasi qo'shilganini qaytaramiz.")],
                 "qosh(\"A\", \"B\", \"C\") → 3"),
            step("todo.py", "Default qiymat va enumerate", r'''
def korsat(sarlavha="Vazifalar"):
    print(f"--- {sarlavha} ({len(vazifalar)}) ---")
    for n, v in enumerate(vazifalar, start=1):
        print(f"{n}. {v}")''',
                 [("sarlavha=\"Vazifalar\"", "argument berilmasa shu qiymat ishlatiladi."),
                  ("enumerate(..., start=1)", "raqam va element birga — n += 1 kerak emas.")],
                 "--- Vazifalar (3) ---\n1. Kitob o'qish\n2. Sport\n3. Ingliz tili"),
            step("todo.py", "O'chirish va chaqirish", r'''
def ochir(raqam):
    if 1 <= raqam <= len(vazifalar):
        return vazifalar.pop(raqam - 1)
    return None


soni = qosh("Kitob o'qish", "Sport", "Ingliz tili")
print("Qo'shildi:", soni)
korsat()
print("O'chirildi:", ochir(2))
korsat("Bugun")''',
                 [("raqam - 1", "foydalanuvchi 1 dan, indeks 0 dan sanaydi."),
                  ("korsat()", "argumentsiz — default sarlavha."),
                  ("korsat(\"Bugun\")", "o'z sarlavhamiz.")],
                 "O'chirildi: Sport\n--- Bugun (2) ---\n1. Kitob o'qish\n2. Ingliz tili"),
        ],
        {"todo.py": TODO2},
        [("python/", ""), ("├── calc.py", ""), ("└── todo.py", "o‘zgardi")],
        ["Default qiymatli parametr", "*args", "enumerate", "Global va lokal o'zgaruvchi"],
        ["Majburiy: 5 ta vazifani birdan qo'shing va 3-sini o'chiring.",
         "Qo'shimcha: **kwargs bilan vazifaga muhimlik va muddat bering."],
        "4.10 · lambda, sorted, map va filter.",
        run={"file": "todo.py", "input": "", "expect": ["Qo'shildi: 3", "O'chirildi: Sport", "--- Bugun (2) ---", "2. Ingliz tili"]},
    ),
    "DP22": lesson(
        M, 10, "lambda, sorted, map va filter",
        "Reytingni turli mezon bo'yicha saralaymiz va filtrlaymiz — qisqa funksiyalar bilan.",
        "O'tgan darsda: default qiymat, *args, enumerate.",
        "def kv(x): return x * x ni qisqaroq qanday yozish mumkin?",
        "lambda x: ifoda; sorted(key=..., reverse=True); map — har elementga; filter — shartga mos; max(key=...).",
        "O'quvchilarni ism uzunligi bo'yicha saralang.",
        [("📋", "Juftliklar", "(ism, ball)", ""),
         ("λ", "lambda", "o[1] — ball", "mem"),
         ("⇅", "sorted", "ball / ism", ""),
         ("🔍", "filter", "≥ 70", ""),
         ("🏆", "max(key)", "eng yuqori", "")],
        [
            step("rating.py", "Ball bo'yicha saralash", r'''
oquvchilar = [("Ali", 87), ("Laylo", 95), ("Vali", 72), ("Sardor", 64)]

by_ball = sorted(oquvchilar, key=lambda o: o[1], reverse=True)
print("Reyting:", by_ball)''',
                 [("lambda o: o[1]", "o ni olib o[1] ni qaytaradigan qisqa funksiya."),
                  ("key=", "qaysi belgi bo'yicha solishtirish."),
                  ("reverse=True", "kattadan kichikka.")],
                 "Reyting: [('Laylo', 95), ('Ali', 87), ('Vali', 72), ('Sardor', 64)]"),
            step("rating.py", "Alifbo va map", r'''
by_name = sorted(oquvchilar, key=lambda o: o[0])
print("Alifbo:", list(map(lambda o: o[0], by_name)))''',
                 [("o[0]", "ism bo'yicha saralash."),
                  ("map(f, ro'yxat)", "har elementga f ni qo'llaydi."),
                  ("list(...)", "map iterator qaytaradi — ro'yxatga o'raymiz.")],
                 "Alifbo: ['Ali', 'Laylo', 'Sardor', 'Vali']"),
            step("rating.py", "filter va max(key)", r'''
otganlar = list(filter(lambda o: o[1] >= 70, oquvchilar))
print("O'tganlar:", len(otganlar))

print("Eng yuqori:", max(oquvchilar, key=lambda o: o[1])[0])''',
                 [("filter", "lambda True qaytarganlarini qoldiradi."),
                  ("max(key=...)", "eng katta ballli juftlik; [0] — uning ismi.")],
                 "O'tganlar: 3\nEng yuqori: Laylo"),
        ],
        {"rating.py": RATING2},
        [("python/", ""), ("├── todo.py", ""), ("└── rating.py", "o‘zgardi")],
        ["lambda", "sorted(key, reverse)", "map va filter", "max(key)"],
        ["Majburiy: o'quvchilarni ism uzunligi bo'yicha saralang.",
         "Qo'shimcha: map bilan har ballga 5 ball bonus qo'shing (100 dan oshmasin)."],
        "4.11 · List comprehension va matn tahlili.",
        run={"file": "rating.py", "input": "", "expect": ["Reyting: [('Laylo', 95), ('Ali', 87), ('Vali', 72), ('Sardor', 64)]", "Alifbo: ['Ali', 'Laylo', 'Sardor', 'Vali']", "O'tganlar: 3", "Eng yuqori: Laylo"]},
    ),
    "DP23": lesson(
        M, 11, "List comprehension va matn tahlili",
        "Matnni tahlil qilamiz: so'zlar, uzun so'zlar va eng ko'p takrorlangani.",
        "O'tgan darsda: lambda, sorted, map, filter.",
        "filter(lambda x: x > 3, [1, 5, 2, 7]) nima qoldiradi?",
        "[ifoda for x in ro'yxat if shart] — sikl va shart bir qatorda; split(); lug'at bilan sanash.",
        "Matndagi raqamlar sonini comprehension bilan toping.",
        [("⌨", "Matn", "input()", ""),
         ("✂", "split()", "so'zlarga", ""),
         ("🧹", "comprehension", "tozalash", "mem"),
         ("🔢", "sanoq{}", "get(s, 0) + 1", ""),
         ("🏆", "max(key)", "eng ko'p so'z", "")],
        [
            step("text_stats.py", "So'zlarni ajratib tozalaymiz", r'''
matn = input("Matn: ")

sozlar = [s.strip(".,!?").lower() for s in matn.split()]
print("So'zlar soni:", len(sozlar))''',
                 [(".split()", "probellar bo'yicha so'zlarga bo'ladi."),
                  ("[... for s in ...]", "har so'zni tozalab yangi ro'yxat yasaydi."),
                  (".strip(\".,!?\")", "chetidagi tinish belgilarini olib tashlaydi.")],
                 "Matn: Python oson. Python kuchli va Python qiziqarli!\nSo'zlar soni: 7"),
            step("text_stats.py", "Shartli comprehension", r'''
uzunlar = [s for s in sozlar if len(s) > 4]
print("Uzun so'zlar:", uzunlar)''',
                 [("if len(s) > 4", "faqat shartga mos so'zlar qoladi."),
                  ("filter o'rnida", "comprehension ko'pincha o'qishga osonroq.")],
                 "Uzun so'zlar: ['python', 'python', 'kuchli', 'python', 'qiziqarli']"),
            step("text_stats.py", "Sanash va eng ko'pi", r'''
sanoq = {}
for s in sozlar:
    sanoq[s] = sanoq.get(s, 0) + 1
eng_kop = max(sanoq, key=sanoq.get)
print(f"Eng ko'p: {eng_kop} ({sanoq[eng_kop]} marta)")

unlilar = [h for h in matn.lower() if h in "aeiou"]
print("Unli harflar:", len(unlilar))''',
                 [("get(s, 0) + 1", "birinchi uchraganda 0 dan boshlaydi."),
                  ("max(sanoq, key=sanoq.get)", "qiymati eng katta kalit."),
                  ("h in \"aeiou\"", "satr ichida harf bormi.")],
                 "Eng ko'p: python (3 marta)\nUnli harflar: 12"),
        ],
        {"text_stats.py": TEXT},
        [("python/", ""), ("├── rating.py", ""), ("└── text_stats.py", "yangi")],
        ["List comprehension", "Shartli comprehension", "Lug'at bilan sanash", "max(key=d.get)"],
        ["Majburiy: matndagi raqamlar sonini comprehension bilan toping.",
         "Qo'shimcha: har so'zning uzunligi bilan lug'at yasang ({s: len(s) ...})."],
        "4.12 · 4-oy loyihasi: “Kundalik”.",
        run={"file": "text_stats.py", "input": "Python oson. Python kuchli va Python qiziqarli!\n", "expect": ["So'zlar soni: 7", "Eng ko'p: python (3 marta)", "Unli harflar: 12"]},
    ),
    "DP24": lesson(
        M, 12, "4-oy loyihasi: “Kundalik” va nazorat",
        "Oy davomida o'rganganlarni bitta dasturga yig'amiz: list[dict], funksiyalar va menyu.",
        "4-oyda: list, tuple, set, dict, funksiyalar, lambda, comprehension.",
        "list[dict] va funksiyalar — oyni 5 savol bilan takrorlaymiz.",
        "Loyiha tuzilmasi: ma'lumot (vazifalar) → har amal uchun funksiya → menyu sikli.",
        "Vazifaga muhimlik darajasini qo'shib, shu bo'yicha saralang.",
        [("📋", "vazifalar", "list[dict]", "mem"),
         ("🧩", "Funksiyalar", "qosh, royxat, ...", ""),
         ("📋", "Menyu", "while True", "loop"),
         ("✔", "Bajarildi", "True qilish", ""),
         ("👋", "Chiqish", "hisobot", "")],
        [
            step("diary.py", "Ma'lumot va menyu funksiyasi", r'''
vazifalar = []


def menyu():
    print("\n1) Qo'shish  2) Ro'yxat  3) Bajarildi  4) O'chirish  0) Chiqish")
    return input("Tanlang: ")


def qosh():
    matn = input("Vazifa: ").strip()
    if matn:
        vazifalar.append({"matn": matn, "bajarildi": False})
        print("✅ Qo'shildi")''',
                 [("{\"matn\", \"bajarildi\"}", "har vazifa — lug'at: matn va holat."),
                  ("menyu()", "menyuni chiqarib, tanlovni qaytaradi."),
                  ("if matn:", "bo'sh vazifa qo'shilmaydi.")],
                 "1) Qo'shish  2) Ro'yxat  3) Bajarildi  4) O'chirish  0) Chiqish\nTanlang: 1\nVazifa: Kitob o'qish\n✅ Qo'shildi"),
            step("diary.py", "Ro'yxat va raqamni so'rash", r'''
def royxat():
    if not vazifalar:
        print("Ro'yxat bo'sh")
    for n, v in enumerate(vazifalar, start=1):
        belgi = "✔" if v["bajarildi"] else "☐"
        print(f"{n}. {belgi} {v['matn']}")


def raqam_sora():
    javob = input("Raqam: ")
    if javob.isdigit() and 1 <= int(javob) <= len(vazifalar):
        return int(javob) - 1
    print("Noto'g'ri raqam")
    return None''',
                 [("belgi", "bajarilganiga ✔, qolganiga ☐."),
                  ("raqam_sora()", "tekshirib indeks qaytaradi — 2 joyda ishlatiladi."),
                  ("None", "noto'g'ri raqam bo'lsa.")],
                 "1. ✔ Kitob o'qish\n2. ☐ Sport"),
            step("diary.py", "Menyu sikli", r'''
while True:
    tanlov = menyu()
    if tanlov == "1":
        qosh()
    elif tanlov == "2":
        royxat()
    elif tanlov == "3":
        i = raqam_sora()
        if i is not None:
            vazifalar[i]["bajarildi"] = True
    elif tanlov == "4":
        i = raqam_sora()
        if i is not None:
            print("🗑", vazifalar.pop(i)["matn"])
    elif tanlov == "0":
        bajarilgan = len([v for v in vazifalar if v["bajarildi"]])
        print(f"Xayr! Bajarildi: {bajarilgan}/{len(vazifalar)}")
        break''',
                 [("qisqa sikl", "har amal — bitta funksiya chaqiruvi."),
                  ("vazifalar[i][\"bajarildi\"]", "lug'atdagi holatni o'zgartiramiz."),
                  ("comprehension", "bajarilganlarni sanash.")],
                 "Tanlang: 4\nRaqam: 2\n🗑 Sport\nTanlang: 0\nXayr! Bajarildi: 1/1"),
        ],
        {"diary.py": DIARY},
        [("python/", ""), ("├── text_stats.py", ""), ("└── diary.py", "yangi")],
        ["list[dict] bilan loyiha", "Har amal uchun funksiya", "Kiritishni tekshirish", "Hisobot (comprehension)"],
        ["Majburiy: vazifaga muhimlik (1–3) qo'shing va ro'yxatni shu bo'yicha saralang.",
         "Qo'shimcha: “5) Qidirish” — matn bo'yicha vazifa topish."],
        "5.1 · Modullar: random va datetime.",
        run={"file": "diary.py", "input": "1\nKitob o'qish\n1\nSport\n3\n1\n2\n4\n2\n0\n", "expect": ["1. ✔ Kitob o'qish", "2. ☐ Sport", "🗑 Sport", "Xayr! Bajarildi: 1/1"]},
    ),
}
