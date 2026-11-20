"""Dasturchi 11-oy (WB25–WB36, EduCenter: server, integratsiya, yakuniy loyiha) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "WB25": """
? ListView nima?
+ Ro'yxat sahifasi uchun tayyor class-based view
- Model
- Shablon
- Forma

? paginate_by = 5 nima qiladi?
+ Har sahifada 5 ta element ko'rsatadi
- 5 ta sahifa yaratadi
- 5 ta elementni o'chiradi
- Hech narsa

? Shablonda joriy sahifa obyekti qanday nomlanadi?
+ page_obj
- page
- paginator_page
- current

? ?page=2 nima?
+ GET parametri — ikkinchi sahifa
- URL xatosi
- Ikkinchi yangilik
- Hech narsa

? as_view() nima uchun?
+ Klassni URL uchun view funksiyaga aylantiradi
- Shablon yaratadi
- Modelni ko'rsatadi
- Hech narsa

? app_name = "news" nima beradi?
+ URL nomlari uchun namespace: {% url 'news:list' %}
- App nomini o'zgartiradi
- Papka yaratadi
- Hech narsa

? ordering = ["-created"] dagi minus nima?
+ Kamayish tartibi — eng yangisi birinchi
- Xato
- O'chirish
- Manfiy son

? ListView qaysi shablonni avtomatik qidiradi?
+ news/post_list.html
- list.html
- news.html
- post.html

? queryset = Post.objects.filter(is_published=True) nima kafolatlaydi?
+ Nashr qilinmagan yangiliklar ko'rinmaydi
- Hammasi ko'rinadi
- Yangiliklar o'chadi
- Hech narsa

? Funksiya view o'rniga class-based view'ning foydasi?
+ Ro'yxat, sahifalash kabi tayyor imkoniyatlar — kam kod
- Tezroq ishlaydi
- Majburiy
- Hech qanday
""",
    "WB26": """
? Django testlari qaysi klassdan meros oladi?
+ TestCase
- Test
- unittest.Model
- View

? Testlar qaysi bazada ishlaydi?
+ Alohida vaqtinchalik test bazasida
- Haqiqiy bazada
- Bazasiz
- Serverdagi bazada

? self.client nima?
+ Brauzer o'rnida so'rov yuboruvchi test mijozi
- Foydalanuvchi
- Server
- Baza

? assertContains nimani tekshiradi?
+ Javobda matn borligi va status 200
- Faqat status
- Faqat sarlavha
- Hech narsa

? setUpTestData nima uchun?
+ Ma'lumot bir marta yaratiladi — testlar tez
- Har testdan oldin baza o'chiriladi
- Test o'chiriladi
- Hech narsa

? SECRET_KEY nega kodda yozilmaydi?
+ Maxfiy — GitHub'ga chiqib ketsa xavfli
- Uzun bo'lgani uchun
- Django taqiqlaydi
- Shart emas

? os.environ["SECRET_KEY"] kalit bo'lmasa nima bo'ladi?
+ Sayt ishga tushmaydi — xato darhol ko'rinadi
- Bo'sh kalit ishlatiladi
- Standart kalit
- Hech narsa

? DEBUG = os.environ.get("DEBUG", "0") == "1" ning foydasi?
+ Unutilsa ham DEBUG o'chiq qoladi
- Doim yoqiq
- Tezlik
- Hech qanday

? .env.example nima?
+ Git'dagi namuna — qaysi sozlamalar kerakligini ko'rsatadi
- Haqiqiy kalitlar
- Kod fayli
- Log

? python manage.py test dagi nuqta (.) nimani bildiradi?
+ Bitta test o'tdi
- Xato
- Test o'tkazib yuborildi
- Hech narsa
""",
    "WB27": """
? Serverda runserver nega ishlatilmaydi?
+ U faqat ishlab chiqish uchun — sekin va xavfsiz emas
- Ishlamaydi
- Pullik
- Taqiqlangan

? Gunicorn nima?
+ Python saytlari uchun WSGI ishlab chiqarish serveri
- Baza
- Brauzer
- Telegram kutubxonasi

? --workers 3 nima beradi?
+ Bir vaqtda 3 ta so'rovni qayta ishlash
- 3 ta sayt
- 3 ta foydalanuvchi
- 3 marta qayta ishga tushish

