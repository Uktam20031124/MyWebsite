"""Dasturchi 5-oy (DP25–DP36) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "DP25": """
? Modul nima?
+ Tayyor kod yozilgan fayl, uni import qilib ishlatamiz
- Python'ning xatosi
- O'zgaruvchi turi
- Sikl turi

? import random dan keyin choice qanday chaqiriladi?
+ random.choice(royxat)
- choice(royxat)
- random(royxat)
- import.choice()

? from datetime import date dan keyin bugungi sana qanday olinadi?
+ date.today()
- datetime.date.today()
- today()
- date.now

? random.choice(["a", "b", "c"]) nima qaytaradi?
+ Ro'yxatdan tasodifiy bitta element
- Hamma elementni
- Birinchi elementni
- Indeksni

? date(2026, 1, 1) - date(2025, 12, 25) natijasining .days qiymati?
+ 7
- 6
- 8
- -7

? timedelta(days=7) nima?
+ 7 kunlik muddat
- 7-sana
- 7 soat
- Xato

? strftime("%d.%m.%Y") nima qiladi?
+ Sanani 19.11.2026 kabi matnga aylantiradi
- Matnni sanaga aylantiradi
- Sanani o'chiradi
- Vaqtni chiqaradi

? random.randint(1, 6) qaysi sonlarni beradi?
+ 1 dan 6 gacha, ikkalasi ham kiradi
- 1 dan 5 gacha
- 0 dan 6 gacha
- Faqat 6

? Fayl nomini random.py qo'ysak nima bo'ladi?
+ Python o'z faylimizni import qiladi va dastur buziladi
- Hech narsa
- Tezroq ishlaydi
- Avtomatik nomi o'zgaradi

? import random as r dan keyin to'g'ri chaqiruv?
+ r.randint(1, 6)
- random.randint(1, 6)
- randint(1, 6)
- as.randint(1, 6)
""",
    "DP26": """
? try bloki nima uchun kerak?
+ Xato bo'lishi mumkin bo'lgan kodni yozish uchun
- Siklni tezlatish uchun
- Funksiya e'lon qilish uchun
- Faylni ochish uchun

? int("abc") qaysi xatoni beradi?
+ ValueError
- TypeError
- KeyError
- IndexError

? 10 / 0 qaysi xatoni beradi?
+ ZeroDivisionError
- ValueError
- NameError
- FileNotFoundError

? finally bloki qachon bajariladi?
+ Har doim — xato bo'lsa ham, bo'lmasa ham
- Faqat xato bo'lsa
- Faqat xato bo'lmasa
- Hech qachon

? except ValueError: qaysi xatoni ushlaydi?
+ Faqat ValueError'ni
- Hamma xatoni
- Hech qaysini
- Faqat ZeroDivisionError'ni

? input_int() ichida continue nima qiladi?
+ Noto'g'ri kiritishdan keyin qayta so'raydi
- Funksiyadan chiqadi
- Xatoni chiqaradi
- Sonni qaytaradi

? Nega kichik=None va is not None tekshiruvi?
+ Chegara ixtiyoriy bo'lsin va 0 ham to'g'ri chegara bo'lsin
- None tezroq ishlaydi
- Python shuni talab qiladi
- Xato chiqmasligi uchun shart emas

? raise ValueError("...") nima qiladi?
+ O'zimiz xato chiqaramiz
- Xatoni yashiradi
- Dasturni qayta boshlaydi
- Hech narsa

? Bo'sh except: (turisiz) nega yomon?
+ Hamma xatoni yashirib, muammoni topishni qiyinlashtiradi
- Ishlamaydi
- Sekin ishlaydi
- Faqat ValueError'ni ushlaydi

? except (ValueError, IndexError): nima qiladi?
+ Ikki turdagi xatoni ham ushlaydi
- Faqat birinchisini
- Hech qaysini
- Xato beradi
""",
    "DP27": """
? with open(...) as f: ning afzalligi?
+ Blok tugagach fayl avtomatik yopiladi
- Fayl tezroq o'qiladi
- Fayl o'chib ketmaydi
- Xato bo'lmaydi

? "w" rejimi eski mazmun bilan nima qiladi?
+ O'chirib, yangidan yozadi
- Oxiriga qo'shadi
- O'zgartirmaydi
- Faqat o'qiydi

