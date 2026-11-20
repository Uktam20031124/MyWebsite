"""Dasturchi 10-oy · 2-sayt: EduCenter (Django) — WB13–WB24 "Dars kodi".

Loyiha fayllari ``project(n)`` dan bosqichma-bosqich yig'iladi; dars "files" — shu darsda yangi yoki o'zgargan fayllar.
Har bosqich vaqtinchalik Django loyihasida yig'ilib (startproject/startapp + fayllar), check, makemigrations,
migrate va test client bilan tekshirilgan; "Brauzerda natija" — runserver'dagi haqiqiy skrinshot.
"""

from .lesson_kit import lesson, step

M = "10-oy · 2-sayt: EduCenter (Django)"


def pick(n: int, rows: list) -> str:
    """Qatorlar: "matn" — doim; (s, "matn") — n >= s; (s, e, "matn") — s <= n < e."""
    out = []
    for r in rows:
        if isinstance(r, str):
            out.append(r)
        elif len(r) == 2 and n >= r[0]:
            out.append(r[1])
        elif len(r) == 3 and r[0] <= n < r[1]:
            out.append(r[2])
    return "\n".join(out) + "\n"


GITIGNORE = """.venv/
__pycache__/
db.sqlite3
media/
.env
"""


def requirements(n):
    return pick(n, ["Django>=5.2,<6.0", (20, "Pillow>=11.0")])


def settings_py(n):
    return pick(n, [
        "from pathlib import Path",
        "",
        "BASE_DIR = Path(__file__).resolve().parent.parent",
        "",
        'SECRET_KEY = "django-insecure-faqat-dars-uchun"',
        "DEBUG = True",
        "ALLOWED_HOSTS = []",
        "",
        "INSTALLED_APPS = [",
        '    "django.contrib.admin",',
        '    "django.contrib.auth",',
        '    "django.contrib.contenttypes",',
        '    "django.contrib.sessions",',
        '    "django.contrib.messages",',
        '    "django.contrib.staticfiles",',
        (14, '    "courses",'),
        (22, '    "accounts",'),
        "]",
        "",
        "MIDDLEWARE = [",
        '    "django.middleware.security.SecurityMiddleware",',
        '    "django.contrib.sessions.middleware.SessionMiddleware",',
        '    "django.middleware.common.CommonMiddleware",',
        '    "django.middleware.csrf.CsrfViewMiddleware",',
        '    "django.contrib.auth.middleware.AuthenticationMiddleware",',
        '    "django.contrib.messages.middleware.MessageMiddleware",',
        '    "django.middleware.clickjacking.XFrameOptionsMiddleware",',
        "]",
        "",
        'ROOT_URLCONF = "config.urls"',
        "",
        "TEMPLATES = [",
        "    {",
        '        "BACKEND": "django.template.backends.django.DjangoTemplates",',
        (13, 14, '        "DIRS": [],'),
        (14, '        "DIRS": [BASE_DIR / "templates"],'),
        '        "APP_DIRS": True,',
        '        "OPTIONS": {',
        '            "context_processors": [',
        '                "django.template.context_processors.request",',
        '                "django.contrib.auth.context_processors.auth",',
        '                "django.contrib.messages.context_processors.messages",',
        "            ],",
        "        },",
        "    },",
        "]",
        "",
        'WSGI_APPLICATION = "config.wsgi.application"',
        "",
        "DATABASES = {",
        '    "default": {',
        '        "ENGINE": "django.db.backends.sqlite3",',
        '        "NAME": BASE_DIR / "db.sqlite3",',
        "    }",
        "}",
        "",
        "AUTH_PASSWORD_VALIDATORS = [",
        '    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},',
        '    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},',
        '    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},',
        '    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},',
        "]",
        "",
        'LANGUAGE_CODE = "uz"',
        'TIME_ZONE = "Asia/Tashkent"',
        "USE_I18N = True",
        "USE_TZ = True",
        "",
        'STATIC_URL = "static/"',
        (14, 'STATICFILES_DIRS = [BASE_DIR / "static"]'),
        (20, ""),
        (20, 'MEDIA_URL = "media/"'),
        (20, 'MEDIA_ROOT = BASE_DIR / "media"'),
        (22, ""),
        (22, 'LOGIN_URL = "login"'),
        (22, 'LOGIN_REDIRECT_URL = "home"'),
        (22, 'LOGOUT_REDIRECT_URL = "home"'),
        "",
        'DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"',
    ])


def config_urls(n):
    return pick(n, [
        (20, "from django.conf import settings"),
        (20, "from django.conf.urls.static import static"),
        "from django.contrib import admin",
        (13, 14, "from django.urls import path"),
        (14, "from django.urls import include, path"),
        "",
        "urlpatterns = [",
        '    path("admin/", admin.site.urls),',
        (22, '    path("accounts/", include("django.contrib.auth.urls")),'),
        (22, '    path("accounts/", include("accounts.urls")),'),
        (14, '    path("", include("courses.urls")),'),
        "]",
        (20, ""),
        (20, "if settings.DEBUG:"),
        (20, "    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"),
    ])


def courses_urls(n):
    return pick(n, [
        "from django.urls import path",
        "",
        "from . import views",
        "",
        "urlpatterns = [",
        '    path("", views.home, name="home"),',
        (17, '    path("kurslar/", views.course_list, name="course_list"),'),
        (18, '    path("kurslar/<slug:slug>/", views.course_detail, name="course_detail"),'),
        (19, '    path("ustozlar/<int:pk>/", views.teacher_detail, name="teacher_detail"),'),
        "]",
    ])


CATEGORY = '''class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

'''


def models_py(n):
    return pick(n, [
        (23, "from django.conf import settings"),
        "from django.db import models",
        (18, "from django.urls import reverse"),
        "",
        "",
        (19, CATEGORY),
        (19, "class Teacher(models.Model):"),
        (19, "    name = models.CharField(max_length=100)"),
        (19, "    bio = models.TextField(blank=True)"),
        (20, '    photo = models.ImageField(upload_to="teachers/", blank=True)'),
        (19, ""),
        (19, "    def __str__(self):"),
        (19, "        return self.name"),
        (19, ""),
        (19, ""),
        "class Course(models.Model):",
        "    title = models.CharField(max_length=200)",
        "    slug = models.SlugField(max_length=200, unique=True)",
        "    description = models.TextField()",
        (16, "    price = models.PositiveIntegerField(default=0)"),
        (16, "    duration_months = models.PositiveSmallIntegerField(default=3)"),
        "    is_active = models.BooleanField(default=True)",
        (19, '    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="courses")'),
        (19, '    teachers = models.ManyToManyField(Teacher, blank=True, related_name="courses")'),
        (20, '    image = models.ImageField(upload_to="courses/", blank=True)'),
        "    created = models.DateTimeField(auto_now_add=True)",
        "",
        "    class Meta:",
        '        ordering = ["title"]',
        "",
        "    def __str__(self):",
        "        return self.title",
        (18, ""),
        (18, "    def get_absolute_url(self):"),
        (18, '        return reverse("course_detail", args=[self.slug])'),
        (21, ""),
        (21, ""),
        (21, "class Enrollment(models.Model):"),
        (21, '    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")'),
        (23, "    user = models.ForeignKey("),
        (23, '        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="enrollments"'),
        (23, "    )"),
        (21, "    name = models.CharField(max_length=100)"),
        (21, "    phone = models.CharField(max_length=20)"),
        (21, "    created = models.DateTimeField(auto_now_add=True)"),
        (21, ""),
        (21, "    def __str__(self):"),
        (21, '        return f"{self.name} — {self.course}"'),
    ]).replace("\n\n\n\n", "\n\n\n")


