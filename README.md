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
python manage.py bootstrap      # ustoz hisobi + guruhlar va o'quvchilar (faqat bo'sh bazaga)
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
**reyting = ball × 0.5 + test × 0.3 + davomat × 0.2** (test natijasi bo‘lmasa — ball × 0.7 + davomat × 0.3), o‘rinlar (teng reytingga bir xil o‘rin).
Jurnalni “Excel (CSV)” tugmasi bilan yuklab olish mumkin.

## Mavzu testlari (Telegram orqali, bir martalik havola)

O‘quvchi mavzuni to‘liq o‘zlashtirganini tekshirish uchun:

1. **Savollar banki tayyor**: Starter va Python kurslarining barcha 53 mavzusi uchun 12 tadan
   mavzuga oid savol (`academy/school_data/quizzes_starter.py`, `quizzes_python.py`). Ular
   `migrate` (mavjud mavzular uchun) va `load_school` bilan bazaga yoziladi. Ustoz o‘zi to‘ldirgan
   testlarga (10+ savol) tegilmaydi; qayta ishga tushirish savollarni takrorlamaydi.
   Mavzu sahifasi → “Test” orqali savollarni tahrirlash yoki o‘z testingizni yozish mumkin:
   ```text
   ? Quyidagi kod nima chiqaradi?
   for i in range(2):
       print(i)
   + 0 va 1
   - 1 va 2
   ```
   `?` — savol, `+` — to‘g‘ri javob (bittasi), `-` — noto‘g‘ri javob; savoldan keyingi qatorlar —
   kod (o‘quvchiga chekinishlari bilan ko‘rsatiladi).
2. **Test jo‘natish** — 2 qadam:
   - *Mavzu*: ro‘yxatdan tanlanadi (qidiruv bor; dars mavzusi va guruhda o‘tilgan mavzular tepada).
   - *Kimga va qanday*: shogirdlar (belgilash), **har biriga nechta savol** va **necha daqiqa**.
   Kirish nuqtalari: **yo‘qlama** (“Test jo‘natish” / “Saqlash va test jo‘natish” — yo‘qlama avval
   saqlanadi, darsga kelganlar avtomatik belgilanadi), **dars sahifasi**, **mavzular ro‘yxati**
   (har bir mavzu yonida), **mavzu sahifasi** va yon menyudagi **Testlar** bo‘limi.
   Har bir shogird bankdan tasodifiy N ta savol oladi; savollar va variantlar tartibi ham har xil.
3. **Yuborish — faqat ustozning Telegram akkauntidan** (`TELEGRAM_SENDER_ID`, standart: `7730996406`).
   Havolalar yaratilishi bilan sayt ularni shu akkauntdan har bir shogirdga o‘zi yuboradi: shogird
   kartasidagi Telegram @username orqali, username bo‘lmasa — telefon raqami orqali. Jo‘natma
   sahifasida har bir shogird uchun holat (“Yuborildi”, “Yuborilmadi” + sabab), “Telegramda yuborish”
   (yuborilmaganlarga) va “Qayta yuborish” bor. Havolani boshqa akkauntdan yuborish (share / nusxa)
   tugmalari yo‘q; sessiya boshqa akkauntga tegishli bo‘lsa, sayt hech narsa yubormaydi.
4. O‘quvchi havolani bosadi → “Testni boshlash” → yuqorida **teskari sanoq taymer**. Vaqt tugasa
   test avtomatik yakunlanadi va natija (to‘g‘ri javoblar soni, foiz) ekranda ko‘rsatiladi.
5. **Havola faqat bir marta ishlaydi**: boshlangandan keyin boshqa brauzer/qurilmada ochilmaydi,
   yakunlangandan keyin test qayta ochilmaydi. (Telegram havola “preview”ini o‘zi ochganda test
   boshlanib ketmaydi — test faqat tugma bosilganda boshlanadi.) Sahifa tasodifan yangilansa,
   o‘sha brauzerda davom etadi, taymer qayta boshlanmaydi.
6. Natijalar jo‘natma sahifasida, “Testlar” bo‘limida (guruh bo‘yicha), dars va mavzu sahifalarida
   (o‘rtacha foiz) va o‘quvchi kartasida ko‘rinadi.
   Ochilmagan havolani “↻” bilan yangisiga almashtirish mumkin (eskisi ishlamay qoladi).