? Faylga eskisini saqlab qo'shish uchun qaysi rejim?
+ "a"
- "w"
- "r"
- "x"

? Yo'q faylni "r" bilan ochsak?
+ FileNotFoundError
- Bo'sh fayl yaratiladi
- None qaytadi
- Hech narsa

? encoding="utf-8" nima uchun?
+ O'zbekcha harflar buzilmasligi uchun
- Fayl kichikroq bo'lishi uchun
- Tezroq ishlashi uchun
- Shart emas

? f.write("Sport") yangi qatorga o'tadimi?
+ Yo'q — "\\n" ni o'zimiz qo'shamiz
- Ha, avtomatik
- Faqat oxirgi qatorda
- Xato beradi

? qator.strip() nima uchun?
+ Qator oxiridagi \\n va probellarni olib tashlash uchun
- Qatorni o'chirish uchun
- Qatorni katta harf qilish uchun
- Faylni yopish uchun

? for qator in f: nima qiladi?
+ Faylni qatorma-qator o'qiydi
- Faylga yozadi
- Faylni o'chiradi
- Faylni yopadi

? Dasturda fayl bilan ishlashning oddiy tartibi?
+ yukla → o'zgartir → saqla
- saqla → yukla → o'chir
- o'chir → yoz
- Faqat yoz

? Fayl birinchi marta yo'q bo'lsa yukla() nima qaytaradi?
+ Bo'sh ro'yxat (except FileNotFoundError tufayli)
- Xato
- None
- Fayl nomini
""",
    "DP28": """
? json.dump(obj, f) nima qiladi?
+ Python obyektini faylga JSON qilib yozadi
- Fayldan o'qiydi
- Satrga aylantiradi
- Faylni o'chiradi

? json.load(f) nima qaytaradi?
+ Fayldagi JSON'dan Python list/dict
- Satr
- Fayl nomi
- None

? json.dumps va json.dump farqi?
+ dumps satr qaytaradi, dump faylga yozadi
- Farqi yo'q
- dumps faylga yozadi
- dump satr qaytaradi

? json.dumps(True) natijasi?
+ "true"
- "True"
- "1"
- Xato

? ensure_ascii=False nima beradi?
+ O'zbekcha harflar \\u kodlarsiz saqlanadi
- Fayl kichrayadi
- Xatolar yashiriladi
- Faqat inglizcha saqlanadi

? indent=2 nima qiladi?
+ JSON'ni chiroyli, o'qiladigan qilib yozadi
- 2 ta fayl yaratadi
- 2 ta element saqlaydi
- Xato

? Nega sanani str(date.today()) qilib saqlaymiz?
+ JSON date turini bilmaydi — matn qilib saqlaymiz
- Tezroq ishlashi uchun
- Sana o'chib ketmasligi uchun
- Shart emas

? None JSON'da qanday yoziladi?
+ null
- None
- nil
- ""

? Buzilgan JSON faylni o'qisak qaysi xato?
+ json.JSONDecodeError
- FileNotFoundError
- KeyError
- ZeroDivisionError

? JSON'da lug'at kalitlari qanday bo'ladi?
+ Faqat satr
- Istalgan tur
- Faqat son
- Faqat bool
""",
    "DP29": """
? class nima?
+ Obyektlar uchun chizma (shablon)
- O'zgaruvchi
- Fayl
- Sikl

? __init__ qachon chaqiriladi?
+ Obyekt yaratilganda avtomatik
- Dastur tugaganda
- Faqat qo'lda
- Hech qachon

? self nima?
+ Metod chaqirilayotgan obyektning o'zi
- Klass nomi
- Global o'zgaruvchi
- Kalit so'z, ma'nosi yo'q

? self.matn = matn qatori nima qiladi?
+ Obyektga matn atributini yozadi
- Global o'zgaruvchi yaratadi
- Matnni chiqaradi
- Xato beradi

? Metod nima?
+ Klass ichidagi, obyekt bajaradigan funksiya
- Atribut
- Modul
- Klass nomi

? t1 = Task("A"); t2 = Task("B"); t1.bajar(). t2.bajarildi nima?
+ False — har obyekt mustaqil
- True
- None
- Xato

? Klass nomi qanday yoziladi?
+ PascalCase: TaskManager
- snake_case: task_manager
- KATTA: TASKMANAGER
- Raqam bilan

