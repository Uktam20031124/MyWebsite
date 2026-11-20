"""Dasturchi 9-oy (WB01–WB12, Portfolio sayti) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "WB01": """
? Sayt ochilganda brauzer serverdan nimani oladi?
+ HTML faylni
- Python kodini
- Telegram xabarini
- Bazani

? HTML nima?
+ Sahifa tuzilmasini belgilovchi teglar tili
- Dasturlash tili
- Uslub tili
- Baza

? <!DOCTYPE html> nimani bildiradi?
+ Hujjat zamonaviy HTML5 ekanini
- Sahifa sarlavhasini
- Izohni
- Xatoni

? Ekranda ko'rinadigan mazmun qaysi tegda bo'ladi?
+ <body>
- <head>
- <title>
- <meta>

? <title> qayerda ko'rinadi?
+ Brauzer tabida
- Sahifa o'rtasida
- Footer'da
- Ko'rinmaydi

? meta charset="UTF-8" nega kerak?
+ o‘, g‘ kabi harflar to'g'ri chiqishi uchun
- Sahifa tez yuklanishi uchun
- Rang uchun
- Shart emas

? viewport meta nima qiladi?
+ Telefonda sahifa to'g'ri kattalikda ochiladi
- Rasm qo'shadi
- Sahifani yashiradi
- Shriftni o'zgartiradi

? Sahifada nechta <h1> bo'lishi tavsiya etiladi?
+ Bitta
- Uchta
- Har bo'limda bittadan
- Cheklanmagan

? </p> nima?
+ Yopiluvchi teg
- Ochiluvchi teg
- Atribut
- Izoh

? lang="uz" nima uchun?
+ Sahifa tilini ekran o'quvchi va qidiruv tizimlariga bildiradi
- Tarjima qiladi
- Shrift tanlaydi
- Shart emas
""",
    "WB02": """
? Rasm qaysi teg bilan qo'shiladi?
+ <img>
- <pic>
- <image>
- <src>

? alt atributi nima uchun?
+ Rasm ochilmasa yoki ko'rmaydigan foydalanuvchi uchun matn
- Rasm o'lchami
- Rasm manzili
- Rasm rangi

? Havola qaysi teg bilan yoziladi?
+ <a href="...">
- <link>
- <url>
- <href>

? target="_blank" nima qiladi?
+ Havolani yangi tabda ochadi
- Havolani yashiradi
- Sahifani yopadi
- Hech narsa

? Nuqtali ro'yxat qaysi teg?
+ <ul>
- <ol>
- <li>
- <list>

? Ro'yxat elementi qaysi teg?
+ <li>
- <ul>
- <item>
- <el>

? <strong> nima qiladi?
+ Muhim so'zni qalin ko'rsatadi
- Rang beradi
- Havola qiladi
- O'chiradi

? src="images/ali.jpg" qanday yo'l?
+ Nisbiy — index.html yonidagi images papkasidan
- To'liq internet manzil
- Xato
- Faqat serverda ishlaydi

? Atribut nima?
+ Tegning qo'shimcha sozlamasi (masalan href, src)
- Yangi teg
- Izoh
- CSS fayli

? Raqamli ro'yxat qaysi teg?
+ <ol>
- <ul>
- <nl>
- <num>
""",
    "WB03": """
? Semantik teg nima?
+ Mazmunining ma'nosini bildiruvchi teg (header, nav, footer)
- Rangli teg
- Yashirin teg
- Eski teg

? Navigatsiya menyusi qaysi tegda?
+ <nav>
- <menu>
- <head>
- <section>

? href="#about" nima qiladi?
+ Shu sahifadagi id="about" bo'limiga sakraydi
- Yangi sahifa ochadi
- Xato
- Hech narsa

? <article> qachon ishlatiladi?
+ Mustaqil mazmun uchun (masalan bitta loyiha kartasi)
- Menyu uchun
- Sarlavha uchun
- Rasm uchun