? collectstatic nima qiladi?
+ Hamma statik fayllarni STATIC_ROOT ga yig'adi
- Statik fayllarni o'chiradi
- Rasm yuklaydi
- Hech narsa

? Gunicorn nega 127.0.0.1:8000 da tinglaydi?
+ Tashqaridan yopiq — oldida Nginx turadi
- Tezroq
- Majburiy
- Xato

? EnvironmentFile nima qiladi?
+ .env qiymatlarini xizmatga uzatadi
- Log yozadi
- Kodni yuklaydi
- Hech narsa

? Restart=always nima qiladi?
+ Xizmat to'xtasa qayta ishga tushiradi
- Har kuni o'chiradi
- Hech narsa
- Serverni o'chiradi

? systemctl enable --now educenter nima qiladi?
+ Hozir ishga tushiradi va server yoqilganda ham avtomatik
- Faqat o'chiradi
- Faqat hozir
- Hech narsa

? curl -I nima qaytaradi?
+ Faqat javob sarlavhalari (status)
- Butun sahifa
- Rasm
- Hech narsa

? Serverdagi .env da DEBUG qanday bo'ladi?
+ DEBUG=0
- DEBUG=1
- Bo'lmaydi
- DEBUG=True doim
""",
    "WB28": """
? Nginx bu loyihada nima vazifani bajaradi?
+ Reverse proxy: static fayllarni beradi, qolganini gunicorn'ga uzatadi
- Baza
- Python'ni bajaradi
- Telegram bot

? location /static/ { alias ... } nima beradi?
+ Statik fayllarni Nginx o'zi tez beradi
- Django beradi
- Fayllarni o'chiradi
- Hech narsa

? X-Forwarded-Proto sarlavhasi nima uchun?
+ Django so'rov https orqali kelganini bilishi uchun
- Tezlik uchun
- Rasm uchun
- Hech narsa

? nginx -t nima qiladi?
+ Sozlamalarni xatosizligini tekshiradi
- Nginx'ni o'chiradi
- Sertifikat oladi
- Hech narsa

? certbot nima qiladi?
+ Let's Encrypt'dan bepul HTTPS sertifikat oladi va yangilaydi
- Domen sotib oladi
- Saytni tezlashtiradi
- Hech narsa

? SECURE_SSL_REDIRECT = True nima qiladi?
+ http so'rovlarni https ga yo'naltiradi
- https ni o'chiradi
- Cookie o'chiradi
- Hech narsa

? SESSION_COOKIE_SECURE nima beradi?
+ Sessiya cookie faqat HTTPS orqali yuboriladi
- Cookie o'chadi
- Tezlik
- Hech narsa

? HSTS nima?
+ Brauzerga “bu saytga faqat HTTPS bilan kir” degan ko'rsatma
- Sertifikat turi
- Nginx moduli
- Baza

? Nega HSTS 3600 soniyadan boshlanadi?
+ HTTPS barqaror ishlashiga ishonch hosil qilgach oshirish uchun
- Django talab qiladi
- Xato
- Tezlik uchun

? check --deploy nima qiladi?
+ Ishlab chiqarish xavfsizlik sozlamalarini tekshiradi
- Saytni joylaydi
- Testlarni ishga tushiradi
- Hech narsa
""",
    "WB29": """
? API nima?
+ Dasturlar bir-biri bilan ma'lumot almashadigan interfeys
- Sayt dizayni
- Baza
- Brauzer

? JSON nima?
+ Ma'lumot almashish uchun matn formati
- Dasturlash tili
- Rasm formati
- Baza

? JsonResponse nima qaytaradi?
+ Content-Type: application/json bo'lgan javob
- HTML sahifa
- Fayl
- Hech narsa

? ensure_ascii=False nima beradi?
+ O'zbekcha harflar \\u kodlarsiz chiqadi
- Tezlik
- Xavfsizlik
- Hech narsa

? request.build_absolute_uri nima qaytaradi?
+ To'liq manzil (https://domen/...)
- Faqat yo'l
- IP manzil
- Hech narsa

? Nega API'da modelning hamma maydonlari chiqarilmaydi?
+ Faqat kerakli va ochiq ma'lumot — ichki ma'lumot chiqmasin
- Joy kam
- Django taqiqlaydi
- Xato

? Testda JSON javob qanday o'qiladi?
+ response.json()
- response.text()
- json(response)
- response.data