def admin_py(n):
    return pick(n, [
        "from django.contrib import admin",
        "",
        (16, 19, "from .models import Course"),
        (19, 21, "from .models import Category, Course, Teacher"),
        (21, "from .models import Category, Course, Enrollment, Teacher"),
        "",
        "",
        "@admin.register(Course)",
        "class CourseAdmin(admin.ModelAdmin):",
        '    list_display = ["title", "price", "duration_months", "is_active"]',
        '    list_editable = ["is_active"]',
        (19, '    list_filter = ["category", "is_active"]'),
        '    search_fields = ["title"]',
        '    prepopulated_fields = {"slug": ["title"]}',
        (19, ""),
        (19, ""),
        (19, "admin.site.register(Category)"),
        (19, "admin.site.register(Teacher)"),
        (21, ""),
        (21, ""),
        (21, "@admin.register(Enrollment)"),
        (21, "class EnrollmentAdmin(admin.ModelAdmin):"),
        (21, '    list_display = ["name", "phone", "course", "created"]'),
        (21, '    list_filter = ["course"]'),
    ])


def views_py(n):
    return pick(n, [
        (21, "from django.contrib import messages"),
        (23, "from django.db.models import Q"),
        (14, 18, "from django.shortcuts import render"),
        (18, 21, "from django.shortcuts import get_object_or_404, render"),
        (21, "from django.shortcuts import get_object_or_404, redirect, render"),
        (17, ""),
        (21, "from .forms import EnrollmentForm"),
        (17, 19, "from .models import Course"),
        (19, "from .models import Course, Teacher"),
        "",
        "",
        "def home(request):",
        (14, 17, '    return render(request, "courses/home.html")'),
        (17, "    courses = Course.objects.filter(is_active=True)[:3]"),
        (17, '    return render(request, "courses/home.html", {"courses": courses})'),
        (17, ""),
        (17, ""),
        (17, "def course_list(request):"),
        (17, "    courses = Course.objects.filter(is_active=True)"),
        (17, 23, '    return render(request, "courses/course_list.html", {"courses": courses})'),
        (23, '    query = request.GET.get("q", "").strip()'),
        (23, "    if query:"),
        (23, "        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))"),
        (23, '    return render(request, "courses/course_list.html", {"courses": courses, "query": query})'),
        (18, ""),
        (18, ""),
        (18, "def course_detail(request, slug):"),
        (18, "    course = get_object_or_404(Course, slug=slug, is_active=True)"),
        (18, 21, '    return render(request, "courses/course_detail.html", {"course": course})'),
        (21, "    form = EnrollmentForm(request.POST or None)"),
        (21, '    if request.method == "POST" and form.is_valid():'),
        (21, "        enrollment = form.save(commit=False)"),
        (21, "        enrollment.course = course"),
        (23, "        if request.user.is_authenticated:"),
        (23, "            enrollment.user = request.user"),
        (21, "        enrollment.save()"),
        (21, "        messages.success(request, \"Arizangiz qabul qilindi! Tez orada bog'lanamiz.\")"),
        (21, "        return redirect(course)"),
        (21, '    return render(request, "courses/course_detail.html", {"course": course, "form": form})'),
        (19, ""),
        (19, ""),
        (19, "def teacher_detail(request, pk):"),
        (19, "    teacher = get_object_or_404(Teacher, pk=pk)"),
        (19, '    return render(request, "courses/teacher_detail.html", {"teacher": teacher})'),
    ])


FORMS = '''from django import forms

from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["name", "phone"]
        labels = {"name": "Ismingiz", "phone": "Telefon"}
        widgets = {"phone": forms.TextInput(attrs={"placeholder": "+998 90 123 45 67"})}
'''


def accounts_views(n):
    return pick(n, [
        "from django.contrib.auth import login",
        (23, "from django.contrib.auth.decorators import login_required"),
        "from django.contrib.auth.forms import UserCreationForm",
        "from django.shortcuts import redirect, render",
        "",
        "",
        "def signup(request):",
        "    form = UserCreationForm(request.POST or None)",
        '    if request.method == "POST" and form.is_valid():',
        "        user = form.save()",
        "        login(request, user)",
        '        return redirect("home")',
        '    return render(request, "registration/signup.html", {"form": form})',
        (23, ""),
        (23, ""),
        (23, "@login_required"),
        (23, "def cabinet(request):"),
        (23, '    enrollments = request.user.enrollments.select_related("course")'),
        (23, '    return render(request, "accounts/cabinet.html", {"enrollments": enrollments})'),
    ])


def accounts_urls(n):
    return pick(n, [
        "from django.urls import path",
        "",
        "from . import views",
        "",
        "urlpatterns = [",
        '    path("signup/", views.signup, name="signup"),',
        (23, '    path("cabinet/", views.cabinet, name="cabinet"),'),
        "]",
    ])


def base_html(n):
    return pick(n, [
        "{% load static %}",
        "<!DOCTYPE html>",
        '<html lang="uz">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "  <title>{% block title %}EduCenter{% endblock %}</title>",
        "  <link rel=\"stylesheet\" href=\"{% static 'css/style.css' %}\">",
        "</head>",
        "<body>",
        "  <header>",
        "    <nav>",
        "      <a href=\"{% url 'home' %}\" class=\"logo\">EduCenter</a>",
        '      <ul class="menu">',
        (14, 17, "        <li><a href=\"{% url 'home' %}\">Bosh sahifa</a></li>"),
        (17, "        <li><a href=\"{% url 'course_list' %}\">Kurslar</a></li>"),
        (22, "        {% if user.is_authenticated %}"),
        (23, "          <li><a href=\"{% url 'cabinet' %}\">Kabinet</a></li>"),
        (22, "          <li>"),
        (22, "            <form method=\"post\" action=\"{% url 'logout' %}\">"),
        (22, "              {% csrf_token %}"),
        (22, '              <button type="submit" class="link">Chiqish</button>'),
        (22, "            </form>"),
        (22, "          </li>"),
        (22, "        {% else %}"),
        (22, "          <li><a href=\"{% url 'login' %}\">Kirish</a></li>"),
        (22, "          <li><a href=\"{% url 'signup' %}\" class=\"btn\">Ro'yxatdan o'tish</a></li>"),
        (22, "        {% endif %}"),
        "      </ul>",
        "    </nav>",
        "  </header>",
        "  <main>",
        (21, "    {% for message in messages %}"),
        (21, '      <p class="alert">{{ message }}</p>'),
        (21, "    {% endfor %}"),
        "    {% block content %}{% endblock %}",
        "  </main>",
        "  <footer>",
        "    <p>© 2026 EduCenter · Toshkent</p>",
        "  </footer>",
        "</body>",
        "</html>",
    ])


def home_html(n):
    return pick(n, [
        '{% extends "base.html" %}',
        "",
        "{% block content %}",
        '  <section class="hero">',
        "    <h1>Kelajak kasblarini biz bilan o'rganing</h1>",
        "    <p>Python, Telegram bot va web dasturlash kurslari — Toshkentda.</p>",
        (14, 17, '    <a href="#" class="btn">Kurslarni ko\'rish</a>'),
        (17, "    <a href=\"{% url 'course_list' %}\" class=\"btn\">Kurslarni ko'rish</a>"),
        "  </section>",
        (17, "  <section>"),
        (17, "    <h2>Mashhur kurslar</h2>"),
        (17, '    <div class="grid">'),
        (17, "      {% for course in courses %}"),
        (17, '        {% include "courses/_card.html" %}'),
        (17, "      {% empty %}"),
        (17, "        <p>Hozircha kurslar yo'q.</p>"),
        (17, "      {% endfor %}"),
        (17, "    </div>"),
        (17, "  </section>"),
        "{% endblock %}",
    ])


def card_html(n):
    return pick(n, [
        '<article class="card">',
        (20, '  {% if course.image %}<img src="{{ course.image.url }}" alt="{{ course.title }}">{% endif %}'),
        (17, 18, "  <h3>{{ course.title }}</h3>"),
        (18, '  <h3><a href="{{ course.get_absolute_url }}">{{ course.title }}</a></h3>'),
        "  <p>{{ course.description|truncatewords:15 }}</p>",
        "  <p class=\"price\">{{ course.price }} so'm · {{ course.duration_months }} oy</p>",
        "</article>",
    ])


