"""Dasturchi 8-oy · QuizBot 3-qism: server — Linux, VPS, systemd, deploy, zaxira, monitoring, Docker, sifat, himoya.

Shell skriptlar ``bash -n`` bilan, Dockerfile ``docker build`` bilan, monitoring kodi aiogram 3 bilan va
yakuniy loyiha ``ruff`` bilan tekshirilgan.
"""

from .lesson_kit import lesson, step
from .lessons_m07 import BOT_23, DB_22, ERRORS, SCHEDULER

M = "8-oy · Telegram bot, 3-qism: server"

LINUX = r'''
ssh quiz@203.0.113.10
pwd
ls -la
cd quizbot
mkdir backups
nano notes.txt
cat notes.txt
chmod +x deploy.sh
df -h
free -h
htop
exit
'''

SETUP = r'''
#!/usr/bin/env bash
# Yangi VPS'ni sozlash (root sifatida bir marta ishga tushiriladi)
set -euo pipefail

apt update && apt upgrade -y
apt install -y python3-venv python3-pip git sqlite3 ufw

adduser --disabled-password --gecos "" quiz
usermod -aG sudo quiz
mkdir -p /home/quiz/.ssh
cp /root/.ssh/authorized_keys /home/quiz/.ssh/
chown -R quiz:quiz /home/quiz/.ssh

ufw allow OpenSSH
ufw --force enable
'''

ENV_EXAMPLE = r'''
BOT_TOKEN=7412345678:AAH...xyz
ADMIN_IDS=111111111
DB_PATH=quizbot.db
'''

SERVICE = r'''
[Unit]
Description=QuizBot Telegram bot
After=network-online.target
Wants=network-online.target

[Service]
User=quiz
WorkingDirectory=/home/quiz/quizbot
EnvironmentFile=/home/quiz/quizbot/.env
ExecStart=/home/quiz/quizbot/.venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''

DEPLOY = r'''
#!/usr/bin/env bash
# Botni yangilash: kod → kutubxonalar → testlar → qayta ishga tushirish
set -euo pipefail

cd /home/quiz/quizbot
git pull --ff-only
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -m pytest -q
sudo systemctl restart quizbot
sleep 3
systemctl is-active --quiet quizbot && echo "✅ Yangilandi: $(git log -1 --oneline)"
'''

BACKUP = r'''
#!/usr/bin/env bash
# Bazani zaxiralash: har kuni 03:00 da (cron), 7 kundan eskilari o'chiriladi
set -euo pipefail

SRC="${SRC:-/home/quiz/quizbot/quizbot.db}"
DIR="${DIR:-/home/quiz/backups}"
FILE="$DIR/quizbot-$(date +%F).db"

mkdir -p "$DIR"
sqlite3 "$SRC" ".backup '$FILE'"
gzip -f "$FILE"
find "$DIR" -name 'quizbot-*.db.gz' -mtime +7 -delete
echo "Zaxira: $FILE.gz"
'''

CRON = r'''
# crontab -e
0 3 * * * /home/quiz/quizbot/backup.sh >> /home/quiz/backups/backup.log 2>&1
'''

ERRORS_31 = ERRORS.replace(
    "from aiogram import Router\nfrom aiogram.types import ErrorEvent\n",
    "from aiogram import Bot, Router\nfrom aiogram.types import ErrorEvent\n\nfrom config import ADMIN_IDS\n",
).replace(
    '''async def on_error(event: ErrorEvent):
    logger.exception("Xato: %s", event.exception)''',
    '''async def on_error(event: ErrorEvent, bot: Bot):
    logger.exception("Xato: %s", event.exception)
    text = f"⚠️ {type(event.exception).__name__}: {event.exception}"[:3500]
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)''',
)

SCHEDULER_31 = SCHEDULER.replace(
    "from database import reminder_user_ids\n", "from config import ADMIN_IDS\nfrom database import reminder_user_ids, stats\n"
).replace(
    '''def setup_scheduler(bot: Bot) -> AsyncIOScheduler:''',
    '''async def heartbeat(bot: Bot):
    s = await stats()
    text = f"✅ Bot ishlayapti · foydalanuvchilar: {s['users']} · bugun testlar: {s['today']}"
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:''',
).replace(
    '''    scheduler.add_job(daily_reminder, "cron", hour=19, minute=0, args=[bot])''',
    '''    scheduler.add_job(daily_reminder, "cron", hour=19, minute=0, args=[bot])
    scheduler.add_job(heartbeat, "cron", hour=9, minute=0, args=[bot])''',
)

DOCKERFILE = r'''
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
'''

DOCKERIGNORE = r'''
.venv/
__pycache__/
*.db
.env
bot.log
'''

COMPOSE = r'''
services:
  bot:
    build: .
    env_file: .env
    environment:
      DB_PATH: /data/quizbot.db
    volumes:
      - ./data:/data
    restart: always
'''

PYPROJECT = r'''
[tool.ruff]
line-length = 110
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
'''

FETCH_ALL = r'''

async def fetch_all(query: str, params: tuple = ()) -> list[tuple]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(query, params)
        return await cursor.fetchall()
'''

TOP_USERS_33 = r'''
async def top_users(limit: int = 10) -> list[tuple]:
    return await fetch_all(
        "SELECT u.name, SUM(a.score) AS ball, COUNT(a.id) AS testlar "
        "FROM attempts a JOIN users u ON u.id = a.user_id "
        "GROUP BY a.user_id ORDER BY ball DESC LIMIT ?",
        (limit,),
    )
