"""Python kursi: dars rasmlari (mavzu kaliti bo'yicha). Shakl — ``poster_kit``; manba — ``study_python``.

``code`` ko'rgazmasidagi "Natija" — kodni ishga tushirib tekshiriladi (``tests/test_posters.py``).
"""

from .poster_kit import card, code, poster

POSTERS = {
    "PY01": poster(
        "Python o'rnatamiz, VS Code'da <b>birinchi dasturni</b> yozamiz va ekranga chiqaramiz.",
        code('''
# Birinchi dasturim
print("Salom, dunyo!")
print("Mening ismim", "Ali")
print(2026, 10, 7, sep=".")
print("Bir", end=" ")
print("qatorda")
print("Ha" * 3)
print(15 + 27)
''', '''
Salom, dunyo!
Mening ismim Ali
2026.10.7
Bir qatorda
HaHaHa
42
'''),
        [
            card("Ishga tushirish", code="python --version\npython salom.py", text="Windows'da o'rnatishda <b>Add Python to PATH</b> belgisini qo'ying."),
            card("sep va end", text="<code>sep</code> — qiymatlar orasidagi belgi (probel), <code>end</code> — oxiridagi belgi (yangi qator)."),
            card("Izoh va REPL", text="<code>#</code> — izoh, Python o'qimaydi. Terminalda <code>python</code> → <code>&gt;&gt;&gt;</code> — buyruq darhol bajariladi."),
        ],
        ("Kod qatorma-qator, yuqoridan pastga bajariladi", "Fayl kengaytmasi — .py"),
        [
            ("print(\"A\", \"B\", sep=\"-\") nima chiqaradi?", "A-B"),
            ("Python faylining kengaytmasi qanday?", ".py"),
            ("print(\"Ha\" * 3) natijasi?", "HaHaHa"),
        ],
        title="Kod va uning natijasi",
        badge=("py", "dastur"),
    ),
    "PY02": poster(
        "O'zgaruvchi — qiymat saqlaydigan <b>nomli quti</b>. Python'ning 4 ta asosiy turini o'rganamiz.",
        ("tiles", [
            ("14", "int", "Butun son: yosh = 14"),
            ("3.14", "float", "Kasr son: narx = 3.14"),
            ('"salom"', "str", "Matn — qo'shtirnoq ichida."),
            ("True", "bool", "Rost yoki yolg'on: True / False"),
        ]),
        [
            card("= — qiymat ber", code="yosh = 14\nyosh = yosh + 1  # 15", text="<code>=</code> “teng” emas, <b>o'ng tomondagini chapga yoz</b> degani."),
            card("Nomlash qoidalari", text="Harf yoki <code>_</code> bilan boshlanadi, probel va <code>-</code> yo'q, kalit so'z emas. Uslub: <code>snake_case</code>."),
            card("type() va konstanta", text="<code>type(3.14)</code> → <code>float</code>. O'zgarmas qiymat KATTA harflarda: <code>PI = 3.14159</code>."),
        ],
        ("Nom — ma'noli: x emas, yosh", "2ism, mening-ismim, class — noto'g'ri nomlar."),
        [
            ("type(\"14\") qaysi turni qaytaradi?", "str — qo'shtirnoq ichida bo'lgani uchun."),
            ("Qaysi nom to'g'ri: 2ism, ism_2, ism-2?", "ism_2"),
            ("a = 5; a = a + 3. a nechaga teng?", "8"),
        ],
        title="4 ta asosiy tur",
        badge=("4", "tur"),
    ),
    "PY03": poster(
        "<code>input()</code> doim <b>matn</b> qaytaradi — hisoblash uchun uni songa aylantiramiz.",
        code('''
yosh = "14"          # input() shunday beradi
print(yosh + "1")
print(int(yosh) + 1)
print(int(3.9))
print(int(float("3.5")))
print(round(3.567, 2))
print(bool(""), bool("0"))
print(str(10) + " ball")
''', '''
141
15
3
3
3.57
False True
10 ball
'''),
        [
            card("Aylantirish", text="<code>int(\"12\")</code> → 12, <code>float(\"2.5\")</code> → 2.5, <code>str(10)</code> → \"10\"."),
            card("Kasr tashlanadi", formula="int(3.9) = [3]", text="<code>int()</code> yaxlitlamaydi — kasr qismini <b>tashlaydi</b>. Yaxlitlash — <code>round()</code>."),
            card("ValueError", code='int("3.5")   # ValueError\nint(float("3.5"))  # 3', text="Avval float, keyin int."),
        ],
        ("input() → str. Hisob uchun: int(input(...))", "Aks holda \"14\" + \"1\" = \"141\" bo'ladi."),
        [
            ("input() qaysi turni qaytaradi?", "str (matn)."),
            ("int(7.8) natijasi?", "7"),
            ("\"5\" + \"5\" va int(\"5\") + 5 natijalari?", "\"55\" va 10."),
        ],
        title="Matn va son farqi",
        badge=("str", "→ int"),
    ),
    "PY04": poster(
        "Matnni <b>indeks va kesish</b> bilan bo'laklaymiz, metodlar va f-string bilan bezaymiz.",
        code('''
s = "Python"
print(s[0], s[-1])
print(s[1:4])
print(s[::-1])
print(len(s))
print(s.upper())
print("  salom  ".strip())
print("a,b,c".split(","))
ism, yosh = "Ali", 14
print(f"{ism} {yosh} yoshda")
''', '''
P n
yth
nohtyP
6
PYTHON
salom
['a', 'b', 'c']
Ali 14 yoshda
'''),
        [
            card("Indeks", formula="P y t h o n → 0 1 2 3 4 5", text="Teskari indeks: <code>s[-1]</code> — oxirgi belgi."),
            card("Slicing", text="<code>s[boshi:oxiri:qadam]</code> — <b>oxiri kirmaydi</b>. <code>s[::-1]</code> — teskari."),
            card("O'zgarmas", text="<code>s[0] = \"z\"</code> → TypeError. Metodlar <b>yangi</b> satr qaytaradi."),
        ],
        ("Indeks 0 dan boshlanadi, kesishda oxiri kirmaydi", "s[1:4] — 1, 2, 3-belgilar."),
        [
            ("\"Python\"[2] nima qaytaradi?", "'t'"),
            ("\"salom\"[::-1] natijasi?", "'molas'"),
            ("ism = \"Vali\" bo'lsa, f\"Salom, {ism}!\" nima chiqaradi?", "Salom, Vali!"),
        ],
        title="Satr bilan ishlash",
        badge=("f\"\"", "string"),
    ),
    "PY05": poster(
        "Python — kuchli kalkulyator: <b>7 ta arifmetik amal</b> va ularning bajarilish tartibi.",
        ("tiles", [
            ("10 / 4", "Bo'lish → 2.5", "Natija doim float: 10 / 5 → 2.0"),
            ("7 // 2", "Butun bo'lish → 3", "Pastga yaxlitlaydi."),
            ("7 % 2", "Qoldiq → 1", "Juft-toqni aniqlash: x % 2 == 0"),
            ("2 ** 3", "Daraja → 8", "2 · 2 · 2"),
            ("2+3*4", "Tartib → 14", "Avval **, keyin * / // %, keyin + −"),
            ("x += 5", "Qisqa yozuv", "x = x + 5; shuningdek −=, *="),
        ]),
        [
            card("Soat:daqiqa", formula="3725 // 3600 = [1] soat", example="(3725 % 3600) // 60 = <b>2</b> daqiqa, 3725 % 60 = <b>5</b> soniya"),
            card("Raqamlar", formula="472 % 10 = [2]", text="Oxirgi raqam — <code>% 10</code>, qolgani — <code>// 10</code> → 47."),
            card("Qavslar", formula="(2 + 3) * 4 = [20]", text="Shubha bo'lsa — qavs qo'ying."),
        ],
        ("Juftmi? — x % 2 == 0", "Qoldiq 0 bo'lsa juft, 1 bo'lsa toq."),
        [
            ("17 // 5 va 17 % 5 natijalari?", "3 va 2."),
            ("2 + 3 * 2 ** 2 nechaga teng?", "14"),
            ("9 / 3 natijasi qanday turda chiqadi?", "float — 3.0"),
        ],
        title="Arifmetik amallar",
        badge=("%", "qoldiq"),
    ),
    "PY06": poster(
        "Savolga <b>True yoki False</b> javob beramiz: taqqoslash va mantiqiy amallar.",
        code('''
yosh = 14
print(yosh == 14, yosh != 14)
print(yosh >= 13 and yosh <= 17)
print(13 <= yosh <= 17)
print(yosh < 10 or yosh > 12)
print(not yosh > 18)
print("a" < "b", "A" == "a")
print(True or False and False)
''', '''
True False
True
True
True
True
True False
True
'''),
        [
            card("= va ==", text="<code>=</code> — qiymat <b>beradi</b>, <code>==</code> — tenglikni <b>tekshiradi</b>."),
            card("and / or / not", text="<b>and</b> — ikkalasi rost bo'lsa, <b>or</b> — bittasi yetarli, <b>not</b> — teskarisi."),
            card("Tartib", formula="not → and → [or]", text="Zanjir: <code>13 &lt;= yosh &lt;= 17</code>."),
        ],
        ("Shubha bo'lsa — qavs qo'ying", "(a or b) and c ≠ a or (b and c)"),
        [
            ("5 != 5 natijasi?", "False"),
            ("True and False or True nechaga teng?", "True"),
            ("x = 20 da 13 <= x <= 17 natijasi?", "False"),
        ],
        title="Taqqoslash va mantiq",
        badge=("==", "tekshir"),
    ),
    "PY07": poster(
        "Dastur <b>qaror qabul qiladi</b>: shartga qarab faqat bitta yo'l bajariladi.",
        code('''
ball = 78
if ball >= 86:
    baho = 5
elif ball >= 71:
    baho = 4
elif ball >= 56:
    baho = 3
else:
    baho = 2
print("Baho:", baho)
x = 7
print("juft" if x % 2 == 0 else "toq")
''', '''
Baho: 4
toq
'''),
        [
            card("Sintaksis", text="<code>if shart:</code> — oxirida <b>ikki nuqta</b>, tanasi <b>4 probel</b> chekinish bilan."),
            card("Faqat bittasi", text="Zanjirda <b>birinchi rost</b> shart bajariladi, qolganlari tekshirilmaydi."),
            card("Bo'sh qiymat", text="<code>0</code>, <code>\"\"</code>, <code>[]</code>, <code>None</code> shartda <b>False</b> hisoblanadi."),
        ],
        ("Tartib muhim: kattadan kichikka tekshiring", "ball >= 56 birinchi tursa, 95 ham “3” oladi."),
        [
            ("ball = 90 bo'lsa, yuqoridagi kod qaysi bahoni beradi?", "5"),
            ("else'dan keyin shart yoziladimi?", "Yo'q — else: shartsiz."),
            ("if \"\": print(\"Ha\") — nima chiqadi?", "Hech narsa: bo'sh satr False."),
        ],
        title="if / elif / else",
        badge=("if", "shart"),
    ),
    "PY08": poster(
        "Murakkab tekshiruvlar: <b>ichma-ich shart, match-case</b> va RegEx andozalari.",
        code('''
import re
buyruq = "2"
match buyruq:
    case "1":
        print("Yangi o'yin")
    case "2":
        print("Natijalar")
    case _:
        print("Noma'lum")
tel = "+998901234567"
ok = re.fullmatch(r"\\+998\\d{9}", tel)
print(bool(ok))
''', '''
Natijalar
True
'''),
        [
            card("Soddalashtirish", code="if yosh >= 13:\n    if yosh <= 17: ...\n# ↓\nif 13 <= yosh <= 17: ...", text=""),
            card("RegEx belgilari", text="<code>\\d</code> raqam, <code>[A-Z]</code> katta harf, <code>{9}</code> aynan 9 marta, <code>+</code> bir yoki ko'p."),
            card("fullmatch / search", text="<code>fullmatch</code> — butun matn mos, <code>search</code> — matn ichida biror joyda. Mos kelmasa — <code>None</code>."),
        ],
        ("Andozani r\"...\" bilan yozing", "case _: — “boshqa hamma holat”."),
        [
            ("match'da case _ nimani bildiradi?", "Boshqa hamma holat (default)."),
            ("\\d{4} andozasi nimaga mos keladi?", "Aynan 4 ta raqamga."),
            ("re.fullmatch mos kelmasa nima qaytaradi?", "None"),
        ],
        title="match-case va RegEx",
        badge=("re", "andoza"),
    ),
    "PY09": poster(
        "List — <b>tartiblangan ro'yxat</b>: bir o'zgaruvchida ko'p qiymat, indeks bilan murojaat.",
        code('''
a = [10, 20, 30, 40, 50]
print(a[0], a[-1])
print(a[1:3])
print(a[::2])
a[0] = 100
print(a)
print(len(a), 30 in a)
print([1, 2] + [3])
print([0] * 3)
''', '''
10 50
[20, 30]
[10, 30, 50]
[100, 20, 30, 40, 50]
5 True
[1, 2, 3]
[0, 0, 0]
'''),
        [
            card("Indeks", formula="[10, 20, 30] → 0, 1, [2]", text="Mavjud bo'lmagan indeks — <b>IndexError</b>."),
            card("Slicing", text="<code>a[1:3]</code>, <code>a[:2]</code>, <code>a[::-1]</code> — <b>yangi</b> ro'yxat qaytaradi."),
            card("O'rtacha", formula="sum(a) ÷ len(a) = [o'rtacha]", example="[80, 90, 70] → 240 ÷ 3 = <b>80</b>"),
        ],
        ("List o'zgaruvchan: a[0] = 100 ishlaydi", "Satrdan farqi shu — satrni o'zgartirib bo'lmaydi."),
        [
            ("a = [5, 6, 7]. a[-1] nechaga teng?", "7"),
            ("a = [5, 6, 7]. a[3] nima beradi?", "IndexError"),
            ("[1, 2, 3, 4][1:3] natijasi?", "[2, 3]"),
        ],
        title="List: indeks va kesish",
        badge=("[ ]", "list"),
    ),
    "PY10": poster(
        "Ro'yxatga <b>qo'shamiz, o'chiramiz, saralaymiz</b> va comprehension bilan bir qatorda yasaymiz.",
        code('''
a = [3, 1, 2]
a.append(5)
a.insert(0, 9)
print(a)
a.remove(1)
x = a.pop()
print(a, x)
print(sorted(a), a)
a.sort()
print(a)
print([n * n for n in range(5) if n % 2 == 0])
''', '''
[9, 3, 1, 2, 5]
[9, 3, 2] 5
[2, 3, 9] [9, 3, 2]
[2, 3, 9]
[0, 4, 16]
'''),
        [
            card("Qo'shish va o'chirish", text="<code>append</code> — oxiriga, <code>insert(i, x)</code> — o'ringa; <code>remove(x)</code> — qiymat bo'yicha, <code>pop()</code> — oxirgisini qaytaradi."),
            card("sort va sorted", text="<code>a.sort()</code> — <b>o'zini</b> saralaydi (None qaytaradi), <code>sorted(a)</code> — <b>yangi</b> ro'yxat."),
            card("Comprehension", formula="[ifoda for x in a if shart]", text="Sikl + shart bitta qatorda."),
        ],
        ("b = a — nusxa emas!", "Bitta ro'yxatga ikkinchi nom. Nusxa: b = a.copy()"),
        [
            ("a = [1, 2]; a.append(3). a nima bo'ladi?", "[1, 2, 3]"),
            ("print(a.sort()) nima chiqaradi?", "None"),
            ("[x * 2 for x in [1, 2, 3]] natijasi?", "[2, 4, 6]"),
        ],
        title="List metodlari",
        badge=(".append", "metod"),
    ),
    "PY11": poster(
        "<b>Tuple</b> — o'zgarmas ro'yxat, <b>set</b> — takrorlanmas to'plam. Qachon qaysi biri kerak?",
        code('''
nuqta = (3, 4)
x, y = nuqta
print(x, y)
bitta = (5,)
print(type(bitta).__name__)
s = set([1, 2, 2, 3, 3])
print(s)
a, b = {1, 2, 3}, {2, 3, 4}
print(a & b, a | b)
print(a - b, a ^ b)
''', '''
3 4
tuple
{1, 2, 3}
{2, 3} {1, 2, 3, 4}
{1} {1, 4}
'''),
        [
            card("Tuple", text="<code>(1, 2, 3)</code> — o'zgartirib bo'lmaydi (TypeError). Bitta element: <code>(5,)</code> — <b>vergul shart</b>."),
            card("Set", text="<code>{1, 2}</code> — takror yo'q, tartib yo'q, indeks yo'q. Bo'sh set — <code>set()</code>, <code>{}</code> — bu lug'at!"),
            card("To'plam amallari", text="<code>&amp;</code> kesishma, <code>|</code> birlashma, <code>-</code> ayirma, <code>^</code> simmetrik ayirma."),
        ],
        ("Takrorlarni olib tashlash — set()", "list(set(a)) — har bir qiymat bir marta qoladi."),
        [
            ("type((5)) va type((5,)) qanday?", "int va tuple."),
            ("set([1, 1, 2]) natijasi?", "{1, 2}"),
            ("{1, 2} & {2, 3} natijasi?", "{2}"),
        ],
        title="Tuple va Set",
        badge=("( )", "{ }"),
    ),
    "PY12": poster(
        "Lug'at — <b>kalit → qiymat</b> juftliklari: ma'lumotni nom bilan saqlaymiz va topamiz.",
        code('''
d = {"ism": "Ali", "yosh": 14}
print(d["ism"])
print(d.get("shahar", "—"))
d["shahar"] = "Toshkent"
d["yosh"] = 15
print(d.pop("yosh"))
print(list(d.keys()))
print("ism" in d)
for k, v in d.items():
    print(k, "=", v)
''', '''
Ali
—
15
['ism', 'shahar']
True
ism = Ali
shahar = Toshkent
'''),
        [
            card("Yo'q kalit", text="<code>d[\"x\"]</code> → <b>KeyError</b>. Xavfsiz: <code>d.get(\"x\", 0)</code> → 0."),
            card("keys / values / items", text="Kalitlar, qiymatlar va juftliklar. <code>in</code> — faqat <b>kalitni</b> tekshiradi."),
            card("Sanash", code='son = {}\nfor h in "olma":\n    son[h] = son.get(h, 0) + 1', text=""),
        ],
        ("Kalit — o'zgarmas tur: str, int, tuple", "List kalit bo'la olmaydi."),
        [
            ("d = {\"a\": 1}. d[\"b\"] nima beradi?", "KeyError"),
            ("d.get(\"b\", 0) natijasi?", "0"),
            ("\"Ali\" in {\"ism\": \"Ali\"} natijasi?", "False — in kalitni tekshiradi."),
        ],
        title="Dictionary bilan ishlash",
        badge=("{ : }", "dict"),
    ),
    "PY13": poster(
        "Haqiqiy ma'lumot ichma-ich: <b>lug'atlar ro'yxati</b> va ro'yxatli lug'atlar bilan ishlaymiz.",
        code('''
oquvchilar = [
    {"ism": "Ali", "ball": 85},
    {"ism": "Laylo", "ball": 97},
    {"ism": "Vali", "ball": 72},
]
top = sorted(oquvchilar,
             key=lambda o: o["ball"],
             reverse=True)
print(top[0]["ism"])
m = [[1, 2, 3], [4, 5, 6]]
print(m[1][2])
''', '''
Laylo
6
'''),
        [
            card("Qadam-baqadam", formula="data[\"guruh\"][\"oquvchilar\"][0]", text="Har qavs bir qavat ichkariga kiradi."),
            card("Matritsa", formula="m[qator][ustun]", text="<code>m[1][2]</code> — 2-qator, 3-ustun."),
            card("Saralash", text="<code>sorted(a, key=lambda x: x[\"ball\"], reverse=True)</code> — ball bo'yicha kamayish tartibida."),
        ],
        ("Murojaatni ichkaridan emas, tashqaridan boshlang", "Har qadamda print() bilan tekshiring."),
        [
            ("m = [[1, 2], [3, 4]]. m[1][0] nechaga teng?", "3"),
            ("Yuqoridagi koddan Vali'ning balli qanday olinadi?", "oquvchilar[2][\"ball\"]"),
            ("reverse=True nima qiladi?", "Kamayish tartibida saralaydi."),
        ],
        title="Ichma-ich ma'lumot",
        badge=("[{ }]", "JSON"),
    ),
    "PY14": poster(
        "Bir ishni ko'p marta: <b>for sikli</b> ro'yxat va <code>range()</code> ustida aylanadi.",
        code('''
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(0, 10, 3)))
print(list(range(5, 0, -1)))
jami = 0
for n in range(1, 6):
    jami += n
print("Yig'indi:", jami)
for i, f in enumerate(["olma", "nok"], start=1):
    print(i, f)
''', '''
[0, 1, 2, 3, 4]
[2, 3, 4, 5]
[0, 3, 6, 9]
[5, 4, 3, 2, 1]
Yig'indi: 15
1 olma
2 nok
'''),
        [
            card("range", formula="range(boshi, oxiri, qadam)", text="<b>Oxiri kirmaydi</b>: <code>range(5)</code> → 0…4."),
            card("Yig'uvchi", text="Natija o'zgaruvchisi sikldan <b>oldin</b> 0 (yig'indi) yoki 1 (ko'paytma) bilan boshlanadi."),
            card("enumerate", text="Indeks va element birga: <code>for i, x in enumerate(a, start=1)</code>."),
        ],
        ("range(1, 11) — 1 dan 10 gacha", "Oxiri kirmasligini unutmang."),
        [
            ("range(3) qaysi sonlarni beradi?", "0, 1, 2"),
            ("range(10, 0, -2) ning birinchi va oxirgi sonlari?", "10 va 2."),
            ("1 dan 4 gacha sonlar ko'paytmasi uchun boshlang'ich qiymat?", "1 (natija 24)."),
        ],
        title="for va range()",
        badge=("for", "sikl"),
    ),
    "PY15": poster(
        "<b>while</b> — shart rost ekan takrorlaydi. break, continue va pass bilan boshqaramiz.",
        code('''
n = 1
while n <= 5:
    if n == 2:
        n += 1
        continue
    if n == 5:
        break
    print(n)
    n += 1
son, jami = 472, 0
while son > 0:
    jami += son % 10
    son //= 10
print(jami)
''', '''
1
3
4
13
'''),
        [
            card("Cheksiz sikl", text="Shartdagi o'zgaruvchi sikl <b>ichida o'zgarishi</b> kerak, aks holda sikl to'xtamaydi."),
            card("break / continue / pass", text="<b>break</b> — chiqish, <b>continue</b> — keyingi aylanishga o'tish, <b>pass</b> — hech narsa qilmaslik."),
            card("Menyu shakli", code='while True:\n    t = input("> ")\n    if t == "0":\n        break', text=""),
        ],
        ("Har aylanishda shartga yaqinlashing", "n += 1 ni unutsangiz — cheksiz sikl."),
        [
            ("continue va break ning farqi?", "continue — keyingi aylanishga, break — sikldan butunlay chiqadi."),
            ("Yuqoridagi kodda 472 raqamlari yig'indisi nechaga teng?", "13"),
            ("Bo'sh if blokiga nima yoziladi?", "pass"),
        ],
        title="while, break, continue",
        badge=("∞", "while"),
    ),
    "PY16": poster(
        "Sikl bilan ma'lumotni qayta ishlaymiz: <b>eng kattasini topish, sanash, filtrlash</b>.",
        code('''
a = [4, 9, 2, 7]
eng = a[0]
for x in a:
    if x > eng:
        eng = x
print(eng)
son = {}
for h in "kitob":
    son[h] = son.get(h, 0) + 1
print(son["k"], len(son))
ism = ["Ali", "Vali"]
ball = [90, 75]
for i, b in zip(ism, ball):
    print(i, b)
''', '''
9
1 5
Ali 90
Vali 75
'''),
        [
            card("Filtrlash", formula="[x for x in a if x >= 60]", text="Shartga moslarini yangi ro'yxatga yig'amiz."),
            card("zip va items", text="<code>zip(a, b)</code> — ikki ro'yxat juftlab, <code>d.items()</code> — kalit va qiymat birga."),
            card("Sanash", formula="son.get(k, 0) + 1", text="Lug'atda har elementning soni."),
        ],
        ("Sikl ichida ro'yxatdan o'chirmang!", "Elementlar siljiydi va ba'zilari o'tib ketadi — yangi ro'yxat yig'ing."),
        [
            ("[3, 8, 5] dan eng kattasini qaysi tayyor funksiya topadi?", "max()"),
            ("zip([1, 2], [\"a\", \"b\"]) qanday juftlar beradi?", "(1, 'a') va (2, 'b')."),
            ("\"olma\" so'zida nechta har xil harf bor?", "4 ta."),
        ],
        title="Sikl bilan qayta ishlash",
        badge=("zip", "juft"),
    ),
    "PY17": poster(
        "Funksiya — <b>nomli, qayta ishlatiladigan</b> kod bo'lagi: parametr oladi, natija qaytaradi.",
        code('''
def kvadrat(n):
    return n * n

def salom(ism):
    print("Salom,", ism)

print(kvadrat(4))
natija = salom("Ali")
print(natija)

def min_max(a):
    return min(a), max(a)
print(min_max([4, 9, 2]))
''', '''
16
Salom, Ali
None
(2, 9)
'''),
        [
            card("Parametr va argument", text="<b>Parametr</b> — e'londagi nom (<code>n</code>), <b>argument</b> — chaqirishdagi qiymat (<code>4</code>)."),
            card("print ≠ return", text="<code>print</code> ekranga chiqaradi, <code>return</code> qiymatni <b>qaytaradi</b>. return yo'q — <code>None</code>."),
            card("return tugatadi", text="<code>return</code>'dan keyingi qatorlar bajarilmaydi. Bir nechta qiymat — tuple."),
        ],
        ("Funksiya bitta ishni yaxshi bajarsin", "Nomi fe'l bilan: hisobla, tekshir, kvadrat."),
        [
            ("return yozilmagan funksiya nima qaytaradi?", "None"),
            ("def f(a, b): return a - b. f(b=2, a=10) natijasi?", "8"),
            ("Parametr va argumentning farqi nima?", "Parametr — e'londa, argument — chaqirishda."),
        ],
        title="def, parametr, return",
        badge=("def", "funksiya"),
    ),
    "PY18": poster(
        "Moslashuvchan funksiyalar: <b>default qiymat, *args, **kwargs</b> va o'zgaruvchi ko'rinish sohasi.",
        code('''
def salom(ism="Mehmon"):
    return f"Salom, {ism}!"
print(salom())
print(salom("Laylo"))

def jami(*sonlar):
    return sum(sonlar)
print(jami(1, 2, 3, 4))

def profil(**info):
    return info
print(profil(ism="Ali", yosh=14))
''', '''
Salom, Mehmon!
Salom, Laylo!
10
{'ism': 'Ali', 'yosh': 14}
'''),
        [
            card("Default", text="Default'li parametrlar <b>oxirida</b>: <code>def f(a, b=2)</code> ✓, <code>def f(a=1, b)</code> ✗."),
            card("*args va **kwargs", text="<code>*args</code> → <b>tuple</b>, <code>**kwargs</code> → <b>dict</b>."),
            card("Scope", text="Funksiya ichidagi o'zgaruvchi — <b>lokal</b>, tashqarida ko'rinmaydi. <code>global</code> — kam ishlating."),
        ],
        ("Tashqi o'zgaruvchini emas — parametr va return ishlating", "Shunda funksiya mustaqil va sinash oson."),
        [
            ("def f(*a): return a. f(1, 2) natijasi?", "(1, 2) — tuple."),
            ("**kwargs qaysi turda keladi?", "dict"),
            ("def f(a=1, b): ... nega xato?", "Default'li parametr default'sizdan oldin turibdi."),
        ],
        title="Default, *args, **kwargs",
        badge=("**", "kwargs"),
    ),
    "PY19": poster(
        "Qisqa va kuchli: <b>lambda</b> va tayyor funksiyalar bilan ro'yxatni bir qatorda qayta ishlaymiz.",
        code('''
a = [3, 8, 1, 6]
print(list(map(lambda x: x * 2, a)))
print(list(filter(lambda x: x > 4, a)))
print(sum(a), min(a), max(a))
sozlar = ["olma", "nok", "anor"]
print(sorted(sozlar, key=len))
print(max(sozlar, key=len))
print(any(x > 7 for x in a))
print(all(x > 0 for x in a))
''', '''
[6, 16, 2, 12]
[8, 6]
18 1 8
['nok', 'olma', 'anor']
olma
True
True
'''),
        [
            card("lambda", formula="lambda x: x * 2", text="<code>def f(x): return x * 2</code> ning qisqa shakli — faqat bitta ifoda."),
            card("map va filter", text="<code>map</code> — har elementga qo'llaydi, <code>filter</code> — rostlarini qoldiradi. Natijani <code>list()</code> ga o'rang."),
            card("key=", text="<code>sorted</code>, <code>min</code>, <code>max</code> — qaysi belgi bo'yicha solishtirish: <code>key=len</code>."),
        ],
        ("map/filter iterator qaytaradi → list() ga o'rang", "Aks holda <map object> chiqadi."),
        [
            ("list(map(lambda x: x + 1, [1, 2])) natijasi?", "[2, 3]"),
            ("filter qaysi elementlarni qoldiradi?", "Funksiya True qaytarganlarini."),
            ("max([\"a\", \"ccc\", \"bb\"], key=len) natijasi?", "'ccc'"),
        ],
        title="lambda, map, filter, sorted",
        badge=("λ", "lambda"),
    ),
    "PY20": poster(
        "Tayyor kodni ishlatamiz: <b>import</b> va tasodifiy sonlar uchun <code>random</code> kutubxonasi.",
        ("tiles", [
            ("import", "import random", "random.randint(1, 6)"),
            ("from", "from random import randint", "To'g'ridan-to'g'ri: randint(1, 6)"),
            ("as", "import random as r", "Qisqa nom: r.randint(1, 6)"),
            ("randint", "randint(a, b)", "a dan b gacha butun son — ikkalasi ham kiradi."),
            ("choice", "choice / sample", "Bitta tasodifiy element / k ta takrorlanmas."),
            ("seed", "seed(42)", "Har safar bir xil ketma-ketlik — test uchun."),
        ]),
        [
            card("Zar tashlash", code="from random import randint\nzar = randint(1, 6)", text="1, 2, 3, 4, 5 yoki 6."),
            card("Tanlov", code='choice(["tosh", "qog\'oz", "qaychi"])', text="Kompyuterning tasodifiy yurishi."),
            card("shuffle", text="<code>shuffle(a)</code> ro'yxatni <b>joyida</b> aralashtiradi va <code>None</code> qaytaradi."),
        ],
        ("Fayl nomini random.py qo'ymang!", "Aks holda Python o'z faylingizni import qiladi."),
        [
            ("randint(1, 3) qaysi sonlarni berishi mumkin?", "1, 2 yoki 3."),
            ("Ro'yxatdan 3 ta takrorlanmas element qaysi funksiya bilan olinadi?", "sample(a, 3)"),
            ("print(shuffle(a)) nima chiqaradi?", "None"),
        ],
        title="import usullari va random",
        badge=("🎲", "random"),
    ),
    "PY21": poster(
        "<code>math</code> bilan hisoblaymiz, <code>datetime</code> bilan <b>sana va vaqt</b> ustida amallar bajaramiz.",
        code('''
import math
from datetime import date, timedelta
print(math.sqrt(16), math.pi > 3)
print(math.ceil(4.2), math.floor(4.8))
print(math.factorial(5))
d = date(2026, 10, 7)
print(d + timedelta(days=7))
print((date(2026, 12, 31) - d).days)
print(d.strftime("%d.%m.%Y"))
''', '''
4.0 True
5 4
120
2026-10-14
85
07.10.2026
'''),
        [
            card("Yaxlitlash", formula="ceil(4.2) = [5], floor(4.8) = [4]", text="<code>ceil</code> — yuqoriga, <code>floor</code> — pastga."),
            card("Avtobuslar", formula="ceil(130 ÷ 50) = [3]", text="130 o'quvchiga 50 o'rinli avtobus — 3 ta kerak, 2.6 emas."),
            card("Sana ↔ matn", text="<code>strftime(\"%d.%m.%Y\")</code> — sanani matnga, <code>strptime</code> — matnni sanaga."),
        ],
        ("Ikki sana ayirmasi → timedelta → .days", "Tug'ilgan kungacha necha kun qolganini shunday topamiz."),
        [
            ("math.ceil(7.1) natijasi?", "8"),
            ("date(2026, 1, 1) + timedelta(days=31) qaysi sana?", "2026-02-01"),
            ("math.factorial(4) nechaga teng?", "24"),
        ],
        title="math va datetime",
        badge=("📅", "sana"),
    ),
    "PY22": poster(
        "Matndan <b>andoza bo'yicha</b> qidiramiz: telefon, email, son — <code>re</code> moduli bilan.",
        code('''
import re
t = "Ali 14 yosh, Vali 15, tel 901234567"
print(re.findall(r"\\d+", t))
print(re.search(r"\\d{9}", t).group())
m = re.search(r"(\\w+)@(\\w+)\\.uz", "ali@mail.uz")
print(m.group(1), m.group(2))
print(re.sub(r"\\s+", " ", "a   b    c"))
print(bool(re.fullmatch(r"[A-Z]\\d{3}", "B123")))
''', '''
['14', '15', '901234567']
901234567
ali mail
a b c
True
'''),
        [
            card("Funksiyalar", text="<code>findall</code> — hammasi, <code>search</code> — birinchisi, <code>fullmatch</code> — butun matn, <code>sub</code> — almashtirish."),
            card("Belgilar", text="<code>\\d</code> raqam, <code>\\w</code> harf/raqam, <code>\\s</code> bo'sh joy, <code>.</code> istalgan, <code>^</code> boshi, <code>$</code> oxiri."),
            card("Takror", text="<code>+</code> 1+, <code>*</code> 0+, <code>?</code> 0 yoki 1, <code>{3}</code> aynan 3, <code>{2,4}</code> 2–4."),
        ],
        ("Andoza — r\"...\" ichida", "Aks holda \\d kabi belgilar buziladi."),
        [
            ("re.findall(r\"\\d\", \"a1b2\") natijasi?", "['1', '2']"),
            ("\\d{2,3} nimaga mos keladi?", "2 yoki 3 ta raqamga."),
            ("Matndagi barcha probellarni olib tashlash uchun qaysi funksiya?", "re.sub"),
        ],
        title="RegEx amalda",
        badge=("\\d+", "andoza"),
    ),
    "PY23": poster(
        "Fayl tizimi bilan ishlaymiz va kodni <b>o'z modullarimizga</b> bo'lamiz.",
        ("flow", [
            ("os.getcwd()", "Joriy papka qayer?"),
            ("os.path.join()", "Tizimga mos yo'l: papka / fayl.txt"),
            ("os.makedirs()", "Papka yaratish: exist_ok=True bilan xatosiz."),
            ("utils.py", "O'z funksiyalaringiz alohida faylda."),
            ("from utils import", "main.py'da ishlatish."),
        ]),
        [
            card("Tekshiruvlar", text="<code>os.path.exists(p)</code>, <code>isfile(p)</code>, <code>getsize(p)</code>, <code>os.listdir(\".\")</code>."),
            card("__name__", code='if __name__ == "__main__":\n    main()', text="Faqat fayl to'g'ridan-to'g'ri ishga tushganda bajariladi."),
            card("pip va venv", text="<code>python -m venv .venv</code> — virtual muhit, <code>pip install nom</code> — tashqi kutubxona."),
        ],
        ("Yo'lni qo'lda \"/\" bilan yig'mang — os.path.join", "Windows'da \\, Linux'da / — join o'zi tanlaydi."),
        [
            ("Joriy papkani qaysi funksiya qaytaradi?", "os.getcwd()"),
            ("utils.py dagi qosh funksiyasini qanday import qilamiz?", "from utils import qosh"),
            ("__name__ == \"__main__\" qachon rost?", "Fayl to'g'ridan-to'g'ri ishga tushirilganda."),
        ],
        title="os va o'z modulingiz",
        badge=("os", "modul"),
    ),
    "PY24": poster(
        "Xato dasturni to'xtatmasin: <b>try / except</b> bilan ushlaymiz va foydalanuvchiga tushuntiramiz.",
        code('''
def bol(a, b):
    try:
        natija = a / b
    except ZeroDivisionError:
        print("Nolga bo'lib bo'lmaydi")
    else:
        print("Natija:", natija)
    finally:
        print("Tugadi")
bol(10, 2)
bol(5, 0)
''', '''
Natija: 5.0
Tugadi
Nolga bo'lib bo'lmaydi
Tugadi
'''),
        [
            card("Bloklar", text="<b>try</b> — xavfli kod, <b>except</b> — xato bo'lsa, <b>else</b> — xato bo'lmasa, <b>finally</b> — har doim."),
            card("Xato turlari", text="ValueError, TypeError, ZeroDivisionError, KeyError, IndexError, FileNotFoundError."),
            card("raise", code='if yosh < 0:\n    raise ValueError("Manfiy yosh")', text=""),
        ],
        ("Aniq xatoni ushlang: except ValueError", "Bo'sh except: hamma xatoni yashirib qo'yadi."),
        [
            ("int(\"abc\") qaysi xatoni beradi?", "ValueError"),
            ("finally bloki qachon bajariladi?", "Har doim — xato bo'lsa ham, bo'lmasa ham."),
            ("else bloki qachon bajariladi?", "try'da xato bo'lmasa."),
        ],
        title="try / except / else / finally",
        badge=("⚠", "xato"),
    ),
    "PY25": poster(
        "Dastur yopilsa ham ma'lumot qolsin: <b>txt faylga yozamiz va o'qiymiz</b>.",
        ("tiles", [
            ('"r"', "O'qish", "Fayl yo'q bo'lsa — FileNotFoundError."),
            ('"w"', "Yozish", "Eski mazmun o'chadi!"),
            ('"a"', "Qo'shish", "Oxiriga yozadi, eskisi qoladi."),
            ('"x"', "Faqat yangi", "Fayl bor bo'lsa — xato."),
        ]),
        [
            card("with open", code='with open("b.txt", "w",\n          encoding="utf-8") as f:\n    f.write("Ali 90\\n")', text="Blok tugagach fayl <b>avtomatik yopiladi</b>."),
            card("O'qish usullari", text="<code>read()</code> — hammasi, <code>readlines()</code> — ro'yxat, <code>for qator in f</code> — eng tejamkor."),
            card("strip()", text="Har qator oxirida <code>\\n</code> bor — <code>qator.strip()</code> bilan olib tashlang."),
        ],
        ("O'zbekcha harflar uchun encoding=\"utf-8\"", "Aks holda o‘, g‘ buzilib chiqadi."),
        [
            ("\"w\" rejimi eski mazmun bilan nima qiladi?", "O'chirib yuboradi."),
            ("Faylga eskisini saqlab qo'shish uchun qaysi rejim?", "\"a\""),
            ("with open(...) ning afzalligi nima?", "Fayl avtomatik yopiladi, xato bo'lsa ham."),
        ],
        title="Fayl rejimlari",
        badge=("txt", "fayl"),
    ),
    "PY26": poster(
        "Ma'lumotni <b>JSON</b> formatida saqlaymiz: lug'at va ro'yxatlar faylga yoziladi va qayta yuklanadi.",
        code('''
import json
d = {"ism": "Ali", "ball": [90, 85], "faol": True}
s = json.dumps(d, ensure_ascii=False)
print(s)
qayta = json.loads(s)
print(qayta["ball"][0])
print(json.loads(json.dumps({1: "a"})))
print(json.dumps(None), json.dumps(False))
''', '''
{"ism": "Ali", "ball": [90, 85], "faol": true}
90
{'1': 'a'}
null false
'''),
        [
            card("s bilan va s siz", text="<code>dumps/loads</code> — <b>satr</b> bilan, <code>dump/load</code> — <b>fayl</b> bilan."),
            card("Moslik", text="dict ↔ object, list ↔ array, True ↔ <code>true</code>, None ↔ <code>null</code>."),
            card("Chiroyli saqlash", text="<code>ensure_ascii=False</code> — o'zbekcha harflar, <code>indent=2</code> — o'qiladigan format."),
        ],
        ("JSON kalitlari — faqat satr", "{1: \"a\"} saqlansa, qayta yuklanganda {\"1\": \"a\"} bo'ladi."),
        [
            ("json.dumps(True) natijasi?", "'true'"),
            ("Faylga yozish uchun qaysi funksiya: dump yoki dumps?", "json.dump(obj, f)"),
            ("Nega {5: \"x\"} qayta yuklanganda kalit \"5\" bo'ladi?", "JSON'da kalitlar faqat satr."),
        ],
        title="JSON: saqlash va yuklash",
        badge=("{ }", "JSON"),
    ),
    "PY27": poster(
        "Klass — <b>chizma</b>, obyekt — undan yasalgan narsa. Ma'lumot va harakatni birga saqlaymiz.",
        code('''
class Mushuk:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh
        self.toq = False

    def ovqatlan(self):
        self.toq = True
        return f"{self.ism} to'ydi"

m1 = Mushuk("Momiq", 2)
m2 = Mushuk("Tom", 4)
print(m1.ovqatlan())
print(m1.toq, m2.toq)
''', '''
Momiq to'ydi
True False
'''),
        [
            card("__init__", text="Obyekt yaratilganda <b>avtomatik</b> chaqiriladi va atributlarni o'rnatadi."),
            card("self", text="Metod chaqirilayotgan obyektning <b>o'zi</b>. Har bir metodning birinchi parametri."),
            card("Atribut va metod", text="<b>Atribut</b> — ma'lumot (<code>self.ism</code>), <b>metod</b> — obyekt bajaradigan funksiya."),
        ],
        ("Bitta klass — istalgancha mustaqil obyekt", "m1 o'zgarsa, m2 o'zgarmaydi."),
        [
            ("Obyekt yaratilganda qaysi metod avtomatik chaqiriladi?", "__init__"),
            ("Klass nomi qaysi uslubda yoziladi?", "PascalCase: Mushuk, BankHisob."),
            ("m1.ovqatlan() dan keyin m2.toq nechaga teng?", "False — har obyekt mustaqil."),
        ],
        title="class va obyekt",
        badge=("class", "OOP"),
    ),
    "PY28": poster(
        "<b>Vorislik</b> — tayyor klassni kengaytirish, <b>polimorfizm</b> — bir xil buyruqqa har xil javob.",
        code('''
class Hayvon:
    def __init__(self, ism):
        self.ism = ism
    def ovoz(self):
        return "..."

class Kuchuk(Hayvon):
    def ovoz(self):
        return "Vov!"

class Mushuk(Hayvon):
    def ovoz(self):
        return "Miyov!"

for h in [Kuchuk("Bobik"), Mushuk("Tom")]:
    print(h.ism, h.ovoz())
print(isinstance(Kuchuk("A"), Hayvon))
''', '''
Bobik Vov!
Tom Miyov!
True
'''),
        [
            card("Voris klass", formula="class Kuchuk(Hayvon)", text="Kuchuk Hayvon'ning hamma atribut va metodlarini oladi."),
            card("super()", code="def __init__(self, ism, zot):\n    super().__init__(ism)\n    self.zot = zot", text=""),
            card("Overriding", text="Vorisda ota metodini <b>qayta yozish</b> — <code>ovoz()</code> har birida o'zicha."),
        ],
        ("Umumiy narsa — otada, farqi — vorisda", "Kodni takrorlamaslikning asosiy yo'li."),
        [
            ("Ota klass __init__ ini chaqirish uchun nima yoziladi?", "super().__init__(...)"),
            ("isinstance(Mushuk(\"Tom\"), Hayvon) natijasi?", "True"),
            ("Polimorfizm nima?", "Turli obyektlarga bir xil metod — har biri o'z javobini beradi."),
        ],
        title="Vorislik va polimorfizm",
        badge=("⇣", "voris"),
    ),
    "PY29": poster(
        "Obyektni himoya qilamiz va \"aqlli\" qilamiz: <b>inkapsulyatsiya, property</b> va maxsus metodlar.",
        code('''
class Mahsulot:
    def __init__(self, nom, narx):
        self.nom = nom
        self.narx = narx
    @property
    def narx(self):
        return self._narx
    @narx.setter
    def narx(self, qiymat):
        if qiymat < 0:
            raise ValueError("Manfiy narx")
        self._narx = qiymat
    def __str__(self):
        return f"{self.nom}: {self.narx} so'm"
print(Mahsulot("Non", 4000))
''', '''
Non: 4000 so'm
'''),
        [
            card("_ va __", text="<code>_narx</code> — “ichki, tegmang” kelishuvi. <code>__narx</code> — nomi o'zgartiriladi (name mangling)."),
            card("@property", text="Metodni atribut kabi o'qish: <code>m.narx</code>. <code>@narx.setter</code> — qiymat berishda tekshirish."),
            card("Maxsus metodlar", text="<code>__str__</code> print, <code>__len__</code> len, <code>__eq__</code> ==, <code>__lt__</code> &lt; va sorted, <code>__add__</code> +."),
        ],
        ("Noto'g'ri qiymat obyektga kira olmasin", "Setter ichida tekshiring va raise qiling."),
        [
            ("print(obj) qaysi maxsus metodni chaqiradi?", "__str__"),
            ("sorted() obyektlarni solishtirishi uchun qaysi metod kerak?", "__lt__"),
            ("Mahsulot(\"Non\", -5) nima bo'ladi?", "ValueError: Manfiy narx."),
        ],
        title="property va maxsus metodlar",
        badge=("@", "property"),
    ),
    "PY30": poster(
        "O'rganganlarni birlashtirib, <b>konsol o'yinlari</b> yasaymiz: Tosh-qog'oz-qaychi va Sonni top.",
        code('''
YUTADI = {"tosh": "qaychi",
          "qaychi": "qog'oz",
          "qog'oz": "tosh"}

def golib(men, komp):
    if men == komp:
        return "durang"
    if YUTADI[men] == komp:
        return "men"
    return "komp"

print(golib("tosh", "qaychi"))
print(golib("tosh", "qog'oz"))
print(golib("qaychi", "qaychi"))
''', '''
men
komp
durang
'''),
        [
            card("Tuzilma", text="Har o'yin — <b>alohida funksiya</b>; asosiy menyu — <code>while True</code> + <code>match</code>."),
            card("Xavfsiz kiritish", code="try:\n    son = int(input(\"Son: \"))\nexcept ValueError:\n    print(\"Raqam kiriting\")", text=""),
            card("Natijani saqlash", text="Eng yaxshi natija — <code>scores.json</code> faylida, keyingi safar yuklanadi."),
        ],
        ("Mantiqni kiritishdan ajrating", "golib() funksiyasini input'siz sinab ko'rish mumkin."),
        [
            ("golib(\"qog'oz\", \"tosh\") natijasi?", "men"),
            ("Sonni top o'yinida 1–100 orasidagi sonni nechta urinishda albatta topish mumkin?", "7 ta (har safar yarmiga bo'lib)."),
            ("Foydalanuvchi \"abc\" kiritsa, dastur yiqilmasligi uchun nima kerak?", "try / except ValueError."),
        ],
        title="G'olibni aniqlash",
        badge=("✊", "o'yin"),
    ),
    "PY31": poster(
        "Haqiqiy dastur kabi: <b>CRUD</b> amallari, JSON ombor va modullarga bo'lingan kod.",
        ("tiles", [
            ("C", "Create", "Yangi yozuv qo'shish — takrorlanmas id bilan."),
            ("R", "Read", "Ro'yxatni ko'rish, qidirish, saralash."),
            ("U", "Update", "Yozuvni id bo'yicha tahrirlash."),
            ("D", "Delete", "O'chirish — avval tasdiq so'rab."),
        ]),
        [
            card("Modullar", text="<code>storage.py</code> — JSON yuklash/saqlash, <code>models.py</code> — klass, <code>main.py</code> — menyu."),
            card("id", formula="max(id lar) + 1 = [yangi id]", text="Ism bir xil bo'lsa ham yozuvlar adashmaydi."),
            card("Saqlash", text="Har bir o'zgarishdan keyin <b>darhol</b> <code>save()</code> — dastur yopilsa ham ma'lumot qoladi."),
        ],
        ("O'chirishdan oldin — “Ishonchingiz komilmi? (ha/yo'q)”", "Qaytarib bo'lmaydigan amalni tasdiqlating."),
        [
            ("CRUD qisqartmasi nimani bildiradi?", "Create, Read, Update, Delete."),
            ("Nega har yozuvga id beramiz, ism yetmaydimi?", "Ismlar takrorlanishi mumkin — id takrorlanmas."),
            ("id lar [1, 2, 5] bo'lsa, yangi yozuv id si?", "6"),
        ],
        title="CRUD — 4 amal",
        badge=("CRUD", "ombor"),
    ),
    "PY32": poster(
        "BotFather'dan token olib, Python'da <b>birinchi Telegram botni</b> ishga tushiramiz.",
        code('''
import os
import telebot

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Salom! 👋")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id,
                     message.text)

bot.infinity_polling()
''', '''
/start
→ Salom! 👋

Qalaysan?
→ Qalaysan?
''', run=False),
        [
            card("BotFather", text="<b>@BotFather</b> → <code>/newbot</code> → nom va username → <b>token</b>."),
            card("Handler", text="Xabarga javob beruvchi funksiya: <code>@bot.message_handler(commands=[\"start\"])</code>."),
            card("O'rnatish", code="pip install pyTelegramBotAPI", text="<code>infinity_polling()</code> — yangi xabarlarni muntazam so'raydi."),
        ],
        ("Token — parol! Kodga yozmang, GitHub'ga yuklamang", "Muhit o'zgaruvchisi yoki .env faylida saqlang."),
        [
            ("Yangi bot qaysi bot orqali yaratiladi?", "@BotFather"),
            ("Nega tokenni kodga yozmaymiz?", "U maxfiy — kim bilsa, botni boshqaradi."),
            ("/start buyrug'iga javob beruvchi funksiya qanday belgilanadi?", "@bot.message_handler(commands=[\"start\"])"),
        ],
        title="Eng oddiy bot",
        badge=("🤖", "bot"),
    ),
    "PY33": poster(
        "Botni aqlli qilamiz: <b>inline tugmalar</b>, foydalanuvchi holati va ma'lumotni saqlash.",
        ("flow", [
            ("Inline tugma", "Xabar ostida: InlineKeyboardMarkup, callback_data bilan."),
            ("callback_query_handler", "Tugma bosilishini ushlaydi."),
            ("answer_callback_query", "“Soat” belgisini yo'qotadi."),
            ("register_next_step_handler", "Keyingi xabarni kutish: “Ismingiz?”"),
            ("users.json", "{\"user_id\": {...}} — ma'lumot saqlanadi."),
        ]),
        [
            card("Holat (state)", text="Foydalanuvchi qaysi bosqichda: “ism kutilmoqda”, “yosh kutilmoqda”."),
            card("JSON kaliti", formula="str(user_id) → [kalit]", text="JSON'da kalit faqat satr — <code>str(message.from_user.id)</code>."),
            card("Ishonchlilik", text="Handler ichidagi xavfli joylar — <code>try/except</code>. Bot bitta xatodan to'xtamasin."),
        ],
        ("Har tugma bosilishiga javob bering", "answer_callback_query bo'lmasa tugma “osilib” qoladi."),
        [
            ("Inline tugma bosilganda botga nima keladi?", "callback_data."),
            ("Foydalanuvchidan ketma-ket ism va yoshni so'rash uchun nima ishlatamiz?", "register_next_step_handler."),
            ("Nega user_id ni str() qilib saqlaymiz?", "JSON kalitlari faqat satr bo'ladi."),
        ],
        title="Callback va holat",
        badge=("⌨", "tugma"),
    ),
    "PY34": poster(
        "Loyihani <b>GitHub'ga joylaymiz</b>, README yozamiz va 5 daqiqalik demo bilan himoya qilamiz.",
        ("flow", [
            ("git add .", "O'zgarishlarni tayyorlash."),
            ("git commit -m", "Saqlash nuqtasi: “Menyu qo'shildi”."),
            ("git push", "GitHub'ga yuborish."),
            ("README.md", "Nima qiladi, qanday o'rnatiladi, skrinshot."),
            ("Himoya", "5 daqiqa demo + 3 daqiqa savol-javob."),
        ]),
        [
            card(".gitignore", code=".env\n.venv/\n__pycache__/\n*.json", text="Maxfiy va keraksiz fayllar GitHub'ga tushmasin."),
            card("Baholash", formula="40 + 30 + 20 + 10 = [100]", text="Ishlashi, kod sifati, taqdimot, GitHub va README."),
            card("requirements.txt", text="Kerakli kutubxonalar ro'yxati: <code>pip install -r requirements.txt</code>."),
        ],
        ("Demo oldidan bir marta to'liq sinab ko'ring", "Internet, token va ma'lumotlar tayyor bo'lsin."),
        [
            ("Git'da o'zgarishni GitHub'ga yuborish buyrug'i?", "git push"),
            (".env fayli nega .gitignore ga yoziladi?", "Unda token va parollar bor."),
            ("Baholashda eng katta ulush nimaga beriladi?", "Ishlashi va foydaliligiga — 40 ball."),
        ],
        title="Koddan himoyagacha",
        badge=("🎓", "himoya"),
    ),
}
