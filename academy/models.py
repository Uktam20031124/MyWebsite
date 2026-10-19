import random
import secrets
from datetime import date, time, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

MAX_SCORE = 100

# Hafta kunlari: date.weekday() bilan bir xil (0 — dushanba).
WEEKDAYS = [
    (0, "Dushanba", "Du"),
    (1, "Seshanba", "Se"),
    (2, "Chorshanba", "Chor"),
    (3, "Payshanba", "Pay"),
    (4, "Juma", "Ju"),
    (5, "Shanba", "Sha"),
    (6, "Yakshanba", "Ya"),
]
WEEKDAY_CHOICES = [(n, full) for n, full, _ in WEEKDAYS]
WEEKDAY_SHORT = {n: short for n, _, short in WEEKDAYS}


def format_schedule(days: list[int], starts: time | None, ends: time | None) -> str:
    """[1, 4, 5], 14:00, 15:00 -> "Se / Ju / Sha 14:00–15:00"."""
    text = " / ".join(WEEKDAY_SHORT[d] for d in sorted(days))
    if starts:
        text += f" {starts:%H:%M}" + (f"–{ends:%H:%M}" if ends else "")
    return text.strip()


class Group(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Faol"
        PAUSED = "paused", "To'xtatilgan"
        ARCHIVED = "archived", "Arxiv"

    name = models.CharField("Nomi", max_length=120)
    code = models.CharField("Kod", max_length=32, unique=True)
    schedule = models.CharField(
        "Jadval",
        max_length=200,
        blank=True,
        help_text="Dars kunlari va vaqti tanlansa, avtomatik to'ldiriladi.",
    )
    days = models.CharField(
        "Dars kunlari",
        max_length=20,
        blank=True,
        help_text="Hafta kunlari raqamlari (0 — dushanba), vergul bilan: 1,4,5",
    )
    starts_at = models.TimeField("Boshlanish vaqti", null=True, blank=True)
    ends_at = models.TimeField("Tugash vaqti", null=True, blank=True)
    room = models.CharField("Xona", max_length=80, blank=True)
    start_date = models.DateField("Boshlanish", null=True, blank=True)
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    notes = models.TextField("Izoh", blank=True)
    # O'quvchilar o'z Telegram/telefonini kiritadigan ochiq havola kaliti (bo'sh — o'chiq).
    contact_token = models.CharField(max_length=32, blank=True, editable=False, db_index=True)
    # Guruhning Telegram chati (@username yoki raqamli ID) — haftalik reyting uchun.
    telegram_chat = models.CharField(
        "Telegram guruh chati",
        max_length=100,
        blank=True,
        help_text="@guruh_nomi, t.me/guruh_nomi yoki raqamli ID (manage.py telegram_chats).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

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


class QuizLanguage(models.TextChoices):
    """Test qaysi tilda yechiladi (savollar, sahifa matnlari, xabar)."""

    UZ = "uz", "O‘zbekcha"
    RU = "ru", "Русский"


class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Faol"
        PAUSED = "paused", "Tanaffus"
        GRADUATED = "graduated", "Bitirgan"
        DROPPED = "dropped", "Ketgan"

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Guruh",
    )
    full_name = models.CharField("F.I.Sh.", max_length=160)
    phone = models.CharField("Telefon", max_length=40, blank=True)
    telegram = models.CharField("Telegram", max_length=80, blank=True)
    email = models.EmailField("Email", blank=True)
    # Test jo'natishda shu til oldindan tanlanadi (har safar o'zgartirish mumkin).
    quiz_language = models.CharField(
        "Test tili", max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ
    )
    # Profil (shaxsiy sahifa): o'quvchi kirishga so'rov yuboradi, ustoz vaqt bilan ruxsat beradi.
    profile_requested_at = models.DateTimeField("Profilga kirish so'ralgan", null=True, blank=True)
    profile_until = models.DateTimeField("Profil ochiq (gacha)", null=True, blank=True)
    # O'quvchi o'zi test so'ray oladigan mavzular (ustoz belgilaydi).
    allowed_topics = models.ManyToManyField(
        "Topic", blank=True, related_name="allowed_students", verbose_name="Test uchun ruxsat etilgan mavzular"
    )
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    joined_at = models.DateField("Qo'shilgan", default=timezone.localdate)
    notes = models.TextField("Izoh", blank=True)
    # O'quvchining shaxsiy natijalar sahifasi kaliti (/men/<kalit>/); bo'sh — hali yaratilmagan.
    portal_token = models.CharField(max_length=32, blank=True, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Shogird"
        verbose_name_plural = "Shogirdlar"
        indexes = [
            models.Index(fields=["group", "status"]),
        ]

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self):
        return reverse("student_detail", args=[self.pk])

    def initials(self) -> str:
        parts = [p for p in self.full_name.split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def save(self, *args, **kwargs):
        self.telegram = self.telegram.strip().lstrip("@")
        super().save(*args, **kwargs)


class Module(models.Model):
    """Mavzular bo'limi (kurs qismi): masalan, "Python asoslari"."""

    title = models.CharField("Bo'lim", max_length=160, unique=True)
    description = models.TextField("Tavsif", blank=True)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return f"{reverse('topic_list')}?module={self.pk}"


class Topic(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        related_name="topics",
        verbose_name="Bo'lim",
        null=True,
        blank=True,
    )
    title = models.CharField("Mavzu", max_length=200)
    title_ru = models.CharField(
        "Mavzu (ruscha)", max_length=200, blank=True, help_text="Ruscha testlarda ko'rsatiladi."
    )
    description = models.TextField("Tavsif", blank=True)
    homework = models.TextField(
        "Uyga vazifa (shablon)",
        blank=True,
        help_text="Shu mavzuda dars yaratilganda avtomatik qo'yiladi.",
    )
    resources = models.TextField(
        "Materiallar",
        blank=True,
        help_text="Har qatorda bitta havola yoki manba.",
    )
    study = models.TextField(
        "Mustahkamlash materiali",
        blank=True,
        help_text="O'quvchi testdan past natija olsa, profilida ko'rinadi: tushuntirish, "
        "bajarilgan misollar. Format: ## sarlavha, - ro'yxat, ``` kod ```, **qalin**, `kod`.",
    )
    duration_minutes = models.PositiveIntegerField("Davomiyligi (daq.)", default=90)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["module__order", "module__title", "order", "title"]
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
        constraints = [
            models.UniqueConstraint(
                fields=["module", "title"], name="uniq_topic_title_per_module"
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("topic_detail", args=[self.pk])

    def title_in(self, lang: str) -> str:
        return self.title_ru if lang == QuizLanguage.RU and self.title_ru else self.title

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
        PLANNED = "planned", "Rejada"
        TAUGHT = "taught", "O'tildi"
        SKIPPED = "skipped", "O'tkazib yuborildi"

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="syllabus",
        verbose_name="Guruh",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="syllabus_items",
        verbose_name="Mavzu",
    )
    order = models.PositiveIntegerField("Tartib", default=0)
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True,
    )
    taught_on = models.DateField("O'tilgan sana", null=True, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Guruh mavzusi"
        verbose_name_plural = "Guruh mavzulari"
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
        PLANNED = "planned", "Rejada"
        COMPLETED = "completed", "O'tildi"
        CANCELLED = "cancelled", "Bekor"

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Guruh",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="Mavzu",
        null=True,
        blank=True,
    )
    held_on = models.DateField("Sana", db_index=True)
    starts_at = models.TimeField("Boshlanish", null=True, blank=True)
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True,
    )
    homework = models.TextField("Uyga vazifa", blank=True)
    notes = models.TextField("Dars izohi", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-held_on", "-starts_at"]
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        indexes = [
            models.Index(fields=["group", "held_on"]),
        ]

    def __str__(self) -> str:
        title = self.topic.title if self.topic else "Mavzusiz dars"
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
        PRESENT = "present", "Keldi"
        ABSENT = "absent", "Kelmadi"
        LATE = "late", "Kechikdi"
        EXCUSED = "excused", "Sababli"

    # Davomat foizida "keldi" deb hisoblanadigan holatlar.
    ATTENDED = (Status.PRESENT, Status.LATE)

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="Dars",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="Shogird",
    )
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.PRESENT,
    )
    note = models.CharField("Izoh", max_length=200, blank=True)
    score = models.PositiveSmallIntegerField(
        "Ball (0–100)",
        null=True,
        blank=True,
        validators=[MaxValueValidator(MAX_SCORE)],
        help_text="Darsdagi faollik va uy vazifasi uchun baho. Bo'sh — baholanmagan.",
    )

    class Meta:
        verbose_name = "Yo'qlama"
        verbose_name_plural = "Yo'qlamalar"
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
        verbose_name="Mavzu",
    )
    time_limit_minutes = models.PositiveSmallIntegerField(
        "Vaqt (daq.)",
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        help_text="Jo'natishda taklif qilinadigan vaqt. Har bir jo'natmada o'zgartirish mumkin.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

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
        Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Test"
    )
    text = models.TextField("Savol")
    # Ruscha tarjima (bo'sh — tarjima qilinmagan, o'zbekchasi ko'rsatiladi).
    text_ru = models.TextField("Savol (ruscha)", blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)
    image = models.FileField("Rasm", upload_to=question_image_path, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

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
        Question, on_delete=models.CASCADE, related_name="choices", verbose_name="Savol"
    )
    text = models.CharField("Javob", max_length=500)
    text_ru = models.CharField("Javob (ruscha)", max_length=500, blank=True)
    is_correct = models.BooleanField("To'g'ri", default=False)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self) -> str:
        return self.text

    def text_in(self, lang: str) -> str:
        return self.text_ru if lang == QuizLanguage.RU and self.text_ru else self.text


