"""Dasturchi 3-oy · Python asoslari: 12 dars "Dars kodi" (kalit — ``dev.py``). Kod ``run`` bilan sinaladi."""

from .lesson_kit import lesson, step

M = "3-oy · Python asoslari"

HELLO = r'''
# Mening birinchi dasturim
print("Salom! Mening ismim Ali.")
print("Men 13 yoshdaman.")
print("Sevimli fanim: informatika")
print("Orzuim: dasturchi bo'lish")
print("Python", "juda", "zo'r", sep=" ⭐ ")
print("=" * 30)
print("Tugadi", end="!\n")
'''

PROFILE = r'''
ism = "Ali"
yosh = 13
boy = 1.58
oquvchi = True

print("Ism:", ism)
print("Yosh:", yosh)
print("Bo'y:", boy, "m")
print("O'quvchimi:", oquvchi)

print(type(ism), type(yosh))
print(type(boy), type(oquvchi))

yosh = yosh + 1
print("Keyingi yil:", yosh)
'''

AGE = r'''
ism = input("Ismingiz: ")
yil = int(input("Tug'ilgan yilingiz: "))

JORIY_YIL = 2026
yosh = JORIY_YIL - yil

print(f"{ism}, siz {yosh} yoshdasiz")
print("100 yoshga", 100 - yosh, "yil qoldi")
print("Oylarda:", yosh * 12)
'''

CALC1 = r'''
a = float(input("Birinchi son: "))
b = float(input("Ikkinchi son: "))

print("Yig'indi:", a + b)
print("Ayirma:", a - b)
print("Ko'paytma:", a * b)
print("Bo'linma:", round(a / b, 2))
'''

NAME = r'''
ism = input("Ism: ").strip()
familiya = input("Familiya: ").strip()

ism = ism.title()
familiya = familiya.title()
toliq = f"{familiya} {ism}"

print("To'liq ism:", toliq)
print("Harflar soni:", len(ism + familiya))
print("Bosh harflar:", ism[0] + familiya[0])
print("Katta harflarda:", toliq.upper())
print("Teskari:", ism[::-1])
'''

LOGIN = r'''
LOGIN = "admin"
PAROL = "minar2026"

login = input("Login: ")
parol = input("Parol: ")

togri_login = login == LOGIN
togri_parol = parol == PAROL
print("Login to'g'rimi?", togri_login)
print("Parol to'g'rimi?", togri_parol)

print("Kirish mumkinmi?", togri_login and togri_parol)
print("Biror xato bormi?", not togri_login or not togri_parol)
print("Parol uzunmi?", len(parol) >= 8)
'''

GRADE = r'''
ball = int(input("Ballingiz (0–100): "))

if ball >= 86:
    baho = 5
    izoh = "A'lo"
elif ball >= 71:
    baho = 4
    izoh = "Yaxshi"
elif ball >= 56:
    baho = 3
    izoh = "Qoniqarli"
else:
    baho = 2
    izoh = "Qayta topshiring"

print(f"Baho: {baho} ({izoh})")
if ball == 100:
    print("🏆 Mukammal natija!")
'''

CALC2 = r'''
print("1) Qo'shish  2) Ayirish  3) Ko'paytirish  4) Bo'lish")
tanlov = input("Amal: ")
a = float(input("a = "))
b = float(input("b = "))

match tanlov:
    case "1":
        print("Natija:", a + b)
    case "2":
        print("Natija:", a - b)
    case "3":
        print("Natija:", a * b)
    case "4":
        if b == 0:
            print("Nolga bo'lib bo'lmaydi!")
        else:
            print("Natija:", a / b)
    case _:
        print("Bunday amal yo'q")
'''

GUESS1 = r'''
import random

son = random.randint(1, 100)
taxmin = 0

while taxmin != son:
    taxmin = int(input("1–100 orasida son: "))
    if taxmin < son:
        print("Kattaroq son ayting ⬆")
    elif taxmin > son:
        print("Kichikroq son ayting ⬇")

print("🎉 Topdingiz! Son:", son)
'''

TABLE = r'''
n = int(input("Qaysi son uchun jadval? "))

for i in range(1, 11):
    print(f"{n} × {i} = {n * i}")

jami = 0
for i in range(1, 101):
    jami += i
print("1 dan 100 gacha yig'indi:", jami)

for i in range(10, 0, -2):
    print(i, end=" ")
print()
'''

GUESS2 = r'''
import random

while True:
    son = random.randint(1, 100)
    urinish = 0
    while True:
        javob = input("Son: ")
        if not javob.isdigit():
            print("Faqat raqam kiriting!")
            continue
        urinish += 1
        taxmin = int(javob)
        if taxmin == son:
            print(f"🎉 Topdingiz! {urinish} ta urinishda")
            break
        print("Kattaroq ⬆" if taxmin < son else "Kichikroq ⬇")
        if urinish == 7:
            print("Urinishlar tugadi. Son:", son)
            break
    if input("Yana o'ynaysizmi? (ha/yo'q): ") != "ha":
        break

print("Xayr! 👋")
'''

BANK = r'''
balans = 0
tarix = ""

while True:
    print("\n1) Balans  2) Kirim  3) Chiqim  4) Tarix  0) Chiqish")
    tanlov = input("Tanlang: ")
    if tanlov == "1":
        print(f"💰 Balans: {balans:,} so'm")
    elif tanlov == "2":
        summa = int(input("Kirim summasi: "))
        balans += summa
        tarix += f"+{summa:,}\n"
        print("✅ Qabul qilindi")
    elif tanlov == "3":
        summa = int(input("Chiqim summasi: "))
        if summa > balans:
            print("❌ Mablag' yetarli emas")
        else:
            balans -= summa
            tarix += f"-{summa:,}\n"
            print("✅ Yechildi")
    elif tanlov == "4":
        print(tarix or "Hali amal yo'q")
    elif tanlov == "0":
        print("Xayr! 👋")
        break
    else:
        print("Noto'g'ri tanlov")
'''

