from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy.forms import QuizForm
from academy.models import Quiz, QuizAttempt, Student
from academy.services import ensure_quiz_attempts, parse_quiz

from . import factories as f

QUIZ_TEXT = """? 2 + 2 nechiga teng?
+ 4
- 5
- 3

? Python'da ro'yxat
qaysi qavs bilan yoziladi?
- ( )
+ [ ]
"""


class ParseQuizTests(TestCase):
    def test_parses_questions_and_multiline_text(self):
        parsed, errors = parse_quiz(QUIZ_TEXT)
        self.assertEqual(errors, [])
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0], ("2 + 2 nechiga teng?", [("4", True), ("5", False), ("3", False)]))
        self.assertEqual(parsed[1][0], "Python'da ro'yxat\nqaysi qavs bilan yoziladi?")

    def test_reports_errors(self):
        _, errors = parse_quiz("+ javob\n? Savol\n- a\n- b\n? Ikkinchi\n+ a\n+ b\nxato qator")
        joined = " ".join(errors)
        self.assertIn("1-qator", joined)
        self.assertIn("1-savol: aynan bitta", joined)
        self.assertIn("2-savol: aynan bitta", joined)
        self.assertIn("8-qator", joined)

    def test_form_roundtrip(self):
        topic = f.topic()
        form = QuizForm({"time_limit_minutes": 5, "text": QUIZ_TEXT}, instance=Quiz(topic=topic))
        self.assertTrue(form.is_valid(), form.errors)
        quiz = form.save()
        self.assertEqual(quiz.questions.count(), 2)
        self.assertEqual(parse_quiz(quiz.as_text())[0], parse_quiz(QUIZ_TEXT)[0])


class QuizTestCase(TestCase):
    def setUp(self):
        self.group = f.group()
        self.student = f.student(self.group, full_name="Aliyev Sardor", telegram="sardor")
        f.student(self.group, status=Student.Status.DROPPED)
        self.topic = f.topic(title="Sikllar")
        self.quiz = Quiz.objects.create(topic=self.topic, time_limit_minutes=5)
        self.quiz.replace_questions(parse_quiz(QUIZ_TEXT)[0])
        self.lesson = f.lesson(self.group, topic=self.topic)
        ensure_quiz_attempts(self.lesson)
        self.attempt = QuizAttempt.objects.get(student=self.student)
        self.url = self.attempt.get_absolute_url()

    def correct_answers(self):
        return {
            f"q{q.pk}": str(q.choices.get(is_correct=True).pk) for q in self.quiz.questions.all()
        }


