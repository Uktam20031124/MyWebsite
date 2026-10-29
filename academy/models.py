import random
import re
import secrets
from datetime import date, time, timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language, gettext, gettext_noop
from django.utils.translation import gettext_lazy as _

MAX_SCORE = 100

# Hafta kunlari: date.weekday() bilan bir xil (0 — dushanba).
WEEKDAYS = [
    (0, gettext_noop("Dushanba"), gettext_noop("Du")),
    (1, gettext_noop("Seshanba"), gettext_noop("Se")),
    (2, gettext_noop("Chorshanba"), gettext_noop("Chor")),
    (3, gettext_noop("Payshanba"), gettext_noop("Pay")),
    (4, gettext_noop("Juma"), gettext_noop("Ju")),
    (5, gettext_noop("Shanba"), gettext_noop("Sha")),
    (6, gettext_noop("Yakshanba"), gettext_noop("Ya")),
]
# Formadagi tanlovlar — so'rov paytida tarjima qilinadi.
WEEKDAY_CHOICES = [(n, _(full)) for n, full, _short in WEEKDAYS]
WEEKDAY_SHORT = {n: short for n, _full, short in WEEKDAYS}


def format_schedule(days: list[int], starts: time | None, ends: time | None) -> str:
    """[1, 4, 5], 14:00, 15:00 -> "Se / Ju / Sha 14:00–15:00"."""
    text = " / ".join(gettext(WEEKDAY_SHORT[d]) for d in sorted(days))
    if starts:
        text += f" {starts:%H:%M}" + (f"–{ends:%H:%M}" if ends else "")
    return text.strip()


