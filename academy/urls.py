from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("kirish/", views.ThrottledLoginView.as_view(), name="login"),
    path("chiqish/", auth_views.LogoutView.as_view(), name="logout"),
    path("healthz/", views.healthz, name="healthz"),
    path("", views.dashboard, name="dashboard"),
    path("qidiruv/", views.search, name="search"),
    path("jadval/", views.timetable, name="timetable"),
    # Guruhlar
    path("guruhlar/", views.GroupListView.as_view(), name="group_list"),
    path("guruhlar/yangi/", views.GroupCreateView.as_view(), name="group_create"),
    path("guruhlar/<int:pk>/", views.GroupDetailView.as_view(), name="group_detail"),
    path("guruhlar/<int:pk>/tahrir/", views.GroupUpdateView.as_view(), name="group_update"),
    path("guruhlar/<int:pk>/ochirish/", views.GroupDeleteView.as_view(), name="group_delete"),
    path("guruhlar/<int:pk>/jurnal/", views.group_journal_view, name="group_journal"),
    path("guruhlar/<int:pk>/boshlash/", views.start_lesson, name="start_lesson"),
    path("guruhlar/<int:pk>/mavzu/", views.add_syllabus_item, name="syllabus_add"),
    path(
        "guruhlar/<int:pk>/mavzu/<int:item_id>/",
        views.toggle_syllabus,
        name="syllabus_toggle",
    ),
    # Shogirdlar
    path("shogirdlar/", views.StudentListView.as_view(), name="student_list"),
    path("shogirdlar/yangi/", views.StudentCreateView.as_view(), name="student_create"),
    path("shogirdlar/eksport/", views.student_export, name="student_export"),
    path("shogirdlar/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("shogirdlar/<int:pk>/tahrir/", views.StudentUpdateView.as_view(), name="student_update"),
    path("shogirdlar/<int:pk>/ochirish/", views.StudentDeleteView.as_view(), name="student_delete"),
    # Mavzular va bo'limlar
    path("mavzular/", views.TopicListView.as_view(), name="topic_list"),
    path("mavzular/yangi/", views.TopicCreateView.as_view(), name="topic_create"),
    path("mavzular/import/", views.TopicImportView.as_view(), name="topic_import"),
    path("mavzular/eksport/", views.topic_export, name="topic_export"),
    path("mavzular/<int:pk>/", views.TopicDetailView.as_view(), name="topic_detail"),
    path("mavzular/<int:pk>/tahrir/", views.TopicUpdateView.as_view(), name="topic_update"),
    path("mavzular/<int:pk>/ochirish/", views.TopicDeleteView.as_view(), name="topic_delete"),
    path("bolimlar/yangi/", views.ModuleCreateView.as_view(), name="module_create"),
    path("bolimlar/<int:pk>/tahrir/", views.ModuleUpdateView.as_view(), name="module_update"),
    path("bolimlar/<int:pk>/ochirish/", views.ModuleDeleteView.as_view(), name="module_delete"),
    # Darslar
    path("darslar/", views.LessonListView.as_view(), name="lesson_list"),
    path("darslar/yangi/", views.LessonCreateView.as_view(), name="lesson_create"),
    path("darslar/<int:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("darslar/<int:pk>/tahrir/", views.LessonUpdateView.as_view(), name="lesson_update"),
    path("darslar/<int:pk>/ochirish/", views.LessonDeleteView.as_view(), name="lesson_delete"),
    path("darslar/<int:pk>/yakun/", views.complete_lesson, name="lesson_complete"),
    path("darslar/<int:pk>/yoqlama/", views.attendance_sheet, name="attendance"),
    # Testlar
    path("mavzular/<int:pk>/test/", views.quiz_edit, name="quiz_edit"),
    path("mavzular/<int:pk>/test/ochirish/", views.QuizDeleteView.as_view(), name="quiz_delete"),
    path("testlar/", views.QuizBatchListView.as_view(), name="quiz_batches"),
    path("testlar/jonatish/", views.quiz_send, name="quiz_send"),
    path("testlar/<int:pk>/", views.quiz_batch_detail, name="quiz_batch"),
    path("testlar/<int:pk>/ochirish/", views.QuizBatchDeleteView.as_view(), name="quiz_batch_delete"),
    path("test-havola/<int:pk>/yangilash/", views.quiz_attempt_renew, name="quiz_attempt_renew"),
    # O'quvchi uchun ochiq test sahifasi (login talab qilinmaydi)
    path("t/<str:token>/", views.quiz_take, name="quiz_take"),
    path("t/<str:token>/saqlash/", views.quiz_save, name="quiz_save"),
    path("t/<str:token>/yakunlash/", views.quiz_submit, name="quiz_submit"),
]
