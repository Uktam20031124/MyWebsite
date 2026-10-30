"""O'qituvchilar: bosh ustoz yaratgan loginlar, Telegramni QR orqali ulash va ruxsatlar.

- **Bosh ustoz** (superuser) — hamma narsani ko'radi va o'qituvchilarni boshqaradi.
- **O'qituvchi** (bosh ustoz yaratgan login) — faqat o'z guruhlari: test jo'natish (o'z Telegramidan)
  va natijalar. Boshqa sahifalar unga yopiq (``TeacherAccessMiddleware`` — ruxsat ro'yxati).
- Birinchi kirishda Telegram QR-kod orqali bir marta ulanadi; keyin qayta so'ralmaydi.

QR orqali kirish (Telethon) bir necha daqiqa davom etadi va bir nechta HTTP so'rovdan o'tadi:
u fon oqimida ishlaydi va holatni bazaga (``TeacherAccount.link_*``) yozadi — sahifa uni o'qiydi
(gunicorn'ning qaysi jarayoniga tushishidan qat'i nazar).
"""

import asyncio
import threading
from datetime import timedelta

from asgiref.sync import sync_to_async
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import Resolver404, resolve
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from . import telegram_sender as tg
from .models import (
    Group,
    HomeworkSubmission,
    Lesson,
    Purchase,
    QuizAttempt,
    QuizBatch,
    Registration,
    RegistrationLink,
    Student,
    TeacherAccount,
    TestRequest,
)

# Bosh ustoz o'qituvchiga ochadigan bo'limlar: (kalit, nomi, sahifalar). Har bir bo'limda
# o'qituvchi faqat o'z guruhlariga tegishli ma'lumotni ko'radi (``OBJECT_SCOPES`` va ro'yxatlarda
# ``scope``). Guruh ochish — alohida ruxsat (ochilgan guruh o'qituvchiga biriktiriladi); guruh/shogird
# o'chirish va "O'qituvchilar" — faqat bosh ustozda.
SECTIONS = [
    ("timetable", gettext_lazy("Dars jadvali"), {"timetable"}),
    (
        "groups",
        gettext_lazy("Guruhlar"),
        {
            "group_list",
            "group_detail",
            "group_update",
            "group_journal",
            "start_lesson",
            "syllabus_add",
            "syllabus_toggle",
            "group_contact_link",
            "group_portal_send",
            "group_qr",
            "group_leaderboard_send",
            "group_telegram_chat",
        },
    ),
    ("group_create", gettext_lazy("Guruh ochish (yangi guruh — o‘ziga biriktiriladi)"), {"group_create"}),
    (
        "students",
        gettext_lazy("Shogirdlar"),
        {
            "student_list",
            "student_create",
            "student_export",
            "student_detail",
            "student_update",
            "student_portal_action",
            "student_portal_open",
            "student_certificate",
            "student_certificate_send",
            "student_qr",
            "student_profile_access",
            "student_honor",
            "student_coin_gift",
            "student_coin_undo",
            "student_allowed_topics",
        },
    ),
    (
        "registrations",
        gettext_lazy("Arizalar"),
        {"registrations", "registration_action", "registration_approve_all", "registration_link_action"},
    ),
    (
        "lessons",
        gettext_lazy("Darslar"),
        {
            "lesson_list",
            "lesson_create",
            "lesson_detail",
            "lesson_update",
            "lesson_delete",
            "lesson_complete",
            "attendance",
        },
    ),
    ("topics", gettext_lazy("Mavzular (ko‘rish va taqdimot)"), {"topic_list", "topic_detail", "topic_slides"}),
    (
        "tests",
        gettext_lazy("Testlar (jo‘natmalar ro‘yxati)"),
        {"quiz_batches", "quiz_batch_retake", "quiz_batch_delete", "quiz_attempt_renew"},
    ),
    ("homework", gettext_lazy("Uyga vazifalar"), {"homework_list", "homework_check", "homework_file"}),
    ("rewards", gettext_lazy("Mukofotlar"), {"rewards", "reward_edit", "purchase_decide"}),
    ("warnings", gettext_lazy("Ogohlantirishlar"), {"quiz_warnings", "attempt_penalty"}),
    (
        "requests",
        gettext_lazy("So‘rovlar"),
        {
            "quiz_review_requests",
            "quiz_review_decide",
            "quiz_review_approve_all",
            "test_request_decide",
            "purchase_decide",
            "student_profile_access",
        },
    ),
]
SECTION_KEYS = [key for key, _label, _pages in SECTIONS]