? <label for="name"> nima beradi?
+ Yozuv bosilganda maydon faollashadi
- Maydonni yashiradi
- Maydonni o'chiradi
- Hech narsa

? required atributi nima qiladi?
+ Maydonni bo'sh qoldirib yuborib bo'lmaydi
- Maydonni yashiradi
- Qiymat beradi
- Hech narsa

? type="email" nima qiladi?
+ Brauzer email formatini tekshiradi
- Email yuboradi
- Parolni yashiradi
- Hech narsa

? Ko'p qatorli matn maydoni qaysi teg?
+ <textarea>
- <input>
- <text>
- <p>

? Asosiy mazmun qaysi tegda?
+ <main>
- <body>
- <div>
- <head>

? class atributi nima uchun?
+ Keyin CSS bilan bezash uchun nom berish
- Havola uchun
- Rasm uchun
- Shart emas
""",
    "WB04": """
? CSS fayl HTML'ga qanday ulanadi?
+ <link rel="stylesheet" href="style.css">
- <script src="style.css">
- <css>style.css</css>
- <style href>

? .card selektori nimani tanlaydi?
+ class="card" bo'lgan elementlarni
- id="card" ni
- <card> tegini
- Hammasini

? padding nima?
+ Element ichidagi bo'shliq
- Tashqi bo'shliq
- Chegara
- Rang

? margin nima?
+ Elementning tashqi bo'shlig'i
- Ichki bo'shliq
- Shrift
- Chegara

? box-sizing: border-box nima beradi?
+ Kenglikka padding va border ham kiradi
- Burchaklar yumaloq
- Soyalar
- Hech narsa

? margin: 0 auto nima qiladi?
+ Blokni gorizontal markazga qo'yadi
- Blokni yashiradi
- Chapga suradi
- Hech narsa

? * selektori nimani tanlaydi?
+ Hamma elementlarni
- Faqat body'ni
- Faqat class'larni
- Hech narsani

? border-radius nima qiladi?
+ Burchaklarni yumaloqlaydi
- Chegara rangini
- Soyani
- Shriftni

? line-height nima?
+ Qatorlar orasidagi masofa
- Shrift o'lchami
- Kenglik
- Rang

? max-width: 960px nima beradi?
+ Katta ekranda ham matn juda kengayib ketmaydi
- Blokni yashiradi
- Telefonni o'chiradi
- Hech narsa
""",
    "WB05": """
? display: flex nima qiladi?
+ Ichki elementlarni bir qatorga tizadi
- Elementni yashiradi
- Grid yaratadi
- Rang beradi

? justify-content: space-between nima qiladi?
+ Birinchi element chapda, oxirgisi o'ngda, oraliq teng
- Hammasini markazga
- Hammasini chapga
- Hech narsa

? align-items: center nima qiladi?
+ Elementlarni ko'ndalang o'q bo'yicha markazlaydi
- Yashiradi
- Kattalashtiradi
- Hech narsa

? gap nima?
+ Elementlar orasidagi masofa
- Chegara
- Ichki bo'shliq
- Shrift

? flex-direction: column nima qiladi?
+ Elementlarni ustma-ust joylaydi
- Bir qatorga
- Yashiradi
- Teskari aylantiradi

? border-radius: 50% kvadrat rasmga nima qiladi?
+ Dumaloq qiladi
- Yashiradi
- Kattalashtiradi
- Hech narsa

? list-style: none nima qiladi?
+ Ro'yxat nuqtalarini olib tashlaydi
- Ro'yxatni o'chiradi
- Rang beradi
- Hech narsa

? Bitta elementga ikki class qanday beriladi?
+ class="btn btn-outline"
- class="btn,btn-outline"
- class="btn" class="btn-outline"
- Mumkin emas

? Flexbox qachon qulay?
+ Elementlarni bir o'q bo'ylab (qator yoki ustun) joylashda
- Faqat jadvalda
- Faqat rasmda
- Hech qachon

