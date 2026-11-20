"""Dasturchi 10-oy (WB13–WB24, EduCenter Django sayti) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "WB13": """
? Django nima?
+ Python'da sayt yaratish uchun web-freymvork
- Ma'lumotlar bazasi
- Brauzer
- Telegram kutubxonasi

? MVT'da “M” nima?
+ Model — ma'lumotlar va baza
- Menyu
- Media
- Modul

? MVT'da “V” nima qiladi?
+ So'rovni qayta ishlab javob tayyorlaydi
- Faqat rang beradi
- Bazani o'chiradi
- Rasm yuklaydi

? MVT'da “T” nima?
+ Template — HTML ko'rinish
- Test
- Terminal
- Token

? django-admin startproject config . dagi nuqta nimani bildiradi?
+ Loyiha joriy papkada yaratiladi
- Xato
- Yangi papka ochiladi
- Hech narsa

? python manage.py runserver nima qiladi?
+ Ishlab chiqish serverini 8000-portda ishga tushiradi
- Serverni o'chiradi
- Bazani yaratadi
- Loyihani GitHub'ga yuklaydi

? Birinchi migrate nima yaratadi?
+ Django'ning tayyor jadvallarini (foydalanuvchilar, sessiyalar)
- Kurslar jadvalini
- HTML fayllarni
- Hech narsa

? LANGUAGE_CODE = "uz" nima beradi?
+ Django xabarlari va admin o'zbekcha bo'ladi
- Kod o'zbekcha yoziladi
- Sayt o'zi tarjima qilinadi
- Hech narsa

? Nega Django saytini GitHub Pages'ga qo'yib bo'lmaydi?
+ Python kodi serverda ishlashi kerak, Pages faqat statik fayl beradi
- Django pullik
- GitHub taqiqlagan
- Mumkin

? db.sqlite3 .gitignore'da nega bor?
+ Bu lokal baza — har kompyuterda o'ziniki
- Juda kichik
- Kod emas, lekin kerak
- Xato
""",
    "WB14": """
? App nima?
+ Loyihaning alohida qismi (masalan courses)
- Telefon ilovasi
- Shablon
- Baza

? Yangi app qanday yaratiladi?
+ python manage.py startapp courses
- django-admin newapp
- pip install courses
- mkdir courses

? App yaratilgach nima qilish shart?
+ INSTALLED_APPS ga qo'shish
- Serverni o'chirish
- Bazani o'chirish
- Hech narsa

? include("courses.urls") nima qiladi?
+ App URL'larini loyiha URL'lariga ulaydi
- Faylni o'chiradi
- Shablonni yuklaydi
- Hech narsa

? render(request, "courses/home.html") nima qaytaradi?
+ Shablondan yasalgan HTML javob
- JSON
- Faylni
- Xato

? {% extends "base.html" %} nima qiladi?
+ Shablonni base.html asosida quradi
- base.html ni o'chiradi
- Yangi sahifa ochadi
- Hech narsa

? {% block content %} nima uchun?
+ Har sahifa shu joyni o'z mazmuni bilan to'ldiradi
- Kodni bloklaydi
- Izoh
- Xato

? name="home" URL'da nima beradi?
+ Shablonda {% url 'home' %} bilan havola yasash
- Sahifa sarlavhasi
- Fayl nomi
- Hech narsa

? {% static 'css/style.css' %} nima qiladi?
+ Statik fayl manzilini yasaydi
- CSS yozadi
- Rasm yuklaydi
- Hech narsa

? "DIRS": [BASE_DIR / "templates"] nimani bildiradi?
+ Umumiy shablonlar papkasi
- Rasm papkasi
- Baza fayli
- Xato
""",
    "WB15": """
? Django modeli nima?
+ Bazadagi jadvalni ifodalovchi Python klass
- HTML fayl
- URL
- CSS

? CharField uchun nima majburiy?
+ max_length
- default
- unique
- Hech narsa

? SlugField nima uchun?
+ URL uchun qisqa nom (python-asoslari)
- Rasm uchun
- Narx uchun
- Parol uchun

? unique=True nima qiladi?
+ Bir xil qiymat ikki marta bo'lmaydi
- Maydonni yashiradi
- Majburiy qiladi
- Hech narsa

