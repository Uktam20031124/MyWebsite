from unittest import mock

from django.test import TestCase
from django.urls import reverse

from academy import telegram_sender as tg
from academy.automation import reminder_text
from academy.forms import QuizForm
from academy.models import Quiz, QuizAttempt, QuizBatch
from academy.quiz_format import translation_errors
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

UZ = """? Ro'yxat qaysi qavs bilan yoziladi?
+ [ ]
- ( )

? len("salom") nimaga teng?
- 4
+ 5"""

RU = """? Какой скобкой записывается список?
+ [ ]
- ( )

? Чему равно len("salom")?
- 4
+ 5"""


def ok_results(items, **kw):
    return [tg.Result(i.key, True) for i in items]


class Base(TestCase):
    def setUp(self):
        self.group = f.group(name="S-009 · Starter", code="S-009")
        self.ali = f.student(self.group, full_name="Ali Valiyev", telegram="ali_v")
        self.ivan = f.student(self.group, full_name="Ivan Petrov", telegram="ivan_p")
        self.topic = f.topic(title="Ro'yxatlar", title_ru="Списки")
        self.quiz = Quiz.objects.create(topic=self.topic)
        self.quiz.replace_questions(parse_quiz(UZ)[0])
        self.quiz.apply_translation(parse_quiz(RU)[0])
        self.client.force_login(f.user())


class TranslationTests(Base):
    def test_apply_and_roundtrip(self):
        first = self.quiz.questions.first()
        self.assertEqual(first.text_ru, "Какой скобкой записывается список?")
        # "[ ]" tarjimada ham bir xil — "tarjima yo'q" deb saqlanadi, o'zbekchasi ko'rinadi.
        self.assertEqual(first.choices.first().text_ru, "")
        self.assertEqual(first.choices.first().text_in("ru"), "[ ]")
        self.assertEqual(self.quiz.translated_count, 2)
        self.assertEqual(self.quiz.as_text_ru(), RU)

    def test_alignment_errors(self):
        uz = parse_quiz(UZ)[0]
        self.assertIn("2 ta", translation_errors(uz, parse_quiz(RU.split("\n\n")[0])[0])[0])
        swapped = RU.replace("+ [ ]\n- ( )", "- [ ]\n+ ( )")
        self.assertIn("boshqa o‘rinda", translation_errors(uz, parse_quiz(swapped)[0])[0])

    def test_edit_form(self):
        form = QuizForm({"time_limit_minutes": 5, "text": UZ, "text_ru": RU.split("\n\n")[0]}, instance=self.quiz)
        self.assertFalse(form.is_valid())
        self.assertIn("text_ru", form.errors)
        form = QuizForm({"time_limit_minutes": 5, "text": UZ, "text_ru": ""}, instance=self.quiz)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(self.quiz.translated_count, 0)
        response = self.client.post(
            reverse("quiz_edit", args=[self.topic.pk]),
            {"time_limit_minutes": 5, "text": UZ, "text_ru": RU},
            follow=True,
        )
        self.assertContains(response, "ruscha tarjimasi bor: 2 ta")


class SendLanguageTests(Base):
    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_language_per_student(self, send, _):
        page = self.client.get(f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}")
        self.assertContains(page, f'name="lang_{self.ivan.pk}" value="ru"')
        self.assertContains(page, "<strong>2 / 2</strong>")
        self.client.post(
            f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}",
            {
                "students": [self.ali.pk, self.ivan.pk],
                "question_count": 2,
                "time_limit_minutes": 5,
                "channels": ["telegram"],
                f"lang_{self.ali.pk}": "uz",
                f"lang_{self.ivan.pk}": "ru",
            },
        )
        batch = QuizBatch.objects.get()
        self.assertEqual(batch.attempts.get(student=self.ivan).language, "ru")
        self.assertEqual(batch.attempts.get(student=self.ali).language, "uz")
        self.ivan.refresh_from_db()
        self.assertEqual(self.ivan.quiz_language, "ru")  # keyingi safar uchun eslab qolinadi
        texts = {i.username: i.text for i in send.call_args.args[0]}
        self.assertIn("Здравствуйте, Ivan Petrov!", texts["ivan_p"])
        self.assertIn("Тест по теме «Списки»", texts["ivan_p"])
        self.assertIn("Salom, Ali Valiyev!", texts["ali_v"])
        page = self.client.get(f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}")
        self.assertContains(page, f'name="lang_{self.ivan.pk}" value="ru" checked')

    def test_reminder_in_russian(self):
        attempt = create_quiz_batch(self.quiz, [self.ivan], 2, 5, languages={self.ivan.pk: "ru"}).attempts.get()
        self.assertIn("ещё не открыт", reminder_text(attempt, "https://x/t/1"))


class TakeInRussianTests(Base):
    def test_student_sees_russian_teacher_sees_uzbek(self):
        attempt = create_quiz_batch(self.quiz, [self.ivan], 2, 5, languages={self.ivan.pk: "ru"}).attempts.get()
        student = self.client_class()
        start = student.get(attempt.get_absolute_url())
        self.assertContains(start, '<html lang="ru"')
        self.assertContains(start, "Начать тест")
        self.assertContains(start, "Списки")
        student.post(attempt.get_absolute_url())
        take = student.get(attempt.get_absolute_url())
        self.assertContains(take, "Какой скобкой записывается список?")
        self.assertContains(take, "Завершить тест")
        self.assertNotContains(take, "qaysi qavs")
        attempt.refresh_from_db()
        answers = {}
        for q in attempt.questions().prefetch_related("choices"):
            answers[f"q{q.pk}"] = q.choices.get(is_correct=True).pk
        student.post(reverse("quiz_submit", args=[attempt.token]), answers)
        result = student.get(attempt.get_absolute_url())
        self.assertContains(result, "Правильных ответов: 2 из 2")
        self.assertContains(result, "Чему равно len")
        review = self.client.get(reverse("quiz_attempt_review", args=[attempt.pk]))
        self.assertContains(review, "qaysi qavs")
        self.assertContains(review, "rus tilida")
        self.assertContains(self.client.get(attempt.batch.get_absolute_url()), ">RU</span>")

    def test_russian_prefers_translated_questions(self):
        self.quiz.replace_questions(parse_quiz(UZ + "\n\n? Yangi savol\n+ ha\n- yo'q")[0])
        attempt = create_quiz_batch(self.quiz, [self.ivan], 2, 5, languages={self.ivan.pk: "ru"}).attempts.get()
        attempt.start("k")
        self.assertTrue(all(q.text_ru for q in attempt.questions()))

    def test_retake_keeps_language(self):
        b = create_quiz_batch(self.quiz, [self.ivan], 2, 5, languages={self.ivan.pk: "ru"})
        a = b.attempts.get()
        a.start("k")
        a.finish({})
        self.client.post(reverse("quiz_batch_retake", args=[b.pk]))
        retake = QuizAttempt.objects.exclude(batch=b).get()
        self.assertEqual(retake.language, "ru")
