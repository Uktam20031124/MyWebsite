from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path(
        "kirish/",
        auth_views.LoginView.as_view(
            template_name="academy/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path(
        "chiqish/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("", views.dashboard, name="dashboard"),
    path("qidiruv/", views.search, name="search"),
    path("guruhlar/", views.GroupListView.as_view(), name="group_list"),
    path("guruhlar/yangi/", views.GroupCreateView.as_view(), name="group_create"),
    path("guruhlar/<int:pk>/", views.GroupDetailView.as_view(), name="group_detail"),
    path("guruhlar/<int:pk>/tahrir/", views.GroupUpdateView.as_view(), name="group_update"),
    path("guruhlar/<int:pk>/ochirish/", views.GroupDeleteView.as_view(), name="group_delete"),
    path("guruhlar/<int:pk>/mavzu/", views.add_syllabus_item, name="syllabus_add"),
    path(
        "guruhlar/<int:pk>/mavzu/<int:item_id>/",
        views.toggle_syllabus,
        name="syllabus_toggle",
    ),
    path("shogirdlar/", views.StudentListView.as_view(), name="student_list"),
    path("shogirdlar/yangi/", views.StudentCreateView.as_view(), name="student_create"),
    path("shogirdlar/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path(
        "shogirdlar/<int:pk>/tahrir/",
        views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path(
        "shogirdlar/<int:pk>/ochirish/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path("mavzular/", views.TopicListView.as_view(), name="topic_list"),
    path("mavzular/yangi/", views.TopicCreateView.as_view(), name="topic_create"),
    path("mavzular/<int:pk>/tahrir/", views.TopicUpdateView.as_view(), name="topic_update"),
    path("mavzular/<int:pk>/ochirish/", views.TopicDeleteView.as_view(), name="topic_delete"),
    path("darslar/", views.LessonListView.as_view(), name="lesson_list"),
    path("darslar/yangi/", views.LessonCreateView.as_view(), name="lesson_create"),
    path("darslar/<int:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("darslar/<int:pk>/tahrir/", views.LessonUpdateView.as_view(), name="lesson_update"),
    path(
        "darslar/<int:pk>/ochirish/", views.LessonDeleteView.as_view(), name="lesson_delete"
    ),
    path("darslar/<int:pk>/yakun/", views.complete_lesson, name="lesson_complete"),
    path("darslar/<int:pk>/yoqlama/", views.attendance_sheet, name="attendance"),
]