def list_html(n):
    return pick(n, [
        '{% extends "base.html" %}',
        "",
        "{% block title %}Kurslar — EduCenter{% endblock %}",
        "",
        "{% block content %}",
        "  <section>",
        "    <h1>Kurslar</h1>",
        (23, '    <form method="get" class="search">'),
        (23, '      <input type="search" name="q" value="{{ query }}" placeholder="Kurs qidirish..." aria-label="Kurs qidirish">'),
        (23, '      <button type="submit" class="btn">Qidirish</button>'),
        (23, "    </form>"),
        '    <div class="grid">',
        "      {% for course in courses %}",
        '        {% include "courses/_card.html" %}',
        "      {% empty %}",
        "        <p>Hech narsa topilmadi.</p>",
        "      {% endfor %}",
        "    </div>",
        "  </section>",
        "{% endblock %}",
    ])


def detail_html(n):
    return pick(n, [
        '{% extends "base.html" %}',
        "",
        "{% block title %}{{ course.title }} — EduCenter{% endblock %}",
        "",
        "{% block content %}",
        '  <section class="detail">',
        (20, '    {% if course.image %}<img src="{{ course.image.url }}" alt="{{ course.title }}">{% endif %}'),
        "    <div>",
        (19, '      {% if course.category %}<p class="tag">{{ course.category }}</p>{% endif %}'),
        "      <h1>{{ course.title }}</h1>",
        "      {{ course.description|linebreaks }}",
        "      <p class=\"price\">{{ course.price }} so'm · {{ course.duration_months }} oy</p>",
        (19, "      <h2>Ustozlar</h2>"),
        (19, "      <ul>"),
        (19, "        {% for teacher in course.teachers.all %}"),
        (19, "          <li><a href=\"{% url 'teacher_detail' teacher.pk %}\">{{ teacher.name }}</a></li>"),
        (19, "        {% empty %}"),
        (19, "          <li>Ustoz tez orada e'lon qilinadi.</li>"),
        (19, "        {% endfor %}"),
        (19, "      </ul>"),
        "    </div>",
        "  </section>",
        (21, "  <section>"),
        (21, "    <h2>Kursga yozilish</h2>"),
        (21, '    <form method="post" class="form">'),
        (21, "      {% csrf_token %}"),
        (21, "      {{ form.as_p }}"),
        (21, '      <button type="submit" class="btn">Yuborish</button>'),
        (21, "    </form>"),
        (21, "  </section>"),
        "{% endblock %}",
    ])


def teacher_html(n):
    return pick(n, [
        '{% extends "base.html" %}',
        "",
        "{% block title %}{{ teacher.name }} — EduCenter{% endblock %}",
        "",
        "{% block content %}",
        '  <section class="detail">',
        (20, '    {% if teacher.photo %}<img src="{{ teacher.photo.url }}" alt="{{ teacher.name }}">{% endif %}'),
        "    <div>",
        "      <h1>{{ teacher.name }}</h1>",
        "      {{ teacher.bio|linebreaks }}",
        "    </div>",
        "  </section>",
        "{% endblock %}",
    ])


def auth_html(title, button, footer):
    return f'''{{% extends "base.html" %}}

{{% block title %}}{title} — EduCenter{{% endblock %}}

{{% block content %}}
  <section class="narrow">
    <h1>{title}</h1>
    <form method="post" class="form">
      {{% csrf_token %}}
      {{{{ form.as_p }}}}
      <button type="submit" class="btn">{button}</button>
    </form>
    <p>{footer}</p>
  </section>
{{% endblock %}}
'''


LOGIN_HTML = auth_html("Kirish", "Kirish", "Akkauntingiz yo'qmi? <a href=\"{% url 'signup' %}\">Ro'yxatdan o'ting</a>")
SIGNUP_HTML = auth_html("Ro'yxatdan o'tish", "Ro'yxatdan o'tish", "Akkauntingiz bormi? <a href=\"{% url 'login' %}\">Kirish</a>")

CABINET_HTML = '''{% extends "base.html" %}

{% block title %}Kabinet — EduCenter{% endblock %}

{% block content %}
  <section>
    <h1>Mening arizalarim</h1>
    <div class="table-wrap">
      <table>
        <tr><th>Kurs</th><th>Telefon</th><th>Sana</th></tr>
        {% for e in enrollments %}
          <tr>
            <td><a href="{{ e.course.get_absolute_url }}">{{ e.course }}</a></td>
            <td>{{ e.phone }}</td>
            <td>{{ e.created|date:"d.m.Y H:i" }}</td>
          </tr>
        {% empty %}
          <tr><td colspan="3">Hali ariza yo'q. <a href="{% url 'course_list' %}">Kurs tanlang</a></td></tr>
        {% endfor %}
      </table>
    </div>
  </section>
{% endblock %}
'''

CSS_BASE = '''* {
  box-sizing: border-box;
}

:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --text: #1f2937;
  --muted: #64748b;
  --accent: #0f766e;
  --border: #e5e7eb;
}

body {
  margin: 0;
  font-family: "Segoe UI", system-ui, sans-serif;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
}

a {
  color: var(--accent);
}

header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}

nav,
main,
footer {
  max-width: 1040px;
  margin: 0 auto;
  padding: 16px 20px;
}

nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.logo {
  font-weight: 800;
  font-size: 20px;
  color: var(--accent);
  text-decoration: none;
}

.menu {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu a {
  color: inherit;
  text-decoration: none;
}

.hero {
  padding: 56px 0;
  text-align: center;
}

.hero h1 {
  font-size: clamp(28px, 5vw, 44px);
  line-height: 1.2;
  margin: 0 0 12px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  border: 0;
  border-radius: 8px;
  background: var(--accent);
  color: #ffffff;
  font: inherit;
  text-decoration: none;
  cursor: pointer;
}

.menu .btn {
  color: #ffffff;
}

footer {
  color: var(--muted);
  font-size: 14px;
}
'''

CSS_CARDS = '''
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
}

.card h3 {
  margin: 0 0 8px;
}

.card a {
  color: inherit;
}

.price {
  font-weight: 700;
  color: var(--accent);
}
'''

CSS_DETAIL = '''
.detail {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: start;
}

.tag {
  display: inline-block;
  margin: 0;
  padding: 2px 10px;
  border-radius: 999px;
  background: #ccfbf1;
  color: #115e59;
  font-size: 13px;
}
'''

CSS_IMAGES = '''
.card img,
.detail img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 8px;
}

.card img {
  margin-bottom: 12px;
}
'''

CSS_FORM = '''
.form {
  display: grid;
  gap: 4px;
  max-width: 420px;
}

.form input {
  width: 100%;
  font: inherit;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}

.errorlist {
  color: #b91c1c;
  padding-left: 18px;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  background: #dcfce7;
  color: #166534;
}
'''

CSS_AUTH = '''
.narrow {
  max-width: 460px;
  margin: 0 auto;
}

.helptext,
.form ul:not(.errorlist) {
  color: var(--muted);
  font-size: 13px;
}

.link {
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;
}
'''

CSS_SEARCH = '''
.search {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.search input {
  flex: 1;
  min-width: 0;
  font: inherit;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: var(--surface);
}

th,
td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}
'''


def style_css(n):
    parts = [(14, CSS_BASE), (17, CSS_CARDS), (18, CSS_DETAIL), (20, CSS_IMAGES), (21, CSS_FORM),
             (22, CSS_AUTH), (23, CSS_SEARCH)]
    return "".join(css for s, css in parts if n >= s)