? cursor: pointer nima qiladi?
+ Sichqoncha ko'rsatkichi qo'lcha bo'ladi
- Tugmani o'chiradi
- Rang beradi
- Hech narsa
""",
    "WB06": """
? display: grid nima yaratadi?
+ Ustun va qatorlardan iborat to'r
- Bir qator
- Jadval tegi
- Hech narsa

? repeat(auto-fit, minmax(240px, 1fr)) nima qiladi?
+ Sig'gancha ustun yaratadi, har biri kamida 240px
- Doim 3 ustun
- Doim 1 ustun
- Xato

? 1fr nimani bildiradi?
+ Bo'sh joyning bir ulushi
- 1 piksel
- 1 foiz
- 1 qator

? auto-fit bilan telefonda nechta ustun bo'ladi?
+ Sig'ganicha — odatda 1
- Doim 3
- 0
- 10

? Grid'da gap nima?
+ Kataklar orasidagi masofa
- Chegara
- Rang
- Shrift

? inline-block nima beradi?
+ Matn ichida turadi, lekin padding va o'lcham oladi
- Yangi qatordan
- Yashiradi
- Hech narsa

? border-radius: 999px nima qiladi?
+ To'liq yumaloq chetli yorliq
- Kvadrat
- Yashiradi
- Hech narsa

? Grid va Flexbox farqi?
+ Grid ikki o'lchamli (ustun + qator), Flexbox bir o'qli
- Farqi yo'q
- Flexbox yangi
- Grid faqat rasmlar uchun

? Kartalar konteyneri qaysi class bilan yozildi?
+ .grid
- .flex
- .card
- .list

? minmax(240px, 1fr) nima kafolatlaydi?
+ Karta 240px dan torroq bo'lmaydi
- Karta 240px dan kengroq bo'lmaydi
- Karta yashiriladi
- Hech narsa
""",
    "WB07": """
? Media query nima?
+ Ekran o'lchamiga qarab CSS qoidalarini qo'llash
- JS funksiya
- HTML teg
- Rasm formati

? @media (max-width: 700px) qachon ishlaydi?
+ Ekran kengligi 700px yoki undan tor bo'lsa
- 700px dan keng bo'lsa
- Doim
- Hech qachon

? Telefonda menyu nega yashiriladi?
+ Joy kam — ☰ tugmasi ostiga yig'iladi
- Kerak emas
- Xato
- Sekin bo'lgani uchun

? position: absolute nimaga nisbatan joylashadi?
+ Eng yaqin position: relative ota elementga
- Doim sahifaga
- Ekranga
- Hech narsaga

? aria-label="Menyu" nima uchun?
+ Ekran o'quvchi tugmani “Menyu” deb o'qiydi
- Rang uchun
- Tezlik uchun
- Shart emas

? aria-expanded nimani bildiradi?
+ Menyu ochiq yoki yopiqligini
- Tugma rangini
- Sahifa tilini
- Hech narsa

? .menu.open selektori nimani tanlaydi?
+ Ikkala class'ga ega elementni
- Faqat .menu ni
- Faqat .open ni
- Xato

? Telefonda tugmalar nega kattaroq padding oladi?
+ Barmoq bilan bosish qulay bo'lishi uchun
- Chiroy uchun
- Shart emas
- Xato

? Brauzerda telefon ko'rinishini qanday tekshiramiz?
+ F12 → qurilma rejimi (device toolbar)
- Sahifani yangilab
- Telefon sotib olib
- Iloji yo'q

? Telefonda gorizontal aylantirish paydo bo'lsa?
+ Biror element ekrandan keng — tuzatish kerak
- Hammasi joyida
- Telefon eski
- Shunday bo'lishi kerak
""",
    "WB08": """
? CSS o'zgaruvchi qanday e'lon qilinadi?
+ --accent: #0f766e;
- $accent = #0f766e
- var accent
- @accent

? O'zgaruvchi qiymati qanday olinadi?
+ var(--accent)
- $(accent)
- {{ accent }}
- get(--accent)

