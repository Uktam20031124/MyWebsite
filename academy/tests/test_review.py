from django.urls import reverse

from academy.models import QuizAttempt
from academy.services import create_quiz_batch, hardest_questions, parse_quiz

from . import factories as f
from .test_quiz import QuizTestCase


class ReviewTestCase(QuizTestCase):
    """Sardor testni yechadi: 1-savol to'g'ri, 2-savol xato, 3-savol javobsiz."""

    def setUp(self):
        super().setUp()
        self.client.post(self.url)  # testni boshlash
        self.attempt.refresh_from_db()
        q = {qq.text.split("\n")[0]: qq for qq in self.quiz.questions.all()}
        self.q_sum = q["2 + 2 nechiga teng?"]
        self.q_list = q["Python'da ro'yxat"]
        self.q_code = q["Quyidagi kod nima chiqaradi?"]
        answers = {
            f"q{self.q_sum.pk}": str(self.q_sum.choices.get(text="4").pk),
            f"q{self.q_list.pk}": str(self.q_list.choices.get(text="( )").pk),
        }
        self.client.post(reverse("quiz_submit", args=[self.attempt.token]), answers)
        self.attempt.refresh_from_db()
        self.review_url = reverse("quiz_attempt_review", args=[self.attempt.pk])


class SnapshotTests(ReviewTestCase):
    def test_snapshot_saved_on_finish(self):
        snap = {item["id"]: item for item in self.attempt.snapshot}
        self.assertEqual(len(snap), 3)
        self.assertTrue(snap[self.q_sum.pk]["is_correct"])
        self.assertFalse(snap[self.q_list.pk]["is_correct"])
        self.assertIsNone(snap[self.q_code.pk]["picked"])
        self.assertEqual((self.attempt.correct, self.attempt.total), (1, 3))
        # Tartib — o'quvchiga berilgan tartib.
        self.assertEqual([i["id"] for i in self.attempt.snapshot], self.attempt.question_ids)

    def test_review_survives_quiz_edit(self):
        self.quiz.replace_questions(parse_quiz("? Butunlay yangi savol\n+ ha\n- yo'q")[0])
        texts = [i["title"] for i in self.attempt.review()]
        self.assertIn("2 + 2 nechiga teng?", texts)
        self.assertNotIn("Butunlay yangi savol", texts)

    def test_legacy_attempt_without_snapshot(self):
        QuizAttempt.objects.filter(pk=self.attempt.pk).update(snapshot=[])
        self.attempt.refresh_from_db()
        items = {i["id"]: i for i in self.attempt.review()}
        self.assertEqual(items[self.q_list.pk]["correct_text"], "[ ]")
        self.assertEqual(items[self.q_list.pk]["picked_text"], "( )")

    def test_review_does_not_mutate_snapshot(self):
        self.attempt.review()
        self.attempt.save()
        self.attempt.refresh_from_db()
        self.assertNotIn("correct_text", self.attempt.snapshot[0])


class StudentCannotSeeAnswersTests(ReviewTestCase):
    def test_result_page_shows_own_marks_but_not_correct_answers(self):
        self.attempt.decide_reveal(True)  # ustoz ruxsat bergan
        page = self.client.get(self.url)  # o'quvchining o'z brauzeri (cookie bor)
        self.assertContains(page, "33%")
        self.assertContains(page, "1 / 3 to‘g‘ri javob")
        # O'z javoblari va to'g'ri/xato belgisi ko'rinadi.
        self.assertContains(page, "Javobingiz: <strong>4</strong>")
        self.assertContains(page, "Javobingiz: <strong>( )</strong>")
        self.assertContains(page, "— to‘g‘ri", count=1)
        self.assertContains(page, "— xato", count=1)
        self.assertContains(page, "Javob berilmagan")
        # To'g'ri variant (xato va javobsiz savollarda) va boshqa variantlar ko'rinmaydi.
        for secret in ("[ ]", "0 va 1", "1 va 2", "to‘g‘ri javob</span>", "<strong>5</strong>"):
            self.assertNotContains(page, secret)

    def test_result_order_matches_order_shown_in_test(self):
        from academy.views import _shuffled_questions, review_in_shown_order

        shown = [q.pk for q in _shuffled_questions(self.attempt)]
        self.assertEqual([i["id"] for i in review_in_shown_order(self.attempt)], shown)
        self.attempt.decide_reveal(True)
        page = self.client.get(self.url).content.decode()
        titles = [self.quiz.questions.get(pk=pk).text.split("\n")[0] for pk in shown]
        positions = [page.index(f"{n}. {t}".replace("'", "&#x27;")) for n, t in enumerate(titles, 1)]
        self.assertEqual(positions, sorted(positions))

    def test_other_device_sees_nothing(self):
        self.client.cookies.clear()
        page = self.client.get(self.url)
        self.assertEqual(page.status_code, 410)
        self.assertNotContains(page, "Javobingiz", status_code=410)

    def test_review_requires_login(self):
        response = self.client.get(self.review_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])