class Group(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Faol")
        PAUSED = "paused", _("To'xtatilgan")
        ARCHIVED = "archived", _("Arxiv")

    name = models.CharField(_("Nomi"), max_length=120)
    code = models.CharField(_("Kod"), max_length=32, unique=True)
    schedule = models.CharField(
        _("Jadval"),
        max_length=200,
        blank=True,
        help_text=_("Dars kunlari va vaqti tanlansa, avtomatik to'ldiriladi."),
    )
    days = models.CharField(
        _("Dars kunlari"),
        max_length=20,
        blank=True,
        help_text=_("Hafta kunlari raqamlari (0 — dushanba), vergul bilan: 1,4,5"),
    )
    starts_at = models.TimeField(_("Boshlanish vaqti"), null=True, blank=True)
    ends_at = models.TimeField(_("Tugash vaqti"), null=True, blank=True)
    room = models.CharField(_("Xona"), max_length=80, blank=True)
    start_date = models.DateField(_("Boshlanish"), null=True, blank=True)
    status = models.CharField(
        _("Holat"),
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    notes = models.TextField(_("Izoh"), blank=True)
    # O'quvchilar o'z Telegram/telefonini kiritadigan ochiq havola kaliti (bo'sh — o'chiq).
    contact_token = models.CharField(max_length=32, blank=True, editable=False, db_index=True)
    # Guruhning Telegram chati (@username yoki raqamli ID) — haftalik reyting uchun.
    telegram_chat = models.CharField(
        _("Telegram guruh chati"),
        max_length=100,
        blank=True,
        help_text=_("@guruh_nomi, t.me/guruh_nomi yoki raqamli ID (manage.py telegram_chats)."),
    )
    # Guruh o'qituvchisi (bo'sh — bosh ustoz). O'qituvchi faqat o'z guruhlarini ko'radi va ularga
    # testlarni o'z Telegramidan yuboradi.
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_groups",
        verbose_name=_("O‘qituvchi"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Guruh")
        verbose_name_plural = _("Guruhlar")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("group_detail", args=[self.pk])

    def save(self, *args, **kwargs):
        if self.day_list:
            self.schedule = format_schedule(self.day_list, self.starts_at, self.ends_at)
        super().save(*args, **kwargs)

    @property
    def day_list(self) -> list[int]:
        return sorted({int(d) for d in self.days.split(",") if d.strip().isdigit()} & set(range(7)))

    @property
    def has_timetable(self) -> bool:
        """Jadvali tuzilgan (kunlar + boshlanish vaqti) — kalendarda ko'rinadi."""
        return bool(self.day_list and self.starts_at)

    def meets_on(self, day: date) -> bool:
        return self.has_timetable and day.weekday() in self.day_list

    @property
    def active_students(self):
        return self.students.filter(status=Student.Status.ACTIVE)

    def next_syllabus_item(self):
        """Dasturdagi navbatdagi (hali o'tilmagan) mavzu."""
        return (
            self.syllabus.filter(status=SyllabusItem.Status.PLANNED)
            .select_related("topic")
            .first()
        )

    def add_topics(self, topics) -> int:
        """Mavzularni dastur oxiriga qo'shadi; mavjudlarini o'tkazib yuboradi."""
        with transaction.atomic():
            existing = set(self.syllabus.values_list("topic_id", flat=True))
            order = self.syllabus.aggregate(m=Max("order"))["m"] or 0
            new_items = []
            for topic in topics:
                if topic.pk in existing:
                    continue
                order += 1
                existing.add(topic.pk)
                new_items.append(SyllabusItem(group=self, topic=topic, order=order))
            SyllabusItem.objects.bulk_create(new_items)
        return len(new_items)


def initials_of(full_name: str) -> str:
    """Avatar uchun bosh harflar: "Aliyev Vali" → "AV"."""
    parts = full_name.split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


class QuizLanguage(models.TextChoices):
    """Test qaysi tilda yechiladi (savollar, sahifa matnlari, xabar)."""

    UZ = "uz", _("O‘zbekcha")
    RU = "ru", _("Русский")


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Faol")
        PAUSED = "paused", _("Tanaffus")
        GRADUATED = "graduated", _("Bitirgan")
        DROPPED = "dropped", _("Ketgan")

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name=_("Guruh"),
    )
    full_name = models.CharField(_("F.I.Sh."), max_length=160)
    phone = models.CharField(_("Telefon"), max_length=40, blank=True)
    telegram = models.CharField(_("Telegram"), max_length=80, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    # Test jo'natishda shu til oldindan tanlanadi (har safar o'zgartirish mumkin).
    quiz_language = models.CharField(
        _("Test tili"), max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ
    )
    # Profil (shaxsiy sahifa): o'quvchi kirishga so'rov yuboradi, ustoz vaqt bilan ruxsat beradi.
    profile_requested_at = models.DateTimeField(_("Profilga kirish so'ralgan"), null=True, blank=True)
    profile_until = models.DateTimeField(_("Profil ochiq (gacha)"), null=True, blank=True)
    # O'quvchi o'zi test so'ray oladigan mavzular (ustoz belgilaydi).
    allowed_topics = models.ManyToManyField(
        "Topic", blank=True, related_name="allowed_students", verbose_name=_("Test uchun ruxsat etilgan mavzular")
    )
    status = models.CharField(
        _("Holat"),
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    joined_at = models.DateField(_("Qo'shilgan"), default=timezone.localdate)
    notes = models.TextField(_("Izoh"), blank=True)
    # O'quvchining shaxsiy natijalar sahifasi kaliti (/men/<kalit>/); bo'sh — hali yaratilmagan.
    portal_token = models.CharField(max_length=32, blank=True, editable=False, db_index=True)
    # "A'lochi" unvoni (do'kondan olingan yoki ustoz bergan): ism hamma joyda oltin, medal bilan.
    honor_since = models.DateTimeField(_("A’lochi (berilgan sana)"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = _("Shogird")
        verbose_name_plural = _("Shogirdlar")
        indexes = [
            models.Index(fields=["group", "status"]),
        ]

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self):
        return reverse("student_detail", args=[self.pk])

    def initials(self) -> str:
        return initials_of(self.full_name)

    def profile_is_open(self) -> bool:
        """Profilga kirish ruxsati hozir amaldami (``profiles.is_open`` bilan bir xil)."""
        return bool(self.profile_until and self.profile_until > timezone.now())

    def save(self, *args, **kwargs):
        self.telegram = self.telegram.strip().lstrip("@")
        super().save(*args, **kwargs)


class Module(models.Model):
    """Mavzular bo'limi (kurs qismi): masalan, "Python asoslari"."""

    title = models.CharField(_("Bo'lim"), max_length=160, unique=True)
    description = models.TextField(_("Tavsif"), blank=True)
    order = models.PositiveIntegerField(_("Tartib"), default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = _("Bo'lim")
        verbose_name_plural = _("Bo'limlar")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return f"{reverse('topic_list')}?module={self.pk}"


class Topic(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        related_name="topics",
        verbose_name=_("Bo'lim"),
        null=True,
        blank=True,
    )
    title = models.CharField(_("Mavzu"), max_length=200)
    title_ru = models.CharField(
        _("Mavzu (ruscha)"), max_length=200, blank=True, help_text=_("Ruscha testlarda ko'rsatiladi.")
    )
    description = models.TextField(_("Tavsif"), blank=True)
    homework = models.TextField(
        _("Uyga vazifa (shablon)"),
        blank=True,
        help_text=_("Shu mavzuda dars yaratilganda avtomatik qo'yiladi."),
    )
    resources = models.TextField(
        _("Materiallar"),
        blank=True,
        help_text=_("Har qatorda bitta havola yoki manba."),
    )
    study = models.TextField(
        _("Mustahkamlash materiali"),
        blank=True,
        help_text=_(
            "O'quvchi testdan past natija olsa, profilida ko'rinadi: tushuntirish, bajarilgan misollar. "
            "Format: ## sarlavha, - ro'yxat, ``` kod ```, **qalin**, `kod`."
        ),
    )
    study_ru = models.TextField(
        _("Mustahkamlash materiali (ruscha)"),
        blank=True,
        help_text=_("Ruscha test tanlagan o'quvchilarga ko'rsatiladi (bo'sh — o'zbekchasi)."),
    )
    slides = models.TextField(
        _("Taqdimot slaydlari"),
        blank=True,
        help_text=_(
            "Dars paytida ekranga chiqariladi. Slaydlar orasida --- qatori; # sarlavha slaydi; "
            "!! katta ibora; :: timer 25 — 25 daqiqalik taymer; qolgani — material formati."
        ),
    )
    duration_minutes = models.PositiveIntegerField(_("Davomiyligi (daq.)"), default=90)
    order = models.PositiveIntegerField(_("Tartib"), default=0, db_index=True)
    is_active = models.BooleanField(_("Faol"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["module__order", "module__title", "order", "title"]
        verbose_name = _("Mavzu")
        verbose_name_plural = _("Mavzular")
        constraints = [
            models.UniqueConstraint(
                fields=["module", "title"], name="uniq_topic_title_per_module"
            ),
        ]

    def __str__(self) -> str:
        return self.title_in(get_language())

    def get_absolute_url(self):
        return reverse("topic_detail", args=[self.pk])

    def title_in(self, lang: str) -> str:
        return self.title_ru if lang == QuizLanguage.RU and self.title_ru else self.title

    def study_in(self, lang: str) -> str:
        return self.study_ru if lang == QuizLanguage.RU and self.study_ru else self.study

    def resource_list(self) -> list[dict]:
        items = []
        for line in self.resources.splitlines():
            line = line.strip()
            if not line:
                continue
            is_link = line.startswith(("http://", "https://"))
            items.append({"text": line, "url": line if is_link else ""})
        return items


class SyllabusItem(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", _("Rejada")
        TAUGHT = "taught", _("O'tildi")
        SKIPPED = "skipped", _("O'tkazib yuborildi")

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="syllabus",
        verbose_name=_("Guruh"),
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="syllabus_items",
        verbose_name=_("Mavzu"),
    )
    order = models.PositiveIntegerField(_("Tartib"), default=0)
    status = models.CharField(
        _("Holat"),
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True,
    )
    taught_on = models.DateField(_("O'tilgan sana"), null=True, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Guruh mavzusi")
        verbose_name_plural = _("Guruh mavzulari")
        constraints = [
            models.UniqueConstraint(
                fields=["group", "topic"], name="uniq_syllabus_group_topic"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.group.code}: {self.topic.title}"

    def move(self, direction: str) -> bool:
        """Elementni yuqoriga ("up") yoki pastga ("down") siljitadi."""
        siblings = self.group.syllabus.all()
        if direction == "up":
            other = siblings.filter(order__lt=self.order).order_by("-order", "-id").first()
        else:
            other = siblings.filter(order__gt=self.order).order_by("order", "id").first()
        if other is None:
            return False
        with transaction.atomic():
            self.order, other.order = other.order, self.order
            self.save(update_fields=["order"])
            other.save(update_fields=["order"])
        return True


class Lesson(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", _("Rejada")
        COMPLETED = "completed", _("O'tildi")
        CANCELLED = "cancelled", _("Bekor")

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Guruh"),
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name=_("Mavzu"),
        null=True,
        blank=True,
    )
    held_on = models.DateField(_("Sana"), db_index=True)
    starts_at = models.TimeField(_("Boshlanish"), null=True, blank=True)
    status = models.CharField(
        _("Holat"),
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True,
    )
    homework = models.TextField(_("Uyga vazifa"), blank=True)
    notes = models.TextField(_("Dars izohi"), blank=True)
    # Darsni o'tgan o'qituvchi (guruh o'qituvchisidan avtomatik). Guruh keyin boshqa o'qituvchiga
    # o'tsa ham, hisobot va maosh shu yerdan olinadi. Bo'sh — bosh ustoz.
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taught_lessons",
        verbose_name=_("O‘qituvchi"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-held_on", "-starts_at"]
        verbose_name = _("Dars")
        verbose_name_plural = _("Darslar")
        indexes = [
            models.Index(fields=["group", "held_on"]),
        ]

    def __str__(self) -> str:
        title = self.topic.title_in(get_language()) if self.topic else gettext("Mavzusiz dars")
        return f"{self.group.code} · {self.held_on:%d.%m.%Y} · {title}"

    def get_absolute_url(self):
        return reverse("lesson_detail", args=[self.pk])

    def save(self, *args, **kwargs):
        previous = None
        if self.pk:
            previous = (
                Lesson.objects.filter(pk=self.pk)
                .values_list("group_id", "topic_id", "status")
                .first()
            )
        if self.teacher_id is None and self.group_id:
            # O'qituvchi — guruhniki (dars yaratilganda yoki o'tilganda).
            self.teacher_id = Group.objects.filter(pk=self.group_id).values_list("teacher_id", flat=True).first()
            fields = kwargs.get("update_fields")
            if fields is not None and self.teacher_id:
                kwargs["update_fields"] = {*fields, "teacher"}
        super().save(*args, **kwargs)
        # Dars qaysi yo'l bilan "o'tildi" bo'lmasin (forma, yo'qlama, tugma),
        # guruh dasturi bir xil tarzda yangilanadi. Dars "o'tildi"dan qaytarilsa
        # yoki mavzusi/guruhi almashsa, eski mavzu ham qayta hisoblanadi.
        if previous and previous[2] == self.Status.COMPLETED:
            if previous != (self.group_id, self.topic_id, self.status):
                resync_syllabus_item(previous[0], previous[1])
        if self.status == self.Status.COMPLETED:
            resync_syllabus_item(self.group_id, self.topic_id)

    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.save(update_fields=["status"])


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", _("Keldi")
        ABSENT = "absent", _("Kelmadi")
        LATE = "late", _("Kechikdi")
        EXCUSED = "excused", _("Sababli")

    # Davomat foizida "keldi" deb hisoblanadigan holatlar.
    ATTENDED = (Status.PRESENT, Status.LATE)

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("Dars"),
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name=_("Shogird"),
    )
    status = models.CharField(
        _("Holat"),
        max_length=16,
        choices=Status.choices,
        default=Status.PRESENT,
    )
    note = models.CharField(_("Izoh"), max_length=200, blank=True)
    score = models.PositiveSmallIntegerField(
        _("Ball (0–100)"),
        null=True,
        blank=True,
        validators=[MaxValueValidator(MAX_SCORE)],
        help_text=_("Darsdagi faollik va uy vazifasi uchun baho. Bo'sh — baholanmagan."),
    )

    class Meta:
        verbose_name = _("Yo'qlama")
        verbose_name_plural = _("Yo'qlamalar")
        constraints = [
            models.UniqueConstraint(
                fields=["lesson", "student"], name="uniq_attendance_lesson_student"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.student} — {self.get_status_display()}"


def resync_syllabus_item(group_id, topic_id) -> None:
    """Guruh dasturidagi mavzu holatini "o'tildi" darslarga moslaydi.

    O'tilgan dars bo'lsa — "o'tildi" (sana: eng so'nggi dars). Bo'lmasa, faqat
    darsdan kelib chiqqan "o'tildi" holati "rejada"ga qaytadi; "o'tkazib
    yuborildi" kabi qo'lda qo'yilgan holatlarga tegilmaydi.
    """
    if not topic_id:
        return
    items = SyllabusItem.objects.filter(group_id=group_id, topic_id=topic_id)
    last = Lesson.objects.filter(
        group_id=group_id, topic_id=topic_id, status=Lesson.Status.COMPLETED
    ).aggregate(d=Max("held_on"))["d"]
    if last:
        items.update(status=SyllabusItem.Status.TAUGHT, taught_on=last)
    else:
        items.filter(status=SyllabusItem.Status.TAUGHT).update(
            status=SyllabusItem.Status.PLANNED, taught_on=None
        )


# Guruh reytingidagi 1–3-o'rinlar keshi (``engagement.podium_places``): quvvat yoki o'quvchi
# (guruh, holat) o'zgarsa — darhol yangilanadi.
PODIUM_CACHE_KEY = "academy:podium"


def _podium_changed(sender, **kwargs):
    from django.core.cache import cache

    cache.delete(PODIUM_CACHE_KEY)


@receiver(post_delete, sender=Lesson)
def _lesson_deleted(sender, instance, **kwargs):
    if instance.status == Lesson.Status.COMPLETED:
        resync_syllabus_item(instance.group_id, instance.topic_id)


# --- Testlar ----------------------------------------------------------------


class Quiz(models.Model):
    """Mavzu bo'yicha savollar banki: jo'natishda undan tasodifiy savollar tanlanadi."""

    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        related_name="quiz",
        verbose_name=_("Mavzu"),
    )
    time_limit_minutes = models.PositiveSmallIntegerField(
        _("Vaqt (daq.)"),
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        help_text=_("Jo'natishda taklif qilinadigan vaqt. Har bir jo'natmada o'zgartirish mumkin."),
    )
    BONUS_CHOICES = [(n, f"{n} ⚡️") for n in range(1, 6)]
    bonus_quvvat = models.PositiveSmallIntegerField(
        _("Qo‘shimcha savol uchun quvvat"),
        choices=BONUS_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_("O‘quvchi profilidagi “Qo‘shimcha savollar”da shu testning savoliga to‘g‘ri javob uchun."),
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Testlar")

    def __str__(self) -> str:
        return f"Test: {self.topic.title}"

    def as_text(self) -> str:
        """Savollarni tahrirlash formatiga qaytaradi (`parse_quiz` teskarisi)."""
        blocks = []
        for q in self.questions.prefetch_related("choices"):
            lines = [f"? {q.text}"]
            lines += [f"{'+' if c.is_correct else '-'} {c.text}" for c in q.choices.all()]
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks)

    def as_text_ru(self) -> str:
        """Ruscha tarjima tahrirlash formatida; tarjima qilinmagan joylar — o'zbekchasi.
        Hech narsa tarjima qilinmagan bo'lsa — bo'sh."""
        questions = list(self.questions.prefetch_related("choices"))
        if not any(q.text_ru or any(c.text_ru for c in q.choices.all()) for q in questions):
            return ""
        ru = QuizLanguage.RU
        blocks = []
        for q in questions:
            lines = [f"? {q.text_in(ru)}"]
            lines += [f"{'+' if c.is_correct else '-'} {c.text_in(ru)}" for c in q.choices.all()]
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks)

    def apply_translation(self, translated) -> int:
        """Ruscha tarjimani savollarga tartib bo'yicha yozadi (`translation_errors` bilan
        tekshirilgan bo'lishi kerak). O'zbekchasi bilan bir xil matn — "tarjima yo'q".
        Bo'sh ro'yxat — barcha tarjimalar o'chiriladi. Natija: tarjimasi bor savollar soni."""
        with transaction.atomic():
            if not translated:
                Question.objects.filter(quiz=self).update(text_ru="")
                Choice.objects.filter(question__quiz=self).update(text_ru="")
                return 0
            done = 0
            for q, (text, choices) in zip(self.questions.prefetch_related("choices"), translated, strict=False):
                value = "" if text == q.text else text
                if value != q.text_ru:
                    q.text_ru = value
                    q.save(update_fields=["text_ru"])
                done += bool(q.text_ru)
                for c, (ru, _ok) in zip(q.choices.all(), choices, strict=False):
                    value = "" if ru == c.text else ru
                    if value != c.text_ru:
                        c.text_ru = value
                        c.save(update_fields=["text_ru"])
            return done

    @property
    def translated_count(self) -> int:
        return self.questions.exclude(text_ru="").count()

    def replace_questions(self, parsed) -> None:
        """Savollarni `parse_quiz` natijasi bilan almashtiradi.

        O'zgarmagan savollar (matni va variantlari bir xil) saqlanib qoladi — ularning
        id'lari yechilayotgan testlarda ishlatiladi, shuning uchun tahrir ularni buzmaydi.
        """
        with transaction.atomic():
            existing: dict[tuple, Question] = {}
            for q in self.questions.prefetch_related("choices"):
                existing.setdefault(q.signature(), q)
            keep = []
            for order, (text, choices) in enumerate(parsed, start=1):
                question = existing.pop((text, tuple(choices)), None)
                if question is not None:
                    if question.order != order:
                        question.order = order
                        question.save(update_fields=["order"])
                else:
                    question = Question.objects.create(quiz=self, text=text, order=order)
                    Choice.objects.bulk_create(
                        Choice(question=question, text=c, is_correct=ok, order=i)
                        for i, (c, ok) in enumerate(choices, start=1)
                    )
                keep.append(question.pk)
            self.questions.exclude(pk__in=keep).delete()


def question_image_path(instance, filename: str) -> str:
    """Taxmin qilib bo'lmaydigan nom: quiz/<tasodifiy>.<kengaytma>."""
    ext = filename.rsplit(".", 1)[-1].lower()[:5] if "." in filename else "bin"
    return f"quiz/{secrets.token_urlsafe(12)}.{ext}"


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name=_("Test")
    )
    text = models.TextField(_("Savol"))
    # Ruscha tarjima (bo'sh — tarjima qilinmagan, o'zbekchasi ko'rsatiladi).
    text_ru = models.TextField(_("Savol (ruscha)"), blank=True)
    order = models.PositiveIntegerField(_("Tartib"), default=0)
    image = models.FileField(_("Rasm"), upload_to=question_image_path, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Savol")
        verbose_name_plural = _("Savollar")

    def __str__(self) -> str:
        return self.text[:80]

    @property
    def title(self) -> str:
        """Savolning birinchi qatori."""
        return self.text.split("\n", 1)[0]

    @property
    def code(self) -> str:
        """Birinchi qatordan keyingi qismi (odatda kod) — chekinishlari bilan."""
        parts = self.text.split("\n", 1)
        return parts[1] if len(parts) > 1 else ""

    def signature(self) -> tuple:
        return (self.text, tuple((c.text, c.is_correct) for c in self.choices.all()))

    def text_in(self, lang: str) -> str:
        return self.text_ru if lang == QuizLanguage.RU and self.text_ru else self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices", verbose_name=_("Savol")
    )
    text = models.CharField(_("Javob"), max_length=500)
    text_ru = models.CharField(_("Javob (ruscha)"), max_length=500, blank=True)
    is_correct = models.BooleanField(_("To'g'ri"), default=False)
    order = models.PositiveIntegerField(_("Tartib"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Javob varianti")
        verbose_name_plural = _("Javob variantlari")

    def __str__(self) -> str:
        return self.text

    def text_in(self, lang: str) -> str:
        return self.text_ru if lang == QuizLanguage.RU and self.text_ru else self.text


class QuizBatch(models.Model):
    """Test jo'natmasi: bitta mavzu testi, tanlangan shogirdlar, savollar soni va vaqt."""

    MAX_TIME_LIMIT = 180

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="batches", verbose_name=_("Test")
    )
    # Dars o'chirilsa ham natijalar saqlanib qoladi.
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_batches",
        verbose_name=_("Dars"),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_batches",
        verbose_name=_("Guruh"),
    )
    question_count = models.PositiveSmallIntegerField(
        _("Savollar soni"), validators=[MinValueValidator(1)]
    )
    time_limit_minutes = models.PositiveSmallIntegerField(
        _("Vaqt (daq.)"), validators=[MinValueValidator(1), MaxValueValidator(MAX_TIME_LIMIT)]
    )
    created_at = models.DateTimeField(_("Jo'natilgan"), auto_now_add=True)
    # Belgilangan vaqtda yuborish (manage.py send_scheduled); bo'sh — darhol.
    scheduled_at = models.DateTimeField(_("Yuborish vaqti"), null=True, blank=True)
    scheduled_sent_at = models.DateTimeField(_("Rejali yuborilgan"), null=True, blank=True)
    # Havolalar qaysi kanallar orqali yuboriladi (rejalashtirilgan yuborish uchun): "telegram,email".
    channels = models.CharField(_("Kanallar"), max_length=32, default="telegram", blank=True)
    # O'quvchi profilidan (ustoz ruxsati bilan) o'zi boshlagan test.
    from_profile = models.BooleanField(_("Profildan"), default=False)
    # Kim jo'natgan: havolalar (rejalashtirilganlari ham) o'sha o'qituvchining Telegramidan ketadi.
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_batches",
        verbose_name=_("Jo‘natgan"),
    )
    retake_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="retakes",
        verbose_name=_("Qayta topshirish (asosiy jo'natma)"),
    )

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("Test jo'natmasi")
        verbose_name_plural = _("Test jo'natmalari")

    def __str__(self) -> str:
        return f"{self.quiz.topic.title} · {self.created_at:%d.%m.%Y %H:%M}"

    def get_absolute_url(self):
        return reverse("quiz_batch", args=[self.pk])

    # Quyidagilar `services.annotate_batches` qo'shgan maydonlardan hisoblanadi.
    @property
    def avg_percent(self):
        total = getattr(self, "total_sum", None)
        return round(100 * (self.correct_sum or 0) / total) if total else None

    @property
    def progress(self) -> int:
        sent = getattr(self, "sent_n", 0)
        return round(100 * self.done_n / sent) if sent else 0


def new_attempt_token() -> str:
    return secrets.token_urlsafe(16)


class AttemptScoringMixin:
    """Test urinishining umumiy mantig'i: savol tanlash, vaqt, baholash, javoblar tahlili.

    Model quyidagi maydonlarga ega bo'lishi kerak: quiz, language, question_ids, answers,
    snapshot, deadline, status (Status.FINISHED), finished_at, timed_out, correct, total.
    ``QuizAttempt`` (o'quvchiga shaxsiy havola) va ``OpenAttempt`` (umumiy havola) ishlatadi.
    """

    # Vaqt tugash paytida yuborilgan javoblar tarmoq kechikishi bilan kelsa ham qabul qilinadi.
    GRACE_SECONDS = 15

    @property
    def warning_count(self) -> int:
        """Test paytidagi ogohlantirishlar: oynadan chiqish + nusxalash urinishlari."""
        return self.leave_count + self.copy_count

    @property
    def percent(self):
        if not self.total:
            return None
        return round(100 * (self.correct or 0) / self.total)

    def seconds_left(self, now=None) -> int:
        if not self.deadline:
            return 0
        now = now or timezone.now()
        return max(0, int((self.deadline - now).total_seconds()))

    def is_expired(self, now=None, grace: int = 0) -> bool:
        now = now or timezone.now()
        return bool(self.deadline) and now > self.deadline + timedelta(seconds=grace)

    def pick_questions(self, count: int, prefer=()) -> list[int]:
        """Bankdan tasodifiy ``count`` ta savol; ``prefer`` dagilardan yarmigacha albatta tushadi."""
        pool = list(self.quiz.questions.values_list("pk", flat=True))
        count = min(count, len(pool))
        if self.language == QuizLanguage.RU:
            # Tarjimasi bor savollar yetarli bo'lsa — faqat ulardan (aralash til bo'lmasin).
            translated = list(self.quiz.questions.exclude(text_ru="").values_list("pk", flat=True))
            if len(translated) >= count:
                pool = translated
        rng = random.SystemRandom()
        pool_set = set(pool)
        prefer = [q for q in prefer if q in pool_set]
        again = rng.sample(prefer, min(len(prefer), count // 2))
        rest = [q for q in pool if q not in set(again)]
        picked = again + rng.sample(rest, count - len(again))
        rng.shuffle(picked)
        return picked

    def questions(self):
        """O'quvchiga tushgan savollar (eski havolalarda — bankning hammasi)."""
        qs = self.quiz.questions.all()
        return qs.filter(pk__in=self.question_ids) if self.question_ids else qs

    def build_review(self) -> list[dict]:
        """O'quvchiga tushgan savollar, variantlar, tanlagani va to'g'ri javob — hozirgi
        savollar bankidan. Tartib — o'quvchiga berilgan tartib (question_ids)."""
        question_ids = self.question_ids or list(self.quiz.questions.values_list("pk", flat=True))
        questions = {
            q.pk: q for q in Question.objects.filter(pk__in=question_ids).prefetch_related("choices")
        }
        review = []
        for qid in question_ids:
            picked = _as_int(self.answers.get(str(qid)))
            q = questions.get(qid)
            if q is None:
                # Test yechilayotganda o'chirilgan savol ham umumiy songa kiradi (javobsiz).
                review.append({"id": qid, "text": "", "missing": True, "choices": [],
                               "picked": picked, "is_correct": False})
                continue
            choices = [
                {"id": c.pk, "text": c.text, "text_ru": c.text_ru, "correct": c.is_correct}
                for c in q.choices.all()
            ]
            review.append({
                "id": qid,
                "text": q.text,
                "text_ru": q.text_ru,
                "image": q.image.url if q.image else "",
                "choices": choices,
                "picked": picked,
                "is_correct": any(c["correct"] and c["id"] == picked for c in choices),
            })
        return review

    def review(self, lang: str = QuizLanguage.UZ) -> list[dict]:
        """Javoblar tahlili: yakunlanganda saqlangan nusxa (keyinchalik test tahrirlansa
        ham o'zgarmaydi); eski natijalarda — hozirgi bankdan. `lang` — matnlar tili
        (tarjimasi bo'lmasa o'zbekchasi)."""

        def pick(d):
            return d.get("text_ru") or d["text"] if lang == QuizLanguage.RU else d["text"]

        # Nusxa: ko'rsatish uchun qo'shilgan maydonlar bazadagi snapshot'ga tushmasin.
        items = [dict(item) for item in (self.snapshot or self.build_review())]
        for item in items:
            title, _sep, code = (pick(item) if item["text"] else "").partition("\n")
            item["title"], item["code"] = title, code
            item["answered"] = item["picked"] is not None
            item["correct_text"] = next((pick(c) for c in item["choices"] if c["correct"]), "")
            item["picked_text"] = next(
                (pick(c) for c in item["choices"] if c["id"] == item["picked"]), ""
            )
        return items

    def on_finished(self) -> None:
        """Yakunlangandan keyingi qo'shimcha ish (tranzaksiya ichida) — modelda qayta yoziladi."""

    def finish(self, answers: dict | None = None, timed_out: bool = False) -> None:
        """Javoblarni baholab, testni yakunlaydi. `answers`: {savol_id: variant_id}."""
        model = type(self)
        with transaction.atomic():
            attempt = model.objects.select_for_update().get(pk=self.pk)
            if attempt.status == model.Status.FINISHED:
                self.refresh_from_db()
                return
            if answers is not None:
                attempt.answers = answers
            # Baholash va ustoz ko'radigan javoblar tahlili — bitta nusxadan.
            attempt.snapshot = attempt.build_review()
            attempt.correct = sum(item["is_correct"] for item in attempt.snapshot)
            attempt.total = len(attempt.snapshot)
            attempt.status = model.Status.FINISHED
            attempt.finished_at = timezone.now()
            attempt.timed_out = timed_out
            attempt.save()
            attempt.on_finished()
        self.refresh_from_db()


class QuizAttempt(AttemptScoringMixin, models.Model):
    """Bitta o'quvchi uchun bir martalik test havolasi."""

    COOKIE_PREFIX = "quiz_"

    class Status(models.TextChoices):
        PENDING = "pending", _("Ochilmagan")
        ACTIVE = "active", _("Yechilmoqda")
        FINISHED = "finished", _("Tugatgan")

    class Reveal(models.TextChoices):
        """O'quvchi o'z javoblarini (to'g'ri/xato) ko'rishi: bir marta 1 daqiqa o'zi, keyin —
        faqat ustoz ruxsati bilan."""

        NONE = "", _("So‘ralmagan")
        PREVIEW = "preview", _("1 daqiqa ko‘rdi")
        REQUESTED = "requested", _("So‘ralgan")
        APPROVED = "approved", _("Ruxsat berilgan")
        REJECTED = "rejected", _("Rad etilgan")

    batch = models.ForeignKey(
        QuizBatch, on_delete=models.CASCADE, related_name="attempts", verbose_name=_("Jo'natma")
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts", verbose_name=_("Test")
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="quiz_attempts", verbose_name=_("Shogird")
    )
    token = models.CharField(max_length=32, unique=True, default=new_attempt_token, editable=False)
    status = models.CharField(
        _("Holat"), max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    language = models.CharField(
        _("Til"), max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ
    )
    # Testni boshlagan brauzer kaliti (cookie): havola boshqa joyda qayta ochilmaydi.
    owner_key = models.CharField(max_length=64, blank=True, editable=False)
    # Boshlanganda bankdan tasodifiy tanlangan savollar (har bir o'quvchida o'zicha).
    question_ids = models.JSONField(_("Savollar"), default=list, blank=True, editable=False)
    # Test paytida boshqa oyna/ilovaga o'tishlar (ko'chirishga qarshi qayd) — faqat ustozga.
    leave_count = models.PositiveSmallIntegerField(_("Chiqib ketishlar"), default=0)
    away_seconds = models.PositiveIntegerField(_("Tashqarida (s)"), default=0)
    # Nusxalash/qo'yish/sichqoncha o'ng tugmasi urinishlari (bloklanadi va qayd qilinadi).
    copy_count = models.PositiveSmallIntegerField(_("Nusxalash urinishlari"), default=0)
    # Ustoz ogohlantirishlarni ko'rib chiqdi: jarima (0 — kechirildi) va qachon.
    penalty = models.PositiveSmallIntegerField(_("Jarima ⚡️"), default=0)
    warning_checked_at = models.DateTimeField(_("Ogohlantirish ko'rib chiqilgan"), null=True, blank=True)
    answers = models.JSONField(_("Javoblar"), default=dict, blank=True)
    # Yakunlanganda: savollar, variantlar, tanlangani va to'g'ri javob nusxasi — faqat
    # ustoz ko'radi; test keyinchalik tahrirlansa ham natija tahlili o'zgarmaydi.
    snapshot = models.JSONField(_("Javoblar tahlili"), default=list, blank=True, editable=False)
    started_at = models.DateTimeField(_("Boshlangan"), null=True, blank=True)
    deadline = models.DateTimeField(_("Tugash vaqti"), null=True, blank=True)
    finished_at = models.DateTimeField(_("Tugagan"), null=True, blank=True)
    timed_out = models.BooleanField(_("Vaqt tugadi"), default=False)
    correct = models.PositiveSmallIntegerField(_("To'g'ri javoblar"), null=True, blank=True)
    total = models.PositiveSmallIntegerField(_("Savollar soni"), null=True, blank=True)
    # Ustozning Telegram akkauntidan yuborilgan payt va oxirgi xato (bo'lsa).
    sent_at = models.DateTimeField(_("Telegramda yuborilgan"), null=True, blank=True)
    # Ochilmagan test haqida bitta avtomatik eslatma (manage.py quiz_reminders).
    reminded_at = models.DateTimeField(_("Eslatma yuborilgan"), null=True, blank=True)
    # Email (Gmail) orqali yuborilgan payt va oxirgi xato (bo'lsa).
    email_sent_at = models.DateTimeField(_("Emailga yuborilgan"), null=True, blank=True)
    email_error = models.CharField(_("Email xatosi"), max_length=255, blank=True)
    reveal = models.CharField(
        _("Javoblarni ko'rish"), max_length=12, choices=Reveal.choices, default=Reveal.NONE,
        blank=True, db_index=True,
    )
    reveal_requested_at = models.DateTimeField(_("Ko'rish so'ralgan"), null=True, blank=True)
    reveal_decided_at = models.DateTimeField(_("Ustoz qarori"), null=True, blank=True)
    # Bir martalik bepul ko'rish (PREVIEW) shu paytgacha.
    reveal_until = models.DateTimeField(_("Ko'rish (gacha)"), null=True, blank=True)
    send_error = models.CharField(_("Yuborish xatosi"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__full_name"]
        verbose_name = _("Test havolasi")
        verbose_name_plural = _("Test havolalari")
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "student"], name="uniq_quiz_attempt_batch_student"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.student} — {self.quiz}"

    def get_absolute_url(self):
        return reverse("quiz_take", args=[self.token])

    @property
    def time_limit_minutes(self) -> int:
        return self.batch.time_limit_minutes

    @property
    def question_count(self) -> int:
        """O'quvchi oladigan savollar soni (bankdagidan ko'p bo'lmaydi)."""
        if self.question_ids:
            return len(self.question_ids)
        return min(self.batch.question_count, self.quiz.questions.count())

    def start(self, owner_key: str) -> bool:
        """Testni boshlaydi va savollarni tanlaydi. Faqat birinchi chaqiruv muvaffaqiyatli."""
        now = timezone.now()
        # Xato qilingan savollardan yarmigacha albatta tushadi (qolgani bankdan tasodifiy).
        mistakes = Mistake.objects.filter(
            student_id=self.student_id, question__quiz_id=self.quiz_id, resolved_at__isnull=True
        ).values_list("question_id", flat=True)
        picked = self.pick_questions(self.batch.question_count, prefer=list(mistakes))
        started = QuizAttempt.objects.filter(pk=self.pk, status=self.Status.PENDING).update(
            status=self.Status.ACTIVE,
            owner_key=owner_key,
            question_ids=picked,
            started_at=now,
            deadline=now + timedelta(minutes=self.batch.time_limit_minutes),
        )
        self.refresh_from_db()
        return bool(started)

    # O'quvchi javoblarini ustoz ruxsatisiz ko'rishi mumkin bo'lgan vaqt (bir marta).
    PREVIEW_SECONDS = 60

    @property
    def preview_seconds_left(self) -> int:
        if self.reveal != self.Reveal.PREVIEW or not self.reveal_until:
            return 0
        return max(0, int((self.reveal_until - timezone.now()).total_seconds()))

    @property
    def can_see_answers(self) -> bool:
        if self.status != self.Status.FINISHED:
            return False
        return self.reveal == self.Reveal.APPROVED or self.preview_seconds_left > 0

    def ask_reveal(self) -> str:
        """O'quvchi "javoblarni ko'rish"ni bosdi. Birinchi marta — 1 daqiqa o'zi ko'radi
        ("preview"); u tugagach — ustozga so'rov ("requested"). Rad etilgani va takror
        bosishlar hech narsani o'zgartirmaydi (""). Shartli UPDATE — ikki marta bosish poyga
        holatida ham bitta natija beradi."""
        now = timezone.now()
        finished = QuizAttempt.objects.filter(pk=self.pk, status=self.Status.FINISHED)
        outcome = ""
        if finished.filter(reveal=self.Reveal.NONE).update(
            reveal=self.Reveal.PREVIEW, reveal_until=now + timedelta(seconds=self.PREVIEW_SECONDS)
        ):
            outcome = "preview"
        elif finished.filter(reveal=self.Reveal.PREVIEW, reveal_until__lte=now).update(
            reveal=self.Reveal.REQUESTED, reveal_requested_at=now
        ):
            outcome = "requested"
        self.refresh_from_db(fields=["reveal", "reveal_requested_at", "reveal_until"])
        return outcome

    def decide_reveal(self, approve: bool) -> None:
        """Ustoz qarori (so'rovsiz ham ruxsat berish yoki ruxsatni qaytarib olish mumkin)."""
        self.reveal = self.Reveal.APPROVED if approve else self.Reveal.REJECTED
        self.reveal_decided_at = timezone.now()
        self.save(update_fields=["reveal", "reveal_decided_at"])

    def on_finished(self) -> None:
        # Coin, xatolar ro'yxati, faol kun (streak) — test yakunlangan tranzaksiyaning o'zida.
        from .engagement import on_attempt_finished

        on_attempt_finished(self)


def new_open_quiz_token() -> str:
    return secrets.token_urlsafe(9)


def name_key(full_name: str) -> str:
    """F.I.Sh. solishtirish kaliti: katta-kichik harf, ortiqcha bo'sh joy va apostrof turlari
    farq qilmaydi ("aliyev  vali" == "Aliyev Vali", "Oʻ" == "O'")."""
    text = re.sub(r"[ʻʼ‘’`´]", "'", full_name or "")
    return " ".join(text.lower().split())


def warning_attempts():
    """Yakunlangan, ogohlantirishi bor testlar (profil va ustoz jo'natgan — farqsiz)."""
    return QuizAttempt.objects.filter(status=QuizAttempt.Status.FINISHED).filter(
        models.Q(leave_count__gt=0) | models.Q(copy_count__gt=0)
    )


class OpenQuiz(models.Model):
    """Umumiy test havolasi: bitta havola — ko'p qatnashchi. Har biri F.I.Sh. kiritib boshlaydi.

    Shaxsiy havoladan (``QuizAttempt``) farqi: qatnashchi bazadagi shogird bo'lishi shart emas
    (olimpiada, saralash, ochiq dars), natijalar F.I.Sh. bo'yicha ajratiladi.
    """

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="open_quizzes", verbose_name=_("Test")
    )
    title = models.CharField(
        _("Nomi"), max_length=160, blank=True,
        help_text=_("Masalan: “Saralash bosqichi” yoki “Ochiq dars”. Bo‘sh — mavzu nomi."),
    )
    token = models.CharField(max_length=24, unique=True, default=new_open_quiz_token, editable=False)
    language = models.CharField(
        _("Test tili"), max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ,
        help_text=_("Qatnashchi boshlashdan oldin tilni o‘zi ham tanlashi mumkin."),
    )
    question_count = models.PositiveSmallIntegerField(_("Savollar soni"), validators=[MinValueValidator(1)])
    time_limit_minutes = models.PositiveSmallIntegerField(
        _("Vaqt (daq.)"),
        validators=[MinValueValidator(1), MaxValueValidator(QuizBatch.MAX_TIME_LIMIT)],
    )
    is_active = models.BooleanField(_("Faol"), default=True)
    closes_at = models.DateTimeField(
        _("Yopilish vaqti"), null=True, blank=True,
        help_text=_("Bo‘sh — qo‘lda yopguningizcha ochiq."),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("Umumiy test havolasi")
        verbose_name_plural = _("Umumiy test havolalari")

    def __str__(self) -> str:
        return self.display_title

    @property
    def display_title(self) -> str:
        return self.title or self.quiz.topic.title_in(get_language())

    def get_absolute_url(self):
        return reverse("open_quiz", args=[self.pk])

    def get_public_url(self):
        return reverse("open_quiz_public", args=[self.token])

    def is_open(self, now=None) -> bool:
        now = now or timezone.now()
        return self.is_active and not (self.closes_at and now >= self.closes_at)

    @property
    def question_total(self) -> int:
        """Qatnashchi oladigan savollar soni (bankdagidan ko'p bo'lmaydi)."""
        return min(self.question_count, self.quiz.questions.count())


class OpenAttempt(AttemptScoringMixin, models.Model):
    """Umumiy havola orqali kirgan qatnashchining bitta urinishi."""

    COOKIE_PREFIX = "open_"

    class Status(models.TextChoices):
        ACTIVE = "active", _("Yechilmoqda")
        FINISHED = "finished", _("Tugatgan")

    open_quiz = models.ForeignKey(
        OpenQuiz, on_delete=models.CASCADE, related_name="attempts", verbose_name=_("Umumiy havola")
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="open_attempts", verbose_name=_("Test"))
    full_name = models.CharField(_("F.I.Sh."), max_length=160)
    name_key = models.CharField(max_length=160, editable=False)
    token = models.CharField(max_length=32, unique=True, default=new_attempt_token, editable=False)
    owner_key = models.CharField(max_length=64, blank=True, editable=False)
    status = models.CharField(
        _("Holat"), max_length=16, choices=Status.choices, default=Status.ACTIVE, db_index=True
    )
    language = models.CharField(_("Til"), max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ)
    question_ids = models.JSONField(_("Savollar"), default=list, blank=True, editable=False)
    leave_count = models.PositiveSmallIntegerField(_("Chiqib ketishlar"), default=0)
    away_seconds = models.PositiveIntegerField(_("Tashqarida (s)"), default=0)
    copy_count = models.PositiveSmallIntegerField(_("Nusxalash urinishlari"), default=0)
    answers = models.JSONField(_("Javoblar"), default=dict, blank=True)
    snapshot = models.JSONField(_("Javoblar tahlili"), default=list, blank=True, editable=False)
    started_at = models.DateTimeField(_("Boshlangan"), default=timezone.now)
    deadline = models.DateTimeField(_("Tugash vaqti"), null=True, blank=True)
    finished_at = models.DateTimeField(_("Tugagan"), null=True, blank=True)
    timed_out = models.BooleanField(_("Vaqt tugadi"), default=False)
    correct = models.PositiveSmallIntegerField(_("To'g'ri javoblar"), null=True, blank=True)
    total = models.PositiveSmallIntegerField(_("Savollar soni"), null=True, blank=True)

    class Meta:
        ordering = ["-started_at", "-pk"]
        verbose_name = _("Umumiy test natijasi")
        verbose_name_plural = _("Umumiy test natijalari")
        constraints = [
            # Bitta F.I.Sh. bilan bir havolada faqat bir marta (boshqa brauzerdan ham).
            models.UniqueConstraint(fields=["open_quiz", "name_key"], name="uniq_open_attempt_name"),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} — {self.open_quiz}"

    def save(self, *args, **kwargs):
        self.name_key = name_key(self.full_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("open_quiz_take", args=[self.open_quiz.token, self.token])

    @property
    def time_limit_minutes(self) -> int:
        return self.open_quiz.time_limit_minutes

    @property
    def question_count(self) -> int:
        return len(self.question_ids) if self.question_ids else self.open_quiz.question_total

    @property
    def duration_seconds(self):
        if self.finished_at and self.started_at:
            return int((self.finished_at - self.started_at).total_seconds())
        return None

    @property
    def initials(self) -> str:
        return initials_of(self.full_name)

    @property
    def duration_text(self) -> str:
        """Sarflangan vaqt "daq:ss" ko'rinishida (yakunlanmagan bo'lsa — bo'sh)."""
        seconds = self.duration_seconds
        return f"{seconds // 60}:{seconds % 60:02d}" if seconds is not None else ""

    @classmethod
    def begin(cls, open_quiz: OpenQuiz, full_name: str, language: str, owner_key: str) -> "OpenAttempt":
        """Yangi urinish: savollar tanlanadi, vaqt shu paytdan boshlanadi."""
        now = timezone.now()
        attempt = cls(
            open_quiz=open_quiz,
            quiz=open_quiz.quiz,
            full_name=" ".join(full_name.split()),
            language=language,
            owner_key=owner_key,
            started_at=now,
            deadline=now + timedelta(minutes=open_quiz.time_limit_minutes),
        )
        attempt.question_ids = attempt.pick_questions(open_quiz.question_count)
        attempt.save()
        return attempt


class OpenQuizInvite(models.Model):
    """Umumiy havola emailga yuborilgan manzil (kimga yuborilgani va xatosi)."""

    open_quiz = models.ForeignKey(
        OpenQuiz, on_delete=models.CASCADE, related_name="invites", verbose_name=_("Umumiy havola")
    )
    email = models.EmailField(_("Email"))
    sent_at = models.DateTimeField(_("Yuborilgan"), null=True, blank=True)
    error = models.CharField(_("Xato"), max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "email"]
        verbose_name = _("Email taklif")
        verbose_name_plural = _("Email takliflar")

    def __str__(self) -> str:
        return self.email


def _as_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def new_registration_token() -> str:
    return secrets.token_urlsafe(9)


class RegistrationLink(models.Model):
    """Ochiq ro'yxatdan o'tish havolasi (Telegram guruhlariga tashlanadi)."""

    title = models.CharField(_("Nomi"), max_length=120, help_text=_("Masalan: S-009 Telegram guruhi"))
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration_links",
        verbose_name=_("Guruh"),
        help_text=_("Arizalar shu guruhga taklif qilinadi (bo'sh — tasdiqlashda tanlaysiz)."),
    )
    token = models.CharField(max_length=24, unique=True, default=new_registration_token, editable=False)
    is_active = models.BooleanField(_("Faol"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ro'yxat havolasi")
        verbose_name_plural = _("Ro'yxat havolalari")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("registration_public", args=[self.token])


class Registration(models.Model):
    """O'quvchi to'ldirgan ariza: ustoz tekshirib, bazaga qo'shadi yoki rad etadi."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        APPROVED = "approved", _("Qabul qilingan")
        REJECTED = "rejected", _("Rad etilgan")

    link = models.ForeignKey(
        RegistrationLink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
        verbose_name=_("Havola"),
    )
    full_name = models.CharField(_("F.I.Sh."), max_length=160)
    phone = models.CharField(_("Telefon"), max_length=40)
    telegram = models.CharField(_("Telegram"), max_length=80)
    email = models.EmailField(_("Email"), blank=True)
    status = models.CharField(
        _("Holat"), max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
        verbose_name=_("O'quvchi"),
    )
    ip = models.GenericIPAddressField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(_("Yuborilgan"), auto_now_add=True)
    reviewed_at = models.DateTimeField(_("Ko'rib chiqilgan"), null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ariza")
        verbose_name_plural = _("Arizalar")

    def __str__(self) -> str:
        return f"{self.full_name} ({self.get_status_display()})"


class TestRequest(models.Model):
    """O'quvchining profildan "shu mavzudan test topshirsam bo'ladimi?" so'rovi.

    Ustoz ruxsat bergach, o'quvchi savollar soni (10/12) va vaqtni (5/10 daq.) o'zi
    tanlab, testni boshlaydi. Bir mavzu bo'yicha kuniga ko'pi bilan DAILY_LIMIT ta.
    """

    DAILY_LIMIT = 2
    QUESTION_CHOICES = (10, 12)
    MINUTE_CHOICES = (5, 10)

    class Status(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        APPROVED = "approved", _("Ruxsat berilgan")
        REJECTED = "rejected", _("Rad etilgan")
        USED = "used", _("Boshlangan")

    class Kind(models.TextChoices):
        FIRST = "first", _("Test")
        RETAKE = "retake", _("Qayta topshirish")
        PREVIEW = "preview", _("Yangi mavzu (oldindan)")

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="test_requests", verbose_name=_("O'quvchi")
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="test_requests", verbose_name=_("Mavzu")
    )
    kind = models.CharField(_("Turi"), max_length=8, choices=Kind.choices, default=Kind.FIRST)
    status = models.CharField(
        _("Holat"), max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    created_at = models.DateTimeField(_("So'ralgan"), auto_now_add=True)
    decided_at = models.DateTimeField(_("Ustoz qarori"), null=True, blank=True)
    attempt = models.OneToOneField(
        QuizAttempt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="test_request",
        verbose_name=_("Test"),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Test so'rovi")
        verbose_name_plural = _("Test so'rovlari")

    def __str__(self) -> str:
        return f"{self.student} — {self.topic} ({self.get_status_display()})"


class StudySession(models.Model):
    """O'quvchi mustahkamlash (yoki yangi mavzuga tayyorlanish) materialini ochgan payt.

    Qayta topshirish / yangi mavzu testi shundan ``MIN_MINUTES`` daqiqa o'tgach ochiladi.
    """

    class Kind(models.TextChoices):
        REVIEW = "review", _("Mustahkamlash")
        PREVIEW = "preview", _("Yangi mavzuga tayyorlanish")

    MIN_MINUTES = {Kind.REVIEW: 20, Kind.PREVIEW: 30}

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="study_sessions", verbose_name=_("O'quvchi")
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="study_sessions", verbose_name=_("Mavzu")
    )
    kind = models.CharField(_("Turi"), max_length=8, choices=Kind.choices)
    started_at = models.DateTimeField(_("Boshlangan"), default=timezone.now)

    class Meta:
        ordering = ["-started_at"]
        verbose_name = _("Mustahkamlash")
        verbose_name_plural = _("Mustahkamlashlar")

    def __str__(self) -> str:
        return f"{self.student} — {self.topic} ({self.get_kind_display()})"

    @property
    def unlocks_at(self):
        return self.started_at + timedelta(minutes=self.MIN_MINUTES[self.kind])


class CoinTransaction(models.Model):
    """Coin harakati (balans — yig'indi). Test uchun coin bir marta beriladi."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="coins", verbose_name=_("O'quvchi")
    )
    amount = models.IntegerField(_("Quvvat ⚡️"))
    reason = models.CharField(_("Sabab"), max_length=120)
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coins",
        verbose_name=_("Test"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("Quvvat")
        verbose_name_plural = _("Quvvat harakatlari")
        constraints = [
            models.UniqueConstraint(fields=["attempt", "reason"], name="uniq_coin_per_attempt_reason"),
        ]

    def __str__(self) -> str:
        return f"{self.student}: {self.amount:+d} ({self.reason})"

    # Bazadagi sabab matnlari (o'zbekcha) — interfeys tilida ko'rsatish uchun andozalar.
    REASON_PATTERNS = [
        (re.compile(r"^Test: (?P<p>\d+)%$"), gettext_noop("Test: {p}%")),
        (re.compile(r"^Takroriy test: (?P<p>\d+)%$"), gettext_noop("Takroriy test: {p}%")),
        (re.compile(r"^Mustahkamlab, qayta topshirdi$"), gettext_noop("Mustahkamlab, qayta topshirdi")),
        (re.compile(r"^Yangi mavzuni oldindan o‘zlashtirdi$"), gettext_noop("Yangi mavzuni oldindan o‘zlashtirdi")),
        (re.compile(r"^Xato tuzatildi: (?P<t>.+)$"), gettext_noop("Xato tuzatildi: {t}")),
        (re.compile(r"^🔥 (?P<n>\d+) kun ketma-ket faol$"), gettext_noop("🔥 {n} kun ketma-ket faol")),
        (re.compile(r"^Do‘kon: (?P<t>.+)$"), gettext_noop("🎁 Mukofot: {t}")),
        (re.compile(r"^🔓 Mavzu ochildi: (?P<t>.+)$"), gettext_noop("🔓 Mavzu ochildi: {t}")),
        (re.compile(r"^🎁 Ustozdan sovg‘a$"), gettext_noop("🎁 Ustozdan sovg‘a")),
        (re.compile(r"^🎁 Ustozdan sovg‘a: (?P<t>.+)$"), gettext_noop("🎁 Ustozdan sovg‘a: {t}")),
        (re.compile(r"^➕ Qo‘shimcha savol: (?P<t>.+)$"), gettext_noop("➕ Qo‘shimcha savol: {t}")),
        (re.compile(r"^⚠️ Test qoidasi buzildi: (?P<t>.+)$"), gettext_noop("⚠️ Test qoidasi buzildi: {t}")),
        (re.compile(r"^📝 Uyga vazifa: (?P<t>.+)$"), gettext_noop("📝 Uyga vazifa: {t}")),
    ]

    @property
    def is_gift(self) -> bool:
        return self.attempt_id is None and self.amount > 0 and self.reason.startswith("🎁 Ustozdan sovg‘a")

    @property
    def can_undo(self) -> bool:
        """Ustoz sovg'asi va berilganiga 24 soat bo'lmagan (``coins.GIFT_UNDO_HOURS``)."""
        return self.is_gift and self.created_at > timezone.now() - timedelta(hours=24)

    @property
    def display_reason(self) -> str:
        for pattern, template in self.REASON_PATTERNS:
            m = pattern.match(self.reason)
            if m:
                return gettext(template).format(**m.groupdict())
        return self.reason


class Mistake(models.Model):
    """O'quvchi xato qilgan (yoki javobsiz qoldirgan) savol — "Xatolar ustida ishlash".

    Mashqda ketma-ket ``RESOLVE_AFTER`` marta to'g'ri yechilsa — ro'yxatdan chiqadi.
    Testda yana xato qilsa — qaytadan ochiladi.
    """

    RESOLVE_AFTER = 3

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="mistakes", verbose_name=_("O'quvchi")
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="mistakes", verbose_name=_("Savol")
    )
    streak = models.PositiveSmallIntegerField(_("Ketma-ket to'g'ri"), default=0)
    wrong_count = models.PositiveSmallIntegerField(_("Xato soni"), default=1)
    last_wrong_at = models.DateTimeField(_("Oxirgi xato"), default=timezone.now)
    last_practiced_at = models.DateTimeField(_("Oxirgi mashq"), null=True, blank=True)
    resolved_at = models.DateTimeField(_("O'zlashtirildi"), null=True, blank=True)

    class Meta:
        verbose_name = _("Xato savol")
        verbose_name_plural = _("Xato savollar")
        constraints = [
            models.UniqueConstraint(fields=["student", "question"], name="uniq_mistake_student_question"),
        ]

    def __str__(self) -> str:
        return f"{self.student} — {self.question}"


class BonusAnswer(models.Model):
    """"Qo'shimcha savollar": o'tilgan mavzulardan savolga javob — har savolga bir marta.
    To'g'ri bo'lsa — test uchun ustoz belgilagan quvvat (``Quiz.bonus_quvvat``)."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="bonus_answers", verbose_name=_("O'quvchi")
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="bonus_answers", verbose_name=_("Savol")
    )
    is_correct = models.BooleanField(_("To'g'ri"), default=False)
    coins = models.PositiveSmallIntegerField(_("Quvvat ⚡️"), default=0)
    answered_at = models.DateTimeField(_("Javob berilgan"), default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-answered_at", "-pk"]
        verbose_name = _("Qo‘shimcha savol javobi")
        verbose_name_plural = _("Qo‘shimcha savollar javoblari")
        constraints = [
            models.UniqueConstraint(fields=["student", "question"], name="uniq_bonus_student_question"),
        ]

    def __str__(self) -> str:
        return f"{self.student} — {self.question} ({'+' if self.is_correct else '-'})"


class DailyActivity(models.Model):
    """O'quvchi faol bo'lgan kun (test yoki mashq) — streak uchun."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="activity_days", verbose_name=_("O'quvchi")
    )
    day = models.DateField(_("Kun"))

    class Meta:
        ordering = ["-day"]
        verbose_name = _("Faol kun")
        verbose_name_plural = _("Faol kunlar")
        constraints = [
            models.UniqueConstraint(fields=["student", "day"], name="uniq_activity_student_day"),
        ]

    def __str__(self) -> str:
        return f"{self.student} · {self.day:%d.%m.%Y}"


class TopicUnlock(models.Model):
    """O'quvchi quvvat ⚡️ sarflab guruhdan oldin ochgan mavzu (material va test ochiladi)."""

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="topic_unlocks", verbose_name=_("O'quvchi")
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="unlocks", verbose_name=_("Mavzu"))
    cost = models.PositiveIntegerField(_("Narxi (⚡️ quvvat)"))
    transaction = models.OneToOneField(
        CoinTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name="topic_unlock"
    )
    created_at = models.DateTimeField(_("Ochilgan"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ochilgan mavzu")
        verbose_name_plural = _("Ochilgan mavzular")
        constraints = [models.UniqueConstraint(fields=["student", "topic"], name="uniq_topic_unlock")]

    def __str__(self) -> str:
        return f"{self.student} — {self.topic}"


class Reward(models.Model):
    """Coin do'konidagi sovg'a (ustoz qo'shadi)."""

    class Perk(models.TextChoices):
        """Tasdiqlanganda avtomatik nima bo'ladi."""

        NONE = "", _("Oddiy — ustoz o‘zi beradi")
        HONOR = "honor", _("A’lochi unvoni — oltin medal va sertifikatda belgi")

    title = models.CharField(_("Sovg'a"), max_length=120)
    perk = models.CharField(
        _("Avtomatik ta’sir"), max_length=16, choices=Perk.choices, default=Perk.NONE, blank=True,
        help_text=_("“A’lochi unvoni”: tasdiqlanishi bilan o‘quvchi ismi hamma joyda oltin rangda, "
                    "medal bilan ko‘rinadi va sertifikatga “A’lochi” muhri tushadi."),
    )
    description = models.CharField(_("Izoh"), max_length=255, blank=True)
    cost = models.PositiveIntegerField(_("Narxi (⚡️ quvvat)"), validators=[MinValueValidator(1)])
    is_active = models.BooleanField(_("Do'konda ko'rinadi"), default=True)
    order = models.PositiveIntegerField(_("Tartib"), default=0)

    class Meta:
        ordering = ["order", "cost", "id"]
        verbose_name = _("Sovg'a")
        verbose_name_plural = _("Sovg'alar")

    def __str__(self) -> str:
        return f"{self.title} ({self.cost} ⚡️)"


class Purchase(models.Model):
    """O'quvchining sovg'a so'rovi: ustoz tasdiqlasa — coin yechiladi."""

    class Status(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        APPROVED = "approved", _("Berildi")
        REJECTED = "rejected", _("Rad etildi")

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="purchases", verbose_name=_("O'quvchi")
    )
    reward = models.ForeignKey(
        Reward, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchases", verbose_name=_("Sovg'a")
    )
    title = models.CharField(_("Sovg'a"), max_length=120)  # sovg'a keyin o'zgarsa ham tarix saqlanadi
    cost = models.PositiveIntegerField(_("Narxi (⚡️ quvvat)"))
    status = models.CharField(
        _("Holat"), max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    created_at = models.DateTimeField(_("So'ralgan"), auto_now_add=True)
    decided_at = models.DateTimeField(_("Ustoz qarori"), null=True, blank=True)
    transaction = models.OneToOneField(
        CoinTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Sovg'a so'rovi")
        verbose_name_plural = _("Sovg'a so'rovlari")

    def __str__(self) -> str:
        return f"{self.student} — {self.title} ({self.get_status_display()})"


for _model in (CoinTransaction, Student):
    post_save.connect(_podium_changed, sender=_model, dispatch_uid=f"podium_{_model.__name__}_save")
    post_delete.connect(_podium_changed, sender=_model, dispatch_uid=f"podium_{_model.__name__}_delete")


class TeacherAccount(models.Model):
    """O'qituvchi (bosh ustoz yaratgan login): Telegram akkaunti va QR orqali ulash holati.

    Telegram sessiyasi bazada emas — ``TELEGRAM_SESSIONS_DIR/<user id>.session`` faylida (0600),
    shuning uchun baza zaxiralariga tushmaydi.
    """

    class Link(models.TextChoices):
        NONE = "", _("Ulanmagan")
        STARTING = "starting", _("Tayyorlanmoqda")
        QR = "qr", _("QR kutilmoqda")
        PASSWORD = "password", _("2 bosqichli parol kutilmoqda")
        DONE = "done", _("Ulangan")
        ERROR = "error", _("Xato")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_account"
    )
    telegram_id = models.BigIntegerField(_("Telegram ID"), null=True, blank=True)
    telegram_name = models.CharField(_("Telegram nomi"), max_length=120, blank=True)
    telegram_username = models.CharField(_("Telegram username"), max_length=64, blank=True)
    linked_at = models.DateTimeField(_("Telegram ulangan"), null=True, blank=True)
    # QR orqali ulash jarayoni (fon oqimi yozadi, sahifa har 2 soniyada o'qiydi).
    link_status = models.CharField(max_length=12, choices=Link.choices, default=Link.NONE, blank=True)
    link_url = models.CharField(max_length=255, blank=True)
    link_error = models.CharField(max_length=255, blank=True)
    link_updated_at = models.DateTimeField(null=True, blank=True)
    # 2 bosqichli parol: sahifadan fon oqimiga uzatiladi va darhol o'chiriladi.
    link_password = models.CharField(max_length=255, blank=True)
    # Bosh ustoz ruxsat bergan bo'limlar (``teachers.SECTIONS`` kalitlari); har birida — faqat
    # o'qituvchining o'z guruhlari ma'lumoti.
    permissions = models.JSONField(_("Ruxsat etilgan bo‘limlar"), default=list, blank=True)
    # Maosh: o'tilgan har bir dars uchun + oylik qat'iy qism (so'm).
    lesson_rate = models.PositiveIntegerField(_("Bir dars uchun (so‘m)"), default=0)
    monthly_fixed = models.PositiveIntegerField(_("Oylik qat’iy qism (so‘m)"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("O‘qituvchi")
        verbose_name_plural = _("O‘qituvchilar")

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username

    @property
    def is_linked(self) -> bool:
        return bool(self.linked_at and self.telegram_id)


class TeacherPayout(models.Model):
    """O'qituvchiga oylik to'langani (hisoblangan summaning o'sha paytdagi nusxasi)."""

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payouts", verbose_name=_("O‘qituvchi")
    )
    month = models.DateField(_("Oy"), help_text=_("Oyning 1-sanasi."))
    lessons = models.PositiveIntegerField(_("O‘tilgan darslar"), default=0)
    amount = models.PositiveIntegerField(_("Summa (so‘m)"), default=0)
    paid_at = models.DateTimeField(_("To‘langan"), default=timezone.now)

    class Meta:
        ordering = ["-month", "teacher__first_name"]
        verbose_name = _("O‘qituvchi maoshi")
        verbose_name_plural = _("O‘qituvchilar maoshi")
        constraints = [models.UniqueConstraint(fields=["teacher", "month"], name="uniq_payout_teacher_month")]

    def __str__(self) -> str:
        return f"{self.teacher} · {self.month:%m.%Y} · {self.amount}"


class ActionLog(models.Model):
    """Harakatlar jurnali: kim, qachon, nima qildi (bosh ustoz va o'qituvchilarning POST amallari,
    kirish/chiqish). Yozuvlar ``audit.ActionLogMiddleware`` va kirish signallaridan."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actions",
        verbose_name=_("Foydalanuvchi"),
    )
    username = models.CharField(_("Login"), max_length=150, blank=True)  # foydalanuvchi o'chirilsa ham
    action = models.CharField(_("Amal"), max_length=64, db_index=True)
    target = models.CharField(_("Obyekt"), max_length=200, blank=True)
    path = models.CharField(_("Manzil"), max_length=255, blank=True)
    ip = models.CharField(_("IP"), max_length=64, blank=True)
    created_at = models.DateTimeField(_("Vaqt"), default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("Harakat")
        verbose_name_plural = _("Harakatlar jurnali")

    def __str__(self) -> str:
        return f"{self.username} · {self.action} · {self.target}"


def homework_file_path(instance, filename: str) -> str:
    """Taxmin qilib bo'lmaydigan nom: homework/<tasodifiy>.<kengaytma> (faqat ruxsat bilan beriladi)."""
    ext = filename.rsplit(".", 1)[-1].lower()[:5] if "." in filename else "bin"
    return f"homework/{secrets.token_urlsafe(16)}.{ext}"


class HomeworkSubmission(models.Model):
    """O'quvchining uyga vazifasi (profil orqali): matn, havola va/yoki fayl; o'qituvchi baholaydi."""

    class Status(models.TextChoices):
        SUBMITTED = "submitted", _("Tekshirilmoqda")
        CHECKED = "checked", _("Baholangan")

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="homework", verbose_name=_("O'quvchi")
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="submissions", verbose_name=_("Dars")
    )
    text = models.TextField(_("Javob"), blank=True)
    link = models.URLField(_("Havola"), max_length=500, blank=True)
    file = models.FileField(_("Fayl"), upload_to=homework_file_path, blank=True)
    file_name = models.CharField(_("Fayl nomi"), max_length=200, blank=True)
    submitted_at = models.DateTimeField(_("Topshirilgan"), default=timezone.now)
    on_time = models.BooleanField(_("Vaqtida"), default=True)
    status = models.CharField(
        _("Holat"), max_length=12, choices=Status.choices, default=Status.SUBMITTED, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        _("Ball"), null=True, blank=True, validators=[MaxValueValidator(100)]
    )
    comment = models.TextField(_("Izoh"), blank=True)
    checked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checked_homework",
        verbose_name=_("Tekshirgan"),
    )
    checked_at = models.DateTimeField(_("Tekshirilgan"), null=True, blank=True)
    coins = models.PositiveSmallIntegerField(_("Quvvat ⚡️"), default=0)

    class Meta:
        ordering = ["-submitted_at", "-pk"]
        verbose_name = _("Uyga vazifa")
        verbose_name_plural = _("Uyga vazifalar")
        constraints = [
            models.UniqueConstraint(fields=["student", "lesson"], name="uniq_homework_student_lesson"),
        ]

    def __str__(self) -> str:
        return f"{self.student} · {self.lesson}"
