from django.contrib import admin

from config import admin_setup  # noqa: F401  (sayt sarlavhalari)

from .models import (
    Attendance,
    Choice,
    Group,
    Lesson,
    Module,
    Question,
    Quiz,
    QuizAttempt,
    QuizBatch,
    Student,
    SyllabusItem,
    Topic,
)


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ("full_name", "phone", "telegram", "status")


class SyllabusInline(admin.TabularInline):
    model = SyllabusItem
    extra = 0
    autocomplete_fields = ("topic",)


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0
    fields = ("order", "title", "duration_minutes", "is_active")


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ("student",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "schedule", "room", "status")
    list_filter = ("status",)
    search_fields = ("name", "code")
    inlines = [StudentInline, SyllabusInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "group", "phone", "status")
    list_filter = ("status", "group")
    search_fields = ("full_name", "phone", "telegram")
    list_select_related = ("group",)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("order", "title")
    list_display_links = ("title",)
    list_editable = ("order",)
    search_fields = ("title",)
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "module", "duration_minutes", "is_active")
    list_display_links = ("title",)
    list_editable = ("order",)
    list_filter = ("module", "is_active")
    search_fields = ("title", "description")
    list_select_related = ("module",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("held_on", "group", "topic", "status")
    list_filter = ("status", "group")
    date_hierarchy = "held_on"
    list_select_related = ("group", "topic")
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("lesson", "student", "status")
    list_filter = ("status",)
    list_select_related = ("lesson__group", "lesson__topic", "student")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("topic", "time_limit_minutes", "updated_at")
    search_fields = ("topic__title",)
    list_select_related = ("topic",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "order")
    list_select_related = ("quiz__topic",)
    inlines = [ChoiceInline]


class QuizAttemptInline(admin.TabularInline):
    model = QuizAttempt
    extra = 0
    fields = ("student", "status", "correct", "total", "finished_at")
    readonly_fields = fields
    can_delete = False


@admin.register(QuizBatch)
class QuizBatchAdmin(admin.ModelAdmin):
    list_display = ("quiz", "group", "lesson", "question_count", "time_limit_minutes", "created_at")
    list_filter = ("group",)
    search_fields = ("quiz__topic__title",)
    list_select_related = ("quiz__topic", "group", "lesson__group", "lesson__topic")
    inlines = [QuizAttemptInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "batch", "status", "correct", "total", "finished_at")
    list_filter = ("status",)
    search_fields = ("student__full_name", "quiz__topic__title")
    list_select_related = ("student", "quiz__topic", "batch__quiz__topic")
    readonly_fields = (
        "token", "owner_key", "question_ids", "started_at", "deadline", "finished_at"
    )


@admin.register(SyllabusItem)
class SyllabusItemAdmin(admin.ModelAdmin):
    list_display = ("group", "order", "topic", "status", "taught_on")
    list_filter = ("status", "group")
    list_select_related = ("group", "topic")
