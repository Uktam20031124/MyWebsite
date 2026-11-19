"""Dasturchi 4-oy (DP13–DP24) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "DP13": """
? sinf = ["Ali", "Laylo", "Vali"]. sinf[0] nima?
+ "Ali"
- "Laylo"
- "Vali"
- Xato

? sinf[-1] nima qaytaradi?
+ Oxirgi elementni
- Birinchi elementni
- Xato
- Bo'sh ro'yxatni

? [10, 20, 30, 40][:2] natijasi?
+ [10, 20]
- [10, 20, 30]
- [30, 40]
- [20]

? [1, 2, 3, 4, 5][::2] natijasi?
+ [1, 3, 5]
- [2, 4]
- [1, 2]
- [5, 3, 1]

? len([5, 4, 3]) natijasi?
+ 3
- 12
- 5
- 2

? "Laylo" in ["Ali", "Laylo"] natijasi?
+ True
- False
- 1
- Xato

? sinf[2] = "Valijon" nima qiladi?
+ 3-elementni almashtiradi
- Yangi element qo'shadi
- Xato beradi
- 2-elementni o'chiradi

? sinf = ["A", "B"]. sinf[5] nima beradi?
+ IndexError xatosi
- None
- Bo'sh satr
- "B"

? List va satrning asosiy farqi?
+ List o'zgaruvchan, satrni o'zgartirib bo'lmaydi
- Farqi yo'q
- Satr o'zgaruvchan
- List faqat son saqlaydi

? [1, 2, 3][::-1] natijasi?
+ [3, 2, 1]
- [1, 2, 3]
- [3]
- Xato
""",
    "DP14": """
? append(x) nima qiladi?
+ Ro'yxat oxiriga x ni qo'shadi
- Boshiga qo'shadi
- x ni o'chiradi
- Ro'yxatni tozalaydi

? remove(x) nima qiladi?
+ Qiymati x bo'lgan birinchi elementni o'chiradi
- x-indeksdagi elementni o'chiradi
- Hammasini o'chiradi
- Oxirgisini o'chiradi

? pop() argumentsiz nima qiladi?
+ Oxirgi elementni olib tashlab qaytaradi
- Birinchisini o'chiradi
- Ro'yxatni tozalaydi
- Xato beradi

? Bo'sh ro'yxat qanday yoziladi?
+ []
- {}
- ()
- None

? Yo'q qiymatni remove() qilsak nima bo'ladi?
+ ValueError xatosi
- Hech narsa
- None qaytadi
- Ro'yxat tozalanadi

? if not vazifalar: qachon rost?
+ Ro'yxat bo'sh bo'lganda
- Ro'yxatda 1 element bo'lganda
- Har doim
- Hech qachon

? a = [1]; a.append(2); a.append(3). a nima?
+ [1, 2, 3]
- [3, 2, 1]
- [1]
- [6]

? insert(0, x) nima qiladi?
+ x ni ro'yxat boshiga qo'yadi
- x ni oxiriga qo'yadi
- 0 ni o'chiradi
- x ni almashtiradi

? for v in vazifalar: da v nima?
+ Navbatdagi element
- Element indeksi
- Ro'yxat uzunligi
- Har doim birinchi element

? a = ["x", "y", "z"]; a.pop(1). Natija va a?
+ "y" qaytadi, a = ["x", "z"]
- "x" qaytadi
- a o'zgarmaydi
- Xato
""",
    "DP15": """
? [5, 4, 3] yig'indisini hisoblashda jami qayerda 0 qilinadi?
+ Sikldan oldin
- Sikl ichida
- Sikldan keyin
- Kerak emas

? sum([5, 4, 3]) natijasi?
+ 12
- 3
- 5
- 543

? max([2, 9, 4]) natijasi?
+ 9
- 2
- 4
- 15

? O'rtacha qanday hisoblanadi?
+ sum(a) / len(a)
- max(a) / 2
- sum(a) * len(a)
- len(a) / sum(a)

? eng_katta = baholar[0] nima uchun?
+ Solishtirishni haqiqiy qiymatdan boshlash uchun
- Birinchi bahoni o'chirish uchun
- Xato chiqmasligi uchun shart emas
- O'rtachani topish uchun