# ``pk`` bilan ochiladigan sahifalar: obyekt o'qituvchi guruhiga tegishli bo'lmasa — 404.
OBJECT_SCOPES = {
    **dict.fromkeys(
        [
            "group_detail",
            "group_update",
            "group_journal",
            "start_lesson",
            "syllabus_add",
            "syllabus_toggle",
            "group_contact_link",
            "group_portal_send",
            "group_qr",
            "group_leaderboard_send",
            "group_telegram_chat",
        ],
        (Group, "teacher"),
    ),
    **dict.fromkeys(
        [
            "student_detail",
            "student_update",
            "student_portal_action",
            "student_portal_open",
            "student_certificate",
            "student_certificate_send",
            "student_qr",
            "student_profile_access",
            "student_honor",
            "student_coin_gift",
            "student_coin_undo",
            "student_allowed_topics",
        ],
        (Student, "group__teacher"),
    ),
    **dict.fromkeys(
        ["lesson_detail", "lesson_update", "lesson_delete", "lesson_complete", "attendance"],
        (Lesson, "group__teacher"),
    ),
    **dict.fromkeys(
        ["quiz_batch", "quiz_batch_send", "quiz_batch_retake", "quiz_batch_delete"], (QuizBatch, "group__teacher")
    ),
    **dict.fromkeys(
        ["quiz_attempt_review", "attempt_penalty", "quiz_review_decide", "quiz_attempt_renew"],
        (QuizAttempt, "student__group__teacher"),
    ),
    "test_request_decide": (TestRequest, "student__group__teacher"),
    "homework_check": (HomeworkSubmission, "student__group__teacher"),
    "homework_file": (HomeworkSubmission, "student__group__teacher"),
    "purchase_decide": (Purchase, "student__group__teacher"),
    "registration_action": (Registration, "link__group__teacher"),
    "registration_link_action": (RegistrationLink, "group__teacher"),
}

# O'qituvchi doim kira oladigan sahifalar (Telegram ulangandan keyin).
TEACHER_PAGES = {
    "teacher_home",
    "quiz_send",
    "quiz_batch",
    "quiz_batch_send",
    "quiz_attempt_review",
    "quiz_question_image",
}
# Telegramni ulash sahifalari (ulanmagan o'qituvchi faqat shularni ochadi).
LINK_PAGES = {
    "teacher_telegram",
    "teacher_telegram_status",
    "teacher_telegram_password",
    "teacher_telegram_restart",
}
# Login'siz ochiladigan (o'quvchi, test havolasi, ro'yxatdan o'tish) va umumiy sahifalar.
PUBLIC_PAGES = {
    "login",
    "logout",
    "healthz",
    "set_language",
    "media_file",
    "contact_self",
    "registration_public",
    "quiz_take",
    "quiz_save",
    "quiz_submit",
    "quiz_language",
    "quiz_review_request",
    "open_quiz_public",
    "open_quiz_take",
    "open_quiz_save",
    "open_quiz_submit",
    "open_quiz_language",
    "student_portal",
    "portal_language",
    "portal_review_request",
    "portal_access_request",
    "portal_test_request",
    "portal_test_start",
    "portal_study",
    "portal_unlock",
    "portal_practice",
    "portal_bonus",
    "portal_buy",
    "portal_homework",
    "portal_homework_file",
}

LINK_SECONDS = 240  # QR'ni skanerlash va parol kiritish uchun jami vaqt
QR_REFRESH_SECONDS = 25
STALE_SECONDS = 45  # shuncha vaqt yangilanmagan "jarayon" — to'xtagan hisoblanadi