LESSONS = {
    "DP01": lesson(
        M, 1, "Python va VS Code: birinchi dastur (print)",
        "Python va VS Code'ni o'rnatamiz, birinchi faylni yozib, terminalda ishga tushiramiz.",
        "Starter'da: Terminal buyruqlari (cd, ls), fayl va papka yaratish.",
        "Terminal: cd, ls, mkdir — 3 ta savol bilan eslatamiz.",
        "Dastur nima, interpretator, .py fayl, print() va satr (qo'shtirnoq ichidagi matn).",
        "O'z “vizitkangiz”ni 5 qator qilib yozing va sep bilan bezang.",
        [("⬇", "O'rnatish", "python.org, “Add to PATH” ✓", ""),
         ("🗂", "VS Code", "papka va hello.py fayli", ""),
         ("✍", "Kod", "print(\"...\")", "mem"),
         ("▶", "Ishga tushirish", "python hello.py", ""),
         ("🖥", "Natija", "terminalda 7 qator", "")],
        [
            step("hello.py", "print bilan matn chiqaramiz", r'''
# Mening birinchi dasturim
print("Salom! Mening ismim Ali.")
print("Men 13 yoshdaman.")
print("Sevimli fanim: informatika")
print("Orzuim: dasturchi bo'lish")''',
                 [("print(...)", "qavs ichidagini ekranga chiqaradi."),
                  ("\"...\"", "satr — qo'shtirnoq ichidagi matn. Qo'shtirnoq yopilishini unutmang."),
                  ("# izoh", "Python o'qimaydi — o'zimiz uchun eslatma.")],
                 "Salom! Mening ismim Ali.\nMen 13 yoshdaman.\nSevimli fanim: informatika\nOrzuim: dasturchi bo'lish"),
            step("hello.py", "sep, * va end", r'''
print("Python", "juda", "zo'r", sep=" ⭐ ")
print("=" * 30)
print("Tugadi", end="!\n")''',
                 [("sep=", "vergul bilan berilgan qiymatlar orasiga qo'yiladigan belgi (odatda probel)."),
                  ("\"=\" * 30", "satrni 30 marta takrorlaydi — chiziq chizish uchun qulay."),
                  ("end=", "qator oxiridagi belgi (odatda yangi qator)."),],
                 "Python ⭐ juda ⭐ zo'r\n==============================\nTugadi!"),
            step("Terminal", "Dasturni ishga tushiramiz", r'''
$ cd Desktop/python
$ python hello.py''',
                 [("cd", "hello.py turgan papkaga o'tamiz."),
                  ("python hello.py", "Python faylni yuqoridan pastga, qatorma-qator bajaradi."),
                  ("xato bo'lsa", "qizil xabarda qator raqami bor — o'sha qatorni tekshiring.")],
                 "Salom! Mening ismim Ali.\n...\nTugadi!"),
        ],
        {"hello.py": HELLO},
        [("python/", ""), ("└── hello.py", "yangi")],
        ["print() va satrlar", "sep va end parametrlari", "Satrni * bilan takrorlash", "Terminalda python fayl.py"],
        ["Majburiy: vizitkaga sevimli fan va orzu kasbni qo'shing, sep bilan bezang.",
         "Qo'shimcha: print bilan 5 qatorli “archa” chizing (*)."],
        "3.2 · O'zgaruvchilar va ma'lumot turlari.",
        run={"file": "hello.py", "input": "", "expect": ["Python ⭐ juda ⭐ zo'r", "=" * 30, "Tugadi!"]},
    ),
    "DP02": lesson(
        M, 2, "O'zgaruvchilar va ma'lumot turlari",
        "Ma'lumotni nomli o'zgaruvchilarda saqlaymiz va 4 ta asosiy turni farqlaymiz.",
        "O'tgan darsda: print(), satrlar, sep va end.",
        "print(\"A\", \"B\", sep=\"-\") nima chiqaradi? hello.py ni eslaymiz.",
        "O'zgaruvchi = nomli quti. = — “qiymat ber”. Turlar: int, float, str, bool. type().",
        "O'zingiz haqingizda 5 ta o'zgaruvchi yarating va turlarini chiqaring.",
        [("📦", "O'zgaruvchi", "yosh = 13", "mem"),
         ("🔢", "int / float", "13 · 1.58", ""),
         ("🔤", "str", "\"Ali\"", ""),
         ("✅", "bool", "True / False", ""),
         ("🔍", "type()", "turini ko'rish", "")],
        [
            step("profile.py", "O'zgaruvchilar yaratamiz", r'''
ism = "Ali"
yosh = 13
boy = 1.58
oquvchi = True''',
                 [("ism = \"Ali\"", "o'ngdagi qiymat chapdagi nomga yoziladi."),
                  ("nomlash", "harf yoki _ bilan boshlanadi, probel yo'q: <code>mening_ismim</code>."),
                  ("True", "bool — faqat True yoki False, bosh harf bilan.")],
                 "(hali hech narsa chiqmaydi — qiymatlar xotirada)"),
            step("profile.py", "Qiymatlarni chiqaramiz va turini bilamiz", r'''
print("Ism:", ism)
print("Yosh:", yosh)
print("Bo'y:", boy, "m")
print("O'quvchimi:", oquvchi)

print(type(ism), type(yosh))
print(type(boy), type(oquvchi))''',
                 [("print(\"Ism:\", ism)", "o'zgaruvchi qo'shtirnoqsiz yoziladi — qiymati chiqadi."),
                  ("type()", "qiymat turini ko'rsatadi: str, int, float, bool.")],
                 "Ism: Ali\nYosh: 13\nBo'y: 1.58 m\nO'quvchimi: True\n<class 'str'> <class 'int'>\n<class 'float'> <class 'bool'>"),
            step("profile.py", "Qiymatni yangilaymiz", r'''
yosh = yosh + 1
print("Keyingi yil:", yosh)''',
                 [("yosh = yosh + 1", "avval o'ng tomon hisoblanadi (13 + 1), keyin yoshga yoziladi."),
                  ("eski qiymat", "o'chadi — o'zgaruvchida doim oxirgi qiymat turadi.")],
                 "Keyingi yil: 14"),
        ],
        {"profile.py": PROFILE},
        [("python/", ""), ("├── hello.py", ""), ("└── profile.py", "yangi")],
        ["O'zgaruvchi va = belgisi", "int, float, str, bool", "type() funksiyasi", "Qiymatni yangilash"],
        ["Majburiy: do'stingiz uchun profile2.py — 5 ta o'zgaruvchi va turlari.",
         "Qo'shimcha: ikki o'zgaruvchining qiymatini almashtiring (a, b = b, a)."],
        "3.3 · input() va turlarni o'zgartirish.",
        run={"file": "profile.py", "input": "", "expect": ["<class 'str'> <class 'int'>", "Keyingi yil: 14"]},
    ),
    "DP03": lesson(
        M, 3, "input() va turlarni o'zgartirish",
        "Foydalanuvchidan ma'lumot so'raymiz va matnni songa aylantirib hisoblaymiz.",
        "O'tgan darsda: o'zgaruvchilar, int / float / str / bool, type().",
        "type(\"13\") va type(13) farqi nima?",
        "input() doim str qaytaradi. int(), float(), str() — turlarni o'zgartirish. f-string.",
        "Tug'ilgan yil va oydan yoshni oylarda hisoblang.",
        [("⌨", "input()", "foydalanuvchi yozadi", ""),
         ("🔤", "str", "\"2013\" — matn", ""),
         ("🔁", "int()", "2013 — son", "mem"),
         ("➖", "Hisob", "2026 − 2013", ""),
         ("🖥", "Natija", "f\"{ism}, ...\"", "")],
        [
            step("age.py", "Ma'lumot so'raymiz", r'''
ism = input("Ismingiz: ")
yil = int(input("Tug'ilgan yilingiz: "))''',
                 [("input(\"...\")", "savolni chiqarib, foydalanuvchi yozganini <b>matn</b> qilib qaytaradi."),
                  ("int(...)", "\"2013\" → 2013. Matn bilan hisoblab bo'lmaydi."),
                  ("ichma-ich", "avval input, keyin int — ichkaridan tashqariga.")],
                 "Ismingiz: Ali\nTug'ilgan yilingiz: 2013"),
            step("age.py", "Hisoblaymiz va chiqaramiz", r'''
JORIY_YIL = 2026
yosh = JORIY_YIL - yil

print(f"{ism}, siz {yosh} yoshdasiz")
print("100 yoshga", 100 - yosh, "yil qoldi")
print("Oylarda:", yosh * 12)''',
                 [("JORIY_YIL", "o'zgarmas qiymat — KATTA harflar bilan (konstanta)."),
                  ("f\"{ism}\"", "f-string: qavs ichidagi o'zgaruvchi qiymati matnga qo'yiladi."),
                  ("100 - yosh", "hisobni print ichida ham yozish mumkin.")],
                 "Ali, siz 13 yoshdasiz\n100 yoshga 87 yil qoldi\nOylarda: 156"),
            step("Terminal", "Xatoni ko'ramiz va tushunamiz", r'''
$ python age.py
Tug'ilgan yilingiz: ikki ming
ValueError: invalid literal for int()''',
                 [("ValueError", "int() ga son bo'lmagan matn berildi."),
                  ("yechim", "hozircha raqam bilan yozamiz; 5-oyda try/except bilan ushlashni o'rganamiz.")],
                 "Raqam bilan yozsangiz — dastur to'g'ri ishlaydi."),
        ],
        {"age.py": AGE},
        [("python/", ""), ("├── profile.py", ""), ("└── age.py", "yangi")],
        ["input() — matn qaytaradi", "int() va float() bilan aylantirish", "Konstantalar", "f-string"],
        ["Majburiy: yil va oy bo'yicha yoshni oylarda hisoblang.",
         "Qo'shimcha: kvadrat tomoni so'rab, yuzi va perimetrini chiqaring."],
        "3.4 · Arifmetik amallar: kalkulyator.",
        run={"file": "age.py", "input": "Ali\n2013\n", "expect": ["Ali, siz 13 yoshdasiz", "100 yoshga 87 yil qoldi", "Oylarda: 156"]},
    ),
    "DP04": lesson(
        M, 4, "Arifmetik amallar: kalkulyator",
        "Python'da hisoblaymiz va ikki son uchun oddiy kalkulyator yasaymiz.",
        "O'tgan darsda: input(), int() va float(), f-string.",
        "input() qaysi turni qaytaradi? Nega int() kerak?",
        "+ − * / // % ** amallari, amallar tartibi, round().",
        "Kalkulyatorga //, % va ** amallarini qo'shing.",
        [("⌨", "a va b", "float(input())", ""),
         ("➕", "Amallar", "+  −  *  /", "mem"),
         ("🎯", "round()", "2 xona", ""),
         ("🖥", "Natija", "4 qator", "")],
        [
            step("calc.py", "Ikki sonni so'raymiz", r'''
a = float(input("Birinchi son: "))
b = float(input("Ikkinchi son: "))''',
                 [("float", "kasr sonlar ham kiritilsin: 7.5, 2.25."),
                  ("ikki o'zgaruvchi", "har biri alohida so'raladi.")],
                 "Birinchi son: 7\nIkkinchi son: 2"),
            step("calc.py", "To'rt amalni hisoblaymiz", r'''
print("Yig'indi:", a + b)
print("Ayirma:", a - b)
print("Ko'paytma:", a * b)
print("Bo'linma:", round(a / b, 2))''',
                 [("/", "bo'lish natijasi doim float: 7 / 2 = 3.5."),
                  ("round(x, 2)", "verguldan keyin 2 xona qoldiradi."),
                  ("tartib", "avval ** keyin * / // %, keyin + −; qavs birinchi.")],
                 "Yig'indi: 9.0\nAyirma: 5.0\nKo'paytma: 14.0\nBo'linma: 3.5"),
            step("Terminal", "Qo'shimcha amallarni sinaymiz", r'''
>>> 7 // 2
3
>>> 7 % 2
1
>>> 2 ** 10
1024''',
                 [("//", "butun bo'lish — kasr qismi tashlanadi."),
                  ("%", "qoldiq: juft sonlarda 0 bo'ladi."),
                  (">>>", "terminalda <code>python</code> deb yozsangiz, buyruqlar darhol bajariladi.")],
                 "Uyga vazifada shu amallarni kalkulyatorga qo'shasiz."),
        ],
        {"calc.py": CALC1},
        [("python/", ""), ("├── age.py", ""), ("└── calc.py", "yangi")],
        ["7 ta arifmetik amal", "/ va // farqi", "round()", "Amallar tartibi"],
        ["Majburiy: kalkulyatorga //, % va ** qo'shing.",
         "Qo'shimcha: soniyalarni soat:daqiqa:soniyaga aylantiring (3725 → 1:2:5)."],
        "3.5 · Satrlar, metodlar va f-string.",
        run={"file": "calc.py", "input": "7\n2\n", "expect": ["Yig'indi: 9.0", "Ko'paytma: 14.0", "Bo'linma: 3.5"]},
    ),
    "DP05": lesson(
        M, 5, "Satrlar, metodlar va f-string",
        "Matn bilan ishlaymiz: tozalash, katta-kichik harf, indeks, kesish va uzunlik.",
        "O'tgan darsda: arifmetik amallar va kalkulyator.",
        "7 // 2 va 7 % 2 natijasi qancha?",
        "Satr metodlari (strip, title, upper), len(), indeks [0] va kesish [::-1].",
        "Ism va familiyadan “Ali V.” ko'rinishidagi qisqa ism yasang.",
        [("⌨", "Kiritish", "\"  ali\"", ""),
         ("🧹", "strip / title", "\"Ali\"", "mem"),
         ("📏", "len · [0]", "uzunlik, bosh harf", ""),
         ("🔄", "[::-1]", "teskari", ""),
         ("🖥", "Natija", "5 qator", "")],
        [
            step("name_tool.py", "Kiritilgan matnni tozalaymiz", r'''
ism = input("Ism: ").strip()
familiya = input("Familiya: ").strip()

ism = ism.title()
familiya = familiya.title()
toliq = f"{familiya} {ism}"''',
                 [(".strip()", "boshi va oxiridagi probellarni olib tashlaydi."),
                  (".title()", "har so'zni bosh harf bilan: \"ali\" → \"Ali\"."),
                  ("metod", "satrning o'zini o'zgartirmaydi — yangi satr qaytaradi, shuning uchun qayta yozamiz.")],
                 "Ism:   ali\nFamiliya: valiyev"),
            step("name_tool.py", "Uzunlik, indeks va kesish", r'''
print("To'liq ism:", toliq)
print("Harflar soni:", len(ism + familiya))
print("Bosh harflar:", ism[0] + familiya[0])
print("Katta harflarda:", toliq.upper())
print("Teskari:", ism[::-1])''',
                 [("len()", "satrdagi belgilar soni."),
                  ("ism[0]", "indeks 0 dan boshlanadi — birinchi harf."),
                  ("[::-1]", "kesish: qadam −1 — satrni teskari o'qish.")],
                 "To'liq ism: Valiyev Ali\nHarflar soni: 10\nBosh harflar: AV\nKatta harflarda: VALIYEV ALI\nTeskari: ilA"),
        ],
        {"name_tool.py": NAME},
        [("python/", ""), ("├── calc.py", ""), ("└── name_tool.py", "yangi")],
        ["strip, title, upper metodlari", "len() va indeks", "Kesish va teskari satr", "f-string bilan yig'ish"],
        ["Majburiy: “Ali V.” ko'rinishidagi qisqa ism yasang.",
         "Qo'shimcha: so'z palindrom ekanini tekshiring (s == s[::-1])."],
        "3.6 · Taqqoslash va mantiqiy amallar.",
        run={"file": "name_tool.py", "input": "  ali\nvaliyev\n", "expect": ["To'liq ism: Valiyev Ali", "Harflar soni: 10", "Bosh harflar: AV", "Teskari: ilA"]},
    ),
    "DP06": lesson(
        M, 6, "Taqqoslash va mantiqiy amallar",
        "Savolga True yoki False javob beramiz: login va parolni tekshiradigan dastur.",
        "O'tgan darsda: satr metodlari, len(), indeks va kesish.",
        "len(\"Python\") va \"Python\"[::-1] nima beradi?",
        "== != > < >= <= taqqoslash; and, or, not; = va == farqi.",
        "Parol 8+ belgi va ichida raqam borligini tekshiring.",
        [("⌨", "Login, parol", "input()", ""),
         ("⚖", "==", "to'g'rimi?", "mem"),
         ("🔗", "and / or / not", "ikkala shart", ""),
         ("✅", "True / False", "natija", "")],
        [
            step("login.py", "Konstanta va kiritish", r'''
LOGIN = "admin"
PAROL = "minar2026"

login = input("Login: ")
parol = input("Parol: ")''',
                 [("LOGIN, PAROL", "to'g'ri qiymatlar — konstanta (KATTA harf)."),
                  ("login", "foydalanuvchi yozgani — kichik harfli boshqa o'zgaruvchi.")],
                 "Login: admin\nParol: 12345"),
            step("login.py", "Taqqoslaymiz", r'''
togri_login = login == LOGIN
togri_parol = parol == PAROL
print("Login to'g'rimi?", togri_login)
print("Parol to'g'rimi?", togri_parol)''',
                 [("==", "tenglikni <b>tekshiradi</b> va True/False qaytaradi."),
                  ("=", "qiymat beradi — adashtirmang!"),
                  ("natija", "taqqoslash natijasini o'zgaruvchiga saqlash mumkin.")],
                 "Login to'g'rimi? True\nParol to'g'rimi? False"),
            step("login.py", "Mantiqiy amallar", r'''
print("Kirish mumkinmi?", togri_login and togri_parol)
print("Biror xato bormi?", not togri_login or not togri_parol)
print("Parol uzunmi?", len(parol) >= 8)''',
                 [("and", "ikkalasi True bo'lsagina True."),
                  ("or", "bittasi True bo'lsa yetarli."),
                  ("not", "teskarisi: not True → False.")],
                 "Kirish mumkinmi? False\nBiror xato bormi? True\nParol uzunmi? False"),
        ],
        {"login.py": LOGIN},
        [("python/", ""), ("├── name_tool.py", ""), ("└── login.py", "yangi")],
        ["Taqqoslash amallari", "= va == farqi", "and, or, not", "bool natijani saqlash"],
        ["Majburiy: parol 8+ belgi va ichida raqam borligini tekshiring (any yoki in).",
         "Qo'shimcha: yosh 13 dan 17 gacha ekanini 13 <= yosh <= 17 bilan tekshiring."],
        "3.7 · Shartlar: if, elif, else.",
        run={"file": "login.py", "input": "admin\n12345\n", "expect": ["Login to'g'rimi? True", "Parol to'g'rimi? False", "Kirish mumkinmi? False"]},
    ),
    "DP07": lesson(
        M, 7, "Shartlar: if, elif, else",
        "Dastur qaror qabul qiladi: balldan bahoni aniqlaymiz.",
        "O'tgan darsda: taqqoslash, and / or / not.",
        "True and False nima? 5 != 5 nima?",
        "if / elif / else, ikki nuqta va 4 probel chekinish; faqat bitta blok bajariladi.",
        "Haroratga qarab kiyim maslahatini beradigan dastur yozing.",
        [("⌨", "Ball", "78", ""),
         ("❓", "if ≥ 86", "yo'q", ""),
         ("❓", "elif ≥ 71", "ha → 4", "mem"),
         ("⏭", "qolganlari", "tekshirilmaydi", ""),
         ("🖥", "Natija", "Baho: 4", "")],
        [
            step("grade.py", "Ballni so'raymiz va shart yozamiz", r'''
ball = int(input("Ballingiz (0–100): "))

if ball >= 86:
    baho = 5
    izoh = "A'lo"''',
                 [("if shart:", "oxirida <b>ikki nuqta</b>."),
                  ("4 probel", "chekinish — blok ichidagi qatorlar. Tab ham bo'ladi, aralashtirmang.")],
                 "Ballingiz (0–100): 92 → baho = 5"),
            step("grade.py", "elif va else", r'''
elif ball >= 71:
    baho = 4
    izoh = "Yaxshi"
elif ball >= 56:
    baho = 3
    izoh = "Qoniqarli"
else:
    baho = 2
    izoh = "Qayta topshiring"''',
                 [("elif", "oldingi shart yolg'on bo'lsa, keyingisi tekshiriladi."),
                  ("else:", "hech biri mos kelmasa; shart yozilmaydi."),
                  ("tartib", "kattadan kichikka — aks holda 95 ham “3” oladi.")],
                 "78 → birinchi rost shart: ball >= 71 → baho = 4"),
            step("grade.py", "Natija va alohida shart", r'''
print(f"Baho: {baho} ({izoh})")
if ball == 100:
    print("🏆 Mukammal natija!")''',
                 [("chekinishsiz", "print — shartdan tashqarida, doim bajariladi."),
                  ("yangi if", "alohida savol — oldingi zanjirga bog'liq emas.")],
                 "Baho: 4 (Yaxshi)"),
        ],
        {"grade.py": GRADE},
        [("python/", ""), ("├── login.py", ""), ("└── grade.py", "yangi")],
        ["if / elif / else", "Chekinish (4 probel)", "Shartlar tartibi", "Bitta zanjirda faqat bitta blok"],
        ["Majburiy: haroratga qarab kiyim maslahati (≤0, 1–15, 16–25, >25).",
         "Qo'shimcha: kiritilgan son musbat, manfiy yoki nol ekanini aniqlang."],
        "3.8 · Ichma-ich shart va match-case: menyuli kalkulyator.",
        run={"file": "grade.py", "input": "78\n", "expect": ["Baho: 4 (Yaxshi)"]},
    ),
    "DP08": lesson(
        M, 8, "Ichma-ich shart va match-case: menyuli kalkulyator",
        "Menyudan amal tanlanadigan kalkulyator: match-case va ichma-ich shart.",
        "O'tgan darsda: if / elif / else, baho dasturi.",
        "if, elif, else dan qaysi biriga shart yozilmaydi?",
        "match-case — bitta qiymatni variantlar bilan solishtirish; case _ — qolgan hammasi; ichma-ich if.",
        "Menyuga “0 — chiqish” va noto'g'ri raqam tekshiruvini qo'shing.",
        [("📋", "Menyu", "1–4 amal", ""),
         ("⌨", "Tanlov", "\"4\"", ""),
         ("🔀", "match", "case \"4\"", "mem"),
         ("❓", "if b == 0", "ichma-ich", "loop"),
         ("🖥", "Natija", "yoki ogohlantirish", "")],
        [
            step("calc.py", "Menyu va kiritish", r'''
print("1) Qo'shish  2) Ayirish  3) Ko'paytirish  4) Bo'lish")
tanlov = input("Amal: ")
a = float(input("a = "))
b = float(input("b = "))''',
                 [("menyu", "foydalanuvchi raqam tanlaydi."),
                  ("tanlov", "matn bo'lib qoladi — \"1\", \"2\" bilan solishtiramiz.")],
                 "1) Qo'shish  2) Ayirish  3) Ko'paytirish  4) Bo'lish\nAmal: 4\na = 10\nb = 0"),
            step("calc.py", "match-case bilan tanlaymiz", r'''
match tanlov:
    case "1":
        print("Natija:", a + b)
    case "2":
        print("Natija:", a - b)
    case "3":
        print("Natija:", a * b)''',
                 [("match tanlov:", "qaysi qiymat bilan solishtiramiz."),
                  ("case \"1\":", "tanlov \"1\" bo'lsa shu blok bajariladi."),
                  ("if-elif o'rnida", "variantlar ko'p bo'lsa match o'qishga oson.")],
                 "Amal: 1, a = 10, b = 5 → Natija: 15.0"),
            step("calc.py", "Ichma-ich shart va case _", r'''
    case "4":
        if b == 0:
            print("Nolga bo'lib bo'lmaydi!")
        else:
            print("Natija:", a / b)
    case _:
        print("Bunday amal yo'q")''',
                 [("ichma-ich if", "case ichida yana savol: b nolmi?"),
                  ("case _:", "hech bir variant mos kelmasa (else kabi)."),
                  ("chekinish", "har bosqichda 4 probel ko'payadi.")],
                 "Nolga bo'lib bo'lmaydi!"),
        ],
        {"calc.py": CALC2},
        [("python/", ""), ("├── grade.py", ""), ("└── calc.py", "o‘zgardi")],
        ["match-case", "case _ — qolgan hammasi", "Ichma-ich shart", "Nolga bo'lish tekshiruvi"],
        ["Majburiy: menyuga 5) Daraja amalini qo'shing.",
         "Qo'shimcha: hafta kuni raqamidan (1–7) nomini match bilan chiqaring."],
        "3.9 · while sikli va random: “Sonni top” o'yini.",
        run={"file": "calc.py", "input": "4\n10\n0\n", "expect": ["Nolga bo'lib bo'lmaydi!"]},
    ),
    "DP09": lesson(
        M, 9, "while sikli va random: “Sonni top” o'yini",
        "Kompyuter son o'ylaydi, biz topgunimizcha so'raydi — birinchi o'yinimiz.",
        "O'tgan darsda: match-case, menyuli kalkulyator.",
        "case _ nimani bildiradi?",
        "while shart: — shart rost ekan takrorlaydi; import random, randint(a, b); cheksiz sikldan qochish.",
        "O'yinga “taxmin 10 dan ko'p farq qiladi” maslahatini qo'shing.",
        [("🎲", "randint", "1–100", ""),
         ("⌨", "Taxmin", "input()", "loop"),
         ("⚖", "Solishtirish", "katta / kichik", "loop"),
         ("🔁", "while", "topmaguncha", "mem"),
         ("🎉", "G'alaba", "Topdingiz!", "")],
        [
            step("guess.py", "Tasodifiy son", r'''
import random

son = random.randint(1, 100)
taxmin = 0''',
                 [("import random", "tayyor modulni ulaymiz."),
                  ("randint(1, 100)", "1 dan 100 gacha (ikkalasi ham kiradi) tasodifiy son."),
                  ("taxmin = 0", "sikl boshlanishi uchun son bilan teng bo'lmagan qiymat.")],
                 "son = 42 (har safar boshqa)"),
            step("guess.py", "while sikli", r'''
while taxmin != son:
    taxmin = int(input("1–100 orasida son: "))
    if taxmin < son:
        print("Kattaroq son ayting ⬆")
    elif taxmin > son:
        print("Kichikroq son ayting ⬇")''',
                 [("while shart:", "har aylanishdan oldin shart tekshiriladi."),
                  ("taxmin o'zgaradi", "sikl ichida — aks holda sikl hech qachon tugamaydi."),
                  ("maslahat", "katta/kichik — o'yinchi sonni tez topadi.")],
                 "1–100 orasida son: 50\nKichikroq son ayting ⬇\n1–100 orasida son: 30\nKattaroq son ayting ⬆"),
            step("guess.py", "G'alaba xabari", r'''
print("🎉 Topdingiz! Son:", son)''',
                 [("sikldan keyin", "shart yolg'on bo'ldi — demak taxmin == son."),
                  ("strategiya", "har safar yarmini tashlasangiz, 7 urinishda albatta topasiz.")],
                 "1–100 orasida son: 42\n🎉 Topdingiz! Son: 42"),
        ],
        {"guess.py": GUESS1},
        [("python/", ""), ("├── calc.py", ""), ("└── guess.py", "yangi")],
        ["while sikli", "import random va randint", "Sikl ichida o'zgaruvchini yangilash", "Cheksiz sikldan qochish"],
        ["Majburiy: “juda yaqin” (farq ≤ 5) maslahatini qo'shing.",
         "Qo'shimcha: 10 dan 1 gacha teskari sanaydigan while yozing."],
        "3.10 · for sikli va range().",
        run={"file": "guess.py", "input": "50\n30\n42\n", "randint": 42, "expect": ["Kichikroq son ayting ⬇", "Kattaroq son ayting ⬆", "🎉 Topdingiz! Son: 42"]},
    ),
    "DP10": lesson(
        M, 10, "for sikli va range()",
        "Necha marta takrorlash aniq bo'lsa — for: ko'paytirish jadvali va yig'indi.",
        "O'tgan darsda: while sikli, “Sonni top” o'yini.",
        "while sikli qachon to'xtaydi?",
        "for i in range(...), range(boshi, oxiri, qadam) — oxiri kirmaydi; yig'uvchi o'zgaruvchi.",
        "1 dan N gacha juft sonlar yig'indisini chiqaring.",
        [("⌨", "n", "7", ""),
         ("🔁", "for i", "range(1, 11)", "mem"),
         ("✖", "n × i", "har aylanishda", "loop"),
         ("➕", "jami +=", "yig'uvchi", ""),
         ("🖥", "Natija", "jadval va 5050", "")],
        [
            step("table.py", "Ko'paytirish jadvali", r'''
n = int(input("Qaysi son uchun jadval? "))

for i in range(1, 11):
    print(f"{n} × {i} = {n * i}")''',
                 [("range(1, 11)", "1, 2, … 10 — <b>oxiri kirmaydi</b>."),
                  ("i", "har aylanishda navbatdagi son i ga tushadi."),
                  ("for", "takrorlashlar soni oldindan ma'lum bo'lsa.")],
                 "7 × 1 = 7\n7 × 2 = 14\n...\n7 × 10 = 70"),
            step("table.py", "Yig'uvchi o'zgaruvchi", r'''
jami = 0
for i in range(1, 101):
    jami += i
print("1 dan 100 gacha yig'indi:", jami)''',
                 [("jami = 0", "sikldan <b>oldin</b> boshlang'ich qiymat."),
                  ("jami += i", "jami = jami + i ning qisqa yozuvi."),
                  ("print sikldan keyin", "chekinishsiz — faqat bir marta chiqadi.")],
                 "1 dan 100 gacha yig'indi: 5050"),
            step("table.py", "Qadam bilan range", r'''
for i in range(10, 0, -2):
    print(i, end=" ")
print()''',
                 [("range(10, 0, -2)", "10 dan boshlab 2 tadan kamayadi, 0 kirmaydi."),
                  ("end=\" \"", "bir qatorga yozish uchun."),
                  ("print()", "oxirida yangi qatorga o'tish.")],
                 "10 8 6 4 2"),
        ],
        {"table.py": TABLE},
        [("python/", ""), ("├── guess.py", ""), ("└── table.py", "yangi")],
        ["for va range()", "range(boshi, oxiri, qadam)", "Yig'uvchi o'zgaruvchi", "for va while farqi"],
        ["Majburiy: 1 dan N gacha juft sonlar yig'indisi.",
         "Qo'shimcha: 1 dan 10 gacha sonlar kvadratlari jadvali."],
        "3.11 · break, continue va sikl amaliyoti.",
        run={"file": "table.py", "input": "7\n", "expect": ["7 × 10 = 70", "1 dan 100 gacha yig'indi: 5050", "10 8 6 4 2"]},
    ),
    "DP11": lesson(
        M, 11, "break, continue va sikl amaliyoti",
        "“Sonni top” o'yinini yaxshilaymiz: urinishlar soni, noto'g'ri kiritish va qayta o'ynash.",
        "O'tgan darsda: for, range() va yig'uvchi o'zgaruvchi.",
        "range(1, 11) qaysi sonlarni beradi?",
        "while True + break — menyu va o'yinlar shakli; continue — keyingi aylanishga o'tish; ichma-ich sikl.",
        "Eng yaxshi natijani (eng kam urinish) eslab qoling.",
        [("🔁", "Tashqi sikl", "yangi o'yin", "loop"),
         ("⌨", "Ichki sikl", "taxminlar", "loop"),
         ("⏭", "continue", "harf kiritilsa", ""),
         ("⛔", "break", "topdi yoki 7 urinish", "mem"),
         ("❓", "Yana?", "ha / yo'q", "")],
        [
            step("guess.py", "while True va noto'g'ri kiritish", r'''
import random

while True:
    son = random.randint(1, 100)
    urinish = 0
    while True:
        javob = input("Son: ")
        if not javob.isdigit():
            print("Faqat raqam kiriting!")
            continue''',
                 [("while True:", "o'zi to'xtamaydi — ichidan break bilan chiqamiz."),
                  (".isdigit()", "satr faqat raqamdan iboratmi?"),
                  ("continue", "qolgan qatorlarni o'tkazib, keyingi aylanishga o'tadi.")],
                 "Son: o'n\nFaqat raqam kiriting!"),
            step("guess.py", "Urinishlarni sanaymiz va break", r'''
        urinish += 1
        taxmin = int(javob)
        if taxmin == son:
            print(f"🎉 Topdingiz! {urinish} ta urinishda")
            break
        print("Kattaroq ⬆" if taxmin < son else "Kichikroq ⬇")
        if urinish == 7:
            print("Urinishlar tugadi. Son:", son)
            break''',
                 [("break", "faqat <b>ichki</b> sikldan chiqadi."),
                  ("A if shart else B", "qisqa shart — bitta qatorda."),
                  ("7 urinish", "o'yinga chegara qo'yamiz.")],
                 "Son: 50\nKichikroq ⬇\nSon: 42\n🎉 Topdingiz! 2 ta urinishda"),
            step("guess.py", "Qayta o'ynash", r'''
    if input("Yana o'ynaysizmi? (ha/yo'q): ") != "ha":
        break

print("Xayr! 👋")''',
                 [("tashqi break", "bu chekinishda — tashqi sikldan chiqadi."),
                  ("input to'g'ridan-to'g'ri", "javobni o'zgaruvchisiz solishtirish mumkin.")],
                 "Yana o'ynaysizmi? (ha/yo'q): yo'q\nXayr! 👋"),
        ],
        {"guess.py": GUESS2},
        [("python/", ""), ("├── table.py", ""), ("└── guess.py", "o‘zgardi")],
        ["while True + break", "continue", "Ichma-ich sikl", "Qisqa shart (A if ... else B)"],
        ["Majburiy: eng kam urinishli natijani eslab qoling va har o'yin oxirida ko'rsating.",
         "Qo'shimcha: qiyinlik darajasi — 1–10, 1–100 yoki 1–1000."],
        "3.12 · 3-oy loyihasi: “Bank terminali”.",
        run={"file": "guess.py", "input": "o'n\n50\n42\nyo'q\n", "randint": 42, "expect": ["Faqat raqam kiriting!", "Kichikroq ⬇", "🎉 Topdingiz! 2 ta urinishda", "Xayr! 👋"]},
    ),
    "DP12": lesson(
        M, 12, "3-oy loyihasi: “Bank terminali” va nazorat",
        "Oy davomida o'rganganlarni bitta dasturga yig'amiz: menyu, shartlar, sikl va hisob.",
        "3-oyda: print, o'zgaruvchilar, input, amallar, satrlar, shartlar, while va for.",
        "while True + break qanday ishlaydi? Bir oyni 5 savol bilan takrorlaymiz.",
        "Loyiha tuzilmasi: holat (balans, tarix) → menyu sikli → har tanlov uchun blok.",
        "Terminalga PIN-kod bilan kirishni qo'shing (3 urinish).",
        [("💰", "Holat", "balans, tarix", "mem"),
         ("📋", "Menyu", "while True", "loop"),
         ("➕", "Kirim", "balans += summa", ""),
         ("➖", "Chiqim", "yetarlimi?", ""),
         ("📜", "Tarix", "satrda", ""),
         ("👋", "Chiqish", "break", "")],
        [
            step("bank.py", "Holat va menyu", r'''
balans = 0
tarix = ""

while True:
    print("\n1) Balans  2) Kirim  3) Chiqim  4) Tarix  0) Chiqish")
    tanlov = input("Tanlang: ")
    if tanlov == "1":
        print(f"💰 Balans: {balans:,} so'm")''',
                 [("balans, tarix", "dastur “eslab” turadigan ma'lumot — sikldan oldin."),
                  ("\\n", "satr ichida yangi qator."),
                  ("{balans:,}", "minglik ajratgich: 150000 → 150,000.")],
                 "1) Balans  2) Kirim  3) Chiqim  4) Tarix  0) Chiqish\nTanlang: 1\n💰 Balans: 0 so'm"),
            step("bank.py", "Kirim va chiqim", r'''
    elif tanlov == "2":
        summa = int(input("Kirim summasi: "))
        balans += summa
        tarix += f"+{summa:,}\n"
        print("✅ Qabul qilindi")
    elif tanlov == "3":
        summa = int(input("Chiqim summasi: "))
        if summa > balans:
            print("❌ Mablag' yetarli emas")
        else:
            balans -= summa
            tarix += f"-{summa:,}\n"
            print("✅ Yechildi")''',
                 [("balans += summa", "holatni yangilaymiz."),
                  ("tarix +=", "satrga yangi qator qo'shib boramiz."),
                  ("ichma-ich if", "pul yetmasa chiqim bajarilmaydi.")],
                 "Tanlang: 2\nKirim summasi: 150000\n✅ Qabul qilindi\nTanlang: 3\nChiqim summasi: 200000\n❌ Mablag' yetarli emas"),
            step("bank.py", "Tarix va chiqish", r'''
    elif tanlov == "4":
        print(tarix or "Hali amal yo'q")
    elif tanlov == "0":
        print("Xayr! 👋")
        break
    else:
        print("Noto'g'ri tanlov")''',
                 [("tarix or \"...\"", "tarix bo'sh bo'lsa — ikkinchi qiymat chiqadi."),
                  ("break", "0 tanlansa sikl va dastur tugaydi."),
                  ("else", "menyuda yo'q raqam uchun.")],
                 "Tanlang: 4\n+150,000\n-50,000\nTanlang: 0\nXayr! 👋"),
        ],
        {"bank.py": BANK},
        [("python/", ""), ("├── guess.py", ""), ("└── bank.py", "yangi")],
        ["Dastur holati (o'zgaruvchilar)", "Menyu sikli", "Shartlar zanjiri", "Formatlash: {x:,}"],
        ["Majburiy: PIN-kod bilan kirish (3 ta urinish, keyin bloklanadi).",
         "Qo'shimcha: kirim va chiqimlar sonini sanab, chiqishda ko'rsating."],
        "4.1 · List: yaratish, indeks va kesish.",
        run={"file": "bank.py", "input": "2\n150000\n3\n200000\n3\n50000\n1\n4\n0\n", "expect": ["❌ Mablag' yetarli emas", "💰 Balans: 100,000 so'm", "+150,000", "-50,000", "Xayr! 👋"]},
    ),
}