? [5, 4, 3, 5, 2] da 4 dan past baholar nechta?
+ 2
- 3
- 1
- 0

? min([7, 3, 9]) natijasi?
+ 3
- 7
- 9
- 19

? round(28 / 7, 2) natijasi?
+ 4.0
- 4
- 28
- 0.25

? Shart bo'yicha sanashda qaysi qator kerak?
+ if shart: son += 1
- son = len(a)
- son = sum(a)
- son = max(a)

? Bo'sh ro'yxatga max([]) nima beradi?
+ ValueError xatosi
- 0
- None
- []
""",
    "DP16": """
? Tuple qanday yoziladi?
+ (1, 2, 3)
- [1, 2, 3]
- {1, 2, 3}
- <1, 2, 3>

? Tuple elementini o'zgartirsak nima bo'ladi?
+ TypeError xatosi
- O'zgaradi
- Yangi tuple yaratiladi
- None qaytadi

? x, y = (3, 4) dan keyin y nima?
+ 4
- 3
- (3, 4)
- Xato

? set([1, 1, 2, 2, 3]) natijasi?
+ {1, 2, 3}
- [1, 2, 3]
- {1, 1, 2, 2, 3}
- 3

? Bo'sh set qanday yaratiladi?
+ set()
- {}
- []
- ()

? {1, 2, 3} & {2, 3, 4} natijasi?
+ {2, 3}
- {1, 2, 3, 4}
- {1}
- {4}

? {1, 2} | {2, 3} natijasi?
+ {1, 2, 3}
- {2}
- {1, 3}
- {1, 2, 2, 3}

? {1, 2, 3} - {2} natijasi?
+ {1, 3}
- {2}
- {1, 2, 3}
- Xato

? Nega set'ni chiqarishda sorted() ishlatamiz?
+ set'da tartib yo'q — natija har xil tartibda chiqishi mumkin
- set'ni ro'yxatga aylantirib bo'lmaydi
- Xato bo'lmasligi uchun shart
- Takrorlarni o'chirish uchun

? set elementiga indeks bilan murojaat (s[0]) qilsa bo'ladimi?
+ Yo'q — set'da indeks yo'q
- Ha
- Faqat sonlarda
- Faqat bo'sh set'da
""",
    "DP17": """
? Lug'at qanday yoziladi?
+ {"Ali": "+998..."}
- ["Ali", "+998..."]
- ("Ali": "+998...")
- {"Ali", "+998..."}

? kitob["Ali"] nima qaytaradi?
+ "Ali" kalitining qiymatini
- Birinchi elementni
- "Ali" so'zini
- Kalitlar ro'yxatini

? Yo'q kalitga kitob["X"] bilan murojaat qilsak?
+ KeyError xatosi
- None
- Bo'sh satr
- 0

? kitob.get("X", "Topilmadi") X yo'q bo'lsa nima qaytaradi?
+ "Topilmadi"
- None
- KeyError
- "X"

? kitob["Vali"] = "+998..." Vali yo'q bo'lsa nima bo'ladi?
+ Yangi juftlik qo'shiladi
- Xato chiqadi
- Hech narsa
- Eski qiymat o'chadi

? kitob["Ali"] = "yangi" Ali bor bo'lsa?
+ Qiymat almashtiriladi
- Ikkinchi Ali qo'shiladi
- Xato
- Hech narsa

? kitob.items() nima beradi?
+ (kalit, qiymat) juftliklarini
- Faqat kalitlarni
- Faqat qiymatlarni
- Lug'at uzunligini

? len({"a": 1, "b": 2}) natijasi?
+ 2
- 4
- 1
- 3

? Lug'atda bir xil kalit ikki marta bo'ladimi?
+ Yo'q — kalitlar takrorlanmaydi
- Ha
- Faqat satr kalitlarda
- Faqat son kalitlarda

? for ism, tel in kitob.items(): da tel nima?
+ Shu kalitning qiymati
- Kalitning o'zi
- Indeks
- Lug'at uzunligi
""",
    "DP18": """
