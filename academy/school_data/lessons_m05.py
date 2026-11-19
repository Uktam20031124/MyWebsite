"""Dasturchi 5-oy · Fayl, xato, OOP, API, Git — 12 dars "Dars kodi" (kalit — ``dev.py``)."""

from .lesson_kit import lesson, step

M = "5-oy · Fayl, xato, OOP va Git"

TIPS = r'''
import random
from datetime import date, timedelta

maslahatlar = [
    "Har kuni 30 daqiqa kod yozing",
    "Xatoni o'qing — u yo'l ko'rsatadi",
    "Katta masalani kichik qismlarga bo'ling",
]

bugun = date.today()
print("Bugun:", bugun.strftime("%d.%m.%Y"))
print("Kun maslahati:", random.choice(maslahatlar))

hafta_keyin = bugun + timedelta(days=7)
print("Bir haftadan keyin:", hafta_keyin.strftime("%d.%m.%Y"))

yangi_yil = date(bugun.year + 1, 1, 1)
print("Yangi yilgacha:", (yangi_yil - bugun).days, "kun")
print("Zar:", random.randint(1, 6))
'''

UTILS = r'''
def input_int(savol, kichik=None, katta=None):
    while True:
        javob = input(savol)
        try:
            son = int(javob)
        except ValueError:
            print("❌ Butun son kiriting")
            continue
        if kichik is not None and son < kichik:
            print(f"❌ {kichik} dan kichik bo'lmasin")
        elif katta is not None and son > katta:
            print(f"❌ {katta} dan katta bo'lmasin")
        else:
            return son


def bol(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("bol() tugadi")


yosh = input_int("Yoshingiz: ", 5, 100)
print("Qabul qilindi:", yosh)
print(bol(10, 0))
'''

DIARY_TXT = r'''
FAYL = "tasks.txt"


def yukla():
    try:
        with open(FAYL, encoding="utf-8") as f:
            return [qator.strip() for qator in f if qator.strip()]
    except FileNotFoundError:
        return []


def saqla(vazifalar):
    with open(FAYL, "w", encoding="utf-8") as f:
        for v in vazifalar:
            f.write(v + "\n")


vazifalar = yukla()
print("Yuklandi:", len(vazifalar))
yangi = input("Yangi vazifa: ")
vazifalar.append(yangi)
saqla(vazifalar)
print("Saqlandi:", vazifalar)

with open(FAYL, "a", encoding="utf-8") as f:
    f.write("Suv ichish\n")
print("Fayldagi qatorlar:", len(yukla()))
'''

DIARY_JSON = r'''
import json
from datetime import date

FAYL = "tasks.json"


def yukla():
    try:
        with open(FAYL, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def saqla(vazifalar):
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(vazifalar, f, ensure_ascii=False, indent=2)


vazifalar = yukla()
matn = input("Vazifa: ")
vazifalar.append({"matn": matn, "bajarildi": False, "sana": str(date.today())})
saqla(vazifalar)

qayta = yukla()
print("Fayldan o'qildi:", len(qayta), "ta")
print("Birinchisi:", qayta[0]["matn"])
print(json.dumps({"ism": "Ali", "faol": True}, ensure_ascii=False))
'''

MODELS = r'''
class Task:
    def __init__(self, matn, muhim=False):
        self.matn = matn
        self.muhim = muhim
        self.bajarildi = False

    def bajar(self):
        self.bajarildi = True

    def korinish(self):
        belgi = "✔" if self.bajarildi else "☐"
        yulduz = " ⭐" if self.muhim else ""
        return f"{belgi} {self.matn}{yulduz}"


if __name__ == "__main__":
    t1 = Task("Kitob o'qish")
    t2 = Task("Imtihonga tayyorlanish", muhim=True)
    t1.bajar()
    print(t1.korinish())
    print(t2.korinish())
    print(t1.bajarildi, t2.bajarildi)
'''

USERS = r'''
class User:
    def __init__(self, ism):
        self.ism = ism

    def salom(self):
        return f"Salom, {self.ism}!"

    def huquq(self):
        return "o'qish"


class Admin(User):
    def __init__(self, ism, daraja):
        super().__init__(ism)
        self.daraja = daraja

    def huquq(self):
        return "o'qish, yozish, o'chirish"


foydalanuvchilar = [User("Ali"), Admin("Laylo", 2)]
for f in foydalanuvchilar:
    print(f.salom(), "—", f.huquq())
print(isinstance(foydalanuvchilar[1], User))
print("Admin darajasi:", foydalanuvchilar[1].daraja)
'''

MANAGER = r'''
import json


class Task:
    def __init__(self, matn, bajarildi=False):
        self.matn = matn
        self.bajarildi = bajarildi

    def __str__(self):
        belgi = "✔" if self.bajarildi else "☐"
        return f"{belgi} {self.matn}"


class TaskManager:
    def __init__(self):
        self._vazifalar = []

    def qosh(self, matn):
        if not matn.strip():
            raise ValueError("Bo'sh vazifa")
        self._vazifalar.append(Task(matn.strip()))

    @property
    def bajarilgan(self):
        return sum(1 for t in self._vazifalar if t.bajarildi)

    def __len__(self):
        return len(self._vazifalar)

    def __getitem__(self, i):
        return self._vazifalar[i]

    def to_json(self):
        return json.dumps([t.__dict__ for t in self._vazifalar], ensure_ascii=False)


menejer = TaskManager()
menejer.qosh("Kitob o'qish")
menejer.qosh("Sport")
menejer[0].bajarildi = True
print("Jami:", len(menejer), "| bajarilgan:", menejer.bajarilgan)
for t in menejer:
    print(t)
try:
    menejer.qosh("   ")
except ValueError as e:
    print("Xato:", e)
print(menejer.to_json())
'''

CURRENCY = r'''
import requests

URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


def kurslar():
    javob = requests.get(URL, timeout=10)
    javob.raise_for_status()
    return {k["Ccy"]: float(k["Rate"]) for k in javob.json()}


def main():
    try:
        data = kurslar()
    except requests.RequestException:
        print("Internet yoki sayt bilan muammo")
        return
    summa = float(input("Summa (so'm): "))
    for kod in ("USD", "EUR", "RUB"):
        print(f"{kod}: {summa / data[kod]:.2f}")


if __name__ == "__main__":
    main()
'''

