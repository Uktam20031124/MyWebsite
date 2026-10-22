from django.test import TestCase
from django.urls import reverse

from academy import coins
from academy.models import Quiz, QuizAttempt
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 4))


class TestWarningsTests(TestCase):
    def setUp(self):
        self.ali = f.student(f.group(), full_name="Ali Valiyev")
        quiz = Quiz.objects.create(topic=f.topic(title="Sikllar"))
        quiz.replace_questions(parse_quiz(TEXT)[0])
        self.attempt = create_quiz_batch(quiz, [self.ali], 3, 5).attempts.get()
        self.student = self.client_class()
        self.student.post(self.attempt.get_absolute_url())  # boshlash (cookie)
        self.attempt.refresh_from_db()
        self.answers = {f"q{q.pk}": q.choices.get(is_correct=True).pk for q in self.attempt.questions()}
        self.teacher = self.client_class()
        self.teacher.force_login(f.user())

    def finish(self, **warnings):
        self.student.post(reverse("quiz_submit", args=[self.attempt.token]), {**self.answers, **warnings})
        self.attempt.refresh_from_db()

    def test_warnings_saved_on_finish_and_never_decrease(self):
        save = reverse("quiz_save", args=[self.attempt.token])
        self.student.post(save, {"leave_count": "2", "away_seconds": "30", "copy_count": "3"})
        self.finish(leave_count="1", copy_count="0")  # o'quvchi kamaytira olmaydi
        self.assertEqual(self.attempt.status, QuizAttempt.Status.FINISHED)
        self.assertEqual((self.attempt.leave_count, self.attempt.copy_count), (2, 3))
        self.assertEqual(self.attempt.warning_count, 5)

    def test_take_page_has_copy_tracking(self):
        r = self.student.get(self.attempt.get_absolute_url())
        self.assertContains(r, "data-quiz-copies")
        self.assertContains(r, 'data-reason="copy"')

    def test_teacher_list_and_penalty(self):
        self.finish(leave_count="2", copy_count="1")
        coins.gift(self.ali, 3)
        balance = coins.balance(self.ali)
        r = self.teacher.get(reverse("quiz_warnings"))
        self.assertContains(r, "Ali Valiyev")
        self.assertEqual(r.context["pending_n"], 1)
        self.assertEqual(r.context["nav_warnings"], 1)

        url = reverse("attempt_penalty", args=[self.attempt.pk])
        self.teacher.post(url, {"amount": "4"})
        self.assertEqual(coins.balance(self.ali), balance - 4)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.penalty, 4)
        self.assertIsNotNone(self.attempt.warning_checked_at)
        tx = self.ali.coins.get(amount=-4)
        self.assertEqual(tx.display_reason, "⚠️ Test qoidasi buzildi: Sikllar")

        # Qayta qaror avvalgisini almashtiradi (ikki marta olinmaydi), 0 — kechirish.
        self.teacher.post(url, {"amount": "2"})
        self.assertEqual(coins.balance(self.ali), balance - 2)
        self.teacher.post(url, {"amount": "0"})
        self.assertEqual(coins.balance(self.ali), balance)
        self.assertEqual(self.teacher.get(reverse("quiz_warnings")).context["pending_n"], 0)
        # 1–5 dan tashqari — rad etiladi.
        self.teacher.post(url, {"amount": "9"})
        self.assertEqual(coins.balance(self.ali), balance)

    def test_penalty_capped_by_balance(self):
        self.finish(leave_count="1")
        before = coins.balance(self.ali)
        self.assertEqual(coins.penalize(self.attempt, 5), min(5, before))
        self.assertEqual(coins.balance(self.ali), max(0, before - 5))

    def test_no_warnings_not_listed_and_review_has_form(self):
        self.finish()
        self.assertEqual(self.teacher.get(reverse("quiz_warnings")).context["pending_n"], 0)
        r = self.teacher.post(reverse("attempt_penalty", args=[self.attempt.pk]), {"amount": "1"})
        self.assertEqual(r.status_code, 404)  # ogohlantirishsiz testga jarima yo'q
        self.attempt.copy_count = 1
        self.attempt.save()
        r = self.teacher.get(reverse("quiz_attempt_review", args=[self.attempt.pk]))
        self.assertContains(r, reverse("attempt_penalty", args=[self.attempt.pk]))

    def test_forgive_all(self):
        self.finish(leave_count="1")
        self.teacher.post(reverse("quiz_warnings"), {"action": "forgive_all"})
        self.attempt.refresh_from_db()
        self.assertIsNotNone(self.attempt.warning_checked_at)
        self.assertEqual(self.attempt.penalty, 0)

    def test_login_required(self):
        self.assertEqual(self.client.get(reverse("quiz_warnings")).status_code, 302)