'''

DB_33 = DB_22.replace(
    '''async def top_users(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT u.name, SUM(a.score) AS ball, COUNT(a.id) AS testlar "
            "FROM attempts a JOIN users u ON u.id = a.user_id "
            "GROUP BY a.user_id ORDER BY ball DESC LIMIT ?",
            (limit,),
        )
        return await cursor.fetchall()
''',
    TOP_USERS_33.lstrip("\n"),
) + FETCH_ALL

# 9-dars: ruff format (uzun qator) natijasi.
BOT_33 = BOT_23.replace(
    "    dp.include_routers(errors.router, admin.router, settings.router, start.router, register.router, "
    "rating.router, menu.router, quiz.router)\n",
    "    dp.include_routers(\n"
    "        errors.router,\n"
    "        admin.router,\n"
    "        settings.router,\n"
    "        start.router,\n"
    "        register.router,\n"
    "        rating.router,\n"
    "        menu.router,\n"
    "        quiz.router,\n"
    "    )\n",
    1,
)
assert BOT_33 != BOT_23

README_FULL = r'''
# QuizBot — Telegram test boti

Ro'yxatdan o'tish, fanlar bo'yicha 10 savollik test, natijalar tarixi, reyting,
ikki til (uz/ru), kunlik eslatma va admin panel. aiogram 3 + SQLite + APScheduler.

## Imkoniyatlar
- 📝 Test: tasodifiy 10 savol, 30 soniya, rasmli savollar
- 📊 Reyting va 📈 shaxsiy natijalar
- 🛠 Admin: savol qo'shish, sahifalash, broadcast, statistika va CSV

## Ishga tushirish (Docker)

```
cp .env.example .env   # BOT_TOKEN va ADMIN_IDS ni yozing
docker compose up -d --build
```

## Muallif
Ali Valiyev · Minar Dasturchi, 8-oy
'''

LICENSE = r'''
MIT License

Copyright (c) 2026 Ali Valiyev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software, to deal in the Software without restriction.
'''

DEMO = r'''
# Demo ssenariysi (3 daqiqa)

1. Muammo (20 s): o'quvchilar test ishlashi va natijani kuzatish qiyin.
2. Foydalanuvchi (60 s): /start → /register → 📝 Test → natija → 📊 Reyting.
3. Admin (60 s): /admin → ➕ Savol → 📣 Xabar → 📈 Statistika + CSV.
4. Texnik (30 s): aiogram 3, SQLite, Docker, systemd, zaxira, pytest.
5. Kelajak (10 s): sayt bilan bog'lash (11-oy).
'''

QA = r'''
# Kutiladigan savollar

- Token qayerda saqlanadi? — .env, .gitignore'da.
- Bot server o'chsa nima bo'ladi? — systemd / Docker restart: always.
- Baza buzilsa? — har kuni 03:00 da zaxira, 7 kunlik.
- Spam bo'lsa? — ThrottlingMiddleware.
- Xatoni qanday bilasiz? — error handler admin'ga yozadi + bot.log.
'''

CHECKLIST = r'''
# Himoya oldidan tekshiruv

- [ ] Bot serverda ishlayapti: systemctl status quizbot
- [ ] pytest o'tadi, ruff check toza
- [ ] README, LICENSE, .env.example GitHub'da
- [ ] Zaxira fayli bor: ls ~/backups
- [ ] Demo ssenariysi va savollarga javoblar tayyor
'''

LESSONS = {
    "TB25": lesson(
        M, 1, "Linux asoslari va SSH",
        "Uzoqdagi serverga ulanamiz va Linux buyruqlari bilan ishlashni o'rganamiz.",
        "Starter'da: Terminal (cd, ls, mkdir); 7-oyda: bot kompyuterimizda ishladi.",
        "Kompyuter o'chsa bot ishlaydimi? Nega server kerak?",
        "VPS — internetdagi doim yoqiq kompyuter; SSH — xavfsiz ulanish; Linux fayl tizimi, ruxsatlar (chmod), resurslar (df, free, htop).",
        "Serverda o'z papkangizni yarating va unda README yozing.",
        [("💻", "Kompyuter", "ssh quiz@IP", ""),
         ("🔐", "SSH", "shifrlangan ulanish", "mem"),
         ("🐧", "Linux server", "24/7 yoqiq", ""),
         ("📂", "Fayllar", "ls, cd, nano", ""),
         ("📊", "Resurslar", "df, free, htop", "")],
        [
            step("Terminal", "Serverga ulanish", r'''
$ ssh quiz@203.0.113.10
quiz@server:~$ pwd
/home/quiz
quiz@server:~$ ls -la''',
                 [("ssh foydalanuvchi@IP", "server bilan shifrlangan ulanish."),
                  ("~", "uy papkasi: /home/quiz."),
                  ("ls -la", "yashirin fayllar (.env) va ruxsatlar bilan.")],
                 "drwxr-xr-x  quiz quiz  4096  quizbot"),
            step("Terminal", "Fayllar va ruxsatlar", r'''