SEED_DEMO = '''from django.core.management.base import BaseCommand

from courses.models import Category, Course, Teacher

COURSES = [
    ("Python asoslari", "python-asoslari", "Dasturlash", 450000, 3, "O'zgaruvchilar, sikllar, funksiyalar va OOP — noldan boshlab."),
    ("Telegram bot", "telegram-bot", "Dasturlash", 550000, 3, "aiogram 3 bilan haqiqiy bot: tugmalar, baza va server."),
    ("Web dasturlash", "web-dasturlash", "Web", 650000, 3, "HTML, CSS, JavaScript va Django bilan to'liq sayt."),
    ("Kompyuter savodxonligi", "kompyuter-savodxonligi", "Boshlang'ich", 300000, 2, "Word, Excel, internet va xavfsizlik asoslari."),
]


class Command(BaseCommand):
    help = "Demo uchun kategoriya, ustoz va kurslar yaratadi (qayta ishga tushirsa ham takrorlamaydi)"

    def handle(self, *args, **options):
        teacher, _ = Teacher.objects.get_or_create(
            name="Aziza Karimova", defaults={"bio": "Python va web dasturchi, 6 yillik tajriba."}
        )
        for title, slug, category_name, price, months, text in COURSES:
            category, _ = Category.objects.get_or_create(name=category_name)
            course, created = Course.objects.update_or_create(
                slug=slug,
                defaults={"title": title, "category": category, "price": price,
                          "duration_months": months, "description": text},
            )
            course.teachers.add(teacher)
            self.stdout.write(("+ " if created else "= ") + title)
        self.stdout.write(self.style.SUCCESS(f"Tayyor: {Course.objects.count()} ta kurs"))
'''


def project(n: int) -> dict:
    """EduCenter loyihasining n-darsdagi o'quvchi yozadigan fayllari (Django yaratadiganlari — startproject/startapp)."""
    if n < 13:
        return {}
    out = {
        ".gitignore": GITIGNORE,
        "requirements.txt": requirements(n),
        "config/settings.py": settings_py(n),
        "config/urls.py": config_urls(n),
    }
    if n >= 14:
        out |= {
            "courses/urls.py": courses_urls(n),
            "courses/views.py": views_py(n),
            "templates/base.html": base_html(n),
            "templates/courses/home.html": home_html(n),
            "static/css/style.css": style_css(n),
        }
    if n >= 15:
        out["courses/models.py"] = models_py(n)
    if n >= 16:
        out["courses/admin.py"] = admin_py(n)
    if n >= 17:
        out["templates/courses/_card.html"] = card_html(n)
        out["templates/courses/course_list.html"] = list_html(n)
    if n >= 18:
        out["templates/courses/course_detail.html"] = detail_html(n)
    if n >= 19:
        out["templates/courses/teacher_detail.html"] = teacher_html(n)
    if n >= 21:
        out["courses/forms.py"] = FORMS
    if n >= 22:
        out |= {
            "accounts/views.py": accounts_views(n),
            "accounts/urls.py": accounts_urls(n),
            "templates/registration/login.html": LOGIN_HTML,
            "templates/registration/signup.html": SIGNUP_HTML,
        }
    if n >= 23:
        out["templates/accounts/cabinet.html"] = CABINET_HTML
    if n >= 24:
        out |= {
            "courses/management/__init__.py": "",
            "courses/management/commands/__init__.py": "",
            "courses/management/commands/seed_demo.py": SEED_DEMO,
        }
    return out


def changed(n: int) -> dict:
    old = project(n - 1)
    return {k: v for k, v in project(n).items() if old.get(k) != v}


def files(n: int) -> dict:
    return {k: (v if v else "# bo'sh fayl — papkani Python paketiga aylantiradi\n") for k, v in changed(n).items()}


def tree(n: int, extra: list | None = None) -> list:
    old = project(n - 1)
    rows = [("educenter/", "")]
    names = sorted(changed(n)) + [p for p, _ in (extra or [])]
    tags = {k: ("o‘zgardi" if k in old else "yangi") for k in changed(n)} | dict(extra or [])
    for i, name in enumerate(names):
        rows.append((("└── " if i == len(names) - 1 else "├── ") + name, tags[name]))
    return rows


def preview(n: int, path: str, checks: list) -> dict:
    return {"image": f"lessons/WB{n:02}/site.png", "title": "Brauzerda natija",
            "sub": "chapda — kompyuter, o'ngda — telefon", "url": "127.0.0.1:8000" + path, "checks": checks}


def lines(text: str, first: str, last: str) -> str:
    """Fayldan first..last qatorlar oralig'ini (ikkalasi ham kiradi) qirqib oladi — qadam kodi faylga mos bo'lishi uchun."""
    rows = text.split("\n")
    i = next(k for k, r in enumerate(rows) if r == first)
    j = next(k for k in range(i, len(rows)) if rows[k] == last)
    return "\n".join(rows[i:j + 1])