? Task("Kitob") yozilganda nima bo'ladi?
+ Yangi obyekt yaratiladi va __init__ ishlaydi
- Klass o'chadi
- Xato chiqadi
- Faqat matn chiqadi

? if __name__ == "__main__": bloki qachon ishlaydi?
+ Fayl to'g'ridan-to'g'ri ishga tushganda
- Fayl import qilinganda
- Hech qachon
- Har doim

? Atribut va metod farqi?
+ Atribut — ma'lumot, metod — harakat (funksiya)
- Farqi yo'q
- Metod — ma'lumot
- Atribut — funksiya
""",
    "DP30": """
? class Admin(User): nimani bildiradi?
+ Admin User'dan voris oladi
- User Admin'dan voris oladi
- Ikki klass bir xil
- Xato

? super().__init__(ism) nima qiladi?
+ Ota klassning __init__ ini chaqiradi
- Yangi obyekt yaratadi
- Klassni o'chiradi
- Hech narsa

? Overriding nima?
+ Voris klassda ota metodini qayta yozish
- Metodni o'chirish
- Yangi klass yaratish
- Atribut qo'shish

? isinstance(Admin("L", 2), User) natijasi?
+ True
- False
- None
- Xato

? Admin'da salom() yozilmagan. Admin("L", 2).salom() ishlaydimi?
+ Ha — User'dan meros
- Yo'q, xato
- None qaytaradi
- Faqat super() bilan

? Polimorfizm nima?
+ Turli obyektlarga bir xil metod — har biri o'z javobini beradi
- Bitta obyektni ko'p marta yaratish
- Klassni o'chirish
- Metodni yashirish

? Vorislikning foydasi?
+ Umumiy kodni takrorlamaslik
- Dastur sekinlashadi
- Klasslar kerak bo'lmaydi
- Faqat chiroyli ko'rinish

? User("Ali").huquq() natijasi?
+ "o'qish"
- "o'qish, yozish, o'chirish"
- None
- Xato

? Admin("Laylo", 2).daraja nima?
+ 2
- "Laylo"
- None
- Xato

? Ota klass qanday nomlanadi?
+ Asosiy (parent / base) klass
- Voris klass
- Modul
- Obyekt
""",
    "DP31": """
? print(obj) qaysi maxsus metodni chaqiradi?
+ __str__
- __len__
- __init__
- __getitem__

? len(obj) ishlashi uchun qaysi metod kerak?
+ __len__
- __str__
- __size__
- __count__

? @property nima qiladi?
+ Metodni atribut kabi qavssiz o'qish imkonini beradi
- Metodni o'chiradi
- Atributni yashiradi
- Klassni statik qiladi

? _vazifalar dagi pastki chiziq nimani bildiradi?
+ “Ichki, tashqaridan tegmang” degan kelishuv
- Xato
- Global o'zgaruvchi
- Konstanta

? raise ValueError("Bo'sh vazifa") qachon kerak?
+ Noto'g'ri qiymat kelganda o'zimiz xato chiqarish uchun
- Har doim
- Hech qachon
- Faqat fayl bilan ishlaganda

? __getitem__ nima beradi?
+ obj[i] va for ... in obj ishlaydi
- obj o'chadi
- obj chiqariladi
- obj nusxalanadi

? t.__dict__ nima qaytaradi?
+ Obyekt atributlarini lug'at ko'rinishida
- Klass nomini
- Metodlar ro'yxatini
- JSON satrini

? menejer.bajarilgan (qavssiz) nega ishlaydi?
+ U @property
- U oddiy atribut
- Xato bo'ladi
- __str__ tufayli

? try: menejer.qosh("   ") except ValueError as e: print(e) nima chiqaradi?
+ Bo'sh vazifa
- ValueError
- Hech narsa
- None

? sum(1 for t in vazifalar if t.bajarildi) nimani hisoblaydi?
+ Bajarilgan vazifalar sonini
- Barcha vazifalar sonini
- Bajarilmaganlarni
- Xato
""",
    "DP32": """
? Virtual muhit (venv) nima uchun?
+ Har loyihaning kutubxonalari alohida bo'lishi uchun
- Internetni tezlatish uchun
- Python'ni o'chirish uchun
- Fayllarni yashirish uchun

? Kutubxona qanday o'rnatiladi?
+ pip install requests
- python install requests
- import install requests
- get requests