? "la" in "laylo" natijasi?
+ True
- False
- 2
- Xato

? Nega qidirishda .lower() ishlatamiz?
+ Katta-kichik harfga qaramay topish uchun
- Tezroq ishlashi uchun
- Xato chiqmasligi uchun
- Ismni o'zgartirish uchun

? kitob.pop("Ali", None) Ali bor bo'lsa nima qiladi?
+ O'chiradi va qiymatini qaytaradi
- Faqat qiymatini qaytaradi
- None qaytaradi
- Xato beradi

? kitob.pop("X", None) X yo'q bo'lsa?
+ None qaytaradi, xato bo'lmaydi
- KeyError
- Lug'at tozalanadi
- "X" qaytaradi

? sorted(kitob) nima beradi?
+ Kalitlarning saralangan ro'yxatini
- Qiymatlarning ro'yxatini
- Saralangan lug'atni
- Xato

? "vali".title() natijasi?
+ "Vali"
- "VALI"
- "vali"
- "vAli"

? topildi = False bayrog'i nimaga kerak?
+ Birorta mos kontakt topilmasa xabar berish uchun
- Siklni to'xtatish uchun
- Kontaktni o'chirish uchun
- Ismni saqlash uchun

? Lug'atni for bilan aylanganda nima keladi?
+ Kalitlar
- Qiymatlar
- Juftliklar
- Indekslar

? Kontaktni tahrirlash uchun nima qilamiz?
+ kitob[ism] = yangi_tel — qayta yozamiz
- kitob.edit(ism)
- kitob.update_value()
- Avval o'chirish shart

? "+998901112233".startswith("+998") natijasi?
+ True
- False
- "+998"
- Xato
""",
    "DP19": """
? oquvchilar = [{"ism": "Ali"}, ...] qanday tuzilma?
+ Lug'atlar ro'yxati
- Ro'yxatlar lug'ati
- Tuple
- Set

? oquvchilar[1]["baholar"][1] nimani anglatadi?
+ 2-o'quvchining 2-bahosi
- 1-o'quvchining 1-bahosi
- 2-o'quvchining barcha baholari
- Xato

? o["orta"] = 4.5 nima qiladi?
+ Lug'atga yangi kalit qo'shadi
- Xato beradi
- Ro'yxatga element qo'shadi
- Kalitni o'chiradi

? for o in oquvchilar: da o ni o'zgartirsak, ro'yxatdagi lug'at o'zgaradimi?
+ Ha — o o'sha lug'atning o'zi
- Yo'q — o nusxa
- Faqat satrlar o'zgaradi
- Xato chiqadi

? f"{o['ism']}" da nega ichida bitta qo'shtirnoq?
+ Tashqi qo'shtirnoq bilan adashmasligi uchun
- Python faqat bittasini qabul qiladi
- Tezroq ishlaydi
- Farqi yo'q

? [5, 4, 5] o'rtachasi (2 xona)?
+ 4.67
- 4.5
- 5
- 14

? m = [[1, 2], [3, 4]]. m[1][0] nima?
+ 3
- 2
- 1
- 4

? Eng yaxshi o'quvchini topish uchun nima qilamiz?
+ Birinchidan boshlab, kattaroq o'rtachali chiqsa almashtiramiz
- Ro'yxatni o'chiramiz
- Har doim birinchisini olamiz
- len() ishlatamiz

? Ichma-ich ma'lumotga misol?
+ JSON, API javoblari, o'quvchilar bazasi
- Bitta son
- Bitta satr
- True qiymati

? oquvchilar[0]["ism"] nima qaytaradi?
+ Birinchi o'quvchining ismini
- Barcha ismlarni
- "ism" so'zini
- Xato
""",
    "DP20": """
? Funksiya qanday e'lon qilinadi?
+ def nom(parametrlar):
- function nom():
- func nom[]:
- define nom:

? return nima qiladi?
+ Natijani qaytaradi va funksiyani tugatadi
- Ekranga chiqaradi
- Funksiyani qayta boshlaydi
- Xato chiqaradi

? return yozilmagan funksiya nima qaytaradi?
+ None
- 0
- Bo'sh satr
- Xato

