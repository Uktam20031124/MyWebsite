"""Dasturchi 3-oy (DP01–DP12) testlari: har darsga 10 ta savol. Format — ``quizzes_ai.py`` kabi."""

QUIZZES = {
    "DP01": """
? Python faylining kengaytmasi qanday?
+ .py
- .txt
- .exe
- .python

? print("Salom") nima qiladi?
+ Ekranga Salom yozadi
- Salom nomli fayl yaratadi
- Salomni xotiraga saqlaydi
- Hech narsa qilmaydi

? Windows'da Python o'rnatishda qaysi belgini qo'yish kerak?
+ Add Python to PATH
- Install for all users
- Disable path length limit
- Hech qaysi

? Terminalda hello.py faylini qanday ishga tushiramiz?
+ python hello.py
- run hello.py
- open hello.py
- start python

? # belgisidan keyingi matn nima?
+ Izoh — Python uni bajarmaydi
- Xato
- Sarlavha
- Maxfiy kod

? print("A", "B", sep="-") nima chiqaradi?
+ A-B
- A B
- AB
- A-B-

? print("=" * 3) nima chiqaradi?
+ ===
- =3
- = = =
- Xato

? print("Salom", end="!") dan keyin nima chiqadi?
+ Salom! va yangi qator yo'q
- Salom va yangi qator
- !Salom
- Salom !

? Python kodni qanday bajaradi?
+ Yuqoridan pastga, qatorma-qator
- Pastdan yuqoriga
- Tasodifiy tartibda
- Faqat birinchi qatorni

? print(Salom) (qo'shtirnoqsiz) nima beradi?
+ Xato: Salom nomli o'zgaruvchi yo'q
- Salom
- "Salom"
- Bo'sh qator
""",
    "DP02": """
? yosh = 13 qatorida = belgisi nimani bildiradi?
+ O'ngdagi qiymatni chapdagi nomga yozadi
- Ikki qiymat tengligini tekshiradi
- Qiymatlarni qo'shadi
- Hech narsani

? type(3.14) qaysi turni qaytaradi?
+ float
- int
- str
- bool

? type("13") qaysi turni qaytaradi?
+ str
- int
- float
- bool

? Qaysi o'zgaruvchi nomi to'g'ri?
+ mening_ismim
- 2ism
- mening ismim
- class

? bool turida qanday qiymatlar bor?
+ True va False
- 0 va 1 faqat
- "ha" va "yo'q"
- Istalgan son

? yosh = 13; yosh = yosh + 1. yosh nechaga teng?
+ 14
- 13
- 1
- Xato

? O'zgarmas qiymat (konstanta) qanday nomlanadi?
+ KATTA harflar bilan: PI = 3.14
- Kichik harflar bilan
- Raqam bilan boshlanib
- Probel bilan

? print("Ism:", ism) da ism qo'shtirnoqsiz yozilsa nima chiqadi?
+ ism o'zgaruvchisining qiymati
- ism so'zining o'zi
- Xato
- Bo'sh joy

? Python'da Ism va ism bir xil o'zgaruvchimi?
+ Yo'q — katta-kichik harf farqlanadi
- Ha
- Faqat satrlar uchun
- Faqat sonlar uchun

? a, b = b, a nima qiladi?
+ a va b qiymatlarini almashtiradi
- Ikkalasini o'chiradi
- Xato beradi
- a ni b ga tenglaydi
""",
    "DP03": """
? input() qaysi turdagi qiymat qaytaradi?
+ str (matn)
- int
- float
- bool

? int("2013") natijasi nima?
+ 2013 (son)
- "2013"
- Xato
- 2013.0

? int(input("Yil: ")) da qaysi biri birinchi bajariladi?
+ input
- int
- Ikkalasi bir vaqtda
- print

? "20" + "13" natijasi nima?
+ "2013"
- 33
- 2013
- Xato

? int(3.9) natijasi nima?
+ 3
- 4
- 3.9
- Xato

? f"{ism}, salom" da ism = "Ali" bo'lsa natija?
+ Ali, salom
- {ism}, salom
- ism, salom
- Xato

? int("ikki") nima beradi?
+ ValueError xatosi
- 2
- 0
- "ikki"

? float("2.5") natijasi?
+ 2.5
- 2
- "2.5"
- 25

? str(10) + " ball" natijasi?
+ "10 ball"
- 10 ball xato
- 20
- "10" va "ball" alohida

? Joriy yil 2026, tug'ilgan yil 2013. yosh = 2026 - 2013 nechaga teng?
+ 13
- 14
- 12
- 4039
""",
    "DP04": """
? 7 / 2 natijasi?
+ 3.5
- 3
- 4
- 1

? 7 // 2 natijasi?
+ 3
- 3.5
- 1
- 4

? 7 % 2 natijasi?
+ 1
- 3
- 3.5
- 0

? 2 ** 3 natijasi?
+ 8
- 6
- 9
- 5

? 2 + 3 * 4 natijasi?
+ 14
- 20
- 24
- 9

? (2 + 3) * 4 natijasi?
+ 20
- 14
- 9
- 24

? round(3.14159, 2) natijasi?
+ 3.14
- 3.1
- 3
- 3.15

? 10 / 5 natijasi qanday turda chiqadi?
+ float — 2.0
- int — 2
- str — "2"
- bool

? Son juftligini qanday tekshiramiz?
+ son % 2 == 0
- son / 2 == 0
- son // 2 == 1
- son ** 2 == 0

? x = 5; x += 3. x nechaga teng?
+ 8
- 5
- 3
- 53
""",
    "DP05": """
? "Python"[0] nima qaytaradi?
+ "P"
- "y"
- "n"
- Xato

? "Python"[-1] nima qaytaradi?
+ "n"
- "P"
- "o"
- Xato

? len("Salom") natijasi?
+ 5
- 4
- 6
- "5"

? "  ali  ".strip() natijasi?
+ "ali"
- "  ali"
- "ALI"
- "ali  "

? "ali valiyev".title() natijasi?
+ "Ali Valiyev"
- "ALI VALIYEV"
- "Ali valiyev"
- "ali Valiyev"

? "salom".upper() natijasi?
+ "SALOM"
- "Salom"
- "salom"
- "S"

? "salom"[::-1] natijasi?
+ "molas"
- "salom"
- "s"
- Xato

? "Python"[1:4] natijasi?
+ "yth"
- "Pyt"
- "ytho"
- "tho"

? s = "abc"; s.upper() dan keyin s nima?
+ "abc" — metod satrni o'zgartirmaydi
- "ABC"
- Xato
- Bo'sh satr

? Satr palindrom ekanini qanday tekshiramiz?
+ s == s[::-1]
- s == s.upper()
- len(s) == 0
- s[0] == s[1]
""",
    "DP06": """
? 5 == 5 natijasi?
+ True
- False
- 5
- Xato

? 5 != 3 natijasi?
+ True
- False
- 2
- Xato

? = va == farqi nima?
+ = qiymat beradi, == tenglikni tekshiradi
- Farqi yo'q
- == qiymat beradi
- = faqat sonlar uchun

? True and False natijasi?
+ False
- True
- None
- Xato

? True or False natijasi?
+ True
- False
- None
- Xato

? not True natijasi?
+ False
- True
- 0
- Xato

? len("12345") >= 8 natijasi?
+ False
- True
- 5
- Xato

? x = 15 bo'lsa 13 <= x <= 17 natijasi?
+ True
- False
- 15
- Xato

? "admin" == "Admin" natijasi?
+ False — katta-kichik harf farqlanadi
- True
- Xato
- None

? Login ham, parol ham to'g'ri bo'lishi kerak. Qaysi amal?
+ and
- or
- not
- ==
""",
    "DP07": """
? if qatorining oxirida nima bo'lishi shart?
+ Ikki nuqta (:)
- Nuqta-vergul (;)
- Vergul
- Hech narsa

? if blokidagi qatorlar qanday yoziladi?
+ 4 probel chekinish bilan
- Qavs ichida
- Bir qatorda
- Chekinishsiz

? elif qachon tekshiriladi?
+ Oldingi shartlar yolg'on bo'lsa
- Har doim
- Oldingi shart rost bo'lsa
- Hech qachon

? else ga shart yoziladimi?
+ Yo'q
- Ha
- Faqat son bo'lsa
- Faqat matn bo'lsa

? Bitta if-elif-else zanjirida nechta blok bajariladi?
+ Faqat bittasi — birinchi rost shartli
- Hammasi
- Rost bo'lganlarning hammasi
- Ikkitasi

? ball = 78. Kod: if ball >= 86 → 5, elif ball >= 71 → 4, else → 3. Natija?
+ 4
- 5
- 3
- Xato

? Nega shartlarni kattadan kichikka tartiblaymiz?
+ Aks holda katta ball ham kichik shartga birinchi tushib qoladi
- Tezroq ishlashi uchun
- Python shuni talab qiladi
- Farqi yo'q

? if ball == 100: blokidagi print qachon bajariladi?
+ Faqat ball 100 bo'lganda
- Har doim
- Hech qachon
- ball 100 dan katta bo'lganda

? Chekinishsiz yozilgan print if dan keyin qachon bajariladi?
+ Har doim — u shartga tegishli emas
- Faqat shart rost bo'lsa
- Faqat else da
- Hech qachon

? Qaysi qiymat shartda False hisoblanadi?
+ 0
- 1
- "0"
- -1
""",
    "DP08": """
? match tanlov: dan keyin variantlar qaysi so'z bilan yoziladi?
+ case
- if
- when
- option

? case _: nimani bildiradi?
+ Boshqa hamma holatni
- Bo'sh qiymatni
- Xatoni
- Birinchi variantni

? tanlov = input() bo'lsa, case 1: yoki case "1": qaysi to'g'ri?
+ case "1": — input matn qaytaradi
- case 1:
- Ikkalasi bir xil
- Hech qaysi

? Ichma-ich shart nima?
+ Shart ichidagi yana bir shart
- Ikki shartni and bilan ulash
- Takrorlanuvchi shart
- Xato

? Nolga bo'lishdan oldin nimani tekshiramiz?
+ b == 0
- a == 0
- b > 100
- a == b

? Ichma-ich shartda chekinish qanday?
+ Har bosqichda yana 4 probel
- Bir xil qoladi
- Kamayadi
- Kerak emas

? match qachon if-elif dan qulayroq?
+ Bitta qiymatni ko'p variant bilan solishtirganda
- Har doim
- Faqat sonlar uchun
- Hech qachon

? 10 / 0 nima beradi?
+ ZeroDivisionError xatosi
- 0
- 10
- Cheksizlik belgisi

? Menyu dasturida foydalanuvchi "9" tanlasa, case _ yo'q bo'lsa nima bo'ladi?
+ Hech qaysi blok bajarilmaydi
- Xato chiqadi
- Birinchi case bajariladi
- Dastur qayta boshlanadi

? if b == 0 ... else ... da b = 5 bo'lsa qaysi blok?
+ else
- if
- Ikkalasi
- Hech qaysi
""",
    "DP09": """
? while sikli qachongacha takrorlanadi?
+ Shart rost ekan
- 10 marta
- Shart yolg'on ekan
- Bir marta

? random.randint(1, 100) qaysi sonlarni berishi mumkin?
+ 1 dan 100 gacha, ikkalasi ham kiradi
- 1 dan 99 gacha
- 0 dan 100 gacha
- Faqat juft sonlar

? random modulidan foydalanish uchun nima yoziladi?
+ import random
- use random
- include random
- random()

? Cheksiz sikl nima uchun paydo bo'ladi?
+ Shartdagi o'zgaruvchi sikl ichida o'zgarmasa
- Sikl juda qisqa bo'lsa
- print ko'p bo'lsa
- import yozilmasa

? “Sonni top” o'yinida taxmin = 0 nega boshida beriladi?
+ while shartini birinchi marta tekshirish uchun
- O'yin 0 dan boshlanishi uchun
- Xato chiqmasligi uchun shart emas
- Ballni saqlash uchun

? 1–100 oralig'ida har safar yarmini tashlasak, son ko'pi bilan nechta urinishda topiladi?
+ 7
- 10
- 50
- 100

? while taxmin != son: sikli qachon tugaydi?
+ taxmin son bilan teng bo'lganda
- taxmin 0 bo'lganda
- 100 urinishdan keyin
- Hech qachon

? Sikldan keyingi print qachon bajariladi?
+ Sikl tugagandan keyin bir marta
- Har aylanishda
- Hech qachon
- Sikldan oldin

? i = 3; while i > 0: i -= 1. Sikl necha marta aylanadi?
+ 3
- 2
- 4
- Cheksiz

? Terminalda cheksiz siklni qanday to'xtatamiz?
+ Ctrl + C
- Ctrl + S
- Esc
- Enter
""",
    "DP10": """
? range(5) qaysi sonlarni beradi?
+ 0, 1, 2, 3, 4
- 1, 2, 3, 4, 5
- 0 dan 5 gacha
- 5 ta tasodifiy son

? range(1, 11) ning oxirgi soni?
+ 10
- 11
- 1
- 9

? range(10, 0, -2) qaysi sonlarni beradi?
+ 10, 8, 6, 4, 2
- 10, 8, 6, 4, 2, 0
- 0, 2, 4, 6, 8, 10
- 10, 9, 8 ... 1

? for va while ning farqi?
+ for — takrorlar soni ma'lum, while — shart bo'yicha
- Farqi yo'q
- while tezroq
- for faqat satrlar uchun

? Yig'uvchi o'zgaruvchi qayerda boshlanadi?
+ Sikldan oldin, masalan jami = 0
- Sikl ichida
- Sikldan keyin
- Kerak emas

? 1 dan 100 gacha sonlar yig'indisi nechaga teng?
+ 5050
- 5000
- 100
- 10100

? jami += i nimani bildiradi?
+ jami = jami + i
- jami = i
- i = jami + i
- jami == i

? for i in range(3): print(i) nima chiqaradi?
+ 0 1 2 (har biri alohida qatorda)
- 1 2 3
- 0 1 2 3
- 3

? print(i, end=" ") nima qiladi?
+ Sonlarni bir qatorga probel bilan yozadi
- Har birini yangi qatorga yozadi
- Probelni o'chiradi
- Xato

? n = 7 uchun jadvalning oxirgi qatori?
+ 7 × 10 = 70
- 7 × 11 = 77
- 7 × 9 = 63
- 7 × 7 = 49
""",
    "DP11": """
? break nima qiladi?
+ Sikldan darhol chiqadi
- Keyingi aylanishga o'tadi
- Dasturni o'chiradi
- Siklni qaytadan boshlaydi

? continue nima qiladi?
+ Qolgan qatorlarni o'tkazib, keyingi aylanishga o'tadi
- Sikldan chiqadi
- Dasturni to'xtatadi
- Hech narsa

? while True: sikli qanday to'xtaydi?
+ Ichidagi break bilan
- O'zi to'xtaydi
- 10 marta aylangach
- Hech qachon to'xtamaydi

? Ichma-ich sikldagi break qaysi sikldan chiqadi?
+ Faqat o'zi turgan (ichki) sikldan
- Ikkala sikldan
- Tashqi sikldan
- Dasturdan

? "12".isdigit() natijasi?
+ True
- False
- 12
- Xato

? "o'n".isdigit() natijasi?
+ False
- True
- 10
- Xato

? "Kattaroq" if 30 < 42 else "Kichikroq" natijasi?
+ "Kattaroq"
- "Kichikroq"
- True
- Xato

? Nega harf kiritilganda continue ishlatamiz?
+ int() xatosiz, qayta so'rash uchun
- O'yinni tugatish uchun
- Urinishni ko'paytirish uchun
- Sonni o'zgartirish uchun

? 7 urinishdan keyin o'yin tugashi uchun nima kerak?
+ if urinish == 7: ... break
- while urinish:
- continue
- import random

? Tashqi sikl “Yana o'ynaysizmi?” savolida “yo'q” bo'lsa?
+ break bilan tashqi sikldan chiqadi va “Xayr!” chiqadi
- Yangi o'yin boshlanadi
- Xato chiqadi
- Ichki sikl qaytadan boshlanadi
""",
    "DP12": """
? Bank terminalida balans va tarix qayerda e'lon qilinadi?
+ Sikldan oldin
- Sikl ichida
- Har tanlovda qaytadan
- Dastur oxirida

? Nega balans sikl ichida 0 qilib e'lon qilinmaydi?
+ Har aylanishda nolga tushib qolardi
- Xato chiqadi
- Python ruxsat bermaydi
- Farqi yo'q

? f"{150000:,}" natijasi?
+ "150,000"
- "150000"
- "150.000"
- Xato

? Chiqim summasi balansdan katta bo'lsa nima qilamiz?
+ “Mablag' yetarli emas” deb, balansni o'zgartirmaymiz
- Balansni manfiy qilamiz
- Dasturni to'xtatamiz
- Kirim qilamiz

? tarix += f"+{summa:,}\\n" nima qiladi?
+ Tarix satriga yangi qator qo'shadi
- Tarixni o'chiradi
- Balansni oshiradi
- Xato beradi

? print(tarix or "Hali amal yo'q") tarix bo'sh bo'lsa nima chiqaradi?
+ Hali amal yo'q
- Bo'sh qator
- False
- Xato

? 0 tanlanganda dastur qanday tugaydi?
+ break bilan sikldan chiqib
- exit() bilan majburiy
- Xato chiqarib
- Tugamaydi

? Menyuda yo'q raqam kiritilsa qaysi blok ishlaydi?
+ else — “Noto'g'ri tanlov”
- Birinchi if
- Hech qaysi
- Dastur yopiladi

? Balans 0, kirim 150000, chiqim 50000. Balans nechaga teng?
+ 100000
- 200000
- 150000
- 50000

? balans -= summa nimani bildiradi?
+ balans = balans - summa
- balans = summa
- summa = balans - summa
- balans == summa
""",
}
