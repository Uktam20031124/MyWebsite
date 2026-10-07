from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy.forms import QuizForm
from academy.models import (
    Attendance,
    Choice,
    Question,
    Quiz,
    QuizAttempt,
    QuizBatch,
    Student,
    SyllabusItem,
    Topic,
)
from academy.quiz_bank import MIN_QUESTIONS, bank_entries, seed_quizzes, validate_bank
from academy.school_data import all_modules
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

QUIZ_TEXT = """? 2 + 2 nechiga teng?
+ 4
- 5
- 3

? Python'da ro'yxat
qaysi qavs bilan yoziladi?
- ( )
+ [ ]

? Quyidagi kod nima chiqaradi?
for i in range(2):
    print(i)
+ 0 va 1
- 1 va 2
"""


class ParseQuizTests(TestCase):
    def test_parses_questions_and_multiline_text(self):
        parsed, errors = parse_quiz(QUIZ_TEXT)
        self.assertEqual(errors, [])
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0], ("2 + 2 nechiga teng?", [("4", True), ("5", False), ("3", False)]))
        self.assertEqual(parsed[1][0], "Python'da ro'yxat\nqaysi qavs bilan yoziladi?")

    def test_code_indentation_is_kept(self):
        parsed, _ = parse_quiz(QUIZ_TEXT)
        self.assertEqual(
            parsed[2][0], "Quyidagi kod nima chiqaradi?\nfor i in range(2):\n    print(i)"
        )

    def test_reports_errors(self):
        _, errors = parse_quiz("+ javob\n? Savol\n- a\n- b\n? Ikkinchi\n+ a\n+ b\nxato qator")
        joined = " ".join(errors)
        self.assertIn("1-qator", joined)
        self.assertIn("1-savol: aynan bitta", joined)
        self.assertIn("2-savol: aynan bitta", joined)
        self.assertIn("8-qator", joined)

    def test_duplicate_choices_rejected(self):
        _, errors = parse_quiz("? Savol\n+ a\n- a")
        self.assertIn("1-savol: javob variantlari takrorlangan.", errors)

    def test_form_roundtrip(self):
        topic = f.topic()
        form = QuizForm({"time_limit_minutes": 5, "text": QUIZ_TEXT}, instance=Quiz(topic=topic))
        self.assertTrue(form.is_valid(), form.errors)
        quiz = form.save()
        self.assertEqual(quiz.questions.count(), 3)
        self.assertEqual(parse_quiz(quiz.as_text())[0], parse_quiz(QUIZ_TEXT)[0])

    def test_edit_keeps_unchanged_questions(self):
        # Yechilayotgan testlar savol id'lariga tayanadi — tahrir ularni buzmasligi kerak.
        quiz = Quiz.objects.create(topic=f.topic())
        quiz.replace_questions(parse_quiz(QUIZ_TEXT)[0])
        ids = list(quiz.questions.values_list("pk", flat=True))
        edited = QUIZ_TEXT.replace("- 5\n", "- 6\n") + "\n? Yangi savol\n+ ha\n- yo'q\n"
        quiz.replace_questions(parse_quiz(edited)[0])
        new_ids = list(quiz.questions.values_list("pk", flat=True))
        self.assertEqual(len(new_ids), 4)
        self.assertNotIn(ids[0], new_ids)  # o'zgargan savol almashtirildi
        self.assertEqual(new_ids[1:3], ids[1:3])  # o'zgarmaganlar saqlandi


