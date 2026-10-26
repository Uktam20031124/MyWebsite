from django.test import TestCase

from academy import coins
from academy.models import Quiz
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 11))


class RepeatProfileTestCoinsTests(TestCase):
    def setUp(self):
        self.ali = f.student(f.group())
        self.quiz = Quiz.objects.create(topic=f.topic())
        self.quiz.replace_questions(parse_quiz(TEXT)[0])

    def take(self, correct: int, from_profile=True):
        batch = create_quiz_batch(self.quiz, [self.ali], 10, 5)
        batch.from_profile = from_profile
        batch.save(update_fields=["from_profile"])
        attempt = batch.attempts.get()
        attempt.start("k")
        attempt.refresh_from_db()
        qs = list(attempt.questions())
        attempt.finish({str(q.pk): q.choices.get(is_correct=i < correct).pk for i, q in enumerate(qs)})
        before = getattr(self, "_balance", 0)
        self._balance = coins.balance(self.ali)
        return self._balance - before

    def test_after_two_profile_attempts_only_90_plus_gets_one(self):
        self.assertIsNone(coins.repeat_info(self.ali, self.quiz.pk))
        self.assertEqual(self.take(10), 10)  # 1-urinish: odatdagidek
        self.assertEqual(self.take(8), 7)  # 2-urinish: odatdagidek
        self.assertEqual(coins.repeat_info(self.ali, self.quiz.pk)["done"], 2)
        self.assertEqual(self.take(8), 0)  # 3-urinish, 80% — berilmaydi
        self.assertEqual(self.take(9), 1)  # 90% — 1 ⚡️
        self.assertEqual(self.take(10), 1)  # 100% — 1 ⚡️
        tx = self.ali.coins.first()
        self.assertEqual(tx.display_reason, "Takroriy test: 100%")

    def test_teacher_sent_tests_unchanged(self):
        self.take(10)
        self.take(10)
        self.assertEqual(self.take(8, from_profile=False), 7)  # ustoz yuborgan — odatdagi qoida
        self.assertEqual(self.take(10, from_profile=False), 10)