7. **Javoblar tahlili.** O‘quvchi test tugagach har bir savolda o‘z javobi to‘g‘ri yoki xato ekanini ko‘radi
   (to‘g‘ri variantning o‘zi unga ko‘rsatilmaydi — javoblar tarqalib ketmasligi uchun). Ustoz esa
   jo‘natma sahifasida har bir o‘quvchi yonidagi **“Javoblar”** orqali har bir savolni, o‘quvchi tanlagan
   javobni (xato — qizil), to‘g‘ri javobni (yashil) va javobsiz qolganlarni ko‘radi (“Faqat xatolar”
   filtri, oldingi/keyingi o‘quvchi). Jo‘natma sahifasida — **eng ko‘p xato qilingan savollar** (foiz,
   to‘g‘ri javob, eng ko‘p tanlangan xato variant). Test yakunlanganda javoblar nusxasi saqlanadi —
   keyinchalik savollar tahrirlansa ham natija tahlili o‘zgarmaydi.

Production’da havolalar to‘g‘ri domen bilan chiqishi uchun `DJANGO_ALLOWED_HOSTS` va HTTPS sozlangan bo‘lsin.

### Telegram akkauntini ulash (bir marta)

1. https://my.telegram.org → **API development tools** → ilova yarating; `api_id` va `api_hash` ni
   `.env` ga yozing:
   ```bash
   TELEGRAM_API_ID=1234567
   TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef
   # TELEGRAM_SENDER_ID=7730996406   # standart qiymat
   ```
2. Serverda: `pip install -r requirements.txt`, so‘ng
   ```bash
   python manage.py telegram_login          # telefon, Telegram'ga kelgan kod, (bo'lsa) 2FA parol
   python manage.py telegram_login --check  # qaysi akkaunt ulanganini ko'rish
   python manage.py telegram_login --logout # uzish
   ```
   **Kod kelmasa** (Telegram yangi API ilova/server IP'dan kirishda kodni ba'zan yetkazmaydi) —
   QR-kod bilan: telefonda Telegram → Sozlamalar → Qurilmalar → “Kompyuterni ulash”:
   ```bash
   python manage.py telegram_login --qr                    # (2FA bo'lsa: --qr --password PAROL)
   ```
   Terminal so‘roviga javob berib bo‘lmasa (masalan, masofadan) — ikki bosqichda:
   ```bash
   python manage.py telegram_login --phone +998901234567   # Telegram'ga kod keladi
   python manage.py telegram_login --code 12345            # (2FA bo'lsa: --password PAROL)
   ```
   Faqat `TELEGRAM_SENDER_ID` akkauntiga ruxsat beriladi — boshqa akkaunt bilan kirilsa, sessiya
   saqlanmaydi. Sessiya `.telegram_session` faylida (`TELEGRAM_SESSION_FILE`, huquqlar 600) — u
   akkauntga to‘liq kirish kaliti, hech kimga bermang va repozitoriyga qo‘shmang.
3. Ko‘p notanish odamga qisqa vaqtda xabar yuborish Telegram’da spam cheklovini keltirib chiqarishi
   mumkin: xabarlar orasida pauza bor, cheklov bo‘lsa yuborish to‘xtaydi va sabab ko‘rsatiladi.
   O‘quvchilar sizning raqamingizni kontaktga saqlab qo‘ysa, xabarlar ishonchli yetib boradi.

## Ro‘yxatdan o‘tish arizalari (Telegram guruhlari uchun havola)

`Arizalar` bo‘limida har bir Telegram guruhi uchun havola yaratasiz (`/royxat/<kalit>/`) va guruhga
tashlaysiz. O‘quvchi **F.I.Sh., telefon va Telegram username** yuboradi — ma’lumot bazaga o‘z-o‘zidan
yozilmaydi, **ariza** bo‘lib keladi (yon menyuda soni, Telegram ulangan bo‘lsa — “Saqlangan xabarlar”ga
bildirishnoma). Har bir arizada mos o‘quvchi taklif qilinadi:

- **Biriktirish** — mavjud o‘quvchining telefoni va Telegram’i yangilanadi;
- **Yangi o‘quvchi** — tanlangan guruhga qo‘shiladi (havola guruhi oldindan tanlangan);
- **Rad etish**.

“Ishonchlilarni tasdiqlash” — ismi yagona o‘quvchiga mos kelganlarni biriktiradi, bazada yo‘q va havolasi
guruhga bog‘langanlarni yangi o‘quvchi qiladi; qolganlarini siz hal qilasiz. O‘quvchi xato yozsa, xuddi shu
telefon bilan qayta yuboradi — yangi ariza ochilmaydi, o‘sha yangilanadi. Havolani to‘xtatish/o‘chirish mumkin.