def is_teacher(user) -> bool:
    """Bosh ustoz "O'qituvchilar" bo'limida yaratgan login (``TeacherAccount`` bor). Boshqa loginlar
    (masalan, admin panelda qo'shilgan xodim) — to'liq ustoz huquqida."""
    if not (user and user.is_authenticated) or user.is_superuser:
        return False
    try:
        return user.teacher_account is not None
    except TeacherAccount.DoesNotExist:
        return False


def account_of(user) -> TeacherAccount:
    account, _created = TeacherAccount.objects.get_or_create(user=user)
    return account


def teacher_groups(user):
    """Foydalanuvchi ko'radigan guruhlar (bosh ustoz — hammasi)."""
    if not is_teacher(user):
        return Group.objects.all()
    return Group.objects.filter(teacher=user)


def scope(user, qs, path: str = "group__teacher"):
    """Ro'yxatni o'qituvchining guruhlari bilan cheklaydi (bosh ustoz — o'zgarishsiz)."""
    return qs.filter(**{path: user}) if is_teacher(user) else qs


def permissions_of(user) -> set[str]:
    """Foydalanuvchiga ochiq bo'limlar (bosh ustoz — hammasi)."""
    if not is_teacher(user):
        return set(SECTION_KEYS)
    return set(user.teacher_account.permissions or []) & set(SECTION_KEYS)


def check_group(user, group_id) -> None:
    """O'qituvchi boshqa guruhga tegishli narsani ochmoqchi bo'lsa — 404 (borligini ham bildirmaymiz)."""
    if is_teacher(user) and not (group_id and Group.objects.filter(pk=group_id, teacher=user).exists()):
        raise Http404


def allowed_for_teacher(url_name: str, linked: bool, permissions=()) -> bool:
    if url_name in PUBLIC_PAGES or url_name in LINK_PAGES:
        return True
    if not linked:
        return False
    if url_name in TEACHER_PAGES:
        return True
    return any(url_name in pages for key, _label, pages in SECTIONS if key in permissions)


def owns_object(user, url_name: str, kwargs: dict) -> bool:
    """``pk`` bilan ochilgan obyekt o'qituvchi guruhiga tegishlimi (``OBJECT_SCOPES`` dagi sahifalar)."""
    target = OBJECT_SCOPES.get(url_name)
    if target is None or "pk" not in kwargs:
        return True
    model, path = target
    return model.objects.filter(pk=kwargs["pk"], **{path: user}).exists()


class TeacherAccessMiddleware:
    """O'qituvchi uchun: Telegram ulanmagan bo'lsa — ulash sahifasi; ruxsat etilmagan sahifa —
    o'z sahifasi. Bosh ustoz va login qilmaganlarga ta'sir qilmaydi."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if is_teacher(user) and not request.path.startswith("/static/"):
            try:
                match = resolve(request.path_info)
            except Resolver404:
                return self.get_response(request)
            url_name = match.url_name or ""
            account = account_of(user)
            linked = account.is_linked
            if linked and not owns_object(user, url_name, match.kwargs):
                raise Http404
            if not allowed_for_teacher(url_name, linked, set(account.permissions or [])):
                if not linked:
                    return redirect("teacher_telegram")
                if url_name != "dashboard":
                    messages.info(request, _("Bu bo‘lim faqat bosh ustoz uchun."))
                return redirect("teacher_home")
        return self.get_response(request)


# --- Telegramni QR orqali ulash ---------------------------------------------------------


def link_running(account: TeacherAccount) -> bool:
    if account.link_status not in {account.Link.STARTING, account.Link.QR, account.Link.PASSWORD}:
        return False
    limit = timezone.now() - timedelta(seconds=STALE_SECONDS)
    return bool(account.link_updated_at and account.link_updated_at > limit)


def start_link(account: TeacherAccount) -> bool:
    """Ulash jarayonini fon oqimida boshlaydi (allaqachon ketayotgan bo'lsa — yo'q). True — boshlandi."""
    if account.is_linked or link_running(account):
        return False
    TeacherAccount.objects.filter(pk=account.pk).update(
        link_status=TeacherAccount.Link.STARTING,
        link_url="",
        link_error="",
        link_password="",
        link_updated_at=timezone.now(),
    )
    threading.Thread(target=run_link, args=(account.pk,), daemon=True, name=f"tg-link-{account.pk}").start()
    return True


def run_link(account_pk: int, client_factory=None) -> None:
    try:
        asyncio.run(link_flow(account_pk, client_factory or tg.make_client))
    except Exception as exc:  # noqa: BLE001 — har qanday xato sahifada ko'rinsin
        _update(account_pk, link_status=TeacherAccount.Link.ERROR, link_error=_link_error(exc), link_password="")


def _link_error(exc: Exception) -> str:
    if isinstance(exc, tg.TelegramError):
        return str(exc)[:255]
    if isinstance(exc, (OSError, ConnectionError)):
        return _("Telegram serveriga ulanib bo‘lmadi — keyinroq qayta urinib ko‘ring.")
    return _("Telegramni ulashda xato: {name}").format(name=type(exc).__name__)


def _update(account_pk: int, **fields) -> None:
    TeacherAccount.objects.filter(pk=account_pk).update(link_updated_at=timezone.now(), **fields)


def _take_password(account_pk: int) -> str:
    """Sahifadan kiritilgan 2 bosqichli parolni oladi va bazadan darhol o'chiradi."""
    password = TeacherAccount.objects.filter(pk=account_pk).values_list("link_password", flat=True).first() or ""
    if password:
        TeacherAccount.objects.filter(pk=account_pk).update(link_password="")
    return password


