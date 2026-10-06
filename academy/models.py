from django.db import models
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

    def syllabus_stats(self):
        total = self.syllabus.count()
        taught = self.syllabus.filter(status=SyllabusItem.Status.TAUGHT).count()
        pct = int(round((taught / total) * 100)) if total else 0
        return {"total": total, "taught": taught, "percent": pct}


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

    def attendance_stats(self):
        total = self.attendances.count()
        if not total:
            return {"total": 0, "present": 0, "percent": 0}
        present = self.attendances.filter(
            status__in=[Attendance.Status.PRESENT, Attendance.Status.LATE]
        ).count()
        return {
            "total": total,
            "present": present,
            "percent": int(round((present / total) * 100)),
        }


class Topic(models.Model):
    title = models.CharField("Mavzu", max_length=200)
    description = models.TextField("Tavsif", blank=True)
    duration_minutes = models.PositiveIntegerField("Davomiyligi (daq.)", default=90)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("topic_list")


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
        unique_together = [("group", "topic")]
        verbose_name = "Guruh mavzusi"
        verbose_name_plural = "Guruh mavzulari"

    def __str__(self) -> str:
        return f"{self.group.code}: {self.topic.title}"


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

    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.save(update_fields=["status"])
        if self.topic_id:
            SyllabusItem.objects.filter(
                group=self.group, topic=self.topic
            ).update(status=SyllabusItem.Status.TAUGHT, taught_on=self.held_on)


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Keldi"
        ABSENT = "absent", "Kelmadi"
        LATE = "late", "Kechikdi"
        EXCUSED = "excused", "Sababli"

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
        unique_together = [("lesson", "student")]
        verbose_name = "Yo'qlama"
        verbose_name_plural = "Yo'qlamalar"

    def __str__(self) -> str:
        return f"{self.student} — {self.get_status_display()}"