class QuizBatch(models.Model):
    """Test jo'natmasi: bitta mavzu testi, tanlangan shogirdlar, savollar soni va vaqt."""

    MAX_TIME_LIMIT = 180

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="batches", verbose_name="Test"
    )
    # Dars o'chirilsa ham natijalar saqlanib qoladi.
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_batches",
        verbose_name="Dars",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quiz_batches",
        verbose_name="Guruh",
    )
    question_count = models.PositiveSmallIntegerField(
        "Savollar soni", validators=[MinValueValidator(1)]
    )
    time_limit_minutes = models.PositiveSmallIntegerField(
        "Vaqt (daq.)", validators=[MinValueValidator(1), MaxValueValidator(MAX_TIME_LIMIT)]
    )
    created_at = models.DateTimeField("Jo'natilgan", auto_now_add=True)
    # Belgilangan vaqtda yuborish (manage.py send_scheduled); bo'sh — darhol.
    scheduled_at = models.DateTimeField("Yuborish vaqti", null=True, blank=True)
    scheduled_sent_at = models.DateTimeField("Rejali yuborilgan", null=True, blank=True)
    # Havolalar qaysi kanallar orqali yuboriladi (rejalashtirilgan yuborish uchun): "telegram,email".
    channels = models.CharField("Kanallar", max_length=32, default="telegram", blank=True)
    # O'quvchi profilidan (ustoz ruxsati bilan) o'zi boshlagan test.
    from_profile = models.BooleanField("Profildan", default=False)
    retake_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="retakes",
        verbose_name="Qayta topshirish (asosiy jo'natma)",
    )

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "Test jo'natmasi"
        verbose_name_plural = "Test jo'natmalari"

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