$ mkdir backups
$ nano notes.txt
$ cat notes.txt
$ chmod +x deploy.sh
$ ls -l deploy.sh
-rwxr-xr-x 1 quiz quiz 312 deploy.sh''',
                 [("nano", "terminaldagi matn muharriri: Ctrl+O saqlash, Ctrl+X chiqish."),
                  ("chmod +x", "faylni ishga tushiriladigan qiladi."),
                  ("rwx", "o'qish, yozish, bajarish ruxsatlari.")],
                 "-rwxr-xr-x deploy.sh"),
            step("Terminal", "Server holati", r'''
$ df -h
/dev/vda1   25G  4.1G   20G  17% /
$ free -h
Mem:  1.9Gi  412Mi  1.1Gi
$ htop''',
                 [("df -h", "disk joyi."),
                  ("free -h", "operativ xotira."),
                  ("htop", "jarayonlar: bot qancha resurs ishlatyapti (q — chiqish).")],
                 "Disk 17%, xotira 412 MB band"),
        ],
        {"linux-buyruqlar.txt": LINUX},
        [("/home/quiz/", ""), ("├── quizbot/", ""), ("├── backups/", "yangi"), ("└── notes.txt", "yangi")],
        ["VPS va SSH", "Linux fayl buyruqlari", "chmod va ruxsatlar", "df, free, htop"],
        ["Majburiy: serverda papka yarating va README yozing.",
         "Qo'shimcha: scp bilan kompyuterdan serverga fayl yuboring."],
        "8.2 · VPS sozlash: foydalanuvchi, firewall, Python.",
    ),
    "TB26": lesson(
        M, 2, "VPS sozlash: foydalanuvchi, firewall, Python",
        "Yangi serverni xavfsiz qilamiz: alohida foydalanuvchi, SSH kalit va firewall.",
        "O'tgan darsda: SSH, Linux buyruqlari.",
        "chmod +x nima qiladi?",
        "root bilan ishlamaslik; adduser va sudo; SSH kalit (ssh-keygen, ssh-copy-id); ufw; apt bilan dasturlar.",
        "SSH kalit bilan parolsiz kirishni sozlang.",
        [("👑", "root", "faqat sozlash", ""),
         ("👤", "quiz", "sudo huquqi", "mem"),
         ("🔑", "SSH kalit", "parolsiz kirish", ""),
         ("🧱", "ufw", "faqat SSH ochiq", ""),
         ("🐍", "apt install", "python3-venv, git", "")],
        [
            step("setup_server.sh", "Dasturlarni o'rnatish", r'''
apt update && apt upgrade -y
apt install -y python3-venv python3-pip git sqlite3 ufw''',
                 [("apt", "Ubuntu'ning dastur menejeri (Windows'dagi o'rnatuvchi kabi)."),
                  ("-y", "savollarga avtomatik “ha”.")],
                 "Setting up python3-venv ... done"),
            step("setup_server.sh", "Alohida foydalanuvchi", r'''
adduser --disabled-password --gecos "" quiz
usermod -aG sudo quiz
mkdir -p /home/quiz/.ssh
cp /root/.ssh/authorized_keys /home/quiz/.ssh/
chown -R quiz:quiz /home/quiz/.ssh''',
                 [("root emas", "xato buyruq butun serverni buzmasligi uchun."),
                  ("sudo guruhi", "kerak bo'lganda vaqtincha admin huquqi."),
                  ("authorized_keys", "SSH kalitni yangi foydalanuvchiga ko'chiramiz.")],
                 "quiz foydalanuvchisi tayyor"),
            step("setup_server.sh", "Firewall", r'''
ufw allow OpenSSH
ufw --force enable''',
                 [("ufw", "keraksiz portlar yopiq — faqat SSH (22) ochiq."),
                  ("bot uchun port shart emas", "polling — bot o'zi Telegram'ga ulanadi.")],
                 "Status: active · 22/tcp ALLOW"),
        ],
        {"setup_server.sh": SETUP},
        [("server/", ""), ("├── /home/quiz", "yangi"), ("└── setup_server.sh", "yangi")],
        ["root va oddiy foydalanuvchi", "sudo", "SSH kalit", "ufw firewall"],
        ["Majburiy: ssh-keygen va ssh-copy-id bilan parolsiz kirish.",
         "Qo'shimcha: /etc/ssh/sshd_config'da parol bilan kirishni o'chiring."],
        "8.3 · Botni serverga joylash.",
    ),
    "TB27": lesson(
        M, 3, "Botni serverga joylash",
        "GitHub'dagi botni serverga olib kelamiz va qo'lda ishga tushiramiz.",
        "O'tgan darsda: quiz foydalanuvchisi, firewall, Python.",
        "Nega bot uchun port ochish shart emas?",
        "git clone; venv va requirements.txt; .env serverda alohida yaratiladi (.env.example namunasi); seed va qo'lda ishga tushirish.",
        "Bot serverda ishlayotganini skrinshot bilan ko'rsating.",
        [("🐙", "GitHub", "git clone", ""),
         ("🧪", ".venv", "pip install -r", ""),
         ("🔑", ".env", "serverda yaratiladi", "mem"),
         ("🌱", "seed.py", "savollar", ""),
         ("▶", "python bot.py", "ishlayapti", "")],
        [
            step("Terminal", "Kodni olib kelish", r'''
