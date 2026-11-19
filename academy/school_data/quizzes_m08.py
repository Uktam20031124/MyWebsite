"""Dasturchi 8-oy (TB25–TB36) testlari: har darsga 10 ta savol."""

QUIZZES = {
    "TB25": """
? VPS nima?
+ Internetdagi doim yoqiq virtual server
- Telegram boti
- Dasturlash tili
- Antivirus

? Serverga qanday ulanamiz?
+ ssh foydalanuvchi@IP
- http foydalanuvchi@IP
- ping IP
- git IP

? pwd buyrug'i nimani ko'rsatadi?
+ Hozirgi papka yo'lini
- Parolni
- Fayllar ro'yxatini
- Disk joyini

? ls -la nimani ko'rsatadi?
+ Yashirin fayllar bilan batafsil ro'yxat
- Faqat papkalar
- Faqat yashirin fayllar
- Fayl ichini

? chmod +x deploy.sh nima qiladi?
+ Faylni ishga tushiriladigan qiladi
- Faylni o'chiradi
- Faylni ochadi
- Faylni nusxalaydi

? df -h nimani ko'rsatadi?
+ Disk joyi
- Operativ xotira
- Jarayonlar
- Fayllar

? free -h nimani ko'rsatadi?
+ Operativ xotira holatini
- Disk joyi
- Internet tezligi
- Foydalanuvchilar

? nano'da faylni qanday saqlaymiz?
+ Ctrl + O
- Ctrl + S
- Esc
- :wq

? ~ belgisi nimani bildiradi?
+ Foydalanuvchining uy papkasini
- Ildiz papkani
- Joriy papkani
- Xatoni

? Nega bot uchun server kerak?
+ Kompyuter o'chsa ham bot 24/7 ishlashi uchun
- Bot tezlashadi
- Telegram talab qiladi
- Token uchun
""",
    "TB26": """
? Nega root bilan doim ishlamaymiz?
+ Xato buyruq butun serverni buzib qo'yishi mumkin
- root sekin ishlaydi
- root'da internet yo'q
- Farqi yo'q

? sudo nima?
+ Vaqtincha admin huquqi bilan buyruq bajarish
- Yangi foydalanuvchi
- Fayl muharriri
- Firewall

? apt install -y git nima qiladi?
+ git dasturini savolsiz o'rnatadi
- git'ni o'chiradi
- Repozitoriy yaratadi
- Faylni yuklaydi

? SSH kalitning afzalligi?
+ Parolsiz va xavfsizroq kirish
- Tezroq internet
- Fayllarni shifrlaydi
- Shart emas

? ufw nima?
+ Firewall — keraksiz portlarni yopadi
- Matn muharriri
- Dastur menejeri
- Baza

? ufw allow OpenSSH nega kerak?
+ Firewall yoqilgach ham SSH bilan kira olish uchun
- Botni ishga tushirish uchun
- Internetni yoqish uchun
- Shart emas

? Polling bot uchun port ochish kerakmi?
+ Yo'q — bot o'zi Telegram'ga ulanadi
- Ha, 80-port
- Ha, 443-port
- Ha, hamma portlar

? usermod -aG sudo quiz nima qiladi?
+ quiz foydalanuvchisini sudo guruhiga qo'shadi
- quiz'ni o'chiradi
- Parolni o'zgartiradi
- Papka yaratadi

? authorized_keys fayli nima?
+ Kirishga ruxsat berilgan ochiq SSH kalitlar ro'yxati
- Parollar fayli
- Bot tokeni
- Log fayli

? apt update nima qiladi?
+ Dasturlar ro'yxatini yangilaydi
- Hamma dasturlarni o'chiradi
- Serverni o'chiradi
- Botni yangilaydi
""",
    "TB27": """
? git clone nima qiladi?
+ Repozitoriyning to'liq nusxasini serverga oladi
- Faylni o'chiradi
- Yangi repo yaratadi
- Commit qiladi

? Serverda kutubxonalar qanday o'rnatiladi?
+ .venv/bin/pip install -r requirements.txt
- apt install aiogram
- Qo'lda nusxalab
- O'rnatish shart emas

? .env.example nima uchun?
+ Qaysi sozlamalar kerakligini ko'rsatadigan namuna
- Haqiqiy token saqlash
- Kod fayli
- Log

? Haqiqiy .env serverda qanday paydo bo'ladi?
+ cp .env.example .env va tokenni yozish
- git clone bilan avtomatik
- Telegram yuboradi
- O'zi yaratiladi

? Yangi serverda nega seed.py ishga tushiriladi?
+ Baza bo'sh — savollar kerak
- Botni tezlashtirish uchun
- Tokenni tekshirish uchun
- Shart emas

? Bot qo'lda ishga tushganda SSH oynasi yopilsa?
+ Bot ham to'xtaydi
- Ishlayveradi
- Qayta ishga tushadi
- Server o'chadi

? .env GitHub'da bo'lishi kerakmi?
+ Yo'q
- Ha
- Faqat token
- Faqat bir kun

? requirements.txt'ning foydasi serverda?
+ Kompyuterdagi bilan bir xil versiyalar o'rnatiladi
- Kod yoziladi
- Token saqlanadi
- Shart emas

? python3 -m venv .venv nima qiladi?
+ Loyiha uchun virtual muhit yaratadi
- Python'ni o'chiradi
- Botni ishga tushiradi
- Kutubxona o'rnatadi

? Bot ishlayotganini qanday bilamiz?
+ Terminalda “Run polling” chiqadi va bot javob beradi
- Hech qanday
- Server o'chadi
- Fayl paydo bo'ladi
""",
    "TB28": """
? systemd nima?
+ Linux'da xizmatlarni boshqaruvchi tizim
- Matn muharriri
- Telegram kutubxonasi
- Baza

? Restart=always nima qiladi?
+ Xizmat to'xtasa qayta ishga tushiradi
- Serverni o'chiradi
- Xizmatni o'chiradi
- Hech narsa

? EnvironmentFile nima uchun?
+ .env dagi qiymatlarni xizmatga uzatish uchun
- Log yozish uchun
- Kodni saqlash uchun
- Shart emas

? systemctl enable --now quizbot nima qiladi?
+ Hozir ishga tushiradi va server yoqilganda ham avtomatik ishga tushadi
- Faqat hozir
- Faqat o'chiradi
- Hech narsa

? daemon-reload nega kerak?
+ systemd yangi yoki o'zgargan .service faylini o'qishi uchun
- Serverni qayta yoqish uchun
- Botni o'chirish uchun
- Shart emas

? journalctl -u quizbot -f nima qiladi?
+ Xizmat loglarini jonli ko'rsatadi
- Xizmatni o'chiradi
- Faylni o'chiradi
- Botni yangilaydi

? systemctl status quizbot nimani ko'rsatadi?
+ Xizmat ishlayaptimi va qachondan beri
- Kodni
- Tokenni
- Foydalanuvchilarni

? User=quiz nega yoziladi?
+ Xizmat root emas, oddiy foydalanuvchi nomidan ishlashi uchun
- Shart emas
- Tezlik uchun
- Telegram uchun

? .service fayli qayerga qo'yiladi?
+ /etc/systemd/system/
- /home/quiz/
- /tmp/
- /var/log/

? Kod yangilangach nima qilinadi?
+ sudo systemctl restart quizbot
- Server qayta yoqiladi
- Hech narsa
- .service o'chiriladi
""",
    "TB29": """
? #!/usr/bin/env bash nima?
+ Skriptni bash bajarishini bildiruvchi shebang
- Izoh
- Xato
- Parol

? set -e nima qiladi?
+ Biror buyruq xato bersa skriptni to'xtatadi
- Hamma xatoni yashiradi
- Skriptni tezlashtiradi
- Hech narsa

? git pull --ff-only nima uchun?
+ Serverda qo'lda o'zgartirilgan bo'lsa aralashtirmay to'xtash uchun
- Majburiy yangilash uchun
- Branch yaratish uchun
- Shart emas

? deploy.sh da testlar yiqilsa nima bo'ladi?
+ restart bajarilmaydi, eski bot ishlayveradi
- Bot o'chadi
- Testlar o'tkazib yuboriladi
- Server o'chadi

? systemctl is-active --quiet quizbot nima tekshiradi?
+ Xizmat haqiqatan ishlayaptimi
- Kod to'g'rimi
- Internet bormi
- Disk to'lganmi

? $(git log -1 --oneline) nima qiladi?
+ Oxirgi commit qatorini matnga qo'yadi
- Commit yaratadi
- Logni o'chiradi
- Hech narsa

? deploy.sh qanday ishga tushiriladi?
+ ./deploy.sh (chmod +x qilingan bo'lsa)
- python deploy.sh
- git deploy.sh
- systemctl deploy

? Nega yangilash skriptini yozamiz?
+ Har safar bir xil, xatosiz va tez yangilash uchun
- Kod chiroyli bo'lishi uchun
- Telegram talab qiladi
- Shart emas

? pip install -q -r requirements.txt deploy'da nega bor?
+ Yangi qo'shilgan kutubxonalar o'rnatilishi uchun
- Kutubxonalarni o'chirish uchun
- Tezlik uchun
- Shart emas

? sleep 3 nima uchun?
+ Bot ishga tushishiga vaqt berish uchun
- Serverni sekinlashtirish uchun
- Xatoni yashirish uchun
- Shart emas
""",
    "TB30": """
? Nega bazani cp emas, sqlite3 .backup bilan nusxalaymiz?
+ Bot yozayotgan paytda ham buzilmagan nusxa olinadi
- Tezroq
- cp ishlamaydi
- Farqi yo'q

? $(date +%F) nima beradi?
+ Bugungi sana: 2026-11-19
- Hozirgi vaqt
- Fayl nomi
- Xato

? gzip nima qiladi?
+ Faylni siqadi
- Faylni o'chiradi
- Faylni ochadi
- Faylni shifrlaydi

? find ... -mtime +7 -delete nima qiladi?
+ 7 kundan eski fayllarni o'chiradi
- 7 ta fayl qoldiradi
- 7 kunlik fayllarni nusxalaydi
- Hech narsa

? Cron'da "0 3 * * *" nimani bildiradi?
+ Har kuni soat 03:00
- Har 3 daqiqada
- Har 3 soatda
- 3-kuni

? Cron jadvali qanday tahrirlanadi?
+ crontab -e
- nano cron
- systemctl cron
- cron edit

? >> backup.log 2>&1 nima qiladi?
+ Natija va xatolarni log faylga yozadi
- Logni o'chiradi
- Xatolarni yashiradi
- Hech narsa

? ${SRC:-/home/...} nimani bildiradi?
+ SRC berilmasa standart yo'l ishlatiladi
- SRC ni o'chiradi
- Xato
- Har doim standart

? Zaxiradan tiklashda birinchi nima qilinadi?
+ Botni to'xtatish (systemctl stop)
- Zaxirani o'chirish
- Serverni o'chirish
- Hech narsa

? Nega eski zaxiralar o'chiriladi?
+ Disk to'lib qolmasligi uchun
- Xavfsizlik uchun
- Telegram talab qiladi
- Shart emas
""",
    "TB31": """
? Monitoring nima?
+ Bot holatini kuzatish va muammo haqida darhol bilish
- Kod yozish
- Test ishlash
- Zaxira

? Xato bo'lganda admin qanday biladi?
+ Error handler admin'ga Telegram'da xabar yuboradi
- Bilmaydi
- Email keladi
- Bot o'chadi

? type(e).__name__ nima qaytaradi?
+ Xato turi nomini (masalan KeyError)
- Xato matnini
- Qator raqamini
- Fayl nomini

? Nega matn [:3500] bilan qisqartiriladi?
+ Telegram xabari 4096 belgidan oshmasligi uchun
- Chiroyli bo'lishi uchun
- Tezlik uchun
- Shart emas

? Heartbeat nima?
+ “Bot ishlayapti” degan muntazam hisobot
- Xato xabari
- Zaxira
- Log

? Heartbeat kelmasa nimani bildiradi?
+ Bot ishlamayotgan bo'lishi mumkin
- Hammasi joyida
- Admin bloklangan
- Server yangi

? Bitta scheduler'da nechta vazifa bo'lishi mumkin?
+ Bir nechta
- Faqat bitta
- Ikkita
- Hech qancha

? Error handler'ga bot qanday keladi?
+ Parametr sifatida (bot: Bot)
- Global o'zgaruvchidan
- Import qilib
- Kelmaydi

? Heartbeat qaysi ma'lumotni qayta ishlatadi?
+ 7-oydagi stats() funksiyasini
- Faqat vaqtni
- Tokenni
- Hech narsa

? Foydalanuvchi xatoda nima ko'radi?
+ Tushunarli “Kutilmagan xato” xabarini
- Traceback'ni
- Hech narsa
- Admin ID'sini
""",
    "TB32": """
? Docker image nima?
+ Dastur va uning muhiti yig'ilgan tayyor “quti” shabloni
- Rasm fayli
- Baza
- Log

? Konteyner nima?
+ Image'dan ishga tushirilgan jarayon
- Fayl
- Papka
- Server

? FROM python:3.12-slim nimani bildiradi?
+ Python o'rnatilgan kichik asosiy image'dan boshlash
- Python'ni o'chirish
- Yangi Python yozish
- Xato

? Nega requirements.txt kod'dan oldin ko'chiriladi?
+ Kod o'zgarganda kutubxonalar qatlami keshdan olinadi — build tez
- Python talab qiladi
- Tasodifiy
- Shart emas

? .dockerignore nima uchun?
+ .venv, .env va bazani image'ga qo'shmaslik uchun
- Docker'ni o'chirish uchun
- Fayllarni yashirish uchun
- Shart emas

? docker-compose.yml'dagi volumes nima beradi?
+ Baza konteyner o'chsa ham saqlanadi
- Tezlik
- Xavfsizlik
- Hech narsa

? restart: always nima qiladi?
+ Konteyner to'xtasa qayta ishga tushiradi
- Har kuni o'chiradi
- Image'ni yangilaydi
- Hech narsa

? docker compose up -d --build nima qiladi?
+ Image'ni qayta yig'ib, fonda ishga tushiradi
- Konteynerni o'chiradi
- Loglarni ko'rsatadi
- Image'ni o'chiradi

? env_file: .env nimani ta'minlaydi?
+ Token image ichiga yozilmaydi, ishga tushganda beriladi
- Token GitHub'ga yuklanadi
- Token o'chadi
- Hech narsa

? docker compose logs -f bot nima qiladi?
+ Bot konteyneri loglarini jonli ko'rsatadi
- Botni to'xtatadi
- Image yaratadi
- Hech narsa
""",
    "TB33": """
? Linter nima?
+ Koddagi xato va uslub muammolarini avtomatik topadigan dastur
- Kod yozadigan AI
- Test
- Debugger

? ruff qaysi faylda sozlanadi?
+ pyproject.toml
- requirements.txt
- .env
- README.md

? ruff check --fix nima qiladi?
+ Xavfsiz tuzatishlarni o'zi bajaradi
- Hamma kodni o'chiradi
- Testlarni ishga tushiradi
- Hech narsa

? E501 qoidasi nimani bildiradi?
+ Qator juda uzun
- Import tartibi
- Noma'lum o'zgaruvchi
- Bo'sh fayl

? ruff format nima qiladi?
+ Kodni bir xil uslubga keltiradi, uzun qatorlarni bo'ladi
- Kodni o'chiradi
- Kodni shifrlaydi
- Testlarni yozadi

? Refaktoring nima?
+ Ishlashini o'zgartirmasdan kodni tozalash
- Yangi imkoniyat qo'shish
- Kodni o'chirish
- Xatoni yashirish

? fetch_all() helper'ining foydasi?
+ Ulanish va so'rov kodini har funksiyada takrorlamaslik
- Bazani tezlashtirish
- Xatolarni yashirish
- Shart emas

? -> list[tuple] nima?
+ Funksiya qaytaradigan tur haqida type hint
- Xato
- Izoh
- Shart

? Refaktoringdan keyin nima tekshiriladi?
+ Testlar baribir o'tishi
- Hech narsa
- Kod uzunligi
- Fayl nomlari

? I001 qoidasi nimani tekshiradi?
+ Importlar tartibini
- Qator uzunligini
- O'zgaruvchi nomlarini
- Bo'sh qatorlarni
""",
    "TB34": """
? Yaxshi README'ning birinchi qatorida nima bo'ladi?
+ Loyiha nima qilishi — bir jumlada
- Muallif ismi
- Litsenziya
- Token

? LICENSE fayli nega kerak?
+ Boshqalar kodni qanday shartlarda ishlatishini belgilaydi
- Kodni himoya qiladi
- Shart emas
- Telegram talab qiladi

? MIT litsenziyasi nimani bildiradi?
+ Hamma foydalanishi va o'zgartirishi mumkin
- Faqat muallif ishlatadi
- Pullik
- Taqiqlangan

? git tag -a v1.0 nima qiladi?
+ Muhim holatga v1.0 nomini beradi
- Branch yaratadi
- Commit o'chiradi
- Faylni yuklaydi

? git push --follow-tags nima qiladi?
+ Commitlar bilan birga teglarni ham yuboradi
- Faqat teglarni o'chiradi
- Faqat kodni
- Hech narsa

? README'dagi “Ishga tushirish” bo'limi nima uchun?
+ Boshqa dasturchi loyihani tez ko'tara olishi uchun
- Chiroyli bo'lishi uchun
- Shart emas
- Token uchun

? .env.example'da haqiqiy token bo'ladimi?
+ Yo'q — faqat namuna qiymat
- Ha
- Faqat admin ID
- Ba'zan

? GitHub Releases nima?
+ Versiyalar (teglar) sahifasi
- Xatolar ro'yxati
- Branchlar
- Commitlar

? Portfolio uchun repozitoriyda nima muhim?
+ Tushunarli README, skrinshotlar, toza kod
- Ko'p fayllar
- Uzun kod
- Hech narsa

? “Pinned” repozitoriy nima?
+ GitHub profilda ko'zga tashlanadigan qilib qo'yilgan loyiha
- O'chirilgan repo
- Yashirin repo
- Fork
""",
    "TB35": """
? Demo qancha davom etadi?
+ 3 daqiqa
- 10 daqiqa
- 30 soniya
- 1 soat

? Demo nimadan boshlanadi?
+ Muammodan
- Koddan
- Texnik tafsilotlardan
- Savollardan

? Demo kim ko'zi bilan ko'rsatiladi?
+ Oddiy foydalanuvchi va admin
- Faqat admin
- Faqat dasturchi
- Hech kim

? Nega savollarga oldindan tayyorlanamiz?
+ Ishonch bilan aniq javob berish uchun
- Shart emas
- Vaqt o'tishi uchun
- Komissiya talab qiladi

? Bilmagan savolga qanday javob beramiz?
+ Halol: “hali sinamadim, tekshiraman”
- To'qib chiqaramiz
- Javob bermaymiz
- Mavzuni o'zgartiramiz

? Bot server o'chsa nima bo'ladi degan savolga javob?
+ systemd yoki Docker restart: always qayta ko'taradi
- Bot o'chib qoladi
- Bilmayman
- Server o'chmaydi

? Spamdan himoya qaysi qismda?
+ ThrottlingMiddleware
- texts.py
- seed.py
- README

? Mashq nega soat bilan qilinadi?
+ Vaqtga sig'ishni tekshirish uchun
- Shart emas
- Chiroyli bo'lishi uchun
- Telegram talab qiladi

? Demo ssenariysida texnik qismga qancha vaqt?
+ 30 soniya
- 3 daqiqa
- 10 daqiqa
- Umuman yo'q

? Kelajak rejasida nima aytiladi?
+ Loyiha qanday rivojlanadi (masalan sayt bilan bog'lash)
- Hech narsa
- Bot o'chiriladi
- Faqat muallif ismi
""",
    "TB36": """
? Baholashda eng katta ulush nimaga?
+ Ishlashi — 40 ball
- Taqdimot
- README
- Kod uzunligi

? Kod sifatiga necha ball?
+ 30
- 40
- 10
- 20

? Taqdimotga necha ball?
+ 20
- 40
- 30
- 10

? GitHub va README'ga necha ball?
+ 10
- 30
- 40
- 20

? Himoya oldidan serverda nima tekshiriladi?
+ Bot ishlayotgani (systemctl status yoki docker compose ps)
- Hech narsa
- Faqat kod
- Faqat README

? pytest va ruff himoyada nega ko'rsatiladi?
+ Kod sifati va ishonchliligini isbotlash uchun
- Vaqt o'tishi uchun
- Shart emas
- Telegram talab qiladi

? Himoyadan keyin nima qilinadi?
+ Izohlar bo'yicha yaxshilab, yangi versiya (v1.1) chiqariladi
- Loyiha o'chiriladi
- Hech narsa
- Qaytadan yoziladi

? 6–8-oylarda bot uchun nima o'rganildi?
+ aiogram 3, SQLite, admin, middleware, server, Docker
- Django
- HTML va CSS
- Scratch

? 9-oyda nima boshlanadi?
+ Birinchi sayt: Portfolio (HTML, CSS, JS)
- Yangi bot
- Python asoslari
- Starter

? Zaxira mavjudligi qanday ko'rsatiladi?
+ ls ~/backups
- cat .env
- git log
- htop
""",
}