GIT_LOG = r'''
git config --global user.name "Ali Valiyev"
git config --global user.email "ali@example.com"
cd kundalik
git init
git status
git add diary.py
git commit -m "Kundalik: birinchi versiya"
git add .
git commit -m "JSON bilan saqlash"
git log --oneline
git diff
'''

README = r'''
# Kundalik

Konsolda ishlaydigan vazifalar ro'yxati: qo'shish, bajarildi, o'chirish.
Ma'lumot `kundalik.json` faylida saqlanadi.

## Ishga tushirish

```
python main.py
```

## Muallif
Ali Valiyev · Minar Dasturchi, 5-oy
'''

GITIGNORE = r'''
__pycache__/
.venv/
*.json
.env
'''

GIT_PUSH = r'''
git remote add origin https://github.com/ali/kundalik.git
git branch -M main
git push -u origin main
git add README.md .gitignore
git commit -m "README va .gitignore"
git push
'''

GIT_BRANCH = r'''
git switch -c qidiruv
git add main.py
git commit -m "Vazifa qidirish qo'shildi"
git push -u origin qidiruv
git switch main
git pull
git branch -d qidiruv
'''

FINAL = r'''
import json

FAYL = "kundalik.json"


class Task:
    def __init__(self, matn, bajarildi=False):
        self.matn = matn
        self.bajarildi = bajarildi

    def __str__(self):
        belgi = "✔" if self.bajarildi else "☐"
        return f"{belgi} {self.matn}"


class Kundalik:
    def __init__(self, fayl=FAYL):
        self.fayl = fayl
        self.vazifalar = self._yukla()

    def _yukla(self):
        try:
            with open(self.fayl, encoding="utf-8") as f:
                return [Task(**d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def saqla(self):
        data = [t.__dict__ for t in self.vazifalar]
        with open(self.fayl, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def qosh(self, matn):
        self.vazifalar.append(Task(matn))
        self.saqla()

    def bajar(self, raqam):
        self.vazifalar[raqam - 1].bajarildi = True
        self.saqla()


def main():
    k = Kundalik()
    while True:
        tanlov = input("1) Qo'shish 2) Ro'yxat 3) Bajarildi 0) Chiqish: ")
        if tanlov == "1":
            k.qosh(input("Vazifa: "))
        elif tanlov == "2":
            for n, t in enumerate(k.vazifalar, start=1):
                print(f"{n}. {t}")
        elif tanlov == "3":
            try:
                k.bajar(int(input("Raqam: ")))
            except (ValueError, IndexError):
                print("Noto'g'ri raqam")
        elif tanlov == "0":
            print("Saqlandi. Xayr! 👋")
            break


if __name__ == "__main__":
    main()
'''

