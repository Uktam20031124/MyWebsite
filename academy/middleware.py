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


# O'quvchi profili tili — faqat o'sha profil manziliga bog'langan cookie (path=/men/<kalit>/):
# bir profilda til almashtirish boshqa profillarga ham, ustoz paneliga ham ta'sir qilmaydi.
PORTAL_LANG_COOKIE = "portal_lang"


def activate_portal_language(request, student) -> None:
    """Profil tili: o'quvchi shu profilda tanlagani, bo'lmasa — uning test tili. Saytning umumiy
    til cookie'si (ustoz tanlovi) bu yerda hisobga olinmaydi."""
    from django.urls import reverse

    languages = dict(settings.LANGUAGES)
    lang = request.COOKIES.get(PORTAL_LANG_COOKIE, "")
    if lang not in languages:
        lang = student.quiz_language if student.quiz_language in languages else settings.LANGUAGE_CODE
    translation.activate(lang)
    request.LANGUAGE_CODE = lang
    # lang_switch.html shu manzilga yuboradi (umumiy set_language o'rniga).
    request.portal_lang_url = reverse("portal_language", args=[student.portal_token])
