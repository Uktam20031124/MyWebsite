"""Harakatlar jurnali: bosh ustoz va o'qituvchilarning amallari (kim, qachon, nima, qaysi obyekt).

Yoziladi: tizimga kirgan foydalanuvchining har bir muvaffaqiyatli POST amali (``ActionLogMiddleware``),
kirish va chiqish (signal). O'quvchilarning amallari (test, profil) va parollar yozilmaydi.
Obyekt nomi view ishlashidan oldin olinadi — o'chirilgan obyekt ham jurnalda nomi bilan qoladi.
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.urls import Resolver404, resolve
from django.utils.translation import gettext, gettext_noop

from .models import (
    ActionLog,
    Group,
    HomeworkSubmission,
    Lesson,
    Module,
    OpenQuiz,
    Purchase,
    QuizAttempt,
    QuizBatch,
    Registration,
    RegistrationLink,
    Reward,
    Student,
    TeacherAccount,
    TestRequest,
    Topic,
)

# Amal nomlari (jurnalda ko'rsatiladi).
LABELS = {
    "login": gettext_noop("Tizimga kirdi"),
    "logout": gettext_noop("Tizimdan chiqdi"),
    "teacher_list": gettext_noop("O‘qituvchi yaratdi"),
    "teacher_edit": gettext_noop("O‘qituvchini tahrirladi"),
    "teacher_unlink": gettext_noop("O‘qituvchi Telegramini uzdi"),
    "teacher_payout": gettext_noop("Maosh to‘lovini belgiladi"),
    "teacher_telegram_restart": gettext_noop("Telegram QR-kodini yangiladi"),
    "group_create": gettext_noop("Guruh yaratdi"),
    "group_update": gettext_noop("Guruhni tahrirladi"),
    "group_delete": gettext_noop("Guruhni o‘chirdi"),
    "start_lesson": gettext_noop("Darsni boshladi"),
    "syllabus_add": gettext_noop("Dasturga mavzu qo‘shdi"),
    "syllabus_toggle": gettext_noop("Dastur mavzusi holatini o‘zgartirdi"),
    "group_contact_link": gettext_noop("Aloqa havolasini o‘zgartirdi"),
    "group_portal_send": gettext_noop("Guruhga shaxsiy sahifalarni yubordi"),
    "group_leaderboard_send": gettext_noop("Reytingni guruh chatiga yubordi"),
    "group_telegram_chat": gettext_noop("Guruh Telegram chatini belgiladi"),
    "student_create": gettext_noop("Shogird qo‘shdi"),
    "student_update": gettext_noop("Shogirdni tahrirladi"),
    "student_delete": gettext_noop("Shogirdni o‘chirdi"),
    "contacts_import": gettext_noop("Aloqa ma’lumotlarini import qildi"),
    "student_portal_action": gettext_noop("Shaxsiy sahifa havolasini yubordi/yangiladi"),
    "student_certificate": gettext_noop("Sertifikat yaratdi"),
    "student_certificate_send": gettext_noop("Sertifikat yubordi"),
    "student_profile_access": gettext_noop("Profilga kirish ruxsatini o‘zgartirdi"),
    "student_honor": gettext_noop("A’lochi unvonini o‘zgartirdi"),
    "student_coin_gift": gettext_noop("Quvvat sovg‘a qildi"),
    "student_coin_undo": gettext_noop("Quvvat sovg‘asini bekor qildi"),
    "student_allowed_topics": gettext_noop("Test uchun mavzularni belgiladi"),
    "test_request_decide": gettext_noop("Test so‘roviga javob berdi"),
    "rewards": gettext_noop("Mukofot qo‘shdi"),
    "reward_edit": gettext_noop("Mukofotni tahrirladi"),
    "purchase_decide": gettext_noop("Mukofot so‘roviga javob berdi"),
    "registrations": gettext_noop("Ro‘yxatdan o‘tish havolasini yaratdi"),
    "registration_action": gettext_noop("Arizani ko‘rib chiqdi"),
    "registration_approve_all": gettext_noop("Arizalarni ommaviy tasdiqladi"),
    "registration_link_action": gettext_noop("Ro‘yxatdan o‘tish havolasini o‘zgartirdi"),
    "topic_create": gettext_noop("Mavzu yaratdi"),
    "topic_update": gettext_noop("Mavzuni tahrirladi"),
    "topic_delete": gettext_noop("Mavzuni o‘chirdi"),
    "topic_import": gettext_noop("Mavzularni import qildi"),
    "module_create": gettext_noop("Bo‘lim yaratdi"),
    "module_update": gettext_noop("Bo‘limni tahrirladi"),
    "module_delete": gettext_noop("Bo‘limni o‘chirdi"),
    "lesson_create": gettext_noop("Dars yozdi"),
    "lesson_update": gettext_noop("Darsni tahrirladi"),
    "lesson_delete": gettext_noop("Darsni o‘chirdi"),
    "lesson_complete": gettext_noop("Darsni o‘tildi deb belgiladi"),
    "attendance": gettext_noop("Yo‘qlama qildi"),
    "quiz_edit": gettext_noop("Test savollarini tahrirladi"),
    "quiz_delete": gettext_noop("Testni o‘chirdi"),
    "quiz_send": gettext_noop("Test jo‘natdi"),
    "quiz_batch_send": gettext_noop("Test havolalarini yubordi"),
    "quiz_batch_retake": gettext_noop("Qayta topshirish testini yaratdi"),
    "quiz_batch_delete": gettext_noop("Test jo‘natmasini o‘chirdi"),
    "quiz_attempt_renew": gettext_noop("Test havolasini yangiladi"),
    "attempt_penalty": gettext_noop("Ogohlantirish bo‘yicha qaror qildi"),
    "quiz_warnings": gettext_noop("Ogohlantirishlarni ommaviy kechirdi"),
    "quiz_review_decide": gettext_noop("Javoblarni ko‘rish so‘roviga javob berdi"),
    "quiz_review_approve_all": gettext_noop("Javoblarni ko‘rish so‘rovlarini ommaviy tasdiqladi"),
    "homework_check": gettext_noop("Uyga vazifani baholadi"),
    "open_quiz_create": gettext_noop("Ochiq test yaratdi"),
    "open_quiz_invite": gettext_noop("Ochiq testga taklif yubordi"),
    "open_quiz_toggle": gettext_noop("Ochiq testni yoqdi/o‘chirdi"),
    "open_quiz_delete": gettext_noop("Ochiq testni o‘chirdi"),
}

# URL'dagi pk qaysi obyekt (jurnalda nomi ko'rinishi uchun).
TARGET_MODELS = {
    **dict.fromkeys(
        ["group_update", "group_delete", "start_lesson", "syllabus_add", "syllabus_toggle", "group_contact_link",
         "group_portal_send", "group_leaderboard_send", "group_telegram_chat"],
        Group,
    ),
    **dict.fromkeys(
        ["student_update", "student_delete", "student_portal_action", "student_certificate",
         "student_certificate_send", "student_profile_access", "student_honor", "student_coin_gift",
         "student_coin_undo", "student_allowed_topics"],
        Student,
    ),
    **dict.fromkeys(["lesson_update", "lesson_delete", "lesson_complete", "attendance"], Lesson),
    **dict.fromkeys(["topic_update", "topic_delete", "quiz_edit", "quiz_delete"], Topic),
    **dict.fromkeys(["module_update", "module_delete"], Module),
    **dict.fromkeys(["quiz_batch_send", "quiz_batch_retake", "quiz_batch_delete"], QuizBatch),
    **dict.fromkeys(["attempt_penalty", "quiz_review_decide", "quiz_attempt_renew"], QuizAttempt),
    **dict.fromkeys(["open_quiz_invite", "open_quiz_toggle", "open_quiz_delete"], OpenQuiz),
    "homework_check": HomeworkSubmission,
    "reward_edit": Reward,
    "purchase_decide": Purchase,
    "test_request_decide": TestRequest,
    "registration_action": Registration,
    "registration_link_action": RegistrationLink,
    "teacher_edit": TeacherAccount,
    "teacher_unlink": TeacherAccount,
    "teacher_payout": TeacherAccount,
}
TEACHER_BY_USER = {"teacher_edit", "teacher_unlink", "teacher_payout"}  # pk — foydalanuvchi id
# Yaratishda obyekt nomi formadan (parol kabi maydonlar hech qachon olinmaydi).
NAME_FIELDS = ("full_name", "title", "name", "first_name", "username")
# Jurnalga yozilmaydigan POST'lar: o'quvchi/umumiy sahifalar va texnik so'rovlar.
SKIP = {
    "login",  # signal orqali
    "logout",  # signal orqali
    "set_language",
    "teacher_telegram_password",
    "teacher_telegram_status",
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
    "contact_self",
    "registration_public",
}


def label(action: str) -> str:
    return gettext(LABELS[action]) if action in LABELS else action


def target_of(url_name: str, kwargs: dict, post) -> str:
    model = TARGET_MODELS.get(url_name)
    pk = kwargs.get("pk")
    if model is not None and pk is not None:
        lookup = {"user_id": pk} if url_name in TEACHER_BY_USER else {"pk": pk}
        obj = model.objects.filter(**lookup).first()
        if obj is not None:
            return str(obj)[:200]
    for name in NAME_FIELDS:
        value = (post.get(name) or "").strip()
        if value:
            return value[:200]
    return ""


def client_ip(request) -> str:
    from .views import client_ip as ip

    return ip(request)[:64]


def record(request, action: str, target: str = "", user=None) -> None:
    user = user or request.user
    ActionLog.objects.create(
        user=user if user.is_authenticated else None,
        username=user.get_username() if user.is_authenticated else "",
        action=action,
        target=target,
        path=request.path[:255],
        ip=client_ip(request),
    )


class ActionLogMiddleware:
    """Tizimga kirgan foydalanuvchining muvaffaqiyatli POST amallarini jurnalga yozadi."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if request.method != "POST" or not (user and user.is_authenticated):
            return self.get_response(request)
        try:
            match = resolve(request.path_info)
        except Resolver404:
            return self.get_response(request)
        url_name = match.url_name or ""
        student_page = url_name.startswith(("portal_", "student_portal")) and url_name not in TARGET_MODELS
        if url_name in SKIP or student_page:
            return self.get_response(request)
        target = target_of(url_name, match.kwargs, request.POST)  # o'chirishdan oldin
        response = self.get_response(request)
        if succeeded(response):
            record(request, url_name, target, user)
        return response


def succeeded(response) -> bool:
    """Muvaffaqiyatli POST — yo'naltirish (PRG) yoki fayl (PDF, CSV). HTML 200/422 — forma xato bilan
    qayta ko'rsatilgan; 4xx/5xx — rad etilgan."""
    if 300 <= response.status_code < 400:
        return True
    return response.status_code == 200 and not response.get("Content-Type", "").startswith("text/html")


@receiver(user_logged_in, dispatch_uid="audit_login")
def _logged_in(sender, request, user, **kwargs):
    if request is not None:
        record(request, "login", user=user)


@receiver(user_logged_out, dispatch_uid="audit_logout")
def _logged_out(sender, request, user, **kwargs):
    if request is not None and user is not None:
        record(request, "logout", user=user)
