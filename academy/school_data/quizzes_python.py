"""Python kursi mavzulari bo'yicha test savollari (har bir mavzuga 12 ta).

Format — mavzu testi formasidagi bilan bir xil:
"?" — savol (keyingi qatorlar savol davomi yoki kod), "+" — to'g'ri javob, "-" — noto'g'ri javob.
Kalit — ``python.py`` dagi mavzu kaliti. Koddagi natijalar testlarda Python bilan tekshiriladi.
"""

QUIZZES = {
    "PY01": """
? Python qanday dasturlash tili?
+ Yuqori darajali, interpretatsiya qilinadigan, umumiy maqsadli til
- Faqat veb-sahifa bezash tili
- Faqat ma'lumotlar bazasi so'rovlari tili
- Faqat mobil o'yinlar tili

? Windows'da Python o'rnatishda qaysi belgini qo'yish muhim?
+ Add Python to PATH
- Install for all games
- Disable internet
- Add to Desktop only

? O'rnatilgan Python versiyasini terminalda qanday tekshirasiz?
+ python --version
- python --start
- version python
- pip version

? Python fayllari qaysi kengaytmaga ega?
+ .py
- .pt
- .txt
- .exe

? fayl.py dasturini terminalda qanday ishga tushirasiz?
+ python fayl.py
- run fayl.py
- open fayl.py
- start python

? Python'da bir qatorli izoh qaysi belgi bilan boshlanadi?
+ #
- //
- --
- /*

? Quyidagi kod nima chiqaradi?
print("Salom", "Dunyo", sep="-")
+ Salom-Dunyo
- Salom Dunyo
- Salom-Dunyo-
- SalomDunyo

? Quyidagi kod nima chiqaradi?
print("A", end="")
print("B")
+ AB
- A B
- A (keyingi qatorda) B
- B

? print("Ha" * 3) nima chiqaradi?
+ HaHaHa
- Ha3
- Ha Ha Ha
- Xato beradi

? Interaktiv rejimda (REPL) satr boshida qaysi belgi turadi?
+ >>>
- $$$
- ###
- :::

? print("Salom) qatori qanday xato beradi?
+ SyntaxError — qo'shtirnoq yopilmagan
- NameError
- ZeroDivisionError
- Xato bermaydi

? VS Code'da Python bilan qulay ishlash uchun nima o'rnatiladi?
+ Python kengaytmasi (extension)
- Photoshop
- Faqat yangi shrift
- Antivirus
""",
    "PY02": """
? Quyidagi o'zgaruvchi nomlaridan qaysi biri to'g'ri?
+ talaba_yoshi
- 2ism
- talaba-yoshi
- class

? type(3.14) natijasi qaysi?
+ <class 'float'>
- <class 'int'>
- <class 'str'>
- <class 'bool'>

? type("25") natijasi qaysi?
+ <class 'str'>
- <class 'int'>
- <class 'float'>
- <class 'bool'>

? bool turi qaysi qiymatlarni qabul qiladi?
+ True va False
- yes va no
- 1 va 2
- "ha" va "yo'q"

? Python'da o'zgaruvchilarni nomlashning tavsiya etilgan uslubi qaysi?
+ snake_case
- camelCase
- kebab-case
- HAMMASI_KATTA

? Quyidagi koddan keyin a va b qiymatlari qanday?
a = 5
b = 10
a, b = b, a
+ a = 10, b = 5
- a = 5, b = 10
- a = 10, b = 10
- Xato beradi

? Konstanta nomini qanday yozish odat tusiga kirgan?
+ KATTA_HARFLAR bilan: PI = 3.14159
- kichik harflar bilan: pi
- Raqam bilan boshlab: 1PI
- Bo'sh joy bilan: P I

? Python'da Ism va ism o'zgaruvchilari haqida qaysi gap to'g'ri?
+ Ular ikki xil o'zgaruvchi — Python katta-kichik harfni farqlaydi
- Ular bitta o'zgaruvchi
- Bunday nom berib bo'lmaydi
- Faqat birinchisi ishlaydi

? Quyidagi kod nima chiqaradi?
x = 7
x = "yetti"
print(type(x))
+ <class 'str'>
- <class 'int'>
- Xato beradi
- <class 'float'>

? Quyidagi kod nima chiqaradi?
r = 5
PI = 3.14
print(PI * r * r)
+ 78.5
- 31.4
- 15.7
- 78

? Bir qatorda uchta o'zgaruvchiga qiymat berishning to'g'ri usuli qaysi?
+ x, y, z = 1, 2, 3
- x = 1, y = 2, z = 3
- x y z = 1 2 3
- (x; y; z) = 1; 2; 3

? Quyidagilardan qaysi biri kalit so'z va o'zgaruvchi nomi bo'la olmaydi?
+ for
- son
- ism2
- _yosh
""",
    "PY03": """
? input() funksiyasi doim qanday turdagi qiymat qaytaradi?
+ str
- int
- float
- Kiritilgan qiymatga qarab har xil

? Quyidagi kod nima chiqaradi?
print(int("12") + 3)
+ 15
- 123
- "123"
- Xato beradi

? Quyidagi kod nima chiqaradi?
print("12" + "3")
+ 123
- 15
- 12 3
- Xato beradi

? int("3.5") qanday natija beradi?
+ ValueError xatosi
- 3
- 4
- 3.5

? int(3.9) natijasi qancha?
+ 3
- 4
- 3.9
- Xato beradi

? float("2.5") * 2 natijasi qancha?
+ 5.0
- 5
- 2.52.5
- Xato beradi

? str(10) + "5" natijasi qaysi?
+ "105"
- 15
- "15"
- Xato beradi

? bool("") va bool("0") natijalari qanday?
+ False va True
- True va False
- False va False
- True va True

? Foydalanuvchi kiritgan yoshni butun son sifatida olishning to'g'ri usuli qaysi?
+ yosh = int(input("Yoshingiz: "))
- yosh = input(int("Yoshingiz: "))
- yosh = int("Yoshingiz: ")
- yosh = input("Yoshingiz: ") + 0

? Quyidagi kod nima chiqaradi?
print("5" * 3)
+ 555
- 15
- 5 5 5
- Xato beradi

? print(5 + "5") qanday xato beradi?
+ TypeError
- ValueError
- NameError
- Xato bermaydi, 10 chiqadi

? round(3.567, 2) natijasi qancha?
+ 3.57
- 3.56
- 3.5
- 4
""",
    "PY04": """
? s = "Python" bo'lsa, s[0] nimaga teng?
+ "P"
- "y"
- "n"
- Xato beradi

? s = "Python" bo'lsa, s[-1] nimaga teng?
+ "n"
- "P"
- "o"
- Xato beradi

? "Python"[1:4] natijasi qaysi?
+ "yth"
- "Pyt"
- "ytho"
- "ython"

? "Python"[::-1] natijasi qaysi?
+ "nohtyP"
- "Python"
- "P"
- Xato beradi

? "salom dunyo".title() natijasi qaysi?
+ "Salom Dunyo"
- "Salom dunyo"
- "SALOM DUNYO"
- "salom Dunyo"

? "  matn  ".strip() nima qiladi?
+ Boshidagi va oxiridagi bo'sh joylarni olib tashlaydi
- Barcha harflarni kattalashtiradi
- Matnni teskari qiladi
- Faqat o'rtadagi bo'sh joylarni olib tashlaydi

? "olma,nok,uzum".split(",") natijasi qaysi?
+ ['olma', 'nok', 'uzum']
- "olma nok uzum"
- ('olma', 'nok', 'uzum')
- ['olma,nok,uzum']

? "banan".count("a") natijasi qancha?
+ 2
- 1
- 3
- 0

? Quyidagi kod nima chiqaradi?
ism = "Ali"
yosh = 14
print(f"{ism} {yosh} yoshda")
+ Ali 14 yoshda
- {ism} {yosh} yoshda
- ism yosh yoshda
- Xato beradi

? len("Salom!") natijasi qancha?
+ 6
- 5
- 7
- 1

? "kitob".replace("k", "K") natijasi qaysi?
+ "Kitob"
- "kitob"
- "KITOB"
- "Kitob K"

? s = "abc" bo'lsa, s[0] = "z" buyrug'i nima bo'ladi?
+ TypeError — satrlar o'zgarmas (immutable)
- s "zbc" ga aylanadi
- s "zabc" ga aylanadi
- Hech narsa bo'lmaydi
""",
    "PY05": """
? 7 / 2 natijasi qancha?
+ 3.5
- 3
- 4
- 1

? 7 // 2 natijasi qancha?
+ 3
- 3.5
- 4
- 1

? 7 % 2 natijasi qancha?
+ 1
- 3
- 3.5
- 0

? 2 ** 3 natijasi qancha?
+ 8
- 6
- 9
- 5

? 2 + 3 * 4 natijasi qancha?
+ 14
- 20
- 24
- 9

? (2 + 3) * 4 natijasi qancha?
+ 20
- 14
- 24
- 9

? Sonning juft ekanini qaysi ifoda bilan tekshirish mumkin?
+ son % 2 == 0
- son / 2 == 0
- son // 2 == 1
- son ** 2 == 0

? 10 / 5 natijasi qaysi?
+ 2.0
- 2
- "2"
- 5

? Quyidagi kod nima chiqaradi?
x = 10
x += 5
x *= 2
print(x)
+ 30
- 25
- 20
- 15

? 3725 sekundda nechta to'liq soat bor (qaysi ifoda to'g'ri)?
+ 3725 // 3600
- 3725 / 3600
- 3725 % 3600
- 3725 ** 3600

? 17 % 5 natijasi qancha?
+ 2
- 3
- 3.4
- 5

? 5 / 0 ifodasi qanday natija beradi?
+ ZeroDivisionError
- 0
- Cheksizlik (inf)
- None
""",
    "PY06": """
? 5 == 5.0 ifodasining natijasi qaysi?
+ True
- False
- Xato beradi
- None

? = va == operatorlarining farqi nima?
+ = qiymat beradi, == ikki qiymatni tengligini tekshiradi
- Ikkalasi bir xil
- == qiymat beradi, = tekshiradi
- = faqat satrlar uchun ishlatiladi

? True and False natijasi qaysi?
+ False
- True
- None
- Xato beradi

? True or False natijasi qaysi?
+ True
- False
- None
- Xato beradi

? not True natijasi qaysi?
+ False
- True
- 0
- Xato beradi

? 3 != 4 natijasi qaysi?
+ True
- False
- 1
- Xato beradi

? yosh = 15 bo'lsa, 13 <= yosh <= 17 natijasi qaysi?
+ True
- False
- Xato beradi
- 15

? "a" < "b" natijasi qaysi?
+ True
- False
- Xato beradi
- None

? Quyidagi kod nima chiqaradi?
x = 8
print(x > 5 and x < 10)
+ True
- False
- 8
- Xato beradi

? Mantiqiy operatorlarning bajarilish tartibi (birinchidan oxirgiga) qanday?
+ not, and, or
- or, and, not
- and, or, not
- Hammasi chapdan o'ngga bir xil

? not (5 > 3 or 2 > 10) natijasi qaysi?
+ False
- True
- None
- Xato beradi

? "Python" == "python" natijasi qaysi?
+ False
- True
- Xato beradi
- None
""",
    "PY07": """
? if operatoridan keyin qaysi belgi qo'yiladi?
+ : (ikki nuqta)
- ; (nuqtali vergul)
- {
- ->

? if blokining tanasi qanday belgilanadi?
+ Chekinish (indentatsiya), odatda 4 ta bo'sh joy
- Jingalak qavslar {}
- begin va end so'zlari
- Qatorni katta harf bilan boshlash

? Quyidagi kod nima chiqaradi?
x = 7
if x > 5:
    print("katta")
else:
    print("kichik")
+ katta
- kichik
- katta kichik
- Hech narsa chiqmaydi

? Quyidagi kod nima chiqaradi?
ball = 75
if ball >= 90:
    print("A")
elif ball >= 70:
    print("B")
else:
    print("C")
+ B
- A
- C
- A B

? elif nima uchun ishlatiladi?
+ Oldingi shart yolg'on bo'lsa, navbatdagi shartni tekshirish uchun
- Dasturni tugatish uchun
- Siklni boshlash uchun
- Funksiya e'lon qilish uchun

? Bitta if/elif/else zanjirida nechta blok bajariladi?
+ Faqat bittasi — birinchi rost shartli blok (yoki else)
- Rost bo'lgan barcha bloklar
- Har doim hammasi
- Har doim faqat else

? Quyidagi kod nima chiqaradi?
x = 0
if x:
    print("bor")
else:
    print("yo'q")
+ yo'q
- bor
- 0
- Xato beradi

? Quyidagi kodning qaysi qatorida xato bor?
if x > 5
    print(x)
+ Birinchi qatorda — ikki nuqta (:) yo'q
- Ikkinchi qatorda — print noto'g'ri
- Xato yo'q
- x e'lon qilinmagani uchun faqat ikkinchi qatorda

? else bloki shartsiz yoziladimi?
+ Ha, else'dan keyin shart yozilmaydi
- Yo'q, else'dan keyin ham shart yoziladi
- else faqat elif'dan oldin keladi
- else Python'da yo'q

? Quyidagi kod nima chiqaradi?
son = -3
if son > 0:
    print("musbat")
elif son < 0:
    print("manfiy")
else:
    print("nol")
+ manfiy
- musbat
- nol
- Xato beradi

? Qisqa shart ifodasi natijasi qanday?
x = 4
natija = "juft" if x % 2 == 0 else "toq"
+ "juft"
- "toq"
- True
- Xato beradi

? Kiritilgan son 1 dan 7 gacha bo'lsa, hafta kunini chiqaradigan dasturda qaysi tuzilma eng mos?
+ if / elif / else zanjiri
- Faqat bitta if
- Faqat else
- Shartsiz print'lar
""",
    "PY08": """
? Quyidagi kod nima chiqaradi?
x = 15
if x > 10:
    if x % 2 == 0:
        print("katta juft")
    else:
        print("katta toq")
+ katta toq
- katta juft
- Hech narsa
- Xato beradi

? Ichma-ich shartni qanday soddalashtirish mumkin?
if a > 0:
    if b > 0:
        print("ikkalasi musbat")
+ if a > 0 and b > 0:
- if a > 0 or b > 0:
- if not a > 0:
- Soddalashtirib bo'lmaydi

? match-case Python'ning qaysi versiyasidan boshlab bor?
+ 3.10
- 2.7
- 3.6
- 3.0

? Quyidagi kod nima chiqaradi?
tanlov = "2"
match tanlov:
    case "1":
        print("salom")
    case "2":
        print("sana")
    case _:
        print("noma'lum")
+ sana
- salom
- noma'lum
- Xato beradi

? match-case ichidagi case _ nimani bildiradi?
+ Boshqa hech bir case mos kelmasa bajariladigan holat
- Bo'sh qatorni tekshiradi
- Xato beradi
- Faqat raqamlarni tekshiradi

? RegEx bilan ishlash uchun qaysi modul import qilinadi?
+ re
- regex
- math
- os

? re.fullmatch(andoza, matn) qachon natija qaytaradi?
+ Butun matn andozaga to'liq mos kelsa
- Matn boshi mos kelsa
- Andoza matn ichida biror joyda uchrasa
- Har doim

? \\d andozasi nimani bildiradi?
+ Bitta raqam (0–9)
- Bitta harf
- Bo'sh joy
- Istalgan belgi

? "+998XXXXXXXXX" formatidagi telefon raqamini qaysi andoza to'g'ri tekshiradi?
+ r"\\+998\\d{9}"
- r"998\\d{7}"
- r"\\d+"
- r"[a-z]{9}"

? {9} kvantifikatori nimani bildiradi?
+ Oldingi element aynan 9 marta takrorlanadi
- 9 dan kam takrorlanadi
- 9-belgi
- 9 ta istalgan andoza

? Quyidagi kod nima chiqaradi?
import re
print(bool(re.fullmatch(r"\\d{3}", "12a")))
+ False
- True
- 12
- Xato beradi

? Parol kuchini tekshirishda katta harf borligini qaysi andoza aniqlaydi (re.search bilan)?
+ [A-Z]
- [a-z]
- \\d
- \\s
""",
    "PY09": """
? Bo'sh ro'yxat qanday yaratiladi?
+ []
- ()
- {}
- ""

? mevalar = ["olma", "nok", "uzum"] bo'lsa, mevalar[1] nimaga teng?
+ "nok"
- "olma"
- "uzum"
- Xato beradi

? mevalar = ["olma", "nok", "uzum"] bo'lsa, mevalar[-1] nimaga teng?
+ "uzum"
- "olma"
- "nok"
- Xato beradi

? a = [10, 20, 30, 40, 50] bo'lsa, a[1:3] nimaga teng?
+ [20, 30]
- [10, 20, 30]
- [20, 30, 40]
- [10, 20]

? a = [10, 20, 30, 40, 50] bo'lsa, a[:2] nimaga teng?
+ [10, 20]
- [10, 20, 30]
- [30, 40, 50]
- [20]

? a = [10, 20, 30, 40, 50] bo'lsa, a[::2] nimaga teng?
+ [10, 30, 50]
- [20, 40]
- [10, 20]
- [50, 30, 10]

? a = [1, 2, 3] bo'lsa, a[5] nima qaytaradi?
+ IndexError xatosi
- None
- 0
- 3

? len([4, 8, 15, 16]) natijasi qancha?
+ 4
- 3
- 43
- 16

? Ro'yxatdagi elementni qanday o'zgartirish mumkin?
+ a[0] = 100
- a(0) = 100
- a.0 = 100
- Ro'yxat elementini o'zgartirib bo'lmaydi

? Ro'yxatda turli turdagi elementlar bo'lishi mumkinmi?
+ Ha: [1, "ikki", 3.0, True]
- Yo'q, faqat bir xil turdagi
- Faqat sonlar bo'lishi mumkin
- Faqat satrlar bo'lishi mumkin

? 3 in [1, 2, 3] ifodasi natijasi qaysi?
+ True
- False
- 3
- 2

? [1, 2] + [3] natijasi qaysi?
+ [1, 2, 3]
- [4, 2]
- [1, 2, [3]]
- Xato beradi
""",
    "PY10": """
? Ro'yxat oxiriga element qo'shish metodi qaysi?
+ append()
- add()
- insert_end()
- push()

? a = [1, 2, 3]; a.insert(0, 9) dan keyin a nimaga teng?
+ [9, 1, 2, 3]
- [1, 2, 3, 9]
- [9, 2, 3]
- [1, 9, 2, 3]

? remove() metodi nima qiladi?
+ Berilgan qiymatning birinchi uchragan nusxasini o'chiradi
- Berilgan indeksdagi elementni o'chiradi
- Barcha elementlarni o'chiradi
- Ro'yxatni teskari qiladi

? a = [5, 6, 7]; x = a.pop() dan keyin x va a qanday?
+ x = 7, a = [5, 6]
- x = 5, a = [6, 7]
- x = [5, 6], a = 7
- Xato beradi

? a = [3, 1, 2]; a.sort() dan keyin a nimaga teng?
+ [1, 2, 3]
- [3, 2, 1]
- [3, 1, 2]
- None

? a.sort() va sorted(a) farqi nima?
+ sort() ro'yxatning o'zini o'zgartiradi, sorted() yangi ro'yxat qaytaradi
- Ikkalasi bir xil
- sorted() ro'yxatning o'zini o'zgartiradi
- sort() faqat satrlar uchun

? [1, 2, 3].index(3) natijasi qancha?
+ 2
- 3
- 1
- 0

? [x * 2 for x in [1, 2, 3]] natijasi qaysi?
+ [2, 4, 6]
- [1, 2, 3, 1, 2, 3]
- [1, 4, 9]
- 12

? [x for x in range(10) if x % 2 == 0] natijasi qaysi?
+ [0, 2, 4, 6, 8]
- [1, 3, 5, 7, 9]
- [2, 4, 6, 8, 10]
- [0, 1, 2, 3, 4]

? [1, 2, 2, 3].count(2) natijasi qancha?
+ 2
- 1
- 3
- 4

? a = [1, 2]; a.extend([3, 4]) dan keyin a nimaga teng?
+ [1, 2, 3, 4]
- [1, 2, [3, 4]]
- [3, 4]
- [4, 6]

? Quyidagi kod nima chiqaradi?
a = [1, 2, 3]
b = a
b.append(4)
print(a)
+ [1, 2, 3, 4]
- [1, 2, 3]
- [4]
- Xato beradi
""",
    "PY11": """
? Tuple qanday qavs bilan yoziladi?
+ ()
- []
- {}
- <>

? Tuple va list'ning asosiy farqi nima?
+ Tuple o'zgarmas (immutable), list o'zgaruvchan
- Tuple faqat sonlarni saqlaydi
- List o'zgarmas, tuple o'zgaruvchan
- Farqi yo'q

? t = (1, 2, 3) bo'lsa, t[0] = 5 buyrug'i nima bo'ladi?
+ TypeError — tuple'ni o'zgartirib bo'lmaydi
- t (5, 2, 3) ga aylanadi
- t (1, 2, 3, 5) ga aylanadi
- Hech narsa bo'lmaydi

? Bitta elementli tuple qanday yaratiladi?
+ (5,)
- (5)
- [5]
- {5}

? set (to'plam) ning asosiy xususiyati nima?
+ Elementlari takrorlanmaydi va tartiblanmagan
- Elementlari doim tartiblangan
- Faqat satrlarni saqlaydi
- Elementlari indeks bilan olinadi

? set([1, 2, 2, 3, 3, 3]) natijasi qaysi?
+ {1, 2, 3}
- [1, 2, 3]
- {1, 2, 2, 3, 3, 3}
- (1, 2, 3)

? Bo'sh set qanday yaratiladi?
+ set()
- {}
- []
- ()

? {1, 2, 3} & {2, 3, 4} natijasi qaysi?
+ {2, 3}
- {1, 2, 3, 4}
- {1, 4}
- {1}

? {1, 2} | {2, 3} natijasi qaysi?
+ {1, 2, 3}
- {2}
- {1, 3}
- {1, 2, 2, 3}

? {1, 2, 3} - {2} natijasi qaysi?
+ {1, 3}
- {2}
- {1, 2, 3}
- {-1, 0, 1}

? Set'ga element qo'shish metodi qaysi?
+ add()
- append()
- insert()
- push()

? Quyidagi kod nima chiqaradi?
x, y = (10, 20)
print(y)
+ 20
- 10
- (10, 20)
- Xato beradi
""",
    "PY12": """
? Lug'at (dict) qanday tuzilmaga ega?
+ Kalit: qiymat juftliklari
- Faqat tartiblangan qiymatlar ro'yxati
- Faqat takrorlanmas qiymatlar
- Faqat sonlar

? d = {"ism": "Ali", "yosh": 14} bo'lsa, d["ism"] nimaga teng?
+ "Ali"
- "ism"
- 14
- Xato beradi

? Lug'atda mavjud bo'lmagan kalitga d["x"] ko'rinishida murojaat qilinsa nima bo'ladi?
+ KeyError xatosi
- None qaytadi
- 0 qaytadi
- Yangi kalit yaratiladi

? d.get("x", 0) mavjud bo'lmagan kalit uchun nima qaytaradi?
+ 0
- KeyError
- "x"
- False

? Lug'atga yangi juftlik qanday qo'shiladi?
+ d["shahar"] = "Toshkent"
- d.append("shahar", "Toshkent")
- d.add("shahar": "Toshkent")
- d + {"shahar": "Toshkent"}

? d.keys() nimani qaytaradi?
+ Lug'atning barcha kalitlarini
- Barcha qiymatlarni
- Juftliklar sonini
- Birinchi kalitni

? d.items() nimani qaytaradi?
+ (kalit, qiymat) juftliklarini
- Faqat kalitlarni
- Faqat qiymatlarni
- Lug'atning nusxasini

? Lug'at kaliti bo'la oladigan qiymat qaysi?
+ "ism" (satr)
- [1, 2] (ro'yxat)
- {"a": 1} (lug'at)
- {1, 2} (to'plam)

? Quyidagi kod nima chiqaradi?
d = {"a": 1}
d["a"] = 5
print(d)
+ {'a': 5}
- {'a': 1, 'a': 5}
- {'a': 1}
- Xato beradi

? "yosh" in {"ism": "Ali", "yosh": 14} natijasi qaysi?
+ True
- False
- 14
- Xato beradi

? d.pop("ism") nima qiladi?
+ "ism" kalitini o'chiradi va uning qiymatini qaytaradi
- Barcha kalitlarni o'chiradi
- Faqat qiymatni None qiladi
- Oxirgi juftlikni qo'shadi

? len({"a": 1, "b": 2, "c": 3}) natijasi qancha?
+ 3
- 6
- 2
- 1
""",
    "PY13": """
? oquvchilar = [{"ism": "Ali", "ball": 90}, {"ism": "Vali", "ball": 75}] bo'lsa, oquvchilar[1]["ism"] nimaga teng?
+ "Vali"
- "Ali"
- 75
- Xato beradi

? data = {"guruh": {"oquvchilar": ["Ali", "Vali"]}} bo'lsa, Ali'ni qanday olish mumkin?
+ data["guruh"]["oquvchilar"][0]
- data["oquvchilar"][0]
- data[0]["guruh"]
- data.guruh.oquvchilar[0]

? m = [[1, 2], [3, 4]] bo'lsa, m[1][0] nimaga teng?
+ 3
- 2
- 1
- 4

? Quyidagi kod nima chiqaradi?
m = [[1, 2], [3, 4]]
print(len(m))
+ 2
- 4
- 1
- Xato beradi

? Ro'yxatdagi lug'atlarni "ball" bo'yicha kamayish tartibida saralash qaysi?
+ sorted(oquvchilar, key=lambda x: x["ball"], reverse=True)
- sorted(oquvchilar, key="ball")
- oquvchilar.sort("ball")
- sorted(oquvchilar["ball"])

? Saralangan ro'yxatdan eng yaxshi 3 talikni qanday olish mumkin?
+ reyting[:3]
- reyting[3]
- reyting[-3]
- reyting[3:]

? ombor = {"olma": {"narx": 5000, "soni": 10}} bo'lsa, olmaning umumiy qiymati qanday hisoblanadi?
+ ombor["olma"]["narx"] * ombor["olma"]["soni"]
- ombor["narx"] * ombor["soni"]
- ombor["olma"] * 10
- ombor.olma.narx * 10

? Quyidagi kod nima chiqaradi?
guruhlar = {"A": ["Ali", "Vali"], "B": ["Sami"]}
print(len(guruhlar["A"]))
+ 2
- 3
- 1
- Xato beradi

? Ichma-ich lug'atga yangi qiymat qo'shish to'g'ri usuli qaysi?
+ data["guruh"]["xona"] = 5
- data["guruh"].append("xona", 5)
- data.guruh.xona = 5
- data["xona"]["guruh"] = 5

? Quyidagi kod nima chiqaradi?
m = [[1, 2], [3, 4]]
print(sum(m[0]) + sum(m[1]))
+ 10
- 4
- [4, 6]
- Xato beradi

? JSON'ga o'xshash ma'lumot nima uchun qulay?
+ Real hayotdagi murakkab ma'lumotni tushunarli tuzilmada saqlaydi
- Faqat sonlarni saqlaydi
- Xotirada joy egallamaydi
- Faqat bitta qiymat saqlaydi

? Quyidagi kod nima chiqaradi?
data = {"a": [1, {"b": 2}]}
print(data["a"][1]["b"])
+ 2
- 1
- {'b': 2}
- Xato beradi
""",
    "PY14": """
? range(5) qaysi sonlarni hosil qiladi?
+ 0, 1, 2, 3, 4
- 1, 2, 3, 4, 5
- 0, 1, 2, 3, 4, 5
- 5

? range(2, 6) qaysi sonlarni hosil qiladi?
+ 2, 3, 4, 5
- 2, 3, 4, 5, 6
- 3, 4, 5, 6
- 2, 6

? range(0, 10, 3) qaysi sonlarni hosil qiladi?
+ 0, 3, 6, 9
- 0, 3, 6, 9, 12
- 3, 6, 9
- 0, 10, 3

? range(5, 0, -1) qaysi sonlarni hosil qiladi?
+ 5, 4, 3, 2, 1
- 5, 4, 3, 2, 1, 0
- 0, 1, 2, 3, 4
- Hech narsa

? Quyidagi kod nima chiqaradi?
s = 0
for i in range(1, 4):
    s += i
print(s)
+ 6
- 10
- 3
- 4

? Quyidagi kod necha marta "Salom" chiqaradi?
for i in range(3):
    print("Salom")
+ 3
- 2
- 4
- 1

? Quyidagi kod nima chiqaradi?
for harf in "abc":
    print(harf, end="")
+ abc
- a b c
- cba
- Xato beradi

? Ro'yxat elementlarini indeksi bilan birga aylanish uchun qaysi funksiya qulay?
+ enumerate()
- range()
- zip()
- len()

? Quyidagi kod nima chiqaradi?
for i in range(3):
    pass
print(i)
+ 2
- 3
- 0
- Xato beradi

? Ko'paytirish jadvali uchun qanday sikl kerak?
+ Ichma-ich (nested) for sikli
- Bitta while sikli, shartsiz
- Faqat if
- Sikl kerak emas

? Quyidagi kod nima chiqaradi?
n = 1
for i in range(1, 5):
    n *= i
print(n)
+ 24
- 10
- 120
- 4

? for sikli qachon tugaydi?
+ Ketma-ketlikdagi barcha elementlar aylanib chiqilganda (yoki break bo'lsa)
- Faqat break bo'lganda
- Hech qachon
- Faqat shart False bo'lganda
""",
    "PY15": """
? while sikli qachon ishlaydi?
+ Shart True bo'lib turgan paytda
- Aniq 10 marta
- Faqat bir marta
- Shart False bo'lganda

? Quyidagi kod nima chiqaradi?
i = 0
while i < 3:
    print(i, end=" ")
    i += 1
+ 0 1 2
- 0 1 2 3
- 1 2 3
- Cheksiz sikl

? Quyidagi kodda nima bo'ladi?
i = 0
while i < 3:
    print(i)
+ Cheksiz sikl — i o'zgarmaydi
- 0 1 2 chiqadi
- Hech narsa chiqmaydi
- Xato beradi

? break operatori nima qiladi?
+ Sikldan darhol chiqadi
- Keyingi iteratsiyaga o'tadi
- Hech narsa qilmaydi
- Dasturni qayta boshlaydi

? continue operatori nima qiladi?
+ Joriy iteratsiyaning qolgan qismini o'tkazib, keyingisiga o'tadi
- Sikldan chiqadi
- Dasturni to'xtatadi
- Siklni boshidan boshlaydi

? pass operatori nima uchun kerak?
+ Sintaktik jihatdan blok kerak, lekin hech narsa qilinmasligi kerak bo'lganda
- Sikldan chiqish uchun
- Xatoni ushlash uchun
- Keyingi iteratsiyaga o'tish uchun

? Quyidagi kod nima chiqaradi?
for i in range(5):
    if i == 3:
        break
    print(i, end="")
+ 012
- 0123
- 01234
- 3

? Quyidagi kod nima chiqaradi?
for i in range(5):
    if i == 2:
        continue
    print(i, end="")
+ 0134
- 01234
- 01
- 2

? while True: sikli qanday to'xtatiladi?
+ Sikl ichida break bilan
- Faqat kompyuterni o'chirib
- continue bilan
- To'xtatib bo'lmaydi

? "Sonni top" o'yinida foydalanuvchi to'g'ri topguncha so'rash uchun qaysi sikl mos?
+ while
- for i in range(1)
- Sikl kerak emas
- Faqat if

? Quyidagi kod nima chiqaradi?
n = 10
while n > 0:
    n -= 3
print(n)
+ -2
- 0
- 1
- -3

? Quyidagi kod nima chiqaradi?
s = 0
n = 1
while n <= 5:
    s += n
    n += 1
print(s)
+ 15
- 10
- 5
- 21
""",
    "PY16": """
? Quyidagi kod nima chiqaradi?
sonlar = [3, 8, 1, 6]
eng_katta = sonlar[0]
for s in sonlar:
    if s > eng_katta:
        eng_katta = s
print(eng_katta)
+ 8
- 3
- 6
- 1

? Lug'atning kalit va qiymatlarini birga aylanish uchun nima ishlatiladi?
+ for k, v in d.items():
- for k, v in d:
- for k in d.values():
- for d in k, v:

? Quyidagi kod nima chiqaradi?
d = {"a": 1, "b": 2}
for k in d:
    print(k, end="")
+ ab
- 12
- a1b2
- Xato beradi

? Ro'yxatdagi juft sonlarni yangi ro'yxatga yig'ishning to'g'ri usuli qaysi?
+ juftlar = [s for s in sonlar if s % 2 == 0]
- juftlar = sonlar % 2
- juftlar = sonlar.even()
- juftlar = [sonlar if s % 2]

? Matndagi har bir harf sonini sanash uchun qanday tuzilma mos?
+ Lug'at: {harf: soni}
- Faqat bitta int o'zgaruvchi
- Tuple
- Bo'sh satr

? Quyidagi kod nima chiqaradi?
matn = "olma"
sanoq = {}
for h in matn:
    sanoq[h] = sanoq.get(h, 0) + 1
print(sanoq["o"])
+ 1
- 0
- 4
- Xato beradi

? Siklda ro'yxatni aylanayotganda undan element o'chirish nima uchun xavfli?
+ Elementlar siljiydi va ba'zilari o'tkazib yuboriladi
- Python bunga umuman ruxsat bermaydi
- Ro'yxat avtomatik saralanadi
- Hech qanday xavfi yo'q

? Ikki ro'yxatni juftlab aylanish uchun qaysi funksiya ishlatiladi?
+ zip()
- enumerate()
- map()
- range()

? Quyidagi kod nima chiqaradi?
ismlar = ["Ali", "Vali"]
ballar = [90, 80]
for i, b in zip(ismlar, ballar):
    print(i, b)
+ Ali 90 va keyingi qatorda Vali 80
- Ali Vali 90 80
- (Ali, Vali) (90, 80)
- Xato beradi

? Quyidagi kod nima chiqaradi?
narxlar = {"non": 4000, "sut": 12000}
jami = 0
for v in narxlar.values():
    jami += v
print(jami)
+ 16000
- 4000
- 12000
- 2

? Quyidagi kod nima chiqaradi?
for i, x in enumerate(["a", "b"], start=1):
    print(i, x)
+ 1 a va keyingi qatorda 2 b
- 0 a va keyingi qatorda 1 b
- a 1 va keyingi qatorda b 2
- Xato beradi

? Ballari 60 dan yuqori o'quvchilar sonini topishning to'g'ri usuli qaysi?
+ sum(1 for b in ballar if b > 60)
- len(ballar > 60)
- ballar.count(> 60)
- max(ballar) > 60
""",
    "PY17": """
? Python'da funksiya qaysi kalit so'z bilan e'lon qilinadi?
+ def
- function
- func
- define

? Quyidagi kod nima chiqaradi?
def kvadrat(x):
    return x * x
print(kvadrat(4))
+ 16
- 8
- 4
- None

? return yozilmagan funksiya nima qaytaradi?
+ None
- 0
- Bo'sh satr
- Xato beradi

? Parametr va argument farqi nima?
+ Parametr — funksiya e'lonidagi nom, argument — chaqirishda berilgan qiymat
- Ikkalasi bir xil
- Argument — funksiya nomi
- Parametr — funksiya natijasi

? Quyidagi kod nima chiqaradi?
def salom(ism):
    print("Salom,", ism)
salom("Ali")
+ Salom, Ali
- Salom,Ali
- salom Ali
- Xato beradi

? Funksiyadan bir nechta qiymat qanday qaytariladi?
+ return a, b — tuple sifatida qaytadi
- Faqat bitta qiymat qaytarish mumkin
- return a; return b
- print(a, b)

? Quyidagi kod nima chiqaradi?
def f(a, b):
    return a - b
print(f(b=2, a=10))
+ 8
- -8
- 12
- Xato beradi

? return'dan keyingi qatorlar bajariladimi?
+ Yo'q, return funksiyani darhol tugatadi
- Ha, har doim
- Faqat print bo'lsa
- Faqat sikl ichida

? Funksiyalarning asosiy foydasi nima?
+ Kodni qayta ishlatish va dasturni tushunarli qismlarga ajratish
- Dastur tezligini 10 baravar oshiradi
- O'zgaruvchilar kerak bo'lmaydi
- Xatolar umuman bo'lmaydi

? Quyidagi kod nima chiqaradi?
def juftmi(n):
    return n % 2 == 0
print(juftmi(7))
+ False
- True
- 1
- None

? Funksiyani chaqirishda argumentlar soni parametrlardan kam bo'lsa (default'siz) nima bo'ladi?
+ TypeError xatosi
- Yetishmagan parametr None bo'ladi
- Yetishmagan parametr 0 bo'ladi
- Funksiya chaqirilmaydi, xato ham bo'lmaydi

? Quyidagi kod nima chiqaradi?
def f():
    return 1
    return 2
print(f())
+ 1
- 2
- (1, 2)
- None
""",
    "PY18": """
? Quyidagi kod nima chiqaradi?
def salom(ism="Mehmon"):
    return "Salom, " + ism
print(salom())
+ Salom, Mehmon
- Salom,
- Salom, ism
- Xato beradi

? *args parametri funksiyada qanday ko'rinishda keladi?
+ tuple
- list
- dict
- set

? **kwargs parametri funksiyada qanday ko'rinishda keladi?
+ dict
- tuple
- list
- str

? Quyidagi kod nima chiqaradi?
def yigindi(*args):
    return sum(args)
print(yigindi(1, 2, 3))
+ 6
- (1, 2, 3)
- 123
- Xato beradi

? Quyidagi kod nima chiqaradi?
def info(**kwargs):
    return len(kwargs)
print(info(ism="Ali", yosh=14))
+ 2
- 1
- 4
- Xato beradi

? Funksiya ichida yaratilgan o'zgaruvchi qayerda ko'rinadi?
+ Faqat shu funksiya ichida (lokal)
- Butun dasturda
- Boshqa fayllarda ham
- Hech qayerda

? Quyidagi kod nima chiqaradi?
x = 5
def f():
    x = 10
f()
print(x)
+ 5
- 10
- None
- Xato beradi

? Funksiya ichidan global o'zgaruvchini o'zgartirish uchun qaysi kalit so'z ishlatiladi?
+ global
- nonlocal
- static
- public

? Default qiymatli parametrlar qayerda yozilishi kerak?
+ Default qiymatsiz parametrlardan keyin
- Default qiymatsizlardan oldin
- Istalgan joyda
- Faqat birinchi o'rinda

? def f(a, b=2, *args, **kwargs) e'lonida f(1) chaqirilsa, b nimaga teng?
+ 2
- 1
- None
- Xato beradi

? Quyidagi kod nima chiqaradi?
def f(a, *args):
    return args
print(f(1, 2, 3))
+ (2, 3)
- (1, 2, 3)
- [2, 3]
- 1

? Quyidagi kod nima chiqaradi?
def narx(summa, chegirma=10):
    return summa - summa * chegirma // 100
print(narx(1000, chegirma=20))
+ 800
- 900
- 980
- 1000
""",
    "PY19": """
? lambda nima?
+ Bitta ifodadan iborat nomsiz (anonim) funksiya
- Sikl turi
- Modul nomi
- Xato turi

? Quyidagi kod nima chiqaradi?
kv = lambda x: x ** 2
print(kv(5))
+ 25
- 10
- 5
- Xato beradi

? list(map(lambda x: x * 2, [1, 2, 3])) natijasi qaysi?
+ [2, 4, 6]
- [1, 2, 3]
- 12
- [1, 4, 9]

? list(filter(lambda x: x > 2, [1, 2, 3, 4])) natijasi qaysi?
+ [3, 4]
- [1, 2]
- [True, True]
- [False, False, True, True]

? sorted(["olma", "nok", "uzum"], key=len) natijasi qaysi?
+ ['nok', 'olma', 'uzum']
- ['olma', 'nok', 'uzum']
- ['uzum', 'olma', 'nok']
- ['nok', 'uzum', 'olma']

? sorted([3, 1, 2], reverse=True) natijasi qaysi?
+ [3, 2, 1]
- [1, 2, 3]
- [3, 1, 2]
- None

? sum([1, 2, 3, 4]) natijasi qancha?
+ 10
- 24
- 4
- 1234

? max(["olma", "nok", "uzum"], key=len) natijasi qaysi?
+ "olma"
- "nok"
- "uzum"
- Xato beradi

? min([5, 2, 8]) natijasi qancha?
+ 2
- 5
- 8
- 15

? map() funksiyasi qanday turdagi obyekt qaytaradi?
+ map obyekti — natijani ko'rish uchun list() ga o'raladi
- Har doim ro'yxat
- Har doim tuple
- Satr

? Lug'atlar ro'yxatini "ball" bo'yicha saralashning qisqa usuli qaysi?
+ sorted(talabalar, key=lambda t: t["ball"])
- sorted(talabalar, "ball")
- talabalar.sort(ball)
- sorted(talabalar["ball"])

? Quyidagi kod nima chiqaradi?
print(list(map(int, ["1", "2", "3"])))
+ [1, 2, 3]
- ['1', '2', '3']
- 6
- Xato beradi
""",
    "PY20": """
? Modul nima?
+ Funksiya, klass va o'zgaruvchilar saqlangan .py fayl
- Python o'rnatuvchisi
- Xato turi
- Ma'lumot turi

? random modulini import qilishning to'g'ri usuli qaysi?
+ import random
- include random
- using random
- require("random")

? random.randint(1, 6) qaysi qiymatlarni qaytarishi mumkin?
+ 1 dan 6 gacha (ikkalasi ham kiradi) butun son
- 1 dan 5 gacha butun son
- 0 dan 6 gacha kasr son
- Faqat 1 yoki 6

? random.choice(["tosh", "qog'oz", "qaychi"]) nima qiladi?
+ Ro'yxatdan tasodifiy bitta elementni tanlaydi
- Ro'yxatni aralashtiradi
- Ro'yxatni saralaydi
- Birinchi elementni qaytaradi

? random.shuffle(a) nima qiladi?
+ a ro'yxatini joyida aralashtiradi va None qaytaradi
- Aralashtirilgan yangi ro'yxat qaytaradi
- Bitta tasodifiy element qaytaradi
- Ro'yxatni saralaydi

? from random import randint yozilgandan keyin funksiya qanday chaqiriladi?
+ randint(1, 10)
- random.randint(1, 10)
- random(randint)
- import.randint(1, 10)

? import random as r yozuvi nimani bildiradi?
+ Modulga qisqa r nomi berildi: r.randint(1, 10)
- random moduli o'chirildi
- Faqat r funksiyasi import qilindi
- Xato beradi

? random.random() qanday qiymat qaytaradi?
+ 0.0 va 1.0 oralig'idagi kasr son (1.0 kirmaydi)
- 0 yoki 1
- 1 dan 100 gacha butun son
- Har doim 0.5

? random.sample(range(1, 50), 6) nima qiladi?
+ 1–49 oralig'idan 6 ta takrorlanmas son tanlaydi
- 6 marta bir xil son qaytaradi
- 6 dan 50 gacha sonlarni qaytaradi
- Xato beradi

? Modulning ichida qanday funksiyalar borligini qanday ko'rish mumkin?
+ dir(random) yoki help(random)
- print(random)
- len(random)
- random.list()

? Python bilan birga o'rnatiladigan modullar to'plami nima deyiladi?
+ Standart kutubxona
- PyPI
- Virtual muhit
- Interpretator

? Har safar bir xil "tasodifiy" ketma-ketlik olish uchun nima qilinadi?
+ random.seed(42)
- random.fix()
- random.same()
- Buning iloji yo'q
""",
    "PY21": """
? math.sqrt(16) natijasi qaysi?
+ 4.0
- 4
- 8
- 256

? math.ceil(4.2) natijasi qancha?
+ 5
- 4
- 4.2
- 4.0

? math.floor(4.8) natijasi qancha?
+ 4
- 5
- 4.8
- 5.0

? math.pi nimani bildiradi?
+ π sonini (≈ 3.14159)
- Funksiya
- Kvadrat ildiz
- 100 ni

? math.pow(2, 3) natijasi qaysi?
+ 8.0
- 6
- 9
- 5

? Bugungi sanani qanday olish mumkin?
+ datetime.date.today()
- datetime.today.date()
- date.now.today()
- time.date()

? datetime.datetime.now() nimani qaytaradi?
+ Hozirgi sana va vaqtni
- Faqat yilni
- Faqat soatni
- Kompyuter yoqilgan vaqtni

? Sanani "07.10.2026" ko'rinishida chiqarish uchun qaysi format ishlatiladi?
+ sana.strftime("%d.%m.%Y")
- sana.strftime("%Y-%m-%d")
- sana.format("dd.mm.yyyy")
- str(sana, "%d.%m.%Y")

? Bugundan 7 kun keyingi sanani qanday hisoblaysiz?
+ date.today() + timedelta(days=7)
- date.today() + 7
- date.today().add(7)
- timedelta(date.today(), 7)

? Ikki sana ayirmasi qanday turdagi obyekt bo'ladi?
+ timedelta
- date
- int
- str

? Quyidagi kod nima chiqaradi?
from datetime import date
print(date(2026, 10, 7).year)
+ 2026
- 10
- 7
- 2026-10-07

? math.factorial(5) natijasi qancha?
+ 120
- 25
- 15
- 5
""",
    "PY22": """
? re.findall(r"\\d+", "a12b3c456") natijasi qaysi?
+ ['12', '3', '456']
- ['1', '2', '3', '4', '5', '6']
- '123456'
- [12, 3, 456]

? re.search() va re.fullmatch() farqi nima?
+ search — matn ichida biror joyda topadi, fullmatch — butun matn mos bo'lishi kerak
- Ikkalasi bir xil
- search faqat raqamlarni qidiradi
- fullmatch faqat birinchi harfni tekshiradi

? \\w andozasi nimaga mos keladi?
+ Harf, raqam yoki pastki chiziq (_)
- Faqat bo'sh joy
- Faqat raqam
- Faqat nuqta

? \\s andozasi nimaga mos keladi?
+ Bo'sh joy belgisi (probel, tab, yangi qator)
- Istalgan harf
- Raqam
- Satr oxiri

? + kvantifikatori nimani bildiradi?
+ Oldingi element 1 yoki undan ko'p marta
- 0 yoki 1 marta
- Aynan 1 marta
- 0 yoki ko'p marta

? * kvantifikatori nimani bildiradi?
+ Oldingi element 0 yoki undan ko'p marta
- Aynan 1 marta
- 1 yoki ko'p marta
- Ko'paytirish amalini

? Nima uchun RegEx andozalari r"..." (raw string) ko'rinishida yoziladi?
+ Teskari chiziq (\\) Python tomonidan maxsus belgi sifatida o'zgartirilmasligi uchun
- Andoza tezroq ishlashi uchun
- Faqat katta harflarni qidirish uchun
- Bu majburiy emas va hech narsa o'zgartirmaydi

? re.sub(r"\\d", "#", "a1b2") natijasi qaysi?
+ "a#b#"
- "a1b2"
- "##"
- "ab"

? [abc] andozasi nimaga mos keladi?
+ a, b yoki c dan bittasiga
- Faqat "abc" so'ziga
- a, b, c dan boshqa belgilarga
- Uchta istalgan belgiga

? ^ va $ belgilari andozada nimani bildiradi?
+ Satr boshi va satr oxirini
- Daraja va dollar belgisini
- Istalgan belgini
- Takrorlanishni

? Matndan barcha email manzillarni ajratib olish uchun qaysi funksiya mos?
+ re.findall()
- re.fullmatch()
- re.compile() yolg'iz o'zi
- str.split()

? Quyidagi kod nima chiqaradi?
import re
m = re.search(r"(\\d{2})\\.(\\d{2})", "Sana: 07.10")
print(m.group(2))
+ 10
- 07
- 07.10
- Xato beradi
""",
    "PY23": """
? os.getcwd() nimani qaytaradi?
+ Joriy ishchi papka yo'lini
- Kompyuter nomini
- Fayllar sonini
- Python versiyasini

? os.listdir(".") nima qiladi?
+ Joriy papkadagi fayl va papkalar nomlari ro'yxatini qaytaradi
- Papkani o'chiradi
- Yangi papka yaratadi
- Faylni o'qiydi

? Yangi papka yaratish uchun qaysi funksiya ishlatiladi?
+ os.mkdir("yangi")
- os.create("yangi")
- os.newdir("yangi")
- open("yangi", "d")

? Yo'llarni operatsion tizimga mos birlashtirishning to'g'ri usuli qaysi?
+ os.path.join("papka", "fayl.txt")
- "papka" + "fayl.txt"
- os.join("papka", "fayl.txt")
- path("papka" - "fayl.txt")

? Fayl yoki papka mavjudligini qanday tekshirasiz?
+ os.path.exists("fayl.txt")
- os.exists.file("fayl.txt")
- open("fayl.txt").exists
- os.check("fayl.txt")

? Ichma-ich papkalarni (masalan, "Hisobotlar/2026-10") bir yo'la yaratish uchun nima ishlatiladi?
+ os.makedirs("Hisobotlar/2026-10", exist_ok=True)
- os.mkdir("Hisobotlar/2026-10") har doim
- os.path.join("Hisobotlar", "2026-10")
- os.listdir("Hisobotlar/2026-10")

? pathlib modulidagi zamonaviy yo'l bilan ishlash klassi qaysi?
+ Path
- Dir
- Folder
- File

? utils.py faylidagi funksiyani main.py'da ishlatish uchun nima yoziladi?
+ from utils import funksiya_nomi
- import utils.py
- include "utils"
- open("utils.py")

? if __name__ == "__main__": bloki qachon bajariladi?
+ Fayl to'g'ridan-to'g'ri ishga tushirilganda (import qilinganda emas)
- Fayl import qilinganda
- Har doim
- Hech qachon

? Tashqi kutubxonani o'rnatish buyrug'i qaysi?
+ pip install kutubxona_nomi
- python get kutubxona_nomi
- import install kutubxona_nomi
- os.install("kutubxona_nomi")

? Virtual muhit (venv) nima uchun kerak?
+ Har bir loyihaning kutubxonalarini alohida saqlash uchun
- Python'ni tezlashtirish uchun
- Internetsiz ishlash uchun
- Kodni shifrlash uchun

? Virtual muhit qanday yaratiladi?
+ python -m venv .venv
- pip venv create
- os.venv()
- python install venv
""",
    "PY24": """
? Xato bo'lishi mumkin bo'lgan kod qaysi blok ichiga yoziladi?
+ try
- except
- finally
- else

? except bloki qachon bajariladi?
+ try blokida xato yuz berganda
- Har doim
- Xato bo'lmaganda
- Dastur oxirida

? else bloki (try/except bilan) qachon bajariladi?
+ try blokida xato yuz bermaganda
- Xato yuz berganda
- Har doim
- Hech qachon

? finally bloki qachon bajariladi?
+ Har doim — xato bo'lsa ham, bo'lmasa ham
- Faqat xato bo'lganda
- Faqat xato bo'lmaganda
- Hech qachon

? int("abc") qanday xato beradi?
+ ValueError
- TypeError
- ZeroDivisionError
- KeyError

? Quyidagi kod nima chiqaradi?
try:
    print(10 / 0)
except ZeroDivisionError:
    print("Nolga bo'lish mumkin emas")
+ Nolga bo'lish mumkin emas
- 0
- inf
- Dastur xato bilan to'xtaydi

? Quyidagi kod nima chiqaradi?
try:
    x = int("5")
except ValueError:
    print("xato")
else:
    print("ok", x)
finally:
    print("tugadi")
+ ok 5 va keyingi qatorda tugadi
- xato va keyingi qatorda tugadi
- faqat tugadi
- faqat ok 5

? Bitta except bilan bir nechta xato turini ushlashning to'g'ri usuli qaysi?
+ except (ValueError, ZeroDivisionError):
- except ValueError, ZeroDivisionError:
- except ValueError or ZeroDivisionError:
- except [ValueError, ZeroDivisionError]:

? Xato xabarini o'zgaruvchiga olishning to'g'ri usuli qaysi?
+ except ValueError as e:
- except ValueError in e:
- except e = ValueError:
- except ValueError(e):

? O'zingiz xato chiqarish uchun qaysi kalit so'z ishlatiladi?
+ raise
- throw
- error
- except

? Nega bo'sh except: (xato turini ko'rsatmasdan) yozish yomon odat?
+ U barcha xatolarni, hatto kutilmaganlarini ham yashirib yuboradi
- U ishlamaydi
- Dastur sekinlashadi
- Python bunga ruxsat bermaydi

? Foydalanuvchi son o'rniga harf kiritsa, dastur to'xtamasligi uchun nima qilinadi?
+ int(input()) ni try/except ValueError ichiga olib, qayta so'raladi
- input() o'rniga print() yoziladi
- Hech narsa qilib bo'lmaydi
- Faqat if bilan uzunlik tekshiriladi
""",
    "PY25": """
? Faylni o'qish uchun qaysi rejimda ochiladi?
+ "r"
- "w"
- "a"
- "x"

? "w" rejimida mavjud fayl ochilsa nima bo'ladi?
+ Faylning eski mazmuni o'chib, yangidan yoziladi
- Yangi matn oxiriga qo'shiladi
- Xato beradi
- Fayl faqat o'qiladi

? "a" rejimi nima qiladi?
+ Yangi ma'lumotni fayl oxiriga qo'shadi
- Faylni o'chiradi
- Faylni faqat o'qiydi
- Faylni ikki baravar ko'paytiradi

? with open(...) as f: ko'rinishining afzalligi nima?
+ Blok tugagach fayl avtomatik yopiladi (xato bo'lsa ham)
- Fayl tezroq o'qiladi
- Fayl shifrlanadi
- Fayl hech qachon yopilmaydi

? f.read() nimani qaytaradi?
+ Faylning butun mazmunini bitta satr sifatida
- Faqat birinchi qatorni
- Qatorlar sonini
- Fayl nomini

? f.readlines() nimani qaytaradi?
+ Qatorlar ro'yxatini
- Bitta satrni
- Fayl hajmini
- Faqat oxirgi qatorni

? Faylni qatorma-qator o'qishning eng qulay usuli qaysi?
+ for qator in f:
- while f:
- f.loop()
- for qator in range(f):

? f.write("Salom") nima qiladi?
+ Faylga "Salom" matnini yozadi (yangi qatorsiz)
- Ekranga "Salom" chiqaradi
- Faylni o'qiydi
- Faylni o'chiradi

? Mavjud bo'lmagan faylni "r" rejimida ochsangiz qanday xato chiqadi?
+ FileNotFoundError
- ValueError
- KeyError
- Xato chiqmaydi, fayl yaratiladi

? O'zbekcha harflar to'g'ri saqlanishi uchun faylni qaysi kodlash bilan ochish tavsiya etiladi?
+ encoding="utf-8"
- encoding="ascii"
- encoding="bin"
- Kodlash ko'rsatish mumkin emas

? Har bir yozuvni yangi qatordan boshlash uchun nima qilinadi?
+ Matn oxiriga "\\n" qo'shiladi
- Har safar fayl qayta ochiladi
- write() o'zi yangi qator qo'shadi
- print() ishlatib bo'lmaydi

? Qatordagi oxirgi "\\n" belgisini olib tashlash uchun qaysi metod ishlatiladi?
+ qator.strip() (yoki rstrip())
- qator.split()
- qator.upper()
- qator.find()
""",
    "PY26": """
? JSON bilan ishlash uchun qaysi modul import qilinadi?
+ json
- pickle
- csv
- os

? json.dumps() nima qiladi?
+ Python obyektini JSON satriga aylantiradi
- JSON satrini Python obyektiga aylantiradi
- Faylni o'chiradi
- Faylni o'qiydi

? json.loads() nima qiladi?
+ JSON satrini Python obyektiga aylantiradi
- Python obyektini faylga yozadi
- Faylni yaratadi
- JSON'ni chiroyli formatlaydi

? Python ma'lumotini JSON faylga yozishning to'g'ri usuli qaysi?
+ json.dump(data, f)
- json.load(data, f)
- f.write(data)
- json.save(f)

? JSON fayldan ma'lumot o'qishning to'g'ri usuli qaysi?
+ data = json.load(f)
- data = json.dump(f)
- data = f.json()
- data = json.read(f)

? Python'dagi True JSON'da qanday yoziladi?
+ true
- True
- "True"
- 1

? Python'dagi None JSON'da qanday yoziladi?
+ null
- None
- nil
- ""

? JSON'dagi kalitlar qanday turda bo'ladi?
+ Faqat satr (qo'shtirnoqda)
- Istalgan tur
- Faqat son
- Faqat ro'yxat

? json.dump(..., ensure_ascii=False) nima uchun kerak?
+ O'zbekcha va boshqa harflar \\u kodlar emas, o'qiladigan holda saqlanishi uchun
- Faylni kichraytirish uchun
- Faqat ASCII harflarni saqlash uchun
- Xatoni yashirish uchun

? indent=2 parametri nima qiladi?
+ JSON'ni chekinishlar bilan chiroyli, o'qiladigan qilib yozadi
- Faqat 2 ta elementni yozadi
- Faylni ikki marta yozadi
- Kalitlarni saralaydi

? Dastur birinchi marta ishga tushganda JSON fayl hali yo'q bo'lsa, qanday yo'l to'g'ri?
+ FileNotFoundError'ni ushlab, bo'sh ma'lumot ({} yoki []) bilan boshlash
- Dasturni xato bilan to'xtatish
- json.load() ni bo'sh satr bilan chaqirish
- Faylni "r" rejimida yaratishga urinish

? Quyidagi kod nima chiqaradi?
import json
print(json.dumps({"a": [1, 2]}))
+ {"a": [1, 2]}
- {'a': [1, 2]}
- a: 1, 2
- Xato beradi
""",
    "PY27": """
? Klass (class) nima?
+ Obyektlar yaratish uchun shablon (chizma)
- Bitta o'zgaruvchi
- Python moduli
- Xato turi

? Obyekt nima?
+ Klass asosida yaratilgan aniq nusxa (instance)
- Klassning nomi
- Funksiya
- Fayl

? __init__ metodi qachon chaqiriladi?
+ Yangi obyekt yaratilganda avtomatik
- Obyekt o'chirilganda
- Dastur tugaganda
- Faqat qo'lda chaqirilganda

? self nimani bildiradi?
+ Metod chaqirilayotgan obyektning o'zini
- Klass nomini
- Global o'zgaruvchini
- Ota klassni

? Quyidagi kod nima chiqaradi?
class Mushuk:
    def __init__(self, ism):
        self.ism = ism
m = Mushuk("Momiq")
print(m.ism)
+ Momiq
- ism
- Mushuk
- Xato beradi

? Klass nomlari odatda qanday yoziladi?
+ PascalCase: TalabaKarta
- snake_case: talaba_karta
- kebab-case: talaba-karta
- HAMMASI_KATTA

? Quyidagi kod nima chiqaradi?
class Hisob:
    def __init__(self):
        self.balans = 0
    def toldir(self, summa):
        self.balans += summa
h = Hisob()
h.toldir(500)
h.toldir(300)
print(h.balans)
+ 800
- 500
- 300
- 0

? Atribut va metod farqi nima?
+ Atribut — obyekt ma'lumoti, metod — obyekt bajaradigan funksiya
- Ikkalasi bir xil
- Metod — ma'lumot, atribut — funksiya
- Atributlar faqat sonlar bo'ladi

? Bitta klassdan nechta obyekt yaratish mumkin?
+ Istalgancha
- Faqat bitta
- Faqat ikkita
- Faqat 10 ta

? Metod e'lon qilishda birinchi parametr sifatida nima yoziladi?
+ self
- this
- cls har doim
- Hech narsa

? Quyidagi kod nima chiqaradi?
class A:
    def __init__(self, x):
        self.x = x
a = A(3)
b = A(7)
print(a.x + b.x)
+ 10
- 3
- 7
- Xato beradi

? Mushuk("Momiq") qatori nima qiladi?
+ Mushuk klassidan yangi obyekt yaratadi va __init__ ni chaqiradi
- Mushuk klassini o'chiradi
- Klassni import qiladi
- Faqat "Momiq" satrini chiqaradi
""",
    "PY28": """
? Vorislik (inheritance) nima?
+ Yangi klass mavjud klassning atribut va metodlarini meros qilib oladi
- Ikki klassni o'chirish
- Funksiyani nusxalash
- Modul import qilish

? Kuchuk klassi Hayvon klassidan voris olishini qanday yozasiz?
+ class Kuchuk(Hayvon):
- class Kuchuk extends Hayvon:
- class Kuchuk -> Hayvon:
- class Kuchuk inherits Hayvon:

? super().__init__(ism) nima qiladi?
+ Ota klassning __init__ metodini chaqiradi
- Yangi klass yaratadi
- Obyektni o'chiradi
- Global o'zgaruvchi yaratadi

? Metodni qayta aniqlash (overriding) nima?
+ Voris klassda ota klassdagi metodni o'zgacha qilib qayta yozish
- Metodni o'chirish
- Metodni ikki marta chaqirish
- Metod nomini o'zgartirish

? Quyidagi kod nima chiqaradi?
class Hayvon:
    def ovoz(self):
        return "..."
class Mushuk(Hayvon):
    def ovoz(self):
        return "Miyov"
print(Mushuk().ovoz())
+ Miyov
- ...
- None
- Xato beradi

? Polimorfizm nima?
+ Turli klass obyektlarining bir xil nomli metodi o'zicha ishlashi
- Bitta klassdan bitta obyekt yaratish
- Klasslarni o'chirish
- Faqat bitta metodga ega bo'lish

? Quyidagi kod nima chiqaradi?
class A:
    def salom(self):
        return "A"
class B(A):
    pass
print(B().salom())
+ A
- B
- None
- Xato beradi

? isinstance(obj, Hayvon) nimani tekshiradi?
+ obj Hayvon klassi yoki uning vorisining obyekti ekanini
- obj nomi "Hayvon" ekanini
- Hayvon klassi mavjudligini
- obj ichida Hayvon atributi borligini

? Agar Kuchuk(Hayvon) bo'lsa, isinstance(Kuchuk(), Hayvon) natijasi qaysi?
+ True
- False
- None
- Xato beradi

? Vorislikning asosiy foydasi nima?
+ Umumiy kodni takrorlamasdan qayta ishlatish
- Dasturni sekinlashtirish
- Klasslar sonini kamaytirish shart
- Xatolarni yashirish

? Quyidagi kod nima chiqaradi?
class Shakl:
    def yuza(self):
        return 0
class Kvadrat(Shakl):
    def __init__(self, a):
        self.a = a
    def yuza(self):
        return self.a ** 2
shakllar = [Shakl(), Kvadrat(3)]
print([s.yuza() for s in shakllar])
+ [0, 9]
- [0, 0]
- [9, 9]
- Xato beradi

? Voris klass ota klassda yo'q yangi metod qo'sha oladimi?
+ Ha
- Yo'q, faqat ota metodlarini ishlatadi
- Faqat __init__ qo'shish mumkin
- Faqat atribut qo'shish mumkin
""",
    "PY29": """
? Inkapsulyatsiya nima?
+ Obyekt ma'lumotini yashirib, unga faqat metodlar orqali to'g'ri kirishni ta'minlash
- Klasslarni bir faylga yig'ish
- Funksiyani nusxalash
- Ma'lumotni JSON'ga saqlash

? _balans (bitta pastki chiziq) nomlash qoidasi nimani bildiradi?
+ "Ichki foydalanish uchun" — tashqaridan tegmaslik tavsiya etiladi (protected)
- Atribut butunlay yashirin va unga kirib bo'lmaydi
- Bu global o'zgaruvchi
- Xato beradi

? __balans (ikkita pastki chiziq) nima bilan ajralib turadi?
+ Nom o'zgartiriladi (name mangling) — tashqaridan obj.__balans bilan kirib bo'lmaydi
- U umumiy (public) atribut
- U metod bo'ladi
- Uni klass ichida ham ishlatib bo'lmaydi

? @property dekoratori nima qiladi?
+ Metodni atribut kabi (qavssiz) o'qish imkonini beradi
- Metodni o'chiradi
- Klassni statik qiladi
- Atributni ro'yxatga aylantiradi

? Property setter nima uchun ishlatiladi?
+ Qiymat o'rnatishdan oldin uni tekshirish uchun (masalan, narx manfiy bo'lmasin)
- Qiymatni o'qish uchun
- Obyektni o'chirish uchun
- Klass nomini o'zgartirish uchun

? __str__ metodi qachon ishlatiladi?
+ print(obj) yoki str(obj) chaqirilganda
- Obyekt yaratilganda
- Obyekt solishtirilganda
- len(obj) chaqirilganda

? __len__ metodi qaysi funksiya chaqirilganda ishlaydi?
+ len(obj)
- str(obj)
- print(obj)
- sorted(obj)

? __eq__ metodi qaysi operator uchun ishlaydi?
+ ==
- <
- +
- in

? sorted() obyektlarni solishtira olishi uchun klassda qaysi metod yetarli?
+ __lt__
- __str__
- __len__
- __init__

? Quyidagi kod nima chiqaradi?
class Mahsulot:
    def __init__(self, nom):
        self.nom = nom
    def __str__(self):
        return "Mahsulot: " + self.nom
print(Mahsulot("Non"))
+ Mahsulot: Non
- Non
- <__main__.Mahsulot object at ...>
- Xato beradi

? Quyidagi kod nima chiqaradi?
class Savat:
    def __init__(self):
        self.items = ["non", "sut", "tuxum"]
    def __len__(self):
        return len(self.items)
print(len(Savat()))
+ 3
- 0
- 1
- Xato beradi

? __repr__ ning __str__ dan farqi nima?
+ __repr__ dasturchi uchun aniq ko'rinish, __str__ foydalanuvchi uchun chiroyli ko'rinish
- Farqi yo'q
- __repr__ faqat sonlar uchun
- __str__ faqat xatolar uchun
""",
    "PY30": """
? Tosh-qog'oz-qaychi o'yinida kompyuter tanlovi qanday olinadi?
+ random.choice(["tosh", "qog'oz", "qaychi"])
- input("tosh, qog'oz yoki qaychi")
- random.randint("tosh", "qaychi")
- sorted(["tosh", "qog'oz", "qaychi"])[0]

? Tosh-qog'oz-qaychida "tosh" nimani yutadi?
+ qaychini
- qog'ozni
- toshni
- hech nimani

? "Sonni top" o'yinida yashirin son qanday tanlanadi?
+ random.randint(1, 100)
- input()
- range(1, 100)
- random.choice(100)

? Foydalanuvchi to'g'ri topguncha takrorlash uchun qaysi tuzilma mos?
+ while sikli va to'g'ri topilganda break
- for i in range(1)
- Faqat if
- Faqat return

? Talabga ko'ra har bir o'yin qanday tashkil qilinadi?
+ Alohida funksiya sifatida
- Bitta katta print ichida
- Global o'zgaruvchilar bilan, funksiyasiz
- Har biri alohida faylda, funksiyasiz

? Menyuda "0 — Chiqish" tanlanganda dastur qanday to'xtaydi?
+ Asosiy while True siklidan break bilan chiqiladi
- Kompyuter o'chiriladi
- Xato chiqariladi
- continue yoziladi

? Foydalanuvchi son o'rniga harf kiritsa, dastur to'xtab qolmasligi uchun nima qilinadi?
+ try/except ValueError bilan ushlab, qayta so'raladi
- Hech narsa qilinmaydi
- Dastur qayta ishga tushiriladi
- input() o'chiriladi

? Natijalar (g'alaba, mag'lubiyat, eng kam urinish) qayerda saqlanadi?
+ scores.json faylida
- Faqat o'zgaruvchida — dastur yopilganda yo'qoladi
- Ekranda
- Rasm faylida

? Sonni top o'yinida foydalanuvchi 40 kiritdi, yashirin son 70. Dastur nima deyishi kerak?
+ "Kattaroq son kiriting"
- "Kichikroq son kiriting"
- "Topdingiz!"
- "Xato"

? Urinishlar sonini hisoblash uchun nima qilinadi?
+ urinish o'zgaruvchisini har kiritishda 1 ga oshirish
- len(input())
- random.randint() natijasini saqlash
- Hech narsa, Python o'zi hisoblaydi

? Quyidagi funksiya "tosh" va "qaychi" uchun nima qaytaradi?
def golib(a, b):
    yutadi = {"tosh": "qaychi", "qaychi": "qog'oz", "qog'oz": "tosh"}
    if a == b:
        return "durang"
    return "a" if yutadi[a] == b else "b"
+ "a"
- "b"
- "durang"
- Xato beradi

? Loyihani boshlashdan oldin nima qilish tavsiya etilgan edi?
+ Tuzilmani rejalashtirish — kerakli funksiyalar ro'yxatini tuzish
- Darhol bitta faylga hammasini yozish
- Faqat dizayn chizish
- Kod yozmasdan taqdimot tayyorlash
""",
    "PY31": """
? CRUD qisqartmasi nimani bildiradi?
+ Create, Read, Update, Delete
- Copy, Run, Upload, Download
- Class, Return, Use, Define
- Code, Review, Upload, Deploy

? Loyiha ma'lumotlari dastur qayta ochilganda saqlanib qolishi uchun qayerda saqlanadi?
+ JSON faylda
- Faqat ro'yxat o'zgaruvchisida
- print() natijasida
- Terminal tarixida

? Tavsiya etilgan modullar bo'linishi qaysi?
+ storage.py, models.py, main.py
- Hammasi bitta main.py da
- Har bir funksiya alohida faylda
- data.txt va main.py

? storage.py modulining vazifasi nima?
+ Ma'lumotni JSON faylga saqlash va fayldan yuklash
- Menyuni chiqarish
- Foydalanuvchidan ma'lumot so'rash
- Rang berish

? "Read" amali tizimda nimani anglatadi?
+ Yozuvlarni ko'rish (ro'yxatni chiqarish yoki qidirish)
- Yangi yozuv qo'shish
- Yozuvni o'chirish
- Yozuvni tahrirlash

? Har bir yozuvni ishonchli topish va tahrirlash uchun nima qo'shiladi?
+ Takrorlanmas id
- Tasodifiy rang
- Faqat ism
- Hech narsa

? Ismi bo'yicha qidirishning to'g'ri usuli qaysi?
+ [x for x in yozuvlar if soz.lower() in x["ism"].lower()]
- yozuvlar.find(soz)
- yozuvlar[soz]
- sorted(soz)

? Yozuvlarni narx bo'yicha saralash uchun qaysi kod mos?
+ sorted(yozuvlar, key=lambda x: x["narx"])
- yozuvlar.sort("narx")
- sorted(yozuvlar["narx"])
- max(yozuvlar)

? Yozuvni o'chirishdan oldin nima qilish yaxshi amaliyot?
+ Foydalanuvchidan tasdiq so'rash
- Hech narsa so'ramasdan o'chirish
- Barcha yozuvlarni o'chirish
- Dasturni qayta ishga tushirish

? Foydalanuvchi noto'g'ri menyu raqami kiritsa nima bo'lishi kerak?
+ Xabar chiqib, menyu qayta ko'rsatiladi
- Dastur xato bilan to'xtaydi
- Barcha ma'lumot o'chadi
- Kompyuter o'chadi

? OOP o'tilgan bo'lsa, yozuvni ifodalashning eng yaxshi usuli qaysi?
+ class (masalan, Talaba) va JSON uchun to_dict / from_dict metodlari
- Har bir maydon uchun alohida global o'zgaruvchi
- Bitta uzun satr
- Ro'yxat ichida ro'yxat, nomsiz

? Har bir o'zgarishdan (qo'shish, tahrirlash, o'chirish) keyin nima qilish kerak?
+ Ma'lumotni JSON faylga saqlash
- Dasturni yopish
- Ekranni tozalash
- Hech narsa
""",
    "PY32": """
? Telegram botni qayerda yaratasiz?
+ @BotFather orqali
- Google Play'da
- python.org saytida
- VS Code'da

? Bot tokeni haqida qaysi gap to'g'ri?
+ U maxfiy — kodga emas, muhit o'zgaruvchisiga (environment variable) yoziladi
- Uni GitHub'ga ochiq yuklash mumkin
- Token har kim uchun bir xil
- Token kerak emas

? Darsda qaysi kutubxona o'rnatildi?
+ pip install pyTelegramBotAPI
- pip install telegram-desktop
- pip install botfather
- pip install tkinter

? Kutubxona kodda qanday import qilinadi?
+ import telebot
- import pyTelegramBotAPI
- import telegram.desktop
- import botfather

? Bot obyekti qanday yaratiladi?
+ bot = telebot.TeleBot(TOKEN)
- bot = telebot.create()
- bot = TeleBot.new()
- bot = BotFather(TOKEN)

? /start buyrug'iga javob beradigan handler qanday yoziladi?
+ @bot.message_handler(commands=["start"])
- @bot.command("start")
- @bot.start()
- @telebot.on("start")

? Foydalanuvchiga xabar yuborish metodi qaysi?
+ bot.send_message(chat_id, "Salom")
- bot.print("Salom")
- bot.reply_all("Salom")
- bot.write(chat_id)

? Kelgan xabarga javob (reply) berishning qisqa usuli qaysi?
+ bot.reply_to(message, "Salom")
- bot.answer(message)
- message.send("Salom")
- print(message)

? Pastki menyu tugmalari uchun qaysi klass ishlatiladi?
+ ReplyKeyboardMarkup
- InlineQuery
- Button.print
- KeyboardHandler

? Botni doimiy ishlatib turish uchun dastur oxirida nima yoziladi?
+ bot.infinity_polling() (yoki bot.polling())
- bot.start()
- while True: pass
- bot.close()

? Polling nima?
+ Bot Telegram serveridan yangi xabarlarni muntazam so'rab turadi
- Bot xabarlarni o'chiradi
- Botni o'chirish usuli
- Token yaratish usuli

? "Tasodifiy fakt" tugmasi bosilganda faktni tanlashning to'g'ri usuli qaysi?
+ random.choice(faktlar)
- faktlar[0] har doim
- input(faktlar)
- sorted(faktlar)
""",
    "PY33": """
? Xabar ichida ko'rinadigan, bosilganda callback yuboradigan tugmalar uchun qaysi klass ishlatiladi?
+ InlineKeyboardMarkup
- ReplyKeyboardMarkup
- ForceReply
- KeyboardRemove

? Inline tugma qanday yaratiladi?
+ InlineKeyboardButton("Ha", callback_data="ha")
- InlineKeyboardButton("Ha", url_data=1)
- Button("Ha")
- ReplyKeyboardButton("Ha")

? Inline tugma bosilishini qaysi handler ushlaydi?
+ @bot.callback_query_handler(func=lambda c: True)
- @bot.message_handler(commands=["callback"])
- @bot.inline()
- @bot.button_handler

? callback_data nima uchun kerak?
+ Qaysi tugma bosilganini aniqlash uchun
- Tugma rangini belgilash uchun
- Botni o'chirish uchun
- Tokenni saqlash uchun

? Har bir foydalanuvchi ma'lumoti qaysi kalit bo'yicha saqlanadi?
+ user_id (message.from_user.id)
- Foydalanuvchi ismi
- Xabar matni
- Tasodifiy son

? Nega foydalanuvchi ma'lumotlari JSON faylda saqlanadi?
+ Bot qayta ishga tushganda ma'lumotlar yo'qolmasligi uchun
- Bot tezroq ishlashi uchun
- Telegram talab qilgani uchun
- Token o'rniga ishlatish uchun

? JSON kalitlari satr bo'lgani uchun user_id qanday saqlanadi?
+ str(user_id) ko'rinishida
- float ko'rinishida
- Ro'yxat ko'rinishida
- Saqlanmaydi

? Bot "holati" (state) nima?
+ Foydalanuvchi qaysi bosqichda ekani (masalan, ism kutilmoqda)
- Bot tokeni
- Botning rasmi
- Telegram versiyasi

? Keyingi xabarni ma'lum funksiyaga yo'naltirish uchun pyTelegramBotAPI'da nima ishlatiladi?
+ bot.register_next_step_handler(message, funksiya)
- bot.next(message)
- bot.wait()
- message.next_step()

? Callback qayta ishlangach, tugmadagi "soat" belgisini olib tashlash uchun nima chaqiriladi?
+ bot.answer_callback_query(call.id)
- bot.stop()
- bot.delete_message()
- bot.close_callback()

? Handler ichidagi xato butun botni to'xtatib qo'ymasligi uchun nima qilinadi?
+ Xavfli joylar try/except bilan o'raladi
- Xatolarga e'tibor berilmaydi
- Bot har daqiqada qayta ishga tushiriladi
- Token o'zgartiriladi

? Yakuniy bot talablari bo'yicha token qayerda bo'lishi kerak?
+ Muhit o'zgaruvchisida yoki .env faylida, kodda emas
- main.py ning birinchi qatorida
- GitHub README'da
- Bot tavsifida
""",
    "PY34": """
? Yakuniy loyiha kodi qayerga joylanishi kerak?
+ GitHub'ga
- Faqat fleshkaga
- Faqat Telegram chatga
- Hech qayerga

? README.md faylida nima bo'lishi kerak?
+ Loyiha nima qilishi va qanday ishga tushirilishi
- Faqat muallif rasmi
- Bot tokeni
- Bo'sh fayl

? Taqdimot qanday tuzilgan?
+ 5 daqiqa demo + 3 daqiqa savol-javob
- 30 daqiqa nazariya
- Faqat kod o'qib berish
- Taqdimot yo'q

? Baholashda eng ko'p ball qaysi mezonga berilgan?
+ Loyiha ishlaydi va foydali — 40 ball
- GitHub va README — 10 ball
- Taqdimot — 20 ball
- Faqat kod hajmi

? Kod sifatiga nimalar kiradi?
+ Funksiya/klasslarga ajratish, tushunarli nomlash, xatolarni ushlash
- Iloji boricha uzun funksiyalar
- Bir harfli o'zgaruvchi nomlari
- Izohsiz va tartibsiz kod

? Loyihaga kerakli kutubxonalar ro'yxati qaysi faylga yoziladi?
+ requirements.txt
- README.png
- token.txt
- main.json

? GitHub'ga tokenlar va maxfiy fayllar tushmasligi uchun nima ishlatiladi?
+ .gitignore fayli
- README.md
- requirements.txt
- LICENSE

? Kod o'zgarishlarini GitHub'ga yuborish uchun qaysi buyruqlar ketma-ketligi to'g'ri?
+ git add . → git commit -m "..." → git push
- git push → git add → git commit
- git delete → git push
- git clone → git commit

? Demo paytida nima muhim?
+ Asosiy imkoniyatlarni ishlayotgan holda ko'rsatish
- Faqat kod qatorlarini sanash
- Kompyuter sozlamalarini ko'rsatish
- Xatolarni yashirish uchun demo qilmaslik

? Savollarga javob berishda qanday yondashuv to'g'ri?
+ Kodni o'zingiz tushunasiz — qaysi qism nima qilishini tushuntira olasiz
- "Bilmayman, internetdan olganman"
- Savolga javob bermaslik
- Mavzuni o'zgartirish

? Qaysi loyiha turlari yakuniy loyiha sifatida qabul qilinadi?
+ Telegram bot yoki konsol boshqaruv tizimi (yoki yangi g'oya)
- Faqat veb-sayt
- Faqat mobil ilova
- Faqat Scratch o'yini

? Loyihani boshqa kompyuterda ishga tushirish uchun odatda nima qilinadi?
+ git clone, virtual muhit, pip install -r requirements.txt va dasturni ishga tushirish
- Faqat README'ni o'qish
- Faylni nusxalab, hech narsa o'rnatmaslik
- Kompyuterni qayta o'rnatish
""",
}
