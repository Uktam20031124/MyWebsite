import smtplib
from datetime import timedelta
from io import StringIO
from unittest import mock

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import mailer
from academy import telegram_sender as tg
from academy.automation import send_reminders, send_scheduled
from academy.contacts import parse_contact, preview_contacts
from academy.models import Quiz, QuizBatch, Registration, RegistrationLink
from academy.registrations import approve_new, submit
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 7))


def ok_results(items, **kw):
    return [tg.Result(i.key, True) for i in items]


class MailerTests(TestCase):
    def test_sends_html_and_reports_bad_addresses(self):
        html = mailer.button_html("Sarlavha", ["Salom"], "https://x.uz/t/1", "Ochish")
        results = mailer.send_mails(
            [
                mailer.Mail(1, "ali@gmail.com", "Mavzu", "matn", html),
                mailer.Mail(2, "noto'g'ri", "Mavzu", "matn"),
            ]
        )
        self.assertEqual([(r.key, r.ok) for r in results], [(1, True), (2, False)])
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ["ali@gmail.com"])
        html, mime = msg.alternatives[0]
        self.assertEqual(mime, "text/html")
        self.assertIn('href="https://x.uz/t/1"', html)

    def test_html_is_escaped(self):
        html = mailer.button_html("<b>", ["<script>alert(1)</script>"])
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend",
        EMAIL_HOST_USER="",
        EMAIL_HOST_PASSWORD="",
    )
    def test_not_configured(self):
        self.assertFalse(mailer.is_configured())
        with self.assertRaisesMessage(mailer.MailError, "Gmail ulanmagan"):
            mailer.send_mails([mailer.Mail(1, "ali@gmail.com", "s", "t")])

    def test_bad_app_password_is_explained(self):
        with mock.patch(
            "django.core.mail.get_connection",
            side_effect=smtplib.SMTPAuthenticationError(535, b"bad"),
        ):
            with self.assertRaisesMessage(mailer.MailError, "App Password"):
                mailer.send_mails([mailer.Mail(1, "ali@gmail.com", "s", "t")])


class Base(TestCase):
    def setUp(self):
        self.group = f.group(name="S-009 · Starter", code="S-009")
        self.ali = f.student(self.group, full_name="Ali Valiyev", telegram="ali_v", email="ali@gmail.com")
        self.bek = f.student(self.group, full_name="Bek Toshev", telegram="bek_t")
        self.topic = f.topic(title="Sikllar")
        self.quiz = Quiz.objects.create(topic=self.topic)
        self.quiz.replace_questions(parse_quiz(TEXT)[0])
        self.client.force_login(f.user())

    def batch(self, students=None, channels="telegram"):
        b = create_quiz_batch(self.quiz, students or [self.ali, self.bek], 6, 10)
        QuizBatch.objects.filter(pk=b.pk).update(channels=channels)
        b.refresh_from_db()
        return b

    def post_send(self, channels, **extra):
        return self.client.post(
            f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}",
            {
                "students": [self.ali.pk, self.bek.pk],
                "question_count": 3,
                "time_limit_minutes": 5,
                "channels": channels,
                **extra,
            },
            follow=True,
        )


