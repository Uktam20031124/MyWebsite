# Darsxona

O‘qituvchi uchun shaxsiy CRM: guruhlar, shogirdlar, bo‘limlarga ajratilgan mavzular katalogi,
guruh dasturi, darslar va yo‘qlama.

## Ishga tushirish

Talab: **Python 3.10+** va **Git**.

**Windows (PowerShell):**

```powershell
git clone https://github.com/Uktam20031124/MyWebsite.git
cd MyWebsite
py -m venv .venv
.venv\Scripts\Activate.ps1      # xato bersa: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap      # ustoz hisobi + namuna ma'lumotlar (faqat bo'sh bazaga)
python manage.py runserver
```

**macOS / Linux:**

```bash
git clone https://github.com/Uktam20031124/MyWebsite.git
cd MyWebsite
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # ixtiyoriy, dev uchun shart emas
python manage.py migrate
python manage.py bootstrap
python manage.py runserver
```

Brauzerda: http://127.0.0.1:8000/ — login `ustoz`, parol `darsxona2026`.

Keyingi yangilanishlarni olish: `git pull`, so'ng `pip install -r requirements.txt` va `python manage.py migrate`.

`bootstrap` qayta ishga tushirilsa mavjud parolni **o‘zgartirmaydi**. Kerak bo‘lsa:

```bash
python manage.py bootstrap --reset-password --password 'yangi-parol' --no-demo
```

## O‘quv markazi ma’lumotlari (guruhlar, o‘quvchilar, mavzular)

Haqiqiy guruhlar va dars rejalari kod ichida, `academy/school_data/` papkasida saqlanadi:

| Fayl | Nima bor |
|---|---|
| `starter.py` | Starter kursi: 19 dars (Google, Canva, Figma, Terminal, Scratch, xavfsizlik, yakuniy loyiha) |
| `python.py` | Python kursi: 34 dars (asoslar → tuzilmalar → sikl/funksiya → modul/fayl/xato → OOP → bot) |
| `groups.py` | Guruhlar (S-009, S005, P-006), o‘quvchilar, o‘tilgan va qolgan mavzular tartibi |

Har bir dars: maqsad, dars rejasi (daqiqalari bilan), darsdagi masalalar, baholash mezoni (100 ball),
uy vazifasi va materiallar.

```bash
python manage.py load_school --reset   # bazani tozalab, shu ma'lumotlarni yuklash (tasdiq so'raydi)
python manage.py load_school           # fayllarni tahrirlagandan keyin yangilash (hech narsa o'chmaydi)
```

`--reset` guruh, o‘quvchi, mavzu, dars va yo‘qlamalarni o‘chiradi; foydalanuvchi (login) qoladi.
Yangi guruh yoki mavzu qo‘shish: `groups.py`/`python.py` ga yozing va `load_school` ni qayta ishga tushiring.

## Baholash va reyting

Yo‘qlama sahifasida har bir o‘quvchiga darsdagi **ball (0–100)** qo‘yiladi (bo‘sh — baholanmagan).
Guruh jurnalida avtomatik: o‘rtacha ball, davomat foizi va
**reyting = o‘rtacha ball × 0.7 + davomat × 0.3**, o‘rinlar (teng reytingga bir xil o‘rin).
Jurnalni “Excel (CSV)” tugmasi bilan yuklab olish mumkin.

## Imkoniyatlar

- **Bosh sahifa** — bugungi va navbatdagi darslar, haftalik davomat, yakunlanmagan (sanasi o‘tgan) darslar,
  haftada 2+ dars qoldirgan shogirdlar, guruhlar progressi.
- **Mavzular katalogi** — bo‘limlar (masalan, “Python asoslari”, “Django”), har bir mavzu uchun tavsif,
  uyga vazifa shabloni, materiallar (havolalar), davomiylik. Yashirish, qidirish, bo‘lim bo‘yicha filtr.
- **Ommaviy import** (`Mavzular → Ommaviy import`) — mavzular ro‘yxatini matn ko‘rinishida qo‘yasiz,
  avval ko‘rib chiqasiz, so‘ng tasdiqlaysiz. Ixtiyoriy ravishda guruh dasturlariga ham qo‘shiladi.
  Qayta import xavfsiz: mavjud mavzular takrorlanmaydi.