? :root nima?
+ Hujjatning ildiz elementi (html)
- body
- Birinchi div
- Xato

? [data-theme="dark"] selektori nimani tanlaydi?
+ data-theme="dark" atributi bor elementni
- dark class'ini
- Hamma elementni
- Hech narsani

? O'zgaruvchilarning asosiy foydasi?
+ Rangni bir joyda o'zgartirsangiz hamma joyda o'zgaradi
- Sahifa tezlashadi
- JS kerak bo'lmaydi
- Hech qanday

? transition nima qiladi?
+ Xususiyat o'zgarishini silliq qiladi
- Elementni yashiradi
- Rang beradi
- Hech narsa

? :hover qachon ishlaydi?
+ Sichqoncha element ustiga kelganda
- Bosilganda
- Sahifa ochilganda
- Hech qachon

? transform: translateY(-4px) nima qiladi?
+ Elementni 4px yuqoriga suradi
- Pastga
- Aylantiradi
- Kattalashtiradi

? prefers-reduced-motion nima uchun?
+ Harakatni yoqtirmaydigan foydalanuvchilar uchun animatsiyani o'chirish
- Animatsiyani tezlashtirish
- Telefon uchun
- Shart emas

? rgba(0, 0, 0, 0.08) dagi oxirgi son nima?
+ Shaffoflik
- Qizil rang
- O'lcham
- Burchak
""",
    "WB09": """
? JS fayl qanday ulanadi?
+ <script src="script.js" defer></script>
- <link href="script.js">
- <js>script.js</js>
- <style src>

? defer nima qiladi?
+ Skript sahifa to'liq yuklangach ishlaydi
- Skriptni o'chiradi
- Skriptni tezlashtiradi
- Hech narsa

? const va let farqi?
+ const qayta tayinlanmaydi, let qiymati o'zgarishi mumkin
- Farqi yo'q
- let qayta tayinlanmaydi
- const faqat son

? document.querySelector("#year") nima qaytaradi?
+ id="year" bo'lgan birinchi elementni
- Hamma elementlarni
- Yilni
- Xato

? textContent nima?
+ Element ichidagi matn
- Element rangi
- Element class'i
- HTML fayl

? new Date().getHours() nima qaytaradi?
+ Hozirgi soatni (0–23)
- Daqiqani
- Sanani
- Yilni

? JS'da else if Python'dagi qaysi so'zga mos?
+ elif
- else
- if
- try

? `${text}!` nima?
+ Shablon satr — Python f-string kabi
- Xato
- Izoh
- Massiv

? JS'da kod bloki qanday belgilanadi?
+ Jingalak qavslar { } bilan
- Chekinish bilan
- end so'zi bilan
- Nuqta-vergul bilan

? Brauzerda JS xatolarini qayerda ko'ramiz?
+ F12 → Console
- Sahifa pastida
- Tab nomida
- Ko'rib bo'lmaydi
""",
    "WB10": """
? addEventListener("click", ...) nima qiladi?
+ Element bosilganda funksiyani chaqiradi
- Elementni bosadi
- Elementni o'chiradi
- Hech narsa

? () => { } nima?
+ Arrow funksiya — qisqa yozuv
- Xato
- Massiv
- Obyekt

? classList.toggle("open") nima qiladi?
+ open class'i bo'lsa olib tashlaydi, yo'q bo'lsa qo'shadi
- Doim qo'shadi
- Doim olib tashlaydi
- Elementni o'chiradi

? document.documentElement.dataset.theme nimani o'zgartiradi?
+ html tegidagi data-theme atributini
- body rangini
- Sahifa tilini
- Hech narsani

? Tungi rejim nega bitta qator JS bilan ishlaydi?
+ Ranglar 8-darsda CSS o'zgaruvchilariga olingan
- Brauzer o'zi qiladi
- Tasodif
- Ishlamaydi