class QuizBankTests(TestCase):
    def test_bank_is_valid_and_covers_every_topic(self):
        self.assertEqual(validate_bank(), [])
        keys = {t.key for m in all_modules() for t in m.topics}
        entries = {key: parsed for key, *_, parsed in bank_entries()}
        self.assertEqual(set(entries), keys)
        for key, parsed in entries.items():
            with self.subTest(topic=key):
                self.assertGreaterEqual(len(parsed), MIN_QUESTIONS)

    def _school_topics(self):
        module_data = all_modules()[0]
        module = f.module(title=module_data.title)
        return [f.topic(module=module, title=t.title) for t in module_data.topics[:2]]

    def test_seed_creates_quizzes_and_is_idempotent(self):
        first, second = self._school_topics()
        created, added = seed_quizzes(Topic, Quiz, Question, Choice)
        self.assertEqual(created, 2)
        self.assertGreaterEqual(first.quiz.questions.count(), MIN_QUESTIONS)
        self.assertEqual(
            Choice.objects.filter(question__quiz=first.quiz, is_correct=True).count(),
            first.quiz.questions.count(),
        )
        self.assertEqual(seed_quizzes(Topic, Quiz, Question, Choice), (0, 0))
        self.assertEqual(added, first.quiz.questions.count() + second.quiz.questions.count())

    def test_seed_respects_teacher_quizzes(self):
        small, full = self._school_topics()
        own = Quiz.objects.create(topic=small)
        own.replace_questions(parse_quiz(QUIZ_TEXT)[0])
        curated = Quiz.objects.create(topic=full)
        curated.replace_questions(parse_quiz(QUIZ_TEXT * 1)[0] * 4)  # 12 ta savol
        seed_quizzes(Topic, Quiz, Question, Choice)
        # Kichik testga bank savollari qo'shiladi, ustozning savollari qoladi.
        self.assertTrue(own.questions.filter(text="2 + 2 nechiga teng?").exists())
        self.assertGreater(own.questions.count(), MIN_QUESTIONS)
        # To'liq (>= 10 savol) testga tegilmaydi.
        self.assertEqual(curated.questions.count(), 12)


class QuizTestCase(TestCase):
    def setUp(self):
        self.group = f.group()
        self.student = f.student(self.group, full_name="Aliyev Sardor", telegram="sardor")
        self.dropped = f.student(self.group, status=Student.Status.DROPPED)
        self.topic = f.topic(title="Sikllar")
        self.quiz = Quiz.objects.create(topic=self.topic, time_limit_minutes=5)
        self.quiz.replace_questions(parse_quiz(QUIZ_TEXT)[0])
        self.lesson = f.lesson(self.group, topic=self.topic)
        self.batch = create_quiz_batch(self.quiz, [self.student], 3, 5, lesson=self.lesson)
        self.attempt = QuizAttempt.objects.get(student=self.student)
        self.url = self.attempt.get_absolute_url()

    def correct_answers(self, attempt=None):
        attempt = attempt or self.attempt
        attempt.refresh_from_db()
        return {
            f"q{q.pk}": str(q.choices.get(is_correct=True).pk) for q in attempt.questions()
        }


