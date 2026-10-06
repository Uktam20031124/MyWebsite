# Darsxona

O‘qituvchi uchun shaxsiy CRM: guruhlar, shogirdlar, bo‘limlarga ajratilgan mavzular katalogi,
guruh dasturi, darslar va yo‘qlama.

## Ishga tushirish

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # ixtiyoriy, dev uchun shart emas
python manage.py migrate
python manage.py bootstrap    # ustoz hisobi + namuna ma'lumotlar (faqat bo'sh bazaga)
python manage.py runserver
```

Brauzerda: http://127.0.0.1:8000/ — login `ustoz`, parol `darsxona2026`.

`bootstrap` qayta ishga tushirilsa mavjud parolni **o‘zgartirmaydi**. Kerak bo‘lsa:

```bash
python manage.py bootstrap --reset-password --password 'yangi-parol' --no-demo
```

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
```

GitHub Actions (`.github/workflows/ci.yml`) har push’da tekshiruv, migratsiyalar, testlar va
production sozlamalarini ishga tushiradi.

## Production

1. `.env`: `DJANGO_DEBUG=0`, kuchli `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`.
   Kalitsiz ilova ishga tushmaydi (ataylab).
2. `python manage.py migrate && python manage.py collectstatic --noinput`
3. `gunicorn config.wsgi -b 127.0.0.1:8000 -w 3` — statikani WhiteNoise beradi, nginx faqat proxy.
4. HTTPS ortida: HSTS, secure cookie va SSL redirect avtomatik yoqiladi.
5. SQLite WAL rejimida ishlaydi; zaxira: `sqlite3 db.sqlite3 ".backup backup.sqlite3"`.

## Tuzilma

```
academy/
  models.py      Group, Student, Module, Topic, SyllabusItem, Lesson, Attendance
  services.py    statistika (N+1 so'rovsiz), mavzular parser/import/eksport
  views.py       sahifalar
  forms.py       validatsiya
  management/commands/   bootstrap, import_topics
  tests/         46 ta test
config/settings.py       .env asosidagi sozlamalar
templates/, static/      UI
```