? select_related("category") API'da nima beradi?
+ Kategoriyalarni bitta so'rovda oladi
- Kategoriyalarni o'chiradi
- Filtrlaydi
- Hech narsa

? Nofaol kurs API'da ko'rinishi kerakmi?
+ Yo'q
- Ha
- Faqat admin uchun
- Ba'zan

? curl ... | python3 -m json.tool nima qiladi?
+ JSON'ni chiroyli formatlab ko'rsatadi
- JSON'ni o'chiradi
- Faylga yozadi
- Hech narsa
""",
    "WB30": """
? Telegram'ga xabar qaysi Bot API metodi bilan yuboriladi?
+ sendMessage
- postMessage
- message.send
- notify

? Bot tokeni qayerda saqlanadi?
+ Serverdagi .env faylida
- Kodda
- GitHub'da
- Shablonda

? timeout=5 nega muhim?
+ Telegram sekin bo'lsa sayt kutib qolmasligi uchun
- Xabar 5 marta yuboriladi
- Majburiy
- Hech narsa

? Tarmoq xatosi bo'lsa ariza nima bo'ladi?
+ Saqlangan bo'ladi — faqat xato log'ga yoziladi
- O'chadi
- Sayt to'xtaydi
- Foydalanuvchi xato ko'radi

? Nega notify_admin enrollment.save() dan keyin chaqiriladi?
+ Avval ariza bazaga yozilishi kerak
- Tezlik uchun
- Farqi yo'q
- Xato

? Token bo'lmasa notify_admin nima qiladi?
+ Hech narsa yubormaydi, False qaytaradi
- Xato beradi
- Sayt to'xtaydi
- Admin'ga email yuboradi

? logger.exception nima qiladi?
+ Xato va traceback'ni log'ga yozadi
- Xatoni yashiradi
- Foydalanuvchiga ko'rsatadi
- Hech narsa

? Testda patch nima uchun?
+ Haqiqiy Telegram'ga so'rov yubormaslik uchun
- Kodni o'zgartirish
- Tezlashtirish
- Hech narsa

? side_effect=OSError(...) nima qiladi?
+ Chaqiruvda sun'iy xato chiqaradi
- Xatoni yashiradi
- Qiymat qaytaradi
- Hech narsa

? Ko'p xabar yuboriladigan katta loyihada nima ishlatiladi?
+ Navbat (masalan Celery) — fonda yuborish
- Ko'proq timeout
- Xabarsiz
- Hech narsa
""",
    "WB31": """
? aiohttp nima?
+ Asinxron HTTP so'rovlar kutubxonasi
- Telegram kutubxonasi
- Baza
- Shablon tili

? Nega botda requests emas, aiohttp?
+ Asinxron — so'rov kutilayotganda bot boshqa foydalanuvchilarga javob beradi
- requests pullik
- Tezroq yoziladi
- Farqi yo'q

? ClientTimeout(total=5) nima qiladi?
+ 5 soniyada javob bo'lmasa so'rovni to'xtatadi
- 5 marta urinadi
- 5 ta so'rov
- Hech narsa

? raise_for_status() nima qiladi?
+ Status 4xx/5xx bo'lsa xato chiqaradi
- Statusni o'zgartiradi
- Javobni o'chiradi
- Hech narsa

? Sayt o'chiq bo'lsa bot nima qiladi?
+ Tushunarli xabar: “Sayt hozir javob bermayapti”
- To'xtab qoladi
- Traceback yuboradi
- Javob bermaydi

? SITE_URL qayerda sozlanadi?
+ Botning .env faylida
- Kodda
- Saytda
- Telegram'da

? .rstrip("/") nega kerak?
+ URL oxirida ikki marta / bo'lib qolmasligi uchun
- Xavfsizlik
- Tezlik
- Hech narsa

? f"{450000:,}".replace(",", " ") natijasi?
+ 450 000
- 450,000
- 450000
- Xato

? Yangi router bot.py da qayerga qo'shiladi?
+ include_routers ichida, menu/quiz'dan oldin
- Oxiriga
- Hech qayerga
- Alohida faylga

? Bu darsda bot va sayt qanday bog'landi?
+ Bot saytning JSON API'sidan ma'lumot oladi
- Bitta baza
- Fayl orqali
- Email orqali
""",
    "WB32": """
? Yakuniy loyiha rejasi nimadan boshlanadi?
+ Muammodan — kimga va nima uchun kerak
- Koddan
- Dizayndan
- Texnologiyadan