$ git clone https://github.com/ali/quizbot.git
$ cd quizbot
$ python3 -m venv .venv
$ .venv/bin/pip install -r requirements.txt''',
                 [("git clone", "repozitoriyning to'liq nusxasi."),
                  ("requirements.txt", "kompyuterdagi versiyalarning o'zi o'rnatiladi.")],
                 "Successfully installed aiogram-3.31.0 ..."),
            step(".env.example", "Maxfiy sozlamalar namunasi", ENV_EXAMPLE,
                 [(".env.example", "GitHub'da turadi — qaysi qiymatlar kerakligini ko'rsatadi."),
                  ("cp .env.example .env", "serverda nusxa olib, haqiqiy token yoziladi."),
                  (".env", "GitHub'ga hech qachon tushmaydi.")],
                 "$ cp .env.example .env && nano .env"),
            step("Terminal", "Ishga tushirish", r'''
$ .venv/bin/python seed.py
math: 3 ta savol
$ .venv/bin/python bot.py
INFO aiogram.dispatcher: Run polling for bot @minar_quiz_bot''',
                 [("seed", "yangi serverda baza bo'sh."),
                  ("muammo", "SSH oynasini yopsak — bot ham to'xtaydi. Yechim — keyingi dars.")],
                 "Bot ishlayapti (hozircha SSH ochiq ekan)"),
        ],
        {".env.example": ENV_EXAMPLE},
        [("/home/quiz/quizbot/", ""), ("├── .venv/", "yangi"), ("├── .env", "yangi"), ("└── quizbot.db", "yangi")],
        ["git clone", "Serverda venv", ".env va .env.example", "Qo'lda ishga tushirish"],
        ["Majburiy: bot serverda ishlayotganini skrinshot qiling.",
         "Qo'shimcha: tmux bilan bot SSH yopilganda ham ishlashini sinang."],
        "8.4 · systemd xizmati: bot 24/7.",
    ),
    "TB28": lesson(
        M, 4, "systemd xizmati: bot 24/7",
        "Bot server yoqilganda o'zi ishga tushadi va yiqilsa qayta turadi.",
        "O'tgan darsda: bot serverda qo'lda ishga tushdi.",
        "SSH oynasini yopsak bot nima bo'ladi?",
        "systemd — Linux xizmatlar menejeri; .service fayli bo'limlari; Restart=always; enable --now; journalctl bilan loglar.",
        "Botni to'xtatib (kill), systemd uni qayta ko'tarishini tekshiring.",
        [("📄", "quizbot.service", "xizmat fayli", "mem"),
         ("🔄", "daemon-reload", "systemd o'qiydi", ""),
         ("▶", "enable --now", "hozir va har yoqilganda", ""),
         ("♻", "Restart=always", "yiqilsa qayta", ""),
         ("📜", "journalctl", "loglar", "")],
        [
            step("quizbot.service", "Xizmat fayli", SERVICE,
                 [("User=quiz", "root emas, oddiy foydalanuvchi nomidan."),
                  ("EnvironmentFile", ".env dagi token xizmatga uzatiladi."),
                  ("Restart=always", "xato bilan to'xtasa 5 soniyadan keyin qayta.")],
                 "/etc/systemd/system/quizbot.service"),
            step("Terminal", "Yoqish va tekshirish", r'''
$ sudo cp quizbot.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now quizbot
$ systemctl status quizbot
● quizbot.service - QuizBot Telegram bot
   Active: active (running)''',
                 [("enable", "server qayta yoqilganda ham ishga tushadi."),
                  ("--now", "hozir darhol ham."),
                  ("status", "ishlayaptimi, qachondan beri.")],
                 "Active: active (running)"),
            step("Terminal", "Loglar", r'''
$ journalctl -u quizbot -f
INFO quizbot: user=111 text='📝 Test'
$ sudo systemctl restart quizbot''',
                 [("-u quizbot", "faqat shu xizmat loglari."),
                  ("-f", "yangi yozuvlarni jonli kuzatish (Ctrl+C — chiqish)."),
                  ("restart", "kod yangilanganda.")],
                 "Loglar jonli oqimda"),
        ],
        {"quizbot.service": SERVICE},
        [("/etc/systemd/system/", ""), ("└── quizbot.service", "yangi")],
        ["systemd xizmati", "Restart=always", "enable --now", "journalctl"],
        ["Majburiy: botni kill qilib, systemd qayta ko'tarishini tekshiring.",
         "Qo'shimcha: serverni reboot qilib, bot o'zi ishga tushganini ko'rsating."],
        "8.5 · Yangilash jarayoni: deploy.sh.",
    ),
    "TB29": lesson(
        M, 5, "Yangilash jarayoni: deploy.sh",
        "Kodni bir buyruq bilan yangilaymiz: pull → kutubxonalar → testlar → restart.",
        "O'tgan darsda: systemd xizmati.",
        "systemctl restart qachon kerak?",
        "Bash skript: shebang, set -euo pipefail; git pull --ff-only; testlar o'tmasa yangilanmaydi; is-active bilan tekshirish.",
        "deploy.sh oxirida bot loglaridan oxirgi 5 qatorni chiqaring.",
        [("💻", "git push", "kompyuterdan", ""),
         ("📥", "git pull", "serverda", ""),
         ("📦", "pip install", "yangi kutubxonalar", ""),
         ("🧪", "pytest", "o'tmasa — to'xta", "mem"),
         ("♻", "restart", "yangi kod", "")],
        [
            step("deploy.sh", "Skript boshi va xavfsizlik", r'''