def _finish(account_pk: int, me, session: str) -> None:
    account = TeacherAccount.objects.get(pk=account_pk)
    tg.save_teacher_session(account.user_id, session)
    name = " ".join(filter(None, [getattr(me, "first_name", ""), getattr(me, "last_name", "")]))
    _update(
        account_pk,
        telegram_id=me.id,
        telegram_name=name[:120],
        telegram_username=(getattr(me, "username", "") or "")[:64],
        linked_at=timezone.now(),
        link_status=TeacherAccount.Link.DONE,
        link_url="",
        link_error="",
        link_password="",
    )


async def link_flow(account_pk: int, client_factory=None) -> None:
    from telethon import errors

    update = sync_to_async(_update)
    loop = asyncio.get_running_loop()
    deadline = loop.time() + LINK_SECONDS
    async with tg.connected((client_factory or tg.make_client)()) as client:
        qr = await client.qr_login()
        while True:
            await update(account_pk, link_status=TeacherAccount.Link.QR, link_url=qr.url[:255], link_error="")
            try:
                await qr.wait(timeout=QR_REFRESH_SECONDS)
                break
            except asyncio.TimeoutError:
                if loop.time() > deadline:
                    raise tg.TelegramError(_("QR-kod skanerlanmadi — “Yangi QR-kod” tugmasini bosing.")) from None
                await qr.recreate()
            except errors.SessionPasswordNeededError:
                await _password_step(client, account_pk, deadline)
                break
        me = await client.get_me()
        await sync_to_async(_finish)(account_pk, me, client.session.save())


async def _password_step(client, account_pk: int, deadline: float) -> None:
    from telethon import errors

    update = sync_to_async(_update)
    take = sync_to_async(_take_password)
    loop = asyncio.get_running_loop()
    await update(account_pk, link_status=TeacherAccount.Link.PASSWORD, link_url="", link_error="")
    while loop.time() < deadline:
        password = await take(account_pk)
        if not password:
            await asyncio.sleep(1)
            await update(account_pk)  # jarayon tirik
            continue
        try:
            await client.sign_in(password=password)
            return
        except errors.PasswordHashInvalidError:
            await update(account_pk, link_error=_("2 bosqichli parol noto‘g‘ri — qayta kiriting."))
    raise tg.TelegramError(_("Parol kiritilmadi — “Yangi QR-kod” tugmasini bosib qayta urinib ko‘ring."))


def unlink(account: TeacherAccount) -> None:
    """Telegramni uzish (bosh ustoz): sessiya o'chiriladi, keyingi kirishda yana QR so'raladi."""
    tg.delete_teacher_session(account.user_id)
    TeacherAccount.objects.filter(pk=account.pk).update(
        telegram_id=None,
        telegram_name="",
        telegram_username="",
        linked_at=None,
        link_status=TeacherAccount.Link.NONE,
        link_url="",
        link_error="",
        link_password="",
    )