- **Eksport** — katalogni xuddi shu formatdagi `.txt` faylga yuklab olish (zaxira yoki boshqa serverga ko‘chirish).
- **Guruh dasturi** — mavzuni yoki butun bo‘limni bir bosishda qo‘shish, ↑/↓ bilan tartiblash,
  “o‘tildi / rejaga / o‘tkazish”. Navbatdagi mavzu avtomatik taklif qilinadi.
- **Darslar** — dars “o‘tildi” bo‘lsa (forma, yo‘qlama yoki tugma orqali) dastur avtomatik yangilanadi;
  uyga vazifa bo‘sh bo‘lsa, mavzudagi shablon qo‘yiladi.
- **Yo‘qlama** — klaviatura bilan ishlaydi, “hammasi keldi”, jonli hisoblagich, saqlanmagan o‘zgarish haqida ogohlantirish.
- **Davomat jurnali** (`Guruh → Jurnal`) — shogirdlar × darslar jadvali, har bir shogird uchun davomat foizi;
  Excel’da ochiladigan CSV eksport.
- **Shogirdlar eksporti** — ro‘yxatdagi filtrlar bilan CSV.
- **Dastur va darslar doim mos** — dars “o‘tildi”dan qaytarilsa, mavzusi almashsa yoki o‘chirilsa,
  guruh dasturidagi mavzu holati avtomatik qayta hisoblanadi. Bir guruhga bir vaqtda ikki dars yozib bo‘lmaydi.
- **Login himoyasi** — 5 ta xato urinishdan keyin IP 15 daqiqaga bloklanadi (sozlanadi).
- Global qidiruv (`/` tugmasi), mobil menyu, chop etish uchun uslub, o‘z 404/403/500 sahifalari.

## Mavzular formatini qanday yozish kerak

```text
# Python asoslari
1. Kirish va muhit — VS Code, terminal
2. O'zgaruvchilar | int, str, bool | 90
3. Sikllar
    for, while, range
    break / continue

# Django
- Modellar va ORM
- Formalar — ModelForm, validatsiya
```

- `#` bilan boshlangan qator — **bo‘lim**; qolganlari — **mavzu**.
- `1.`, `1)`, `-`, `*`, `•` belgilari avtomatik olib tashlanadi.
- Tavsif: `Mavzu — tavsif` yoki `Mavzu | tavsif | daqiqa`.
- Bo‘sh joy bilan boshlangan qator oldingi mavzu tavsifiga qo‘shiladi.

Terminaldan ham import qilish mumkin:

```bash
python manage.py import_topics mavzular.txt --group PY-01 --dry-run   # avval tekshirish
python manage.py import_topics mavzular.txt --group PY-01 --group DJ-01
```

## Testlar

```bash
python manage.py test
pip install ruff && ruff check .     # kod sifati (sozlamalar: pyproject.toml)
```

GitHub Actions (`.github/workflows/ci.yml`) har push’da Python 3.10/3.12/3.13 da lint, tekshiruv,
migratsiyalar, testlar va production sozlamalarini ishga tushiradi.

## Production

1. `.env`: `DJANGO_DEBUG=0`, kuchli `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`.
   Kalitsiz ilova ishga tushmaydi (ataylab).
2. `python manage.py migrate && python manage.py collectstatic --noinput`
3. `gunicorn config.wsgi -b 127.0.0.1:8000 -w 3` — statikani WhiteNoise beradi, nginx faqat proxy.
4. HTTPS ortida: HSTS, secure cookie va SSL redirect avtomatik yoqiladi.
5. SQLite WAL rejimida ishlaydi; zaxira: `sqlite3 db.sqlite3 ".backup backup.sqlite3"`.
6. nginx ortida: `DJANGO_TRUST_X_FORWARDED_FOR=1` (login himoyasi mijoz IP’sini ko‘rishi uchun) va
   bir nechta worker uchun `DJANGO_CACHE_DIR=/var/tmp/darsxona-cache` (urinishlar hisobi umumiy bo‘ladi).
7. Monitoring: `GET /healthz/` → `{"status": "ok"}` (login talab qilmaydi, baza ulanishini tekshiradi).

## Tuzilma

```
academy/
  models.py      Group, Student, Module, Topic, SyllabusItem, Lesson, Attendance
  services.py    statistika (N+1 so'rovsiz), mavzular parser/import/eksport
  views.py       sahifalar
  forms.py       validatsiya
  management/commands/   bootstrap, import_topics, load_school
  school_data/   guruhlar, o‘quvchilar va dars rejalari
  tests/         72 ta test
config/settings.py       .env asosidagi sozlamalar
templates/, static/      UI
```
