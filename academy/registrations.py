"""Ochiq ro'yxatdan o'tish arizalari: o'quvchi to'ldiradi → ustoz tekshiradi → bazaga.

Ariza hech qachon o'z-o'zidan bazaga yozilmaydi: ustoz mavjud o'quvchiga biriktiradi,
yangi o'quvchi sifatida qo'shadi yoki rad etadi.
"""

import logging
import threading

from django.db import transaction
from django.utils import timezone

from . import telegram_sender as tg
from .contacts import match_students
from .models import Group, Registration, RegistrationLink, Student

log = logging.getLogger(__name__)


def submit(link: RegistrationLink, full_name: str, phone: str, telegram: str, email: str = "", ip=None):
    """Arizani saqlaydi: (ariza, yangimi). Shu havola orqali shu telefon bilan kutilayotgan
    ariza bo'lsa — yangisi ochilmaydi, o'sha yangilanadi (qayta yuborish, xatoni tuzatish)."""
    reg = Registration.objects.filter(
        link=link, phone=phone, status=Registration.Status.PENDING
    ).first()
    created = reg is None
    if created:
        reg = Registration(link=link, phone=phone)
    reg.full_name, reg.telegram, reg.email, reg.ip = full_name, telegram, email, ip
    reg.save()
    if created:
        notify_teacher(reg)
    return reg, created


def suggestions(reg: Registration) -> list[Student]:
    """Ariza kimga tegishli bo'lishi mumkin: avval havola guruhidan, keyin hammadan."""
    group_id = reg.link.group_id if reg.link_id else None
    if group_id:
        found = match_students(reg.full_name, Student.objects.filter(group_id=group_id))
        if found:
            return found
    return match_students(reg.full_name, Student.objects.select_related("group"))


def approve_existing(reg: Registration, student: Student) -> Student:
    """Mavjud o'quvchiga biriktiradi: telefon va Telegram (va email, berilgan bo'lsa)
    arizadagiga almashtiriladi."""
    with transaction.atomic():
        student.phone, student.telegram = reg.phone, reg.telegram
        fields = ["phone", "telegram"]
        if reg.email:
            student.email = reg.email
            fields.append("email")
        student.save(update_fields=fields)
        _close(reg, Registration.Status.APPROVED, student)
    return student


def approve_new(reg: Registration, group: Group) -> Student:
    """Arizadan yangi o'quvchi yaratadi."""
    with transaction.atomic():
        student = Student.objects.create(
            group=group,
            full_name=reg.full_name,
            phone=reg.phone,
            telegram=reg.telegram,
            email=reg.email,
        )
        _close(reg, Registration.Status.APPROVED, student)
    return student


def reject(reg: Registration) -> None:
    _close(reg, Registration.Status.REJECTED, None)


def _close(reg: Registration, status: str, student: Student | None) -> None:
    reg.status, reg.student, reg.reviewed_at = status, student, timezone.now()
    reg.save(update_fields=["status", "student", "reviewed_at"])


def notify_teacher(reg: Registration) -> None:
    """Yangi ariza haqida ustozning Telegram "Saqlangan xabarlar"iga — fonda.

    Telegram sekin javob bersa yoki ulanmagan bo'lsa ham o'quvchi kutib qolmaydi.
    """
    if not tg.is_configured():
        return
    where = reg.link.title if reg.link_id else "ro'yxat havolasi"
    text = (
        f"📝 Yangi ariza ({where}):\n{reg.full_name}\n{reg.phone} · @{reg.telegram}"
        + (f" · {reg.email}" if reg.email else "")
        + "\n"
        "Darsxona → Arizalar bo'limida tekshiring."
    )

    def run():
        try:
            tg.send_text_to_self(text)
        except Exception:  # noqa: BLE001 — bildirishnoma ixtiyoriy
            log.warning("Ariza bildirishnomasi yuborilmadi", exc_info=True)

    threading.Thread(target=run, daemon=True).start()
