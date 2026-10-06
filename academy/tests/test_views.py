from django.test import TestCase
from django.urls import reverse

from academy.models import Attendance, Lesson, Module, Student, SyllabusItem, Topic

from . import factories as f


class LoginRequiredTests(TestCase):
    def test_pages_redirect_anonymous_to_login(self):
        for name in ("dashboard", "group_list", "student_list", "topic_list", "lesson_list",
                     "topic_import", "topic_export", "search"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response["Location"])

    def test_logged_in_user_skips_login_page(self):
        self.client.force_login(f.user())
        self.assertRedirects(self.client.get(reverse("login")), reverse("dashboard"))


class ViewTestCase(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.group = f.group(code="PY-1")
        self.student = f.student(self.group, full_name="Aliyev Sardor", phone="+998 90 111 22 33")
        self.module = f.module(title="Python")
        self.topic = f.topic(module=self.module, title="Sikllar", homework="5 ta mashq")
        self.group.add_topics([self.topic])
        self.lesson = f.lesson(self.group, topic=self.topic)


class PageSmokeTests(ViewTestCase):
    def test_all_pages_render(self):
        item = self.group.syllabus.first()
        urls = [
            reverse("dashboard"),
            reverse("search") + "?q=Ali",
            reverse("search"),
            reverse("group_list") + "?status=active&q=py",
            reverse("group_create"),
            reverse("group_detail", args=[self.group.pk]),
            reverse("group_detail", args=[self.group.pk]) + f"#syllabus-{item.pk}",
            reverse("group_update", args=[self.group.pk]),
            reverse("group_delete", args=[self.group.pk]),
            reverse("student_list") + f"?group={self.group.pk}&status=active",
            reverse("student_create") + f"?group={self.group.pk}",
            reverse("student_detail", args=[self.student.pk]),
            reverse("student_update", args=[self.student.pk]),
            reverse("student_delete", args=[self.student.pk]),
            reverse("topic_list"),
            reverse("topic_list") + f"?module={self.module.pk}&hidden=1",
            reverse("topic_list") + "?module=none",
            reverse("topic_create") + f"?module={self.module.pk}",
            reverse("topic_detail", args=[self.topic.pk]),
            reverse("topic_update", args=[self.topic.pk]),
            reverse("topic_delete", args=[self.topic.pk]),
            reverse("topic_import"),
            reverse("module_create"),
            reverse("module_update", args=[self.module.pk]),
            reverse("module_delete", args=[self.module.pk]),
            reverse("lesson_list") + "?status=planned",
            reverse("lesson_create") + f"?group={self.group.pk}",
            reverse("lesson_detail", args=[self.lesson.pk]),
            reverse("lesson_update", args=[self.lesson.pk]),
            reverse("lesson_delete", args=[self.lesson.pk]),
            reverse("attendance", args=[self.lesson.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_garbage_filter_values_do_not_500(self):
        for url in (
            reverse("student_list") + "?group=abc&status=zzz",
            reverse("lesson_list") + "?group=1;drop&status=x",
            reverse("group_list") + "?status=nope",
            reverse("topic_list") + "?module=abc",
            reverse("lesson_create") + "?group=x&topic=y",
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_pagination_keeps_filters(self):
        for i in range(45):
            f.student(self.group, full_name=f"Test {i:02}")
        response = self.client.get(reverse("student_list") + f"?group={self.group.pk}&q=Test")
        self.assertContains(response, f"?group={self.group.pk}&amp;q=Test&amp;page=2")


class TopicViewTests(ViewTestCase):
    def test_import_preview_then_confirm(self):
        url = reverse("topic_import")
        data = {"text": "# Django\n1. ORM — modellar\n2. Formalar", "default_duration": 80,
                "groups": [self.group.pk]}

        preview = self.client.post(url, data)
        self.assertContains(preview, "Ko‘rib chiqish")
        self.assertContains(preview, "ORM")
        self.assertFalse(Module.objects.filter(title="Django").exists())

        done = self.client.post(url, {**data, "confirm": "1"})
        self.assertRedirects(done, reverse("topic_list"))
        self.assertEqual(Topic.objects.filter(module__title="Django").count(), 2)
        self.assertEqual(Topic.objects.get(title="Formalar").duration_minutes, 80)
        self.assertEqual(self.group.syllabus.count(), 3)

    def test_import_rejects_empty_text(self):
        response = self.client.post(reverse("topic_import"), {"text": "  \n", "default_duration": 90})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())

    def test_export_downloads_text(self):
        response = self.client.get(reverse("topic_export"))
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertIn("# Python", response.content.decode())
        self.assertIn("1. Sikllar", response.content.decode())

    def test_duplicate_topic_in_same_module_rejected(self):
        response = self.client.post(reverse("topic_create"), {
            "module": self.module.pk, "title": "sikllar", "duration_minutes": 90, "order": 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["form"].errors)

    def test_hidden_topics_are_filtered_by_default(self):
        f.topic(title="Eski mavzu", is_active=False)
        self.assertNotContains(self.client.get(reverse("topic_list")), "Eski mavzu")
        self.assertContains(self.client.get(reverse("topic_list") + "?hidden=1"), "Eski mavzu")


class SyllabusViewTests(ViewTestCase):
    def test_mutations_require_post(self):
        item = self.group.syllabus.first()
        for url in (
            reverse("syllabus_add", args=[self.group.pk]),
            reverse("syllabus_toggle", args=[self.group.pk, item.pk]),
            reverse("lesson_complete", args=[self.lesson.pk]),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 405)

    def test_add_whole_module(self):
        extra = [f.topic(module=self.module) for _ in range(3)]
        f.topic(module=self.module, is_active=False)
        self.client.post(reverse("syllabus_add", args=[self.group.pk]), {"module": self.module.pk})
        self.assertEqual(
            set(self.group.syllabus.values_list("topic_id", flat=True)),
            {self.topic.pk, *(t.pk for t in extra)},
        )

    def test_toggle_item_of_other_group_is_404(self):
        other = f.group()
        item = self.group.syllabus.first()
        url = reverse("syllabus_toggle", args=[other.pk, item.pk])
        self.assertEqual(self.client.post(url, {"action": "taught"}).status_code, 404)

    def test_reorder(self):
        second = f.topic()
        self.group.add_topics([second])
        item = self.group.syllabus.get(topic=second)
        self.client.post(
            reverse("syllabus_toggle", args=[self.group.pk, item.pk]), {"action": "up"}
        )
        self.assertEqual(self.group.syllabus.first().topic, second)


class LessonViewTests(ViewTestCase):
    def test_create_suggests_next_topic_and_fills_homework(self):
        response = self.client.get(reverse("lesson_create") + f"?group={self.group.pk}")
        self.assertEqual(response.context["form"].initial["topic"], self.topic.pk)

        self.client.post(reverse("lesson_create"), {
            "group": self.group.pk, "topic": self.topic.pk, "held_on": "2026-10-01",
            "status": "planned",
        })
        self.assertEqual(Lesson.objects.latest("pk").homework, "5 ta mashq")

    def test_update_to_completed_syncs_syllabus(self):
        self.client.post(reverse("lesson_update", args=[self.lesson.pk]), {
            "group": self.group.pk, "topic": self.topic.pk,
            "held_on": self.lesson.held_on.isoformat(), "status": "completed",
        })
        item = SyllabusItem.objects.get(group=self.group, topic=self.topic)
        self.assertEqual(item.status, SyllabusItem.Status.TAUGHT)

    def test_attendance_save_and_complete(self):
        other = f.student(self.group)
        url = reverse("attendance", args=[self.lesson.pk])
        response = self.client.post(url, {
            f"status_{self.student.pk}": "late",
            f"status_{other.pk}": "bogus",
            f"note_{self.student.pk}": "10 daq.",
            "complete": "1",
        })
        self.assertRedirects(response, self.lesson.get_absolute_url())
        att = Attendance.objects.get(lesson=self.lesson, student=self.student)
        self.assertEqual((att.status, att.note), ("late", "10 daq."))
        self.assertFalse(Attendance.objects.filter(student=other).exists())
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.status, Lesson.Status.COMPLETED)

    def test_attendance_keeps_students_who_left_later(self):
        Attendance.objects.create(lesson=self.lesson, student=self.student)
        self.student.status = Student.Status.DROPPED
        self.student.save()
        response = self.client.get(reverse("attendance", args=[self.lesson.pk]))
        self.assertContains(response, "Aliyev Sardor")


class FormValidationTests(ViewTestCase):
    def test_group_code_normalized_and_errors_shown(self):
        self.client.post(reverse("group_create"), {"name": "Yangi", "code": " fe-3 ", "status": "active"})
        self.assertTrue(self.group.__class__.objects.filter(code="FE-3").exists())
        response = self.client.post(reverse("group_create"), {"name": "X", "code": "py-1", "status": "active"})
        self.assertContains(response, "errorlist")

    def test_bad_phone_rejected(self):
        response = self.client.post(reverse("student_create"), {
            "group": self.group.pk, "full_name": "Test", "phone": "12", "status": "active",
            "joined_at": "2026-10-01",
        })
        self.assertIn("phone", response.context["form"].errors)

    def test_add_another_redirects_back_to_form(self):
        response = self.client.post(reverse("student_create"), {
            "group": self.group.pk, "full_name": "Yangi Bola", "status": "active",
            "joined_at": "2026-10-01", "add_another": "1",
        })
        self.assertRedirects(response, reverse("student_create") + f"?group={self.group.pk}")