? MVP nima?
+ Eng kichik ishlaydigan birinchi versiya
- Eng katta versiya
- Dizayn maketi
- Test

? Nega foydalanuvchi turlari yoziladi?
+ Sahifalar va huquqlar shundan kelib chiqadi
- Chiroy uchun
- Shart emas
- Hujjat uchun

? Modellar ro'yxati nima beradi?
+ Baza tuzilmasini oldindan o'ylash
- Kodni yozadi
- Dizayn
- Hech narsa

? Rejada nechta MVP funksiya tavsiya etiladi?
+ 3–5 ta asosiy funksiya
- 20 ta
- 1 ta
- Cheklanmagan

? GitHub Issues nima uchun?
+ Har vazifani alohida kuzatish
- Kod saqlash
- Deploy
- Hech narsa

? Jadval nega kunlarga bo'linadi?
+ Vaqtni nazorat qilish va o'z vaqtida tugatish
- Chiroy uchun
- Shart emas
- Hech narsa

? Reja qayerda saqlanadi?
+ README yoki PLAN.md da — loyiha bilan birga
- Daftarda
- Telegram'da
- Hech qayerda

? Kutubxona loyihasida Loan modeli nimani saqlaydi?
+ Qaysi kitob kimda va qachon olingani
- Kitob nomi
- Foydalanuvchi paroli
- Hech narsa

? Katta g'oyani nima qilish kerak?
+ Kichik MVP'ga qisqartirib, keyin kengaytirish
- Birdaniga hammasini yozish
- Voz kechish
- Hech narsa
""",
    "WB33": """
? Yangi funksiya uchun birinchi qadam?
+ Issue va alohida branch
- To'g'ridan main'ga yozish
- Deploy
- Hech narsa

? TDD nima?
+ Avval test yoziladi, keyin uni o'tkazadigan kod
- Avval kod, testsiz
- Faqat test
- Dizayn usuli

? Avval yozilgan test birinchi marta qanday natija beradi?
+ Yiqiladi (FAIL) — funksiya hali yo'q
- O'tadi
- Xato bermaydi
- Hech narsa

? category.isdigit() nega tekshiriladi?
+ ?category=abc kelsa xato bermasligi uchun
- Tezlik uchun
- Majburiy
- Hech narsa

? filter(category_id=...) ning foydasi?
+ ForeignKey ustuni bo'yicha — qo'shimcha JOIN'siz
- Kategoriyani o'chiradi
- Xato
- Hech narsa

? <option ... selected> nima beradi?
+ Tanlangan kategoriya sahifa yangilanganda ham ko'rinadi
- Kategoriyani o'chiradi
- Majburiy maydon
- Hech narsa

? PR tavsifida “Closes #7” nima qiladi?
+ PR qo'shilganda 7-issue avtomatik yopiladi
- 7 ta commit
- Xato
- Hech narsa

? Nega kichik commitlar yaxshi?
+ Tushunish va kerak bo'lsa qaytarish oson
- Ko'p ko'rinadi
- Majburiy
- Hech qanday

? Uzun qatorni context o'zgaruvchisiga olishning foydasi?
+ Kod o'qilishi oson
- Tezlik
- Majburiy
- Hech qanday

? Funksiya tayyor ekanini nima isbotlaydi?
+ Hamma testlar o'tadi
- Kod uzunligi
- Fayllar soni
- Hech narsa
""",
    "WB34": """
? Code review nima?
+ Kodni boshqa dasturchi tekshirib, izoh berishi
- Kodni o'chirish
- Deploy
- Test

? Code review'da nimani tanqid qilamiz?
+ Kodni, odamni emas — taklif bilan
- Odamni
- Hech narsani
- Faqat dizaynni

? set -euo pipefail nima qiladi?
+ Biror buyruq xato bersa skriptni to'xtatadi
- Xatolarni yashiradi
- Tezlashtiradi
- Hech narsa

? deploy.sh da test nega migrate'dan oldin?
+ Test yiqilsa baza o'zgarmaydi, eski sayt ishlayveradi
- Tasodif
- Tezlik
- Farqi yo'q

? git pull --ff-only nima uchun?
+ Serverda qo'lda o'zgarish bo'lsa aralashtirmay to'xtash
- Majburiy yangilash
- Branch yaratish
- Hech narsa

