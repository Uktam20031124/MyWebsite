"""O'quvchining "javoblarimni ko'rsam bo'ladimi?" so'rovi: ustozga bildirishnoma.

O'quvchi testni tugatgach faqat ballini ko'radi. Qaysi savolda to'g'ri, qaysida xato
qilganini ko'rish uchun so'rov yuboradi; ustoz ruxsat bersa — natija sahifasida va
shaxsiy sahifasida ko'rinadi (to'g'ri variantlar baribir ko'rsatilmaydi).
"""

import logging
import threading

from django.conf import settings
from django.urls import reverse

from . import telegram_sender as tg
from .models import QuizAttempt

log = logging.getLogger(__name__)


def pending_requests():
    return (
        QuizAttempt.objects.filter(reveal=QuizAttempt.Reveal.REQUESTED)
        .select_related("student__group", "quiz__topic", "batch")
        .order_by("reveal_requested_at")
    )


def notify_teacher(attempt: QuizAttempt) -> None:
    """Ustozning Telegram "Saqlangan xabarlar"iga — fonda (o'quvchi kutib qolmaydi)."""
    if not tg.is_configured():
        return
    url = settings.SITE_URL + reverse("quiz_review_requests") if settings.SITE_URL else ""
    text = (
        f"🔓 {attempt.student.full_name} “{attempt.quiz.topic.title}” testidagi javoblarini "
        f"ko‘rmoqchi ({attempt.correct}/{attempt.total} · {attempt.percent}%).\n"
        + (url or "Darsxona → Testlar → So‘rovlar")
    )

    def run():
        try:
            tg.send_text_to_self(text)
        except Exception:  # noqa: BLE001 — bildirishnoma ixtiyoriy
            log.warning("Ko'rish so'rovi bildirishnomasi yuborilmadi", exc_info=True)

    threading.Thread(target=run, daemon=True).start()