#!/usr/bin/env bash
# Botni yangilash: kod → kutubxonalar → testlar → qayta ishga tushirish
set -euo pipefail''',
                 [("#!", "shebang — skriptni qaysi dastur bajarishini aytadi."),
                  ("set -e", "biror buyruq xato bersa — skript darhol to'xtaydi."),
                  ("-u -o pipefail", "noma'lum o'zgaruvchi va quvurdagi xatolar ham.")],
                 "(xato bo'lsa keyingi qadamlar bajarilmaydi)"),
            step("deploy.sh", "Yangilash qadamlari", r'''
cd /home/quiz/quizbot
git pull --ff-only
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -m pytest -q
sudo systemctl restart quizbot''',
                 [("--ff-only", "serverda qo'lda o'zgartirilgan bo'lsa — aralashtirmay to'xtaydi."),
                  ("pytest", "testlar yiqilsa — set -e tufayli restart bo'lmaydi, eski bot ishlayveradi.")],
                 "Already up to date.\n2 passed"),
            step("deploy.sh", "Natijani tekshirish", r'''
sleep 3
systemctl is-active --quiet quizbot && echo "✅ Yangilandi: $(git log -1 --oneline)"''',
                 [("is-active", "bot haqiqatan ishga tushdimi."),
                  ("$(...)", "buyruq natijasini matnga qo'yish.")],
                 "✅ Yangilandi: a81d0e4 Reyting qo'shildi"),
        ],
        {"deploy.sh": DEPLOY},
        [("/home/quiz/quizbot/", ""), ("└── deploy.sh", "yangi")],
        ["Bash skript asoslari", "set -euo pipefail", "Testdan keyin restart", "is-active tekshiruvi"],
        ["Majburiy: oxirida journalctl -u quizbot -n 5 chiqarsin.",
         "Qo'shimcha: deploy'ni kompyuterdan bitta ssh buyrug'i bilan ishga tushiring."],
        "8.6 · Zaxira: cron bilan bazani saqlash.",
    ),
    "TB30": lesson(
        M, 6, "Zaxira: cron bilan bazani saqlash",
        "Har kuni 03:00 da bazaning nusxasi olinadi, 7 kundan eskilari o'chadi.",
        "O'tgan darsda: deploy.sh.",
        "set -e nima qiladi?",
        "SQLite .backup — ishlab turgan bazadan to'g'ri nusxa; gzip; find -mtime; cron vaqt formati; tiklash.",
        "Zaxiradan bazani tiklashni sinab ko'ring.",
        [("🗄", "quizbot.db", "ishlab turgan baza", ""),
         ("💾", ".backup", "to'g'ri nusxa", "mem"),
         ("🗜", "gzip", "siqish", ""),
         ("🧹", "find -mtime +7", "eskilarini o'chirish", ""),
         ("⏰", "cron 03:00", "har kuni", "")],
        [
            step("backup.sh", "Nusxa olish", r'''
SRC="${SRC:-/home/quiz/quizbot/quizbot.db}"
DIR="${DIR:-/home/quiz/backups}"
FILE="$DIR/quizbot-$(date +%F).db"

mkdir -p "$DIR"
sqlite3 "$SRC" ".backup '$FILE'"''',
                 [(".backup", "bot yozayotgan paytda ham buzilmagan nusxa (cp bunday kafolat bermaydi)."),
                  ("$(date +%F)", "fayl nomida sana: quizbot-2026-11-19.db."),
                  ("${SRC:-...}", "o'zgaruvchi berilmasa — standart yo'l.")],
                 "backups/quizbot-2026-11-19.db"),
            step("backup.sh", "Siqish va tozalash", r'''
gzip -f "$FILE"
find "$DIR" -name 'quizbot-*.db.gz' -mtime +7 -delete
echo "Zaxira: $FILE.gz"''',
                 [("gzip", "fayl 5–10 baravar kichrayadi."),
                  ("-mtime +7", "7 kundan eski fayllar o'chiriladi — disk to'lmaydi.")],
                 "Zaxira: /home/quiz/backups/quizbot-2026-11-19.db.gz"),
            step("crontab", "Har kuni avtomatik", CRON,
                 [("0 3 * * *", "daqiqa soat kun oy hafta_kuni → har kuni 03:00."),
                  (">> backup.log 2>&1", "natija va xatolar log fayliga."),
                  ("crontab -e", "jadvalni tahrirlash.")],
                 "har kuni 03:00 → yangi zaxira"),
        ],
        {"backup.sh": BACKUP, "crontab": CRON},
        [("/home/quiz/", ""), ("├── quizbot/backup.sh", "yangi"), ("└── backups/", ""), ("    └── quizbot-2026-11-19.db.gz", "yangi")],
        ["SQLite .backup", "gzip va find -mtime", "cron vaqt formati", "Zaxiradan tiklash"],
        ["Majburiy: zaxiradan tiklashni sinang (gunzip + systemctl stop/start).",
         "Qo'shimcha: zaxirani admin'ga Telegram orqali fayl qilib yuboring."],
        "8.7 · Monitoring: xatolar admin'ga.",
    ),
    "TB31": lesson(
        M, 7, "Monitoring: xatolar admin'ga",
        "Xato bo'lsa admin darhol Telegram'da biladi; har kuni ertalab “bot ishlayapti” hisoboti keladi.",
        "O'tgan darsda: cron bilan zaxira.",
        "Bot kechasi yiqilsa, buni qanday bilamiz?",
        "Error handler'da admin'larga xabar; type(e).__name__; matnni Telegram limitiga qisqartirish; heartbeat — kunlik holat hisoboti.",
        "Bir xil xato 1 soatda faqat bir marta yuborilsin.",
        [("💥", "Xato", "handler'da", ""),
         ("🛡", "on_error", "log + javob", ""),
         ("📲", "Admin'ga", "⚠️ xabar", "mem"),
         ("🌅", "09:00 heartbeat", "✅ ishlayapti", "")],
        [
            step("handlers/errors.py", "Xatoni admin'ga yuborish", r'''
