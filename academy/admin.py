from django.contrib import admin

from .models import Attendance, Group, Lesson, Student, SyllabusItem, Topic


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class SyllabusInline(admin.TabularInline):
    model = SyllabusItem
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "schedule", "status")
    list_filter = ("status",)
    search_fields = ("name", "code")
    inlines = [StudentInline, SyllabusInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "group", "phone", "status")
    list_filter = ("status", "group")
    search_fields = ("full_name", "phone", "telegram")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "duration_minutes", "is_active")
    list_display_links = ("title",)
    list_editable = ("order",)
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("held_on", "group", "topic", "status")
    list_filter = ("status", "group")
    date_hierarchy = "held_on"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("lesson", "student", "status")
    list_filter = ("status",)


@admin.register(SyllabusItem)
class SyllabusItemAdmin(admin.ModelAdmin):
    list_display = ("group", "order", "topic", "status", "taught_on")
    list_filter = ("status", "group")
