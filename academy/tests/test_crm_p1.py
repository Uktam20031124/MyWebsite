"""CRM redizayn P1: ro'yxatlar (filtr, CSV doirasi), kechikkan dars, mavzular, vazifalar, jo'natish oqimi, ariza."""

from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy.models import Choice, HomeworkSubmission, Lesson, Question, Quiz, Registration, RegistrationLink, Student

from . import factories as f


class ListTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())

    def test_students_csv_label_states_scope_and_filter_count(self):
        g = f.group()
        f.student(g)
        f.student(g)
        f.student(f.group())
        page = self.client.get(reverse("student_list"), {"group": g.pk, "status": "active"})
        self.assertContains(page, "CSV · 2 ta")
        self.assertContains(page, 'class="badge info count tabular">2<')  # 2 ta filtr faol
        self.assertContains(page, "Filtrlarni tozalash")
        self.assertContains(page, 'class="table responsive"')

    def test_overdue_lesson_shows_only_kechikkan(self):
        g = f.group()
        f.lesson(g, days=-3)
        page = self.client.get(reverse("lesson_list"))
        self.assertContains(page, "Kechikkan")
        self.assertNotContains(page, '<span class="chip info">Rejada</span>')

    def test_topics_sections_collapse_and_open_on_search(self):
        m = f.module(title="Sikllar")
        for n in range(3):
            f.topic(module=m, title=f"for sikli {n}")
        f.topic(module=f.module(title="A"))
        f.topic(module=f.module(title="B"))
        closed = self.client.get(reverse("topic_list"))
        self.assertContains(closed, '<details class="card module-card" data-remember-list="topics">')
        opened = self.client.get(reverse("topic_list"), {"q": "sikl"})
        self.assertContains(opened, 'data-remember-list="topics" open>')
        self.assertContains(opened, "Savol qo‘shish")  # "Test" o'rniga aniq yorliq


class HomeworkRuleTests(TestCase):
    def test_on_time_and_late_chips(self):
        self.client.force_login(f.user())
        g = f.group()
        lesson = f.lesson(g, days=-1, status=Lesson.Status.COMPLETED)
        HomeworkSubmission.objects.create(student=f.student(g), lesson=lesson, text="a", on_time=True)
        HomeworkSubmission.objects.create(student=f.student(g), lesson=lesson, text="b", on_time=False)
        page = self.client.get(reverse("homework_list"))
        self.assertContains(page, "Muddatida")
        self.assertContains(page, "50+ ball → +3 ⚡️")
        self.assertContains(page, "quvvat berilmaydi")


class QuizSendFlowTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.group = f.group()
        f.student(self.group)
        self.ready = f.topic(title="Tayyor")
        quiz = Quiz.objects.create(topic=self.ready)
        for n in range(3):
            q = Question.objects.create(quiz=quiz, text=f"S{n}", order=n)
            Choice.objects.create(question=q, text="A", is_correct=True)
            Choice.objects.create(question=q, text="B")
        f.topic(title="Savolsiz")

    def test_picker_hides_topics_without_bank(self):
        page = self.client.get(reverse("quiz_send"), {"group": self.group.pk})
        self.assertEqual(page.context["empty_n"], 1)
        self.assertContains(page, "pick-row no-bank")
        self.assertContains(page, 'class="steps"')

    def test_step_two_has_review_and_honest_labels(self):
        page = self.client.get(reverse("quiz_send"), {"group": self.group.pk, "topic": self.ready.pk})
        markers = ("data-send-summary", "Faqat havolalarni yaratish", "Yaratish va yuborishni rejalash", "Hammasi (1)")
        for marker in markers:
            self.assertContains(page, marker)


class RegistrationDuplicateTests(TestCase):
    def test_second_click_does_not_create_duplicate(self):
        self.client.force_login(f.user())
        g = f.group()
        link = RegistrationLink.objects.create(title="L", group=g)
        reg = Registration.objects.create(link=link, full_name="Yangi Bola", phone="+998900000001", telegram="yb")
        url = reverse("registration_action", args=[reg.pk])
        before = Student.objects.count()
        first = self.client.post(url, {"action": "create", "group": g.pk})
        second = self.client.post(url, {"action": "create", "group": g.pk})
        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 404)  # faqat "Kutilmoqda" ariza qabul qilinadi
        self.assertEqual(Student.objects.count(), before + 1)
        reg.refresh_from_db()
        self.assertEqual(reg.status, Registration.Status.APPROVED)
        self.assertLess(timezone.now() - reg.reviewed_at, timedelta(minutes=1))
