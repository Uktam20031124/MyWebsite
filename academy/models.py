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
    status = models.CharField(
        "Holat",
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    joined_at = models.DateField("Qo'shilgan", default=timezone.localdate)
    notes = models.TextField("Izoh", blank=True)
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
    """Mavzu bo'yicha test: o'quvchi mavzuni o'zlashtirganini tekshirish uchun."""

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
        help_text="Shu vaqt tugaganda test avtomatik yakunlanadi.",
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

    def replace_questions(self, parsed) -> None:
        """Savollarni `parse_quiz` natijasi bilan almashtiradi."""
        with transaction.atomic():
            self.questions.all().delete()
            for order, (text, choices) in enumerate(parsed, start=1):
                question = Question.objects.create(quiz=self, text=text, order=order)
                Choice.objects.bulk_create(
                    Choice(question=question, text=c, is_correct=ok, order=i)
                    for i, (c, ok) in enumerate(choices, start=1)
                )


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name="Test"
    )
    text = models.TextField("Savol")
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self) -> str:
        return self.text[:80]


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices", verbose_name="Savol"
    )
    text = models.CharField("Javob", max_length=500)
    is_correct = models.BooleanField("To'g'ri", default=False)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self) -> str:
        return self.text


def new_attempt_token() -> str:
    return secrets.token_urlsafe(16)


class QuizAttempt(models.Model):
    """Bitta o'quvchi uchun bir martalik test havolasi (dars bo'yicha)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Ochilmagan"
        ACTIVE = "active", "Yechilmoqda"
        FINISHED = "finished", "Tugatgan"

    # Vaqt tugash paytida yuborilgan javoblar tarmoq kechikishi bilan kelsa ham qabul qilinadi.
    GRACE_SECONDS = 15

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="attempts", verbose_name="Test"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="quiz_attempts", verbose_name="Dars"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="quiz_attempts", verbose_name="Shogird"
    )
    token = models.CharField(max_length=32, unique=True, default=new_attempt_token, editable=False)
    status = models.CharField(
        "Holat", max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True
    )
    # Testni boshlagan brauzer kaliti (cookie): havola boshqa joyda qayta ochilmaydi.
    owner_key = models.CharField(max_length=64, blank=True, editable=False)
    answers = models.JSONField("Javoblar", default=dict, blank=True)
    started_at = models.DateTimeField("Boshlangan", null=True, blank=True)
    deadline = models.DateTimeField("Tugash vaqti", null=True, blank=True)
    finished_at = models.DateTimeField("Tugagan", null=True, blank=True)
    timed_out = models.BooleanField("Vaqt tugadi", default=False)
    correct = models.PositiveSmallIntegerField("To'g'ri javoblar", null=True, blank=True)
    total = models.PositiveSmallIntegerField("Savollar soni", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__full_name"]
        verbose_name = "Test havolasi"
        verbose_name_plural = "Test havolalari"
        constraints = [
            models.UniqueConstraint(
                fields=["lesson", "student"], name="uniq_quiz_attempt_lesson_student"
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

    def seconds_left(self, now=None) -> int:
        if not self.deadline:
            return 0
        now = now or timezone.now()
        return max(0, int((self.deadline - now).total_seconds()))

    def is_expired(self, now=None, grace: int = 0) -> bool:
        now = now or timezone.now()
        return bool(self.deadline) and now > self.deadline + timedelta(seconds=grace)

    def start(self, owner_key: str) -> bool:
        """Testni boshlaydi. Faqat birinchi chaqiruv muvaffaqiyatli (atomik)."""
        now = timezone.now()
        deadline = now + timedelta(minutes=self.quiz.time_limit_minutes)
        started = QuizAttempt.objects.filter(pk=self.pk, status=self.Status.PENDING).update(
            status=self.Status.ACTIVE, owner_key=owner_key, started_at=now, deadline=deadline
        )
        self.refresh_from_db()
        return bool(started)

    def finish(self, answers: dict | None = None, timed_out: bool = False) -> None:
        """Javoblarni baholab, testni yakunlaydi. `answers`: {savol_id: variant_id}."""
        with transaction.atomic():
            attempt = QuizAttempt.objects.select_for_update().get(pk=self.pk)
            if attempt.status == self.Status.FINISHED:
                self.refresh_from_db()
                return
            if answers is not None:
                attempt.answers = answers
            questions = list(attempt.quiz.questions.all())
            correct_ids = set(
                Choice.objects.filter(question__in=questions, is_correct=True).values_list(
                    "question_id", "pk"
                )
            )
            attempt.correct = sum(
                (q.pk, _as_int(attempt.answers.get(str(q.pk)))) in correct_ids for q in questions
            )
            attempt.total = len(questions)
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