? auto_now_add=True nima qiladi?
+ Yaratilgan vaqtni avtomatik yozadi
- Har o'zgarishda vaqtni yangilaydi
- Vaqtni o'chiradi
- Hech narsa

? makemigrations nima qiladi?
+ Model o'zgarishidan migratsiya faylini yasaydi
- Jadvalni darhol yaratadi
- Serverni ishga tushiradi
- Bazani o'chiradi

? migrate nima qiladi?
+ Migratsiyalarni bazaga qo'llaydi
- Fayl yasaydi
- Kodni tekshiradi
- Hech narsa

? __str__ modelda nima uchun?
+ Admin va shell'da obyektning chiroyli nomi
- Saqlash uchun
- Majburiy maydon
- Hech narsa

? Course.objects.create(...) nima qiladi?
+ Bazaga yangi qator qo'shadi
- Jadval yaratadi
- Qatorni o'chiradi
- Hech narsa

? ORM nima?
+ SQL yozmasdan Python orqali baza bilan ishlash
- Server
- Shablon tili
- Brauzer
""",
    "WB16": """
? Admin uchun foydalanuvchi qanday yaratiladi?
+ python manage.py createsuperuser
- python manage.py runserver
- django-admin user
- Admin o'zi yaratadi

? @admin.register(Course) nima qiladi?
+ Course modelini admin panelga qo'shadi
- Modelni o'chiradi
- URL yaratadi
- Hech narsa

? list_display nima?
+ Ro'yxatda ko'rinadigan ustunlar
- Filtrlar
- Qidiruv
- Tartib

? list_editable nima beradi?
+ Ro'yxatning o'zida qiymatni o'zgartirish
- Ro'yxatni yashiradi
- Ustun qo'shadi
- Hech narsa

? search_fields nima qiladi?
+ Admin'da qidiruv maydonini qo'shadi
- Filtr yaratadi
- Ustunlarni o'chiradi
- Hech narsa

? prepopulated_fields = {"slug": ["title"]} nima qiladi?
+ Slug sarlavhadan avtomatik to'ldiriladi
- Slugni o'chiradi
- Sarlavhani o'zgartiradi
- Hech narsa

? Mavjud kurslar bor jadvalga yangi maydon qo'shganda default nega kerak?
+ Eski qatorlar uchun qiymat bo'lishi kerak
- Tezlik uchun
- Shart emas
- Xato

? PositiveIntegerField nimani kafolatlaydi?
+ Manfiy son kiritib bo'lmaydi
- Faqat juft son
- Faqat matn
- Hech narsa

? Admin manzili qanday?
+ /admin/
- /panel/
- /root/
- /login/

? Admin parolini qanday saqlash kerak?
+ Murakkab parol, hech kimga bermaslik
- Oddiy 123
- Kodga yozish
- GitHub'ga yuklash
""",
    "WB17": """
? Course.objects.filter(is_active=True) nima qaytaradi?
+ Faqat faol kurslar QuerySet'ini
- Bitta kursni
- Sonni
- Xato

? [:3] QuerySet'da nima qiladi?
+ Faqat birinchi 3 tasini oladi
- 3-kursni oladi
- 3 ta o'chiradi
- Hech narsa

? View'dan shablonga ma'lumot qanday uzatiladi?
+ Context lug'ati orqali
- Global o'zgaruvchi orqali
- Fayl orqali
- Uzatib bo'lmaydi

? {% for course in courses %} nima qiladi?
+ Har kurs uchun blokni takrorlaydi
- Bitta kursni chiqaradi
- Kurslarni o'chiradi
- Hech narsa

? {% empty %} qachon ishlaydi?
+ Ro'yxat bo'sh bo'lsa
- Har doim
- Xato bo'lsa
- Hech qachon

? {% include "courses/_card.html" %} nima beradi?
+ Kartani bitta faylda yozib, ko'p joyda ishlatish
- Faylni o'chiradi
- Yangi sahifa
- Hech narsa

? truncatewords:15 filtri nima qiladi?
+ Matnni 15 so'zdan keyin qisqartiradi
- 15 belgi qoldiradi
- 15 marta takrorlaydi
- Hech narsa

? order_by("price") nima qiladi?
+ Narx bo'yicha o'sish tartibida saralaydi
- Narxni o'chiradi
- Filtrlaydi
- Hech narsa