? requirements.txt nima?
+ Loyiha kutubxonalari ro'yxati
- Kod fayli
- README
- Parollar fayli

? requests.get(URL) nima qiladi?
+ Saytga so'rov yuboradi va javob qaytaradi
- Faylni o'chiradi
- Saytni yaratadi
- Kodni ishga tushiradi

? javob.json() nima qaytaradi?
+ JSON javobni Python list/dict qilib
- HTML sahifani
- Status kodini
- Faylni

? raise_for_status() nima qiladi?
+ Xato status (404, 500) bo'lsa xato chiqaradi
- Statusni chiqaradi
- Javobni o'chiradi
- Hech narsa

? timeout=10 nimani bildiradi?
+ Javobni ko'pi bilan 10 soniya kutish
- 10 marta urinish
- 10 ta natija
- 10 daqiqa

? Internet yo'q bo'lsa requests qanday xato beradi?
+ requests.RequestException turidagi xato
- ValueError
- KeyError
- Xato bermaydi

? f"{77.8193:.2f}" natijasi?
+ "77.82"
- "77.8"
- "78"
- "77.8193"

? Virtual muhitni yoqqanda terminalda nima ko'rinadi?
+ (.venv) belgisi
- [venv]
- Hech narsa
- Xato
""",
    "DP33": """
? Git nima?
+ Kod versiyalarini saqlaydigan tizim
- Dasturlash tili
- Sayt
- Antivirus

? git init nima qiladi?
+ Papkani Git repozitoriyga aylantiradi
- GitHub'ga yuklaydi
- Commit qiladi
- Faylni o'chiradi

? git status nima ko'rsatadi?
+ Qaysi fayllar o'zgargan yoki yangi
- Commitlar tarixi
- GitHub manzili
- Kod xatolari

? git add nima qiladi?
+ O'zgarishni keyingi commit'ga tayyorlaydi
- Commit qiladi
- GitHub'ga yuboradi
- Faylni o'chiradi

? git commit -m "..." nima?
+ Xabar bilan saqlash nuqtasi
- Faylni yuborish
- Yangi branch
- Faylni tiklash

? git log --oneline nima ko'rsatadi?
+ Commitlar tarixi qisqa ko'rinishda
- O'zgargan fayllar
- Branchlar
- Xatolar

? Yaxshi commit xabari qanday?
+ Qisqa va aniq: "JSON bilan saqlash qo'shildi"
- "o'zgarish"
- "aaa"
- Bo'sh

? git config --global user.name nima uchun?
+ Commit muallifini belgilash uchun
- Parol qo'yish uchun
- Repozitoriy nomi uchun
- Shart emas

? git diff nima ko'rsatadi?
+ Hali commit qilinmagan o'zgarishlarni
- Commitlar ro'yxatini
- Fayllar ro'yxatini
- GitHub sahifasini

? git add . nima qiladi?
+ Hamma o'zgargan fayllarni tayyorlaydi
- Bitta faylni
- Hech narsani
- Hammasini o'chiradi
""",
    "DP34": """
? GitHub nima?
+ Git repozitoriylarni internetda saqlash sayti
- Dasturlash tili
- Git'ning boshqa nomi
- Kod muharriri

? git remote add origin URL nima qiladi?
+ Kompyuterdagi repozitoriyni GitHub'dagisi bilan bog'laydi
- GitHub'da repo yaratadi
- Commit qiladi
- Faylni yuklaydi

? git push nima qiladi?
+ Commitlarni GitHub'ga yuboradi
- GitHub'dan olib keladi
- Commit qiladi
- Branch yaratadi

? README.md nima?
+ Loyiha tavsifi, repo sahifasida birinchi ko'rinadi
- Kod fayli
- Parollar fayli
- Xatolar ro'yxati

? Markdown'da # nima?
+ Sarlavha
- Izoh
- Kod
- Havola

? .gitignore nima uchun?
+ GitHub'ga yuklanmaydigan fayllarni ko'rsatish uchun
- Fayllarni o'chirish uchun
- Kodni yashirish uchun
- Repo nomini o'zgartirish uchun

? Qaysi fayl .gitignore'ga albatta yoziladi?
+ .env (parol va tokenlar)
- main.py
- README.md
- requirements.txt

? Nega .venv/ GitHub'ga yuklanmaydi?
+ Katta va keraksiz — requirements.txt yetarli
- Xato beradi
- Maxfiy
- GitHub taqiqlaydi