LESSONS = {
    "WB13": lesson(
        M, 1, "Django nima: MVT va birinchi loyiha",
        "Django'ni o'rnatamiz, EduCenter loyihasini yaratamiz va birinchi marta ishga tushiramiz.",
        "9-oyda: statik Portfolio sayti (HTML, CSS, JS) va GitHub Pages.",
        "Nega Portfolio GitHub Pages'da ishladi, Django sayti esa ishlamaydi?",
        "Dinamik sayt: server so'rovga qarab sahifa yasaydi. MVT: Model (ma'lumot), View (mantiq), Template (ko'rinish); venv, startproject, runserver, settings.py.",
        "Loyihani GitHub'ga yuklang (.gitignore bilan).",
        [("🌐", "So'rov", "/kurslar/", ""),
         ("🧭", "urls.py", "qaysi view?", ""),
         ("🧠", "View", "mantiq", "mem"),
         ("🗃", "Model", "baza", ""),
         ("🎨", "Template", "HTML javob", "")],
        [
            step("Terminal", "Muhit va loyiha", '''$ mkdir educenter && cd educenter
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install "Django>=5.2,<6.0"
(.venv) $ pip freeze > requirements.txt
(.venv) $ django-admin startproject config .''',
                 [("venv", "har loyihaning kutubxonalari alohida — 5-oydagidek."),
                  ("startproject config .", "nuqta — loyiha shu papkada, config — sozlamalar papkasi."),
                  ("manage.py", "loyihani boshqarish buyruqlari shu orqali.")],
                 "manage.py  config/  .venv/"),
            step("config/settings.py", "Til va vaqt zonasi", '''LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True''',
                 [("LANGUAGE_CODE", "Django xabarlari va admin o'zbekcha."),
                  ("TIME_ZONE", "vaqtlar Toshkent bo'yicha ko'rsatiladi."),
                  ("DEBUG = True", "faqat ishlab chiqishda — xatolar batafsil ko'rinadi.")],
                 "settings.py saqlandi"),
            step("Terminal", "Birinchi ishga tushirish", '''(.venv) $ python manage.py migrate
(.venv) $ python manage.py runserver
Starting development server at http://127.0.0.1:8000/''',
                 [("migrate", "Django'ning tayyor jadvallari (foydalanuvchilar, sessiyalar) yaratiladi."),
                  ("runserver", "faqat dars uchun server — 8000-port."),
                  ("Ctrl + C", "serverni to'xtatish.")],
                 "🚀 The install worked successfully!"),
        ],
        files(13),
        tree(13, [("manage.py", "yangi"), ("db.sqlite3", "yangi")]),
        ["Dinamik va statik sayt", "MVT tuzilmasi", "startproject va manage.py", "migrate va runserver"],
        ["Majburiy: loyihani GitHub'ga yuklang (.gitignore bilan).",
         "Qo'shimcha: settings.py dagi har bir bo'lim nima qilishini izohlab yozing."],
        "10.2 · App, URL, view va shablon.",
        preview=preview(13, "/", ["Brauzerda 127.0.0.1:8000 ochildimi?", "Raketa sahifasi chiqdimi?", "Terminalda so'rovlar ko'rindimi?"]),
    ),
    "WB14": lesson(
        M, 2, "App, URL, view va shablon",
        "courses app'ini yaratamiz va EduCenter'ning bosh sahifasini o'z shablonimiz bilan chiqaramiz.",
        "O'tgan darsda: startproject, runserver, MVT.",
        "MVT'da “T” nima vazifani bajaradi?",
        "startapp; INSTALLED_APPS; include bilan URL'larni bo'lish; view funksiya va render; shablon merosi: base.html, block, extends; static fayllar.",
        "“Biz haqimizda” sahifasini qo'shing (URL, view, shablon).",
        [("🌐", "/", "so'rov", ""),
         ("🧭", "config/urls.py", "include", ""),
         ("🧭", "courses/urls.py", "home", "mem"),
         ("🧠", "views.home", "render", ""),
         ("🎨", "home.html", "extends base", "")],
        [
            step("courses/views.py · courses/urls.py", "App va birinchi view", '''def home(request):
    return render(request, "courses/home.html")''' + "\n\n" + lines(courses_urls(14), "urlpatterns = [", "]"),
                 [("startapp courses", "Terminal'da: python manage.py startapp courses."),
                  ("render", "shablonni HTML'ga aylantirib javob qaytaradi."),
                  ("name=\"home\"", "URL'ga nom — shablonda {% url 'home' %}.")],
                 "/ → views.home"),
            step("config/settings.py · config/urls.py", "Ulash", '''    "courses",''' + "\n" + '''        "DIRS": [BASE_DIR / "templates"],''' + "\n" + '''STATICFILES_DIRS = [BASE_DIR / "static"]''' + "\n" + '''    path("", include("courses.urls")),''',
                 [("INSTALLED_APPS", "Django app'ni taniydi."),
                  ("DIRS", "umumiy templates papkasi."),
                  ("include", "courses ichidagi URL'lar shu yerga ulanadi.")],
                 "loyiha ↔ app ulandi"),
            step("templates/base.html", "Umumiy shablon", lines(base_html(14), "<body>", "</html>"),
                 [("{% block content %}", "har sahifa shu joyni o'z mazmuni bilan to'ldiradi."),
                  ("{% static %}", "CSS yo'li — static/css/style.css (Portfolio uslubidan)."),
                  ("home.html", "{% extends \"base.html\" %} — header va footer qayta yozilmaydi.")],
                 "EduCenter · Kelajak kasblarini biz bilan o'rganing"),
        ],
        files(14),
        tree(14, [("courses/apps.py", "yangi")]),
        ["startapp va INSTALLED_APPS", "URL: include va name", "View va render", "Shablon merosi va static"],
        ["Majburiy: “Biz haqimizda” sahifasini qo'shing.",
         "Qo'shimcha: footer'ga markaz manzili va ish vaqtini yozing."],
        "10.3 · Modellar va migratsiya.",
        preview=preview(14, "/", ["Bosh sahifa o'z dizayni bilan chiqdimi?", "CSS ulandimi (rang va shrift)?"]),
    ),
    "WB15": lesson(
        M, 3, "Modellar va migratsiya",
        "Kurslar uchun Course modelini yozamiz — Django bazada jadval yaratadi.",
        "O'tgan darsda: app, URL, view, shablon.",
        "include nima uchun kerak?",
        "Model — Python klass, jadval; maydonlar: CharField, SlugField, TextField, BooleanField, DateTimeField; makemigrations va migrate; shell'da ORM.",
        "Course'ga price va duration_months maydonlarini qo'shing (keyingi darsda tekshiramiz).",
        [("🐍", "class Course", "Python", "mem"),
         ("📝", "makemigrations", "0001_initial.py", ""),
         ("🗃", "migrate", "jadval", ""),
         ("🔍", "shell", "Course.objects", "")],
        [
            step("courses/models.py", "Course modeli", lines(models_py(15), "class Course(models.Model):", "        return self.title"),
                 [("CharField(max_length)", "qisqa matn — sarlavha."),
                  ("SlugField(unique=True)", "URL uchun nom: python-asoslari."),
                  ("auto_now_add", "yaratilgan vaqt o'zi yoziladi."),
                  ("__str__", "admin va shell'da chiroyli nom.")],
                 "Course modeli tayyor"),
            step("Terminal", "Migratsiya", '''(.venv) $ python manage.py makemigrations
Migrations for 'courses':
  courses/migrations/0001_initial.py
    + Create model Course
(.venv) $ python manage.py migrate
  Applying courses.0001_initial... OK''',
                 [("makemigrations", "model o'zgarishidan reja (fayl) yasaydi."),
                  ("migrate", "rejani bazaga qo'llaydi."),
                  ("migrations/", "fayllari Git'ga qo'shiladi.")],
                 "courses_course jadvali yaratildi"),
            step("Terminal", "Shell'da sinov", '''(.venv) $ python manage.py shell
>>> from courses.models import Course
>>> Course.objects.create(title="Python asoslari", slug="python-asoslari", description="Noldan boshlab")
<Course: Python asoslari>
>>> Course.objects.count()
1''',
                 [("objects.create", "yangi qator qo'shadi — SQL yozmaymiz."),
                  ("count()", "nechta yozuv borligi."),
                  ("ORM", "Python obyektlari ↔ jadval qatorlari.")],
                 "<Course: Python asoslari>"),
        ],
        files(15),
        tree(15, [("courses/migrations/0001_initial.py", "yangi")]),
        ["Model va maydon turlari", "makemigrations va migrate", "ORM: create va count", "__str__"],
        ["Majburiy: Course'ga price va duration_months qo'shing.",
         "Qo'shimcha: shell'da 3 ta kurs yarating va filter(is_active=True) ni sinang."],
        "10.4 · Django admin.",
    ),
    "WB16": lesson(
        M, 4, "Django admin",
        "Kurslarni kod yozmasdan boshqarish uchun admin panelni sozlaymiz.",
        "O'tgan darsda: Course modeli va migratsiya.",
        "makemigrations va migrate farqi?",
        "createsuperuser; admin.site.register va @admin.register; list_display, list_editable, search_fields, prepopulated_fields; yangi maydon — yangi migratsiya.",
        "Admin'da kurslarni narx bo'yicha filtrlash qo'shing.",
        [("👤", "createsuperuser", "admin login", ""),
         ("🛠", "CourseAdmin", "sozlamalar", "mem"),
         ("📋", "list_display", "ustunlar", ""),
         ("🔎", "search_fields", "qidiruv", "")],
        [
            step("courses/models.py", "Narx va davomiylik", '''    price = models.PositiveIntegerField(default=0)
    duration_months = models.PositiveSmallIntegerField(default=3)''',
                 [("default", "mavjud kurslar uchun ham qiymat — migratsiya savol bermaydi."),
                  ("Positive...", "manfiy narx kiritib bo'lmaydi."),
                  ("makemigrations", "0002_course_duration_months_course_price.py fayli.")],
                 "price, duration_months qo'shildi"),
            step("courses/admin.py", "Admin sozlamalari", admin_py(16).strip("\n"),
                 [("@admin.register", "modelni admin'ga qo'shadi."),
                  ("list_editable", "ro'yxatning o'zida belgilash."),
                  ("prepopulated_fields", "slug sarlavhadan avtomatik yoziladi.")],
                 "Kurslar jadvali: nomi · narx · oy · faol"),
            step("Terminal", "Admin foydalanuvchi", '''(.venv) $ python manage.py makemigrations
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
Username: admin
Superuser created successfully.''',
                 [("createsuperuser", "parol terminalda ko'rinmaydi — bu normal."),
                  ("/admin/", "shu login bilan kiriladi."),
                  ("parol", "oddiy parol qo'ymang, hech kimga bermang.")],
                 "127.0.0.1:8000/admin/ — kirish"),
        ],
        files(16),
        tree(16, [("courses/migrations/0002_course_duration_months_course_price.py", "yangi")]),
        ["createsuperuser", "@admin.register va ModelAdmin", "list_display, search_fields", "Yangi maydon — yangi migratsiya"],
        ["Majburiy: admin'da narx bo'yicha filtr qo'shing.",
         "Qo'shimcha: admin orqali 4 ta kurs kiriting."],
        "10.5 · ORM va QuerySet: kurslar ro'yxati.",
        preview=preview(16, "/admin/courses/course/", ["Admin'ga kira oldingizmi?", "Kurslar jadvalida narx va oy ustunlari bormi?"]),
    ),
    "WB17": lesson(
        M, 5, "ORM va QuerySet: kurslar ro'yxati",
        "“Kurslar” sahifasini bazadan chiqaramiz: faqat faol kurslar, kartalar to'rida.",
        "O'tgan darsda: admin panel.",
        "list_display nima qiladi?",
        "QuerySet: all, filter, order_by, [:3]; view'dan shablonga context; {% for %} … {% empty %}; {% include %}; {% url %}.",
        "Faqat faol kurslarni narx bo'yicha saralab chiqaring.",
        [("🧠", "filter(is_active=True)", "QuerySet", "mem"),
         ("📦", "context", "{'courses': ...}", ""),
         ("🔁", "{% for %}", "kartalar", ""),
         ("🧩", "{% include %}", "_card.html", "")],
        [
            step("courses/views.py", "Ro'yxat view'i", lines(views_py(17), "def home(request):", '    return render(request, "courses/course_list.html", {"courses": courses})'),
                 [("filter", "shartga mos qatorlar — SQL WHERE."),
                  ("[:3]", "bosh sahifada faqat 3 ta — SQL LIMIT."),
                  ("context", "lug'at — shablonda {{ courses }}.")],
                 "/kurslar/ → course_list"),
            step("templates/courses/course_list.html", "Kartalar to'ri", lines(list_html(17), '    <div class="grid">', "    </div>"),
                 [("{% for %}", "har kurs uchun karta."),
                  ("{% empty %}", "ro'yxat bo'sh bo'lsa."),
                  ("{% include %}", "karta bitta faylda — bosh sahifada ham ishlatiladi.")],
                 "3 ta kurs kartasi"),
            step("templates/courses/_card.html", "Karta shabloni", card_html(17).strip("\n"),
                 [("{{ course.title }}", "obyekt maydoni."),
                  ("truncatewords:15", "filtr — 15 so'zdan keyin “…”."),
                  ("grid", "9-oydagi auto-fit/minmax to'ri.")],
                 "Python asoslari · 450000 so'm · 3 oy"),
        ],
        files(17),
        tree(17),
        ["QuerySet: filter, [:3]", "context va {{ }}", "{% for %} / {% empty %}", "{% include %} va {% url %}"],
        ["Majburiy: faol kurslarni narx bo'yicha saralang (order_by).",
         "Qo'shimcha: kurslar sonini sahifa sarlavhasida ko'rsating ({{ courses|length }})."],
        "10.6 · Detal sahifa: slug va get_object_or_404.",
        preview=preview(17, "/kurslar/", ["Admin'da kiritilgan kurslar chiqdimi?", "Nofaol kurs ro'yxatda yo'qmi?"]),
    ),
    "WB18": lesson(
        M, 6, "Detal sahifa: slug va get_object_or_404",
        "Har kursning o'z sahifasi: /kurslar/python-asoslari/.",
        "O'tgan darsda: kurslar ro'yxati.",
        "filter va all farqi?",
        "URL parametri <slug:slug>; get_object_or_404 — 404 xato; get_absolute_url va reverse; linebreaks filtri.",
        "Kurs sahifasiga “Boshqa kurslar” blokini qo'shing.",
        [("🔗", "/kurslar/<slug>/", "URL", ""),
         ("🧠", "get_object_or_404", "topadi yoki 404", "mem"),
         ("🧭", "get_absolute_url", "reverse", ""),
         ("🎨", "course_detail.html", "sahifa", "")],
        [
            step("courses/urls.py · courses/views.py", "URL va view", '''    path("kurslar/<slug:slug>/", views.course_detail, name="course_detail"),''' + "\n\n" + lines(views_py(18), "def course_detail(request, slug):", '    return render(request, "courses/course_detail.html", {"course": course})'),
                 [("<slug:slug>", "URL'dagi qism view'ga slug bo'lib keladi."),
                  ("get_object_or_404", "topilmasa “404 — sahifa topilmadi”."),
                  ("is_active=True", "nofaol kursni havola bilan ham ochib bo'lmaydi.")],
                 "/kurslar/python-asoslari/ → 200"),
            step("courses/models.py", "Kurs manzili", '''    def get_absolute_url(self):
        return reverse("course_detail", args=[self.slug])''',
                 [("reverse", "URL nomidan manzil yasaydi — URL o'zgarsa ham havolalar buzilmaydi."),
                  ("_card.html", "{{ course.get_absolute_url }} — karta sarlavhasi havola bo'ldi.")],
                 "/kurslar/telegram-bot/"),
            step("templates/courses/course_detail.html", "Kurs sahifasi", lines(detail_html(18), '  <section class="detail">', "  </section>"),
                 [("linebreaks", "matndagi qatorlar <p> bo'ladi."),
                  ("{% block title %}", "tabda kurs nomi.")],
                 "Python asoslari — 450000 so'm · 3 oy"),
        ],
        files(18),
        tree(18),
        ["URL parametrlari", "get_object_or_404", "get_absolute_url va reverse", "linebreaks"],
        ["Majburiy: kurs sahifasiga “Boshqa kurslar” blokini qo'shing.",
         "Qo'shimcha: o'z 404.html shabloningizni yarating (DEBUG=False da ko'rinadi)."],
        "10.7 · Bog'lanishlar: ForeignKey va ManyToMany.",
        preview=preview(18, "/kurslar/python-asoslari/", ["Kartani bosganda kurs sahifasi ochildimi?", "Noto'g'ri slug 404 berdimi?"]),
    ),
    "WB19": lesson(
        M, 7, "Bog'lanishlar: ForeignKey va ManyToMany",
        "Kurslarni kategoriyalarga bo'lamiz va ustozlarni bog'laymiz.",
        "O'tgan darsda: detal sahifa va slug.",
        "get_object_or_404 nima qaytaradi?",
        "ForeignKey (ko'pga-bir), on_delete; ManyToManyField (ko'pga-ko'p); related_name; course.teachers.all; admin'da list_filter.",
        "Ustoz sahifasida u dars beradigan kurslarni chiqaring (teacher.courses.all).",
        [("🗂", "Category", "1 → ko'p kurs", ""),
         ("🔗", "ForeignKey", "course.category", "mem"),
         ("👥", "ManyToMany", "course.teachers", ""),
         ("🧑‍🏫", "Teacher", "ustoz sahifasi", "")],
        [
            step("courses/models.py", "Category va Teacher", CATEGORY.rstrip("\n") + "\n\n\n" + lines(models_py(19), "class Teacher(models.Model):", "        return self.name"),
                 [("verbose_name_plural", "admin'da “categories” (aks holda “categorys”)."),
                  ("blank=True", "formada bo'sh qoldirish mumkin.")],
                 "2 ta yangi model"),
            step("courses/models.py · courses/admin.py", "Bog'lanishlar", '''    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="courses")
    teachers = models.ManyToManyField(Teacher, blank=True, related_name="courses")''' + "\n\n" + '''    list_filter = ["category", "is_active"]''',
                 [("ForeignKey", "har kursda bitta kategoriya; kategoriyada ko'p kurs."),
                  ("PROTECT", "kursi bor kategoriyani o'chirib bo'lmaydi."),
                  ("ManyToMany", "kursda ko'p ustoz, ustozda ko'p kurs."),
                  ("related_name", "teacher.courses.all() — teskari tomondan.")],
                 "admin: kategoriya bo'yicha filtr"),
            step("templates/courses/course_detail.html", "Ustozlar ro'yxati", lines(detail_html(19), "      <h2>Ustozlar</h2>", "      </ul>"),
                 [("course.teachers.all", "shablonda qavssiz yoziladi."),
                  ("{% url 'teacher_detail' teacher.pk %}", "ustoz sahifasiga havola.")],
                 "Ustozlar: Aziza Karimova"),
        ],
        files(19),
        tree(19, [("courses/migrations/0003_category_teacher_...py", "yangi")]),
        ["ForeignKey va on_delete", "ManyToManyField", "related_name", "list_filter"],
        ["Majburiy: ustoz sahifasida uning kurslarini chiqaring.",
         "Qo'shimcha: kurslar sahifasida kategoriya nomini ham ko'rsating."],
        "10.8 · Rasm yuklash: ImageField va media.",
        preview=preview(19, "/kurslar/telegram-bot/", ["Kategoriya yorlig'i chiqdimi?", "Ustoz nomi bosilganda uning sahifasi ochildimi?"]),
    ),
    "WB20": lesson(
        M, 8, "Rasm yuklash: ImageField va media",
        "Kurs va ustozlarga rasm qo'shamiz — admin orqali yuklanadi, saytda ko'rinadi.",
        "O'tgan darsda: ForeignKey va ManyToMany.",
        "related_name nima beradi?",
        "ImageField va Pillow; upload_to; MEDIA_URL va MEDIA_ROOT; DEBUG'da media'ni berish; static va media farqi; aspect-ratio va object-fit.",
        "Rasm bo'lmasa standart rasm ko'rsating.",
        [("⬆", "Admin", "rasm yuklash", ""),
         ("📁", "media/courses/", "fayl", "mem"),
         ("🗃", "Baza", "faqat yo'l", ""),
         ("🖼", "{{ course.image.url }}", "sahifada", "")],
        [
            step("requirements.txt · courses/models.py", "ImageField", '''Pillow>=11.0''' + "\n\n" + '''    photo = models.ImageField(upload_to="teachers/", blank=True)''' + "\n" + '''    image = models.ImageField(upload_to="courses/", blank=True)''',
                 [("Pillow", "rasm bilan ishlash kutubxonasi — pip install Pillow."),
                  ("upload_to", "media ichidagi papka."),
                  ("bazada", "rasm emas, faqat fayl yo'li saqlanadi.")],
                 "makemigrations → 0004"),
            step("config/settings.py · config/urls.py", "Media sozlamalari", '''MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"''' + "\n\n" + '''if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)''',
                 [("static", "loyiha fayllari (CSS); media — foydalanuvchi yuklagan fayllar."),
                  ("DEBUG", "serverda media'ni Nginx beradi (11-oy)."),
                  (".gitignore", "media/ Git'ga qo'shilmaydi.")],
                 "/media/courses/python.jpg → 200"),
            step("templates/courses/_card.html · style.css", "Rasmni ko'rsatish", '''  {% if course.image %}<img src="{{ course.image.url }}" alt="{{ course.title }}">{% endif %}''' + "\n\n" + lines(CSS_IMAGES, ".card img,", "}"),
                 [("{% if %}", "rasm yo'q bo'lsa xato chiqmaydi."),
                  ("aspect-ratio", "hamma rasmlar bir xil 16:9."),
                  ("object-fit: cover", "rasm cho'zilmaydi, qirqiladi.")],
                 "kartalarda rasmlar"),
        ],
        files(20),
        tree(20, [("courses/migrations/0004_course_image_teacher_photo.py", "yangi"), ("media/courses/", "yangi")]),
        ["ImageField va Pillow", "MEDIA_URL va MEDIA_ROOT", "static va media farqi", "aspect-ratio, object-fit"],
        ["Majburiy: rasm bo'lmasa standart rasm ko'rsating.",
         "Qo'shimcha: ustoz sahifasida rasmni dumaloq qiling."],
        "10.9 · Formalar: kursga yozilish.",
        preview=preview(20, "/kurslar/", ["Admin'da yuklangan rasm kartada chiqdimi?", "Rasmlar bir xil o'lchamdami?"]),
    ),
    "WB21": lesson(
        M, 9, "Formalar: kursga yozilish",
        "Kurs sahifasida “Kursga yozilish” formasi: ariza bazaga tushadi, foydalanuvchi tasdiq xabarini ko'radi.",
        "O'tgan darsda: rasmlar va media.",
        "static va media farqi?",
        "Enrollment modeli; ModelForm; POST va GET; is_valid va xatolar; save(commit=False); CSRF himoyasi; messages; redirect (PRG).",
        "Telefon raqami +998 bilan boshlanishini tekshiring (clean_phone).",
        [("✉", "POST", "forma", ""),
         ("🛡", "csrf_token", "himoya", ""),
         ("✅", "is_valid()", "tekshiruv", "mem"),
         ("💾", "save()", "Enrollment", ""),
         ("↩", "redirect", "+ xabar", "")],
        [
            step("courses/models.py · courses/forms.py", "Model va forma", lines(models_py(21), "class Enrollment(models.Model):", '        return f"{self.name} — {self.course}"') + "\n\n" + lines(FORMS, "class EnrollmentForm(forms.ModelForm):", '        widgets = {"phone": forms.TextInput(attrs={"placeholder": "+998 90 123 45 67"})}'),
                 [("ModelForm", "maydonlar modeldan olinadi — takrorlamaymiz."),
                  ("fields", "foydalanuvchi faqat ism va telefon kiritadi."),
                  ("course", "view'da o'zimiz qo'yamiz.")],
                 "Enrollment + EnrollmentForm"),
            step("courses/views.py", "Formani qayta ishlash", lines(views_py(21), "def course_detail(request, slug):", '    return render(request, "courses/course_detail.html", {"course": course, "form": form})'),
                 [("request.POST or None", "GET'da bo'sh forma, POST'da to'ldirilgan."),
                  ("commit=False", "saqlashdan oldin course'ni qo'shamiz."),
                  ("redirect", "F5 bosilsa ariza ikki marta yuborilmaydi (POST → redirect → GET).")],
                 "Arizangiz qabul qilindi!"),
            step("templates/courses/course_detail.html · base.html", "Forma va xabar", lines(detail_html(21), "  <section>", "  </section>") + "\n\n" + lines(base_html(21), "    {% for message in messages %}", "    {% endfor %}"),
                 [("{% csrf_token %}", "begona saytdan soxta forma yuborishdan himoya."),
                  ("form.as_p", "label, maydon va xatolar avtomatik."),
                  ("messages", "bir martalik xabar — keyingi sahifada ko'rinadi.")],
                 "✅ Arizangiz qabul qilindi! Tez orada bog'lanamiz."),
        ],
        files(21),
        tree(21, [("courses/migrations/0005_enrollment.py", "yangi")]),
        ["ModelForm", "POST, is_valid, save(commit=False)", "CSRF himoyasi", "messages va redirect"],
        ["Majburiy: telefon +998 bilan boshlanishini tekshiring.",
         "Qo'shimcha: admin'da arizalarni sana bo'yicha saralang."],
        "10.10 · Ro'yxatdan o'tish va login.",
        preview=preview(21, "/kurslar/python-asoslari/", ["Forma yuborilgach yashil xabar chiqdimi?", "Ariza admin'da ko'rindimi?", "Bo'sh forma xato ko'rsatdimi?"]),
    ),
    "WB22": lesson(
        M, 10, "Ro'yxatdan o'tish va login",
        "Foydalanuvchilar ro'yxatdan o'tadi, kiradi va chiqadi — Django'ning tayyor auth tizimi bilan.",
        "O'tgan darsda: ModelForm va ariza.",
        "Nega forma yuborilgach redirect qilamiz?",
        "django.contrib.auth.urls (login, logout); UserCreationForm; login(); user.is_authenticated; LOGIN_REDIRECT_URL; Django 5'da logout faqat POST.",
        "Login'dan keyin bosh sahifada “Salom, ism!” chiqsin.",
        [("📝", "signup", "UserCreationForm", ""),
         ("🔐", "login", "tayyor view", "mem"),
         ("🙋", "user.is_authenticated", "menyu", ""),
         ("🚪", "logout", "POST forma", "")],
        [
            step("accounts/views.py · accounts/urls.py", "Ro'yxatdan o'tish", lines(accounts_views(22), "def signup(request):", '    return render(request, "registration/signup.html", {"form": form})') + "\n\n" + '''    path("signup/", views.signup, name="signup"),''',
                 [("startapp accounts", "foydalanuvchi bilan bog'liq hamma narsa alohida app'da."),
                  ("UserCreationForm", "login va parolni ikki marta — tekshiruvlar tayyor."),
                  ("login(request, user)", "ro'yxatdan o'tgach darhol kiritadi.")],
                 "/accounts/signup/"),
            step("config/urls.py · config/settings.py", "Tayyor login va logout", '''    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),''' + "\n\n" + '''LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"''',
                 [("auth.urls", "login/, logout/, password_change/ — tayyor."),
                  ("registration/login.html", "shablonni o'zimiz yozamiz."),
                  ("REDIRECT_URL", "kirgach va chiqqach bosh sahifaga.")],
                 "/accounts/login/ → Kirish"),
            step("templates/base.html", "Menyu: kim kirgan?", lines(base_html(22), "        {% if user.is_authenticated %}", "        {% endif %}"),
                 [("user", "har shablonda bor (auth context processor)."),
                  ("POST forma", "Django 5'da chiqish faqat POST — havola bilan emas."),
                  ("class=\"link\"", "tugma havoladek ko'rinadi.")],
                 "Kurslar · Chiqish"),
        ],
        files(22),
        tree(22, [("accounts/apps.py", "yangi")]),
        ["auth.urls: login va logout", "UserCreationForm", "user.is_authenticated", "logout — POST"],
        ["Majburiy: bosh sahifada “Salom, ism!” chiqsin.",
         "Qo'shimcha: parolni o'zgartirish sahifasini (password_change) ulang."],
        "10.11 · Shaxsiy kabinet va qidiruv.",
        preview=preview(22, "/accounts/login/", ["Ro'yxatdan o'tgach menyuda “Chiqish” chiqdimi?", "Chiqish tugmasi ishladimi?"]),
    ),
    "WB23": lesson(
        M, 11, "Shaxsiy kabinet va qidiruv",
        "Kirgan foydalanuvchi o'z arizalarini ko'radi; kurslar sahifasida qidiruv ishlaydi.",
        "O'tgan darsda: ro'yxatdan o'tish va login.",
        "user.is_authenticated qayerdan keladi?",
        "@login_required; arizani foydalanuvchiga bog'lash; request.user.enrollments; select_related; GET parametri ?q=; Q obyekti va icontains.",
        "Qidiruvga kategoriya bo'yicha filtr qo'shing.",
        [("🔒", "@login_required", "faqat kirganlar", "mem"),
         ("🙋", "request.user", "arizalar", ""),
         ("🔍", "?q=bot", "GET", ""),
         ("🧮", "Q(...) | Q(...)", "yoki", "")],
        [
            step("courses/models.py · courses/views.py", "Arizani foydalanuvchiga bog'lash", '''    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="enrollments"
    )''' + "\n\n" + '''        if request.user.is_authenticated:
            enrollment.user = request.user''',
                 [("AUTH_USER_MODEL", "Django foydalanuvchi modeli."),
                  ("SET_NULL", "foydalanuvchi o'chsa ham ariza qoladi."),
                  ("null=True", "kirmagan mehmon ham ariza qoldira oladi.")],
                 "makemigrations → 0006"),
            step("accounts/views.py · cabinet.html", "Mening arizalarim", lines(accounts_views(23), "@login_required", '    return render(request, "accounts/cabinet.html", {"enrollments": enrollments})'),
                 [("@login_required", "kirmagan bo'lsa login sahifasiga (?next= bilan)."),
                  ("request.user.enrollments", "faqat o'zining arizalari — boshqalarniki emas."),
                  ("select_related", "kurslarni bitta so'rovda oladi.")],
                 "Kabinet: Python asoslari · +998 90 … · 20.11.2026"),
            step("courses/views.py · course_list.html", "Qidiruv", lines(views_py(23), "def course_list(request):", '    return render(request, "courses/course_list.html", {"courses": courses, "query": query})') + "\n\n" + lines(list_html(23), '    <form method="get" class="search">', "    </form>"),
                 [("method=\"get\"", "qidiruv URL'da ko'rinadi — havolani ulashish mumkin."),
                  ("icontains", "katta-kichik harfga qaramay qidiradi."),
                  ("Q | Q", "sarlavhada YOKI tavsifda.")],
                 "?q=bot → Telegram bot"),
        ],
        files(23),
        tree(23, [("courses/migrations/0006_enrollment_user.py", "yangi")]),
        ["@login_required va ?next=", "request.user bilan filtrlash", "select_related", "GET qidiruv, Q va icontains"],
        ["Majburiy: qidiruvga kategoriya filtri qo'shing.",
         "Qo'shimcha: kabinetda arizani bekor qilish tugmasi (POST)."],
        "10.12 · 10-oy nazorati: EduCenter demosi.",
        preview=preview(23, "/accounts/cabinet/", ["Kabinetda faqat o'z arizalaringiz chiqdimi?", "Chiqib turib /accounts/cabinet/ login'ga yo'naltirdimi?", "Qidiruv ishladimi?"]),
    ),
    "WB24": lesson(
        M, 12, "10-oy nazorati: EduCenter demosi",
        "Demo uchun ma'lumotlarni bitta buyruq bilan yaratamiz, saytni ko'rsatamiz va kodni tahlil qilamiz.",
        "10-oyda: Django MVT, modellar, admin, ORM, formalar, auth, kabinet va qidiruv.",
        "@login_required nima qiladi?",
        "Management command (BaseCommand, handle); get_or_create va update_or_create — qayta ishga tushirsa takrorlamaydi; demo ssenariysi; kod tahlili mezonlari.",
        "Tahlildagi izohlar bo'yicha kodni tuzating.",
        [("⚙", "seed_demo", "buyruq", "mem"),
         ("🗃", "4 ta kurs", "kategoriya + ustoz", ""),
         ("🎤", "Demo", "3 daqiqa", ""),
         ("🔍", "Kod tahlili", "izohlar", "")],
        [
            step("courses/management/commands/seed_demo.py", "Demo ma'lumotlar buyrug'i", lines(SEED_DEMO, "class Command(BaseCommand):", '        self.stdout.write(self.style.SUCCESS(f"Tayyor: {Course.objects.count()} ta kurs"))'),
                 [("management/commands/", "fayl nomi — buyruq nomi: python manage.py seed_demo."),
                  ("update_or_create", "slug bo'yicha: bor bo'lsa yangilaydi, yo'q bo'lsa yaratadi."),
                  ("ikki marta", "ishga tushirsa ham kurslar ko'paymaydi.")],
                 "Tayyor: 4 ta kurs"),
            step("Terminal", "Ishga tushirish", '''(.venv) $ python manage.py seed_demo
+ Python asoslari
+ Telegram bot
+ Web dasturlash
+ Kompyuter savodxonligi
Tayyor: 4 ta kurs
(.venv) $ python manage.py seed_demo
= Python asoslari
...
Tayyor: 4 ta kurs''',
                 [("+ / =", "yaratildi yoki yangilandi."),
                  ("yangi kompyuter", "loyihani klonlagan har kim bir buyruq bilan demo oladi.")],
                 "Tayyor: 4 ta kurs"),
            step("Telegram · demo.md", "Demo ssenariysi", '''1. Bosh sahifa → “Kurslarni ko'rish” (20 s)
2. Qidiruv: “bot” → Telegram bot sahifasi (30 s)
3. Ro'yxatdan o'tish → kursga yozilish → yashil xabar (60 s)
4. Kabinet: “Mening arizalarim” (20 s)
5. Admin: yangi ariza, kategoriya filtri (30 s)
6. Kod: models.py va views.py — 2 ta qiziq joy (20 s)''',
                 [("foydalanuvchi ko'zi bilan", "avval sayt, keyin admin, oxirida kod."),
                  ("kod tahlili", "nomlar, takrorlanish, xavfsizlik (login_required, CSRF).")],
                 "3 daqiqalik demo"),
        ],
        files(24),
        tree(24),
        ["Management command", "get_or_create, update_or_create", "Demo ssenariysi", "Kod tahlili"],
        ["Majburiy: tahlildagi izohlar bo'yicha kodni tuzating.",
         "Qo'shimcha: seed_demo ga 2 ta ustoz va ularning rasmlarini qo'shing."],
        "11.1 · Yangiliklar, sahifalash va class-based views.",
        preview=preview(24, "/", ["seed_demo dan keyin bosh sahifada 3 ta kurs chiqdimi?", "Demo 3 daqiqaga sig'dimi?"]),
    ),
}
