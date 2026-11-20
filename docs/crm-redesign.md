# Minar Test / Ustoz CRM — redizayn: inventar va holat

Stack: Django 5.2, server-rendered shablonlar (`templates/academy/`), bitta CSS (`static/css/app.css`, tokenlar boshida),
bitta JS (`static/js/app.js`, Turbo 8 bilan), tarjima — `locale/ru` (`manage.py i18n_catalog`). Rollar: superuser
(bosh ustoz), o'qituvchi (`TeacherAccount.permissions` — bo'limlar ro'yxati, `teachers.scope()` — faqat o'z guruhlari),
anonim/o'quvchi (ochiq havolalar: `/royxat/`, `/men/`, `/t/`, `/o/`, `/aloqa/`). `/admin/` — alohida texnik interfeys.

## Marshrut inventari

| Yo'nalish | Yo'llar | Shablon | Rol | Asosiy amal | Bosqich |
| --- | --- | --- | --- | --- | --- |
| Kirish | `/kirish/`, `/chiqish/` | `login.html` | anonim | Kirish (blok siyosati: `ThrottledLoginView`) | **P0 ✓** |
| Shell | barcha sahifalar | `base.html`, `includes/*` | hammasi | Navigatsiya, Ctrl+K, UZ/RU, kun/tun | **P0 ✓** |
| Bosh sahifa | `/` | `dashboard.html` | ustoz | Navbatdagi dars → yo'qlama/boshlash | **P0 ✓** |
| Jadval | `/jadval/?hafta=&kun=&korinish=grid` | `timetable.html` | ustoz, o'qituvchi (`timetable`) | Kun agendasi, chop etish | **P0 ✓** |
| Guruhlar | `/guruhlar/`, `yangi/`, `<pk>/`, `tahrir/`, `ochirish/`, `jurnal/`, `boshlash/`, `mavzu/…`, `qr/`, `reyting/`, `telegram-chat/`, `aloqa-havola/`, `sahifalar/` | `groups/*` | ustoz, `groups` | Tafsilot: bo'limlar, navbatdagi mavzu | **P0 ✓** tafsilot; ro'yxat, forma, jurnal — P1 |
| Darslar va yo'qlama | `/darslar/`, `yangi/`, `<pk>/`, `tahrir/`, `ochirish/`, `yakun/`, `yoqlama/` | `lessons/*` | ustoz, `lessons` | Yo'qlama → saqlash/yakunlash | **P0 ✓** yo'qlama; ro'yxat, forma, tafsilot — P1 |
| Arizalar | `/arizalar/?status=&korinish=havolalar`, `tasdiqlash/`, `<pk>/`, `havola/<pk>/`, `/royxat/<token>/` | `registrations/*` | ustoz, `registrations`; anonim (ochiq forma) | Navbat (Kutilmoqda) birinchi | **P0 ✓** navbat; ariza tafsiloti va ochiq forma — P1 |
| Shogirdlar | `/shogirdlar/`, `yangi/`, `<pk>/`, `tahrir/`, `ochirish/`, `eksport/`, `aloqa/`, `<pk>/profil|alochi|coin|mavzular|sahifa|sertifikat|qr/` | `students/*`, `contacts/*` | ustoz, `students` | Ro'yxat, profil, ommaviy aloqa | P1 |
| Mavzular | `/mavzular/`, `yangi/`, `import/`, `eksport/`, `<pk>/`, `taqdimot/`, `rasm/`, `dars/`, `test/`; `/bolimlar/…` | `topics/*`, `quiz/edit*` | ustoz, `topics` | Katalog, tafsilot, editor, import preview | P1 |
| Uyga vazifalar | `/vazifalar/`, `<pk>/baho/`, `<pk>/fayl/` | `homework/*` | ustoz, `homework` | Tekshirilmagan navbat | P1 |
| Testlar | `/testlar/`, `jonatish/`, `umumiy/…`, `<pk>/…`, `natija/<pk>/…`, `/t/<token>/…`, `/o/<token>/…` | `quiz/*` | ustoz, `tests`; o'quvchi | Jo'natish oqimi, natija | P1 (jo'natish), P2 (natija, ochiq test) |
| Ogohlantirishlar | `/testlar/ogohlantirishlar/`, `natija/<pk>/jarima/` | `quiz/warnings.html` | ustoz, `warnings` | Ko'rib chiqish, quvvat ayirish | P2 |
| So'rovlar | `/testlar/sorovlar/`, `hammasi/`, `natija/<pk>/ruxsat/`, `testlar/sorov/<pk>/` | `quiz/requests.html` | ustoz, `requests` | Ruxsat/rad | P2 |
| Mukofotlar | `/dokon/`, `<pk>/`, `sorov/<pk>/` | `shop/*` | ustoz, `rewards` | Katalog, so'rov qarori | P2 |
| O'qituvchilar | `/oqituvchilar/`, `<pk>/`, `maosh/`, `hisobot/`, `jurnal/`, `telegram-uzish/`; `/oqituvchi/…` | `teachers/*` | superuser; o'qituvchi (o'z sahifasi) | Hisob, ruxsatlar, maosh | P2 |
| O'quvchi portali | `/men/<token>/…` | `portal/*` | o'quvchi | Profil, test, do'kon | P2 |
| Yordamchi | 403/404/500, `confirm_delete.html`, `search.html`, print/QR/sertifikat | `error_base.html`, … | hammasi | Aniq sabab va keyingi amal | P2 |

## P0 — qilingan ishlar

- **Tokenlar** (`app.css` boshida): brief palitrasi (light `#F4F6FA / #FFFFFF / #152238 / #4D5C70`, nav `#101E36`,
  asosiy `#08746F`; dark `#0D1525 / #142239 / #EEF3FB`, asosiy `#6CDBCE` to'q matn bilan), semantik nomlar
  (`--primary`, `--focus`, `--success`, `--warning`, `--danger`, `--tap`), forma chegarasi `--border-input` (≥ 3:1).
  Bitta shrift oilasi (Onest — lotin va kirill); dekorativ Unbounded va girih naqshi olib tashlandi.
  `.cache/contrast.py`: 26 juftlik × 2 mavzu — hammasi WCAG AA.
- **Shell**: menyu «Bugun / O'quv markazi / Navbatlar / Boshqaruv»; badge faqat bajariladigan ish soni
  (katalog hajmi badge'lari va ularning 5 ta COUNT so'rovi olib tashlandi); rol shartlari o'zgarmagan.
  Mobil drawer: fokus ichida, Tab aylanadi, Escape yopadi, fokus tugmaga qaytadi, asosiy qism `inert`.
  Barcha POST formalar: takror yuborishdan himoya (`is-pending`, Turbo javobida va orqaga qaytishda tiklanadi).
- **Kirish**: «Hisobga kirish», `autocomplete=username/current-password`, `autocapitalize=none`, parolni ko'rsatish.
- **Bosh sahifa**: tartib «Bugun» → navbatdagi dars (holatga mos amal: Yo'qlama / Darsni boshlash / Rejalash) →
  «E'tibor talab qiladi» (yakunlanmagan darslarning **to'liq** soni va eng eskisi) → ixcham KPI.
  Backend: `next_up_session()`, `overdue_count`; davomat belgilanmagan bo'lsa `None` («Ma'lumot yo'q»), haqiqiy 0%
  maxraj bilan (`present / marked`); bo'sh dastur — `None` («Dastur biriktirilmagan»).
- **Jadval**: bir vaqtdagi darslar yonma-yon yo'laklarda (`place_in_lanes`) — avval biri ikkinchisini yopardi;
  mobil standart — kunlar tasmasi + tanlangan kun agendasi (`?kun=`), grid ixtiyoriy (`?korinish=grid`); chop etish
  — butun hafta gridi, interaktiv elementlarsiz.
- **Guruh tafsiloti**: xulosa (holat, jadval, xona, shogirdlar, bajarilgan/jami), bo'limlar navigatsiyasi
  (`#shogirdlar`, `#dastur`, `#darslar`, `#coin-board`, Jurnal), navbatdagi mavzu bloki (siqilgan karta xatosi
  tuzatildi), shogirdlar dasturdan oldin, dastur bo'limlarga yig'ilgan (faqat navbatdagi bo'lim ochiq; `#syllabus-N`
  fragmenti yopiq bo'limni ochadi). Mavjud fragmentlar (`#motivation`, `#contacts`) saqlangan.
- **Yo'qlama**: 4 holat 320px da ham teng (≥ 44px); ball/izoh mobilda yig'iladi, kiritilgan qiymat tugmada
  ko'rinadi; jonli xulosa — har holat soni va saqlanmagan qatorlar; «Hammasi kelmadi» oqibatini aytib tasdiq so'raydi;
  mobil panel — bitta asosiy («Saqlash va yakunlash»), «Saqlash» va «Boshqa amallar» menyusi. POST semantikasi
  (`complete=1`, `then=quiz`) o'zgarmagan.
- **Arizalar**: standart — «Kutilmoqda» navbati; «Havolalar» alohida yorliq (`?korinish=havolalar`), havola amallari
  shu yorliqqa qaytadi.

## P0 — tekshiruv (sintetik baza: 6 guruh, 84 shogird, 31 dars, 9 ariza)

| 390 × 844 | Oldin | Keyin |
| --- | --- | --- |
| Bosh sahifa: asosiy blok | «Bugungi jadval» 585 px | navbatdagi dars 243 px, «Yo'qlama» birinchi viewportda |
| Jadval: sahifa balandligi | 2 972 px (gorizontal grid) | 1 085 px (kun agendasi, gridsiz) |
| Guruh: bo'limlarga yo'l / balandlik | yo'q / 9 056 px | 276 px / 4 727 px |
| Yo'qlama: quyi panel | 3 ta katta tugma | 1 qator (asosiy + saqlash + menyu), 3 shogird birinchi ekranda |
| Arizalar: «Kutilmoqda» | 422 px (havolalardan keyin) | 268 px |
| Hujjat gorizontal overflow (320, 390, 1440) | 0 | 0 |

- axe-core 4.10.2 (WCAG 2.0/2.1/2.2 A–AA): 28 sahifa holati (6 sahifa + kirish × light/dark × 390/1440) — 0 buzilish.
  Topilib tuzatilganlar: sariq fonda ikkilamchi matn (4.42 → `--text-3` to'qlashtirildi), dastur amallari 35% xira
  (1.71), dastur sarlavhasi havolasi tugmalarni geometrik yopardi (2.5.8 target size).
- Klaviatura: drawer fokus/Tab/Escape/qaytish — o'tdi; 320px yo'qlama — 4 holat yopishmaydi, hammasi ≥ 44px.
- Testlar: `manage.py test academy` — 436 (yangi `test_crm_p0.py`: 11), ruff toza; RU tarjima 1700/1700.

Tekshirilmagan: mobil WebKit/Safari (muhitda yo'q), Core Web Vitals dala ma'lumoti (monitoring yo'q).