? {{ course.title }} nima?
+ Shablonda o'zgaruvchi qiymatini chiqarish
- Izoh
- Teg
- Xato

? Meta: ordering = ["title"] nima qiladi?
+ Standart tartib — sarlavha bo'yicha
- Sarlavhani yashiradi
- Ustun qo'shadi
- Hech narsa
""",
    "WB18": """
? <slug:slug> URL'da nima qiladi?
+ URL qismini view'ga slug parametri qilib beradi
- Xato
- Slugni o'chiradi
- Hech narsa

? get_object_or_404 nima qiladi?
+ Obyektni topadi, topilmasa 404 qaytaradi
- Doim 404
- Obyekt yaratadi
- Hech narsa

? Nega get_object_or_404 da is_active=True ham beriladi?
+ Nofaol kursni havola bilan ham ochib bo'lmasin
- Tezlik uchun
- Shart emas
- Xato

? get_absolute_url nima qaytaradi?
+ Obyekt sahifasining manzilini
- Rasm manzilini
- Admin manzilini
- Hech narsa

? reverse("course_detail", args=[slug]) nima qiladi?
+ URL nomidan manzil yasaydi
- URL'ni o'chiradi
- Sahifani ochadi
- Hech narsa

? reverse ishlatishning foydasi?
+ URL o'zgarsa ham havolalar buzilmaydi
- Tezroq
- Shart
- Hech qanday

? linebreaks filtri nima qiladi?
+ Matndagi qator ko'chishlarini <p> va <br> ga aylantiradi
- Matnni o'chiradi
- Qisqartiradi
- Hech narsa

? 404 kodi nimani bildiradi?
+ Sahifa topilmadi
- Server xatosi
- Ruxsat yo'q
- Hammasi joyida

? redirect(course) nima qiladi?
+ get_absolute_url manziliga yo'naltiradi
- Kursni o'chiradi
- Xato
- Hech narsa

? {% block title %} nima uchun?
+ Brauzer tabida har sahifaning o'z nomi
- Sahifa sarlavhasi rangi
- Izoh
- Hech narsa
""",
    "WB19": """
? ForeignKey qanday bog'lanish?
+ Ko'pga-bir: ko'p kurs bitta kategoriyada
- Birga-bir
- Ko'pga-ko'p
- Bog'lanish emas

? ManyToManyField qanday bog'lanish?
+ Ko'pga-ko'p: kursda ko'p ustoz, ustozda ko'p kurs
- Ko'pga-bir
- Birga-bir
- Bog'lanish emas

? on_delete=models.PROTECT nima qiladi?
+ Kursi bor kategoriyani o'chirishga yo'l qo'ymaydi
- Hammasini o'chiradi
- Qiymatni bo'sh qiladi
- Hech narsa

? related_name="courses" nima beradi?
+ Teskari tomondan murojaat: category.courses.all()
- Yangi maydon
- Jadval nomi
- Hech narsa

? Shablonda ustozlar ro'yxati qanday olinadi?
+ course.teachers.all (qavssiz)
- course.teachers()
- course.teachers[]
- teachers.course

? null=True va blank=True farqi?
+ null — bazada bo'sh, blank — formada bo'sh qoldirish mumkin
- Farqi yo'q
- Ikkalasi ham baza uchun
- Ikkalasi ham forma uchun

? verbose_name_plural nima uchun?
+ Admin'dagi ko'plik nomi (categories)
- Jadval nomi
- URL
- Hech narsa

? list_filter admin'da nima qiladi?
+ O'ng tomonda filtrlar paneli
- Qidiruv maydoni
- Ustunlar
- Hech narsa

? <int:pk> URL'da nima?
+ Butun son parametri — obyekt ID'si
- Matn
- Xato
- Slug

? Kategoriya qo'shilganda nega yangi migratsiya kerak?
+ Bazada yangi jadval va ustun paydo bo'ladi
- Shart emas
- Tezlik uchun
- Xato
""",
    "WB20": """
? ImageField uchun qaysi kutubxona kerak?
+ Pillow
- NumPy
- requests
- aiogram

? Bazada rasm qanday saqlanadi?
+ Faqat fayl yo'li, fayl esa media papkada
- Rasmning o'zi
- Base64 matn
- Saqlanmaydi

? upload_to="courses/" nimani bildiradi?
+ media ichidagi papka
- URL
- Baza jadvali
- Hech narsa

