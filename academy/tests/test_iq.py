import importlib
from math import factorial

from django.apps import apps
from django.test import TestCase

from academy.models import Question, Quiz, SyllabusItem, Topic
from academy.quiz_format import parse_quiz
from academy.school_data.iq import MODULES, TIME_LIMIT, TRACK
from academy.school_data.quizzes_iq import QUIZZES

from . import factories as f

migration = importlib.import_module("academy.migrations.0036_iq_tests")


def correct(key: str, n: int) -> str:
    """``key`` testining ``n``-savolidagi (1 dan) to'g'ri javob matni."""
    _text, choices = parse_quiz(QUIZZES[key])[0][n - 1]
    return next(c for c, ok in choices if ok)


class IqBankTests(TestCase):
    def test_answers_are_computed_correctly(self):
        # Sonli ketma-ketliklar: qonuniyat bo'yicha keyingi son.
        expected = [
            32, 19, 36, 13, 1, 42, 28, 125, 25, 17, factorial(6), 15, 360, 63,
        ]
        self.assertEqual([int(correct("IQ01", i)) for i in range(1, 15)], expected)
        self.assertEqual([n * n + 1 for n in range(1, 7)][-1], 37)  # 35 — mos emas
        self.assertEqual(int(correct("IQ01", 15)), 35)
        # Hisob masalalari.
        self.assertEqual(int(correct("IQ05", 1)), 25 * 4 + 50 // 2)
        self.assertEqual(correct("IQ05", 2), f"{7 * 1500 + 3 * 2000} so'm")
        self.assertEqual(int(correct("IQ05", 5)), 30 - 30 * 40 // 100)
        self.assertEqual(int(correct("IQ05", 12)), sum(range(2, 21, 2)))
        self.assertEqual(int(correct("IQ02", 6)), 5 * 4 // 2)
        self.assertEqual(int(correct("IQ04", 7)), 9 + 4 + 1)

    def test_every_topic_has_15_questions(self):
        self.assertEqual(list(QUIZZES), TRACK)
        for key in TRACK:
            parsed, errors = parse_quiz(QUIZZES[key])
            self.assertEqual((len(parsed), errors), (15, []), key)


class IqMigrationTests(TestCase):
    def test_loads_topics_quizzes_without_touching_groups(self):
        group = f.group()
        migration.forwards(apps, None)
        topics = Topic.objects.filter(module__title=MODULES[0].title)
        self.assertEqual(topics.count(), 5)
        self.assertEqual(topics.exclude(title_ru="").exclude(study="").exclude(study_ru="").count(), 5)
        self.assertEqual(Question.objects.filter(quiz__topic__in=topics).count(), 75)
        self.assertEqual(Question.objects.filter(quiz__topic__in=topics, text_ru="").count(), 0)
        self.assertTrue(all(q.time_limit_minutes == TIME_LIMIT for q in Quiz.objects.filter(topic__in=topics)))
        self.assertFalse(SyllabusItem.objects.filter(group=group).exists())  # guruh dasturiga qo'shilmaydi

        migration.forwards(apps, None)  # qayta ishga tushirish — takrorlanmaydi
        self.assertEqual(Question.objects.filter(quiz__topic__in=topics).count(), 75)

    def test_empty_database_untouched(self):
        migration.forwards(apps, None)
        self.assertFalse(Topic.objects.exists())