class TeacherQuizTests(QuizTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(f.user())

    def test_links_only_for_active_students_and_idempotent(self):
        self.assertEqual(self.lesson.quiz_attempts.count(), 1)
        self.assertEqual(ensure_quiz_attempts(self.lesson), 0)
        newcomer = f.student(self.group)
        self.client.post(reverse("lesson_quiz_links", args=[self.lesson.pk]))
        self.assertTrue(self.lesson.quiz_attempts.filter(student=newcomer).exists())

    def test_lesson_page_shows_telegram_share_link(self):
        response = self.client.get(self.lesson.get_absolute_url())
        self.assertContains(response, "https://t.me/share/url?url=http%3A%2F%2Ftestserver%2Ft%2F")
        self.assertContains(response, self.attempt.token)
        self.assertContains(response, "https://t.me/sardor")

    def test_pages_render(self):
        for url in (
            reverse("quiz_edit", args=[self.topic.pk]),
            reverse("quiz_edit", args=[f.topic().pk]),
            reverse("quiz_delete", args=[self.topic.pk]),
            self.topic.get_absolute_url(),
            reverse("topic_list"),
            self.student.get_absolute_url(),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_create_quiz(self):
        topic = f.topic()
        response = self.client.post(
            reverse("quiz_edit", args=[topic.pk]), {"time_limit_minutes": 7, "text": QUIZ_TEXT}
        )
        self.assertRedirects(response, f"{topic.get_absolute_url()}#quiz")
        self.assertEqual(topic.quiz.questions.count(), 2)

    def test_renew_replaces_token(self):
        old = self.attempt.token
        self.client.post(reverse("quiz_attempt_renew", args=[self.attempt.pk]))
        self.attempt.refresh_from_db()
        self.assertNotEqual(self.attempt.token, old)
        self.client.logout()
        self.assertEqual(self.client.get(reverse("quiz_take", args=[old])).status_code, 404)

    def test_teacher_pages_require_login(self):
        self.client.logout()
        response = self.client.get(reverse("quiz_edit", args=[self.topic.pk]))
        self.assertEqual(response.status_code, 302)


class StudentQuizTests(QuizTestCase):
    def test_get_does_not_start(self):
        # Telegram preview botlari havolani GET bilan ochadi — test boshlanib ketmasligi kerak.
        response = self.client.get(self.url)
        self.assertContains(response, "Testni boshlash")
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, QuizAttempt.Status.PENDING)

    def test_full_flow_and_one_time_link(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.url)
        response = self.client.get(self.url)
        self.assertContains(response, "data-quiz-timer")
        self.assertContains(response, 'data-seconds="')

        response = self.client.post(reverse("quiz_submit", args=[self.attempt.token]), self.correct_answers())
        self.assertRedirects(response, self.url)
        self.attempt.refresh_from_db()
        self.assertEqual((self.attempt.correct, self.attempt.total, self.attempt.percent), (2, 2, 100))
        self.assertContains(self.client.get(self.url), "100%")

        # Boshqa brauzer/qurilma: havola ishlamaydi.
        self.client.cookies.clear()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 410)
        self.assertContains(response, "Havola ishlatilgan", status_code=410)

    def test_second_device_cannot_open_active_test(self):
        self.client.post(self.url)
        other = self.client_class()
        self.assertEqual(other.get(self.url).status_code, 410)
        self.assertEqual(other.post(self.url).status_code, 410)
        other.post(reverse("quiz_submit", args=[self.attempt.token]), self.correct_answers())
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, QuizAttempt.Status.ACTIVE)

    def test_resubmit_does_not_change_score(self):
        self.client.post(self.url)
        submit = reverse("quiz_submit", args=[self.attempt.token])
        self.client.post(submit, {})
        self.client.post(submit, self.correct_answers())
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.correct, 0)

    def test_timeout_auto_finishes_with_saved_answers(self):
        self.client.post(self.url)
        response = self.client.post(reverse("quiz_save", args=[self.attempt.token]), self.correct_answers())
        self.assertEqual(response.json()["ok"], True)
        later = timezone.now() + timedelta(minutes=10)
        with mock.patch("django.utils.timezone.now", return_value=later):
            # Kech yuborilgan javoblar qabul qilinmaydi, saqlangani baholanadi.
            self.client.post(reverse("quiz_submit", args=[self.attempt.token]), {})
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, QuizAttempt.Status.FINISHED)
        self.assertTrue(self.attempt.timed_out)
        self.assertEqual(self.attempt.correct, 2)

    def test_expired_attempt_finalized_on_open(self):
        self.client.post(self.url)
        later = timezone.now() + timedelta(minutes=10)
        with mock.patch("django.utils.timezone.now", return_value=later):
            response = self.client.get(self.url)
        self.assertContains(response, "Vaqt tugadi")
        self.attempt.refresh_from_db()
        self.assertEqual((self.attempt.status, self.attempt.correct), (QuizAttempt.Status.FINISHED, 0))

    def test_timeout_flag_from_browser(self):
        self.client.post(self.url)
        self.client.post(
            reverse("quiz_submit", args=[self.attempt.token]), {**self.correct_answers(), "timeout": "1"}
        )
        self.attempt.refresh_from_db()
        self.assertTrue(self.attempt.timed_out)
        self.assertEqual(self.attempt.correct, 2)

    def test_unknown_token_404(self):
        self.assertEqual(self.client.get(reverse("quiz_take", args=["nope"])).status_code, 404)
