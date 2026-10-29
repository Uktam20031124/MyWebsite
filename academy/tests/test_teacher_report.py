from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import teacher_report as report
from academy import teachers
from academy.models import Attendance, Group, Lesson, Quiz, TeacherPayout
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 5))


class TeacherReportTests(TestCase):
    def setUp(self):
        self.admin = f.user(username="ustoz", is_superuser=True)
        self.malika = f.user(username="malika", first_name="Malika")
        account = teachers.account_of(self.malika)
        account.lesson_rate, account.monthly_fixed = 50_000, 200_000
        account.save()
        self.group = f.group(code="M-1")
        Group.objects.filter(pk=self.group.pk).update(teacher=self.malika)
        self.group.refresh_from_db()
        self.ali = f.student(self.group, full_name="Ali")
        self.month = timezone.localdate().replace(day=1)

    def lesson(self, day, status=Lesson.Status.COMPLETED, group=None):
        return f.lesson(group or self.group, days=0, held_on=day, status=status)

    def test_lessons_follow_the_teacher_who_taught_them(self):
        done = self.lesson(self.month)
        self.assertEqual(done.teacher, self.malika)  # guruh o'qituvchisidan
        self.lesson(self.month, Lesson.Status.CANCELLED)
        self.lesson(self.month - timedelta(days=1))  # o'tgan oy
        Attendance.objects.create(lesson=done, student=self.ali, status=Attendance.Status.PRESENT)
        # Guruh boshqa o'qituvchiga o'tsa ham, o'tilgan dars Malikaniki qoladi.
        other = f.user(username="boshqa")
        Group.objects.filter(pk=self.group.pk).update(teacher=other)
        row = report.teacher_row(self.malika.teacher_account, self.month)
        self.assertEqual((row.lessons, row.cancelled), (1, 1))
        self.assertEqual(row.attendance, 100)
        self.assertEqual(row.salary, 1 * 50_000 + 200_000)

    def test_tests_and_results(self):
        quiz = Quiz.objects.create(topic=f.topic())
        quiz.replace_questions(parse_quiz(TEXT)[0])
        batch = create_quiz_batch(quiz, [self.ali], 4, 5)
        batch.sent_by = self.malika
        batch.save()
        attempt = batch.attempts.get()
        attempt.start("k")
        attempt.refresh_from_db()
        attempt.finish({str(q.pk): q.choices.get(is_correct=i < 3).pk for i, q in enumerate(attempt.questions())})
        row = report.teacher_row(self.malika.teacher_account, self.month)
        self.assertEqual((row.tests, row.results, row.avg_percent), (1, 1, 75))

    def test_admin_page_csv_and_payout(self):
        self.lesson(self.month)
        self.client.force_login(self.admin)
        page = self.client.get(reverse("teacher_report"))
        self.assertContains(page, "Malika")
        self.assertContains(page, "250 000")
        csv = self.client.get(reverse("teacher_report"), {"csv": "1"}).content.decode("utf-8-sig")
        self.assertIn("malika", csv)
        self.assertIn("250000", csv)

        url = reverse("teacher_payout", args=[self.malika.pk])
        self.client.post(url, {"oy": f"{self.month:%Y-%m}", "action": "pay"})
        payout = TeacherPayout.objects.get()
        self.assertEqual((payout.month, payout.lessons, payout.amount), (self.month, 1, 250_000))
        self.client.post(url, {"oy": f"{self.month:%Y-%m}", "action": "undo"})
        self.assertFalse(TeacherPayout.objects.exists())

    def test_teacher_sees_own_month_but_not_report(self):
        self.lesson(self.month)
        account = self.malika.teacher_account
        account.telegram_id, account.linked_at = 1, timezone.now()
        account.save()
        self.client.force_login(self.malika)
        home = self.client.get(reverse("teacher_home"))
        self.assertContains(home, "Bu oy")
        self.assertContains(home, "250 000")
        self.assertRedirects(self.client.get(reverse("teacher_report")), reverse("teacher_home"))
        self.assertEqual(self.client.post(reverse("teacher_payout", args=[self.malika.pk])).status_code, 302)
        self.assertFalse(TeacherPayout.objects.exists())

    def test_month_helpers(self):
        self.assertEqual(report.month_start("2026-02"), date(2026, 2, 1))
        self.assertEqual(report.month_start("yomon", today=date(2026, 5, 9)), date(2026, 5, 1))
        self.assertEqual(report.next_month(date(2026, 12, 1)), date(2027, 1, 1))
        self.assertEqual(report.prev_month(date(2026, 1, 1)), date(2025, 12, 1))