class QuizAttempt(models.Model):
    """Bitta o'quvchi uchun bir martalik test havolasi."""

    class Status(models.TextChoices):
        PENDING = "pending", "Ochilmagan"
        ACTIVE = "active", "Yechilmoqda"
        FINISHED = "finished", "Tugatgan"

    class Reveal(models.TextChoices):
        """O'quvchi o'z javoblarini (to'g'ri/xato) ko'rishi — faqat ustoz ruxsati bilan."""

        NONE = "", "So‘ralmagan"
        REQUESTED = "requested", "So‘ralgan"
        APPROVED = "approved", "Ruxsat berilgan"
        REJECTED = "rejected", "Rad etilgan"

    # Vaqt tugash paytida yuborilgan javoblar tarmoq kechikishi bilan kelsa ham qabul qilinadi.
    GRACE_SECONDS = 15

    batch = models.ForeignKey(
        QuizBatch, on_delete=models.CASCADE, related_name="attempts", verbose_name="Jo'natma"
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts", verbose_name="Test"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="quiz_attempts", verbose_name="Shogird"
    )
    token = models.CharField(max_length=32, unique=True, default=new_attempt_token, editable=False)
    status = models.CharField(
        "Holat", max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    language = models.CharField(
        "Til", max_length=2, choices=QuizLanguage.choices, default=QuizLanguage.UZ
    )
    # Testni boshlagan brauzer kaliti (cookie): havola boshqa joyda qayta ochilmaydi.
    owner_key = models.CharField(max_length=64, blank=True, editable=False)
    # Boshlanganda bankdan tasodifiy tanlangan savollar (har bir o'quvchida o'zicha).
    question_ids = models.JSONField("Savollar", default=list, blank=True, editable=False)
    # Test paytida boshqa oyna/ilovaga o'tishlar (ko'chirishga qarshi qayd) — faqat ustozga.
    leave_count = models.PositiveSmallIntegerField("Chiqib ketishlar", default=0)
    away_seconds = models.PositiveIntegerField("Tashqarida (s)", default=0)
    answers = models.JSONField("Javoblar", default=dict, blank=True)
    # Yakunlanganda: savollar, variantlar, tanlangani va to'g'ri javob nusxasi — faqat
    # ustoz ko'radi; test keyinchalik tahrirlansa ham natija tahlili o'zgarmaydi.
    snapshot = models.JSONField("Javoblar tahlili", default=list, blank=True, editable=False)
    started_at = models.DateTimeField("Boshlangan", null=True, blank=True)
    deadline = models.DateTimeField("Tugash vaqti", null=True, blank=True)
    finished_at = models.DateTimeField("Tugagan", null=True, blank=True)
    timed_out = models.BooleanField("Vaqt tugadi", default=False)
    correct = models.PositiveSmallIntegerField("To'g'ri javoblar", null=True, blank=True)
    total = models.PositiveSmallIntegerField("Savollar soni", null=True, blank=True)
    # Ustozning Telegram akkauntidan yuborilgan payt va oxirgi xato (bo'lsa).
    sent_at = models.DateTimeField("Telegramda yuborilgan", null=True, blank=True)
    # Ochilmagan test haqida bitta avtomatik eslatma (manage.py quiz_reminders).
    reminded_at = models.DateTimeField("Eslatma yuborilgan", null=True, blank=True)
    # Email (Gmail) orqali yuborilgan payt va oxirgi xato (bo'lsa).
    email_sent_at = models.DateTimeField("Emailga yuborilgan", null=True, blank=True)
    email_error = models.CharField("Email xatosi", max_length=255, blank=True)
    reveal = models.CharField(
        "Javoblarni ko'rish", max_length=12, choices=Reveal.choices, default=Reveal.NONE,
        blank=True, db_index=True,
    )
    reveal_requested_at = models.DateTimeField("Ko'rish so'ralgan", null=True, blank=True)
    reveal_decided_at = models.DateTimeField("Ustoz qarori", null=True, blank=True)
    send_error = models.CharField("Yuborish xatosi", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__full_name"]
        verbose_name = "Test havolasi"
        verbose_name_plural = "Test havolalari"
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
    def percent(self):
        if not self.total:
            return None
        return round(100 * (self.correct or 0) / self.total)

    @property
    def time_limit_minutes(self) -> int:
        return self.batch.time_limit_minutes

    @property
    def question_count(self) -> int:
        """O'quvchi oladigan savollar soni (bankdagidan ko'p bo'lmaydi)."""
        if self.question_ids:
            return len(self.question_ids)
        return min(self.batch.question_count, self.quiz.questions.count())

    def seconds_left(self, now=None) -> int:
        if not self.deadline:
            return 0
        now = now or timezone.now()
        return max(0, int((self.deadline - now).total_seconds()))

    def is_expired(self, now=None, grace: int = 0) -> bool:
        now = now or timezone.now()
        return bool(self.deadline) and now > self.deadline + timedelta(seconds=grace)

    def start(self, owner_key: str) -> bool:
        """Testni boshlaydi va savollarni tanlaydi. Faqat birinchi chaqiruv muvaffaqiyatli."""
        now = timezone.now()
        pool = list(self.quiz.questions.values_list("pk", flat=True))
        count = min(self.batch.question_count, len(pool))
        if self.language == QuizLanguage.RU:
            # Tarjimasi bor savollar yetarli bo'lsa — faqat ulardan (aralash til bo'lmasin).
            translated = list(
                self.quiz.questions.exclude(text_ru="").values_list("pk", flat=True)
            )
            if len(translated) >= count:
                pool = translated
        picked = random.SystemRandom().sample(pool, count)
        started = QuizAttempt.objects.filter(pk=self.pk, status=self.Status.PENDING).update(
            status=self.Status.ACTIVE,
            owner_key=owner_key,
            question_ids=picked,
            started_at=now,
            deadline=now + timedelta(minutes=self.batch.time_limit_minutes),
        )
        self.refresh_from_db()
        return bool(started)

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
            title, _, code = (pick(item) if item["text"] else "").partition("\n")
            item["title"], item["code"] = title, code
            item["answered"] = item["picked"] is not None
            item["correct_text"] = next((pick(c) for c in item["choices"] if c["correct"]), "")
            item["picked_text"] = next(
                (pick(c) for c in item["choices"] if c["id"] == item["picked"]), ""
            )
        return items

    @property
    def can_see_answers(self) -> bool:
        return self.status == self.Status.FINISHED and self.reveal == self.Reveal.APPROVED

    def request_reveal(self) -> bool:
        """O'quvchi so'rovi: faqat yakunlangan va hali so'ralmagan testga (rad etilgani
        qayta so'ralmaydi — ustozni bezovta qilmaslik uchun). Yangi so'rov bo'lsa True."""
        updated = QuizAttempt.objects.filter(
            pk=self.pk, status=self.Status.FINISHED, reveal=self.Reveal.NONE
        ).update(reveal=self.Reveal.REQUESTED, reveal_requested_at=timezone.now())
        self.refresh_from_db(fields=["reveal", "reveal_requested_at"])
        return bool(updated)

    def decide_reveal(self, approve: bool) -> None:
        """Ustoz qarori (so'rovsiz ham ruxsat berish yoki ruxsatni qaytarib olish mumkin)."""
        self.reveal = self.Reveal.APPROVED if approve else self.Reveal.REJECTED
        self.reveal_decided_at = timezone.now()
        self.save(update_fields=["reveal", "reveal_decided_at"])

    def finish(self, answers: dict | None = None, timed_out: bool = False) -> None:
        """Javoblarni baholab, testni yakunlaydi. `answers`: {savol_id: variant_id}."""
        with transaction.atomic():
            attempt = QuizAttempt.objects.select_for_update().get(pk=self.pk)
            if attempt.status == self.Status.FINISHED:
                self.refresh_from_db()
                return
            if answers is not None:
                attempt.answers = answers
            # Baholash va ustoz ko'radigan javoblar tahlili — bitta nusxadan.
            attempt.snapshot = attempt.build_review()
            attempt.correct = sum(item["is_correct"] for item in attempt.snapshot)
            attempt.total = len(attempt.snapshot)
            attempt.status = self.Status.FINISHED
            attempt.finished_at = timezone.now()
            attempt.timed_out = timed_out
            attempt.save()
        self.refresh_from_db()


def _as_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def new_registration_token() -> str:
    return secrets.token_urlsafe(9)


class RegistrationLink(models.Model):
    """Ochiq ro'yxatdan o'tish havolasi (Telegram guruhlariga tashlanadi)."""

    title = models.CharField("Nomi", max_length=120, help_text="Masalan: S-009 Telegram guruhi")
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registration_links",
        verbose_name="Guruh",
        help_text="Arizalar shu guruhga taklif qilinadi (bo'sh — tasdiqlashda tanlaysiz).",
    )
    token = models.CharField(max_length=24, unique=True, default=new_registration_token, editable=False)
    is_active = models.BooleanField("Faol", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ro'yxat havolasi"
        verbose_name_plural = "Ro'yxat havolalari"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("registration_public", args=[self.token])


class Registration(models.Model):
    """O'quvchi to'ldirgan ariza: ustoz tekshirib, bazaga qo'shadi yoki rad etadi."""

    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        APPROVED = "approved", "Qabul qilingan"
        REJECTED = "rejected", "Rad etilgan"

    link = models.ForeignKey(
        RegistrationLink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
        verbose_name="Havola",
    )
    full_name = models.CharField("F.I.Sh.", max_length=160)
    phone = models.CharField("Telefon", max_length=40)
    telegram = models.CharField("Telegram", max_length=80)
    email = models.EmailField("Email", blank=True)
    status = models.CharField(
        "Holat", max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registrations",
        verbose_name="O'quvchi",
    )
    ip = models.GenericIPAddressField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField("Yuborilgan", auto_now_add=True)
    reviewed_at = models.DateTimeField("Ko'rib chiqilgan", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"

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
        PENDING = "pending", "Kutilmoqda"
        APPROVED = "approved", "Ruxsat berilgan"
        REJECTED = "rejected", "Rad etilgan"
        USED = "used", "Boshlangan"

    class Kind(models.TextChoices):
        FIRST = "first", "Test"
        RETAKE = "retake", "Qayta topshirish"

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="test_requests", verbose_name="O'quvchi"
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="test_requests", verbose_name="Mavzu"
    )
    kind = models.CharField("Turi", max_length=8, choices=Kind.choices, default=Kind.FIRST)
    status = models.CharField(
        "Holat", max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    created_at = models.DateTimeField("So'ralgan", auto_now_add=True)
    decided_at = models.DateTimeField("Ustoz qarori", null=True, blank=True)
    attempt = models.OneToOneField(
        QuizAttempt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="test_request",
        verbose_name="Test",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Test so'rovi"
        verbose_name_plural = "Test so'rovlari"

    def __str__(self) -> str:
        return f"{self.student} — {self.topic} ({self.get_status_display()})"
