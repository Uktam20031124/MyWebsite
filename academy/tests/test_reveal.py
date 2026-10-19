from unittest import mock

from django.test import TestCase
from django.urls import reverse

from academy.models import Quiz, QuizAttempt
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 4))


class RevealFlowTests(TestCase):
    def setUp(self):
        group = f.group()
        self.ali = f.student(group, full_name="Ali Valiyev")
        quiz = Quiz.objects.create(topic=f.topic(title="Sikllar"))
        quiz.replace_questions(parse_quiz(TEXT)[0])
        self.attempt = create_quiz_batch(quiz, [self.ali], 3, 5).attempts.get()
        self.student = self.client_class()
        url = self.attempt.get_absolute_url()
        self.student.post(url)  # boshlash (cookie)
        self.attempt.refresh_from_db()
        answers = {f"q{q.pk}": q.choices.get(is_correct=False).pk for q in self.attempt.questions()}
        self.student.post(reverse("quiz_submit", args=[self.attempt.token]), answers)
        self.url = url
        self.teacher = self.client_class()
        self.teacher.force_login(f.user())

    def test_full_flow(self):
        page = self.student.get(self.url)
        self.assertContains(page, "0 / 3 to‘g‘ri javob")
        self.assertNotContains(page, "Javobingiz")
        self.assertContains(page, "Javoblarimni ko‘rish uchun ruxsat so‘rash")

        with mock.patch("academy.review_access.notify_teacher") as notify:
            self.student.post(reverse("quiz_review_request", args=[self.attempt.token]))
            self.student.post(reverse("quiz_review_request", args=[self.attempt.token]))
        notify.assert_called_once()  # takror so'rov ustozni bezovta qilmaydi
        self.assertContains(self.student.get(self.url), "So‘rov ustozingizga yuborildi")

        dash = self.teacher.get(reverse("dashboard"))
        self.assertContains(dash, "Javoblarini ko‘rish uchun ruxsat so‘ragan")
        listing = self.teacher.get(reverse("quiz_review_requests"))
        self.assertContains(listing, "Ali Valiyev")
        batch_page = self.teacher.get(self.attempt.batch.get_absolute_url())
        self.assertContains(batch_page, "So‘rovlarga ruxsat (1)")

        self.teacher.post(reverse("quiz_review_decide", args=[self.attempt.pk]), {"action": "approve"})
        page = self.student.get(self.url)
        self.assertContains(page, "Javobingiz: <strong>xato 1</strong>")
        self.assertNotContains(page, "to'g'ri 1")  # to'g'ri variant baribir ko'rinmaydi

        # Ruxsatni qaytarib olish.
        self.teacher.post(reverse("quiz_review_decide", args=[self.attempt.pk]), {"action": "reject"})
        page = self.student.get(self.url)
        self.assertNotContains(page, "Javobingiz")
        self.assertContains(page, "ko‘rsatmaslikka qaror qildi")
        # Rad etilgandan keyin qayta so'rab bo'lmaydi.
        self.student.post(reverse("quiz_review_request", args=[self.attempt.token]))
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.reveal, QuizAttempt.Reveal.REJECTED)

    def test_only_owner_can_request(self):
        stranger = self.client_class()
        stranger.post(reverse("quiz_review_request", args=[self.attempt.token]))
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.reveal, "")

    def test_portal_request_and_approve_all(self):
        self.teacher.get(self.ali.get_absolute_url())  # portal kaliti yaratiladi
        self.ali.refresh_from_db()
        portal = reverse("student_portal", args=[self.ali.portal_token])
        with mock.patch("academy.review_access.notify_teacher"):
            self.client_class().post(
                reverse("portal_review_request", args=[self.ali.portal_token, self.attempt.pk])
            )
        self.assertContains(self.client_class().get(portal), "So‘rov yuborildi")
        self.teacher.post(reverse("quiz_review_approve_all"), {"batch": self.attempt.batch_id})
        self.assertContains(self.client_class().get(portal), "Javobingiz:")

    def test_decide_requires_login(self):
        response = self.client_class().post(
            reverse("quiz_review_decide", args=[self.attempt.pk]), {"action": "approve"}
        )
        self.assertEqual(response.status_code, 302)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.reveal, "")

    def test_next_redirect_is_safe(self):
        response = self.teacher.post(
            reverse("quiz_review_decide", args=[self.attempt.pk]),
            {"action": "approve", "next": "https://evil.example/"},
        )
        self.assertEqual(response["Location"], reverse("quiz_review_requests"))