? def qosh(a, b): da a va b nima?
+ Parametrlar
- Argumentlar
- Global o'zgaruvchilar
- Natijalar

? qosh(2, 3) da 2 va 3 nima?
+ Argumentlar
- Parametrlar
- Kalitlar
- Indekslar

? print va return farqi?
+ print ekranga chiqaradi, return qiymatni qaytaradi
- Farqi yo'q
- return ekranga chiqaradi
- print qiymatni qaytaradi

? "12 * 3".split() natijasi?
+ ["12", "*", "3"]
- ["12 * 3"]
- [12, 3]
- "12*3"

? return dan keyingi qatorlar bajariladimi?
+ Yo'q
- Ha
- Faqat print
- Faqat bir marta

? bol(1, 0) yuqoridagi kodda nima qaytaradi?
+ None
- 0
- ZeroDivisionError
- 1

? Funksiyadan nima foyda?
+ Kodni qayta ishlatish va qismlarga bo'lish
- Dastur sekinlashadi
- O'zgaruvchilar kerak bo'lmaydi
- Faqat chiroyli ko'rinish
""",
    "DP21": """
? def salom(ism="Mehmon"): da salom() chaqirilsa ism nima?
+ "Mehmon"
- None
- Xato
- Bo'sh satr

? *args qanday turda keladi?
+ tuple
- list
- dict
- set

? qosh("A", "B", "C") da *yangilar nima?
+ ("A", "B", "C")
- "A"
- ["A", "B", "C"]
- 3

? enumerate(["a", "b"], start=1) qanday juftliklar beradi?
+ (1, "a"), (2, "b")
- (0, "a"), (1, "b")
- ("a", 1), ("b", 2)
- 1, 2

? Funksiya ichida yaratilgan o'zgaruvchi tashqarida ko'rinadimi?
+ Yo'q — u lokal
- Ha
- Faqat print bilan
- Faqat return bo'lsa

? Default'li parametr qayerda yoziladi?
+ Default'sizlardan keyin
- Birinchi bo'lib
- Istalgan joyda
- Faqat oxirgi bo'lib bitta

? vazifalar.pop(raqam - 1) da nega - 1?
+ Foydalanuvchi 1 dan, indeks 0 dan sanaydi
- Oxirgi elementni olish uchun
- Xato chiqmasligi uchun shart emas
- Ro'yxatni teskari qilish uchun

? korsat("Bugun") chaqirilsa sarlavha nima?
+ "Bugun"
- "Vazifalar"
- None
- Xato

? **kwargs qanday turda keladi?
+ dict
- tuple
- list
- set

? 1 <= raqam <= len(vazifalar) nimani tekshiradi?
+ Raqam ro'yxat chegarasida ekanini
- Raqam juftligini
- Ro'yxat bo'shligini
- Raqam satr ekanini
""",
    "DP22": """
? lambda x: x * 2 nima?
+ x ni olib 2 ga ko'paytiradigan qisqa funksiya
- O'zgaruvchi
- Sikl
- Xato

? sorted(a, reverse=True) nima qiladi?
+ Kattadan kichikka saralaydi
- Kichikdan kattaga saralaydi
- Ro'yxatni teskari qiladi, saralamaydi
- Xato

? sorted(oquvchilar, key=lambda o: o[1]) nima bo'yicha saralaydi?
+ Har juftlikning 2-elementi (ball) bo'yicha
- Ism bo'yicha
- Uzunlik bo'yicha
- Tasodifiy

? list(map(lambda x: x + 1, [1, 2])) natijasi?
+ [2, 3]
- [1, 2]
- [3]
- Xato

? filter nima qoldiradi?
+ Funksiya True qaytargan elementlarni
- Funksiya False qaytarganlarni
- Hammasini
- Birinchisini

? Nega map va filter natijasini list() ga o'raymiz?
+ Ular iterator qaytaradi
- Aks holda xato chiqadi
- Tezroq ishlashi uchun
- Saralash uchun

? max([("A", 5), ("B", 9)], key=lambda o: o[1]) natijasi?
+ ("B", 9)
- ("A", 5)
- 9
- "B"

