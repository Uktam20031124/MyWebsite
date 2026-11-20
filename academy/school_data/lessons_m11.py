"""Dasturchi 11-oy · EduCenter: server, integratsiya va yakuniy loyiha — WB25–WB36 "Dars kodi".

Loyiha 10-oy generatoridan (lessons_m10.project) davom etadi: ``project(n)`` = 10-oy fayllari + 11-oy qo'shimchalari.
Loyihadan tashqari fayllar (QuizBot, Portfolio, rezyume, reja) — ``EXTRA``.
Tekshiruv: har bosqich haqiqiy Django loyihasida yig'ilib ``manage.py test`` dan o'tdi; gunicorn + haqiqiy Nginx
orqali so'rovlar, Telegram xabari (urlopen mock), QuizBot handleri jonli API bilan sinaldi.
"""

from . import lessons_m09 as m09
from . import lessons_m10 as m10
from .lesson_kit import lesson, step
from .lessons_m07 import CONFIG_14
from .lessons_m08 import BOT_33

M = "11-oy · EduCenter: server va integratsiya"
pick, lines = m10.pick, m10.lines

NEWS_MODELS = '''from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    text = models.TextField()
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", args=[self.slug])
'''

NEWS_VIEWS = '''from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.objects.filter(is_published=True)
    paginate_by = 5


class PostDetailView(DetailView):
    queryset = Post.objects.filter(is_published=True)
'''

NEWS_URLS = '''from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]
'''

NEWS_ADMIN = '''from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created"]
    list_editable = ["is_published"]
    prepopulated_fields = {"slug": ["title"]}
'''

POST_LIST = '''{% extends "base.html" %}

{% block title %}Yangiliklar — EduCenter{% endblock %}

{% block content %}
  <section>
    <h1>Yangiliklar</h1>
    {% for post in page_obj %}
      <article class="card post">
        <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
        <p class="muted">{{ post.created|date:"d.m.Y" }}</p>
        <p>{{ post.text|truncatewords:30 }}</p>
      </article>
    {% empty %}
      <p>Hozircha yangilik yo'q.</p>
    {% endfor %}
    {% if page_obj.has_other_pages %}
      <nav class="pagination" aria-label="Sahifalar">
        {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}">← Oldingi</a>{% endif %}
        <span>{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
        {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}">Keyingi →</a>{% endif %}
      </nav>
    {% endif %}
  </section>
{% endblock %}
'''

POST_DETAIL = '''{% extends "base.html" %}

{% block title %}{{ post.title }} — EduCenter{% endblock %}

{% block content %}
  <article class="narrow">
    <p class="muted">{{ post.created|date:"d.m.Y" }}</p>
    <h1>{{ post.title }}</h1>
    {{ post.text|linebreaks }}
    <p><a href="{% url 'news:list' %}">← Barcha yangiliklar</a></p>
  </article>
{% endblock %}
'''


def env_example(n):
    return pick(n, [
        "SECRET_KEY=bu-yerga-50-belgidan-uzun-tasodifiy-kalit",
        "DEBUG=1",
        "ALLOWED_HOSTS=127.0.0.1,localhost",
        (30, "TELEGRAM_BOT_TOKEN="),
        (30, "TELEGRAM_ADMIN_ID="),
    ])


def tests_py(n):
    return pick(n, [
        (30, "from unittest.mock import patch"),
        (30, ""),
        (28, 30, "from django.test import TestCase, override_settings"),
        (26, 28, "from django.test import TestCase"),
        (30, "from django.test import TestCase, override_settings"),
        "from django.urls import reverse",
        "",
        (26, 33, "from .models import Course, Enrollment"),
        (33, "from .models import Category, Course, Enrollment"),
        (30, "from .telegram import notify_admin"),
        "",
        "",
        (28, "@override_settings(SECURE_SSL_REDIRECT=False)"),
        "class CourseViewsTests(TestCase):",
        "    @classmethod",
        "    def setUpTestData(cls):",
        '        cls.course = Course.objects.create(title="Python asoslari", slug="python-asoslari", description="Noldan boshlab")',
        '        Course.objects.create(title="Yashirin", slug="yashirin", description="x", is_active=False)',
        "",
        "    def test_list_shows_only_active(self):",
        '        response = self.client.get(reverse("course_list"))',
        '        self.assertContains(response, "Python asoslari")',
        '        self.assertNotContains(response, "Yashirin")',
        "",
        "    def test_unknown_or_inactive_course_is_404(self):",
        '        self.assertEqual(self.client.get("/kurslar/yoq/").status_code, 404)',
        '        self.assertEqual(self.client.get("/kurslar/yashirin/").status_code, 404)',
        "",
        (26, 30, "    def test_enrollment_saves_and_redirects(self):"),
        (30, '    @patch("courses.views.notify_admin")'),
        (30, "    def test_enrollment_saves_and_redirects(self, notify):"),
        "        url = self.course.get_absolute_url()",
        '        response = self.client.post(url, {"name": "Vali", "phone": "+998901234567"})',
        "        self.assertRedirects(response, url)",
        '        self.assertEqual(Enrollment.objects.get().name, "Vali")',
        (30, "        notify.assert_called_once()"),
        (30, '        self.assertIn("Vali", notify.call_args.args[0])'),
        "",
        "    def test_cabinet_requires_login(self):",
        '        response = self.client.get(reverse("cabinet"))',
        '        self.assertRedirects(response, "/accounts/login/?next=/accounts/cabinet/")',
        (29, ""),
        (29, "    def test_api_returns_active_courses(self):"),
        (29, '        data = self.client.get(reverse("api_courses")).json()'),
        (29, '        self.assertEqual([c["slug"] for c in data["courses"]], ["python-asoslari"])'),
        (29, '        self.assertEqual(data["courses"][0]["url"], "http://testserver/kurslar/python-asoslari/")'),
        (33, ""),
        (33, "    def test_list_filters_by_category(self):"),
        (33, '        web = Category.objects.create(name="Web")'),
        (33, '        Course.objects.create(title="Django", slug="django", description="sayt", category=web)'),
        (33, '        response = self.client.get(reverse("course_list"), {"category": web.pk})'),
        (33, '        self.assertContains(response, "Django")'),
        (33, '        self.assertNotContains(response, "Python asoslari")'),
        (30, ""),
        (30, ""),
        (30, "class NotifyAdminTests(TestCase):"),
        (30, '    @override_settings(TELEGRAM_BOT_TOKEN="", TELEGRAM_ADMIN_ID="")'),
        (30, "    def test_disabled_without_token(self):"),
        (30, '        self.assertFalse(notify_admin("x"))'),
        (30, ""),
        (30, '    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_ADMIN_ID="7")'),
        (30, "    @patch(\"courses.telegram.urllib.request.urlopen\", side_effect=OSError(\"tarmoq yo'q\"))"),
        (30, "    def test_network_error_does_not_break_site(self, urlopen):"),
        (30, '        with self.assertLogs("courses.telegram", "ERROR"):'),
        (30, '            self.assertFalse(notify_admin("x"))'),
    ])


