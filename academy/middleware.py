"""Turbo (Hotwire) bilan ishlash uchun kichik moslashuvlar."""


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
