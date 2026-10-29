"""Uyga vazifani profil orqali topshirish va baholash.

- O'quvchi guruhidagi o'tilgan (yoki rejadagi, sanasi kelgan) darslarning uyga vazifasiga matn, havola
  va/yoki fayl topshiradi; baholanmaguncha qayta topshirishi mumkin.
- Muddat — guruhning keyingi darsi (bo'lmasa — dars + 7 kun); kech topshirilgani belgilanadi.
- O'qituvchi 0–100 ball va izoh qo'yadi. Vaqtida topshirilgan va ``PASS_SCORE`` dan yuqori
  baholangan vazifaga bir marta ``COINS`` ⚡️ beriladi.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import CoinTransaction, HomeworkSubmission, Lesson, Student

COINS = 3
PASS_SCORE = 50
DEFAULT_DAYS = 7
RECENT_LESSONS = 12
MAX_FILE_BYTES = 8 * 1024 * 1024  # nginx client_max_body_size 10m — forma bilan birga sig'sin
ALLOWED_EXTENSIONS = {
    "pdf", "png", "jpg", "jpeg", "gif", "webp", "heic", "txt", "doc", "docx", "xls", "xlsx",
    "ppt", "pptx", "odt", "zip", "py", "sb3", "html", "css", "js", "mp3", "mp4",
}  # fmt: skip
REASON = "📝 Uyga vazifa: {topic}"


class HomeworkError(Exception):
    """O'quvchiga ko'rsatiladigan sabab."""


def due_date(lesson: Lesson) -> date:
    """Muddat: guruhning keyingi darsi kuni (shu kun ham vaqtida), bo'lmasa — dars + 7 kun."""
    following = (
        Lesson.objects.filter(group_id=lesson.group_id, held_on__gt=lesson.held_on)
        .exclude(status=Lesson.Status.CANCELLED)
        .order_by("held_on")
        .values_list("held_on", flat=True)
        .first()
    )
    return following or lesson.held_on + timedelta(days=DEFAULT_DAYS)


def lessons_for(student: Student):
    """O'quvchi topshira oladigan uyga vazifali darslar (yangisi birinchi)."""
    return (
        Lesson.objects.filter(group_id=student.group_id, held_on__lte=timezone.localdate())
        .exclude(homework="")
        .exclude(status=Lesson.Status.CANCELLED)
        .select_related("topic")
        .order_by("-held_on", "-pk")[:RECENT_LESSONS]
    )


@dataclass
class Row:
    lesson: Lesson
    due: date
    submission: HomeworkSubmission | None

    @property
    def overdue(self) -> bool:
        return self.submission is None and timezone.localdate() > self.due


def rows_for(student: Student) -> list[Row]:
    lessons = list(lessons_for(student))
    subs = {s.lesson_id: s for s in student.homework.filter(lesson__in=lessons)}
    return [Row(lesson, due_date(lesson), subs.get(lesson.pk)) for lesson in lessons]


def check_file(upload) -> None:
    if upload is None:
        return
    if upload.size > MAX_FILE_BYTES:
        raise HomeworkError(_("Fayl juda katta — ko‘pi bilan {mb} MB.").format(mb=MAX_FILE_BYTES // (1024 * 1024)))
    ext = upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HomeworkError(_("Bu turdagi faylni yuklab bo‘lmaydi (.{ext}).").format(ext=ext or "?"))


def submit(student: Student, lesson: Lesson, text: str = "", link: str = "", upload=None) -> HomeworkSubmission:
    """Topshirish yoki (baholanmagan bo'lsa) yangilash."""
    if lesson.group_id != student.group_id or not lesson.homework or lesson.status == Lesson.Status.CANCELLED:
        raise HomeworkError(_("Bu darsga uyga vazifa topshirib bo‘lmaydi."))
    text, link = (text or "").strip(), (link or "").strip()
    check_file(upload)
    sub = HomeworkSubmission.objects.filter(student=student, lesson=lesson).first()
    if sub and sub.status == HomeworkSubmission.Status.CHECKED:
        raise HomeworkError(_("Vazifa allaqachon baholangan — o‘zgartirib bo‘lmaydi."))
    if not (text or link or upload or (sub and sub.file)):
        raise HomeworkError(_("Javob yozing, havola qo‘shing yoki fayl yuklang."))
    now = timezone.now()
    sub = sub or HomeworkSubmission(student=student, lesson=lesson)
    sub.text, sub.link, sub.submitted_at = text[:20000], link, now
    sub.on_time = timezone.localdate(now) <= due_date(lesson)
    if upload is not None:
        if sub.file:
            sub.file.delete(save=False)
        sub.file = upload
        sub.file_name = upload.name[:200]
    sub.save()
    return sub


def grade(sub: HomeworkSubmission, score: int, comment: str, user) -> int:
    """Baholash. Vaqtida va ``PASS_SCORE``+ — bir marta ⚡️. Natija: shu safar berilgan quvvat."""
    if not 0 <= score <= 100:
        raise HomeworkError(_("Ball 0 dan 100 gacha bo‘lishi kerak."))
    with transaction.atomic():
        sub = HomeworkSubmission.objects.select_for_update().select_related("lesson__topic").get(pk=sub.pk)
        sub.score, sub.comment = score, (comment or "").strip()[:2000]
        sub.status, sub.checked_by, sub.checked_at = HomeworkSubmission.Status.CHECKED, user, timezone.now()
        given = 0
        if not sub.coins and sub.on_time and score >= PASS_SCORE:
            topic = sub.lesson.topic.title if sub.lesson.topic else sub.lesson.held_on.strftime("%d.%m")
            CoinTransaction.objects.create(
                student_id=sub.student_id, amount=COINS, reason=REASON.format(topic=topic)[:120]
            )
            sub.coins = given = COINS
        sub.save()
    return given


def lesson_overview(lesson: Lesson) -> list[dict]:
    """Dars sahifasi uchun: guruhning faol o'quvchilari va ularning topshirig'i (bo'lmasa — None)."""
    subs = {s.student_id: s for s in lesson.submissions.all()}
    students = lesson.group.students.filter(status=Student.Status.ACTIVE).order_by("full_name")
    return [{"student": s, "submission": subs.get(s.pk)} for s in students]
