"""Starter kursi mavzulari bo'yicha test savollari (har bir mavzuga 12 ta).

Format — mavzu testi formasidagi bilan bir xil:
"?" — savol (keyingi qatorlar savol davomi yoki kod), "+" — to'g'ri javob, "-" — noto'g'ri javob.
Kalit — ``starter.py`` dagi mavzu kaliti.
"""

QUIZZES = {
    "ST01": """
? 10 barmoqli yozishda ko'rsatkich barmoqlar "uy qatori"da qaysi tugmalarda turadi?
+ F va J
- A va ;
- D va K
- G va H

? Nima uchun F va J tugmalarida kichik bo'rtiq bor?
+ Klaviaturaga qaramasdan barmoqlarni uy qatoriga qo'yish uchun
- Bu tugmalar tez ishdan chiqmasligi uchun
- Ular eng ko'p bosiladigan tugmalar bo'lgani uchun
- Bu faqat bezak

? Monkeytype'dagi WPM nimani bildiradi?
+ Bir daqiqada yozilgan so'zlar soni
- Xatolar foizi
- Bir soniyada bosilgan tugmalar soni
- Testning davomiyligi

? Accuracy (aniqlik) ko'rsatkichi nimani o'lchaydi?
+ To'g'ri bosilgan belgilar ulushini (foizda)
- Yozish tezligini
- Klaviatura turini
- Test necha marta takrorlanganini

? Chap qo'l barmoqlari uy qatorida qaysi tugmalarda turadi?
+ A S D F
- J K L ;
- Q W E R
- Z X C V

? Monkeytype'dagi "time" rejimi nimani anglatadi?
+ Test belgilangan vaqt (masalan, 15, 30 yoki 60 soniya) davom etadi
- Test belgilangan so'zlar soni bilan tugaydi
- Faqat raqamlar yoziladi
- Vaqt hisoblanmaydi

? To'g'ri o'tirish holati qaysi?
+ Orqa tik, oyoqlar polda, bilaklar klaviaturaga deyarli parallel
- Ekranga juda yaqin egilib o'tirish
- Bir oyoqni ostiga olib, yonboshlab o'tirish
- Bilaklarni stol chetiga qattiq tirab o'tirish

? Probel (Space) tugmasini qaysi barmoq bilan bosish to'g'ri?
+ Bosh barmoq bilan
- Ko'rsatkich barmoq bilan
- Jimjiloq bilan
- O'rta barmoq bilan

? Tez yozishni o'rganishda nimaga birinchi navbatda e'tibor berish kerak?
+ Aniqlikka — tezlik keyin o'zi oshadi
- Faqat tezlikka, xatolar muhim emas
- Klaviaturaga qarab yozishga
- Faqat bitta qo'l bilan yozishga

? Darsda aniqlik bo'yicha qanday maqsad qo'yilgan edi?
+ Kamida 90–95%
- Kamida 50%
- Aniqlik muhim emas
- Faqat 100%

? Katta harf yozish uchun Shift tugmasini qanday bosish to'g'ri?
+ Harfni bosayotgan qo'lning qarama-qarshi qo'lidagi jimjiloq bilan
- Har doim chap qo'l bosh barmog'i bilan
- Harfni bosayotgan barmoqning o'zi bilan
- Caps Lock'ni har safar yoqib-o'chirish bilan

? Haftasiga +5 WPM kabi maqsad qo'yishning foydasi nimada?
+ O'sishni o'lchab, muntazam mashq qilishga undaydi
- Testni tezroq tugatishga yordam beradi
- Aniqlik avtomatik 100% bo'ladi
- Hech qanday foydasi yo'q
""",
    "ST02": """
? Gmail'da yuborilgan xatlar qaysi bo'limda saqlanadi?
+ Sent (Yuborilganlar)
- Inbox (Kiruvchi)
- Drafts (Qoralamalar)
- Spam

? Drafts (Qoralamalar) bo'limida nima bo'ladi?
+ Yozilgan, lekin hali yuborilmagan xatlar
- O'chirilgan xatlar
- Shubhali xatlar
- Yulduzcha qo'yilgan xatlar

? To'g'ri xatning tuzilmasi qaysi javobda berilgan?
+ Mavzu (Subject), salomlashish, asosiy matn, imzo
- Faqat asosiy matn
- Faqat ilova qilingan fayl
- Imzo va mavzu, matn shart emas

? Cc maydoniga yozilgan qabul qiluvchi haqida qaysi gap to'g'ri?
+ Xat nusxasini oladi va boshqa qabul qiluvchilar uni ko'radi
- Uni boshqa qabul qiluvchilar ko'rmaydi
- Xat unga yetib bormaydi
- U faqat javob yoza oladi, o'qiy olmaydi

? Bcc maydonining asosiy xususiyati nima?
+ Bu manzillar boshqa qabul qiluvchilarga ko'rinmaydi
- Xat shu manzilga ikki marta boradi
- Xat avtomatik spam'ga tushadi
- Faqat bitta manzil yozish mumkin

? "Reply" va "Reply all" farqi nima?
+ Reply — faqat yuboruvchiga, Reply all — xatdagi barcha qabul qiluvchilarga javob
- Reply all — faqat yuboruvchiga javob beradi
- Ikkalasi bir xil ishlaydi
- Reply all xatni o'chiradi

? Olingan xatni boshqa odamga yuborish uchun qaysi tugma ishlatiladi?
+ Forward
- Reply
- Archive
- Snooze

? Gmail'da label (yorliq) nima uchun kerak?
+ Xatlarni mavzu bo'yicha guruhlab, tartibda saqlash uchun
- Xatni shifrlash uchun
- Xatni avtomatik o'chirish uchun
- Xatni kechiktirib yuborish uchun

? Filtr yaratishning foydasi nima?
+ Shartga mos kelgan xatlar avtomatik label oladi yoki kerakli joyga o'tadi
- Xat matnidagi xatolar tuzatiladi
- Barcha xatlar bir marta o'chiriladi
- Xatlar faqat kechasi keladi

? Xatga rasm yoki hujjat qo'shish uchun qaysi belgi bosiladi?
+ Qisqich (📎, Attach files)
- Yulduzcha
- Axlat qutisi
- Soat belgisi

? Qaysi belgi xat fishing (firibgarlik) bo'lishi mumkinligini ko'rsatadi?
+ Shoshiltiradi va parol yoki karta raqamini so'raydi
- Tanish odamdan, kutilgan mavzuda kelgan
- Imzo va aniq mavzusi bor
- Ilovasiz oddiy salomlashish xati

? Ustozga uy vazifasi yuborishda qaysi mavzu (Subject) eng to'g'ri?
+ Uy vazifasi — Ism Familiya
- salom
- (mavzusiz)
- !!!!!!
""",
    "ST03": """
? Google Docs'da hujjat qanday saqlanadi?
+ Har bir o'zgarishdan keyin avtomatik saqlanadi
- Faqat Ctrl+S bosilganda
- Faqat hujjat yopilganda
- Saqlanmaydi, har safar yuklab olish kerak

? Hujjatda sarlavhalarni qanday belgilash to'g'ri?
+ Heading 1 / Heading 2 uslublari bilan
- Matnni faqat kattalashtirib
- Hamma harflarni katta harf bilan yozib
- Sarlavha oxiriga ko'p undov qo'yib

? Heading uslublaridan foydalanishning qo'shimcha foydasi nima?
+ Hujjat tuzilmasi (outline) va mundarija avtomatik hosil bo'ladi
- Hujjat hajmi kamayadi
- Matn avtomatik tarjima qilinadi
- Rasm sifati yaxshilanadi

? Faylni o'qiy oladigan, lekin o'zgartira olmaydigan huquq qaysi?
+ Viewer
- Editor
- Owner
- Commenter

? Commenter huquqi nimaga ruxsat beradi?
+ Matnni o'zgartirmasdan izoh va taklif qoldirishga
- Hujjatni o'chirishga
- Hujjatni to'liq tahrirlashga
- Boshqalarni hujjatdan chiqarib yuborishga

? Hujjatga jadval qo'shish qaysi menyu orqali bajariladi?
+ Insert → Table
- File → Table
- View → Table
- Help → Table

? Taklif (Suggesting) rejimining vazifasi nima?
+ O'zgarishlar taklif sifatida ko'rinadi, egasi qabul yoki rad etadi
- Hujjatni boshqa tilga o'giradi
- Hujjatni faqat o'qish uchun yopadi
- Imlo xatolarini avtomatik tuzatadi

? Matnga havola (link) qo'shish uchun qaysi tugmalar birikmasi ishlatiladi?
+ Ctrl + K
- Ctrl + L
- Ctrl + H
- Ctrl + P

? Matnni sahifa o'rtasiga tekislash qaysi amal?
+ Center align (Ctrl + Shift + E)
- Bold (Ctrl + B)
- Underline (Ctrl + U)
- Undo (Ctrl + Z)

? Ro'yxatning qaysi turi raqamli bo'ladi?
+ Numbered list
- Bulleted list
- Checklist
- Table

? Hujjatni ustozga faqat izoh qoldirish huquqi bilan ulashish uchun nima tanlanadi?
+ Share → email → Commenter
- Share → Editor
- File → Download → PDF
- File → Make a copy

? Hujjatga qo'yilgan izohga (comment) qanday javob beriladi?
+ Izoh oynasida Reply orqali yoki uni Resolve qilib
- Hujjatni o'chirib qayta yaratish bilan
- Faqat email orqali
- Izohga javob berib bo'lmaydi
""",
    "ST04": """
? Yaxshi slaydning asosiy qoidasi qaysi?
+ 1 slayd — 1 fikr, kam matn, katta shrift
- Bir slaydga iloji boricha ko'p matn joylash
- Har bir slaydda 5 xil shrift ishlatish
- Matnni kichik shriftda yozish

? Google Slides'da tayyor ranglar va shriftlar to'plami nima deb ataladi?
+ Theme (mavzu)
- Layout
- Speaker notes
- Transition

? Layout (maket) nimani belgilaydi?
+ Slayddagi sarlavha, matn va rasm joylarining joylashuvini
- Slaydlar orasidagi o'tish effektini
- Prezentatsiya nomini
- Faylni kim ko'ra olishini

? Speaker notes nima uchun kerak?
+ Ma'ruzachi uchun eslatmalar — tomoshabin ularni ko'rmaydi
- Slayd fonini o'zgartirish uchun
- Tomoshabinlar savol yozishi uchun
- Slaydlarni avtomatik almashtirish uchun

? Transition (o'tish effekti) nima?
+ Bir slayddan keyingisiga o'tishdagi effekt
- Slayd ichidagi bitta obyektning harakati
- Slayd fonining rangi
- Shrift o'lchami

? Animatsiya va effektlardan qanday foydalanish tavsiya etiladi?
+ Me'yorida — diqqatni chalg'itmaydigan darajada
- Har bir so'zga alohida animatsiya qo'yib
- Umuman foydalanmaslik shart
- Faqat eng shovqinli effektlarni tanlab

? Prezentatsiyani to'liq ekranda ko'rsatish qaysi tugma bilan boshlanadi?
+ Slideshow (Present)
- Share
- Insert
- Format

? Darsdagi "Mening shahrim" prezentatsiyasining to'g'ri tuzilmasi qaysi?
+ Titul slayd, 3 ta asosiy slayd, yakuniy slayd
- Faqat bitta slaydda hamma ma'lumot
- 20 ta slayd, faqat matn
- Faqat rasmlar, sarlavhasiz

? Slayddagi matn yaxshi o'qilishi uchun nima muhim?
+ Fon va matn rangi orasida kuchli kontrast
- Ochiq sariq fonga oq matn
- Matnni rasm ustiga kontrastsiz yozish
- Juda ingichka va mayda shrift

? Slaydga rasm qo'shish qaysi menyu orqali bajariladi?
+ Insert → Image
- File → Image
- Slide → Image
- Tools → Image

? Yangi slayd qo'shishning tez usuli qaysi?
+ Ctrl + M
- Ctrl + N
- Ctrl + S
- Ctrl + D

? 1 daqiqalik taqdimotda eng to'g'ri yo'l qaysi?
+ Slayddagi matnni o'qimasdan, asosiy fikrni o'z so'zlaringiz bilan aytish
- Hamma matnni slayddan so'zma-so'z o'qish
- Tomoshabinga orqa o'girib gapirish
- Barcha slaydlarni tez-tez o'tkazib yuborish
""",
    "ST05": """
? Google Drive nima?
+ Fayllarni saqlash va ulashish uchun bulutli xotira
- Matn muharriri
- Video muloqot dasturi
- Antivirus

? Bepul Google hisobida qancha bulutli xotira beriladi?
+ 15 GB
- 1 GB
- 100 GB
- Cheksiz

? "Shared with me" bo'limida qanday fayllar ko'rinadi?
+ Boshqalar sizga ulashgan fayllar
- Siz o'chirgan fayllar
- Faqat rasmlar
- Kompyuterdagi barcha fayllar

? Faylni o'zgartirish huquqini beradigan rol qaysi?
+ Editor
- Viewer
- Commenter
- Guest

? "Anyone with the link" sozlamasi nimani bildiradi?
+ Havolaga ega bo'lgan har kim faylni ochishi mumkin
- Faqat fayl egasi ochishi mumkin
- Fayl internetdan o'chiriladi
- Faqat bir marta ochish mumkin

? Fayllarni tartibli saqlashning eng yaxshi usuli qaysi?
+ Mazmunli nomlangan papkalar va kichik papkalar yaratish
- Hammasini bitta joyda nomsiz saqlash
- Har bir faylni alohida hisobga yuklash
- Fayllarni "1", "2", "3" deb nomlash

? Version history (versiyalar tarixi) nima uchun kerak?
+ Faylning oldingi holatini ko'rish va tiklash uchun
- Faylni boshqa formatga o'tkazish uchun
- Fayl hajmini kichraytirish uchun
- Faylni parol bilan yopish uchun

? O'chirilgan fayl Drive'da avval qayerga tushadi?
+ Trash (Savat) — u yerdan tiklash mumkin
- Darhol butunlay yo'qoladi
- Shared with me bo'limiga
- Starred bo'limiga

? Bir nechta o'quvchi bitta Slides faylida bir vaqtda ishlay oladimi?
+ Ha, Editor huquqi bo'lsa, o'zgarishlar real vaqtda ko'rinadi
- Yo'q, faqat navbat bilan
- Faqat fayl egasi ishlay oladi
- Faqat fayl yuklab olinsa

? Kompyuterdagi faylni Drive'ga qanday yuklash mumkin?
+ New → File upload yoki faylni brauzer oynasiga sudrab tashlash
- Faqat email orqali
- Faqat telefon orqali
- Faylni Drive'ga yuklab bo'lmaydi

? Darsda yaratilgan papka tuzilmasi qaysi edi?
+ "Starter_Ism" papkasi va ichida Docs, Slides, Rasmlar kichik papkalari
- Hamma fayllar "Yangi papka" ichida
- Har bir fayl alohida hisobda
- Faqat bitta "Rasmlar" papkasi

? Faylni ulashishning ikki usuli qaysi?
+ Email orqali odam qo'shish va havola (link) yuborish
- Faqat USB fleshka orqali
- Faqat faylni chop etib berish
- Faqat skrinshot yuborish
""",
    "ST06": """
? A1 nimani bildiradi?
+ A ustun va 1-qator kesishgan yacheyka manzili
- 1-varaq nomi
- Formula natijasi
- Jadval sarlavhasi

? Sheets'da formula qaysi belgi bilan boshlanadi?
+ =
- +
- #
- @

? =SUM(B2:B10) formulasi nimani hisoblaydi?
+ B2 dan B10 gacha bo'lgan qiymatlar yig'indisini
- B2 va B10 yacheykalarining o'rtachasini
- B ustunidagi yacheykalar sonini
- Faqat B2 va B10 ning yig'indisini

? O'rtacha qiymatni qaysi funksiya hisoblaydi?
+ AVERAGE
- SUM
- COUNT
- MAX

? =COUNT(C2:C20) formulasi nimani qaytaradi?
+ Oraliqdagi sonli qiymatlar sonini
- Oraliqdagi sonlar yig'indisini
- Eng katta qiymatni
- Bo'sh yacheykalar sonini

? Eng kichik qiymatni topish uchun qaysi funksiya ishlatiladi?
+ MIN
- MAX
- LOW
- AVERAGE

? B2:B10 yozuvidagi ikki nuqta (:) nimani bildiradi?
+ B2 dan B10 gacha bo'lgan oraliqni
- B2 ni B10 ga bo'lishni
- Faqat ikkita yacheykani
- Izohni

? Formulani qo'shni qatorlarga tez nusxalash qanday bajariladi?
+ Yacheyka burchagidagi kichik kvadratchani pastga cho'zib
- Har bir qatorga formulani qo'lda qayta yozib
- Faylni qayta ochib
- Formula nusxalanmaydi

? =A1+A2 formulasi pastki qatorga cho'zilsa, keyingi yacheykada qanday formula bo'ladi?
+ =A2+A3
- =A1+A2
- =B1+B2
- =A1+A3

? Ustunni kattadan kichikka tartiblash qanday ataladi?
+ Sort Z → A (kamayish bo'yicha saralash)
- Sort A → Z
- Filter
- Merge

? Filtr (Filter) nima qiladi?
+ Shartga mos qatorlarni ko'rsatib, qolganlarini vaqtincha yashiradi
- Qatorlarni butunlay o'chiradi
- Yacheykalarni bo'yaydi
- Formulalarni hisoblaydi

? 0.85 sonini 85% ko'rinishida chiqarish uchun nima qilinadi?
+ Yacheyka formati "Percent" (foiz) qilib o'zgartiriladi
- Songa qo'lda "%" belgisi yoziladi
- Son 100 ga ko'paytirilib, matnga aylantiriladi
- Yacheyka kengaytiriladi
""",
    "ST07": """
? Vaqt bo'yicha o'zgarishni (masalan, oylar bo'yicha baho) ko'rsatishga qaysi diagramma eng mos?
+ Chiziqli (line) diagramma
- Doiraviy (pie) diagramma
- Faqat jadval
- Diagramma kerak emas

? Butunning qismlarini (foiz ulushlarni) ko'rsatishga qaysi diagramma mos?
+ Doiraviy (pie) diagramma
- Chiziqli (line) diagramma
- Ustunli (column) diagramma
- Nuqtali diagramma

? Bir nechta o'quvchi ballarini solishtirishga qaysi diagramma eng qulay?
+ Ustunli (column) diagramma
- Doiraviy diagramma
- Matn bloki
- Hech qaysi

? Diagramma qanday qo'shiladi?
+ Ma'lumotni belgilab, Insert → Chart tanlanadi
- File → Chart
- Data → Sort
- Faqat Slides'da qo'shish mumkin

? Diagrammadagi legenda nimani ko'rsatadi?
+ Qaysi rang qaysi ma'lumot qatoriga tegishli ekanini
- Diagramma sarlavhasini
- Fayl nomini
- Yacheyka manzilini

? Shartli formatlash (Conditional formatting) nima qiladi?
+ Shartga mos yacheykalarni avtomatik bo'yaydi yoki formatlaydi
- Formulalarni o'chiradi
- Jadvalni saralaydi
- Diagramma yaratadi

? 60 dan past baholarni qizil qilish uchun qaysi qoida tanlanadi?
+ Format cells if → Less than → 60
- Greater than → 60
- Is empty
- Text contains → 60

? =IF(B2>=60; "O'tdi"; "Qayta topshiradi") formulasi B2 = 75 bo'lsa nima qaytaradi?
+ O'tdi
- Qayta topshiradi
- 75
- Xato

? =IF(B2>=60; "O'tdi"; "Qayta topshiradi") formulasi B2 = 59 bo'lsa nima qaytaradi?
+ Qayta topshiradi
- O'tdi
- 59
- Bo'sh qiymat

? IF funksiyasining uchta qismi qaysi?
+ Shart, rost bo'lsa qiymat, yolg'on bo'lsa qiymat
- Yig'indi, o'rtacha, son
- Ustun, qator, varaq
- Sarlavha, legenda, o'q

? Sheets diagrammasini Slides'ga qo'yishning to'g'ri usuli qaysi?
+ Slides'da Insert → Chart → From Sheets (bog'langan diagramma)
- Diagrammani qo'lda qayta chizish
- Faqat jadvalni nusxalash
- Buning iloji yo'q

? Diagramma sarlavhasi va o'q nomlarini qayerda o'zgartirish mumkin?
+ Chart editor → Customize bo'limida
- File → Settings
- Data → Filter
- View → Zoom
""",
    "ST08": """
? Jamoa loyihasida barcha fayllarni bir joyda saqlash va ulashish uchun qaysi vosita ishlatildi?
+ Google Drive (umumiy jamoa papkasi)
- Gmail qoralamalari
- Kompyuter ish stoli
- Google Calendar

? Sayohat rejasi (manzil, kun tartibi, qoidalar) qaysi vositada yozildi?
+ Google Docs
- Google Sheets
- Google Slides
- Gmail

? Xarajatlar smetasini hisoblash uchun qaysi vosita eng mos?
+ Google Sheets
- Google Docs
- Google Slides
- Google Meet

? Smetadagi umumiy xarajat qaysi formula bilan topiladi?
+ =SUM(...)
- =COUNT(...)
- =MIN(...)
- =IF(...)

? Bir kishiga to'g'ri keladigan o'rtacha xarajat qaysi funksiya bilan hisoblanadi?
+ AVERAGE
- SUM
- MAX
- COUNT

? Taqdimotga Sheets diagrammasini qo'shishning to'g'ri usuli qaysi?
+ Slides'da Insert → Chart → From Sheets
- Diagrammani qog'ozga chizib, rasmga olish
- Faqat raqamlarni matn qilib yozish
- Diagrammani qo'shib bo'lmaydi

? Tayyor loyiha havolalari ustozga qanday yuborildi?
+ Gmail orqali, mavzu va imzosi bor rasmiy xat bilan
- Faqat og'zaki aytib
- Telefon SMS orqali
- Hech qanday yuborilmadi

? Jamoa a'zolari bitta faylni birga tahrirlashi uchun qaysi huquq kerak?
+ Editor
- Viewer
- Commenter
- Huquq shart emas

? Ustoz loyihani ko'rib izoh qoldirishi, lekin o'zgartirmasligi uchun qaysi huquq yetarli?
+ Commenter
- Editor
- Owner
- Huquq berilmaydi

? Taqdimot uchun tavsiya etilgan slaydlar soni qancha edi?
+ 5–6 ta
- 1 ta
- 30 ta
- Cheklov yo'q

? Jamoaviy ishda kim nima o'zgartirganini qayerdan ko'rish mumkin?
+ Version history (versiyalar tarixi)
- Spam papkasi
- Calendar
- Trash

? Nima uchun barcha loyiha fayllari bitta jamoa papkasida saqlanadi?
+ Hamma kerakli faylni oson topadi va ulashish bir joydan boshqariladi
- Fayllar avtomatik chiroyli bo'lishi uchun
- Shunda internet kerak bo'lmaydi
- Bu faqat ustozga kerak
""",
    "ST09": """
? Canva'da o'z rasm yoki logongizni qayerdan qo'shasiz?
+ Uploads (Yuklamalar) bo'limidan
- Templates bo'limidan
- Text bo'limidan
- Share tugmasidan

? Dizayndagi kontrast nima?
+ Elementlar orasidagi aniq farq (masalan, to'q fon va och matn)
- Bir xil ranglarni ishlatish
- Hamma narsani bir xil o'lchamda qilish
- Rasmni xiralashtirish

? Tekislash (alignment) nima uchun muhim?
+ Elementlar bir chiziqda turib, dizayn tartibli ko'rinadi
- Dizayn hajmi kamayadi
- Ranglar yorqinroq bo'ladi
- Matn avtomatik tarjima qilinadi

? Darsdagi shrift qoidasi bo'yicha bitta dizaynda nechta shrift ishlatish tavsiya etiladi?
+ 2 ta (sarlavha va matn uchun)
- 5–6 ta
- Iloji boricha ko'p
- Har bir so'z uchun alohida

? Bo'sh joy (white space) haqida qaysi gap to'g'ri?
+ U dizaynga "nafas" beradi va o'qishni osonlashtiradi
- Bo'sh joyni har doim to'ldirish kerak
- U faqat xato natijasida paydo bo'ladi
- U faqat oq rangda bo'ladi

? Darsda rang palitrasi uchun nechta asosiy rang tanlash tavsiya etildi?
+ 3 ta
- 1 ta
- 10 ta
- Cheklov yo'q

? Darsdagi vizitkaning o'lchami qancha edi?
+ 90 × 50 mm
- 1080 × 1080 px
- A4
- 375 × 812 px

? Chop etish uchun eng mos eksport formati qaysi?
+ PDF (Print)
- GIF
- MP4
- PNG kichik o'lchamda

? Vizitkada odatda nimalar bo'ladi?
+ Ism, lavozim yoki kasb, aloqa ma'lumotlari, logo
- Uzun tarjimai hol
- Faqat rasm
- Barcha ijtimoiy tarmoq postlari

? Canva'dagi tayyor shablon (template) nima?
+ Tayyor dizayn — uni o'zingizga moslab o'zgartirasiz
- Faqat bo'sh oq varaq
- Shrift turi
- Rasm formati

? Nima uchun ikki tomonli vizitkaning har ikki tomoni bir xil uslubda bo'lishi kerak?
+ Ular yagona dizayn sifatida qabul qilinishi uchun
- Shunda chop etish arzonlashadi
- Bu Canva talabi
- Muhim emas

? Shaffof fonli logo uchun qaysi format mos?
+ PNG
- JPG
- PDF
- MP4
""",
    "ST10": """
? Instagram post uchun standart kvadrat o'lcham qaysi?
+ 1080 × 1080 px
- 1080 × 1920 px
- 1920 × 1080 px
- 90 × 50 mm

? Instagram story uchun o'lcham qaysi?
+ 1080 × 1920 px
- 1080 × 1080 px
- 1280 × 720 px
- A4

? "Call to action" (chaqiriq) nima?
+ Ko'ruvchini harakatga undovchi matn: "Hoziroq yoziling!"
- Post sarlavhasining shrifti
- Fon rasmi
- Logotip

? Sarlavha ierarxiyasi nimani anglatadi?
+ Eng muhim matn eng katta va ko'zga tashlanadigan bo'ladi
- Barcha matn bir xil o'lchamda bo'ladi
- Sarlavha har doim pastda bo'ladi
- Matn faqat bitta rangda bo'ladi

? Brend to'plami (Brand kit) nimani o'z ichiga oladi?
+ Logo, brend ranglari va shriftlari
- Faqat rasmlar arxivi
- Mijozlar ro'yxati
- Narxlar jadvali

? Post, story va slaydlar bir xil uslubda bo'lishining foydasi nima?
+ Brend taniqli va professional ko'rinadi
- Fayllar hajmi kichrayadi
- Dizayn tezroq chop etiladi
- Hech qanday foydasi yo'q

? Ijtimoiy tarmoq postidagi matn qanday bo'lishi kerak?
+ Qisqa va aniq
- Iloji boricha uzun
- Faqat kichik shriftda
- Faqat inglizcha

? Canva Presentations'da slaydlar orasida izchillik qanday saqlanadi?
+ Bir xil shrift, ranglar va joylashuvni takrorlab
- Har bir slaydga boshqa shablon tanlab
- Har slaydda yangi ranglar ishlatib
- Faqat matnli slaydlar qilib

? Postni telefonda ko'rib chiqishning sababi nima?
+ Ko'pchilik ijtimoiy tarmoqni telefonda ko'radi — matn o'qilishi kerak
- Kompyuterda post ochilmaydi
- Canva faqat telefonda ishlaydi
- Bu shart emas

? Story dizaynida muhim matnni ekranning eng yuqori va eng pastki chetiga qo'ymaslik kerak, chunki…
+ U yerda profil nomi va javob maydoni matnni yopib qo'yishi mumkin
- U yerda rang o'zgarib ketadi
- Story faqat o'rtasi ko'rinadi
- Canva bunga ruxsat bermaydi

? Jamoada dizaynni ko'rib chiqishda (feedback) qanday fikr bildirish to'g'ri?
+ Aniq va hurmat bilan: nima yaxshi va nimani yaxshilash mumkin
- Faqat "yoqmadi" deyish
- Hech narsa demaslik
- Dizaynni o'zingiz o'chirib tashlash

? Ko'proq sahifali taqdimotni yuborish uchun qaysi format eng qulay?
+ PDF
- GIF
- MP3
- TXT
""",
    "ST11": """
? Figma'da Frame nima?
+ Ekran yoki maket chegarasi — ichiga elementlar joylanadi
- Rang palitrasi
- Shrift turi
- Eksport formati

? Darsda telefon ekrani uchun qaysi Frame o'lchami ishlatildi?
+ 375 × 812
- 1920 × 1080
- 1080 × 1080
- 90 × 50

? Layers paneli nimani ko'rsatadi?
+ Sahifadagi barcha qatlamlar (elementlar) va ularning tartibini
- Faqat ranglarni
- Fayl tarixini
- Prototip bog'lanishlarini

? To'rtburchak chizish asbobining tez tugmasi qaysi?
+ R (Rectangle)
- T
- O
- P

? Matn qo'shish asbobining tez tugmasi qaysi?
+ T
- R
- L
- F

? Ellipse (aylana) asbobining tez tugmasi qaysi?
+ O
- E
- C
- A

? Auto layout nima qiladi?
+ Ichidagi elementlarni avtomatik joylashtiradi va matnga qarab o'lchamni moslaydi
- Ranglarni avtomatik tanlaydi
- Faylni avtomatik saqlaydi
- Prototip yaratadi

? Auto layout qaysi tugmalar birikmasi bilan qo'shiladi?
+ Shift + A
- Ctrl + A
- Shift + R
- Alt + L

? Tugma burchaklarini yumaloq qilish uchun qaysi xususiyat o'zgartiriladi?
+ Corner radius
- Opacity
- Stroke
- Blur

? Elementga soya berish uchun qaysi effekt ishlatiladi?
+ Drop shadow
- Layer blur
- Inner glow
- Mask

? Nima uchun qatlamlarni (layer) nomlash kerak?
+ Katta maketda kerakli elementni tez topish va tartibni saqlash uchun
- Shunda dizayn chiroyliroq ko'rinadi
- Figma nomlanmagan qatlamni o'chiradi
- Eksport faqat nomlangan qatlam bilan ishlaydi

? Darsdagi Login ekranida qaysi elementlar bo'lishi kerak edi?
+ Logo, 2 ta input, "Kirish" tugmasi va "Parolni unutdingizmi?" havolasi
- Faqat rasm
- Faqat matn
- Video va musiqa
""",
    "ST12": """
? Figma'da Component nima?
+ Qayta ishlatiladigan asosiy element (masalan, tugma)
- Bir martalik shakl
- Rang palitrasi
- Eksport formati

? Instance nima?
+ Komponentning nusxasi — asosiy komponent o'zgarsa, u ham yangilanadi
- Komponentning mustaqil, bog'lanmagan nusxasi
- Yangi sahifa
- Faylning eski versiyasi

? Asosiy (main) komponentga o'zgartirish kiritilsa nima bo'ladi?
+ Barcha instance'lar avtomatik yangilanadi
- Faqat bitta instance o'zgaradi
- Instance'lar o'chib ketadi
- Hech narsa o'zgarmaydi

? Variants nima uchun kerak?
+ Bitta komponentning holatlari (primary/secondary, hover) ni bir joyda saqlash uchun
- Fayl nusxasini yaratish uchun
- Rasmni kesish uchun
- Sahifani eksport qilish uchun

? Komponent yaratishning tez tugmalari qaysi?
+ Ctrl + Alt + K
- Ctrl + K
- Shift + C
- Alt + C

? Color styles (rang uslublari) ning foydasi nima?
+ Rangni bir joyda o'zgartirsangiz, u ishlatilgan hamma joyda yangilanadi
- Rasmlarni siqadi
- Prototipni tezlashtiradi
- Shriftni o'zgartiradi

? Text styles nimani saqlaydi?
+ Shrift, o'lcham, qalinlik va qator oralig'ini
- Faqat matn rangini
- Faqat rasm o'lchamini
- Prototip bog'lanishlarini

? Darsdagi 3 ekranli ilova qaysi ekranlardan iborat edi?
+ Bosh sahifa, Ro'yxat, Profil
- Login, Xato, Yuklash
- Faqat bitta ekran
- Sozlamalar, To'lov, Chat

? Pastki menyu (bottom navigation) nima uchun komponent qilinadi?
+ U barcha ekranlarda bir xil bo'lishi va bir joydan o'zgartirilishi uchun
- Komponent bo'lmasa ko'rinmaydi
- Bu fayl hajmini oshiradi
- Faqat eksport uchun

? Instance'dagi matnni o'zgartirsa bo'ladimi?
+ Ha, matn va ba'zi xususiyatlar override qilinadi, bog'lanish saqlanadi
- Yo'q, umuman o'zgartirib bo'lmaydi
- Faqat komponentni o'chirib
- Faqat boshqa faylda

? Dizayndagi izchillik (consistency) nimani bildiradi?
+ Bir xil elementlar barcha ekranlarda bir xil ko'rinadi va ishlaydi
- Har bir ekran butunlay boshqacha bo'ladi
- Faqat bitta rang ishlatiladi
- Ekranlar soni ko'p bo'ladi

? Komponentlardan foydalanishning asosiy afzalligi nima?
+ Vaqt tejaladi va dizayn bir xil bo'ladi
- Fayl ochilmaydi
- Ranglar avtomatik tanlanadi
- Prototip kerak bo'lmaydi
""",
    "ST13": """
? Figma'da ekranlarni bog'lash qaysi rejimda bajariladi?
+ Prototype
- Design
- Inspect
- Dev Mode

? Tugma bosilganda boshqa ekranga o'tish uchun qaysi sozlama tanlanadi?
+ On click → Navigate to
- On drag → Scroll to
- While hovering → Close
- After delay → Back

? Smart animate nima qiladi?
+ Ikki ekrandagi bir xil nomli qatlamlarni silliq harakatlantiradi
- Ekranni darhol almashtiradi
- Rasmni siqadi
- Faylni eksport qiladi

? Instant animatsiyasi qanday ishlaydi?
+ Ekran effektsiz, darhol almashadi
- Ekran asta-sekin xiralashib almashadi
- Elementlar silliq siljiydi
- Ekran aylanadi

? Dissolve animatsiyasi qanday ishlaydi?
+ Ekranlar xiralashib, asta-sekin almashadi
- Ekran darhol almashadi
- Ekran yon tomondan suriladi
- Ekran kattalashadi

? Prototipni ko'rish uchun qaysi tugma bosiladi?
+ Present (▶ Play)
- Export
- Share → Delete
- Component

? Prototipni telefonda ko'rish uchun nima qilinadi?
+ Figma ilovasi orqali yoki prototip havolasini telefonda ochib
- Faylni chop etib
- Faqat kompyuterda ko'rish mumkin
- Prototipni PDF qilib

? Ikonka yoki logoni sifatini yo'qotmasdan kattalashtirish uchun qaysi format mos?
+ SVG
- JPG
- PNG @1x
- GIF

? Eksportdagi @2x nimani bildiradi?
+ Rasm ikki baravar katta piksel o'lchamida (aniq ekranlar uchun) saqlanadi
- Ikki marta eksport qilinadi
- Rasm ikki baravar kichik bo'ladi
- Ikkita fayl formatida saqlanadi

? Bir nechta ekranni bitta hujjat qilib yuborish uchun qaysi format qulay?
+ PDF
- SVG
- PNG
- MP3

? Elementni eksport qilish sozlamalari qayerda?
+ O'ng paneldagi Export bo'limida
- Layers panelida
- Prototype rejimida
- Komponentlar ro'yxatida

? Yaxshi prototipda nima bo'lishi kerak?
+ Barcha tugmalar ishlashi va foydalanuvchi har bir ekrandan orqaga qayta olishi
- Faqat birinchi ekran ishlashi
- Tugmalar bog'lanmagan bo'lishi
- Faqat animatsiyalar bo'lishi
""",
    "ST14": """
? Terminal nima?
+ Kompyuterni matnli buyruqlar orqali boshqarish oynasi
- Matn muharriri
- Rasm chizish dasturi
- Brauzer kengaytmasi

? Hozir qaysi papkada turganingizni qaysi buyruq ko'rsatadi?
+ pwd
- ls
- cd
- mkdir

? Papka ichidagi fayllar ro'yxatini qaysi buyruq chiqaradi?
+ ls (Windows'da dir)
- pwd
- rm
- echo

? Bir daraja yuqoridagi (ota) papkaga qanday o'tiladi?
+ cd ..
- cd /
- cd ~
- ls ..

? "loyiha" nomli yangi papka yaratish buyrug'i qaysi?
+ mkdir loyiha
- touch loyiha
- cd loyiha
- rm loyiha

? Bo'sh fayl yaratish uchun Linux/macOS'da qaysi buyruq ishlatiladi?
+ touch
- mkdir
- cat
- pwd

? Faylni ko'chirish yoki nomini o'zgartirish qaysi buyruq bilan bajariladi?
+ mv
- cp
- rm
- ls

? cp buyrug'i nima qiladi?
+ Fayldan nusxa oladi
- Faylni o'chiradi
- Faylni ko'chiradi
- Papka yaratadi

? rm buyrug'i bilan ishlashda nimaga ehtiyot bo'lish kerak?
+ O'chirilgan fayl odatda savatga tushmaydi — buyruqdan oldin tekshirish kerak
- rm faylni faqat yashiradi
- rm faylni nusxalaydi
- rm xavfsiz, ehtiyot shart emas

? Fayl ichidagi matnni ekranga chiqarish buyrug'i qaysi?
+ cat
- cd
- mkdir
- clear

? Fayl yoki papka nomini avtomatik to'ldirish uchun qaysi tugma bosiladi?
+ Tab
- Enter
- Esc
- Shift

? Oldin yozilgan buyruqlarni qayta chaqirish uchun qaysi tugma ishlatiladi?
+ ↑ (yuqoriga strelka)
- Tab
- Ctrl + S
- Delete
""",
    "ST15": """
? Algoritm nima?
+ Masalani yechish uchun aniq va ketma-ket qadamlar
- Kompyuterning ehtiyot qismi
- Faqat matematik formula
- Dasturlash tili

? Scratch'da sprite nima?
+ Sahnada harakatlanadigan qahramon yoki obyekt
- Sahnaning orqa foni
- Ovoz fayli
- Blok turi

? Scratch'dagi "kostyum" nima?
+ Sprite'ning tashqi ko'rinish varianti
- Sahna o'lchami
- Ovoz effekti
- O'zgaruvchi

? Dastur yashil bayroq bosilganda boshlanishi uchun qaysi bo'limdagi blok ishlatiladi?
+ Events (Hodisalar)
- Motion (Harakat)
- Looks (Ko'rinish)
- Sound (Ovoz)

? "10 qadam yur" bloki qaysi bo'limda joylashgan?
+ Motion
- Looks
- Events
- Sound

? Sprite'ga gapirtirish ("Salom! 2 soniya ayt") uchun qaysi bo'lim kerak?
+ Looks
- Motion
- Sound
- Sensing

? Sahna markazining koordinatalari qanday?
+ x: 0, y: 0
- x: 240, y: 180
- x: 100, y: 100
- x: −240, y: 0

? x qiymati ortsa, sprite qaysi tomonga siljiydi?
+ O'ngga
- Chapga
- Yuqoriga
- Pastga

? y qiymati ortsa, sprite qaysi tomonga siljiydi?
+ Yuqoriga
- Pastga
- O'ngga
- Chapga

? Sahna fonini o'zgartirish uchun qaysi blok ishlatiladi?
+ "Fonni … ga almashtir" (switch backdrop to)
- "10 qadam yur"
- "Ovozni ijro et"
- "Kostyumni almashtir"

? "Choy damlash" algoritmida birinchi qadam qaysi bo'lishi mantiqan to'g'ri?
+ Choynakka suv quyib, qaynatish
- Choyni piyolaga quyish
- Choyni ichish
- Piyolani yuvib qo'yish

? Sprite'ni 90 darajaga burish nimani anglatadi (Scratch'da)?
+ Sprite o'ng tomonga qaraydi
- Sprite chapga qaraydi
- Sprite yuqoriga qaraydi
- Sprite yo'qoladi
""",
    "ST16": """
? "repeat 10" bloki nima qiladi?
+ Ichidagi bloklarni 10 marta takrorlaydi
- Dasturni 10 soniya to'xtatadi
- 10 qadam yuradi
- 10 ta sprite yaratadi

? "forever" bloki nima qiladi?
+ Ichidagi bloklarni dastur to'xtatilmaguncha takrorlaydi
- Bloklarni bir marta bajaradi
- Dasturni darhol to'xtatadi
- O'zgaruvchi yaratadi

? "if … then" bloki qachon ishlaydi?
+ Shart rost bo'lgandagina ichidagi bloklar bajariladi
- Har doim bajariladi
- Hech qachon bajarilmaydi
- Faqat yashil bayroq bosilganda

? "if … then … else" blokining "else" qismi qachon bajariladi?
+ Shart yolg'on bo'lganda
- Shart rost bo'lganda
- Har doim
- Hech qachon

? Sprite to'siqqa tekkanini qaysi shart bilan tekshiramiz?
+ "touching … ?" (… ga tegyaptimi?)
- "key pressed?"
- "mouse down?"
- "timer"

? O'yinchini strelkalar bilan boshqarish uchun qaysi shart ishlatiladi?
+ "key … pressed?" (… tugmasi bosilganmi?)
- "touching color?"
- "answer"
- "loudness"

? Ball (score) ni saqlash uchun nima yaratiladi?
+ O'zgaruvchi (Variable)
- Yangi sprite
- Yangi fon
- Ovoz

? Yulduz yig'ilganda ballni 1 ga oshirish uchun qaysi blok kerak?
+ "change score by 1"
- "set score to 1"
- "say score"
- "repeat 1"

? O'yin boshlanishida hayotlar sonini 3 qilish uchun qaysi blok to'g'ri?
+ "set lives to 3"
- "change lives by 3"
- "repeat 3"
- "wait 3 seconds"

? Hayot 0 bo'lganda "Game Over" chiqishi uchun qaysi shart yoziladi?
+ if lives = 0 then
- if lives > 0 then
- if score = 0 then
- repeat until lives > 3

? Nega to'siqqa tegishni "forever" ichida tekshirish kerak?
+ Shart o'yin davomida doimiy tekshirilib turishi uchun
- Aks holda sprite ko'rinmaydi
- forever o'yinni tezlashtiradi
- Bu shart emas, bir marta tekshirish yetarli

? To'siqqa tekkandan keyin "wait 1 seconds" qo'yilmasa nima bo'lishi mumkin?
+ Bir tegishda hayot bir necha marta birdan kamayib ketadi
- O'yin avtomatik saqlanadi
- Ball ikki baravar oshadi
- Hech narsa o'zgarmaydi
""",
    "ST17": """
? Google Meet'da yangi uchrashuv yaratilgach, boshqalarni qanday taklif qilasiz?
+ Uchrashuv havolasini yuborib
- Faylni Drive'ga yuklab
- Faqat telefon qilib
- Taklif qilib bo'lmaydi

? Onlayn darsda gapirmayotganda mikrofon odobi qanday?
+ Mikrofonni o'chirib qo'yish
- Mikrofonni doim yoqib qo'yish
- Musiqa qo'yib qo'yish
- Mikrofonni ovozini maksimal qilish

? O'z ekraningizni boshqalarga ko'rsatish uchun qaysi funksiya ishlatiladi?
+ Present now (Ekranni ulashish)
- Chat
- Raise hand
- Captions

? Gapirish navbatini so'rash uchun Meet'da nima qilinadi?
+ "Raise hand" (qo'l ko'tarish) tugmasi bosiladi
- Mikrofon orqali baqiriladi
- Uchrashuvdan chiqiladi
- Kamera o'chiriladi

? Captions (subtitrlar) nima qiladi?
+ Gapirilgan nutqni ekranda matn qilib ko'rsatadi
- Ekranni yozib oladi
- Chatni tarjima qiladi
- Ovozni balandlatadi

? Google Calendar'da har hafta takrorlanadigan dars qanday yaratiladi?
+ Tadbir yaratib, "Does not repeat" o'rniga "Weekly on …" tanlanadi
- Har hafta yangi tadbirni qo'lda yaratiladi
- Takrorlanuvchi tadbir yaratib bo'lmaydi
- Faqat Gmail orqali

? Tadbirdan oldin eslatma olish uchun nima sozlanadi?
+ Notification (masalan, 30 daqiqa oldin)
- Rang
- Vaqt zonasi
- Tadbir nomi

? Calendar tadbiriga video uchrashuv havolasini qo'shish uchun nima bosiladi?
+ "Add Google Meet video conferencing"
- "Add attachment"
- "Change color"
- "Print"

? Tadbirga boshqa odamlarni qanday qo'shasiz?
+ "Add guests" maydoniga ularning email manzilini yozib
- Faqat Meet chatida yozib
- Ularning telefon raqamini Notes'ga yozib
- Faqat tadbirni chop etib

? Onlayn darsga kirishdan oldin nimani tekshirish kerak?
+ Internet, mikrofon va kamera ishlashini
- Faqat brauzer rangini
- Kompyuter fon rasmini
- Hech narsani

? Ekran ulashishda nimaga e'tibor berish kerak?
+ Faqat kerakli oyna yoki tabni ulashish va shaxsiy narsalarni yopish
- Barcha shaxsiy xabarlarni ochiq qoldirish
- Ekranni doim ulashib turish
- Ulashishdan oldin parollarni ko'rsatish

? Meet chatining vazifasi nima?
+ Uchrashuv davomida matnli xabar va havola yuborish
- Uchrashuvni yozib olish
- Mikrofonni sozlash
- Calendar tadbirini o'chirish
""",
    "ST18": """
? Quyidagi parollardan qaysi biri eng kuchli?
+ Tog'dagi-Olma-Daraxti!2026
- 123456
- qwerty
- ismim2010

? Kuchli parolning tavsiya etilgan minimal uzunligi qancha?
+ 12 belgi va undan ko'p
- 4 belgi
- 6 belgi
- Uzunlik muhim emas

? Nima uchun har bir saytda boshqa parol ishlatish kerak?
+ Bitta sayt buzilsa, boshqa hisoblar xavfsiz qoladi
- Shunda parol esda qolishi oson
- Saytlar bir xil parolni qabul qilmaydi
- Bu shart emas

? 2FA (ikki bosqichli tasdiqlash) nima?
+ Paroldan tashqari qo'shimcha kod yoki tasdiq talab qilinadi
- Ikkita bir xil parol o'rnatish
- Hisobga ikki kishi kirishi
- Parolni ikki marta kiritish

? Parol menejeri nima uchun kerak?
+ Har sayt uchun murakkab parollarni xavfsiz saqlaydi va to'ldiradi
- Parollarni do'stlarga yuboradi
- Parolni qisqartiradi
- Saytlarni bloklaydi

? Fishing (phishing) nima?
+ Soxta xat yoki sayt orqali parol va ma'lumotlarni o'g'irlashga urinish
- Kompyuter viruslarini tozalash
- Internet tezligini oshirish
- Fayllarni zaxiralash

? Qaysi belgi saytning soxta bo'lishi mumkinligini ko'rsatadi?
+ Manzilda imlo farqi bor: gooogle-login.com
- Manzil https://accounts.google.com
- Sayt tanish va manzil to'g'ri
- Brauzer "qulf" belgisini ko'rsatadi va manzil to'g'ri

? "Hisobingiz 1 soatda bloklanadi! Darhol parolni kiriting" degan xat kelsa, nima qilish kerak?
+ Havolani bosmaslik, rasmiy sayt yoki ilovaga o'zingiz kirib tekshirish
- Darhol havolani bosib, parolni kiritish
- Xatni do'stlarga yuborish
- Javob xatida parolni yozish

? SMS orqali kelgan tasdiqlash kodini kimga aytish mumkin?
+ Hech kimga — hatto "bank xodimi"ga ham
- Telefon qilgan har qanday odamga
- Faqat ijtimoiy tarmoqdagi do'stga
- Kod so'ralsa, darhol aytish kerak

? Raqamli gigiyenaga nima kiradi?
+ Shaxsiy ma'lumotni kam ulashish, ilova ruxsatlarini tekshirish, ekran vaqtini nazorat qilish
- Hamma ilovaga kamera va mikrofon ruxsatini berish
- Uy manzilini ochiq profilga yozish
- Barcha xatlardagi havolalarni ochish

? Google hisobingiz xavfsizligini tekshirish uchun qaysi vosita bor?
+ Security Checkup
- Google Translate
- Google Keep
- Google Maps

? Ommaviy (bepul) Wi-Fi'da qaysi harakat xavfli?
+ Bank yoki muhim hisoblarga kirib, maxfiy ma'lumot kiritish
- Ob-havo yangiliklarini o'qish
- Xarita ochish
- Musiqa tinglash
""",
    "ST19": """
? Starter yakuniy loyihasida logo va ijtimoiy tarmoq posti qaysi vositada tayyorlanadi?
+ Canva
- Figma
- Sheets
- Terminal

? 3 ekranli ilova prototipi qaysi vositada yaratiladi?
+ Figma
- Canva
- Docs
- Gmail

? Xarajat va daromad jadvali hamda diagramma qaysi vositada qilinadi?
+ Google Sheets
- Google Docs
- Scratch
- Google Meet

? Loyiha taqdimoti uchun nechta slayd talab qilingan?
+ 6–8 ta
- 1–2 ta
- 20 dan ortiq
- Talab yo'q

? Loyihaning barcha fayllari qanday topshiriladi?
+ Bitta Drive papkasida, ustozga ulashilgan holda
- Har bir fayl alohida fleshkada
- Faqat og'zaki tushuntirish bilan
- Gmail qoralamasida

? Yakuniy loyihada qaysi qism ixtiyoriy edi?
+ Scratch'dagi reklama mini-animatsiyasi
- Canva logosi
- Figma prototipi
- Slides taqdimoti

? Himoyada har bir o'quvchiga qancha vaqt berilgan?
+ 4–5 daqiqa va savollar
- 30 daqiqa
- 30 soniya
- Vaqt chegarasi yo'q

? Baholashda eng ko'p ball qaysi mezonga berilgan?
+ Vositalarni qo'llash (Canva, Figma, Sheets, Slides) — 50 ball
- Tartib va o'z vaqtida topshirish — 20 ball
- Faqat taqdimot — 100 ball
- Faqat fayl nomlari

? Yaxshi taqdimotda nima muhim?
+ Loyihaning g'oyasi, natijasi va ishlatilgan vositalarni aniq ko'rsatish
- Slayddagi matnni o'qib berish
- Iloji boricha uzoq gapirish
- Savollarga javob bermaslik

? Ustozga Drive papkasini qaysi huquq bilan ulashish kifoya (u izoh qoldira olishi uchun)?
+ Commenter
- Viewer
- Huquq bermaslik
- Faqat havolani ijtimoiy tarmoqqa joylash

? Loyiha mavzusi qanday edi?
+ "Mening kichik biznesim / ijtimoiy loyiham"
- "Mening sevimli o'yinim"
- "Python'da kalkulyator"
- Mavzu berilmagan

? Starter kursidan keyin qaysi kursga o'tish mumkin?
+ Python
- Faqat Canva
- Faqat Scratch
- Kurs tugaydi, davomi yo'q
""",
}