async def on_error(event: ErrorEvent, bot: Bot):
    logger.exception("Xato: %s", event.exception)
    text = f"⚠️ {type(event.exception).__name__}: {event.exception}"[:3500]
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)''',
                 [("type(e).__name__", "xato turi: KeyError, ValueError ..."),
                  ("[:3500]", "Telegram xabari 4096 belgidan oshmasin."),
                  ("bot: Bot", "error handler'ga ham bot uzatiladi.")],
                 "⚠️ KeyError: 'subject'"),
            step("scheduler.py", "Kunlik heartbeat", r'''
async def heartbeat(bot: Bot):
    s = await stats()
    text = f"✅ Bot ishlayapti · foydalanuvchilar: {s['users']} · bugun testlar: {s['today']}"
    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)''',
                 [("heartbeat", "“yurak urishi” — xabar kelmasa, bot ishlamayapti."),
                  ("stats()", "7-oydagi statistika qayta ishlatiladi.")],
                 "✅ Bot ishlayapti · foydalanuvchilar: 44 · bugun testlar: 9"),
            step("scheduler.py", "Jadvalga qo'shish", r'''
    scheduler.add_job(daily_reminder, "cron", hour=19, minute=0, args=[bot])
    scheduler.add_job(heartbeat, "cron", hour=9, minute=0, args=[bot])''',
                 [("ikkinchi vazifa", "bitta scheduler — bir nechta vazifa."),
                  ("09:00", "ish kuni boshida admin holatni ko'radi.")],
                 "09:00 va 19:00 — ikki vazifa"),
        ],
        {"handlers/errors.py": ERRORS_31, "scheduler.py": SCHEDULER_31},
        [("quizbot/", ""), ("├── scheduler.py", "o‘zgardi"), ("└── handlers/", ""), ("    └── errors.py", "o‘zgardi")],
        ["Xatoni admin'ga yuborish", "Xato turi va matni", "Heartbeat", "Bir scheduler — ko'p vazifa"],
        ["Majburiy: bir xil xato soatiga bir marta yuborilsin.",
         "Qo'shimcha: heartbeat'ga disk joyini ham qo'shing (shutil.disk_usage)."],
        "8.8 · Docker asoslari.",
        chat=[("bot", "⚠️ KeyError: 'subject'"), ("bot", "✅ Bot ishlayapti · foydalanuvchilar: 44 · bugun testlar: 9")],
        chat_title="Admin'ning Telegram'i", chat_sub="xato va kunlik hisobot",
        checks=["Ataylab xato qilganda admin'ga xabar keldimi?", "Foydalanuvchi ham tushunarli javob oldimi?"],
    ),
    "TB32": lesson(
        M, 8, "Docker asoslari",
        "Botni konteynerga joylaymiz: istalgan serverda bitta buyruq bilan ishga tushadi.",
        "O'tgan darsda: monitoring va heartbeat.",
        "systemd'ning Restart=always nima qiladi?",
        "Image va konteyner; Dockerfile qatlamlari; .dockerignore; docker compose: env_file, volume (ma'lumot saqlanadi), restart.",
        "docker compose logs bilan bot loglarini ko'rsating.",
        [("📄", "Dockerfile", "retsept", ""),
         ("📦", "Image", "docker build", ""),
         ("🐳", "Konteyner", "ishlayotgan bot", "mem"),
         ("💾", "Volume", "./data → /data", ""),
         ("♻", "restart: always", "o'zi turadi", "")],
        [
            step("Dockerfile", "Image retsepti", DOCKERFILE,
                 [("FROM python:3.12-slim", "tayyor Python o'rnatilgan kichik tizim."),
                  ("requirements avval", "kod o'zgarsa ham kutubxonalar qatlami keshdan olinadi — tez build."),
                  ("CMD", "konteyner ishga tushganda bajariladigan buyruq.")],
                 "Successfully built quizbot-bot"),
            step("docker-compose.yml", "Xizmat sozlamasi", COMPOSE,
                 [("env_file", "token .env dan — image ichiga yozilmaydi."),
                  ("volumes", "baza konteyner o'chsa ham ./data papkasida qoladi."),
                  ("restart: always", "systemd'dagi kabi — yiqilsa qayta turadi.")],
                 "services: bot"),
            step("Terminal", "Ishga tushirish", r'''
