from datetime import datetime, timedelta
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import telegram_sender as tg
from academy.automation import daily_report, due_reminders, send_reminders
from academy.models import Attendance, Quiz, QuizAttempt, Registration
from academy.services import (
    create_quiz_batch,
    group_journal,
    parse_quiz,
    quiz_stats,
    rating,
    student_insights,
)

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri\n- xato" for i in range(1, 5))


def finish(attempt, correct: int):
    """Testni boshlab, birinchi `correct` ta savolga to'g'ri javob bilan yakunlaydi."""
    attempt.start(f"k{attempt.pk}")
    attempt.refresh_from_db()
    answers = {}
    for i, q in enumerate(attempt.questions().prefetch_related("choices")):
        good = i < correct
        answers[str(q.pk)] = q.choices.get(is_correct=good).pk
    attempt.finish(answers)
    return attempt


class RatingFormulaTests(SimpleTestCase):
    def test_formula(self):
        self.assertEqual(rating(80, 100, 50), 75)  # 0.5·80 + 0.3·50 + 0.2·100
        self.assertEqual(rating(80, 100), 86)  # testsiz — avvalgi formula
        self.assertEqual(rating(None, 100, 50), 65)  # faqat test: 0.7·50 + 0.3·100
        self.assertEqual(rating(None, None, 64), 64)  # davomat ma'lumoti yo'q
        self.assertEqual(rating(80, None, 50), 69)  # (0.5·80 + 0.3·50) / 0.8
        self.assertIsNone(rating(None, 100))


class QuizInsightTestCase(TestCase):
    def setUp(self):
        self.group = f.group(code="S-1")
        self.good = f.student(self.group, full_name="A'lochi Bola", telegram="alochi")
        self.weak = f.student(self.group, full_name="Qiynalayotgan Bola", telegram="weak_kid")
        topic = f.topic(title="Sikllar")
        self.quiz = Quiz.objects.create(topic=topic)
        self.quiz.replace_questions(parse_quiz(TEXT)[0])

    def batch(self, students, **kw):
        return create_quiz_batch(self.quiz, students, 4, 10, **kw)


class QuizStatsTests(QuizInsightTestCase):
    def test_stats_and_journal_and_insights(self):
        for correct_good, correct_weak in ((4, 1), (3, 1), (4, 2)):
            b = self.batch([self.good, self.weak])
            finish(b.attempts.get(student=self.good), correct_good)
            finish(b.attempts.get(student=self.weak), correct_weak)
        stats = quiz_stats([self.good.pk, self.weak.pk])
        self.assertEqual((stats[self.good.pk].n, stats[self.good.pk].pct), (3, 92))
        self.assertEqual(stats[self.weak.pk].recent_pct, 33)

        lesson = f.lesson(self.group)
        Attendance.objects.create(lesson=lesson, student=self.good, status="present", score=80)
        _, rows = group_journal(self.group)
        row = next(r for r in rows if r.student == self.good)
        self.assertEqual((row.quiz.pct, row.rating), (92, rating(80, 100, 92)))

        insights = student_insights()
        self.assertIn(self.good, insights["leaders"])
        risky = {s.full_name: s.risk_reasons for s in insights["at_risk"]}
        self.assertEqual(risky, {"Qiynalayotgan Bola": ["oxirgi testlar 33%"]})

    def test_pages_show_quiz_numbers(self):
        b = self.batch([self.weak])
        finish(b.attempts.get(), 1)
        b = self.batch([self.weak])
        finish(b.attempts.get(), 1)
        self.client.force_login(f.user())
        page = self.client.get(self.weak.get_absolute_url())
        self.assertContains(page, "ball × 0.5 + test × 0.3 + davomat × 0.2")
        self.assertContains(page, "2 ta test · oxirgi 3 tasi: 25%")
        self.assertContains(page, 'class="low"')
        dash = self.client.get(reverse("dashboard"))
        self.assertContains(dash, "oxirgi testlar 25%")
        journal = self.client.get(reverse("group_journal", args=[self.group.pk]))
        self.assertContains(journal, "2 ta test")
        csv = self.client.get(reverse("group_journal", args=[self.group.pk]), {"format": "csv"})
        self.assertIn("Test %", csv.content.decode("utf-8-sig"))


NOON = timezone.make_aware(datetime(2026, 10, 16, 13, 0))  # Toshkent vaqti
NIGHT = timezone.make_aware(datetime(2026, 10, 16, 23, 30))