? sorted() asl ro'yxatni o'zgartiradimi?
+ Yo'q — yangi ro'yxat qaytaradi
- Ha
- Faqat raqamlarni
- Faqat satrlarni

? lambda'da nechta ifoda bo'lishi mumkin?
+ Faqat bitta
- Istalgancha
- Ikkita
- Hech qancha

? sorted(["olma", "nok", "anor"], key=len) natijasi?
+ ["nok", "olma", "anor"]
- ["anor", "nok", "olma"]
- ["olma", "anor", "nok"]
- Xato
""",
    "DP23": """
? [x * 2 for x in [1, 2, 3]] natijasi?
+ [2, 4, 6]
- [1, 2, 3]
- [3, 6]
- 12

? [x for x in [1, 5, 8] if x > 4] natijasi?
+ [5, 8]
- [1]
- [1, 5, 8]
- [8]

? "Salom dunyo".split() natijasi?
+ ["Salom", "dunyo"]
- ["S", "a", "l"]
- "Salomdunyo"
- ["Salom dunyo"]

? "oson.".strip(".,!?") natijasi?
+ "oson"
- "oson."
- "."
- ""

? sanoq.get(s, 0) + 1 nima uchun?
+ So'z birinchi uchraganda 0 dan boshlash uchun
- Xatoni yashirish uchun
- So'zni o'chirish uchun
- Ro'yxat yaratish uchun

? max(sanoq, key=sanoq.get) nima qaytaradi?
+ Qiymati eng katta kalitni
- Eng katta qiymatni
- Birinchi kalitni
- Lug'at uzunligini

? "a" in "aeiou" natijasi?
+ True
- False
- 0
- Xato

? List comprehension'ning afzalligi?
+ Sikl va shartni bir qatorda, o'qishga oson yozish
- Har doim tezroq va boshqa yo'li yo'q
- Faqat sonlar bilan ishlaydi
- Xatolarni o'zi tuzatadi

? len([s for s in ["ab", "abcde", "x"] if len(s) > 4]) natijasi?
+ 1
- 2
- 3
- 0

? {s: len(s) for s in ["ab", "c"]} natijasi?
+ {"ab": 2, "c": 1}
- ["ab", "c"]
- {2, 1}
- Xato
""",
    "DP24": """
? Kundalikda har vazifa qanday saqlanadi?
+ Lug'at: {"matn": ..., "bajarildi": ...}
- Faqat satr
- Tuple
- Son

? Nega har amal alohida funksiyada?
+ Kod tushunarli va qayta ishlatiladigan bo'ladi
- Python shuni talab qiladi
- Tezroq ishlaydi
- O'zgaruvchilar kerak bo'lmaydi

? raqam_sora() noto'g'ri raqamda nima qaytaradi?
+ None
- 0
- -1
- Xato

? "✔" if v["bajarildi"] else "☐" nima qiladi?
+ Holatga qarab belgi tanlaydi
- Vazifani bajaradi
- Vazifani o'chiradi
- Xato beradi

? vazifalar[i]["bajarildi"] = True nima qiladi?
+ Vazifani bajarilgan deb belgilaydi
- Vazifani o'chiradi
- Yangi vazifa qo'shadi
- Ro'yxatni tozalaydi

? vazifalar.pop(i)["matn"] nima qaytaradi?
+ O'chirilgan vazifaning matnini
- Ro'yxatni
- None
- Indeksni

? Bajarilganlar soni qanday hisoblanadi?
+ len([v for v in vazifalar if v["bajarildi"]])
- len(vazifalar)
- sum(vazifalar)
- vazifalar.count(True)

? if matn: nimani tekshiradi?
+ Vazifa matni bo'sh emasligini
- Matn raqam ekanini
- Matn uzunligi 10 ekanini
- Hech narsani

? "5".isdigit() and 1 <= 5 <= 3 natijasi?
+ False
- True
- 5
- Xato

? Dastur yopilsa vazifalar saqlanib qoladimi?
+ Yo'q — ular faqat xotirada; 5-oyda faylga saqlaymiz
- Ha, avtomatik
- Faqat bajarilganlari
- Faqat Windows'da
""",
}