$ docker compose up -d --build
$ docker compose ps
quizbot-bot-1   running
$ docker compose logs -f bot''',
                 [("-d", "fonda ishlaydi."),
                  ("--build", "kod o'zgarganda image qayta yig'iladi."),
                  (".dockerignore", ".venv, .env va bazani image'ga qo'shmaydi.")],
                 "quizbot-bot-1  running"),
        ],
        {"Dockerfile": DOCKERFILE, ".dockerignore": DOCKERIGNORE, "docker-compose.yml": COMPOSE},
        [("quizbot/", ""), ("├── Dockerfile", "yangi"), ("├── .dockerignore", "yangi"), ("├── docker-compose.yml", "yangi"), ("└── data/", "yangi")],
        ["Image va konteyner", "Dockerfile qatlamlari", "docker compose", "Volume va restart"],
        ["Majburiy: docker compose logs bilan loglarni ko'rsating.",
         "Qo'shimcha: deploy.sh'ni Docker uchun moslang (git pull + up -d --build)."],
        "8.9 · Kod sifati: refaktoring, type hint, ruff.",
    ),
    "TB33": lesson(
        M, 9, "Kod sifati: refaktoring, type hint, ruff",
        "Kodni tartibga keltiramiz: avtomatik tekshiruv, takrorni olib tashlash va turlar.",
        "O'tgan darsda: Docker.",
        "Dockerfile'da nega requirements.txt avval ko'chiriladi?",
        "Linter (ruff) — xato va uslub tekshiruvi; pyproject.toml; refaktoring — ishlashini o'zgartirmay tozalash; type hint.",
        "ruff topgan barcha ogohlantirishlarni tuzating.",
        [("📄", "pyproject.toml", "qoidalar", ""),
         ("🔍", "ruff check", "muammolar", "mem"),
         ("🛠", "--fix", "avtomatik", ""),
         ("🧩", "fetch_all()", "takrorsiz", ""),
         ("🏷", "type hint", "-> list[tuple]", "")],
        [
            step("pyproject.toml", "ruff sozlamalari", PYPROJECT,
                 [("select", "E, F — xatolar; I — import tartibi; B — xavfli joylar; UP — yangi sintaksis."),
                  ("line-length", "qator uzunligi chegarasi.")],
                 "[tool.ruff] sozlandi"),
            step("Terminal", "Tekshirish va tuzatish", r'''
$ pip install ruff
$ ruff check .
bot.py:25:111: E501 Line too long (140 > 110)
Found 1 error.
$ ruff format .
$ ruff check .
All checks passed!''',
                 [("ruff check", "muammolarni fayl va qator bilan ko'rsatadi."),
                  ("ruff format", "uzun qatorlarni bo'ladi, kodni bir xil uslubga keltiradi; --fix — import tartibini."),
                  ("har commit oldidan", "odat qiling — kod doim toza.")],
                 "All checks passed!"),
            step("database.py", "Takrorni olib tashlaymiz", FETCH_ALL + "\n" + TOP_USERS_33,
                 [("fetch_all", "ulanish-so'rov-natija — bir joyda; har funksiyada takrorlanmaydi."),
                  ("-> list[tuple]", "type hint: funksiya nima qaytarishini ko'rsatadi."),
                  ("ishlashi o'zgarmaydi", "refaktoringdan keyin testlar baribir o'tishi kerak.")],
                 "top_users() — 9 qatordan 6 qatorga"),
        ],
        {"pyproject.toml": PYPROJECT, "database.py": DB_33, "bot.py": BOT_33},
        [("quizbot/", ""), ("├── pyproject.toml", "yangi"), ("├── bot.py", "o‘zgardi"), ("└── database.py", "o‘zgardi")],
        ["Linter va ruff", "pyproject.toml", "Refaktoring", "Type hint"],
        ["Majburiy: ruff topgan hammasini tuzating.",
         "Qo'shimcha: boshqa so'rovlarni ham fetch_all orqali yozing."],
        "8.10 · GitHub'da loyiha: README va requirements.",
    ),
    "TB34": lesson(
        M, 10, "GitHub'da loyiha: README va requirements",
        "Repozitoriyni portfolio darajasiga olib chiqamiz: README, LICENSE, .env.example, versiya.",
        "O'tgan darsda: ruff, refaktoring.",
        "ruff check --fix nima qiladi?",
        "Yaxshi README tuzilmasi; LICENSE (MIT); .env.example; git tag — versiya; GitHub Releases.",
        "README'ga 3 ta skrinshot qo'shing.",
        [("📝", "README", "nima va qanday", "mem"),
         ("⚖", "LICENSE", "MIT", ""),
         ("🔑", ".env.example", "namuna", ""),
         ("🏷", "git tag v1.0", "versiya", "")],
        [
            step("README.md", "Portfolio README", README_FULL,
                 [("birinchi qator", "bot nima qiladi — bir jumlada."),
                  ("Imkoniyatlar", "ro'yxat: o'qigan odam 10 soniyada tushunsin."),
                  ("Ishga tushirish", "boshqa dasturchi 2 buyruq bilan ko'tara olsin.")],
                 "github.com/ali/quizbot"),
            step("LICENSE", "Litsenziya", LICENSE,
                 [("MIT", "eng oddiy ochiq litsenziya: hamma foydalanishi mumkin."),
                  ("litsenziyasiz", "rasman hech kim foydalana olmaydi.")],
                 "License: MIT"),
            step("Terminal", "Versiya belgilash", r'''