def ok_sender(items):
    return [tg.Result(i.key, True) for i in items]


@override_settings(SITE_URL="https://darsxona.test", QUIZ_REMINDER_AFTER_HOURS=3)
class ReminderTests(QuizInsightTestCase):
    def sent_batch(self, hours_ago=5, students=None):
        b = self.batch(students or [self.good, self.weak])
        QuizAttempt.objects.filter(batch=b).update(sent_at=NOON - timedelta(hours=hours_ago))
        type(b).objects.filter(pk=b.pk).update(created_at=NOON - timedelta(hours=hours_ago))
        return b

    def test_only_due_attempts_are_reminded_once(self):
        due = self.sent_batch(hours_ago=5)
        self.sent_batch(hours_ago=1, students=[self.good])  # hali erta
        unsent = self.batch([self.weak])  # Telegram'da yuborilmagan
        old = self.sent_batch(hours_ago=24 * 5, students=[self.good])  # juda eski
        done = self.sent_batch(hours_ago=5, students=[self.good])
        finish(done.attempts.get(), 4)

        self.assertEqual({a.batch_id for a in due_reminders(NOON)}, {due.pk})
        sender = mock.Mock(side_effect=ok_sender)
        result = send_reminders(now=NOON, sender=sender)
        self.assertEqual((result.sent, result.failed), (2, 0))
        texts = [i.text for i in sender.call_args.args[0]]
        self.assertTrue(all("https://darsxona.test/t/" in t for t in texts))
        self.assertIn("hali ochilmagan", texts[0])
        self.assertTrue(all(a.reminded_at for a in due.attempts.all()))
        self.assertFalse(unsent.attempts.get().reminded_at or old.attempts.get().reminded_at)
        # Ikkinchi marta eslatilmaydi.
        self.assertEqual(send_reminders(now=NOON, sender=sender).sent, 0)

    def test_night_and_missing_site_url(self):
        self.sent_batch()
        sender = mock.Mock(side_effect=ok_sender)
        self.assertIn("tungi", send_reminders(now=NIGHT, sender=sender).skipped)
        with override_settings(SITE_URL=""):
            self.assertIn("DARSXONA_SITE_URL", send_reminders(now=NOON, sender=sender).skipped)
        sender.assert_not_called()

    def test_failed_reminder_recorded_not_retried(self):
        b = self.sent_batch(students=[self.weak])
        result = send_reminders(now=NOON, sender=lambda items: [tg.Result(items[0].key, False, "username topilmadi")])
        self.assertEqual(result.failed, 1)
        attempt = b.attempts.get()
        self.assertIn("Eslatma: username topilmadi", attempt.send_error)
        self.assertIsNotNone(attempt.reminded_at)

    def test_command_dry_run(self):
        self.sent_batch()
        out = StringIO()
        with mock.patch("django.utils.timezone.now", return_value=NOON):
            call_command("quiz_reminders", "--dry-run", stdout=out)
        self.assertIn("2 ta", out.getvalue())


@override_settings(SITE_URL="https://darsxona.test")
class DailyReportTests(QuizInsightTestCase):
    def test_report_text(self):
        b = self.batch([self.good, self.weak])
        finish(b.attempts.get(student=self.good), 4)
        finish(b.attempts.get(student=self.weak), 1)
        self.batch([self.good])  # ochilmagan
        Registration.objects.create(full_name="Yangi Bola", phone="+998901234567", telegram="yangi")
        f.student(self.group, full_name="Kontaktsiz Bola")
        text = daily_report()
        self.assertIn("Test yechildi: 2 ta · o‘rtacha 62%", text)
        self.assertIn("• Sikllar — 2 kishi, 62%", text)
        self.assertIn("Qiynalayotgan Bola (S-1) — 25%", text)
        self.assertIn("Ochilmagan havolalar: 1 ta", text)
        self.assertIn("Tekshirilmagan arizalar: 1 ta", text)
        self.assertIn("Telegram/telefon/emaili yo‘q o‘quvchilar: 1 ta", text)
        self.assertIn("https://darsxona.test/testlar/", text)

    def test_empty_day_and_command(self):
        self.assertIn("Bugun test yechilmadi.", daily_report())
        with mock.patch("academy.telegram_sender.send_text_to_self") as send:
            call_command("daily_report", stdout=StringIO())
        self.assertIn("kun yakuni", send.call_args.args[0])
