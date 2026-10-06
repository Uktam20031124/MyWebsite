from django.contrib import admin

from config import admin_setup  # noqa: F401  (sayt sarlavhalari)

from .models import Attendance, Group, Lesson, Module, Student, SyllabusItem, Topic


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


@admin.register(SyllabusItem)
class SyllabusItemAdmin(admin.ModelAdmin):
    list_display = ("group", "order", "topic", "status", "taught_on")
    list_filter = ("status", "group")
    list_select_related = ("group", "topic")