$ git add README.md LICENSE .env.example
$ git commit -m "README, litsenziya va .env namunasi"
$ git tag -a v1.0 -m "QuizBot 1.0"
$ git push --follow-tags''',
                 [("git tag", "muhim holatga nom beradi: v1.0."),
                  ("--follow-tags", "teglarni ham GitHub'ga yuboradi."),
                  ("Releases", "GitHub'da versiya sahifasi paydo bo'ladi.")],
                 "* [new tag] v1.0 -> v1.0"),
        ],
        {"README.md": README_FULL, "LICENSE": LICENSE, ".env.example": ENV_EXAMPLE},
        [("quizbot/", ""), ("├── README.md", "o‘zgardi"), ("├── LICENSE", "yangi"), ("└── .env.example", "")],
        ["Yaxshi README", "LICENSE", ".env.example", "git tag va Releases"],
        ["Majburiy: README'ga 3 ta skrinshot qo'shing.",
         "Qo'shimcha: GitHub profilingizda repozitoriyni “Pinned” qiling."],
        "8.11 · Bot himoyasiga tayyorgarlik.",
    ),
    "TB35": lesson(
        M, 11, "Bot himoyasiga tayyorgarlik",
        "3 daqiqalik demo ssenariysi va kutiladigan savollarga javoblarni tayyorlaymiz.",
        "O'tgan darsda: README, LICENSE, versiya.",
        "Yaxshi README'da qanday bo'limlar bo'ladi?",
        "Taqdimot tuzilmasi: muammo → foydalanuvchi → admin → texnik → kelajak; vaqtni o'lchash; savol-javob tayyorgarligi.",
        "Ssenariyni soat bilan 2 marta mashq qiling.",
        [("❓", "Muammo", "20 s", ""),
         ("👤", "Foydalanuvchi", "60 s", ""),
         ("🛠", "Admin", "60 s", "mem"),
         ("⚙", "Texnik", "30 s", ""),
         ("🚀", "Kelajak", "10 s", "")],
        [
            step("demo.md", "Demo ssenariysi", DEMO,
                 [("vaqt", "har qism uchun aniq soniya."),
                  ("ikki rol", "foydalanuvchi va admin ko'zi bilan."),
                  ("texnik qism", "qisqa: nima ishlatilgan va nega.")],
                 "3 daqiqa"),
            step("savollar.md", "Kutiladigan savollar", QA,
                 [("oldindan", "savolga tayyor javob — ishonch."),
                  ("bilmasangiz", "“hali sinamadim, tekshiraman” — halol javob.")],
                 "5 ta savol — 5 ta javob"),
        ],
        {"demo.md": DEMO, "savollar.md": QA},
        [("quizbot/docs/", ""), ("├── demo.md", "yangi"), ("└── savollar.md", "yangi")],
        ["Taqdimot tuzilmasi", "Vaqt boshqaruvi", "Savol-javob tayyorgarligi", "Zaxira reja"],
        ["Majburiy: ssenariyni soat bilan 2 marta mashq qiling.",
         "Qo'shimcha: demo videosini (1 daqiqa) yozib, README'ga qo'shing."],
        "8.12 · QuizBot himoyasi.",
    ),
    "TB36": lesson(
        M, 12, "QuizBot himoyasi: demo kun",
        "Har o'quvchi o'z botini serverda ishlayotgan holda himoya qiladi.",
        "6–8-oylarda: aiogram 3, SQLite, admin, middleware, server, Docker.",
        "Himoya tartibini eslatamiz: demo 3 daq + savollar 2 daq.",
        "Baholash: ishlashi 40, kod sifati 30, taqdimot 20, GitHub va README 10.",
        "Himoyadagi izohlar bo'yicha botni yaxshilab, v1.1 tegini chiqaring.",
        [("✅", "Tekshiruv", "checklist", ""),
         ("🎤", "Demo", "3 daqiqa", "mem"),
         ("❓", "Savollar", "2 daqiqa", ""),
         ("📊", "Baholash", "100 ball", ""),
         ("🏁", "Bot tayyor", "→ 9-oy: saytlar", "")],
        [
            step("checklist.md", "Himoya oldidan tekshiruv", CHECKLIST,
                 [("server", "bot haqiqatan 24/7 ishlayapti."),
                  ("sifat", "pytest va ruff toza."),
                  ("GitHub", "README, LICENSE, .env.example.")],
                 "5/5 ✓"),
            step("Terminal", "Himoya kuni", r'''
$ systemctl status quizbot   (yoki docker compose ps)
$ ls ~/backups
$ pytest -q && ruff check .
Baholash: 40 + 30 + 20 + 10 = 100''',
                 [("jonli tekshiruv", "komissiya oldida bot ishlayotganini ko'rsatish."),
                  ("baholash", "ishlashi 40, kod 30, taqdimot 20, GitHub 10.")],
                 "🏁 QuizBot himoyadan o'tdi"),
        ],
        {"checklist.md": CHECKLIST},
        [("quizbot/", ""), ("└── checklist.md", "yangi")],
        ["Jonli demo", "Savollarga javob", "Baholash mezonlari", "Loyihani davom ettirish"],
        ["Majburiy: izohlar bo'yicha yaxshilab, v1.1 tegini chiqaring.",
         "Qo'shimcha: botga yangi fan va 20 ta savol qo'shing."],
        "9.1 · Veb qanday ishlaydi va HTML skelet.",
    ),
}