class SendQuizTests(QuizTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(f.user())
        self.send = reverse("quiz_send")

    def test_picker_lists_topics_with_lesson_topic_first(self):
        other = f.topic(title="Funksiyalar")
        Quiz.objects.create(topic=other).replace_questions(parse_quiz(QUIZ_TEXT)[0])
        f.topic(title="Testsiz mavzu")
        response = self.client.get(self.send, {"lesson": self.lesson.pk})
        self.assertContains(response, "Qaysi mavzu bo‘yicha test jo‘natamiz?")
        self.assertContains(response, "Dars mavzusi")
        self.assertContains(response, f"?lesson={self.lesson.pk}&amp;topic={other.pk}")
        self.assertContains(response, "Test savollari yo‘q")

    def test_picker_suggests_taught_topics_of_group(self):
        taught = f.topic(title="O'tilgan mavzu")
        Quiz.objects.create(topic=taught).replace_questions(parse_quiz(QUIZ_TEXT)[0])
        SyllabusItem.objects.create(
            group=self.group, topic=taught, order=1, status=SyllabusItem.Status.TAUGHT
        )
        response = self.client.get(self.send, {"lesson": self.lesson.pk})
        self.assertContains(response, "O‘tilgan")

    def test_form_prechecks_students_who_came(self):
        absent = f.student(self.group, full_name="Bo'lmagan Shogird")
        Attendance.objects.create(
            lesson=self.lesson, student=self.student, status=Attendance.Status.PRESENT
        )
        Attendance.objects.create(lesson=self.lesson, student=absent, status=Attendance.Status.ABSENT)
        response = self.client.get(self.send, {"lesson": self.lesson.pk, "topic": self.topic.pk})
        rows = {r["student"].pk: r["checked"] for r in response.context["rows"]}
        self.assertEqual(rows, {self.student.pk: True, absent.pk: False})
        self.assertContains(response, "Darsga kelganlar")
        self.assertContains(response, "bankda 3 ta savol")

    def test_send_creates_batch_with_count_and_time(self):
        second = f.student(self.group)
        response = self.client.post(
            f"{self.send}?lesson={self.lesson.pk}&topic={self.topic.pk}",
            {"students": [self.student.pk, second.pk], "question_count": 2, "time_limit_minutes": 7},
        )
        batch = QuizBatch.objects.latest("pk")
        self.assertRedirects(response, batch.get_absolute_url())
        self.assertEqual((batch.question_count, batch.time_limit_minutes), (2, 7))
        self.assertEqual((batch.lesson, batch.group), (self.lesson, self.group))
        self.assertEqual(set(batch.attempts.values_list("student_id", flat=True)), {self.student.pk, second.pk})

    def test_send_validation(self):
        url = f"{self.send}?topic={self.topic.pk}&group={self.group.pk}"
        response = self.client.post(url, {"students": [], "question_count": 99, "time_limit_minutes": 0})
        self.assertContains(response, "Kamida bitta shogirdni tanlang.")
        self.assertTrue(response.context["form"].errors["question_count"])
        self.assertTrue(response.context["form"].errors["time_limit_minutes"])
        # Boshqa guruh shogirdini yuborib bo'lmaydi.
        stranger = f.student()
        response = self.client.post(url, {"students": [stranger.pk], "question_count": 2, "time_limit_minutes": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(QuizBatch.objects.count(), 1)

    def test_topic_flow_switches_group(self):
        other_group = f.group(name="Boshqa guruh")
        newcomer = f.student(other_group, full_name="Yangi Shogird")
        response = self.client.get(self.send, {"topic": self.topic.pk, "group": other_group.pk})
        self.assertEqual([r["student"] for r in response.context["rows"]], [newcomer])
        self.assertContains(response, "Boshqa guruh")
        self.client.post(
            f"{self.send}?topic={self.topic.pk}&group={other_group.pk}",
            {"students": [newcomer.pk], "question_count": 3, "time_limit_minutes": 10},
        )
        batch = QuizBatch.objects.latest("pk")
        self.assertIsNone(batch.lesson)
        self.assertEqual(batch.group, other_group)

    def test_topic_without_questions_redirects_to_editor(self):
        topic = f.topic()
        response = self.client.get(self.send, {"topic": topic.pk})
        self.assertRedirects(response, reverse("quiz_edit", args=[topic.pk]))

    def test_attendance_save_then_send(self):
        response = self.client.post(
            reverse("attendance", args=[self.lesson.pk]),
            {f"status_{self.student.pk}": "present", "then": "quiz"},
        )
        self.assertRedirects(response, f"{self.send}?lesson={self.lesson.pk}")
        self.assertTrue(Attendance.objects.filter(lesson=self.lesson, student=self.student).exists())

    def test_batch_page_shows_telegram_share_link(self):
        response = self.client.get(self.batch.get_absolute_url())
        self.assertContains(response, "https://t.me/share/url?url=http%3A%2F%2Ftestserver%2Ft%2F")
        self.assertContains(response, "3+ta+savol%2C+5+daqiqa")
        self.assertContains(response, self.attempt.token)
        self.assertContains(response, "https://t.me/sardor")

    def test_renew_replaces_token(self):
        old = self.attempt.token
        response = self.client.post(reverse("quiz_attempt_renew", args=[self.attempt.pk]))
        self.assertRedirects(response, self.batch.get_absolute_url())
        self.attempt.refresh_from_db()
        self.assertNotEqual(self.attempt.token, old)
        self.client.logout()
        self.assertEqual(self.client.get(reverse("quiz_take", args=[old])).status_code, 404)

    def test_delete_batch(self):
        response = self.client.post(reverse("quiz_batch_delete", args=[self.batch.pk]))
        self.assertRedirects(response, f"{self.lesson.get_absolute_url()}#quiz")
        self.assertFalse(QuizAttempt.objects.exists())

    def test_lesson_deletion_keeps_results(self):
        self.lesson.delete()
        self.batch.refresh_from_db()
        self.assertIsNone(self.batch.lesson)
        self.assertTrue(self.batch.attempts.exists())

    def test_pages_render(self):
        for url in (
            reverse("quiz_edit", args=[self.topic.pk]),
            reverse("quiz_edit", args=[f.topic().pk]),
            reverse("quiz_delete", args=[self.topic.pk]),
            reverse("quiz_batches"),
            reverse("quiz_batches") + f"?group={self.group.pk}",
            self.send,
            self.lesson.get_absolute_url(),
            reverse("attendance", args=[self.lesson.pk]),
            self.topic.get_absolute_url(),
            reverse("topic_list"),
            self.student.get_absolute_url(),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_send_entry_points(self):
        send_with_topic = f"{self.send}?topic={self.topic.pk}"
        self.assertContains(self.client.get(reverse("topic_list")), send_with_topic)
        self.assertContains(self.client.get(self.topic.get_absolute_url()), send_with_topic)
        self.assertContains(self.client.get(self.lesson.get_absolute_url()), f"{self.send}?lesson={self.lesson.pk}")
        self.assertContains(self.client.get(reverse("attendance", args=[self.lesson.pk])), 'value="quiz"')

    def test_teacher_pages_require_login(self):
        self.client.logout()
        for url in (reverse("quiz_edit", args=[self.topic.pk]), self.send, self.batch.get_absolute_url()):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 302)


class StudentQuizTests(QuizTestCase):
    def test_get_does_not_start(self):
        # Telegram preview botlari havolani GET bilan ochadi — test boshlanib ketmasligi kerak.
        response = self.client.get(self.url)
        self.assertContains(response, "Testni boshlash")
        self.assertContains(response, "3 ta savol")
        self.assertContains(response, "5 daqiqa")
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, QuizAttempt.Status.PENDING)

    def test_random_subset_and_batch_time_limit(self):
        batch = create_quiz_batch(self.quiz, [self.student], 2, 7)
        attempt = batch.attempts.get()
        url = attempt.get_absolute_url()
        self.assertContains(self.client.get(url), "2 ta savol")
        before = timezone.now()
        self.client.post(url)
        attempt.refresh_from_db()
        self.assertEqual(len(attempt.question_ids), 2)
        self.assertTrue(set(attempt.question_ids) <= set(self.quiz.questions.values_list("pk", flat=True)))
        self.assertAlmostEqual(
            (attempt.deadline - before).total_seconds(), 7 * 60, delta=5
        )
        response = self.client.get(url)
        self.assertEqual(len(response.context["questions"]), 2)
        # Savolning birinchi qatoridan keyingi qismi (kod) alohida blokda, chekinishi bilan.
        multiline = sum("\n" in q.text for q in attempt.questions())
        self.assertContains(response, '<pre class="quiz-code">', count=multiline)
        if attempt.questions().filter(text__startswith="Quyidagi").exists():
            self.assertContains(response, "for i in range(2):\n    print(i)</pre>")
        self.client.post(reverse("quiz_submit", args=[attempt.token]), self.correct_answers(attempt))
        attempt.refresh_from_db()
        self.assertEqual((attempt.correct, attempt.total, attempt.percent), (2, 2, 100))

    def test_full_flow_and_one_time_link(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, self.url)
        response = self.client.get(self.url)
        self.assertContains(response, "data-quiz-timer")
        self.assertContains(response, 'data-seconds="')

        response = self.client.post(reverse("quiz_submit", args=[self.attempt.token]), self.correct_answers())
        self.assertRedirects(response, self.url)
        self.attempt.refresh_from_db()
        self.assertEqual((self.attempt.correct, self.attempt.total, self.attempt.percent), (3, 3, 100))
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
        self.assertEqual(self.attempt.correct, 3)

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
        self.assertEqual(self.attempt.correct, 3)

    def test_unknown_token_404(self):
        self.assertEqual(self.client.get(reverse("quiz_take", args=["nope"])).status_code, 404)