class QuizEmailTests(Base):
    def test_email_only(self):
        response = self.post_send(["email"])
        batch = QuizBatch.objects.get()
        self.assertEqual(batch.channels, "email")
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ["ali@gmail.com"])
        self.assertIn("Sikllar", msg.subject)
        ali = batch.attempts.get(student=self.ali)
        self.assertIn(f"http://testserver{ali.get_absolute_url()}", msg.body)
        self.assertIsNotNone(ali.email_sent_at)
        self.assertIsNone(ali.sent_at)
        self.assertContains(response, "Email orqali 1 ta shogirdga yuborildi")
        self.assertContains(response, "Emaili kiritilmagan 1 ta shogird: Bek Toshev")
        self.assertContains(response, "ali@gmail.com")

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_both_channels(self, send, _):
        self.post_send(["telegram", "email"])
        ali = QuizBatch.objects.get().attempts.get(student=self.ali)
        self.assertIsNotNone(ali.sent_at)
        self.assertIsNotNone(ali.email_sent_at)
        self.assertEqual(len(send.call_args.args[0]), 2)
        self.assertEqual(len(mail.outbox), 1)

    @mock.patch("academy.telegram_sender.is_configured", return_value=False)
    def test_unconfigured_channel_warns_other_still_sends(self, _):
        response = self.post_send(["telegram", "email"])
        self.assertContains(response, "Telegram ulanmagan — yuborilmadi")
        self.assertEqual(len(mail.outbox), 1)

    def test_no_channel_only_creates_links(self):
        self.post_send([])
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(QuizBatch.objects.exists())

    def test_schedule_requires_channel(self):
        when = (timezone.localtime() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        response = self.post_send([], scheduled_at=when)
        self.assertContains(response, "kamida bitta kanalni tanlang")
        self.assertFalse(QuizBatch.objects.exists())

    def test_batch_page_bulk_and_single_email(self):
        b = self.batch()
        page = self.client.get(b.get_absolute_url())
        self.assertContains(page, "Emailga yuborish (1)")
        url = reverse("quiz_batch_send", args=[b.pk])
        self.client.post(url, {"channel": "email"})
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(self.client.get(b.get_absolute_url()), "Email orqali yuborilgan")
        # Hammasiga qayta ketmaydi, bittasiga qayta yuborish mumkin.
        self.client.post(url, {"channel": "email"})
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(url, {"channel": "email", "attempt": b.attempts.get(student=self.ali).pk})
        self.assertEqual(len(mail.outbox), 2)

    def test_gmail_failure_shown(self):
        b = self.batch()
        error = mailer.MailError("Gmail login yoki App Password noto‘g‘ri")
        with mock.patch("academy.mailer.send_mails", side_effect=error):
            response = self.client.post(reverse("quiz_batch_send", args=[b.pk]), {"channel": "email"}, follow=True)
        self.assertContains(response, "App Password")
        self.assertIsNone(b.attempts.get(student=self.ali).email_sent_at)

    def test_retake_uses_original_channels(self):
        from .test_quiz_plus import finish

        b = self.batch([self.ali], channels="email")
        finish(b.attempts.get(), 1)
        self.client.post(reverse("quiz_batch_retake", args=[b.pk]))
        retake = QuizBatch.objects.exclude(pk=b.pk).get()
        self.assertEqual(retake.channels, "email")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(retake.attempts.get().email_sent_at)


@override_settings(SITE_URL="https://darsxona.test", QUIZ_REMINDER_AFTER_HOURS=3)
class EmailAutomationTests(Base):
    def test_scheduled_email(self):
        b = self.batch(channels="email")
        QuizBatch.objects.filter(pk=b.pk).update(scheduled_at=timezone.now() + timedelta(hours=1))
        self.assertEqual(send_scheduled(now=timezone.now()).sent, 0)
        result = send_scheduled(now=timezone.now() + timedelta(hours=2))
        self.assertEqual(result.sent, 1)
        self.assertIn("https://darsxona.test/t/", mail.outbox[0].body)
        b.refresh_from_db()
        self.assertIsNotNone(b.scheduled_sent_at)

    def test_scheduled_channel_down_is_retried(self):
        b = self.batch(channels="email")
        QuizBatch.objects.filter(pk=b.pk).update(scheduled_at=timezone.now() - timedelta(minutes=1))
        down = mock.Mock(side_effect=mailer.MailError("ulanib bo‘lmadi"))
        result = send_scheduled(mail_sender=down)
        self.assertTrue(result.errors)
        b.refresh_from_db()
        self.assertIsNone(b.scheduled_sent_at)
        self.assertEqual(send_scheduled().sent, 1)
        out = StringIO()
        call_command("send_scheduled", stdout=out)  # endi hech narsa qolmagan
        self.assertEqual(out.getvalue(), "")

    def test_reminder_goes_to_email_channel(self):
        b = self.batch()
        ali = b.attempts.get(student=self.ali)
        # Vaqtlar bitta nuqtadan: test kunning istalgan soatida bir xil ishlasin.
        noon = timezone.localtime().replace(hour=13, minute=0, second=0, microsecond=0)
        type(ali).objects.filter(pk=ali.pk).update(email_sent_at=noon - timedelta(hours=5))
        sender = mock.Mock(side_effect=ok_results)
        result = send_reminders(now=noon, sender=sender)
        self.assertEqual(result.sent, 1)
        sender.assert_not_called()  # Telegram'ga yuborilmagan — Telegram eslatmasi yo'q
        self.assertIn("Eslatma", mail.outbox[0].subject)
        ali.refresh_from_db()
        self.assertIsNotNone(ali.reminded_at)

    def test_reminder_channel_down_is_not_marked(self):
        b = self.batch([self.ali])
        ali = b.attempts.get()
        # Vaqtlar bitta nuqtadan: test kunning istalgan soatida bir xil ishlasin.
        noon = timezone.localtime().replace(hour=13, minute=0, second=0, microsecond=0)
        type(ali).objects.filter(pk=ali.pk).update(email_sent_at=noon - timedelta(hours=5))
        result = send_reminders(now=noon, mail_sender=mock.Mock(side_effect=mailer.MailError("x")))
        self.assertEqual(result.errors, ["Email: x"])
        ali.refresh_from_db()
        self.assertIsNone(ali.reminded_at)

    @override_settings(REPORT_EMAIL="ustoz@gmail.com")
    def test_daily_report_by_email(self):
        with mock.patch("academy.telegram_sender.is_configured", return_value=False):
            out = StringIO()
            call_command("daily_report", stdout=out)
        self.assertIn("email", out.getvalue())
        self.assertEqual(mail.outbox[0].to, ["ustoz@gmail.com"])
        self.assertIn("kun yakuni", mail.outbox[0].subject)


class StudentEmailTests(Base):
    def test_portal_and_certificate_by_email(self):
        page = self.client.get(self.ali.get_absolute_url())
        self.assertContains(page, "Emailga yuborish")
        self.client.post(reverse("student_portal_action", args=[self.ali.pk]), {"channel": "email"})
        self.assertIn("/men/", mail.outbox[0].body)
        response = self.client.post(
            reverse("student_certificate_send", args=[self.ali.pk]),
            {"channel": "email", "kurs": "Python asoslari"},
            follow=True,
        )
        self.assertContains(response, "email orqali yuborildi")
        name, content, mime = mail.outbox[1].attachments[0]
        self.assertEqual(mime, "application/pdf")
        self.assertTrue(content.startswith(b"%PDF"))
        self.assertNotContains(self.client.get(self.bek.get_absolute_url()), "Emailga yuborish")

    def test_group_portal_email_only_to_students_with_email(self):
        self.client.post(reverse("group_portal_send", args=[self.group.pk]), {"channel": "email"})
        self.assertEqual([m.to for m in mail.outbox], [["ali@gmail.com"]])

    def test_student_form_saves_email(self):
        data = {
            "group": self.group.pk,
            "full_name": "Bek Toshev",
            "phone": "",
            "telegram": "bek_t",
            "email": " Bek@Gmail.com ",
            "status": "active",
            "joined_at": "2026-09-01",
            "notes": "",
        }
        self.client.post(reverse("student_update", args=[self.bek.pk]), data)
        self.bek.refresh_from_db()
        self.assertEqual(self.bek.email, "bek@gmail.com")


class ContactEmailTests(Base):
    def test_parse_email_not_taken_as_username(self):
        self.assertEqual(
            parse_contact("Ali Valiyev — ali.v@Gmail.com — +998 90 123 45 67"),
            ("Ali Valiyev", "", "+998901234567", "ali.v@gmail.com"),
        )
        self.assertEqual(parse_contact("Bek @bek_t bek@mail.ru")[1:], ("bek_t", "", "bek@mail.ru"))

    def test_preview_updates_email(self):
        rows = preview_contacts("Bek Toshev bek@gmail.com", [self.ali, self.bek])
        self.assertEqual(rows[0].changes, {"email": ("", "bek@gmail.com")})

    def test_registration_email_copied_on_approve(self):
        link = RegistrationLink.objects.create(title="Yangi guruh", group=self.group)
        reg, _ = submit(link, "Sardor Aliyev", "+998901112233", "sardor_a", email="sardor@gmail.com")
        self.assertEqual(Registration.objects.get().email, "sardor@gmail.com")
        student = approve_new(reg, self.group)
        self.assertEqual(student.email, "sardor@gmail.com")
