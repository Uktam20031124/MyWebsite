"""Python kursi: "Darsni qayta mustahkamlash" materiallari (mavzu kaliti bo'yicha).

O'quvchi testdan past natija olsa, profilida ko'radi. Format — ``ui.study_md``:
## sarlavha, ### kichik sarlavha, - / 1. ro'yxat, > eslatma, ``` kod ```, `kod`, **qalin**.
Python misollaridagi "Natija:" bloklari kodni ishga tushirib tekshirilgan.
"""

STUDY = {
    "PY01": """
## Mavzu nima haqida
Python — o'qilishi oson, kuchli dasturlash tili. Sayt, bot, o'yin, sun'iy intellekt, avtomatlashtirish — hammasida ishlatiladi. Bu darsda o'rnatish, VS Code va birinchi dastur.

## Asosiy tushunchalar
- **Interpretator** — kodni qatorma-qator bajaradi. Fayl kengaytmasi `.py`.
- O'rnatishda Windows'da **Add Python to PATH** belgisini qo'ying, aks holda terminal `python` ni tanimaydi.
- Tekshirish: `python --version`. Ishga tushirish: `python fayl.py`.
- **REPL** (interaktiv rejim): terminalda `python` → `>>>` belgisi; har bir buyruq darhol bajariladi.
- `print()` — ekranga chiqaradi. `#` — izoh (Python uni o'qimaydi).
- `print` parametrlari: `sep` — qiymatlar orasidagi belgi (standart: probel), `end` — oxiridagi belgi (standart: yangi qator).

## Bajarilgan misollar
### Misol 1. Birinchi dastur
```
# Bu mening birinchi dasturim
print("Salom, dunyo!")
print("Mening ismim Ali")
```
Natija:
```
Salom, dunyo!
Mening ismim Ali
```

### Misol 2. sep va end
```
print("2026", "10", "19", sep="-")
print("Yuklanmoqda", end="...")
print("tayyor")
```
Natija:
```
2026-10-19
Yuklanmoqda...tayyor
```

### Misol 3. Matnni takrorlash va hisoblash
```
print("=" * 20)
print("Natija:", 7 * 6)
print("=" * 20)
```
Natija:
```
====================
Natija: 42
====================
```

## Ko'p uchraydigan xatolar
- Qo'shtirnoqni yopmaslik: `print("Salom)` → **SyntaxError**.
- `Print` deb katta harf bilan yozish → **NameError** (Python katta-kichik harfni farqlaydi).
- Faylni saqlamasdan ishga tushirish — eski versiya ishlaydi.

## Chuqurroq
- `print()` bo'sh — bitta bo'sh qator chiqaradi.
- `print("A", "B", "C", sep="")` → `ABC`.
- VS Code'da **Python extension** — rangli kod, xatolarni ko'rsatish va ▶ tugmasi bilan ishga tushirish.

## O'zingizni tekshiring
1. `print("Ha", "Yo'q", sep=" / ")` nima chiqaradi? (Ha / Yo'q)
2. `print("-" * 5)` nima chiqaradi? (-----)
3. PATH belgisi qo'yilmasa nima bo'ladi?
""",
    "PY02": """
## Mavzu nima haqida
O'zgaruvchi — qiymatni nom bilan saqlash. Har bir qiymatning turi bor: butun son, kasr son, matn, mantiqiy qiymat. Turni bilish xatolarning oldini oladi.

## Asosiy tushunchalar
- Qiymat berish: `yosh = 14`. `=` — "teng" emas, "qiymat ber".
- **Turlar:** `int` (14), `float` (3.14), `str` ("salom"), `bool` (True/False).
- `type(x)` — turini ko'rsatadi.
- **Nomlash qoidalari:** harf yoki `_` bilan boshlanadi, raqam bilan boshlanmaydi, bo'sh joy va `-` yo'q, kalit so'zlar (`for`, `class`, `if`) bo'lmaydi. Uslub: `snake_case`.
- **Konstanta** — o'zgarmasligi kerak bo'lgan qiymat, KATTA harflar bilan: `PI = 3.14159`.
- Python **dinamik**: bitta o'zgaruvchiga keyin boshqa turdagi qiymat berish mumkin.

## Bajarilgan misollar
### Misol 1. Turlar
```
ism = "Ali"
yosh = 14
boy = 1.62
talaba = True
print(type(ism), type(yosh), type(boy), type(talaba))
```
Natija:
```
<class 'str'> <class 'int'> <class 'float'> <class 'bool'>
```

### Misol 2. Bir qatorda bir nechta qiymat va almashtirish
```
a, b = 5, 10
a, b = b, a
print(a, b)
```
Natija:
```
10 5
```

### Misol 3. Doira yuzi
```
PI = 3.14
r = 5
yuza = PI * r * r
print("Yuza:", yuza)
```
Natija:
```
Yuza: 78.5
```

### Misol 4. Qiymat yangilanadi
```
ball = 10
ball = ball + 5
print(ball)
```
Natija:
```
15
```

## Ko'p uchraydigan xatolar
- `2ism = "Ali"` → SyntaxError (raqam bilan boshlangan).
- `talaba-yoshi = 14` → `-` ayirish deb tushuniladi.
- `Ism` va `ism` — ikki xil o'zgaruvchi.
- `"25"` (matn) va `25` (son) — har xil narsa.

## Chuqurroq
- O'zgaruvchi — qiymatga "yorliq". `a = b = 0` ikkalasiga ham 0.
- `True` va `False` aslida 1 va 0 kabi ishlaydi: `True + True` → 2.
- Yaxshi nom — tushunarli nom: `x` emas, `oylik_tolov`.

## O'zingizni tekshiring
1. `type(10 / 2)` natijasi? (`<class 'float'>`)
2. `x = 5; x = "besh"; print(type(x))`? (`<class 'str'>`)
3. `my-name`, `_yosh`, `class`, `ism2` — qaysi biri to'g'ri nom? (`_yosh`, `ism2`)
""",
    "PY03": """
## Mavzu nima haqida
Foydalanuvchidan ma'lumot olish (`input`) va turlarni o'zgartirish. `input()` doim **matn** qaytaradi — hisoblash uchun uni songa aylantirish kerak.

## Asosiy tushunchalar
- `input("Savol: ")` — foydalanuvchi yozganini **str** sifatida qaytaradi.
- `int("12")` → 12, `float("2.5")` → 2.5, `str(10)` → "10", `bool(x)` → True/False.
- `int(3.9)` → 3 (kasr qismi **tashlanadi**, yaxlitlanmaydi).
- `int("3.5")` → **ValueError** (avval float, keyin int: `int(float("3.5"))` → 3).
- `round(3.567, 2)` → 3.57.
- `bool("")` → False, `bool("0")` → True (bo'sh bo'lmagan har qanday satr — True).

## Bajarilgan misollar
### Misol 1. Matn va son farqi
```
print("12" + "3")
print(int("12") + 3)
print("5" * 3)
```
Natija:
```
123
15
555
```

### Misol 2. Yoshni hisoblash (input bilan)
```
yil = int(input("Tug'ilgan yilingiz: "))
print("Yoshingiz:", 2026 - yil)
```
Foydalanuvchi 2012 kiritsa: `Yoshingiz: 14`.

### Misol 3. Turlarni o'zgartirish
```
print(int(3.9), float("2.5") * 2, str(10) + "5")
print(round(3.567, 2), round(2.5), round(3.5))
print(bool(""), bool("0"), bool(0))
```
Natija:
```
3 5.0 105
3.57 2 4
False True False
```
Diqqat: `round(2.5)` → 2, `round(3.5)` → 4 ("bankir yaxlitlashi" — juft songa).

### Misol 4. O'rtacha baho
```
a = "85"
b = "90"
ortacha = (int(a) + int(b)) / 2
print(ortacha)
```
Natija:
```
87.5
```

## Ko'p uchraydigan xatolar
- `input()` ni songa aylantirmay hisoblash: `"5" + 1` → **TypeError**.
- `int("abc")` yoki `int("3.5")` → **ValueError**.
- `yosh = input(int("..."))` — tartib teskari; to'g'risi `int(input("..."))`.

## Chuqurroq
- `"12".isdigit()` → True — matn faqat raqamlardan iboratmi, tekshirish (xatoni oldini olish).
- `int("101", 2)` → 5 — ikkilik sanoq sistemasidan o'girish.
- f-string bilan formatlash: `f"{3.14159:.2f}"` → '3.14'.

## O'zingizni tekshiring
1. `int("7") * 2` va `"7" * 2` natijalari? (14 va '77')
2. `int(-2.7)`? (-2)
3. Foydalanuvchi kiritgan kasr sonni qanday olasiz? (`float(input())`)
""",
    "PY04": """
## Mavzu nima haqida
Satr (str) bilan ishlash: belgilarga indeks bilan murojaat, kesish (slicing), metodlar va f-string. Matn — dasturlardagi eng ko'p ishlatiladigan ma'lumot.

## Asosiy tushunchalar
- Indeks 0 dan: `"Python"[0]` → 'P'. Teskari: `[-1]` → oxirgi belgi.
- **Slicing:** `s[boshi:oxiri:qadam]` — oxiri **kirmaydi**. `s[1:4]`, `s[:3]`, `s[::-1]` (teskari).
- `len(s)` — uzunlik.
- Metodlar: `upper()`, `lower()`, `title()`, `strip()`, `replace(a, b)`, `split(",")`, `count("a")`, `find("x")`, `startswith()`.
- **f-string:** `f"{ism} {yosh} yoshda"`.
- Satrlar **o'zgarmas** (immutable): `s[0] = "z"` → TypeError. Metodlar yangi satr qaytaradi.

## Bajarilgan misollar
### Misol 1. Indekslash va kesish
```
s = "Python"
print(s[0], s[-1], s[1:4], s[:2], s[::-1])
```
Natija:
```
P n yth Py nohtyP
```

### Misol 2. Metodlar
```
matn = "  salom dunyo  "
print(matn.strip().title())
print("olma,nok,uzum".split(","))
print("banan".count("a"), "kitob".replace("k", "K"))
```
Natija:
```
Salom Dunyo
['olma', 'nok', 'uzum']
2 Kitob
```

### Misol 3. f-string
```
ism = "Ali"
ball = 87.456
print(f"{ism}ning bali: {ball:.1f}")
print(f"{ism.upper()} — {len(ism)} harf")
```
Natija:
```
Alining bali: 87.5
ALI — 3 harf
```

### Misol 4. Palindrom tekshiruvi
```
soz = "Kiyik"
toza = soz.lower()
print(toza == toza[::-1])
```
Natija:
```
True
```

## Ko'p uchraydigan xatolar
- `s[6]` uzunligi 6 bo'lgan satrda → **IndexError** (oxirgi indeks 5).
- `s.upper()` deb yozib, natijani saqlamaslik — `s` o'zgarmaydi: `s = s.upper()`.
- f-string oldidagi `f` ni unutish: `"{ism}"` shunchaki matn bo'lib qoladi.

## Chuqurroq
- `"-".join(["a", "b", "c"])` → 'a-b-c' (split'ning teskarisi).
- `s.find("x")` topilmasa −1 qaytaradi; `s.index("x")` esa xato beradi.
- `"ab" in "abc"` → True — kichik satr bormi tekshirish.

## O'zingizni tekshiring
1. `"dasturlash"[3:7]`? ('turl')
2. `"a,b,,c".split(",")`? (['a', 'b', '', 'c'])
3. `" Hi ".strip().lower() + "!"`? ('hi!')
""",
    "PY05": """
## Mavzu nima haqida
Arifmetik operatorlar — Python kalkulyator sifatida. Butun bo'lish va qoldiq (`//`, `%`) amaliy masalalarda juda ko'p ishlatiladi: vaqtni hisoblash, juft-toqlik, raqamlarni ajratish.

## Asosiy tushunchalar
- `+ - *` — oddiy amallar. `/` — bo'lish, natija doim **float**: `10 / 5` → 2.0.
- `//` — butun bo'lish (pastga yaxlitlaydi): `7 // 2` → 3.
- `%` — qoldiq: `7 % 2` → 1.
- `**` — daraja: `2 ** 3` → 8.
- **Tartib:** `**`, keyin `* / // %`, keyin `+ -`. Qavslar birinchi.
- Qisqa yozuv: `x += 5` (x = x + 5), `x *= 2`, `x -= 1`.

## Bajarilgan misollar
### Misol 1. Asosiy amallar
```
print(7 / 2, 7 // 2, 7 % 2, 2 ** 3)
print(2 + 3 * 4, (2 + 3) * 4)
```
Natija:
```
3.5 3 1 8
14 20
```

### Misol 2. Sekundlarni soat:daqiqa:sekundga
```
jami = 3725
soat = jami // 3600
daqiqa = jami % 3600 // 60
sekund = jami % 60
print(soat, daqiqa, sekund)
```
Natija:
```
1 2 5
```

### Misol 3. Sonning raqamlari
```
son = 547
birlar = son % 10
onlar = son // 10 % 10
yuzlar = son // 100
print(yuzlar, onlar, birlar, yuzlar + onlar + birlar)
```
Natija:
```
5 4 7 16
```

### Misol 4. Juft yoki toq
```
for son in [4, 7, 10]:
    print(son, son % 2 == 0)
```
Natija:
```
4 True
7 False
10 True
```

## Ko'p uchraydigan xatolar
- `5 / 0` → **ZeroDivisionError**.
- `2 + 3 * 4` ni 20 deb o'ylash — ko'paytirish birinchi.
- `-7 // 2` → −4 (pastga yaxlitlaydi, −3 emas!).

## Chuqurroq
- `divmod(17, 5)` → (3, 2) — bir yo'la bo'linma va qoldiq.
- `abs(-5)` → 5, `max(3, 9, 2)` → 9.
- `0.1 + 0.2` → 0.30000000000000004 — kasr sonlar kompyuterda taxminiy saqlanadi; pul uchun `round` yoki butun so'm ishlating.

## O'zingizni tekshiring
1. `17 % 5` va `17 // 5`? (2 va 3)
2. `10 - 2 ** 2 * 2`? (2)
3. 125 daqiqa necha soat va necha daqiqa? (`125 // 60` = 2, `125 % 60` = 5)
""",
    "PY06": """
## Mavzu nima haqida
Taqqoslash va mantiqiy operatorlar — dastur "qaror qabul qilishi" uchun. Har bir shart natijasi `True` yoki `False`.

## Asosiy tushunchalar
- Taqqoslash: `==` (teng), `!=` (teng emas), `>`, `<`, `>=`, `<=`.
- `=` — qiymat berish, `==` — tenglikni **tekshirish**.
- Mantiqiy: `and` (ikkalasi rost bo'lsa rost), `or` (bittasi rost bo'lsa yetarli), `not` (teskarisi).
- **Tartib:** `not` → `and` → `or`. Shubha bo'lsa — qavs qo'ying.
- Zanjir: `13 <= yosh <= 17`.
- Satrlar alifbo tartibida solishtiriladi: `"a" < "b"` → True. Katta-kichik harf farqlanadi.

## Bajarilgan misollar
### Misol 1. Oddiy taqqoslash
```
print(5 == 5.0, 3 != 4, "Python" == "python", "a" < "b")
```
Natija:
```
True True False True
```

### Misol 2. and / or / not
```
yosh = 15
pul = 20000
print(yosh >= 12 and pul >= 25000)
print(yosh >= 12 or pul >= 25000)
print(not (yosh > 18))
```
Natija:
```
False
True
True
```

### Misol 3. Oraliqda tekshirish
```
yosh = 15
print(13 <= yosh <= 17)
ball = 72
print(ball >= 60 and ball < 86)
```
Natija:
```
True
True
```

### Misol 4. Tartib muhim
```
print(True or False and False)
print((True or False) and False)
```
Natija:
```
True
False
```
Birinchisida avval `and` bajariladi: `False and False` → False, keyin `True or False` → True.

## Ko'p uchraydigan xatolar
- `if x = 5:` → SyntaxError; to'g'risi `==`.
- `yosh > 13 and < 17` → xato; har tomonni to'liq yozing: `yosh > 13 and yosh < 17`.
- `"10" > "9"` → False! Satrlar belgi-belgi solishtiriladi ("1" < "9"). Sonlarni songa aylantiring.

## Chuqurroq
- **Qisqa tutashuv:** `and` birinchi qiymat False bo'lsa, ikkinchisini tekshirmaydi. `x != 0 and 10 / x > 1` — nolga bo'lish xatosidan himoya.
- `in` operatori: `"a" in "olma"` → True, `3 in [1, 2, 3]` → True.

## O'zingizni tekshiring
1. `not (5 > 3 or 2 > 10)`? (False)
2. `x = 0` bo'lsa `x != 0 and 10 / x > 1`? (False, xato chiqmaydi)
3. `"apple" < "banana"`? (True)
""",
    "PY07": """
## Mavzu nima haqida
Shart operatorlari (`if`, `elif`, `else`) dasturga tanlov qilish imkonini beradi: "agar ... bo'lsa — buni qil, aks holda — boshqasini".

## Asosiy tushunchalar
- `if shart:` — oxirida **ikki nuqta**; tanasi **4 ta probel** chekinish bilan.
- `elif` — oldingi shartlar yolg'on bo'lsa, navbatdagisini tekshiradi (ko'p bo'lishi mumkin).
- `else:` — hech biri mos kelmasa; shart yozilmaydi.
- Bitta zanjirda **faqat bitta** blok bajariladi — birinchi rost shartli blok.
- "Bo'sh" qiymatlar (0, "", [], None) shartda **False** hisoblanadi.
- Qisqa shart: `natija = "juft" if x % 2 == 0 else "toq"`.

## Bajarilgan misollar
### Misol 1. Baho
```
ball = 75
if ball >= 86:
    print("5")
elif ball >= 71:
    print("4")
elif ball >= 56:
    print("3")
else:
    print("2")
```
Natija:
```
4
```
Diqqat: 75 >= 56 ham rost, lekin zanjir birinchi mos kelganda to'xtaydi.

### Misol 2. Musbat, manfiy, nol
```
for son in [5, -3, 0]:
    if son > 0:
        print(son, "musbat")
    elif son < 0:
        print(son, "manfiy")
    else:
        print(son, "nol")
```
Natija:
```
5 musbat
-3 manfiy
0 nol
```

### Misol 3. Bo'sh qiymat
```
ism = ""
if ism:
    print("Salom,", ism)
else:
    print("Ism kiritilmadi")
```
Natija:
```
Ism kiritilmadi
```

### Misol 4. Qisqa shart
```
x = 7
print("juft" if x % 2 == 0 else "toq")
```
Natija:
```
toq
```

## Ko'p uchraydigan xatolar
- Ikki nuqtani unutish: `if x > 5` → SyntaxError.
- Chekinish noto'g'ri → IndentationError yoki kod noto'g'ri blokka tushadi.
- Bir nechta alohida `if` yozish, `elif` o'rniga — bir nechtasi birdan bajarilishi mumkin.
- Shartlar tartibi: `if ball >= 56` birinchi bo'lsa, 90 ball ham "3" oladi.

## Chuqurroq
- Shartlarni **kattadan kichikka** (yoki aniqdan umumiyga) tartiblang.
- Murakkab shartni o'zgaruvchiga oling: `otdi = ball >= 60 and davomat >= 80`, keyin `if otdi:`.

## O'zingizni tekshiring
1. `x = 10`: `if x > 5: print("A")` va keyin `if x > 8: print("B")` — nima chiqadi? (A va B)
2. Shu shartlar `if/elif` bo'lsa-chi? (faqat A)
3. Yil kabisa: 4 ga bo'linsin, lekin 100 ga bo'linmasin yoki 400 ga bo'linsin — shartni yozing.
""",
    "PY08": """
## Mavzu nima haqida
Murakkab tekshiruvlar: ichma-ich shartlar, `match-case` (Python 3.10+) va RegEx (andoza) bilan matn formatini tekshirish — telefon, email, parol.

## Asosiy tushunchalar
- **Ichma-ich if** — shart ichida yana shart. Ko'pincha `and` bilan soddalashtiriladi.
- **match-case** — bitta qiymatni bir nechta variant bilan solishtirish; `case _:` — "boshqa hamma holat".
- **RegEx:** `import re`. `re.fullmatch(andoza, matn)` — butun matn mos kelsa natija, aks holda None. `re.search` — matn ichida biror joyda.
- Andozalar: `\\d` raqam, `[A-Z]` katta harf, `[a-z]` kichik harf, `{9}` aynan 9 marta, `+` 1 yoki ko'p, `\\+` — "+" belgisining o'zi.
- Andozani `r"..."` (raw string) bilan yozing.

## Bajarilgan misollar
### Misol 1. Ichma-ich va soddalashtirilgan
```
x = 15
if x > 10:
    if x % 2 == 0:
        print("katta juft")
    else:
        print("katta toq")
if x > 10 and x % 2 == 1:
    print("xuddi shu, qisqaroq")
```
Natija:
```
katta toq
xuddi shu, qisqaroq
```

### Misol 2. match-case menyu
```
tanlov = "2"
match tanlov:
    case "1":
        print("Yangi o'yin")
    case "2":
        print("Natijalar")
    case "0":
        print("Chiqish")
    case _:
        print("Noma'lum buyruq")
```
Natija:
```
Natijalar
```

### Misol 3. Telefon raqam
```
import re
for tel in ["+998901234567", "998901234567", "+99890123"]:
    print(tel, bool(re.fullmatch(r"\\+998\\d{9}", tel)))
```
Natija:
```
+998901234567 True
998901234567 False
+99890123 False
```

### Misol 4. Parol kuchi
```
import re
parol = "Olma2026"
tekshiruv = [
    len(parol) >= 8,
    re.search(r"[A-Z]", parol) is not None,
    re.search(r"[a-z]", parol) is not None,
    re.search(r"\\d", parol) is not None,
]
print(tekshiruv, "kuchli" if all(tekshiruv) else "zaif")
```
Natija:
```
[True, True, True, True] kuchli
```

## Ko'p uchraydigan xatolar
- `re.match` faqat boshidan tekshiradi, oxirini emas — to'liq moslik uchun `fullmatch`.
- `+` ni andozada ekranlamaslik: `"+998"` — "+" kvantifikator bo'lib qoladi; `\\+998` yozing.
- `match-case` Python 3.10 dan eski versiyada ishlamaydi.

## Chuqurroq
- `all([...])` — hammasi rost bo'lsa True; `any([...])` — bittasi rost bo'lsa True.
- Email uchun soddalashgan andoza: `r"[\\w.]+@[\\w]+\\.[a-z]{2,}"`.
- match-case bir nechta qiymat: `case "y" | "yes":`.

## O'zingizni tekshiring
1. `re.fullmatch(r"\\d{3}", "12a")` nima qaytaradi? (None)
2. `case _:` qachon bajariladi?
3. "AB-1234" formatidagi raqam uchun andoza yozing. (`r"[A-Z]{2}-\\d{4}"`)
""",
    "PY09": """
## Mavzu nima haqida
Ro'yxat (list) — bir nechta qiymatni tartib bilan saqlaydi: o'quvchilar, baholar, mahsulotlar. Ro'yxat o'zgaruvchan — element qo'shish, o'zgartirish, o'chirish mumkin.

## Asosiy tushunchalar
- Yaratish: `[]` yoki `[10, 20, 30]`. Turli turdagi elementlar bo'lishi mumkin.
- Indeks 0 dan; `a[-1]` — oxirgisi. Mavjud bo'lmagan indeks → **IndexError**.
- Slicing: `a[1:3]`, `a[:2]`, `a[::2]`, `a[::-1]` — **yangi** ro'yxat qaytaradi.
- `len(a)`, `x in a`, `a + b` (birlashtirish), `a * 2` (takrorlash).
- O'zgartirish: `a[0] = 100`.

## Bajarilgan misollar
### Misol 1. Indeks va kesish
```
a = [10, 20, 30, 40, 50]
print(a[1], a[-1], a[1:3], a[:2], a[::2], a[::-1])
```
Natija:
```
20 50 [20, 30] [10, 20] [10, 30, 50] [50, 40, 30, 20, 10]
```

### Misol 2. O'zgartirish va tekshirish
```
mevalar = ["olma", "nok", "uzum"]
mevalar[1] = "anor"
print(mevalar, len(mevalar), "uzum" in mevalar)
```
Natija:
```
['olma', 'anor', 'uzum'] 3 True
```

### Misol 3. Birlashtirish
```
print([1, 2] + [3], [0] * 4)
```
Natija:
```
[1, 2, 3] [0, 0, 0, 0]
```

### Misol 4. Baholar o'rtachasi
```
baholar = [5, 4, 5, 3, 5]
print(sum(baholar) / len(baholar), max(baholar), min(baholar))
```
Natija:
```
4.4 5 3
```

## Ko'p uchraydigan xatolar
- `a[5]` 5 elementli ro'yxatda → IndexError (oxirgi indeks 4).
- `a[1:3]` 3-indeksni ham oladi deb o'ylash — oxiri kirmaydi.
- Bo'sh ro'yxatda `sum(a) / len(a)` → ZeroDivisionError.

## Chuqurroq
- Slicing'ning oxiri chegaradan oshsa xato bermaydi: `[1, 2][0:10]` → [1, 2].
- `a[:]` — ro'yxat nusxasi.
- `list("abc")` → ['a', 'b', 'c'], `list(range(5))` → [0, 1, 2, 3, 4].

## O'zingizni tekshiring
1. `a = [3, 6, 9, 12]; a[-2]`? (9)
2. `a[1:]`? ([6, 9, 12])
3. Ro'yxatning oxirgi ikki elementini qanday olasiz? (`a[-2:]`)
""",
    "PY10": """
## Mavzu nima haqida
Ro'yxat metodlari bilan element qo'shish, o'chirish, saralash; **list comprehension** — bir qatorda yangi ro'yxat yaratish.

## Asosiy tushunchalar
- `append(x)` — oxiriga; `insert(i, x)` — i-o'ringa; `extend([..])` — bir nechtasini qo'shish.
- `remove(x)` — **qiymat** bo'yicha birinchisini o'chiradi; `pop()` — oxirgisini olib tashlab **qaytaradi**; `pop(i)` — i-indeksdagini.
- `sort()` — ro'yxatning **o'zini** saralaydi (None qaytaradi); `sorted(a)` — **yangi** saralangan ro'yxat.
- `index(x)`, `count(x)`, `reverse()`, `clear()`.
- **Comprehension:** `[ifoda for x in ro'yxat if shart]`.
- `b = a` — nusxa emas, **bitta ro'yxatga ikkinchi nom**.

## Bajarilgan misollar
### Misol 1. Qo'shish va o'chirish
```
a = [1, 2, 3]
a.append(4)
a.insert(0, 9)
a.extend([5, 6])
a.remove(2)
x = a.pop()
print(a, x)
```
Natija:
```
[9, 1, 3, 4, 5] 6
```

### Misol 2. sort va sorted
```
a = [3, 1, 2]
b = sorted(a)
print(a, b)
a.sort(reverse=True)
print(a)
```
Natija:
```
[3, 1, 2] [1, 2, 3]
[3, 2, 1]
```

### Misol 3. Comprehension
```
print([x * 2 for x in [1, 2, 3]])
print([x for x in range(10) if x % 2 == 0])
print([s.upper() for s in ["ali", "vali"]])
```
Natija:
```
[2, 4, 6]
[0, 2, 4, 6, 8]
['ALI', 'VALI']
```

### Misol 4. Nusxa tuzog'i
```
a = [1, 2, 3]
b = a
c = a.copy()
b.append(4)
print(a, c)
```
Natija:
```
[1, 2, 3, 4] [1, 2, 3]
```

## Ko'p uchraydigan xatolar
- `a = a.sort()` → a None bo'lib qoladi!
- `remove(5)` ro'yxatda 5 yo'q bo'lsa → ValueError.
- `append([3, 4])` — ichiga ro'yxat qo'shadi: [1, 2, [3, 4]]; ko'p elementlar uchun `extend`.

## Chuqurroq
- `sorted(ismlar, key=len)` — uzunlik bo'yicha; `key=str.lower` — katta-kichik harfga qaramay.
- Comprehension ichida `if-else`: `["juft" if x % 2 == 0 else "toq" for x in a]`.

## O'zingizni tekshiring
1. `a = [5, 6, 7]; a.pop(0)` — nima qaytaradi va a qanday bo'ladi? (5, [6, 7])
2. `[x ** 2 for x in range(1, 4)]`? ([1, 4, 9])
3. `[1, 2, 2, 3].count(2)`? (2)
""",
    "PY11": """
## Mavzu nima haqida
Tuple — o'zgarmas ro'yxat; Set — takrorlanmas elementlar to'plami. Tuple ma'lumotni "qotirish" uchun, set — takrorlarni olib tashlash va to'plam amallari uchun.

## Asosiy tushunchalar
- **Tuple:** `(1, 2, 3)`; bitta elementli: `(5,)` — vergul shart! O'zgartirib bo'lmaydi → TypeError.
- **Ochish (unpacking):** `x, y = (10, 20)`.
- **Set:** `{1, 2, 3}`; bo'sh set — `set()` (`{}` — bu bo'sh lug'at!). Elementlar takrorlanmaydi, tartib yo'q, indeks yo'q.
- Set amallari: `&` kesishma, `|` birlashma, `-` ayirma, `^` simmetrik ayirma.
- `add(x)`, `remove(x)`, `discard(x)` (yo'q bo'lsa ham xato bermaydi).

## Bajarilgan misollar
### Misol 1. Tuple
```
nuqta = (3, 4)
x, y = nuqta
print(x, y, len(nuqta), type((5,)), type((5)))
```
Natija:
```
3 4 2 <class 'tuple'> <class 'int'>
```

### Misol 2. Takrorlarni olib tashlash
```
sonlar = [1, 2, 2, 3, 3, 3]
print(sorted(set(sonlar)), len(set(sonlar)))
```
Natija:
```
[1, 2, 3] 3
```

### Misol 3. To'plam amallari
```
python = {"Ali", "Vali", "Sami"}
dizayn = {"Vali", "Nigora"}
print(sorted(python & dizayn))
print(sorted(python | dizayn))
print(sorted(python - dizayn))
```
Natija:
```
['Vali']
['Ali', 'Nigora', 'Sami', 'Vali']
['Ali', 'Sami']
```

### Misol 4. Funksiyadan tuple
```
def min_max(a):
    return min(a), max(a)
kichik, katta = min_max([4, 9, 1])
print(kichik, katta)
```
Natija:
```
1 9
```

## Ko'p uchraydigan xatolar
- `t[0] = 5` tuple'da → TypeError.
- `s = {}` deb bo'sh set yaratmoqchi bo'lish — bu dict.
- Set'dan indeks bilan olish: `s[0]` → TypeError.

## Chuqurroq
- Set'da `in` tekshiruvi juda tez (ro'yxatdan ko'ra) — katta ma'lumotda muhim.
- Tuple lug'at kaliti bo'la oladi: `{(41.3, 69.2): "Toshkent"}`; ro'yxat — yo'q.

## O'zingizni tekshiring
1. `{1, 2, 3} - {2, 5}`? ({1, 3})
2. `len({"a", "a", "b"})`? (2)
3. Bitta elementli tuple qanday yoziladi? ((5,))
""",
    "PY12": """
## Mavzu nima haqida
Lug'at (dict) — "kalit: qiymat" juftliklari. Ma'lumotni nom bilan saqlash: o'quvchi kartasi, narxlar ro'yxati, sozlamalar.

## Asosiy tushunchalar
- `d = {"ism": "Ali", "yosh": 14}`. Murojaat: `d["ism"]`.
- Yo'q kalit: `d["x"]` → **KeyError**; `d.get("x")` → None, `d.get("x", 0)` → 0.
- Qo'shish/o'zgartirish: `d["shahar"] = "Toshkent"`. O'chirish: `d.pop("ism")` (qiymatni qaytaradi), `del d["ism"]`.
- `keys()`, `values()`, `items()` — kalitlar, qiymatlar, juftliklar.
- `"yosh" in d` — **kalit** bormi.
- Kalit o'zgarmas tur bo'lishi kerak: str, int, tuple (list — yo'q).

## Bajarilgan misollar
### Misol 1. Asosiy amallar
```
d = {"ism": "Ali", "yosh": 14}
d["shahar"] = "Toshkent"
d["yosh"] = 15
print(d)
print(d.get("tel", "yo'q"), "yosh" in d, len(d))
```
Natija:
```
{'ism': 'Ali', 'yosh': 15, 'shahar': 'Toshkent'}
yo'q True 3
```

### Misol 2. Aylanib chiqish
```
narxlar = {"non": 4000, "sut": 12000, "tuxum": 1500}
for nom, narx in narxlar.items():
    print(f"{nom}: {narx} so'm")
print("Jami:", sum(narxlar.values()))
```
Natija:
```
non: 4000 so'm
sut: 12000 so'm
tuxum: 1500 so'm
Jami: 17500
```

### Misol 3. pop
```
d = {"a": 1, "b": 2}
x = d.pop("a")
print(x, d)
```
Natija:
```
1 {'b': 2}
```

### Misol 4. Lug'at bilan sanash
```
ovozlar = ["Ali", "Vali", "Ali", "Sami", "Ali"]
natija = {}
for ism in ovozlar:
    natija[ism] = natija.get(ism, 0) + 1
print(natija)
```
Natija:
```
{'Ali': 3, 'Vali': 1, 'Sami': 1}
```

## Ko'p uchraydigan xatolar
- `d["x"]` yo'q kalit uchun → KeyError; ishonchsiz bo'lsa `get`.
- Bir xil kalitni ikki marta yozish — oxirgisi qoladi: `{"a": 1, "a": 5}` → {'a': 5}.
- `in` qiymatni emas, kalitni tekshiradi: `14 in d` → False.

## Chuqurroq
- `d.update({"a": 10, "c": 3})` — bir nechtasini birdan qo'shish/yangilash.
- `setdefault(k, [])` — kalit yo'q bo'lsa boshlang'ich qiymat qo'yadi.
- Python 3.7+ da lug'at qo'shilish tartibini saqlaydi.

## O'zingizni tekshiring
1. `{"a": 1}.get("b", 5)`? (5)
2. `len({"a": 1, "b": 2, "c": 3})`? (3)
3. Lug'atdagi eng qimmat mahsulot nomini qanday topasiz? (`max(narxlar, key=narxlar.get)`)
""",
    "PY13": """
## Mavzu nima haqida
Real ma'lumot ko'pincha murakkab: ro'yxat ichida lug'atlar, lug'at ichida ro'yxatlar. Bunday tuzilmalar JSON'ga o'xshaydi va ilovalarda eng ko'p uchraydi.

## Asosiy tushunchalar
- **Ro'yxat ichida lug'at:** `[{"ism": "Ali", "ball": 90}, ...]` — har bir o'quvchi bitta lug'at.
- **Lug'at ichida ro'yxat/lug'at:** `{"guruh": {"oquvchilar": ["Ali", "Vali"]}}`.
- Murojaat **qadam-baqadam**: `data["guruh"]["oquvchilar"][0]`.
- 2 o'lchamli ro'yxat (matritsa): `m[qator][ustun]`.
- Saralash: `sorted(royxat, key=lambda x: x["ball"], reverse=True)`.

## Bajarilgan misollar
### Misol 1. O'quvchilar reytingi
```
oquvchilar = [
    {"ism": "Ali", "ball": 90},
    {"ism": "Vali", "ball": 75},
    {"ism": "Sami", "ball": 82},
]
reyting = sorted(oquvchilar, key=lambda x: x["ball"], reverse=True)
for i, o in enumerate(reyting[:2], start=1):
    print(i, o["ism"], o["ball"])
```
Natija:
```
1 Ali 90
2 Sami 82
```

### Misol 2. Chuqur murojaat
```
data = {"guruh": {"nomi": "P-1", "oquvchilar": ["Ali", "Vali"]}}
print(data["guruh"]["oquvchilar"][0])
data["guruh"]["xona"] = 5
print(data["guruh"]["xona"], len(data["guruh"]["oquvchilar"]))
```
Natija:
```
Ali
5 2
```

### Misol 3. Ombor qiymati
```
ombor = {
    "olma": {"narx": 5000, "soni": 10},
    "nok": {"narx": 8000, "soni": 4},
}
jami = 0
for nom, m in ombor.items():
    jami += m["narx"] * m["soni"]
print(jami)
```
Natija:
```
82000
```

### Misol 4. Matritsa
```
m = [[1, 2, 3], [4, 5, 6]]
print(m[1][0], len(m), len(m[0]), sum(m[0]) + sum(m[1]))
```
Natija:
```
4 2 3 21
```

## Ko'p uchraydigan xatolar
- Qatlamni o'tkazib yuborish: `data["oquvchilar"]` → KeyError (avval "guruh").
- `oquvchilar["ism"]` — ro'yxatga kalit bilan murojaat → TypeError; avval indeks: `oquvchilar[0]["ism"]`.

## Chuqurroq
- Murakkab ma'lumotni chiroyli ko'rish: `import json; print(json.dumps(data, indent=2, ensure_ascii=False))`.
- Guruhlash: `{guruh: [ism, ...]}` ko'rinishiga keltirish — hisobotlar uchun.

## O'zingizni tekshiring
1. `m = [[1, 2], [3, 4]]`: `m[0][1]`? (2)
2. Yuqoridagi ombor uchun `ombor["nok"]["soni"]`? (4)
3. Eng past ballni olgan o'quvchi ismini qanday topasiz? (`min(oquvchilar, key=lambda x: x["ball"])["ism"]`)
""",
    "PY14": """
## Mavzu nima haqida
`for` sikli — ketma-ketlikning (ro'yxat, satr, range) har bir elementi uchun bir xil amalni takrorlash. Takrorlanadigan ishni qo'lda 100 marta yozish shart emas.

## Asosiy tushunchalar
- `for x in royxat:` — har bir element navbat bilan `x` ga tushadi.
- `range(5)` → 0..4; `range(2, 6)` → 2..5; `range(0, 10, 3)` → 0, 3, 6, 9; `range(5, 0, -1)` → 5..1. **Oxiri kirmaydi.**
- `enumerate(a, start=1)` — indeks bilan birga.
- Yig'uvchi (akkumulyator) o'zgaruvchi: sikldan **oldin** 0 yoki 1 bilan boshlanadi.
- Ichma-ich sikl — jadval, matritsa uchun.

## Bajarilgan misollar
### Misol 1. range turlari
```
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(0, 10, 3)))
print(list(range(5, 0, -1)))
```
Natija:
```
[0, 1, 2, 3, 4]
[2, 3, 4, 5]
[0, 3, 6, 9]
[5, 4, 3, 2, 1]
```

### Misol 2. Yig'indi va ko'paytma
```
s = 0
p = 1
for i in range(1, 6):
    s += i
    p *= i
print(s, p)
```
Natija:
```
15 120
```

### Misol 3. enumerate
```
for i, meva in enumerate(["olma", "nok"], start=1):
    print(f"{i}. {meva}")
```
Natija:
```
1. olma
2. nok
```

### Misol 4. Ko'paytirish jadvali (3×3)
```
for i in range(1, 4):
    qator = ""
    for j in range(1, 4):
        qator += f"{i * j:4}"
    print(qator)
```
Natija:
```
   1   2   3
   2   4   6
   3   6   9
```

## Ko'p uchraydigan xatolar
- `range(1, 10)` 10 ni oladi deb o'ylash.
- Yig'uvchini sikl **ichida** 0 qilish — har aylanishda qayta nollanadi.
- Ko'paytma uchun 0 dan boshlash → natija doim 0.

## Chuqurroq
- Sikldan keyin o'zgaruvchi oxirgi qiymatda qoladi: `for i in range(3): pass` → i = 2.
- `for ... else:` — sikl `break`siz tugasa `else` bajariladi.
- Satr bo'ylab: `for harf in "abc":`.

## O'zingizni tekshiring
1. `list(range(1, 10, 4))`? ([1, 5, 9])
2. 1 dan 100 gacha juft sonlar yig'indisi? (`sum(range(2, 101, 2))` = 2550)
3. Ichma-ich sikl: tashqi 3, ichki 4 marta — ichki tana jami necha marta bajariladi? (12)
""",
    "PY15": """
## Mavzu nima haqida
`while` sikli — shart rost bo'lib turguncha takrorlaydi. Necha marta aylanishi oldindan noma'lum bo'lganda ishlatiladi: to'g'ri parol kiritilguncha, son topilguncha.

## Asosiy tushunchalar
- `while shart:` — har aylanishdan oldin shart tekshiriladi.
- Shartga ta'sir qiluvchi o'zgaruvchi **sikl ichida o'zgarishi** kerak, aks holda **cheksiz sikl**.
- `break` — sikldan darhol chiqish. `continue` — joriy aylanishning qolganini o'tkazib, keyingisiga o'tish. `pass` — "hech narsa qilma" (bo'sh blok uchun).
- `while True:` + `break` — menyu va o'yinlarning odatiy shakli.

## Bajarilgan misollar
### Misol 1. Oddiy sanash
```
i = 0
while i < 3:
    print("i =", i)
    i += 1
print("tugadi, i =", i)
```
Natija:
```
i = 0
i = 1
i = 2
tugadi, i = 3
```

### Misol 2. break va continue
```
for i in range(6):
    if i == 2:
        continue
    if i == 4:
        break
    print(i, end="")
print()
```
Natija:
```
013
```

### Misol 3. Raqamlar yig'indisi
```
n = 4728
s = 0
while n > 0:
    s += n % 10
    n //= 10
print(s)
```
Natija:
```
21
```

### Misol 4. Omonat o'sishi
```
summa = 1000000
yil = 0
while summa < 1500000:
    summa *= 1.2
    yil += 1
print(yil, round(summa))
```
Natija:
```
3 1728000
```

## Ko'p uchraydigan xatolar
- `i += 1` ni unutish → cheksiz sikl (dasturni Ctrl+C bilan to'xtatasiz).
- Shartni noto'g'ri yozish: `while i > 3` — boshidan yolg'on, sikl umuman ishlamaydi.
- `break` ni if'dan tashqariga qo'yish — sikl birinchi aylanishdayoq tugaydi.

## Chuqurroq
- "Sonni top" o'yini: `while True:` → so'rash → katta/kichik → to'g'ri bo'lsa `break`.
- `while` va `for`: soni ma'lum bo'lsa `for`, shartga bog'liq bo'lsa `while`.

## O'zingizni tekshiring
1. `n = 10; while n > 0: n -= 3` — sikldan keyin n? (-2)
2. 1 dan 5 gacha sonlar yig'indisini while bilan hisoblang. (15)
3. Cheksiz sikl qachon foydali?
""",
    "PY16": """
## Mavzu nima haqida
Sikllar + ro'yxat/lug'at = haqiqiy ma'lumot bilan ishlash: eng kattasini topish, saralash, filtrlash, sanash, ikki ro'yxatni juftlash.

## Asosiy tushunchalar
- Eng katta/kichikni qo'lda topish: birinchi elementdan boshlab solishtirish.
- Filtrlash: yangi ro'yxatga shartga moslarini yig'ish (yoki comprehension).
- Sanash: lug'at `{element: soni}` + `get(k, 0) + 1`.
- `zip(a, b)` — ikki ro'yxatni juftlab aylanish. `d.items()` — kalit va qiymat birga.
- Sikl ichida ro'yxatdan **o'chirmang** — elementlar siljib, ba'zilari o'tkazib yuboriladi.

## Bajarilgan misollar
### Misol 1. Eng kattasi
```
sonlar = [3, 8, 1, 6]
eng_katta = sonlar[0]
for s in sonlar:
    if s > eng_katta:
        eng_katta = s
print(eng_katta)
```
Natija:
```
8
```

### Misol 2. Harflarni sanash
```
matn = "olma"
sanoq = {}
for h in matn:
    sanoq[h] = sanoq.get(h, 0) + 1
print(sanoq)
```
Natija:
```
{'o': 1, 'l': 1, 'm': 1, 'a': 1}
```

### Misol 3. zip
```
ismlar = ["Ali", "Vali"]
ballar = [90, 80]
for ism, ball in zip(ismlar, ballar):
    print(ism, ball)
```
Natija:
```
Ali 90
Vali 80
```

### Misol 4. Filtrlash va sanash
```
ballar = [45, 78, 90, 55, 62]
otdi = [b for b in ballar if b >= 60]
print(otdi, len(otdi), sum(1 for b in ballar if b < 60))
```
Natija:
```
[78, 90, 62] 3 2
```

### Misol 5. O'chirishning to'g'ri usuli
```
a = [1, 2, 2, 3]
a = [x for x in a if x != 2]
print(a)
```
Natija:
```
[1, 3]
```

## Ko'p uchraydigan xatolar
- `for x in a: if x == 2: a.remove(x)` — ketma-ket ikkita 2 bo'lsa, biri qolib ketadi.
- `for k, v in d:` — `.items()` siz → xato.
- zip'da ro'yxatlar uzunligi har xil bo'lsa, qisqasi bo'yicha to'xtaydi.

## Chuqurroq
- `max(d, key=d.get)` — eng katta qiymatli kalit.
- `collections.Counter("olma")` — tayyor sanagich.

## O'zingizni tekshiring
1. `sum(1 for x in [3, 7, 9] if x > 5)`? (2)
2. Lug'atdagi qiymatlar yig'indisini sikl bilan hisoblang.
3. Nega sikl ichida ro'yxatdan o'chirish xavfli?
""",
    "PY17": '''
## Mavzu nima haqida
Funksiya — nom berilgan kod bloki. Bir marta yozib, ko'p marta chaqirasiz. Dastur tushunarli bo'laklarga bo'linadi, takrorlanish yo'qoladi.

## Asosiy tushunchalar
- E'lon: `def nom(parametrlar):`, tanasi chekinish bilan.
- **Parametr** — e'londagi nom; **argument** — chaqirishda berilgan qiymat.
- `return` — natijani qaytaradi va funksiyani **darhol tugatadi**. return bo'lmasa — `None`.
- `print` ekranga chiqaradi, `return` qiymatni qaytaradi — farqi katta!
- Bir nechta qiymat: `return a, b` (tuple).
- Nomli argumentlar: `f(b=2, a=10)`.

## Bajarilgan misollar
### Misol 1. Kvadrat
```
def kvadrat(x):
    return x * x
print(kvadrat(4), kvadrat(1.5))
```
Natija:
```
16 2.25
```

### Misol 2. print va return farqi
```
def a(x):
    print(x * 2)
def b(x):
    return x * 2
natija1 = a(5)
natija2 = b(5)
print(natija1, natija2)
```
Natija:
```
10
None 10
```

### Misol 3. Bir nechta qiymat
```
def statistika(baholar):
    return min(baholar), max(baholar), sum(baholar) / len(baholar)
kichik, katta, ortacha = statistika([3, 5, 4])
print(kichik, katta, ortacha)
```
Natija:
```
3 5 4.0
```

### Misol 4. Mantiqiy funksiya
```
def juftmi(n):
    return n % 2 == 0
print([n for n in range(1, 8) if juftmi(n)])
```
Natija:
```
[2, 4, 6]
```

## Ko'p uchraydigan xatolar
- Funksiyani chaqirmasdan e'lon qilish — hech narsa bo'lmaydi.
- return o'rniga print — natijani keyin ishlatib bo'lmaydi.
- Argument yetishmasa → TypeError: missing 1 required positional argument.
- `return` dan keyingi qatorlar hech qachon bajarilmaydi.

## Chuqurroq
- **Docstring:** funksiya boshidagi `"""..."""` — nima qilishini tushuntiradi; `help(nom)` uni ko'rsatadi.
- Funksiya boshqa funksiyani chaqira oladi; kichik, bitta ishni qiladigan funksiyalar yaxshi.

## O'zingizni tekshiring
1. `def f(): return 1; return 2` — `f()`? (1)
2. `def f(a, b): return a - b`; `f(b=3, a=10)`? (7)
3. Doira yuzini hisoblovchi funksiya yozing.
''',
    "PY18": """
## Mavzu nima haqida
Funksiyalarni moslashuvchan qilish: standart qiymatli parametrlar, istalgancha argument (`*args`, `**kwargs`) va o'zgaruvchining "ko'rinish doirasi" (scope).

## Asosiy tushunchalar
- **Default qiymat:** `def salom(ism="Mehmon")`. Default'li parametrlar **default'sizlardan keyin** yoziladi.
- `*args` — ortiqcha pozitsion argumentlar **tuple** bo'lib keladi.
- `**kwargs` — ortiqcha nomli argumentlar **dict** bo'lib keladi.
- **Scope:** funksiya ichida yaratilgan o'zgaruvchi — lokal, tashqarida ko'rinmaydi. Ichkarida tashqi o'zgaruvchini o'zgartirish uchun `global` (kam ishlating).

## Bajarilgan misollar
### Misol 1. Default qiymat
```
def salom(ism="Mehmon", til="uz"):
    return ("Salom, " if til == "uz" else "Привет, ") + ism
print(salom())
print(salom("Ali"))
print(salom("Ivan", til="ru"))
```
Natija:
```
Salom, Mehmon
Salom, Ali
Привет, Ivan
```

### Misol 2. *args
```
def yigindi(*sonlar):
    return sum(sonlar)
print(yigindi(1, 2, 3), yigindi(), yigindi(10))
```
Natija:
```
6 0 10
```

### Misol 3. **kwargs
```
def profil(ism, **qoshimcha):
    qatorlar = [f"Ism: {ism}"]
    for k, v in qoshimcha.items():
        qatorlar.append(f"{k}: {v}")
    return "\\n".join(qatorlar)
print(profil("Ali", yosh=14, shahar="Toshkent"))
```
Natija:
```
Ism: Ali
yosh: 14
shahar: Toshkent
```

### Misol 4. Scope
```
x = 5
def f():
    x = 10
    return x
print(f(), x)
```
Natija:
```
10 5
```

### Misol 5. Chegirma
```
def narx(summa, chegirma=10):
    return summa - summa * chegirma // 100
print(narx(1000), narx(1000, chegirma=20))
```
Natija:
```
900 800
```

## Ko'p uchraydigan xatolar
- `def f(a=1, b):` → SyntaxError (default'li parametr oldinda).
- O'zgaruvchan default: `def f(a=[])` — ro'yxat chaqiruvlar orasida "eslab qoladi". To'g'risi: `def f(a=None): a = a or []`.
- Funksiya ichida o'zgartirgan o'zgaruvchi tashqarida ham o'zgaradi deb o'ylash.

## Chuqurroq
- Argument ochish: `f(*[1, 2, 3])`, `f(**{"ism": "Ali"})`.
- Funksiyani boshqa funksiyaga argument qilib berish mumkin (keyingi mavzu: lambda, map).

## O'zingizni tekshiring
1. `def f(a, *b): return b`; `f(1, 2, 3)`? ((2, 3))
2. `def f(**k): return len(k)`; `f(x=1, y=2)`? (2)
3. Nega `global` dan kam foydalanish kerak?
""",
    "PY19": """
## Mavzu nima haqida
Lambda — kichik nomsiz funksiya. `map`, `filter`, `sorted`, `min`, `max` bilan birga ishlatilib, ma'lumotni qisqa va tushunarli qayta ishlash imkonini beradi.

## Asosiy tushunchalar
- `lambda x: x * 2` — `def f(x): return x * 2` ning qisqa shakli (faqat bitta ifoda).
- `map(f, a)` — har elementga f ni qo'llaydi; `filter(f, a)` — f rost qaytarganlarini qoldiradi. Ikkalasi ham **iterator** qaytaradi → `list()` ga o'rang.
- `sorted(a, key=...)`, `min/max(a, key=...)` — qaysi belgi bo'yicha solishtirish.
- `sum`, `len`, `any`, `all` — tayyor yordamchilar.

## Bajarilgan misollar
### Misol 1. map va filter
```
a = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, a)))
print(list(filter(lambda x: x > 2, a)))
print(list(map(int, ["1", "2", "3"])))
```
Natija:
```
[2, 4, 6, 8]
[3, 4]
[1, 2, 3]
```

### Misol 2. key bilan saralash
```
mevalar = ["olma", "nok", "uzum", "anor"]
print(sorted(mevalar, key=len))
print(max(mevalar, key=len), min(mevalar, key=len))
```
Natija:
```
['nok', 'olma', 'uzum', 'anor']
olma nok
```
Bir xil uzunlikdagilar o'z tartibini saqlaydi ("barqaror" saralash).

### Misol 3. Lug'atlar ro'yxati
```
talabalar = [{"ism": "Ali", "ball": 70}, {"ism": "Vali", "ball": 95}, {"ism": "Sami", "ball": 82}]
eng_yaxshi = max(talabalar, key=lambda t: t["ball"])
print(eng_yaxshi["ism"])
print([t["ism"] for t in sorted(talabalar, key=lambda t: t["ball"], reverse=True)])
```
Natija:
```
Vali
['Vali', 'Sami', 'Ali']
```

### Misol 4. any va all
```
ballar = [70, 85, 55]
print(any(b < 60 for b in ballar), all(b >= 50 for b in ballar))
```
Natija:
```
True True
```

## Ko'p uchraydigan xatolar
- `print(map(...))` → `<map object ...>`; `list()` ga o'rang.
- Lambda ichida bir nechta qator yozishga urinish — mumkin emas; murakkab bo'lsa `def`.
- `sorted(a, key=len())` — qavs bilan chaqirmang, funksiyaning o'zini bering: `key=len`.

## Chuqurroq
- Ko'p hollarda comprehension map/filter'dan o'qilishi osonroq: `[x * 2 for x in a]`.
- Bir nechta belgi bo'yicha: `key=lambda t: (-t["ball"], t["ism"])` — avval ball (kamayish), keyin ism.

## O'zingizni tekshiring
1. `list(map(lambda x: x ** 2, [1, 2, 3]))`? ([1, 4, 9])
2. `sorted([3, 1, 2], reverse=True)`? ([3, 2, 1])
3. Eng uzun so'zni topish: `max(sozlar, key=len)`.
""",
    "PY20": """
## Mavzu nima haqida
Modul — funksiya va o'zgaruvchilar saqlangan `.py` fayl. Python bilan birga yuzlab tayyor modullar keladi (standart kutubxona). `random` — tasodifiy sonlar: o'yinlar, test savollari, lotereya.

## Asosiy tushunchalar
- `import random` → `random.randint(1, 6)`.
- `from random import randint` → to'g'ridan-to'g'ri `randint(1, 6)`.
- `import random as r` → `r.randint(1, 6)` (qisqa nom).
- `randint(a, b)` — a dan b gacha butun son (**ikkalasi ham kiradi**).
- `random()` — [0.0, 1.0) oralig'idagi kasr son.
- `choice(a)` — ro'yxatdan bitta tasodifiy element. `sample(a, k)` — k ta **takrorlanmas**. `shuffle(a)` — ro'yxatni joyida aralashtiradi (None qaytaradi).
- `seed(42)` — har safar bir xil "tasodifiy" ketma-ketlik (test qilish uchun).

## Bajarilgan misollar
### Misol 1. Seed bilan takrorlanuvchi natija
```
import random
random.seed(1)
a = [random.randint(1, 6) for _ in range(5)]
random.seed(1)
b = [random.randint(1, 6) for _ in range(5)]
print(a == b, all(1 <= x <= 6 for x in a))
```
Natija:
```
True True
```

### Misol 2. sample — takrorlanmas
```
import random
sonlar = random.sample(range(1, 50), 6)
print(len(sonlar), len(set(sonlar)) == 6)
```
Natija:
```
6 True
```

### Misol 3. Zar tashlash statistikasi
```
import random
random.seed(7)
natija = {i: 0 for i in range(1, 7)}
for _ in range(6000):
    natija[random.randint(1, 6)] += 1
print(sum(natija.values()), all(800 < v < 1200 for v in natija.values()))
```
Natija:
```
6000 True
```
Har bir son ~1000 marta tushadi — tasodif "adolatli".

### Misol 4. Tosh-qog'oz-qaychi uchun tanlov
```
import random
tanlovlar = ["tosh", "qog'oz", "qaychi"]
kompyuter = random.choice(tanlovlar)
print(kompyuter in tanlovlar)
```
Natija:
```
True
```

## Ko'p uchraydigan xatolar
- Faylingizni `random.py` deb nomlash — Python sizning faylingizni import qiladi va `randint` topilmaydi!
- `a = random.shuffle(a)` → a None bo'ladi.
- `randint(1, 6)` 6 ni bermaydi deb o'ylash — beradi.

## Chuqurroq
- `dir(random)` — moduldagi hamma nomlar; `help(random.randint)` — yordam.
- Xavfsizlik uchun (parol, token) `random` emas, **`secrets`** moduli: `secrets.token_urlsafe(16)`.

## O'zingizni tekshiring
1. `from math import sqrt` dan keyin qanday chaqirasiz? (`sqrt(16)`)
2. `random.sample([1, 2, 3], 3)` — takror bo'lishi mumkinmi? (Yo'q)
3. Nega faylni `random.py` deb nomlash mumkin emas?
""",
    "PY21": """
## Mavzu nima haqida
`math` — matematik funksiyalar (ildiz, yaxlitlash, π, faktorial). `datetime` — sana va vaqt: bugungi sana, yosh hisoblash, muddatlar.

## Asosiy tushunchalar
- `math.sqrt(16)` → 4.0; `math.ceil(4.2)` → 5 (yuqoriga); `math.floor(4.8)` → 4 (pastga); `math.pi`; `math.pow(2, 3)` → 8.0; `math.factorial(5)` → 120.
- `from datetime import date, datetime, timedelta`.
- `date.today()` — bugun; `datetime.now()` — hozir (sana + vaqt).
- `date(2026, 10, 7)` — aniq sana; `.year`, `.month`, `.day`.
- `timedelta(days=7)` — muddat; sanaga qo'shish/ayirish.
- Ikki sana ayirmasi → `timedelta`; `.days` — kunlar soni.
- `strftime("%d.%m.%Y")` — sanani matnga; `strptime("07.10.2026", "%d.%m.%Y")` — matnni sanaga.

## Bajarilgan misollar
### Misol 1. math
```
import math
print(math.sqrt(16), math.ceil(4.2), math.floor(4.8), math.factorial(5))
print(round(math.pi, 4), math.pow(2, 3))
```
Natija:
```
4.0 5 4 120
3.1416 8.0
```

### Misol 2. Avtobuslar soni
45 o'quvchi, avtobusga 20 kishi sig'adi. Nechta avtobus kerak?
```
import math
print(math.ceil(45 / 20))
```
Natija:
```
3
```
`45 // 20` = 2 bo'lardi — 5 kishi qolib ketardi!

### Misol 3. Sana amallari
```
from datetime import date, timedelta
d = date(2026, 10, 7)
print(d.year, d.month, d.day)
print(d + timedelta(days=30))
print(d.strftime("%d.%m.%Y"))
print((date(2026, 12, 31) - d).days)
```
Natija:
```
2026 10 7
2026-11-06
07.10.2026
85
```

### Misol 4. Matndan sana
```
from datetime import datetime
s = datetime.strptime("19.10.2026 14:30", "%d.%m.%Y %H:%M")
print(s.hour, s.minute, s.strftime("%Y-%m-%d"))
```
Natija:
```
14 30 2026-10-19
```

## Ko'p uchraydigan xatolar
- `date.today() + 7` → TypeError; `timedelta(days=7)` kerak.
- `%m` (oy) va `%M` (daqiqa) ni adashtirish.
- `math.sqrt(-1)` → ValueError.

## Chuqurroq
- Yoshni aniq hisoblash: tug'ilgan kun bu yil o'tgan-o'tmaganini ham tekshirish kerak.
- `date.weekday()` — 0 = dushanba ... 6 = yakshanba.
- Vaqt zonalari: `zoneinfo.ZoneInfo("Asia/Tashkent")`.

## O'zingizni tekshiring
1. `math.ceil(7 / 2)`? (4)
2. `date(2026, 1, 31) + timedelta(days=1)`? (2026-02-01)
3. "2026-10-19" ko'rinishi uchun format? (`"%Y-%m-%d"`)
""",
    "PY22": """
## Mavzu nima haqida
RegEx (muntazam ifodalar) — matndan andoza bo'yicha qidirish: raqamlar, emaillar, telefonlar, sanalar. `re` moduli bilan ishlatiladi.

## Asosiy tushunchalar
- `re.findall(andoza, matn)` — hamma moslar ro'yxati.
- `re.search` — birinchi mos joy (yoki None); `re.fullmatch` — butun matn mosmi.
- `re.sub(andoza, yangi, matn)` — almashtirish.
- **Belgilar:** `\\d` raqam, `\\w` harf/raqam/_, `\\s` bo'sh joy, `.` istalgan belgi, `[abc]` biri, `[^abc]` bulardan boshqa.
- **Takror:** `+` 1+, `*` 0+, `?` 0 yoki 1, `{3}` aynan 3, `{2,4}` 2–4.
- `^` satr boshi, `$` oxiri. `( )` — guruh, `m.group(1)`.
- Andozalar `r"..."` bilan — teskari chiziq o'zgarmasin.

## Bajarilgan misollar
### Misol 1. Sonlarni ajratish
```
import re
print(re.findall(r"\\d+", "a12b3c456"))
print(sum(int(x) for x in re.findall(r"\\d+", "3 olma, 12 nok")))
```
Natija:
```
['12', '3', '456']
15
```

### Misol 2. Emaillar
```
import re
matn = "Bog'lanish: ali@gmail.com, info@minar.uz yoki 901234567"
print(re.findall(r"[\\w.]+@[\\w.]+\\.[a-z]{2,}", matn))
```
Natija:
```
['ali@gmail.com', 'info@minar.uz']
```

### Misol 3. Guruhlar
```
import re
m = re.search(r"(\\d{2})\\.(\\d{2})\\.(\\d{4})", "Imtihon: 25.12.2026 kuni")
kun, oy, yil = m.groups()
print(kun, oy, yil, m.group(0))
```
Natija:
```
25 12 2026 25.12.2026
```

### Misol 4. Tozalash
```
import re
print(re.sub(r"\\s+", " ", "Salom     dunyo  !"))
print(re.sub(r"\\d", "#", "Karta 8600 1234"))
```
Natija:
```
Salom dunyo !
Karta #### ####
```

## Ko'p uchraydigan xatolar
- `.` ni nuqta deb o'ylash — u "istalgan belgi"; nuqtaning o'zi `\\.`.
- `re.search` None qaytarsa `.group()` → AttributeError; avval `if m:` tekshiring.
- `r` siz yozish: `"\\d"` ishlaydi, lekin `"\\b"` (so'z chegarasi) "backspace" bo'lib qoladi.

## Chuqurroq
- `re.compile(andoza)` — ko'p ishlatiladigan andozani bir marta tayyorlash.
- `re.IGNORECASE` — katta-kichik harfga qaramay: `re.findall(r"python", matn, re.I)`.
- regex101.com — andozalarni sinab ko'rish uchun qulay sayt.

## O'zingizni tekshiring
1. `re.findall(r"[A-Z]", "SaLoM")`? (['S', 'L', 'M'])
2. O'zbek raqami `+998XXXXXXXXX` uchun andoza? (`r"\\+998\\d{9}"`)
3. `re.sub(r"a", "o", "banana")`? ('bonono')
""",
    "PY23": """
## Mavzu nima haqida
`os` moduli — operatsion tizim bilan ishlash: papkalar, fayllar ro'yxati, yo'llar. Shuningdek o'z modulingizni yaratib, kodni bir nechta faylga bo'lish.

## Asosiy tushunchalar
- `os.getcwd()` — joriy papka; `os.listdir(".")` — ichidagilar; `os.mkdir("yangi")`, `os.makedirs("a/b", exist_ok=True)`.
- `os.path.join("papka", "fayl.txt")` — tizimga mos yo'l (Windows'da `\\`, Linux'da `/`).
- `os.path.exists(p)`, `os.path.isfile(p)`, `os.path.getsize(p)`.
- Zamonaviy usul — `pathlib.Path`: `Path("papka") / "fayl.txt"`.
- **O'z modulingiz:** `utils.py` dagi funksiyani `main.py` da `from utils import qosh`.
- `if __name__ == "__main__":` — fayl to'g'ridan-to'g'ri ishga tushganda bajariladi, import qilinganda emas.
- `pip install nom` — tashqi kutubxona; `python -m venv .venv` — virtual muhit.

## Bajarilgan misollar
### Misol 1. Yo'llar bilan ishlash
```
import os
yol = os.path.join("hisobotlar", "2026", "oktabr.txt")
print(yol.replace("\\\\", "/"))
print(os.path.basename(yol), os.path.splitext(yol)[1])
```
Natija:
```
hisobotlar/2026/oktabr.txt
oktabr.txt .txt
```

### Misol 2. Papka yaratish va ro'yxat
```
import os
os.makedirs("loyiha/rasmlar", exist_ok=True)
open("loyiha/README.txt", "w").close()
print(sorted(os.listdir("loyiha")))
print(os.path.isdir("loyiha/rasmlar"), os.path.exists("loyiha/yoq.txt"))
```
Natija:
```
['README.txt', 'rasmlar']
True False
```

### Misol 3. O'z modulingiz
`utils.py`:
```
def qosh(a, b):
    return a + b

if __name__ == "__main__":
    print("utils to'g'ridan-to'g'ri ishga tushdi")
```
`main.py`:
```
from utils import qosh
print(qosh(2, 3))
```
`python main.py` → faqat `5` chiqadi (utils ichidagi print ishlamaydi, chunki u import qilingan).

## Ko'p uchraydigan xatolar
- Yo'lni `"papka" + "/" + "fayl"` bilan qo'lda yig'ish — Windows'da muammo; `os.path.join`.
- `os.mkdir` mavjud papkaga → FileExistsError; `makedirs(..., exist_ok=True)`.
- Modul fayli boshqa papkada bo'lsa import ishlamaydi — bir papkada saqlang.

## Chuqurroq
- `requirements.txt` — loyihaga kerakli kutubxonalar: `pip freeze > requirements.txt`, boshqa kompyuterda `pip install -r requirements.txt`.
- Virtual muhit har loyihaning kutubxonalarini alohida saqlaydi — versiyalar to'qnashmaydi.

## O'zingizni tekshiring
1. `os.path.splitext("rasm.png")`? (('rasm', '.png'))
2. `__name__ == "__main__"` qachon rost?
3. Virtual muhit qanday yaratiladi? (`python -m venv .venv`)
""",
    "PY24": """
## Mavzu nima haqida
Xatoliklar (exceptions) bilan ishlash — dastur kutilmagan holatda "qulab" tushmasligi uchun. Foydalanuvchi noto'g'ri ma'lumot kiritsa, xabar berib, qayta so'rash.

## Asosiy tushunchalar
- `try:` — xato bo'lishi mumkin bo'lgan kod.
- `except XatoTuri:` — o'sha xato bo'lsa bajariladi. Bir nechta: `except (ValueError, ZeroDivisionError):`.
- `except ValueError as e:` — xato xabari `e` da.
- `else:` — xato **bo'lmasa**. `finally:` — **har doim**.
- `raise ValueError("...")` — o'zingiz xato chiqarish.
- Ko'p uchraydigan turlar: ValueError, TypeError, ZeroDivisionError, KeyError, IndexError, FileNotFoundError.

## Bajarilgan misollar
### Misol 1. Nolga bo'lish
```
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Nolga bo'lish mumkin emas")
```
Natija:
```
Nolga bo'lish mumkin emas
```

### Misol 2. try / except / else / finally
```
for qiymat in ["5", "abc"]:
    try:
        x = int(qiymat)
    except ValueError as e:
        print("xato:", e)
    else:
        print("ok", x)
    finally:
        print("tekshirildi:", qiymat)
```
Natija:
```
ok 5
tekshirildi: 5
xato: invalid literal for int() with base 10: 'abc'
tekshirildi: abc
```

### Misol 3. Xavfsiz o'giruvchi funksiya
```
def songa(s, standart=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return standart
print(songa("12"), songa("x"), songa(None), songa("7", 1))
```
Natija:
```
12 0 0 7
```

### Misol 4. raise
```
def yosh_tekshir(y):
    if y < 0:
        raise ValueError("Yosh manfiy bo'lishi mumkin emas")
    return y
try:
    yosh_tekshir(-3)
except ValueError as e:
    print("Xabar:", e)
```
Natija:
```
Xabar: Yosh manfiy bo'lishi mumkin emas
```

## Ko'p uchraydigan xatolar
- Bo'sh `except:` — hamma xatoni, hatto dasturdagi xatolaringizni ham yashiradi.
- try ichiga juda ko'p kod qo'yish — qaysi qator xato bergani noaniq.
- Xatoni "yutib yuborish" (`except: pass`) — muammo yashirinib qoladi.

## Chuqurroq
- Qayta so'rash shabloni: `while True: try: n = int(input()); break; except ValueError: print("Son kiriting")`.
- O'z xato klassingiz: `class YetarliPulYoq(Exception): pass`.

## O'zingizni tekshiring
1. `int("3.5")` qaysi xato? (ValueError)
2. `[1, 2][5]`? (IndexError)
3. finally qachon bajariladi? (Har doim)
""",
    "PY25": """
## Mavzu nima haqida
Fayllar bilan ishlash — ma'lumotni dastur yopilgandan keyin ham saqlash: eslatmalar, hisobotlar, natijalar. Matnli (.txt) fayllarni o'qish va yozish.

## Asosiy tushunchalar
- `open(nom, rejim, encoding="utf-8")`. Rejimlar: `"r"` o'qish, `"w"` yozish (**eski mazmun o'chadi**), `"a"` oxiriga qo'shish, `"x"` faqat yangi fayl.
- `with open(...) as f:` — blok tugagach fayl **avtomatik yopiladi** (xato bo'lsa ham).
- O'qish: `f.read()` — hammasi bitta satr; `f.readlines()` — qatorlar ro'yxati; `for qator in f:` — qatorma-qator (eng tejamkor).
- Yozish: `f.write("matn\\n")` — yangi qatorni o'zingiz qo'shasiz.
- `qator.strip()` — oxiridagi `\\n` ni olib tashlaydi.
- Yo'q faylni "r" bilan ochish → **FileNotFoundError**.
- O'zbekcha harflar uchun **encoding="utf-8"**.

## Bajarilgan misollar
### Misol 1. Yozish va o'qish
```
with open("eslatma.txt", "w", encoding="utf-8") as f:
    f.write("Non olish\\n")
    f.write("Uy vazifasi\\n")
with open("eslatma.txt", encoding="utf-8") as f:
    print(f.read(), end="")
```
Natija:
```
Non olish
Uy vazifasi
```

### Misol 2. Qo'shish ("a")
```
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("1-kun\\n")
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("2-kun\\n")
with open("log.txt", encoding="utf-8") as f:
    print([q.strip() for q in f])
```
Natija:
```
['1-kun', '2-kun']
```

### Misol 3. Baholar faylidan o'rtacha
```
with open("baholar.txt", "w", encoding="utf-8") as f:
    f.write("Ali,90\\nVali,75\\nSami,82\\n")
jami, soni = 0, 0
with open("baholar.txt", encoding="utf-8") as f:
    for qator in f:
        ism, ball = qator.strip().split(",")
        jami += int(ball)
        soni += 1
print(round(jami / soni, 1))
```
Natija:
```
82.3
```

### Misol 4. Fayl yo'q bo'lsa
```
try:
    with open("yoq.txt", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("Fayl topilmadi — yangisini yaratamiz")
```
Natija:
```
Fayl topilmadi — yangisini yaratamiz
```

## Ko'p uchraydigan xatolar
- "w" bilan ochib, muhim faylni o'chirib yuborish — qo'shish uchun "a".
- `write(5)` → TypeError; faqat satr: `write(str(5))`.
- encoding ko'rsatmaslik — Windows'da o'zbekcha harflar buziladi.
- `with` siz ochib, `close()` ni unutish.

## Chuqurroq
- CSV uchun tayyor modul: `import csv` (`csv.reader`, `csv.DictWriter`).
- Katta fayllarni `read()` bilan emas, `for qator in f` bilan o'qing — xotira tejaladi.

## O'zingizni tekshiring
1. Faylning oxiriga yozish rejimi? ("a")
2. `"Ali,90\\n".strip().split(",")`? (['Ali', '90'])
3. Nega `with` ishlatish yaxshi?
""",
    "PY26": """
## Mavzu nima haqida
JSON — ma'lumot almashishning eng mashhur formati. Python lug'at va ro'yxatlarini faylga saqlab, keyin aynan o'sha ko'rinishda qayta yuklash mumkin. Botlar, saytlar, ilovalar shu formatda gaplashadi.

## Asosiy tushunchalar
- `import json`.
- `json.dumps(obj)` — Python → JSON **satr**; `json.loads(s)` — JSON satr → Python.
- `json.dump(obj, f)` — **faylga** yozish; `json.load(f)` — fayldan o'qish.
- `ensure_ascii=False` — o'zbekcha harflar `\\u` kodlarsiz saqlanadi; `indent=2` — chiroyli, o'qiladigan format.
- Moslik: dict ↔ object, list ↔ array, str ↔ string, True ↔ true, None ↔ null.
- JSON kalitlari **faqat satr**: `{1: "a"}` saqlansa, qayta yuklanganda `{"1": "a"}` bo'ladi.

## Bajarilgan misollar
### Misol 1. dumps / loads
```
import json
data = {"ism": "Ali", "baholar": [5, 4], "faol": True, "tel": None}
s = json.dumps(data, ensure_ascii=False)
print(s)
qayta = json.loads(s)
print(qayta["baholar"][0], qayta == data)
```
Natija:
```
{"ism": "Ali", "baholar": [5, 4], "faol": true, "tel": null}
5 True
```

### Misol 2. Faylga saqlash va yuklash
```
import json
oquvchilar = [{"ism": "Nigora", "ball": 95}, {"ism": "Sardor", "ball": 80}]
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(oquvchilar, f, ensure_ascii=False, indent=2)
with open("data.json", encoding="utf-8") as f:
    yuklangan = json.load(f)
print(len(yuklangan), yuklangan[0]["ism"])
```
Natija:
```
2 Nigora
```

### Misol 3. Kalitlar satrga aylanadi
```
import json
print(json.loads(json.dumps({1: "bir"})))
```
Natija:
```
{'1': 'bir'}
```

### Misol 4. Birinchi ishga tushirish
```
import json

def yukla(nom):
    try:
        with open(nom, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

print(yukla("hali_yoq.json"))
```
Natija:
```
[]
```

## Ko'p uchraydigan xatolar
- `dump` va `dumps` ni adashtirish (s — "string").
- Fayl bo'sh bo'lsa `json.load` → JSONDecodeError.
- set, datetime kabi turlarni to'g'ridan-to'g'ri saqlab bo'lmaydi → TypeError; avval list yoki str ga aylantiring.

## Chuqurroq
- `sort_keys=True` — kalitlarni alfavit bo'yicha yozadi (fayllarni solishtirish oson).
- Ma'lumot buzilmasligi uchun: avval vaqtinchalik faylga yozing, keyin `os.replace` bilan almashtiring.

## O'zingizni tekshiring
1. Python `False` JSON'da qanday? (false)
2. `json.dumps([1, None])`? ('[1, null]')
3. O'zbekcha harflar `\\u0` ko'rinishida chiqmasligi uchun nima qo'shasiz? (`ensure_ascii=False`)
""",
    "PY27": """
## Mavzu nima haqida
OOP (obyektga yo'naltirilgan dasturlash) — ma'lumot va unga tegishli amallarni bitta "obyekt"ga birlashtirish. Klass — chizma, obyekt — shu chizma bo'yicha yasalgan aniq narsa.

## Asosiy tushunchalar
- `class Mushuk:` — klass (nomi PascalCase).
- `__init__(self, ...)` — obyekt yaratilganda **avtomatik** chaqiriladi; atributlarni o'rnatadi.
- `self` — metod chaqirilayotgan obyektning o'zi. Har bir metodning birinchi parametri.
- **Atribut** — obyekt ma'lumoti (`self.ism`); **metod** — obyekt bajaradigan funksiya.
- Obyekt yaratish: `m = Mushuk("Momiq")`. Bitta klassdan istalgancha obyekt.

## Bajarilgan misollar
### Misol 1. Oddiy klass
```
class Mushuk:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh

    def ovoz(self):
        return f"{self.ism}: Miyov!"

m = Mushuk("Momiq", 2)
print(m.ism, m.yosh, m.ovoz())
```
Natija:
```
Momiq 2 Momiq: Miyov!
```

### Misol 2. Holatni o'zgartiruvchi metodlar
```
class Hisob:
    def __init__(self, egasi):
        self.egasi = egasi
        self.balans = 0

    def toldir(self, summa):
        self.balans += summa

    def yech(self, summa):
        if summa > self.balans:
            return "Mablag' yetarli emas"
        self.balans -= summa
        return "OK"

h = Hisob("Ali")
h.toldir(500)
h.toldir(300)
print(h.yech(1000), h.yech(200), h.balans)
```
Natija:
```
Mablag' yetarli emas OK 600
```

### Misol 3. Har bir obyekt — mustaqil
```
class Talaba:
    def __init__(self, ism):
        self.ism = ism
        self.baholar = []

    def baho_qosh(self, b):
        self.baholar.append(b)

    def ortacha(self):
        return sum(self.baholar) / len(self.baholar) if self.baholar else 0

a, b = Talaba("Ali"), Talaba("Vali")
a.baho_qosh(5)
a.baho_qosh(4)
print(a.ortacha(), b.ortacha(), len(b.baholar))
```
Natija:
```
4.5 0 0
```

## Ko'p uchraydigan xatolar
- Metodda `self` ni unutish: `def ovoz():` → chaqirganda TypeError.
- `self.` siz yozish: `balans += summa` → lokal o'zgaruvchi, atribut emas (UnboundLocalError).
- `Mushuk` (klass) va `Mushuk()` (obyekt) ni adashtirish.

## Chuqurroq
- **Klass atributi** — hamma obyekt uchun umumiy: `class Talaba: maktab = "Minar"`.
- OOP real dunyoni modellaydi: Kitob, Foydalanuvchi, Buyurtma — har biri klass.

## O'zingizni tekshiring
1. `__init__` qachon chaqiriladi?
2. Yuqoridagi `Hisob` da `h.yech(50)` balans 0 bo'lsa nima qaytaradi? ("Mablag' yetarli emas")
3. "Kitob" klassini yozing: nomi, muallifi, `malumot()` metodi.
""",
    "PY28": """
## Mavzu nima haqida
Vorislik (inheritance) — yangi klass mavjud klassning hamma narsasini "meros" qilib oladi va o'zinikini qo'shadi yoki o'zgartiradi. Polimorfizm — turli obyektlarning bir xil nomli metodi o'zicha ishlashi.

## Asosiy tushunchalar
- `class Kuchuk(Hayvon):` — Kuchuk Hayvon'dan voris.
- `super().__init__(...)` — ota klass `__init__` ini chaqirish.
- **Overriding** — voris klassda ota metodini qayta yozish.
- `isinstance(obj, Klass)` — obj shu klass yoki uning vorisi obyektimi.
- Polimorfizm: ro'yxatdagi turli obyektlarga bir xil `obj.ovoz()` — har biri o'z javobini beradi.

## Bajarilgan misollar
### Misol 1. Vorislik va super
```
class Hayvon:
    def __init__(self, ism):
        self.ism = ism

    def ovoz(self):
        return "..."

    def tanishtir(self):
        return f"Men {self.ism}: {self.ovoz()}"

class Mushuk(Hayvon):
    def ovoz(self):
        return "Miyov"

class Kuchuk(Hayvon):
    def __init__(self, ism, zoti):
        super().__init__(ism)
        self.zoti = zoti

    def ovoz(self):
        return "Vov"

for h in [Mushuk("Momiq"), Kuchuk("Bobik", "ovcharka"), Hayvon("Noma'lum")]:
    print(h.tanishtir())
```
Natija:
```
Men Momiq: Miyov
Men Bobik: Vov
Men Noma'lum: ...
```
`tanishtir` faqat ota klassda yozilgan, lekin har bir obyekt o'z `ovoz` ini chaqiradi — bu **polimorfizm**.

### Misol 2. Shakllar
```
class Shakl:
    def yuza(self):
        return 0

class Kvadrat(Shakl):
    def __init__(self, a):
        self.a = a

    def yuza(self):
        return self.a ** 2

class Tortburchak(Shakl):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def yuza(self):
        return self.a * self.b

shakllar = [Kvadrat(3), Tortburchak(2, 5), Shakl()]
print([s.yuza() for s in shakllar], sum(s.yuza() for s in shakllar))
```
Natija:
```
[9, 10, 0] 19
```

### Misol 3. isinstance
```
class Hayvon: pass
class Kuchuk(Hayvon): pass
k = Kuchuk()
print(isinstance(k, Kuchuk), isinstance(k, Hayvon), isinstance(Hayvon(), Kuchuk))
```
Natija:
```
True True False
```

## Ko'p uchraydigan xatolar
- Voris `__init__` yozib, `super().__init__` ni unutish — ota atributlari (masalan, `self.ism`) bo'lmaydi → AttributeError.
- Vorislikni "bor" munosabati uchun ishlatish: Mashina Dvigateldan voris emas, unda dvigatel **bor** (atribut).

## Chuqurroq
- **"is-a" qoidasi:** Kuchuk **bu** Hayvon → vorislik to'g'ri.
- Abstrakt klass: `from abc import ABC, abstractmethod` — vorislar metodni majburan yozishi uchun.

## O'zingizni tekshiring
1. `class B(A): pass` — B'da A'ning metodlari bormi? (Ha)
2. Voris klass ota metodini qayta yozishi nima deyiladi? (Overriding)
3. Doira klassini Shakl'dan voris qilib yozing (yuza = 3.14 × r²).
""",
    "PY29": """
## Mavzu nima haqida
Inkapsulyatsiya — obyekt ma'lumotini "himoyalash": tashqaridan noto'g'ri qiymat berilishiga yo'l qo'ymaslik. `property` va maxsus (dunder) metodlar obyektlarni Python'ning o'z turlaridek qulay qiladi.

## Asosiy tushunchalar
- `_balans` — "ichki" (kelishuv: tashqaridan tegmang). `__balans` — nomi o'zgartiriladi (name mangling), tashqaridan `obj.__balans` ishlamaydi.
- `@property` — metodni atribut kabi o'qish (qavssiz). `@narx.setter` — qiymat berishda tekshirish.
- Maxsus metodlar: `__str__` (print uchun chiroyli ko'rinish), `__repr__` (dasturchi uchun), `__len__` (len), `__eq__` (==), `__lt__` (<, sorted uchun), `__add__` (+).

## Bajarilgan misollar
### Misol 1. property va setter
```
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
            raise ValueError("Narx manfiy bo'lishi mumkin emas")
        self._narx = qiymat

m = Mahsulot("Non", 4000)
m.narx = 4500
print(m.narx)
try:
    m.narx = -10
except ValueError as e:
    print(e)
```
Natija:
```
4500
Narx manfiy bo'lishi mumkin emas
```

### Misol 2. __str__, __len__, __eq__
```
class Savat:
    def __init__(self, *mahsulotlar):
        self.items = list(mahsulotlar)

    def __str__(self):
        return "Savat: " + ", ".join(self.items)

    def __len__(self):
        return len(self.items)

    def __eq__(self, boshqa):
        return sorted(self.items) == sorted(boshqa.items)

a = Savat("non", "sut")
b = Savat("sut", "non")
print(a, len(a), a == b)
```
Natija:
```
Savat: non, sut 2 True
```

### Misol 3. sorted uchun __lt__
```
class Talaba:
    def __init__(self, ism, ball):
        self.ism, self.ball = ism, ball

    def __lt__(self, boshqa):
        return self.ball < boshqa.ball

    def __repr__(self):
        return f"Talaba({self.ism!r}, {self.ball})"

print(sorted([Talaba("Ali", 80), Talaba("Vali", 65), Talaba("Sami", 92)]))
```
Natija:
```
[Talaba('Vali', 65), Talaba('Ali', 80), Talaba('Sami', 92)]
```

## Ko'p uchraydigan xatolar
- property ichida `self.narx = ...` deb yozish — o'zini chaqirib, cheksiz rekursiya. Ichki nom boshqa bo'lsin (`self._narx`).
- `__str__` qaytarish o'rniga print qilish — `__str__` satr **qaytarishi** shart.

## Chuqurroq
- `__repr__` yaxshi yozilsa, debug paytida obyektni darhol tanib olasiz.
- `dataclasses.dataclass` — `__init__`, `__repr__`, `__eq__` ni avtomatik yozib beradi.

## O'zingizni tekshiring
1. `print(obj)` qaysi metodni chaqiradi? (`__str__`)
2. Nega setter'da tekshiruv kerak?
3. Pul klassiga `__add__` qo'shib, `Pul(5) + Pul(3)` ni ishlating.
""",
    "PY30": """
## Mavzu nima haqida
Birinchi to'liq loyiha: konsol o'yinlari ("Tosh-qog'oz-qaychi" va "Sonni top"). O'rganganlarning hammasi birga ishlaydi: funksiyalar, sikllar, shartlar, random, xatolarni ushlash, JSON.

## Asosiy tushunchalar
- **Tuzilma:** har bir o'yin — alohida funksiya; asosiy menyu — `while True` + `match`/`if`.
- **G'olibni aniqlash** — lug'at bilan: `yutadi = {"tosh": "qaychi", "qaychi": "qog'oz", "qog'oz": "tosh"}`.
- **Xavfsiz kiritish** — `try/except ValueError`, noto'g'ri bo'lsa qayta so'rash.
- **Natijalarni saqlash** — `scores.json`.

## Bajarilgan misollar
### Misol 1. G'olib funksiyasi (sinovdan o'tgan)
```
YUTADI = {"tosh": "qaychi", "qaychi": "qog'oz", "qog'oz": "tosh"}

def golib(a, b):
    if a == b:
        return "durang"
    return "a" if YUTADI[a] == b else "b"

print(golib("tosh", "qaychi"), golib("tosh", "qog'oz"), golib("qaychi", "qaychi"))
```
Natija:
```
a b durang
```

### Misol 2. Sonni top mantiqi (kiritishsiz sinov)
```
def maslahat(taxmin, yashirin):
    if taxmin < yashirin:
        return "Kattaroq son kiriting"
    if taxmin > yashirin:
        return "Kichikroq son kiriting"
    return "Topdingiz!"

yashirin = 70
for t in [40, 85, 70]:
    print(t, maslahat(t, yashirin))
```
Natija:
```
40 Kattaroq son kiriting
85 Kichikroq son kiriting
70 Topdingiz!
```

### Misol 3. To'liq o'yin sikli
```
import random

def son_top():
    yashirin = random.randint(1, 100)
    urinish = 0
    while True:
        try:
            taxmin = int(input("Son (1-100): "))
        except ValueError:
            print("Iltimos, son kiriting")
            continue
        urinish += 1
        javob = maslahat(taxmin, yashirin)
        print(javob)
        if javob == "Topdingiz!":
            return urinish
```
Mantiq (`maslahat`) alohida funksiyada — uni input'siz sinab ko'rish oson. Bu professional yondashuv.

### Misol 4. Eng yaxshi natijani saqlash
```
import json

def saqla(natijalar, nom="scores.json"):
    with open(nom, "w", encoding="utf-8") as f:
        json.dump(natijalar, f, ensure_ascii=False)

natijalar = {"galaba": 3, "maglubiyat": 1, "eng_kam_urinish": 5}
yangi_urinish = 4
natijalar["eng_kam_urinish"] = min(natijalar["eng_kam_urinish"], yangi_urinish)
saqla(natijalar)
print(natijalar["eng_kam_urinish"])
```
Natija:
```
4
```

## Ko'p uchraydigan xatolar
- Hammasini bitta uzun kodga yozish — xatoni topish qiyin.
- Foydalanuvchi "Tosh" (katta harf) yozsa — lug'atda topilmaydi; `.strip().lower()` qiling.
- Natijalarni faqat o'zgaruvchida saqlash — dastur yopilsa yo'qoladi.

## Chuqurroq
- **Rejalashtirish:** kod yozishdan oldin funksiyalar ro'yxatini tuzing: menyu(), tosh_qogoz(), son_top(), yukla(), saqla().
- O'yin mantiqini kiritish/chiqarishdan ajrating — shunda uni test qilish mumkin.

## O'zingizni tekshiring
1. `golib("qog'oz", "tosh")`? ("a")
2. Nega `maslahat` funksiyasini alohida yozish foydali?
3. Menyuga "2 — Natijalarni ko'rish" bandini qo'shing.
""",
    "PY31": """
## Mavzu nima haqida
Konsol boshqaruv tizimi — "mini ma'lumotlar bazasi": yozuvlarni qo'shish, ko'rish, tahrirlash, o'chirish (**CRUD**) va JSON faylda saqlash. Real dasturlarning (CRM, do'kon, kutubxona) asosi aynan shu.

## Asosiy tushunchalar
- **CRUD:** Create (qo'shish), Read (ko'rish/qidirish), Update (tahrirlash), Delete (o'chirish).
- **Modullar:** `storage.py` (JSON yuklash/saqlash), `models.py` (klass), `main.py` (menyu).
- Har bir yozuvga **takrorlanmas id** — ism bir xil bo'lsa ham adashmaslik uchun.
- Har bir o'zgarishdan keyin — **saqlash**.
- O'chirishdan oldin — **tasdiq so'rash**.

## Bajarilgan misollar
### Misol 1. Model va JSON o'girish
```
class Talaba:
    def __init__(self, id, ism, ball):
        self.id, self.ism, self.ball = id, ism, ball

    def to_dict(self):
        return {"id": self.id, "ism": self.ism, "ball": self.ball}

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["ism"], d["ball"])

t = Talaba(1, "Ali", 90)
d = t.to_dict()
print(d, Talaba.from_dict(d).ism)
```
Natija:
```
{'id': 1, 'ism': 'Ali', 'ball': 90} Ali
```

### Misol 2. CRUD funksiyalari
```
yozuvlar = []

def yangi_id():
    return max((y["id"] for y in yozuvlar), default=0) + 1

def qosh(ism, ball):
    yozuvlar.append({"id": yangi_id(), "ism": ism, "ball": ball})

def tahrirla(id, **ozgarish):
    for y in yozuvlar:
        if y["id"] == id:
            y.update(ozgarish)
            return True
    return False

def ochir(id):
    global yozuvlar
    oldin = len(yozuvlar)
    yozuvlar = [y for y in yozuvlar if y["id"] != id]
    return len(yozuvlar) < oldin

qosh("Ali", 90)
qosh("Vali", 70)
qosh("Sami", 85)
tahrirla(2, ball=75)
ochir(1)
print(yozuvlar)
```
Natija:
```
[{'id': 2, 'ism': 'Vali', 'ball': 75}, {'id': 3, 'ism': 'Sami', 'ball': 85}]
```

### Misol 3. Qidirish va saralash
```
yozuvlar = [{"ism": "Ali Valiyev", "narx": 50}, {"ism": "Vali Aliyev", "narx": 30}, {"ism": "Sami", "narx": 40}]
soz = "ali"
print([y["ism"] for y in yozuvlar if soz in y["ism"].lower()])
print([y["narx"] for y in sorted(yozuvlar, key=lambda y: y["narx"])])
```
Natija:
```
['Ali Valiyev', 'Vali Aliyev']
[30, 40, 50]
```

## Ko'p uchraydigan xatolar
- Indeks bo'yicha o'chirish (`del yozuvlar[2]`) — o'chirgandan keyin indekslar siljiydi; id ishlating.
- O'zgarishdan keyin saqlashni unutish — dastur yopilsa ish yo'qoladi.
- Noto'g'ri menyu raqami → dastur qulaydi; `else: print("Noto'g'ri tanlov")`.

## Chuqurroq
- `max(..., default=0)` — bo'sh ro'yxatda xato bermaydi.
- Keyingi qadam — haqiqiy ma'lumotlar bazasi: `sqlite3` (Python bilan birga keladi).

## O'zingizni tekshiring
1. CRUD harflarining ma'nosi?
2. Nega har bir yozuvga id kerak?
3. Narxi 40 dan qimmat yozuvlarni chiqaradigan qator yozing.
""",
    "PY32": """
## Mavzu nima haqida
Telegram bot — Python dasturi, Telegram orqali foydalanuvchilar bilan gaplashadi. Bu darsda bot yaratish (BotFather), token, birinchi buyruqlar va tugmalar.

## Asosiy tushunchalar
- **@BotFather** → `/newbot` → nom va username → **token** beradi.
- **Token maxfiy!** Kodga emas, muhit o'zgaruvchisiga yoki `.env` ga; GitHub'ga yuklamang.
- Kutubxona: `pip install pyTelegramBotAPI` → `import telebot`.
- `bot = telebot.TeleBot(TOKEN)`.
- **Handler** — xabarga javob beruvchi funksiya: `@bot.message_handler(commands=["start"])`.
- `bot.send_message(chat_id, "matn")`, `bot.reply_to(message, "matn")`.
- **ReplyKeyboardMarkup** — pastki menyu tugmalari.
- `bot.infinity_polling()` — bot Telegram'dan yangi xabarlarni muntazam so'rab turadi (polling).

## Bajarilgan misollar
### Misol 1. Eng oddiy bot
```
import os
import telebot

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, f"Salom, {message.from_user.first_name}!")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "Siz yozdingiz: " + message.text)

bot.infinity_polling()
```
Ishga tushirish: `BOT_TOKEN=123:ABC python bot.py` (Windows'da `set BOT_TOKEN=...`).

### Misol 2. Tugmalar
```
from telebot import types

@bot.message_handler(commands=["menu"])
def menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Tasodifiy fakt", "Yordam")
    bot.send_message(message.chat.id, "Tanlang:", reply_markup=kb)
```

### Misol 3. Tasodifiy fakt (mantiq alohida — sinab ko'rsa bo'ladi)
```
import random

FAKTLAR = ["Python 1991-yilda chiqqan", "Telegram'da 900 mln+ foydalanuvchi", "Eng mashhur til — Python"]

def fakt():
    return random.choice(FAKTLAR)

print(fakt() in FAKTLAR)
```
Natija:
```
True
```
Botda: `@bot.message_handler(func=lambda m: m.text == "Tasodifiy fakt")` → `bot.send_message(m.chat.id, fakt())`.

## Ko'p uchraydigan xatolar
- Tokenni kodga yozib GitHub'ga yuklash — boshqalar botingizni boshqaradi. Darhol BotFather'da `/revoke`.
- Handler tartibi: umumiy `func=lambda m: True` handler **eng oxirida** bo'lishi kerak, aks holda buyruqlarni "yutib yuboradi".
- `infinity_polling()` ni unutish — dastur darhol tugaydi.

## Chuqurroq
- `message.chat.id` — suhbat identifikatori; `message.from_user.id` — foydalanuvchi.
- Webhook — polling o'rniga Telegram o'zi serveringizga xabar yuboradi (katta botlar uchun).

## O'zingizni tekshiring
1. Token qayerdan olinadi? (@BotFather)
2. `/start` uchun handler qanday yoziladi?
3. Nega umumiy handler oxirida bo'lishi kerak?
""",
    "PY33": """
## Mavzu nima haqida
Yakuniy bot: inline tugmalar, foydalanuvchi holati (state), ma'lumotni JSON'da saqlash va xatolarga chidamlilik. Bot qayta ishga tushsa ham hech narsa yo'qolmasligi kerak.

## Asosiy tushunchalar
- **InlineKeyboardMarkup** — xabar ostidagi tugmalar; bosilganda `callback_data` keladi.
- `@bot.callback_query_handler(func=lambda c: True)` — tugma bosilishini ushlaydi; oxirida `bot.answer_callback_query(call.id)` ("soat" belgisi yo'qoladi).
- **Holat (state)** — foydalanuvchi qaysi bosqichda (masalan, "ism kutilmoqda"). Oddiy usul: `bot.register_next_step_handler(message, funksiya)`.
- **Saqlash** — `{user_id: {...}}` lug'ati JSON faylda; JSON kalitlari satr → `str(user_id)`.
- Handler ichidagi xavfli joylar — `try/except`.

## Bajarilgan misollar
### Misol 1. Foydalanuvchi ma'lumotlarini saqlash (sinab ko'rsa bo'ladi)
```
import json

def yukla(nom):
    try:
        with open(nom, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def saqla(data, nom):
    with open(nom, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users = yukla("users.json")
user_id = 123456789
users.setdefault(str(user_id), {"ism": None, "ball": 0})
users[str(user_id)]["ism"] = "Ali"
users[str(user_id)]["ball"] += 10
saqla(users, "users.json")
print(yukla("users.json"))
```
Natija:
```
{'123456789': {'ism': 'Ali', 'ball': 10}}
```

### Misol 2. Inline tugma va callback
```
from telebot import types

@bot.message_handler(commands=["savol"])
def savol(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("4", callback_data="javob:4"),
           types.InlineKeyboardButton("5", callback_data="javob:5"))
    bot.send_message(message.chat.id, "2 + 2 = ?", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("javob:"))
def javob(call):
    togri = call.data == "javob:4"
    bot.answer_callback_query(call.id, "To'g'ri!" if togri else "Xato")
```

### Misol 3. Ketma-ket so'rash (state)
```
@bot.message_handler(commands=["royxat"])
def royxat(message):
    msg = bot.send_message(message.chat.id, "Ismingiz?")
    bot.register_next_step_handler(msg, ism_olindi)

def ism_olindi(message):
    users[str(message.from_user.id)]["ism"] = message.text.strip()
    saqla(users, "users.json")
    bot.reply_to(message, "Saqlandi!")
```

## Ko'p uchraydigan xatolar
- `user_id` ni int kalit qilib saqlash — qayta yuklanganda "123" (satr) bo'ladi va topilmaydi.
- `answer_callback_query` ni chaqirmaslik — tugmada "yuklanmoqda" belgisi qoladi.
- Bitta xato butun botni to'xtatadi — handler ichida try/except va log.

## Chuqurroq
- Ko'p foydalanuvchili botda faylga bir vaqtda yozish muammo bo'lishi mumkin — keyingi bosqich `sqlite3`.
- `callback_data` 64 baytgacha — qisqa kodlar ishlating ("javob:4").

## O'zingizni tekshiring
1. Nega `str(user_id)`?
2. Inline va Reply klaviatura farqi?
3. Token yakuniy botda qayerda saqlanadi? (muhit o'zgaruvchisi / .env)
""",
    "PY34": """
## Mavzu nima haqida
Yakuniy loyiha himoyasi — siz yaratgan dasturni (Telegram bot yoki konsol tizimi) ko'rsatib, qanday ishlashini tushuntirasiz. Kod GitHub'da, README bilan, boshqa kompyuterda ishga tushadigan holatda bo'lishi kerak.

## Asosiy tushunchalar
- **GitHub repozitoriy:** kod + `README.md` + `requirements.txt` + `.gitignore`.
- **README:** loyiha nima qiladi, qanday o'rnatiladi va ishga tushiriladi, skrinshotlar.
- **.gitignore:** `.env`, `*.json` (shaxsiy ma'lumot), `.venv/`, `__pycache__/` — GitHub'ga tushmasin.
- **Git oqimi:** `git add .` → `git commit -m "..."` → `git push`.
- **Himoya:** 5 daqiqa demo + 3 daqiqa savol-javob.
- **Baholash:** ishlaydi va foydali — 40, kod sifati — 30, taqdimot — 20, GitHub va README — 10.

## Bajarilgan misollar
### Misol 1. README namunasi
```
# Kutubxona boti

Kitoblarni qidirish va band qilish uchun Telegram bot.

## Ishga tushirish
python -m venv .venv
.venv/bin/pip install -r requirements.txt
BOT_TOKEN=... python bot.py

## Imkoniyatlar
- /qidir — nomi bo'yicha qidirish
- /band — kitobni band qilish
```

### Misol 2. Boshqa kompyuterda ishga tushirish
```
git clone https://github.com/ali/kutubxona-bot.git
cd kutubxona-bot
python -m venv .venv
.venv/bin/pip install -r requirements.txt
python bot.py
```

### Misol 3. Kod sifati — oldin va keyin
Oldin: 300 qatorli bitta fayl, `a`, `b`, `x2` nomlari, xatolar ushlanmagan.
Keyin: `storage.py`, `handlers.py`, `bot.py`; nomlar: `kitob_qidir`, `band_qil`; har bir handler'da try/except; funksiyalar 20–30 qatordan oshmaydi.

### Misol 4. Demo rejasi (5 daqiqa)
1. Muammo (30 s): "Kutubxonada kitob borligini bilish uchun borish kerak."
2. Yechim (30 s): bot.
3. Jonli demo (3 daq): qidirish → band qilish → band qilinganlar ro'yxati.
4. Kod tuzilmasi (1 daq): qaysi fayl nima qiladi.

## Ko'p uchraydigan xatolar
- Demo paytida birinchi marta ishga tushirish — oldindan sinab ko'ring!
- Tokenni README yoki kodda qoldirish.
- Savolga "internetdan olganman" deb javob berish — har bir qatorni tushuntira oling.

## Chuqurroq
- Kichik, tez-tez commit qiling: "Qidirish qo'shildi", "Xatolar tuzatildi" — tarix tushunarli bo'ladi.
- Keyingi qadamlar: Django/FastAPI (veb), SQL, Git'da branch va pull request.

## O'zingizni tekshiring
1. `.gitignore` ga nimalar kiradi?
2. Boshqa kompyuterda loyihani ishga tushirish qadamlari?
3. Demo uchun 5 daqiqalik reja tuzing.
""",
}