? git push -u origin main dagi -u nima?
+ Keyingi safar shunchaki git push yozish uchun bog'laydi
- Fayllarni o'chiradi
- Yangi repo yaratadi
- Majburiy yuborish

? GitHub repozitoriysi loyiha uchun nima beradi?
+ Zaxira, portfolio va jamoa bilan ishlash
- Faqat chiroyli ko'rinish
- Kodni tezlashtirish
- Hech narsa
""",
    "DP35": """
? Branch nima?
+ Alohida ish yo'li — asosiy kodni buzmasdan o'zgarish qilish
- Fayl
- Commit
- Server

? git switch -c qidiruv nima qiladi?
+ Yangi branch yaratib, unga o'tadi
- Branch'ni o'chiradi
- main'ga o'tadi
- Commit qiladi

? Pull Request nima?
+ O'zgarishni ko'rib chiqib, main'ga qo'shish so'rovi
- Faylni yuklab olish
- Yangi repo
- Xato hisobot

? Code review nima?
+ Boshqa dasturchi kodni o'qib, fikr bildirishi
- Kodni o'chirish
- Kodni ishga tushirish
- Kodni nusxalash

? Merge nima?
+ Branch o'zgarishlarini boshqa branch'ga birlashtirish
- Branch'ni o'chirish
- Commit'ni bekor qilish
- Fayl yaratish

? git pull nima qiladi?
+ GitHub'dagi yangiliklarni kompyuterga olib keladi
- Kompyuterdagini GitHub'ga yuboradi
- Branch yaratadi
- Faylni o'chiradi

? git branch -d qidiruv nima qiladi?
+ qidiruv branch'ini o'chiradi
- Yangi branch yaratadi
- main'ni o'chiradi
- Commit qiladi

? Nega to'g'ridan-to'g'ri main'ga emas, branch'da ishlaymiz?
+ Asosiy kod buzilmasin va o'zgarish ko'rib chiqilsin
- Git shuni talab qiladi
- Tezroq ishlaydi
- Farqi yo'q

? git push -u origin qidiruv nima qiladi?
+ Yangi branch'ni GitHub'ga yuboradi
- main'ni yuboradi
- Branch'ni o'chiradi
- PR'ni merge qiladi

? Merge conflict nima?
+ Bir qatorni ikki branch har xil o'zgartirgani
- Internet uzilishi
- Fayl yo'qligi
- Commit xabari yo'qligi
""",
    "DP36": """
? Task(**d) nima qiladi?
+ Lug'at kalitlarini parametr sifatida uzatadi
- Lug'atni o'chiradi
- Ikki marta ko'paytiradi
- Xato beradi

? Nega har amaldan keyin saqla() chaqiriladi?
+ Dastur kutilmaganda yopilsa ham ma'lumot qolsin
- Tezroq ishlashi uchun
- Python talab qiladi
- Shart emas

? k.bajar(5) faqat 1 ta vazifa bo'lsa qaysi xato?
+ IndexError
- ValueError
- KeyError
- TypeError

? _yukla dagi pastki chiziq nimani anglatadi?
+ Ichki metod — tashqaridan chaqirilmaydi
- Xato
- Statik metod
- Konstanta

? Loyihada xatolar qanday ushlanadi?
+ try / except (ValueError, IndexError)
- if xato:
- catch Exception
- Ushlanmaydi

? main() funksiyasining vazifasi?
+ Dasturning asosiy oqimi — menyu sikli
- Klass yaratish
- Faylni o'chirish
- Modulni import qilish

? Himoyada nimani ko'rsatish muhim?
+ Ishlaydigan demo va har qatorni tushuntira olish
- Faqat skrinshot
- Faqat GitHub havolasi
- Kod hajmini

? t.__dict__ JSON'ga yozishda nima uchun kerak?
+ Obyektni lug'atga aylantirish uchun
- Obyektni o'chirish uchun
- Obyektni nusxalash uchun
- Shart emas

? 3–5-oylarda o'rganilmagan mavzu qaysi?
+ Telegram bot
- OOP
- JSON
- Git

? Loyihani himoyadan keyin nima qilamiz?
+ Izohlar bo'yicha yaxshilab, GitHub'ga push qilamiz
- O'chirib tashlaymiz
- Hech narsa
- Qaytadan boshlaymiz
""",
}