? event.preventDefault() formada nima qiladi?
+ Sahifa qayta yuklanishini to'xtatadi
- Formani o'chiradi
- Formani yuboradi
- Hech narsa

? form.elements.name.value nima qaytaradi?
+ name maydoniga yozilgan matnni
- Maydon nomini
- Formani
- Xato

? .trim() nima qiladi?
+ Boshidagi va oxiridagi bo'shliqlarni olib tashlaydi
- Matnni o'chiradi
- Katta harf qiladi
- Hech narsa

? form.reset() nima qiladi?
+ Maydonlarni tozalaydi
- Formani yuboradi
- Sahifani yangilaydi
- Formani o'chiradi

? role="status" nima uchun?
+ Ekran o'quvchi yangi xabarni o'qib beradi
- Rang uchun
- Tezlik uchun
- Shart emas
""",
    "WB11": """
? JS massivi qanday yoziladi?
+ [ ... ] kvadrat qavsda
- ( ... )
- { ... }
- < ... >

? { title: "QuizBot" } nima?
+ Obyekt — Python lug'atiga o'xshash
- Massiv
- Funksiya
- Satr

? projects.filter(...) nima qaytaradi?
+ Shartga mos elementlardan yangi massiv
- Bitta element
- Son
- Hech narsa

? map(...) nima qiladi?
+ Har elementdan yangi qiymat yasaydi
- Elementlarni o'chiradi
- Saralaydi
- Hech narsa

? .join("") nima qiladi?
+ Massiv elementlarini bitta satrga birlashtiradi
- Massivni bo'ladi
- Massivni o'chiradi
- Hech narsa

? innerHTML nima qiladi?
+ Element ichini yangi HTML bilan almashtiradi
- Faqat matn qo'yadi
- Elementni o'chiradi
- Hech narsa

? btn.dataset.filter nimani oladi?
+ Tugmadagi data-filter atribut qiymatini
- Tugma matnini
- Tugma rangini
- Xato

? localStorage nima?
+ Brauzerdagi doimiy kichik ombor — sahifa yangilansa ham qoladi
- Server bazasi
- Cookie
- Fayl

? localStorage.getItem("theme") || "light" nima qiladi?
+ Saqlangan qiymat bo'lmasa "light" ni oladi
- Doim "light"
- Xato
- Qiymatni o'chiradi

? querySelectorAll nima qaytaradi?
+ Hamma mos elementlar ro'yxatini
- Faqat birinchisini
- Sonni
- Hech narsa
""",
    "WB12": """
? GitHub Pages nima?
+ GitHub'ning bepul statik sayt hostingi
- Kod muharriri
- Baza
- Telegram bot

? Shaxsiy sayt repozitoriysi qanday nomlanadi?
+ username.github.io
- website
- index
- pages

? Pages qayerda yoqiladi?
+ Settings → Pages
- Issues
- Actions
- Code

? index.html qayerda bo'lishi kerak?
+ Repo ildizida
- images papkasida
- Istalgan joyda
- Shart emas

? meta description nima uchun?
+ Qidiruv natijasida sahifa ostidagi matn
- Tab nomi
- Rasm
- Shart emas

? Favicon nima?
+ Brauzer tabidagi kichik belgi
- Katta rasm
- Shrift
- Havola

? Saytni yangilash uchun nima qilinadi?
+ git push — sayt avtomatik yangilanadi
- Repo o'chiriladi
- Serverga qo'lda yuklanadi
- Iloji yo'q

? Lighthouse nima tekshiradi?
+ Tezlik, qulaylik (accessibility) va SEO
- Faqat kod uzunligi
- Faqat rang
- Hech narsa

? Nega Django sayti GitHub Pages'da ishlamaydi?
+ Pages faqat statik fayllarni beradi, Python ishga tushmaydi
- Django pullik
- GitHub taqiqlagan
- Ishlaydi

? 10-oyda nima boshlanadi?
+ Django: EduCenter sayti
- Yangi bot
- Scratch
- Python asoslari
""",
}