? collectstatic --noinput nima uchun deploy'da?
+ Yangi CSS/JS fayllar Nginx beradigan papkaga tushishi uchun
- Statiklarni o'chirish
- Test
- Hech narsa

? systemctl is-active --quiet educenter nima tekshiradi?
+ Restart'dan keyin xizmat haqiqatan ishlayaptimi
- Kod to'g'rimi
- Internet bormi
- Hech narsa

? REVIEW.md ro'yxatining foydasi?
+ Hamma bir xil mezon bilan tekshiradi
- Kod yozadi
- Majburiy
- Hech qanday

? Xavfsizlik bo'yicha review'da nima tekshiriladi?
+ .env Git'da yo'q, DEBUG=0, login_required, csrf_token
- Ranglar
- Fayl nomlari
- Hech narsa

? deploy.sh qanday ishga tushiriladi?
+ ./deploy/deploy.sh (chmod +x qilingan bo'lsa)
- python deploy.sh
- git deploy
- systemctl deploy
""",
    "WB35": """
? Portfolio'da nechta loyiha ko'rsatish tavsiya etiladi?
+ Eng yaxshi 3 tasi
- Hammasi
- 1 ta
- 10 ta

? Portfolio kartasida nima bo'lishi kerak?
+ Qisqa tavsif va jonli yoki GitHub havola
- Faqat nom
- Kod
- Hech narsa

? Junior rezyumesida eng kuchli dalil?
+ Ishlaydigan loyihalar
- Yosh
- Sertifikatlar soni
- Sevimli ranglar

? Rezyume qancha hajmda bo'ladi?
+ 1 sahifa
- 5 sahifa
- 10 sahifa
- Cheklanmagan

? Portfolio yangilangach GitHub Pages qachon yangilanadi?
+ git push'dan keyin bir necha daqiqada
- Bir haftada
- Hech qachon
- Qo'lda yuklanadi

? 9-oydagi filtr tugmalari qaysi maydon bilan ishlaydi?
+ tags
- url
- title
- text

? GitHub'dagi “pinned” repozitoriy nima?
+ Profilda ko'zga tashlanadigan qilib qo'yilgan loyiha
- O'chirilgan repo
- Yashirin repo
- Fork

? Rezyumeda loyiha qanday tasvirlanadi?
+ Nima qiladi va qaysi texnologiya — bir qatorda
- Butun kod
- Faqat nom
- Hech narsa

? Rezyume qanday formatda yuboriladi?
+ PDF
- .py
- .exe
- Rasm

? GitHub profil README nima?
+ Profil sahifasidagi o'zingiz haqingizdagi qisqa matn
- Loyiha kodi
- Litsenziya
- Hech narsa
""",
    "WB36": """
? Demo Day taqdimoti qancha davom etadi?
+ 5 daqiqa
- 30 daqiqa
- 1 daqiqa
- 1 soat

? Demo nimadan boshlanadi?
+ Muammodan
- Koddan
- Texnologiyalar ro'yxatidan
- Savollardan

? Baholashda eng katta ulush?
+ Ishlashi (internetda, HTTPS) — 40 ball
- Taqdimot
- README
- Kod uzunligi

? Kod sifati va testlarga necha ball?
+ 30
- 40
- 10
- 20

? Demo oldidan saytni qanday tekshiramiz?
+ curl -sI https://... | head -1 — HTTP/2 200
- Tekshirmaymiz
- Faqat lokal
- Hech narsa

? Bilmagan savolga qanday javob beramiz?
+ Halol: “hali sinamadim, tekshiraman”
- To'qib chiqaramiz
- Javob bermaymiz
- Mavzuni o'zgartiramiz

? Demo lokal kompyuterda emas, qayerda ko'rsatiladi?
+ Internetdagi serverda
- Telefonda rasm bilan
- Faqat kodda
- Hech qayerda

? 11 oyda qaysi yo'l bosib o'tildi?
+ Python → Telegram bot → Portfolio → Django → server va integratsiya
- Faqat HTML
- Faqat Scratch
- Faqat Excel

? Kursdan keyin qaysi texnologiyalarni o'rganish mumkin?
+ Django REST Framework, Celery, Docker
- Hech narsa
- Faqat Word
- Scratch

? Loyihani himoyadan keyin nima qilish kerak?
+ Rivojlantirishda davom etish va fikr so'rash
- O'chirish
- Unutish
- Hech narsa
""",
}
