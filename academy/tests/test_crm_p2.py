"""CRM redizayn P2: quvvat ayirish qarori, so'rov muddati, maosh "narx kiritilmagan", xato sahifasi."""

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy.models import Choice, Question, Quiz, QuizAttempt
from academy.services import create_quiz_batch

from . import factories as f


def warned_attempt():
    g = f.group()
    s = f.student(g)
    quiz = Quiz.objects.create(topic=f.topic())
    for n in range(3):
        q = Question.objects.create(quiz=quiz, text=f"S{n}", order=n)
        Choice.objects.create(question=q, text="A", is_correct=True)
        Choice.objects.create(question=q, text="B")
    batch = create_quiz_batch(quiz, [s], 3, 5)
    a = batch.attempts.get()
    QuizAttempt.objects.filter(pk=a.pk).update(status=QuizAttempt.Status.FINISHED, finished_at=timezone.now(),
                                               correct=1, total=3, leave_count=2)
    return QuizAttempt.objects.get(pk=a.pk)


class PenaltyDecisionTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())

    def test_form_is_compact_choice_with_confirmation(self):
        warned_attempt()
        page = self.client.get(reverse("quiz_warnings"))
        self.assertContains(page, 'name="amount"', count=2)  # select + "Kechirish"
        self.assertContains(page, "data-penalty-confirm")
        self.assertContains(page, "Ko‘rib chiqilmagan")

    def test_forgive_button_wins_over_select_value(self):
        a = warned_attempt()
        # Brauzer select (3) va "Kechirish" (0) qiymatini birga yuboradi — oxirgisi hal qiladi.
        self.client.post(reverse("attempt_penalty", args=[a.pk]), {"amount": ["3", "0"], "next": "/"})
        a.refresh_from_db()
        self.assertEqual(a.penalty, 0)
        self.assertIsNotNone(a.warning_checked_at)


class RequestsAndReportTests(TestCase):
    def test_profile_access_buttons_show_end_time(self):
        self.client.force_login(f.user())
        s = f.student(f.group())
        type(s).objects.filter(pk=s.pk).update(profile_requested_at=timezone.now())
        page = self.client.get(reverse("quiz_review_requests"))
        self.assertContains(page, " gacha")

    def test_report_shows_dash_when_rate_missing(self):
        boss = f.user(is_superuser=True, is_staff=True)
        teacher = f.user(username="t1")
        f.group(teacher=teacher)
        teachers.account_of(teacher)  # hisob bor, narx kiritilmagan
        self.client.force_login(boss)
        page = self.client.get(reverse("teacher_report"))
        self.assertContains(page, '<strong class="muted">—</strong>')
        self.assertContains(page, "narx kiritilmagan")


@override_settings(DEBUG=False)
class ErrorPageTests(TestCase):
    def test_404_has_reason_and_next_action_without_internals(self):
        page = self.client.get("/yoq-sahifa-404/")
        self.assertEqual(page.status_code, 404)
        self.assertContains(page, "Bosh sahifaga qaytish", status_code=404)
        self.assertNotContains(page, "URLconf", status_code=404)