SERVICE = '''[Unit]
Description=EduCenter Django sayti (gunicorn)
After=network.target

[Service]
User=edu
Group=www-data
WorkingDirectory=/home/edu/educenter
EnvironmentFile=/home/edu/educenter/.env
ExecStart=/home/edu/educenter/.venv/bin/gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''

NGINX = '''server {
    listen 80;
    server_name educenter.example.com;

    client_max_body_size 10M;

    location /static/ {
        alias /home/edu/educenter/staticfiles/;
    }

    location /media/ {
        alias /home/edu/educenter/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
'''

TELEGRAM = '''import json
import logging
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def notify_admin(text: str) -> bool:
    """Admin'ga Telegram xabari. Xato bo'lsa sayt to'xtamaydi — faqat log yoziladi."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_ADMIN_ID:
        return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": settings.TELEGRAM_ADMIN_ID, "text": text}).encode()
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status == 200
    except OSError:
        logger.exception("Telegram xabari yuborilmadi")
        return False
'''

DEPLOY = '''#!/usr/bin/env bash
# EduCenter'ni serverda yangilash: ./deploy/deploy.sh
set -euo pipefail

cd /home/edu/educenter
git pull --ff-only
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python manage.py test
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart educenter
sleep 2
systemctl is-active --quiet educenter
echo "✅ Yangilandi: $(git log -1 --oneline)"
'''

REVIEW = '''# Kod tahlili (code review) — tekshiruv ro'yxati

## Ishlashi
- [ ] Hamma sahifalar ochiladi, 404 va 500 sahifalari bor
- [ ] Formalar xatoni tushunarli ko'rsatadi
- [ ] `python manage.py test` — hammasi OK

## Xavfsizlik
- [ ] `.env` Git'da yo'q, `SECRET_KEY` kodda yozilmagan
- [ ] Serverda `DEBUG=0`, `check --deploy` toza
- [ ] Shaxsiy sahifalarda `@login_required`
- [ ] Har POST formada `{% csrf_token %}`

## Kod sifati
- [ ] Nomlar tushunarli, takrorlanish yo'q
- [ ] View'lar qisqa, mantiq model yoki alohida funksiyada
- [ ] Bazaga so'rovlar soni oqilona (`select_related`)
'''


def project(n: int) -> dict:
    out = m10.project(n)
    if n >= 25:
        out |= {
            "news/models.py": NEWS_MODELS,
            "news/views.py": NEWS_VIEWS,
            "news/urls.py": NEWS_URLS,
            "news/admin.py": NEWS_ADMIN,
            "templates/news/post_list.html": POST_LIST,
            "templates/news/post_detail.html": POST_DETAIL,
        }
    if n >= 26:
        out |= {".env.example": env_example(n), "courses/tests.py": tests_py(n)}
    if n >= 27:
        out["deploy/educenter.service"] = SERVICE
    if n >= 28:
        out["deploy/nginx.conf"] = NGINX
    if n >= 30:
        out["courses/telegram.py"] = TELEGRAM
    if n >= 34:
        out |= {"deploy/deploy.sh": DEPLOY, "REVIEW.md": REVIEW}
    return out


# --- Loyihadan tashqari fayllar ---------------------------------------------------------------

BOT_COURSES = """import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import SITE_URL

router = Router()


async def fetch_courses() -> list[dict]:
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(f"{SITE_URL}/api/courses/") as response:
            response.raise_for_status()
            data = await response.json()
    return data["courses"]


@router.message(Command("kurslar"))
async def cmd_courses(message: Message):
    try:
        courses = await fetch_courses()
    except (aiohttp.ClientError, TimeoutError):
        await message.answer("Sayt hozir javob bermayapti, birozdan keyin urinib ko'ring.")
        return
    if not courses:
        await message.answer("Hozircha kurslar yo'q.")
        return
    lines = [f"📚 {c['title']} — {c['price']:,} so'm · {c['months']} oy".replace(",", " ") for c in courses]
    await message.answer("EduCenter kurslari:\\n\\n" + "\\n".join(lines))
"""

CONFIG_31 = CONFIG_14.rstrip("\n") + '\nSITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")\n'
BOT_31 = BOT_33.replace(
    "from handlers import admin, errors, menu, quiz, rating, register, settings, start",
    "from handlers import admin, courses, errors, menu, quiz, rating, register, settings, start",
).replace("        admin.router,\n", "        admin.router,\n        courses.router,\n")
assert BOT_31.count("courses") == 2, "bot.py: courses router qo'shilmadi"

PLAN = '''# Yakuniy loyiha rejasi: Kutubxona

## Muammo
Maktab kutubxonasida qaysi kitob kimda ekanini daftarda yozishadi — yo'qoladi va qidirish qiyin.

## Foydalanuvchilar
- O'quvchi: kitob qidiradi, band qiladi
- Kutubxonachi: kitob beradi va qaytarib oladi

## MVP — birinchi versiya
1. Kitoblar ro'yxati va qidiruv
2. Kitob sahifasi: bor yoki band
3. O'quvchi kabineti: mening kitoblarim
4. Admin: kitob berish va qaytarish

## Modellar
- Book: title, author, isbn, copies
- Loan: book, user, taken, returned

## Jadval
| Kun | Ish |
| --- | --- |
| 1 | Modellar, admin, ro'yxat |
| 2 | Kitob sahifasi, qidiruv, kabinet |
| 3 | Testlar, serverga joylash |
'''

RESUME = '''# Ali Valiyev — junior Python dasturchi

Toshkent · Telegram: @ali_dev · github.com/ali

## Loyihalar
- **EduCenter** — o'quv markaz sayti (Django): kurslar, ariza, kabinet, API, HTTPS.
  https://educenter.example.com
- **QuizBot** — Telegram test boti (aiogram 3, SQLite): admin panel, reyting, Docker.
- **Portfolio** — shaxsiy sayt (HTML, CSS, JS): https://ali.github.io

## Ko'nikmalar
Python · Django · aiogram 3 · SQL/SQLite · HTML/CSS/JS · Git/GitHub · Linux, Nginx, systemd

## Ta'lim
Minar Dasturchi — 11 oylik dasturlash kursi, 2026
'''

PORTFOLIO_JS = m09.script_js(12).replace(
    '''const projects = [
  { title: "QuizBot", text: "Telegram test boti: aiogram 3, SQLite.", tags: ["python", "bot"] },
  { title: "Kundalik", text: "Konsol vazifalar ro'yxati: OOP va JSON.", tags: ["python"] },
  { title: "Portfolio", text: "Shu sayt: HTML, CSS va JavaScript.", tags: ["web"] },
];''',
    '''const projects = [
  {
    title: "EduCenter",
    text: "O'quv markaz sayti: Django, kabinet, API va HTTPS.",
    tags: ["python", "web"],
    url: "https://educenter.example.com",
  },
  {
    title: "QuizBot",
    text: "Telegram test boti: aiogram 3, SQLite, Docker.",
    tags: ["python", "bot"],
    url: "https://github.com/ali/quizbot",
  },
  { title: "Portfolio", text: "Shu sayt: HTML, CSS va JavaScript.", tags: ["web"], url: "https://github.com/ali/ali.github.io" },
];''',
).replace(
    '''    .map((p) => `<article class="card"><h3>${p.title}</h3><p>${p.text}</p></article>`)''',
    '''    .map((p) => `<article class="card"><h3>${p.title}</h3><p>${p.text}</p><a href="${p.url}">Ko'rish →</a></article>`)''',
)
assert "EduCenter" in PORTFOLIO_JS and "Ko'rish →" in PORTFOLIO_JS

DEMO_DAY = '''# DEMO DAY — 5 daqiqa

## Ssenariy
1. Muammo va kim uchun (30 s)
2. Jonli demo: foydalanuvchi ko'zi bilan (2 min)
3. Admin va bot integratsiyasi (1 min)
4. Texnik qism: Django, testlar, server, HTTPS (1 min)
5. Keyingi qadamlar (30 s)

## Baholash
| Mezon | Ball |
| --- | --- |
| Ishlashi (internetda, HTTPS) | 40 |
| Kod sifati va testlar | 30 |
| Taqdimot | 20 |
| README va GitHub | 10 |

## Oxirgi tekshiruv
- [ ] Sayt https:// bilan ochiladi
- [ ] `python manage.py test` — OK
- [ ] Bot /kurslar ga javob beradi
- [ ] Zaxira nusxa olingan
'''

EXTRA = {
    31: {"quizbot/handlers/courses.py": BOT_COURSES, "quizbot/config.py": CONFIG_31, "quizbot/bot.py": BOT_31},
    32: {"PLAN.md": PLAN},
    35: {"RESUME.md": RESUME, "portfolio/script.js": PORTFOLIO_JS},
    36: {"DEMO_DAY.md": DEMO_DAY},
}


def changed(n: int) -> dict:
    old = project(n - 1)
    return {k: v for k, v in project(n).items() if old.get(k) != v}


def files(n: int) -> dict:
    return changed(n) | EXTRA.get(n, {})


def tree(n: int, extra: list | None = None) -> list:
    old = project(n - 1)
    tags = {k: ("o‘zgardi" if k in old else "yangi") for k in changed(n)}
    tags |= {k: ("o‘zgardi" if k.endswith(("config.py", "bot.py", "script.js")) else "yangi") for k in EXTRA.get(n, {})}
    tags |= dict(extra or [])
    names = list(tags)
    root = "educenter/" if changed(n) else "loyihalar/"
    rows = [(root, "")]
    for i, name in enumerate(names):
        rows.append((("└── " if i == len(names) - 1 else "├── ") + name, tags[name]))
    return rows


def preview(n: int, path: str, checks: list, url: str | None = None) -> dict:
    return {"image": f"lessons/WB{n}/site.png", "title": "Brauzerda natija", "sub": "chapda — kompyuter, o'ngda — telefon",
            "url": url or "127.0.0.1:8000" + path, "path": path, "checks": checks}


V = project(36)["courses/views.py"]
S = project(36)["config/settings.py"]
T = project(33)["courses/tests.py"]

LESSONS = {
    "WB25": lesson(
        M, 1, "Yangiliklar, sahifalash va class-based views",
        "“Yangiliklar” bo'limini qo'shamiz: ro'yxat 5 tadan sahifalanadi, view'lar klass ko'rinishida.",
        "10-oyda: EduCenter — kurslar, ariza, kabinet, qidiruv.",
        "get_object_or_404 qanday ishlaydi?",
        "Generic class-based views: ListView, DetailView; queryset va paginate_by; page_obj; app_name va namespace ({% url 'news:list' %}); shablon nomlari konvensiyasi.",
        "Yangilik sahifasiga “Oldingi / keyingi” havolalarini qo'shing.",
        [("📰", "Post", "model", ""),
         ("🧩", "ListView", "paginate_by = 5", "mem"),
         ("📄", "page_obj", "?page=2", ""),
         ("🔗", "news:detail", "namespace", "")],
        [
            step("news/models.py", "Post modeli", lines(NEWS_MODELS, "class Post(models.Model):", '        return reverse("news:detail", args=[self.slug])'),
                 [("startapp news", "yangiliklar alohida app — kurslardan mustaqil."),
                  ('ordering = ["-created"]', "minus — eng yangisi birinchi."),
                  ("news:detail", "app_name bilan nom — boshqa app'dagi “detail” bilan to'qnashmaydi.")],
                 "makemigrations news → 0001_initial"),
            step("news/views.py · news/urls.py", "Class-based views", NEWS_VIEWS.split("\n\n\n", 1)[1].strip("\n") + "\n\n" + lines(NEWS_URLS, 'app_name = "news"', "]"),
                 [("ListView", "ro'yxat, sahifalash va shablon — tayyor; 10-oydagi funksiyadan qisqa."),
                  ("paginate_by", "har sahifada 5 ta."),
                  ("as_view()", "klassni URL uchun funksiyaga aylantiradi."),
                  ("shablon", "news/post_list.html — nom konvensiyadan.")],
                 "/yangiliklar/ → 5 ta yangilik"),
            step("templates/news/post_list.html", "Sahifalash", lines(POST_LIST, "    {% if page_obj.has_other_pages %}", "    {% endif %}"),
                 [("page_obj", "joriy sahifa: number, has_next, has_previous."),
                  ("?page=2", "GET parametri — ListView o'zi o'qiydi."),
                  ("aria-label", "ekran o'quvchi “Sahifalar” deb o'qiydi.")],
                 "← Oldingi · 2 / 2"),
        ],
        files(25),
        tree(25, [("news/migrations/0001_initial.py", "yangi")]),
        ["ListView va DetailView", "paginate_by va page_obj", "app_name va namespace", "Shablon nomlari konvensiyasi"],
        ["Majburiy: yangilik sahifasiga “Oldingi / keyingi” havolalari.",
         "Qo'shimcha: bosh sahifada oxirgi 2 ta yangilikni chiqaring."],
        "11.2 · Testlar va sozlamalar (.env).",
        preview=preview(25, "/yangiliklar/", ["5 tadan keyin “Keyingi →” chiqdimi?", "Nashr qilinmagan yangilik ko'rinmadimi?"]),
    ),
    "WB26": lesson(
        M, 2, "Testlar va sozlamalar (.env)",
        "Saytni avtomatik testlar bilan himoya qilamiz va maxfiy sozlamalarni koddan .env ga olamiz.",
        "O'tgan darsda: ListView va sahifalash.",
        "paginate_by nima qiladi?",
        "TestCase, setUpTestData, self.client, assertContains, assertRedirects; test bazasi alohida; python-dotenv; os.environ; DEBUG va ALLOWED_HOSTS; STATIC_ROOT va collectstatic.",
        "Kurs sahifasi uchun yana 2 ta test yozing.",
        [("🔐", ".env", "SECRET_KEY, DEBUG", "mem"),
         ("⚙", "settings.py", "os.environ", ""),
         ("🧪", "tests.py", "TestCase", ""),
         ("✅", "manage.py test", "OK", "")],
        [
            step(".env.example · config/settings.py", "Sozlamalar muhitdan", env_example(26).strip("\n") + "\n\n" + '''import os
from pathlib import Path

from dotenv import load_dotenv''' + "\n" + '''load_dotenv(BASE_DIR / ".env")''' + "\n\n" + '''SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "0") == "1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")''',
                 [('os.environ["SECRET_KEY"]', "kalit bo'lmasa sayt umuman ishga tushmaydi — xato darhol ko'rinadi."),
                  ('"0" == standart', "unutib qo'yilsa ham serverda DEBUG o'chiq qoladi."),
                  (".env.example", "Git'da faqat namuna; haqiqiy .env — .gitignore'da.")],
                 "pip install python-dotenv"),
            step("courses/tests.py", "Birinchi testlar", lines(tests_py(26), "class CourseViewsTests(TestCase):", '        self.assertEqual(Enrollment.objects.get().name, "Vali")'),
                 [("setUpTestData", "ma'lumot bir marta yaratiladi — testlar tez."),
                  ("self.client", "brauzer o'rnida so'rov yuboradi."),
                  ("alohida baza", "testlar haqiqiy ma'lumotga tegmaydi.")],
                 "4 ta test"),
            step("Terminal", "Ishga tushirish", '''(.venv) $ cp .env.example .env
(.venv) $ python manage.py test
Creating test database for alias 'default'...
....
----------------------------------------------------------------------
Ran 4 tests in 0.412s

OK''',
                 [("....", "har nuqta — o'tgan test; F — yiqilgan."),
                  ("har o'zgarishdan keyin", "testlar eski funksiyalar buzilmaganini isbotlaydi.")],
                 "Ran 4 tests · OK"),
        ],
        files(26),
        tree(26),
        ["TestCase va self.client", "assertContains, assertRedirects", ".env va python-dotenv", "DEBUG, ALLOWED_HOSTS, STATIC_ROOT"],
        ["Majburiy: kurs sahifasi uchun yana 2 ta test.",
         "Qo'shimcha: yangiliklar uchun test (nashr qilinmagani ko'rinmaydi)."],
        "11.3 · Gunicorn va systemd.",
    ),
    "WB27": lesson(
        M, 3, "Gunicorn va systemd",
        "EduCenter'ni VPS'ga joylaymiz: gunicorn ishga tushiradi, systemd 24/7 kuzatadi.",
        "8-oyda: VPS, SSH, systemd (QuizBot). O'tgan darsda: .env va testlar.",
        "runserver serverda nega ishlatilmaydi?",
        "WSGI va gunicorn (workers); collectstatic; .env serverda; educenter.service: User, EnvironmentFile, ExecStart, Restart; journalctl.",
        "Xizmat loglarini journalctl bilan ko'rib, xato bo'lsa tuzating.",
        [("🐙", "git clone", "server", ""),
         ("🦄", "gunicorn", "3 worker", "mem"),
         ("⚙", "systemd", "educenter.service", ""),
         ("📜", "journalctl", "loglar", "")],
        [
            step("Terminal", "Serverga joylash", '''$ ssh edu@203.0.113.10
edu@vps:~$ git clone https://github.com/ali/educenter.git && cd educenter
edu@vps:~/educenter$ python3 -m venv .venv
edu@vps:~/educenter$ .venv/bin/pip install -r requirements.txt
edu@vps:~/educenter$ cp .env.example .env && nano .env   # DEBUG=0, kuchli SECRET_KEY
edu@vps:~/educenter$ .venv/bin/python manage.py migrate
edu@vps:~/educenter$ .venv/bin/python manage.py collectstatic --noinput
edu@vps:~/educenter$ .venv/bin/python manage.py createsuperuser''',
                 [("203.0.113.10", "namuna IP — o'quv VPS'ingiz manzili."),
                  ("SECRET_KEY", "python -c \"import secrets; print(secrets.token_urlsafe(50))\""),
                  ("collectstatic", "CSS va admin fayllari staticfiles/ ga yig'iladi.")],
                 "staticfiles/ — 128 ta fayl"),
            step("deploy/educenter.service", "systemd xizmati", SERVICE.strip("\n"),
                 [("gunicorn", "ishlab chiqarish serveri; runserver — faqat dars uchun."),
                  ("--workers 3", "bir vaqtda 3 ta so'rov."),
                  ("127.0.0.1:8000", "tashqaridan yopiq — oldida Nginx turadi (keyingi dars)."),
                  ("EnvironmentFile", ".env dagi qiymatlar xizmatga.")],
                 "/etc/systemd/system/educenter.service"),
            step("Terminal", "Ishga tushirish va kuzatish", '''$ sudo cp deploy/educenter.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now educenter
$ systemctl status educenter
● educenter.service - EduCenter Django sayti (gunicorn)
     Active: active (running)
$ curl -I http://127.0.0.1:8000/
HTTP/1.1 200 OK
$ journalctl -u educenter -f''',
                 [("enable --now", "hozir va server qayta yoqilganda ham."),
                  ("curl -I", "faqat javob sarlavhalari — sayt javob beryaptimi."),
                  ("journalctl -f", "xatolar jonli.")],
                 "active (running) · 200 OK"),
        ],
        files(27),
        tree(27, [("staticfiles/", "yangi")]),
        ["WSGI va gunicorn", "collectstatic", "systemd xizmati", "journalctl va curl -I"],
        ["Majburiy: journalctl bilan loglarni ko'rib chiqing.",
         "Qo'shimcha: workers sonini CPU yadrolari bo'yicha hisoblang (2 × yadro + 1)."],
        "11.4 · Nginx, domen va HTTPS.",
    ),
    "WB28": lesson(
        M, 4, "Nginx, domen va HTTPS",
        "Nginx'ni gunicorn oldiga qo'yamiz, domen ulaymiz va bepul HTTPS sertifikat olamiz.",
        "O'tgan darsda: gunicorn va systemd.",
        "Nega gunicorn 127.0.0.1 da tinglaydi?",
        "Reverse proxy; static va media'ni Nginx beradi; X-Forwarded-Proto; DNS A yozuvi; certbot (Let's Encrypt); xavfsizlik sozlamalari: SECURE_*, HSTS, CSRF_TRUSTED_ORIGINS; check --deploy.",
        "Saytni telefoningizdan HTTPS bilan oching.",
        [("🌍", "educenter.example.com", "DNS", ""),
         ("🛡", "Nginx :443", "HTTPS", "mem"),
         ("📁", "/static/", "fayl to'g'ridan", ""),
         ("🦄", "gunicorn :8000", "Django", "")],
        [
            step("deploy/nginx.conf", "Nginx sayt sozlamasi", NGINX.strip("\n"),
                 [("alias", "static va media'ni Nginx o'zi beradi — Django'dan tez."),
                  ("proxy_pass", "qolgan so'rovlar gunicorn'ga."),
                  ("X-Forwarded-Proto", "Django so'rov https bo'lganini shundan biladi."),
                  ("client_max_body_size", "10 MB gacha rasm yuklash.")],
                 "/etc/nginx/sites-available/educenter"),
            step("config/settings.py", "Xavfsizlik sozlamalari", lines(S, "if not DEBUG:", "    SECURE_HSTS_SECONDS = 3600") + "\n" + 'CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]',
                 [("SSL_REDIRECT", "http → https."),
                  ("COOKIE_SECURE", "sessiya cookie faqat HTTPS orqali."),
                  ("HSTS", "brauzer bu saytga faqat HTTPS bilan kiradi."),
                  ("3600", "HSTS'ni 1 soatdan boshlaymiz: HTTPS barqaror ishlagach oshiramiz."),
                  ("testlarda", "@override_settings(SECURE_SSL_REDIRECT=False).")],
                 "check --deploy → faqat W005, W021 (ongli)"),
            step("Terminal", "Yoqish va sertifikat", '''$ sudo cp deploy/nginx.conf /etc/nginx/sites-available/educenter
$ sudo ln -s /etc/nginx/sites-available/educenter /etc/nginx/sites-enabled/
$ sudo nginx -t
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ sudo systemctl reload nginx
$ sudo ufw allow "Nginx Full"
$ sudo certbot --nginx -d educenter.example.com
Successfully deployed certificate
$ .venv/bin/python manage.py check --deploy''',
                 [("nginx -t", "har o'zgarishdan keyin — xato bo'lsa reload qilinmaydi."),
                  ("Nginx Full", "80 va 443-portlar ochiladi."),
                  ("certbot", "sertifikat va 443 sozlamasini o'zi qo'shadi, 90 kunda yangilaydi.")],
                 "🔒 https://educenter.example.com"),
        ],
        files(28),
        tree(28),
        ["Reverse proxy va Nginx", "static/media'ni Nginx beradi", "DNS va certbot", "SECURE_* va check --deploy"],
        ["Majburiy: saytni telefondan HTTPS bilan oching.",
         "Qo'shimcha: 404.html va 500.html sahifalarini yarating."],
        "11.5 · API: JSON qaytarish.",
    ),
    "WB29": lesson(
        M, 5, "API: JSON qaytarish",
        "Kurslar ro'yxatini JSON ko'rinishida beramiz — bot va boshqa dasturlar ishlatishi uchun.",
        "O'tgan darsda: Nginx va HTTPS.",
        "Nima uchun HSTS kerak?",
        "API va JSON; JsonResponse; ensure_ascii=False; build_absolute_uri; select_related; API testlari.",
        "API'ga ?category= filtri qo'shing.",
        [("🤖", "Bot / dastur", "GET /api/courses/", ""),
         ("🧠", "api_courses", "QuerySet → list", "mem"),
         ("📦", "JsonResponse", '{"courses": [...]}', ""),
         ("🧪", "test", ".json()", "")],
        [
            step("courses/views.py", "JSON view", lines(V, "def api_courses(request):", '    return JsonResponse({"courses": data}, json_dumps_params={"ensure_ascii": False})'),
                 [("lug'atlar ro'yxati", "faqat kerakli maydonlar — ichki ma'lumot chiqmaydi."),
                  ("build_absolute_uri", "to'liq manzil: https://educenter.example.com/kurslar/..."),
                  ("ensure_ascii=False", "o'zbekcha harflar \\u kodlarsiz.")],
                 '{"courses": [{"title": "Python asoslari", ...}]}'),
            step("courses/urls.py · courses/tests.py", "URL va test", '''    path("api/courses/", views.api_courses, name="api_courses"),''' + "\n\n" + lines(tests_py(29), "    def test_api_returns_active_courses(self):", '        self.assertEqual(data["courses"][0]["url"], "http://testserver/kurslar/python-asoslari/")'),
                 [(".json()", "javobni Python lug'atiga aylantiradi."),
                  ("nofaol kurs", "API'da ham ko'rinmaydi — test isbotlaydi.")],
                 "Ran 5 tests · OK"),
            step("Terminal", "Tekshirish", '''$ curl -s https://educenter.example.com/api/courses/ | python3 -m json.tool
{
    "courses": [
        {
            "title": "Python asoslari",
            "slug": "python-asoslari",
            "price": 450000,
            "months": 3,
            "category": "Dasturlash",
            "url": "https://educenter.example.com/kurslar/python-asoslari/"
        }
    ]
}''',
                 [("json.tool", "JSON'ni chiroyli ko'rsatadi."),
                  ("keyingi darslar", "bot shu API'dan foydalanadi.")],
                 "200 · application/json"),
        ],
        files(29),
        tree(29),
        ["API va JSON", "JsonResponse va ensure_ascii", "build_absolute_uri", "API testlari"],
        ["Majburiy: API'ga ?category= filtri.",
         "Qo'shimcha: /api/courses/<slug>/ — bitta kurs."],
        "11.6 · Integratsiya: sayt → bot.",
        preview=preview(29, "/api/courses/", ["Brauzerda JSON ochildimi?", "O'zbekcha harflar to'g'ri chiqdimi?"]),
    ),
    "WB30": lesson(
        M, 6, "Integratsiya: sayt → bot",
        "Saytda yangi ariza tushsa, admin darhol Telegram'da xabar oladi.",
        "8-oyda: bot xatolarni admin'ga yuborardi. O'tgan darsda: JSON API.",
        "JsonResponse nima qaytaradi?",
        "Telegram Bot API (sendMessage) — oddiy HTTPS so'rov; urllib.request; timeout; xato bo'lsa sayt to'xtamasligi; logging; testlarda mock (patch).",
        "Xabarga kurs narxi va ariza vaqtini qo'shing.",
        [("📝", "Ariza", "form.save()", ""),
         ("📤", "notify_admin", "HTTPS POST", "mem"),
         ("🤖", "api.telegram.org", "sendMessage", ""),
         ("📱", "Admin", "xabar", "")],
        [
            step("courses/telegram.py", "Telegram'ga xabar", lines(TELEGRAM, "def notify_admin(text: str) -> bool:", "        return False"),
                 [("token yo'q", "lokal kompyuterda xabar yuborilmaydi — False."),
                  ("timeout=5", "Telegram sekin bo'lsa sayt kutib qolmaydi."),
                  ("except OSError", "tarmoq xatosi — ariza baribir saqlangan, faqat log.")],
                 "notify_admin() → True"),
            step("courses/views.py · config/settings.py", "Ulash", '''        enrollment.save()
        notify_admin(f"🆕 Yangi ariza: {course.title}\\n👤 {enrollment.name}\\n📞 {enrollment.phone}")''' + "\n\n" + '''TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_ID = os.environ.get("TELEGRAM_ADMIN_ID", "")''',
                 [("save() dan keyin", "avval ariza bazaga yoziladi, keyin xabar."),
                  (".env", "token kodda emas — serverdagi .env da."),
                  ("kelajakda", "ko'p xabar bo'lsa — navbat (Celery).")],
                 "admin'ga xabar ketdi"),
            step("courses/tests.py", "Mock bilan test", lines(T, '    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_ADMIN_ID="7")', '            self.assertFalse(notify_admin("x"))'),
                 [("patch", "testda haqiqiy Telegram'ga so'rov ketmaydi."),
                  ("side_effect", "tarmoq xatosini sun'iy yaratamiz."),
                  ("assertLogs", "xato log'ga yozilganini tekshiradi.")],
                 "Ran 7 tests · OK"),
        ],
        files(30),
        tree(30),
        ["Telegram Bot API", "urllib.request va timeout", "Xatoga chidamlilik va logging", "unittest.mock.patch"],
        ["Majburiy: xabarga narx va ariza vaqtini qo'shing.",
         "Qo'shimcha: xabarga admin'dagi ariza sahifasi havolasini qo'shing."],
        "11.7 · Integratsiya: bot → sayt.",
        chat=[("bot", "🆕 Yangi ariza: Python asoslari\n👤 Vali\n📞 +998 90 123 45 67"),
              ("bot", "🆕 Yangi ariza: Telegram bot\n👤 Ali\n📞 +998 90 111 22 33")],
        chat_title="Admin Telegram'da", chat_sub="saytda forma yuborilgan zahoti",
        checks=["Saytda ariza yuborilgach admin'ga xabar keldimi?", "Token noto'g'ri bo'lsa ham ariza saqlandimi?"],
    ),
    "WB31": lesson(
        M, 7, "Integratsiya: bot → sayt",
        "QuizBot'ga /kurslar buyrug'ini qo'shamiz — u saytdagi API'dan kurslarni oladi.",
        "6–8-oylarda: QuizBot. O'tgan darsda: sayt → bot.",
        "notify_admin xato bo'lsa nima qiladi?",
        "aiohttp — asinxron HTTP; ClientSession va timeout; raise_for_status; xatolarni ushlash; SITE_URL — .env da; yangi router ulash.",
        "Har kurs ostiga “Saytda ochish” tugmasini qo'shing (InlineKeyboardButton url=).",
        [("👤", "/kurslar", "foydalanuvchi", ""),
         ("🤖", "QuizBot", "aiohttp GET", "mem"),
         ("🌐", "EduCenter API", "JSON", ""),
         ("💬", "Javob", "kurslar ro'yxati", "")],
        [
            step("quizbot/handlers/courses.py", "API'dan kurslar", lines(BOT_COURSES, "async def fetch_courses() -> list[dict]:", '    return data["courses"]'),
                 [("aiohttp", "aiogram bilan birga o'rnatilgan — bot to'xtab qolmaydi (async)."),
                  ("timeout", "sayt javob bermasa 5 soniyada voz kechadi."),
                  ("raise_for_status", "404 yoki 500 bo'lsa xato.")],
                 "fetch_courses() → 4 ta kurs"),
            step("quizbot/handlers/courses.py", "/kurslar buyrug'i", lines(BOT_COURSES, '@router.message(Command("kurslar"))', '    await message.answer("EduCenter kurslari:\\n\\n" + "\\n".join(lines))'),
                 [("except", "sayt o'chiq bo'lsa ham bot tushunarli javob beradi."),
                  (":,", "450000 → 450 000 (minglik ajratish).")],
                 "📚 Python asoslari — 450 000 so'm · 3 oy"),
            step("quizbot/config.py · quizbot/bot.py", "Ulash", '''SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")''' + "\n\n" + '''from handlers import admin, courses, errors, menu, quiz, rating, register, settings, start''' + "\n" + '''        courses.router,''',
                 [("SITE_URL", "botning .env faylida: SITE_URL=https://educenter.example.com."),
                  ("router tartibi", "menu/quiz'dan oldin — buyruq boshqa handlerga tushib qolmaydi.")],
                 "/kurslar ishlaydi"),
        ],
        files(31),
        tree(31),
        ["aiohttp va ClientSession", "timeout va raise_for_status", "Xatoga chidamli bot", "Yangi router ulash"],
        ["Majburiy: har kursga “Saytda ochish” tugmasi.",
         "Qo'shimcha: /kurslar natijasini 5 daqiqa keshlang."],
        "11.8 · Yakuniy loyiha: g'oya va reja.",
        chat=[("user", "/kurslar"),
              ("bot", "EduCenter kurslari:\n\n📚 Kompyuter savodxonligi — 300 000 so'm · 2 oy\n📚 Python asoslari — 450 000 so'm · 3 oy\n📚 Telegram bot — 550 000 so'm · 3 oy\n📚 Web dasturlash — 650 000 so'm · 3 oy")],
        chat_title="Sinab ko'ramiz", chat_sub="bot saytning API'sidan oladi",
        checks=["Admin'da yangi kurs qo'shilsa bot'da ham chiqdimi?", "Sayt o'chiq bo'lsa bot tushunarli javob berdimi?"],
    ),
    "WB32": lesson(
        M, 8, "Yakuniy loyiha: g'oya va reja",
        "Har o'quvchi o'z yakuniy loyihasini tanlaydi va bir sahifalik reja yozadi.",
        "11-oyda: EduCenter serverda, API, sayt ↔ bot.",
        "EduCenter'da qaysi modellar bor edi?",
        "Muammo → foydalanuvchi → MVP; modellar va sahifalar ro'yxati; 3 kunlik jadval; GitHub Issues bilan vazifalar.",
        "Loyiha rejasini README'ga yozing.",
        [("❓", "Muammo", "kimga kerak?", ""),
         ("🎯", "MVP", "4 ta funksiya", "mem"),
         ("🗃", "Modellar", "Book, Loan", ""),
         ("📅", "Jadval", "3 kun", "")],
        [
            step("PLAN.md", "Muammo va foydalanuvchilar", lines(PLAN, "## Muammo", "- Kutubxonachi: kitob beradi va qaytarib oladi"),
                 [("muammo", "bir jumlada, real hayotdan."),
                  ("foydalanuvchilar", "har biri nima qiladi — sahifalar shundan chiqadi.")],
                 "2 xil foydalanuvchi"),
            step("PLAN.md", "MVP va modellar", lines(PLAN, "## MVP — birinchi versiya", "- Loan: book, user, taken, returned"),
                 [("MVP", "eng kichik ishlaydigan versiya — qolgani keyin."),
                  ("modellar", "10-oydagi Course va Enrollment'ga o'xshash.")],
                 "4 funksiya · 2 model"),
            step("PLAN.md", "Jadval", lines(PLAN, "## Jadval", "| 3 | Testlar, serverga joylash |"),
                 [("3 kun", "WB33 ish kuni, WB34 joylash, WB36 himoya."),
                  ("GitHub Issues", "har qator — alohida issue.")],
                 "reja tayyor"),
        ],
        files(32),
        tree(32),
        ["Muammo va foydalanuvchi", "MVP", "Modellar va sahifalar", "Jadval va Issues"],
        ["Majburiy: reja README'da.",
         "Qo'shimcha: har MVP funksiyasi uchun GitHub Issue oching."],
        "11.9 · Yakuniy loyiha: ishlash kuni.",
    ),
    "WB33": lesson(
        M, 9, "Yakuniy loyiha: ishlash kuni",
        "Professional jarayonni bir funksiya misolida o'tamiz: issue → branch → test → kod → PR. Namuna: kurslarni kategoriya bo'yicha filtrlash.",
        "O'tgan darsda: loyiha rejasi.",
        "MVP nima?",
        "Branch va PR; avval test (TDD); GET filtr va isdigit(); select va selected; kichik commitlar.",
        "Asosiy funksiyalardan birini shu jarayon bilan tugating.",
        [("📌", "Issue #7", "kategoriya filtri", ""),
         ("🌿", "branch", "feature/category-filter", ""),
         ("🧪", "test", "avval yiqiladi", "mem"),
         ("✅", "kod", "test o'tadi → PR", "")],
        [
            step("courses/tests.py", "Avval test", lines(T, "    def test_list_filters_by_category(self):", '        self.assertNotContains(response, "Python asoslari")'),
                 [("git switch -c feature/category-filter", "har funksiya — alohida branch."),
                  ("avval test", "kutilgan natijani yozamiz; hozircha yiqiladi (F)."),
                  ("web.pk", "kategoriya ID'si GET parametrida.")],
                 "FAIL: test_list_filters_by_category"),
            step("courses/views.py", "Kod", lines(V, '    category = request.GET.get("category", "")', '    return render(request, "courses/course_list.html", context)'),
                 [("isdigit()", "?category=abc kelsa xato emas — e'tiborsiz."),
                  ("category_id", "ForeignKey ustunining o'zi — qo'shimcha JOIN yo'q."),
                  ("context", "uzun qatorni o'zgaruvchiga olib, o'qishni osonlashtiramiz.")],
                 "Ran 8 tests · OK"),
            step("templates/courses/course_list.html", "Tanlash maydoni", lines(project(33)["templates/courses/course_list.html"], '      <select name="category" aria-label="Kategoriya">', "      </select>"),
                 [("selected", "tanlangan kategoriya sahifa yangilanganda saqlanadi."),
                  ("stringformat:\"d\"", "son va matnni solishtirish uchun."),
                  ("git push → PR", "Closes #7 — issue o'zi yopiladi.")],
                 "[Dasturlash ▾] [Qidirish]"),
        ],
        files(33),
        tree(33),
        ["Issue → branch → PR", "Avval test (TDD)", "GET filtr va isdigit", "select va selected"],
        ["Majburiy: loyihangizning bitta funksiyasini shu jarayon bilan tugating.",
         "Qo'shimcha: qidiruv va kategoriya birga ishlashini test bilan isbotlang."],
        "11.10 · Yakuniy loyiha: kod tahlili va joylash.",
        preview=preview(33, "/kurslar/?category=1", ["Kategoriya tanlanganda faqat o'sha kurslar chiqdimi?", "Tanlov sahifa yangilanganda saqlandimi?"]),
    ),
    "WB34": lesson(
        M, 10, "Yakuniy loyiha: kod tahlili va joylash",
        "Bir-birimizning kodimizni ro'yxat bo'yicha tahlil qilamiz va bir buyruq bilan serverni yangilaymiz.",
        "O'tgan darsda: issue → branch → test → PR.",
        "Nega avval test yozdik?",
        "Code review madaniyati; tekshiruv ro'yxati; deploy skript: set -euo pipefail, testdan keyin migrate, collectstatic, restart; xato bo'lsa eski versiya ishlayveradi.",
        "Loyihani serverga joylab, havolasini yuboring.",
        [("👀", "Review", "REVIEW.md", ""),
         ("⬇", "git pull", "--ff-only", ""),
         ("🧪", "test", "yiqilsa — to'xta", "mem"),
         ("🔄", "restart", "yangi versiya", "")],
        [
            step("REVIEW.md", "Tekshiruv ro'yxati", lines(REVIEW, "## Xavfsizlik", "- [ ] Har POST formada `{% csrf_token %}`"),
                 [("ro'yxat", "hamma bir xil mezon bilan tekshiradi."),
                  ("odob", "kodni tanqid qilamiz, odamni emas; taklif bilan.")],
                 "PR'da 3 ta izoh"),
            step("deploy/deploy.sh", "Bir buyruq bilan yangilash", DEPLOY.strip("\n"),
                 [("set -euo pipefail", "biror qadam yiqilsa skript to'xtaydi."),
                  ("test → migrate", "testlar yiqilsa baza ham o'zgarmaydi, eski sayt ishlayveradi."),
                  ("is-active", "restart'dan keyin xizmat haqiqatan ishlayaptimi.")],
                 "✅ Yangilandi: a1b2c3d Kategoriya filtri"),
            step("Terminal", "Ishga tushirish", '''edu@vps:~/educenter$ chmod +x deploy/deploy.sh
edu@vps:~/educenter$ ./deploy/deploy.sh
Ran 8 tests in 0.6s
OK
Operations to perform: ... No migrations to apply.
128 static files copied to '/home/edu/educenter/staticfiles'.
✅ Yangilandi: a1b2c3d Kategoriya filtri''',
                 [("8-oydagi deploy.sh", "xuddi shu g'oya — endi Django uchun."),
                  ("har PR'dan keyin", "bir buyruq — xatosiz va tez.")],
                 "sayt yangilandi"),
        ],
        files(34),
        tree(34),
        ["Code review madaniyati", "Tekshiruv ro'yxati", "deploy.sh: test → migrate → restart", "set -euo pipefail"],
        ["Majburiy: loyihani serverga joylab, havolani yuboring.",
         "Qo'shimcha: deploy.sh'ga zaxira nusxa qadamini qo'shing (8-oydagi backup.sh)."],
        "11.11 · Taqdimotga tayyorgarlik: portfolio va rezyume.",
    ),
    "WB35": lesson(
        M, 11, "Taqdimotga tayyorgarlik: portfolio va rezyume",
        "Portfolio saytiga EduCenter va QuizBot'ni qo'shamiz va bir sahifalik rezyume yozamiz.",
        "9-oyda: Portfolio sayti. 6–11-oylarda: QuizBot va EduCenter.",
        "deploy.sh da nega test migrate'dan oldin?",
        "Portfolio — eng yaxshi 3 loyiha; havolalar va qisqa tavsif; rezyume tuzilmasi: loyihalar, ko'nikmalar, ta'lim; GitHub profil README.",
        "Portfolio saytingizga bot va EduCenter havolalarini qo'shing.",
        [("🗂", "Portfolio", "3 loyiha", ""),
         ("🔗", "Havolalar", "jonli + GitHub", "mem"),
         ("📄", "RESUME.md", "1 sahifa", ""),
         ("🐙", "GitHub", "pinned", "")],
        [
            step("portfolio/script.js", "Loyihalar ro'yxati", lines(PORTFOLIO_JS, "const projects = [", "];"),
                 [("url", "har loyihada jonli havola yoki GitHub."),
                  ("tags", "9-oydagi filtr tugmalari shu bilan ishlaydi."),
                  ("tartib", "eng kuchli loyiha birinchi.")],
                 "[Web] → EduCenter, Portfolio"),
            step("portfolio/script.js", "Havola kartada", '''    .map((p) => `<article class="card"><h3>${p.title}</h3><p>${p.text}</p><a href="${p.url}">Ko'rish →</a></article>`)''',
                 [("shablon satr", "9-oydagi map + join."),
                  ("git push", "GitHub Pages bir daqiqada yangilanadi.")],
                 "Ko'rish → https://educenter.example.com"),
            step("RESUME.md", "Rezyume", lines(RESUME, "## Loyihalar", "Python · Django · aiogram 3 · SQL/SQLite · HTML/CSS/JS · Git/GitHub · Linux, Nginx, systemd"),
                 [("loyihalar birinchi", "junior uchun eng kuchli dalil — ishlaydigan loyiha."),
                  ("har loyiha", "nima va qaysi texnologiya — bir qatorda."),
                  ("PDF", "rezyumeni PDF qilib yuborasiz.")],
                 "1 sahifa"),
        ],
        files(35),
        tree(35),
        ["Portfolio: eng yaxshi 3 loyiha", "Havolalar va tavsif", "Rezyume tuzilmasi", "GitHub profil"],
        ["Majburiy: portfolio'ga bot va EduCenter havolalari.",
         "Qo'shimcha: GitHub profil README yozing va 3 loyihani pin qiling."],
        "11.12 · DEMO DAY: himoya va sertifikat.",
        preview=preview(35, "/", ["Portfolio'da EduCenter va QuizBot kartalari chiqdimi?", "“Ko'rish →” havolalari ishladimi?"], url="https://ali.github.io"),
    ),
    "WB36": lesson(
        M, 12, "DEMO DAY: himoya va sertifikat",
        "11 oylik yo'lning yakuni: yakuniy loyiha himoyasi, baholash va sertifikat.",
        "11 oyda: Python → Telegram bot → Portfolio → Django → server va integratsiya.",
        "Demo nimadan boshlanadi?",
        "5 daqiqalik demo ssenariysi; baholash mezonlari; oxirgi tekshiruv; savollarga javob; keyingi qadamlar.",
        "Tabriklaymiz! Loyihangizni rivojlantirishda davom eting.",
        [("🎤", "Demo", "5 daqiqa", ""),
         ("❓", "Savollar", "halol javob", ""),
         ("🏆", "Baholash", "100 ball", "mem"),
         ("🎓", "Sertifikat", "Minar Dasturchi", "")],
        [
            step("DEMO_DAY.md", "Ssenariy", lines(DEMO_DAY, "## Ssenariy", "5. Keyingi qadamlar (30 s)"),
                 [("muammodan boshlang", "kod emas — kimga va nima uchun."),
                  ("jonli demo", "internetdagi sayt — lokal emas.")],
                 "5 daqiqa"),
            step("DEMO_DAY.md", "Baholash", lines(DEMO_DAY, "## Baholash", "| README va GitHub | 10 |"),
                 [("40 ball", "ishlashi — HTTPS bilan internetda."),
                  ("30 ball", "testlar va toza kod.")],
                 "100 ball"),
            step("Terminal", "Oxirgi tekshiruv", '''$ curl -sI https://educenter.example.com | head -1
HTTP/2 200
edu@vps:~/educenter$ .venv/bin/python manage.py test
Ran 8 tests in 0.6s
OK
edu@vps:~/educenter$ .venv/bin/python manage.py check --deploy
?: (security.W005) ... SECURE_HSTS_INCLUDE_SUBDOMAINS ...
?: (security.W021) ... SECURE_HSTS_PRELOAD ...
System check identified 2 issues (0 silenced).''',
                 [("HTTP/2 200", "sayt HTTPS bilan ishlayapti."),
                  ("W005, W021", "ongli qaror: subdomen va preload — HSTS 1 yilga oshirilgandan keyin."),
                  ("keyin", "loyihani rivojlantiring, yangi texnologiyalar: DRF, Celery, Docker.")],
                 "🎓 Tabriklaymiz!"),
        ],
        files(36),
        tree(36),
        ["Demo ssenariysi", "Baholash mezonlari", "Oxirgi tekshiruv", "Keyingi qadamlar"],
        ["Tabriklaymiz! Loyihangizni rivojlantirishda davom eting.",
         "Qo'shimcha: loyihangizni do'stlaringizga ko'rsatib, fikr so'rang."],
        "Minar Dasturchi kursi yakunlandi.",
        preview=preview(36, "/", ["Sayt HTTPS bilan ochildimi?", "Hamma bo'limlar (kurslar, yangiliklar, kabinet) ishladimi?"], url="https://educenter.example.com"),
    ),
}
