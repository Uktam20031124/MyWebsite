"""Turbo (Hotwire) moslashuvlari va interfeys tili."""

from django.conf import settings
from django.utils import translation


def is_turbo_request(request) -> bool:
    # Turbo har bir fetch so'roviga shu sarlavhani qo'shadi.
    return "HTTP_X_TURBO_REQUEST_ID" in request.META


class TurboFormStatusMiddleware:
    """Xatoli formani qayta ko'rsatadigan POST javobi (200 HTML) → 422.

    Turbo forma yuborilgach yo yo'naltirish (3xx), yo xato kodi (4xx/5xx) kutadi; 200
    bilan qaytgan sahifani ko'rsatmaydi. Django'da xatoli forma odatda 200 bilan qayta
    chiziladi — shuning uchun Turbo so'rovlarida holat kodi 422 ga almashtiriladi.
    Turbo'siz so'rovlarga (oddiy brauzer, testlar, ochiq sahifalar) tegilmaydi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method == "POST"
            and response.status_code == 200
            and is_turbo_request(request)
            and response.get("Content-Type", "").startswith("text/html")
        ):
            response.status_code = 422
        return response


def cookie_language(request) -> str:
    """Foydalanuvchi tanlagan til (cookie), bo'lmasa — ""."""
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, "")
    return lang if lang in dict(settings.LANGUAGES) else ""


class LanguageMiddleware:
    """Interfeys tili: tanlangan til (cookie) yoki standart (o'zbekcha).

    Django'ning LocaleMiddleware'idan farqi — brauzerning Accept-Language sarlavhasiga
    qaramaydi: ustoz yoki o'quvchi rus tilli brauzerda bo'lsa ham, tilni o'zi tanlaydi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = cookie_language(request) or settings.LANGUAGE_CODE
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        response.headers.setdefault("Content-Language", translation.get_language())
        return response


def activate_default_language(request, lang: str) -> None:
    """Foydalanuvchi tilni o'zi tanlamagan bo'lsa — berilgan tilni yoqadi (masalan, o'quvchi
    profilida uning test tili)."""
    if not cookie_language(request) and lang in dict(settings.LANGUAGES):
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