## O‘quvchilarning Telegram / telefoni

Test havolalari faqat Telegram username yoki telefoni bor o‘quvchilarga yuboriladi. To‘ldirishning ikki yo‘li:

1. **Ommaviy kiritish** (`Shogirdlar → Telegram kiritish`): ro‘yxatni istalgan ko‘rinishda qo‘yasiz —
   ```text
   Aliyev Sardor — @sardor_a — +998 90 123 45 67
   2) Karimova Nigina, t.me/nigina
   ```
   Ism-familiya tartibi va qisqartma muhim emas; har bir qator ko‘rsatiladi (yangilanadi / o‘zgarishsiz /
   topilmadi / bir nechta mos), tasdiqlagandan keyingina saqlanadi.
2. **O‘quvchi o‘zi to‘ldiradi** (`Guruh → Telegram ma’lumotlari → Havola yaratish`): havolani guruh
   chatiga tashlaysiz, o‘quvchi ismini tanlab username/telefonini kiritadi. Faqat bo‘sh maydonlar
   to‘ldiriladi (boshqaning ma’lumotini o‘zgartirib bo‘lmaydi), havolani yangilash/o‘chirish mumkin.

Guruh sahifasida kimlarda ma’lumot yo‘qligi ko‘rinadi; shogirdlar ro‘yxatida “Telegram/telefon yo‘q” filtri bor.

## Test natijalari reytingda va avtomatik Telegram xabarlari

- **Reyting** = ball × 0.5 + **test** × 0.3 + davomat × 0.2 (test bo‘lmasa — ball × 0.7 + davomat × 0.3;
  davomat yo‘q bo‘lsa — qolganlari o‘z vaznlari nisbatida). Guruh jurnalida “Test” ustuni (dars hali
  bo‘lmasa ham), CSV’da “Test %”, o‘quvchi kartasida testlar o‘rtachasi va oxirgi testlar grafigi.
- **Bosh sahifa → E’tibor talab qiladi**: davomat < 70%, ball < 60 yoki **oxirgi 3 test < 50%** (kamida
  2 ta test) — sababi bilan.
- **Eslatma** (`manage.py quiz_reminders`, har soat): Telegram’da yuborilgan, lekin 3 soatda ochilmagan
  havola haqida o‘quvchiga **bitta** eslatma, faqat 09:00–21:00 (Toshkent). Jo‘natma sahifasida “eslatildi”.
- **Kun yakuni** (`manage.py daily_report`, har kuni 20:00): ustozning “Saqlangan xabarlar”iga — bugun
  nechta test yechildi, o‘rtacha foiz, mavzular bo‘yicha, 50% dan past olganlar, ochilmagan havolalar,
  arizalar va Telegram’i yo‘q o‘quvchilar soni. `--dry-run` — faqat ekranga.
- `.env`: `DARSXONA_SITE_URL=https://...` (eslatmadagi havola uchun), ixtiyoriy
  `DARSXONA_REMINDER_AFTER_HOURS=3`.

## Baza zaxirasi (backup)

```bash
python manage.py backup_db              # DARSXONA_BACKUP_DIR ga siqilgan nusxa, eski (14 kundan) o'chadi
python manage.py backup_db --telegram   # + nusxa Telegram "Saqlangan xabarlar"ga (server tashqarisida)
```
Nusxa sayt ishlab turganda ham xavfsiz olinadi (SQLite backup API) va yaxlitligi tekshiriladi.
Serverda systemd timer'lar: har kuni 03:30 — lokal nusxa, har yakshanba 04:00 — Telegram'ga ham.
Tiklash: `gunzip -c darsxona-YYYYMMDD-HHMMSS.sqlite3.gz > db.sqlite3` (avval xizmatni to‘xtating).

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
  models.py      Group, Student, Module, Topic, SyllabusItem, Lesson, Attendance,
                 Quiz, Question, Choice, QuizAttempt (mavzu testlari)
  services.py    statistika (N+1 so'rovsiz), mavzular parser/import/eksport
  views.py       sahifalar
  forms.py       validatsiya
  management/commands/   bootstrap, import_topics, load_school
  school_data/   guruhlar, o‘quvchilar va dars rejalari
  tests/         72 ta test
config/settings.py       .env asosidagi sozlamalar
templates/, static/      UI
```
