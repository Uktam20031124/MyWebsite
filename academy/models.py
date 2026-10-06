from django.db import models, transaction
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone


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
        help_text="Masalan: Du / Chor 18:00–20:00",
    )
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
        super().save(*args, **kwargs)
        # Dars qaysi yo'l bilan "o'tildi" bo'lmasin (forma, yo'qlama, tugma),
        # guruh dasturi bir xil tarzda yangilanadi.
        if self.status == self.Status.COMPLETED and self.topic_id:
            SyllabusItem.objects.filter(
                group_id=self.group_id, topic_id=self.topic_id
            ).update(status=SyllabusItem.Status.TAUGHT, taught_on=self.held_on)

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