LESSONS = {
    "DP25": lesson(
        M, 1, "Modullar: random va datetime",
        "Tayyor modullardan foydalanamiz: tasodifiy tanlov va sana bilan hisoblash.",
        "3-oyda: import random va randint (“Sonni top”).",
        "random.randint(1, 6) qaysi sonlarni berishi mumkin?",
        "Modul — tayyor kod fayli; import va from ... import; random.choice; date, timedelta, strftime.",
        "Tug'ilgan kuningizgacha necha kun qolganini hisoblang.",
        [("📦", "import", "random, datetime", "mem"),
         ("🎲", "choice", "ro'yxatdan tasodifiy", ""),
         ("📅", "date.today()", "bugungi sana", ""),
         ("➕", "timedelta", "7 kundan keyin", ""),
         ("➖", "sana − sana", ".days", "")],
        [
            step("tips.py", "Modullarni ulaymiz va tasodifiy tanlaymiz", r'''
import random
from datetime import date, timedelta

maslahatlar = [
    "Har kuni 30 daqiqa kod yozing",
    "Xatoni o'qing — u yo'l ko'rsatadi",
    "Katta masalani kichik qismlarga bo'ling",
]''',
                 [("import random", "butun modul: random.choice(...) deb ishlatamiz."),
                  ("from datetime import ...", "faqat kerakli nomlar: to'g'ridan-to'g'ri date(...)."),
                  ("ro'yxat", "maslahatlar — tanlov uchun.")],
                 "(modullar tayyor)"),
            step("tips.py", "Bugungi sana va tasodifiy maslahat", r'''
bugun = date.today()
print("Bugun:", bugun.strftime("%d.%m.%Y"))
print("Kun maslahati:", random.choice(maslahatlar))''',
                 [("date.today()", "kompyuterdagi bugungi sana."),
                  ("strftime(\"%d.%m.%Y\")", "sanani matnga: 19.11.2026."),
                  ("random.choice", "ro'yxatdan tasodifiy bitta element.")],
                 "Bugun: 19.11.2026\nKun maslahati: Har kuni 30 daqiqa kod yozing"),
            step("tips.py", "Sanalar bilan hisoblash", r'''
hafta_keyin = bugun + timedelta(days=7)
print("Bir haftadan keyin:", hafta_keyin.strftime("%d.%m.%Y"))

yangi_yil = date(bugun.year + 1, 1, 1)
print("Yangi yilgacha:", (yangi_yil - bugun).days, "kun")
print("Zar:", random.randint(1, 6))''',
                 [("timedelta(days=7)", "muddat — sanaga qo'shish mumkin."),
                  ("date(yil, oy, kun)", "aniq sana yaratish."),
                  ("(a − b).days", "ikki sana orasidagi kunlar.")],
                 "Bir haftadan keyin: 26.11.2026\nYangi yilgacha: 43 kun\nZar: 4"),
        ],
        {"tips.py": TIPS},
        [("kundalik/", ""), ("└── tips.py", "yangi")],
        ["import va from ... import", "random.choice va randint", "date, timedelta", "strftime"],
        ["Majburiy: tug'ilgan kuningizgacha necha kun qolganini hisoblang.",
         "Qo'shimcha: math modulidan sqrt va ceil bilan 2 ta misol yozing."],
        "5.2 · Xatolar bilan ishlash: try / except.",
        run={"file": "tips.py", "input": "", "randint": 4, "expect": ["Kun maslahati:", "Yangi yilgacha:", "Zar: 4"]},
    ),
    "DP26": lesson(
        M, 2, "Xatolar bilan ishlash: try / except",
        "Dastur noto'g'ri kiritishdan yiqilmasin: xavfsiz input_int() yozamiz.",
        "O'tgan darsda: modullar, random va datetime.",
        "int(\"o'n\") nima beradi? (3-oyda ko'rgan ValueError)",
        "try / except XatoTuri / finally; ValueError, ZeroDivisionError; xatoni ushlab qayta so'rash.",
        "input_float() va oraliq tekshiruvchi funksiya yozing.",
        [("⌨", "input", "\"o'n\"", ""),
         ("🛡", "try", "int(javob)", "mem"),
         ("⚠", "except", "ValueError", "loop"),
         ("📏", "Chegara", "5–100", ""),
         ("✅", "return", "to'g'ri son", "")],
        [
            step("utils.py", "try / except bilan ushlash", r'''
def input_int(savol, kichik=None, katta=None):
    while True:
        javob = input(savol)
        try:
            son = int(javob)
        except ValueError:
            print("❌ Butun son kiriting")
            continue''',
                 [("try:", "xato bo'lishi mumkin bo'lgan kod."),
                  ("except ValueError:", "aynan shu xato bo'lsa — dastur yiqilmaydi."),
                  ("continue", "qayta so'raymiz.")],
                 "Yoshingiz: o'n\n❌ Butun son kiriting"),
            step("utils.py", "Chegarani tekshiramiz", r'''
        if kichik is not None and son < kichik:
            print(f"❌ {kichik} dan kichik bo'lmasin")
        elif katta is not None and son > katta:
            print(f"❌ {katta} dan katta bo'lmasin")
        else:
            return son''',
                 [("kichik=None", "chegara ixtiyoriy — berilmasa tekshirilmaydi."),
                  ("is not None", "0 ham to'g'ri chegara bo'lishi mumkin."),
                  ("return son", "to'g'ri qiymat — sikldan chiqamiz.")],
                 "Yoshingiz: 150\n❌ 100 dan katta bo'lmasin\nYoshingiz: 13"),
            step("utils.py", "finally va ishlatish", r'''
def bol(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("bol() tugadi")


yosh = input_int("Yoshingiz: ", 5, 100)
print("Qabul qilindi:", yosh)
print(bol(10, 0))''',
                 [("ZeroDivisionError", "nolga bo'lish xatosi."),
                  ("finally:", "har doim bajariladi — xato bo'lsa ham."),
                  ("qayta ishlatish", "input_int endi istalgan dasturda.")],
                 "Qabul qilindi: 13\nbol() tugadi\nNone"),
        ],
        {"utils.py": UTILS},
        [("kundalik/", ""), ("├── tips.py", ""), ("└── utils.py", "yangi")],
        ["try / except", "ValueError, ZeroDivisionError", "finally", "Xavfsiz kiritish funksiyasi"],
        ["Majburiy: input_float() va input_range(savol, a, b) yozing.",
         "Qo'shimcha: raise ValueError bilan manfiy yoshni rad eting."],
        "5.3 · Txt fayllar: o'qish va yozish.",
        run={"file": "utils.py", "input": "o'n\n150\n13\n", "expect": ["❌ Butun son kiriting", "❌ 100 dan katta bo'lmasin", "Qabul qilindi: 13", "bol() tugadi", "None"]},
    ),
    "DP27": lesson(
        M, 3, "Txt fayllar: o'qish va yozish",
        "Kundalik yopilganda vazifalar yo'qolmasin: ularni faylga saqlaymiz.",
        "O'tgan darsda: try / except, xavfsiz kiritish.",
        "except qachon bajariladi?",
        "open(fayl, rejim, encoding), with — avtomatik yopish; \"r\", \"w\", \"a\" rejimlari; FileNotFoundError.",
        "Dastur ochilganda vazifalar sonini va oxirgi vazifani ko'rsating.",
        [("📄", "tasks.txt", "fayl", "mem"),
         ("📖", "\"r\"", "yuklash", ""),
         ("✍", "\"w\"", "saqlash", ""),
         ("➕", "\"a\"", "oxiriga qo'shish", ""),
         ("🛡", "FileNotFoundError", "birinchi marta", "")],
        [
            step("diary.py", "Fayldan yuklash", r'''
FAYL = "tasks.txt"


def yukla():
    try:
        with open(FAYL, encoding="utf-8") as f:
            return [qator.strip() for qator in f if qator.strip()]
    except FileNotFoundError:
        return []''',
                 [("with open(...) as f:", "blok tugagach fayl o'zi yopiladi."),
                  ("encoding=\"utf-8\"", "o‘, g‘ harflari buzilmasligi uchun."),
                  ("FileNotFoundError", "birinchi ishga tushirishda fayl yo'q — bo'sh ro'yxat.")],
                 "Yuklandi: 0"),
            step("diary.py", "Faylga yozish", r'''
def saqla(vazifalar):
    with open(FAYL, "w", encoding="utf-8") as f:
        for v in vazifalar:
            f.write(v + "\n")''',
                 [("\"w\"", "yozish — eski mazmun <b>o'chadi</b>, butun ro'yxat qayta yoziladi."),
                  ("\"\\n\"", "har vazifa alohida qatorda.")],
                 "tasks.txt:\nKitob o'qish"),
            step("diary.py", "Ishlatish va \"a\" rejimi", r'''
vazifalar = yukla()
print("Yuklandi:", len(vazifalar))
yangi = input("Yangi vazifa: ")
vazifalar.append(yangi)
saqla(vazifalar)
print("Saqlandi:", vazifalar)

with open(FAYL, "a", encoding="utf-8") as f:
    f.write("Suv ichish\n")
print("Fayldagi qatorlar:", len(yukla()))''',
                 [("yukla → o'zgartir → saqla", "fayl bilan ishlashning oddiy tartibi."),
                  ("\"a\"", "append — oxiriga qo'shadi, eskisi qoladi.")],
                 "Yangi vazifa: Kitob o'qish\nSaqlandi: [\"Kitob o'qish\"]\nFayldagi qatorlar: 2"),
        ],
        {"diary.py": DIARY_TXT},
        [("kundalik/", ""), ("├── diary.py", "o‘zgardi"), ("└── tasks.txt", "yangi")],
        ["open va with", "r, w, a rejimlari", "encoding=\"utf-8\"", "FileNotFoundError"],
        ["Majburiy: ochilganda vazifalar soni va oxirgi vazifani ko'rsating.",
         "Qo'shimcha: “tozalash” buyrug'i — faylni bo'shatish."],
        "5.4 · JSON bilan ishlash.",
        run={"file": "diary.py", "input": "Kitob o'qish\n", "expect": ["Yuklandi: 0", 'Saqlandi: ["Kitob o\'qish"]', "Fayldagi qatorlar: 2"]},
    ),
    "DP28": lesson(
        M, 4, "JSON bilan ishlash",
        "Vazifani matn, holat va sana bilan saqlaymiz — JSON formatida.",
        "O'tgan darsda: txt fayl, with, r / w / a.",
        "\"w\" rejimi eski mazmun bilan nima qiladi?",
        "JSON — dict va list'ni matnga aylantirish; json.dump / json.load, dumps / loads; ensure_ascii, indent.",
        "Har vazifaga muddat (sana) qo'shing.",
        [("📒", "list[dict]", "Python", ""),
         ("➡", "json.dump", "faylga", "mem"),
         ("📄", "tasks.json", "matn", ""),
         ("⬅", "json.load", "qaytib", ""),
         ("🔁", "true ↔ True", "moslik", "")],
        [
            step("diary.py", "JSON yuklash va saqlash", r'''
import json
from datetime import date

FAYL = "tasks.json"


def yukla():
    try:
        with open(FAYL, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def saqla(vazifalar):
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(vazifalar, f, ensure_ascii=False, indent=2)''',
                 [("json.load(f)", "fayldagi JSON → Python list/dict."),
                  ("json.dump(x, f)", "Python → faylga JSON."),
                  ("ensure_ascii=False", "o'zbekcha harflar \\u kodsiz saqlanadi; indent=2 — chiroyli.")],
                 "(fayl bilan ishlovchi 2 funksiya)"),
            step("diary.py", "Lug'at qo'shib saqlaymiz", r'''
vazifalar = yukla()
matn = input("Vazifa: ")
vazifalar.append({"matn": matn, "bajarildi": False, "sana": str(date.today())})
saqla(vazifalar)''',
                 [("lug'at", "endi vazifada 3 ta ma'lumot."),
                  ("str(date.today())", "sana JSON'da matn bo'lib saqlanadi.")],
                 "tasks.json:\n[\n  {\"matn\": \"Kitob o'qish\", \"bajarildi\": false, ...}\n]"),
            step("diary.py", "Qayta o'qish va dumps", r'''
qayta = yukla()
print("Fayldan o'qildi:", len(qayta), "ta")
print("Birinchisi:", qayta[0]["matn"])
print(json.dumps({"ism": "Ali", "faol": True}, ensure_ascii=False))''',
                 [("False → false", "JSON'da kichik harf; None → null."),
                  ("dumps / loads", "s — satr bilan ishlaydi (faylsiz).")],
                 "Fayldan o'qildi: 1 ta\nBirinchisi: Kitob o'qish\n{\"ism\": \"Ali\", \"faol\": true}"),
        ],
        {"diary.py": DIARY_JSON},
        [("kundalik/", ""), ("├── diary.py", "o‘zgardi"), ("└── tasks.json", "yangi")],
        ["json.dump va json.load", "dumps va loads", "ensure_ascii, indent", "Python ↔ JSON moslik"],
        ["Majburiy: vazifaga muddat qo'shing va muddati o'tganlarini belgilang.",
         "Qo'shimcha: buzilgan JSON faylda dastur yiqilmasligini sinang."],
        "5.5 · OOP: class, __init__ va metodlar.",
        run={"file": "diary.py", "input": "Kitob o'qish\n", "expect": ["Fayldan o'qildi: 1 ta", "Birinchisi: Kitob o'qish", "{\"ism\": \"Ali\", \"faol\": true}"]},
    ),
    "DP29": lesson(
        M, 5, "OOP: class, __init__ va metodlar",
        "Vazifani obyektga aylantiramiz: ma'lumot va harakat bir joyda.",
        "O'tgan darsda: JSON, vazifa — lug'at.",
        "Vazifa lug'atida qanday kalitlar bor edi?",
        "class — chizma, obyekt — undan yasalgan narsa; __init__, self, atribut va metod.",
        "Task'ga muddat atributi va muddati_otdimi() metodini qo'shing.",
        [("📐", "class Task", "chizma", "mem"),
         ("🛠", "__init__", "atributlar", ""),
         ("🙋", "self", "obyektning o'zi", ""),
         ("⚙", "metod", "bajar(), korinish()", ""),
         ("📦", "Obyektlar", "t1, t2", "")],
        [
            step("models.py", "Klass va __init__", r'''
class Task:
    def __init__(self, matn, muhim=False):
        self.matn = matn
        self.muhim = muhim
        self.bajarildi = False''',
                 [("class Task:", "nom PascalCase: Task, TaskManager."),
                  ("__init__", "obyekt yaratilganda avtomatik chaqiriladi."),
                  ("self.matn", "atribut — obyektning ma'lumoti.")],
                 "Task(\"Kitob o'qish\") → matn, muhim, bajarildi"),
            step("models.py", "Metodlar", r'''
    def bajar(self):
        self.bajarildi = True

    def korinish(self):
        belgi = "✔" if self.bajarildi else "☐"
        yulduz = " ⭐" if self.muhim else ""
        return f"{belgi} {self.matn}{yulduz}"''',
                 [("metod", "klass ichidagi funksiya — obyekt bajaradigan ish."),
                  ("self", "har metodning birinchi parametri — o'sha obyekt."),
                  ("holat", "bajar() obyektning o'z atributini o'zgartiradi.")],
                 "t.bajar() → t.bajarildi = True"),
            step("models.py", "Obyektlar yaratamiz", r'''
if __name__ == "__main__":
    t1 = Task("Kitob o'qish")
    t2 = Task("Imtihonga tayyorlanish", muhim=True)
    t1.bajar()
    print(t1.korinish())
    print(t2.korinish())
    print(t1.bajarildi, t2.bajarildi)''',
                 [("Task(...)", "obyekt yaratish — __init__ ishlaydi."),
                  ("mustaqil", "t1 o'zgarsa t2 o'zgarmaydi."),
                  ("__name__ == \"__main__\"", "fayl to'g'ridan-to'g'ri ishga tushganda.")],
                 "✔ Kitob o'qish\n☐ Imtihonga tayyorlanish ⭐\nTrue False"),
        ],
        {"models.py": MODELS},
        [("kundalik/", ""), ("├── diary.py", ""), ("└── models.py", "yangi")],
        ["class va obyekt", "__init__ va self", "Atribut va metod", "if __name__ == \"__main__\""],
        ["Majburiy: Task'ga muddat va muddati_otdimi() qo'shing.",
         "Qo'shimcha: Talaba klassi — ism, baholar, orta() metodi."],
        "5.6 · OOP: vorislik.",
        run={"file": "models.py", "input": "", "expect": ["✔ Kitob o'qish", "☐ Imtihonga tayyorlanish ⭐", "True False"]},
    ),
    "DP30": lesson(
        M, 6, "OOP: vorislik",
        "Tayyor klassni kengaytiramiz: oddiy foydalanuvchi va admin.",
        "O'tgan darsda: class, __init__, self, metod.",
        "self nima?",
        "class Admin(User) — vorislik; super().__init__(); metodni qayta yozish (overriding); isinstance; polimorfizm.",
        "Admin'ga delete_user() metodini qo'shing.",
        [("👤", "User", "ism, salom()", ""),
         ("⬇", "Admin(User)", "voris", "mem"),
         ("🔁", "super()", "ota __init__", ""),
         ("✏", "huquq()", "qayta yozilgan", ""),
         ("🎭", "Polimorfizm", "bir xil chaqiruv", "")],
        [
            step("users.py", "Ota klass", r'''
class User:
    def __init__(self, ism):
        self.ism = ism

    def salom(self):
        return f"Salom, {self.ism}!"

    def huquq(self):
        return "o'qish"''',
                 [("User", "umumiy narsalar — ota klassda."),
                  ("salom()", "hamma foydalanuvchida bir xil.")],
                 "User(\"Ali\").huquq() → o'qish"),
            step("users.py", "Voris klass va super()", r'''
class Admin(User):
    def __init__(self, ism, daraja):
        super().__init__(ism)
        self.daraja = daraja

    def huquq(self):
        return "o'qish, yozish, o'chirish"''',
                 [("Admin(User)", "Admin User'ning hamma metodlarini oladi."),
                  ("super().__init__", "ota klass ishini takrorlamaymiz."),
                  ("huquq()", "overriding — vorisda o'zgacha ishlaydi.")],
                 "Admin(\"Laylo\", 2).salom() → Salom, Laylo!"),
            step("users.py", "Polimorfizm", r'''
foydalanuvchilar = [User("Ali"), Admin("Laylo", 2)]
for f in foydalanuvchilar:
    print(f.salom(), "—", f.huquq())
print(isinstance(foydalanuvchilar[1], User))
print("Admin darajasi:", foydalanuvchilar[1].daraja)''',
                 [("bir xil chaqiruv", "f.huquq() — har obyekt o'z javobini beradi."),
                  ("isinstance", "Admin ham User hisoblanadi.")],
                 "Salom, Ali! — o'qish\nSalom, Laylo! — o'qish, yozish, o'chirish\nTrue\nAdmin darajasi: 2"),
        ],
        {"users.py": USERS},
        [("kundalik/", ""), ("├── models.py", ""), ("└── users.py", "yangi")],
        ["Vorislik", "super().__init__()", "Overriding", "isinstance va polimorfizm"],
        ["Majburiy: Admin'ga delete_user(user, royxat) metodini qo'shing.",
         "Qo'shimcha: Hayvon → Mushuk, Kuchuk: ovoz() metodi."],
        "5.7 · OOP: property va maxsus metodlar.",
        run={"file": "users.py", "input": "", "expect": ["Salom, Ali! — o'qish", "Salom, Laylo! — o'qish, yozish, o'chirish", "Admin darajasi: 2"]},
    ),
    "DP31": lesson(
        M, 7, "OOP: property va maxsus metodlar",
        "Vazifalarni boshqaradigan TaskManager klassi: property, __str__, __len__ va xatolar.",
        "O'tgan darsda: vorislik, super(), polimorfizm.",
        "super().__init__() nima qiladi?",
        "__str__ — print uchun; __len__ — len(); __getitem__ — [i] va for; @property; _ — ichki atribut; raise.",
        "TaskManager'ga search(soz) metodini qo'shing.",
        [("📦", "TaskManager", "_vazifalar", "mem"),
         ("🖨", "__str__", "print(t)", ""),
         ("📏", "__len__", "len(m)", ""),
         ("🔢", "@property", "m.bajarilgan", ""),
         ("⚠", "raise", "bo'sh vazifa", "")],
        [
            step("diary.py", "Task va __str__", r'''
class Task:
    def __init__(self, matn, bajarildi=False):
        self.matn = matn
        self.bajarildi = bajarildi

    def __str__(self):
        belgi = "✔" if self.bajarildi else "☐"
        return f"{belgi} {self.matn}"''',
                 [("__str__", "print(t) shu metodni chaqiradi."),
                  ("bajarildi=False", "JSON'dan yuklashda holatni ham berish mumkin.")],
                 "print(Task(\"Sport\")) → ☐ Sport"),
            step("diary.py", "TaskManager: raise va property", r'''
class TaskManager:
    def __init__(self):
        self._vazifalar = []

    def qosh(self, matn):
        if not matn.strip():
            raise ValueError("Bo'sh vazifa")
        self._vazifalar.append(Task(matn.strip()))

    @property
    def bajarilgan(self):
        return sum(1 for t in self._vazifalar if t.bajarildi)''',
                 [("_vazifalar", "pastki chiziq — “ichki, tashqaridan tegmang”."),
                  ("raise ValueError", "noto'g'ri qiymatda o'zimiz xato chiqaramiz."),
                  ("@property", "metodni atribut kabi o'qish: m.bajarilgan (qavssiz).")],
                 "m.qosh(\"   \") → ValueError: Bo'sh vazifa"),
            step("diary.py", "__len__, __getitem__ va ishlatish", r'''
    def __len__(self):
        return len(self._vazifalar)

    def __getitem__(self, i):
        return self._vazifalar[i]

    def to_json(self):
        return json.dumps([t.__dict__ for t in self._vazifalar], ensure_ascii=False)


menejer = TaskManager()
menejer.qosh("Kitob o'qish")
menejer.qosh("Sport")
menejer[0].bajarildi = True
print("Jami:", len(menejer), "| bajarilgan:", menejer.bajarilgan)
for t in menejer:
    print(t)''',
                 [("__len__", "len(menejer) ishlaydi."),
                  ("__getitem__", "menejer[0] va for t in menejer ishlaydi."),
                  ("t.__dict__", "obyekt atributlari lug'at ko'rinishida — JSON uchun.")],
                 "Jami: 2 | bajarilgan: 1\n✔ Kitob o'qish\n☐ Sport"),
        ],
        {"diary.py": MANAGER},
        [("kundalik/", ""), ("├── users.py", ""), ("└── diary.py", "o‘zgardi")],
        ["__str__, __len__, __getitem__", "@property", "_ichki atribut", "raise ValueError"],
        ["Majburiy: TaskManager'ga search(soz) metodini qo'shing.",
         "Qo'shimcha: from_json(matn) — klass metodi (@classmethod)."],
        "5.8 · venv, pip va API: valyuta kursi.",
        run={"file": "diary.py", "input": "", "expect": ["Jami: 2 | bajarilgan: 1", "✔ Kitob o'qish", "Xato: Bo'sh vazifa", "\"matn\": \"Sport\""]},
    ),
    "DP32": lesson(
        M, 8, "venv, pip va API: valyuta kursi",
        "Internetdan ma'lumot olamiz: Markaziy bank API'sidan valyuta kursi.",
        "O'tgan darsda: OOP, JSON.",
        "json.loads nima qiladi?",
        "Virtual muhit (venv), pip install, requests.get, JSON javob, status kodi, timeout va xatolar.",
        "So'mni dollar va yevroga o'tkazuvchi konvertor yozing.",
        [("🧪", "venv", "alohida muhit", ""),
         ("📥", "pip install", "requests", ""),
         ("🌐", "requests.get", "cbu.uz", "mem"),
         ("📄", "JSON javob", "Ccy, Rate", ""),
         ("💱", "Hisob", "so'm ÷ kurs", "")],
        [
            step("Terminal", "Virtual muhit va kutubxona", r'''
$ python -m venv .venv
$ .venv\Scripts\activate        (Windows)
$ source .venv/bin/activate     (Linux/Mac)
(.venv) $ pip install requests
(.venv) $ pip freeze > requirements.txt''',
                 [("venv", "har loyihaning o'z kutubxonalari — bir-biriga xalal bermaydi."),
                  ("pip install", "tashqi kutubxona o'rnatish."),
                  ("requirements.txt", "loyiha kutubxonalari ro'yxati.")],
                 "Successfully installed requests-2.32"),
            step("currency.py", "API'dan ma'lumot olamiz", r'''
import requests

URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"


def kurslar():
    javob = requests.get(URL, timeout=10)
    javob.raise_for_status()
    return {k["Ccy"]: float(k["Rate"]) for k in javob.json()}''',
                 [("requests.get", "saytga so'rov yuboradi, javob qaytaradi."),
                  ("raise_for_status()", "xato status (404, 500) bo'lsa — xato chiqaradi."),
                  ("javob.json()", "JSON → Python ro'yxati; lug'atga aylantiramiz.")],
                 "{'USD': 12850.5, 'EUR': 13540.2, 'RUB': 128.4, ...}"),
            step("currency.py", "Xatolarni ushlab hisoblaymiz", r'''
def main():
    try:
        data = kurslar()
    except requests.RequestException:
        print("Internet yoki sayt bilan muammo")
        return
    summa = float(input("Summa (so'm): "))
    for kod in ("USD", "EUR", "RUB"):
        print(f"{kod}: {summa / data[kod]:.2f}")''',
                 [("RequestException", "internet yo'q, sayt ishlamayapti — dastur yiqilmaydi."),
                  ("timeout=10", "10 soniyadan ko'p kutmaymiz."),
                  (":.2f", "verguldan keyin 2 xona.")],
                 "Summa (so'm): 1000000\nUSD: 77.82\nEUR: 73.85\nRUB: 7788.16"),
        ],
        {"currency.py": CURRENCY, "requirements.txt": "requests==2.32.3\n"},
        [("kundalik/", ""), ("├── .venv/", "yangi"), ("├── currency.py", "yangi"), ("└── requirements.txt", "yangi")],
        ["Virtual muhit", "pip va requirements.txt", "requests.get va JSON javob", "Tarmoq xatolarini ushlash"],
        ["Majburiy: so'mni USD va EUR ga, va aksincha o'tkazuvchi menyu yozing.",
         "Qo'shimcha: kursni sana bilan tasks.json kabi faylga saqlang."],
        "5.9 · Git: init, add, commit, log.",
    ),
    "DP33": lesson(
        M, 9, "Git: init, add, commit, log",
        "Kodning har bir holatini saqlab boramiz: Git — vaqt mashinasi.",
        "O'tgan darsda: venv, pip, API.",
        "requirements.txt nima uchun kerak?",
        "Git — versiyalar tizimi; repozitoriy; status, add (tayyorlash), commit (saqlash nuqtasi), log, diff.",
        "Kundalikka 3 ta o'zgarish kiritib, har birini alohida commit qiling.",
        [("📁", "git init", "repozitoriy", ""),
         ("🔍", "git status", "nima o'zgardi", ""),
         ("📥", "git add", "tayyorlash", "mem"),
         ("💾", "git commit", "saqlash nuqtasi", ""),
         ("📜", "git log", "tarix", "")],
        [
            step("Terminal", "Sozlash va repozitoriy", r'''
$ git config --global user.name "Ali Valiyev"
$ git config --global user.email "ali@example.com"
$ cd kundalik
$ git init
Initialized empty Git repository in kundalik/.git/''',
                 [("git config", "bir marta: commit muallifi kim."),
                  ("git init", "papkani repozitoriyga aylantiradi (.git papkasi)."),
                  ("faqat bir marta", "har loyihada bir marta init qilinadi.")],
                 "Initialized empty Git repository"),
            step("Terminal", "status, add va commit", r'''
$ git status
Untracked files: diary.py
$ git add diary.py
$ git commit -m "Kundalik: birinchi versiya"
[main (root-commit) 3f2a1c9] Kundalik: birinchi versiya''',
                 [("status", "qaysi fayllar o'zgargan yoki yangi."),
                  ("add", "keyingi commit'ga tayyorlash (staging)."),
                  ("commit -m", "saqlash nuqtasi + qisqa, aniq xabar.")],
                 "1 file changed, 54 insertions(+)"),
            step("Terminal", "Tarix va farqlar", r'''
$ git add .
$ git commit -m "JSON bilan saqlash"
$ git log --oneline
a81d0e4 JSON bilan saqlash
3f2a1c9 Kundalik: birinchi versiya
$ git diff''',
                 [("git add .", "hamma o'zgargan fayllar."),
                  ("log --oneline", "commitlar tarixi — har biri o'z kodi bilan."),
                  ("diff", "hali commit qilinmagan o'zgarishlar.")],
                 "a81d0e4 JSON bilan saqlash\n3f2a1c9 Kundalik: birinchi versiya"),
        ],
        {"git-buyruqlar.txt": GIT_LOG},
        [("kundalik/", ""), ("├── .git/", "yangi"), ("├── diary.py", ""), ("└── models.py", "")],
        ["Git va repozitoriy", "status, add, commit", "log va diff", "Yaxshi commit xabari"],
        ["Majburiy: 3 ta o'zgarish — 3 ta alohida commit, git log skrinshoti.",
         "Qo'shimcha: git restore bilan o'zgarishni bekor qilib ko'ring."],
        "5.10 · GitHub: repozitoriy, push, README, .gitignore.",
    ),
    "DP34": lesson(
        M, 10, "GitHub: repozitoriy, push, README, .gitignore",
        "Loyihani internetga joylaymiz: GitHub repozitoriysi va README.",
        "O'tgan darsda: git init, add, commit, log.",
        "git add va git commit farqi nima?",
        "GitHub — Git repozitoriylar sayti; remote, push; README.md — loyiha tavsifi; .gitignore — yuklanmaydigan fayllar.",
        "README'ga skrinshot va ishga tushirish yo'riqnomasini qo'shing.",
        [("🌐", "GitHub repo", "kundalik", ""),
         ("🔗", "remote add", "bog'lash", ""),
         ("⬆", "git push", "yuborish", "mem"),
         ("📝", "README.md", "tavsif", ""),
         ("🙈", ".gitignore", "maxfiy fayllar", "")],
        [
            step("Terminal", "Repozitoriyni bog'lab yuborish", r'''
$ git remote add origin https://github.com/ali/kundalik.git
$ git branch -M main
$ git push -u origin main''',
                 [("remote add origin", "kompyuterdagi repo ↔ GitHub'dagi repo."),
                  ("push -u", "birinchi yuborish; keyin shunchaki git push."),
                  ("login", "GitHub so'raganda — token yoki brauzer orqali kirish.")],
                 "To github.com/ali/kundalik.git\n * [new branch] main -> main"),
            step("README.md", "Loyiha tavsifi", r'''
# Kundalik

Konsolda ishlaydigan vazifalar ro'yxati: qo'shish, bajarildi, o'chirish.
Ma'lumot `kundalik.json` faylida saqlanadi.

## Ishga tushirish''',
                 [("# sarlavha", "Markdown: # — sarlavha, `kod` — kod."),
                  ("README", "repo sahifasida birinchi ko'rinadi — loyihaning “vizitkasi”.")],
                 "GitHub'da chiroyli sahifa"),
            step(".gitignore", "Yuklanmaydigan fayllar", r'''
__pycache__/
.venv/
*.json
.env''',
                 [(".venv/", "kutubxonalar — requirements.txt yetarli."),
                  ("*.json", "shaxsiy ma'lumot GitHub'ga chiqmasin."),
                  (".env", "parol va tokenlar — hech qachon!")],
                 "git status: bu fayllar endi ko'rinmaydi"),
        ],
        {"README.md": README, ".gitignore": GITIGNORE, "git-buyruqlar.txt": GIT_PUSH},
        [("kundalik/", ""), ("├── README.md", "yangi"), ("├── .gitignore", "yangi"), ("└── diary.py", "")],
        ["GitHub repozitoriy", "remote va push", "README.md (Markdown)", ".gitignore"],
        ["Majburiy: README'ga skrinshot va “Ishga tushirish” bo'limini yozing.",
         "Qo'shimcha: GitHub profilingizga o'zingiz haqingizda README qo'shing."],
        "5.11 · Branch va Pull Request.",
    ),
    "DP35": lesson(
        M, 11, "Branch va Pull Request",
        "Jamoada ishlaymiz: alohida branch'da o'zgarish va Pull Request orqali birlashtirish.",
        "O'tgan darsda: GitHub, push, README.",
        ".gitignore ga nega .env yoziladi?",
        "Branch — alohida ish yo'li; switch -c; push -u; Pull Request — ko'rib chiqish va merge; pull.",
        "Do'stingizning PR'iga sharh yozing va merge qiling.",
        [("🌿", "git switch -c", "yangi branch", ""),
         ("💾", "commit", "o'zgarish", ""),
         ("⬆", "push -u", "GitHub'ga", ""),
         ("🔀", "Pull Request", "ko'rib chiqish", "mem"),
         ("✅", "merge + pull", "main yangilandi", "")],
        [
            step("Terminal", "Yangi branch'da ishlash", r'''
$ git switch -c qidiruv
Switched to a new branch 'qidiruv'
$ git add main.py
$ git commit -m "Vazifa qidirish qo'shildi"''',
                 [("switch -c", "yangi branch yaratib, unga o'tadi."),
                  ("main tegilmaydi", "asosiy kod buzilmaydi — tajriba alohida.")],
                 "[qidiruv 7c1e2b0] Vazifa qidirish qo'shildi"),
            step("Terminal", "GitHub'ga yuborish va PR", r'''
$ git push -u origin qidiruv
remote: Create a pull request for 'qidiruv' on GitHub:
remote:   https://github.com/ali/kundalik/pull/new/qidiruv''',
                 [("Pull Request", "“shu o'zgarishni main'ga qo'shaylik” degan so'rov."),
                  ("review", "do'st kodni o'qib, sharh yozadi."),
                  ("Merge", "ma'qul bo'lsa — main'ga qo'shiladi.")],
                 "GitHub: Open pull request → Merge"),
            step("Terminal", "main'ni yangilash", r'''
$ git switch main
$ git pull
$ git branch -d qidiruv''',
                 [("pull", "GitHub'dagi yangiliklarni kompyuterga olib keladi."),
                  ("branch -d", "ishlatib bo'lingan branch'ni o'chirish.")],
                 "Fast-forward\n main.py | 12 ++++++++"),
        ],
        {"git-buyruqlar.txt": GIT_BRANCH},
        [("kundalik/", ""), ("├── main.py", "o‘zgardi"), ("└── README.md", "")],
        ["Branch", "push -u", "Pull Request va review", "merge va pull"],
        ["Majburiy: do'stingiz repozitoriysiga PR yuboring va uning PR'ini ko'rib chiqing.",
         "Qo'shimcha: merge conflict yaratib, uni hal qilib ko'ring."],
        "5.12 · Python yakuniy nazorat va loyiha himoyasi.",
    ),
    "DP36": lesson(
        M, 12, "Python yakuniy nazorat va loyiha himoyasi",
        "3 oyda o'rganganlarni bitta loyihada ko'rsatamiz: OOP + JSON + xatolar — “Kundalik” yakuniy versiyasi.",
        "3–5-oylarda: asoslar, tuzilmalar, funksiyalar, fayl, OOP, Git.",
        "Klass, JSON, try/except — 5 savol bilan takrorlaymiz.",
        "Yakuniy loyiha tuzilmasi va himoya tartibi: demo 3 daq + kod tushuntirish + savollar.",
        "Himoyadagi izohlar bo'yicha loyihani yaxshilab, GitHub'ga push qiling.",
        [("📄", "kundalik.json", "ma'lumot", ""),
         ("📦", "Task", "__str__", ""),
         ("🗂", "Kundalik", "yukla, saqla", "mem"),
         ("📋", "main()", "menyu", "loop"),
         ("🎤", "Himoya", "demo + savollar", "")],
        [
            step("main.py", "Task va Kundalik klassi", r'''
class Kundalik:
    def __init__(self, fayl=FAYL):
        self.fayl = fayl
        self.vazifalar = self._yukla()

    def _yukla(self):
        try:
            with open(self.fayl, encoding="utf-8") as f:
                return [Task(**d) for d in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []''',
                 [("Task(**d)", "lug'at kalitlari parametr bo'lib uzatiladi."),
                  ("_yukla", "ichki metod — obyekt yaratilganda chaqiriladi."),
                  ("ikki xato", "fayl yo'q yoki buzilgan — bo'sh ro'yxat.")],
                 "Kundalik() → fayldagi vazifalar obyekt bo'lib yuklanadi"),
            step("main.py", "Saqlash va amallar", r'''
    def saqla(self):
        data = [t.__dict__ for t in self.vazifalar]
        with open(self.fayl, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def qosh(self, matn):
        self.vazifalar.append(Task(matn))
        self.saqla()

    def bajar(self, raqam):
        self.vazifalar[raqam - 1].bajarildi = True
        self.saqla()''',
                 [("har amaldan keyin saqla()", "dastur kutilmaganda yopilsa ham ma'lumot qoladi."),
                  ("t.__dict__", "obyekt → lug'at → JSON.")],
                 "kundalik.json avtomatik yangilanadi"),
            step("main.py", "Menyu va xatolarni ushlash", r'''
def main():
    k = Kundalik()
    while True:
        tanlov = input("1) Qo'shish 2) Ro'yxat 3) Bajarildi 0) Chiqish: ")
        if tanlov == "1":
            k.qosh(input("Vazifa: "))
        elif tanlov == "2":
            for n, t in enumerate(k.vazifalar, start=1):
                print(f"{n}. {t}")
        elif tanlov == "3":
            try:
                k.bajar(int(input("Raqam: ")))
            except (ValueError, IndexError):
                print("Noto'g'ri raqam")
        elif tanlov == "0":
            print("Saqlandi. Xayr! 👋")
            break''',
                 [("IndexError", "mavjud bo'lmagan raqam — dastur yiqilmaydi."),
                  ("main()", "asosiy oqim alohida funksiyada."),
                  ("himoyada", "har qatorni o'z so'zingiz bilan tushuntira olishingiz kerak.")],
                 "Raqam: 5\nNoto'g'ri raqam\n1. ✔ Kitob o'qish\nSaqlandi. Xayr! 👋"),
        ],
        {"main.py": FINAL},
        [("kundalik/", ""), ("├── main.py", "o‘zgardi"), ("├── README.md", ""), ("└── .gitignore", "")],
        ["OOP + JSON + xatolar bitta loyihada", "Kodni tushuntirish", "GitHub'dagi loyiha", "Himoya tartibi"],
        ["Majburiy: izohlar bo'yicha yaxshilab, GitHub'ga push qiling.",
         "Qo'shimcha: “4) O'chirish” va “5) Qidirish” qo'shing."],
        "6.1 · Bot qanday ishlaydi: BotFather, token, async.",
        run={"file": "main.py", "input": "1\nKitob o'qish\n3\n5\n3\n1\n2\n0\n", "expect": ["Noto'g'ri raqam", "1. ✔ Kitob o'qish", "Saqlandi. Xayr! 👋"]},
    ),
}