? MEDIA_ROOT nima?
+ Yuklangan fayllar saqlanadigan papka
- CSS papkasi
- Shablonlar papkasi
- Baza

? static va media farqi?
+ static — loyiha fayllari, media — foydalanuvchi yuklagan fayllar
- Farqi yo'q
- media — CSS
- static — rasmlar

? urlpatterns += static(...) nega if settings.DEBUG ichida?
+ Faqat ishlab chiqishda; serverda media'ni Nginx beradi
- Xavfsizlik uchun o'chiriladi
- Shart emas
- Xato

? {% if course.image %} nega kerak?
+ Rasm yo'q bo'lsa .url xato bermasligi uchun
- Tezlik uchun
- Shart emas
- Rasmni yuklaydi

? object-fit: cover nima qiladi?
+ Rasm cho'zilmasdan konteynerni to'ldiradi
- Rasmni yashiradi
- Rasmni aylantiradi
- Hech narsa

? aspect-ratio: 16 / 9 nima beradi?
+ Hamma rasmlar bir xil nisbatda
- Rasm 16 piksel
- Rasmni o'chiradi
- Hech narsa

? media/ nega .gitignore'da?
+ Foydalanuvchi fayllari kodga kirmaydi
- Juda kichik
- Xato
- Shart emas
""",
    "WB21": """
? ModelForm nima?
+ Maydonlari modeldan olinadigan forma
- HTML forma
- Admin
- Model

? EnrollmentForm(request.POST or None) nima beradi?
+ GET'da bo'sh, POST'da to'ldirilgan forma
- Doim bo'sh
- Xato
- Faqat POST

? form.is_valid() nima qiladi?
+ Ma'lumotlarni tekshiradi, xatolarni yig'adi
- Saqlaydi
- O'chiradi
- Hech narsa

? save(commit=False) nima uchun?
+ Saqlashdan oldin qo'shimcha maydon (course) qo'yish
- Saqlamaslik
- O'chirish
- Hech narsa

? {% csrf_token %} nimadan himoya qiladi?
+ Begona saytdan soxta forma yuborishdan
- Viruslardan
- Spamdan
- Hech narsadan

? CSRF token yo'q POST so'rovga Django nima qaytaradi?
+ 403 Forbidden
- 200
- 404
- 500

? Nega muvaffaqiyatli POST'dan keyin redirect qilinadi?
+ F5 bosilsa forma ikki marta yuborilmasligi uchun
- Tezlik uchun
- Shart emas
- Xato

? messages.success nima qiladi?
+ Keyingi sahifada bir marta ko'rinadigan xabar qo'yadi
- Email yuboradi
- Log yozadi
- Hech narsa

? form.as_p nima chiqaradi?
+ Label, maydon va xatolarni <p> ichida
- Faqat tugma
- JSON
- Hech narsa

? fields = ["name", "phone"] nimani bildiradi?
+ Formada faqat shu maydonlar bo'ladi
- Bazada faqat shu maydonlar
- Xato
- Hech narsa
""",
    "WB22": """
? include("django.contrib.auth.urls") nima beradi?
+ Tayyor login, logout va parol o'zgartirish URL'lari
- Admin panel
- Ro'yxatdan o'tish sahifasi
- Hech narsa

? Login shabloni qayerda bo'lishi kerak?
+ templates/registration/login.html
- templates/login.html
- accounts/login.py
- static/login.html

? UserCreationForm nima?
+ Login va ikki marta parol bilan tayyor ro'yxatdan o'tish formasi
- Login formasi
- Admin formasi
- Model

? login(request, user) nima qiladi?
+ Foydalanuvchini tizimga kiritadi (sessiya)
- Yangi foydalanuvchi yaratadi
- Parolni o'zgartiradi
- Hech narsa

? Shablonda kirgan-kirmaganini qanday bilamiz?
+ {% if user.is_authenticated %}
- {% if login %}
- {% if session %}
- Bilib bo'lmaydi

? Django 5'da logout qanday qilinadi?
+ POST forma bilan (csrf_token bilan)
- Oddiy havola bilan
- JavaScript bilan
- Brauzerni yopib

? LOGIN_REDIRECT_URL nima?
+ Kirgandan keyin qaysi sahifaga o'tish
- Login sahifasi manzili
- Admin manzili
- Hech narsa