class TeacherReviewTests(ReviewTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(f.user())

    def test_review_page(self):
        page = self.client.get(self.review_url)
        self.assertContains(page, "Aliyev Sardor")
        self.assertContains(page, "33%")
        self.assertContains(page, "o‘quvchi tanlagan", count=2)
        self.assertContains(page, "to‘g‘ri javob</span>", count=3)
        self.assertContains(page, "Javob berilmagan")
        self.assertContains(page, "for i in range(2):\n    print(i)</pre>")
        self.assertContains(page, "Faqat siz ko‘rasiz")

    def test_only_wrong_filter(self):
        page = self.client.get(self.review_url, {"xato": "1"})
        self.assertNotContains(page, "2 + 2 nechiga teng?")
        self.assertContains(page, "Python&#x27;da ro&#x27;yxat")
        self.assertContains(page, "Quyidagi kod nima chiqaradi?")

    def test_unfinished_attempt_404(self):
        other = create_quiz_batch(self.quiz, [self.student], 2, 5).attempts.get()
        self.assertEqual(
            self.client.get(reverse("quiz_attempt_review", args=[other.pk])).status_code, 404
        )

    def test_batch_page_links_and_hardest_questions(self):
        page = self.client.get(self.batch.get_absolute_url())
        self.assertContains(page, self.review_url)
        self.assertContains(page, "Eng ko‘p xato qilingan savollar")
        self.assertContains(page, "to‘g‘ri: [ ]")
        self.assertContains(page, "ko‘p tanlangan xato: «( )» (1)")
        student_page = self.client.get(self.student.get_absolute_url())
        self.assertContains(student_page, self.review_url)

    def test_prev_next_navigation(self):
        second = f.student(self.group, full_name="Bobur Valiyev")
        batch = self.batch
        extra = QuizAttempt.objects.create(batch=batch, quiz=self.quiz, student=second)
        extra.start("k")
        extra.finish({})
        page = self.client.get(self.review_url)
        self.assertContains(page, reverse("quiz_attempt_review", args=[extra.pk]))


class HardestQuestionsTests(QuizTestCase):
    def test_ranking(self):
        quiz_text_qs = {q.text.split("\n")[0]: q for q in self.quiz.questions.all()}
        q_sum = quiz_text_qs["2 + 2 nechiga teng?"]
        attempts = []
        for n, pick in enumerate(["5", "5", "4"]):
            student = f.student(self.group)
            a = QuizAttempt.objects.create(batch=self.batch, quiz=self.quiz, student=student)
            a.start(f"k{n}")
            a.refresh_from_db()
            a.finish({str(q_sum.pk): q_sum.choices.get(text=pick).pk})
            attempts.append(a)
        rows = {r["title"]: r for r in hardest_questions(attempts)}
        row = rows["2 + 2 nechiga teng?"]
        self.assertEqual((row["asked"], row["wrong"], row["pct_wrong"]), (3, 2, 67))
        self.assertEqual((row["top_wrong"], row["top_wrong_n"]), ("5", 2))
        self.assertEqual(rows["Python'da ro'yxat"]["unanswered"], 3)
