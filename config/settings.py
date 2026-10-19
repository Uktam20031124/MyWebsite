import os
import sys
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(int(default))).lower() in ("1", "true", "yes", "on")


def env_list(name: str, default: str = "") -> list[str]:
    return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]


DEBUG = env_bool("DJANGO_DEBUG", True)

_DEV_SECRET = "dev-only-change-me-darsxona-ustoz-crm-local-secret"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", _DEV_SECRET)
if not DEBUG and SECRET_KEY == _DEV_SECRET:
    raise ImproperlyConfigured("Production uchun DJANGO_SECRET_KEY o'rnatilishi shart.")

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "academy",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Production'da statikani gunicorn'ning o'zi (nginx'siz ham) beradi.
    *([] if DEBUG else ["whitenoise.middleware.WhiteNoiseMiddleware"]),
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Sahifalar Turbo bilan ochiladi: xatoli forma javobini Turbo ko'rsatadigan qiladi.
    "academy.middleware.TurboFormStatusMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "academy.context_processors.nav_counts",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_DB_PATH", BASE_DIR / "db.sqlite3"),
        "OPTIONS": {
            # WAL + busy timeout: gunicorn bir nechta worker bilan ishlaganda
            # "database is locked" xatolarining oldini oladi.
            "timeout": 20,
            "transaction_mode": "IMMEDIATE",
            "init_command": "PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

if len(sys.argv) > 1 and sys.argv[1] == "test":
    # Testlarda kuchli hash shart emas — to'plam bir necha barobar tezlashadi.
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Yuklangan fayllar (savol rasmlari). Django o'zi beradi (/media/quiz/...), nginx shart emas.
MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("DARSXONA_MEDIA_DIR", BASE_DIR / "media")
QUIZ_IMAGE_MAX_BYTES = 3 * 1024 * 1024
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Kesh: login urinishlari hisoblagichi uchun. gunicorn bir nechta worker bilan
# ishlaganda hisob umumiy bo'lishi uchun DJANGO_CACHE_DIR (fayl kesh) bering.
_CACHE_DIR = os.environ.get("DJANGO_CACHE_DIR")
CACHES = {
    "default": (
        {"BACKEND": "django.core.cache.backends.filebased.FileBasedCache", "LOCATION": _CACHE_DIR}
        if _CACHE_DIR
        else {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    )
}

LOGIN_URL = "login"

# Test havolalari faqat shu Telegram akkauntidan yuboriladi (Telethon sessiyasi bilan).
# API ID/hash: my.telegram.org → API development tools. Sessiya: manage.py telegram_login.
TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID") or 0)
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
TELEGRAM_SENDER_ID = int(os.environ.get("TELEGRAM_SENDER_ID") or 7730996406)
TELEGRAM_SESSION_FILE = os.environ.get("TELEGRAM_SESSION_FILE", BASE_DIR / ".telegram_session")

# Gmail orqali email (SMTP). Google hisobida 2 bosqichli tasdiqlash yoqilgan bo'lishi va
# "App password" (16 belgi) yaratilgan bo'lishi kerak: myaccount.google.com/apppasswords
GMAIL_USER = os.environ.get("DARSXONA_GMAIL_USER", "").strip()
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = GMAIL_USER
EMAIL_HOST_PASSWORD = os.environ.get("DARSXONA_GMAIL_APP_PASSWORD", "").replace(" ", "")
EMAIL_TIMEOUT = 20
EMAIL_FROM_NAME = os.environ.get("DARSXONA_EMAIL_FROM_NAME", "Darsxona")
DEFAULT_FROM_EMAIL = f"{EMAIL_FROM_NAME} <{GMAIL_USER}>" if GMAIL_USER else "webmaster@localhost"
# Kunlik hisobot qaysi manzilga (standart — Gmail hisobning o'zi).
REPORT_EMAIL = os.environ.get("DARSXONA_REPORT_EMAIL", GMAIL_USER)

# Saytning ochiq manzili: fonda ishlaydigan buyruqlar (eslatmalar) havola yasashi uchun.
SITE_URL = os.environ.get("DARSXONA_SITE_URL", "").rstrip("/")
# Ochilmagan test haqida eslatma: yuborilgandan shuncha soat o'tgach, faqat kunduzi
# (mahalliy vaqt bo'yicha [boshi, oxiri) soatlar oralig'ida), har bir havolaga bir marta.
QUIZ_REMINDER_AFTER_HOURS = int(os.environ.get("DARSXONA_REMINDER_AFTER_HOURS", 3))
QUIZ_REMINDER_HOURS = (9, 21)
# Bundan eski jo'natmalar uchun eslatma yuborilmaydi.
QUIZ_REMINDER_MAX_AGE_DAYS = 3

# Baza zaxirasi (manage.py backup_db): katalog va necha kunlik nusxa saqlanadi.
BACKUP_DIR = os.environ.get("DARSXONA_BACKUP_DIR", BASE_DIR / "backups")
BACKUP_KEEP_DAYS = int(os.environ.get("DARSXONA_BACKUP_KEEP_DAYS", 14))

# Brute-force himoyasi: shuncha xato urinishdan keyin IP vaqtincha bloklanadi.
LOGIN_FAILURE_LIMIT = int(os.environ.get("DJANGO_LOGIN_FAILURE_LIMIT", 5))
LOGIN_LOCKOUT_SECONDS = int(os.environ.get("DJANGO_LOGIN_LOCKOUT_SECONDS", 15 * 60))
# Faqat ilova nginx (yoki boshqa ishonchli proxy) ortida bo'lsa yoqing.
TRUST_X_FORWARDED_FOR = env_bool("DJANGO_TRUST_X_FORWARDED_FOR", False)
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# --- Xavfsizlik --------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", True)
    # Monitoring server ichidan oddiy HTTP bilan tekshira olsin.
    SECURE_REDIRECT_EXEMPT = [r"^healthz/$"]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", 60 * 60 * 24 * 30))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