? Zaif parol (masalan 123) bilan ro'yxatdan o'tsa?
+ Forma xato ko'rsatadi — parol validatorlari
- Qabul qilinadi
- Server o'chadi
- Hech narsa

? Parollar bazada qanday saqlanadi?
+ Xeshlangan holda — asl parolni ko'rib bo'lmaydi
- Ochiq matn
- Base64
- Saqlanmaydi

? Nega foydalanuvchi kodi alohida accounts app'ida?
+ Har app bitta vazifa — tartib va qayta ishlatish oson
- Django talab qiladi
- Tezlik uchun
- Shart emas
""",
    "WB23": """
? @login_required nima qiladi?
+ Kirmagan foydalanuvchini login sahifasiga yo'naltiradi
- Hammaga ruxsat beradi
- Sahifani o'chiradi
- Hech narsa

? ?next= parametri nima uchun?
+ Login'dan keyin avvalgi sahifaga qaytish
- Keyingi sahifa raqami
- Xato
- Hech narsa

? request.user.enrollments nima qaytaradi?
+ Faqat shu foydalanuvchining arizalari
- Hamma arizalar
- Kurslar
- Hech narsa

? on_delete=models.SET_NULL nima qiladi?
+ Foydalanuvchi o'chsa, ariza qoladi, user bo'sh bo'ladi
- Arizani o'chiradi
- O'chirishga yo'l qo'ymaydi
- Hech narsa

? select_related("course") nima beradi?
+ Kurslarni bitta so'rovda olib, bazaga so'rovlarni kamaytiradi
- Kurslarni o'chiradi
- Filtrlaydi
- Hech narsa

? request.GET.get("q", "") nima qiladi?
+ URL'dagi q parametrini oladi, bo'lmasa bo'sh satr
- Formani yuboradi
- Xato
- Hech narsa

? Qidiruv formasi nega method="get"?
+ Natija URL'da ko'rinadi, havolani ulashish mumkin
- Xavfsizroq
- Shart
- Tezroq

? icontains nima qiladi?
+ Katta-kichik harfga qaramay matn ichidan qidiradi
- Aniq moslik
- Raqam qidiradi
- Hech narsa

? Q(title__icontains=q) | Q(description__icontains=q) nimani bildiradi?
+ Sarlavhada YOKI tavsifda
- Sarlavhada VA tavsifda
- Xato
- Hech narsa

? Nega kabinetda boshqalarning arizalari ko'rinmasligi kerak?
+ Shaxsiy ma'lumot (telefon) — maxfiylik
- Joy kam
- Tezlik uchun
- Farqi yo'q
""",
    "WB24": """
? Management command fayli qayerda bo'ladi?
+ app/management/commands/nomi.py
- app/commands.py
- config/commands/
- templates/

? Buyruq qanday ishga tushiriladi?
+ python manage.py seed_demo
- python seed_demo.py
- django seed_demo
- pip seed_demo

? Buyruq klassida asosiy metod?
+ handle
- run
- main
- execute_now

? get_or_create nima qiladi?
+ Bor bo'lsa oladi, yo'q bo'lsa yaratadi
- Doim yaratadi
- Doim o'chiradi
- Hech narsa

? update_or_create nima qiladi?
+ Bor bo'lsa yangilaydi, yo'q bo'lsa yaratadi
- Faqat yaratadi
- Faqat o'chiradi
- Hech narsa

? seed_demo ikki marta ishga tushsa kurslar soni?
+ O'zgarmaydi — 4 ta
- 8 ta
- 0 ta
- Xato

? management/ papkasida __init__.py nega kerak?
+ Papka Python paketi bo'lishi uchun
- Shart emas
- Baza uchun
- Xato

? Demo nimadan boshlanadi?
+ Foydalanuvchi ko'zi bilan saytdan
- Koddan
- Admin'dan
- Terminaldan

? Kod tahlilida nima tekshiriladi?
+ Nomlar, takrorlanish va xavfsizlik (login_required, CSRF)
- Faqat ranglar
- Fayllar soni
- Hech narsa

? 11-oyda EduCenter bilan nima qilinadi?
+ Serverga joylanadi va bot bilan bog'lanadi
- O'chiriladi
- Qaytadan yoziladi
- Hech narsa
""",
}
