from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import profiles
from academy.models import QuizAttempt, SyllabusItem, TestRequest
from academy.services import parse_quiz
from academy.templatetags.ui import study_md

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 15))


@mock.patch("academy.profiles.notify")
class ProfileFlowTests(TestCase):
    def setUp(self):
        self.group = f.group(code="P-1")
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        study = "## Sikl nima?\nTakrorlash **muhim**.\n```\nfor i in range(3):\n    print(i)\n```"
        self.topic = f.topic(title="Sikllar", study=study)
        self.other = f.topic(title="Funksiyalar")
        for t in (self.topic, self.other):
            quiz = t.quiz if hasattr(t, "quiz") else None
            if quiz is None:
                from academy.models import Quiz

                quiz = Quiz.objects.create(topic=t)
            quiz.replace_questions(parse_quiz(TEXT)[0])
        self.teacher = self.client_class()
        self.teacher.force_login(f.user())
        self.teacher.get(self.ali.get_absolute_url())  # portal kaliti yaratiladi
        self.ali.refresh_from_db()
        self.token = self.ali.portal_token
        self.portal = reverse("student_portal", args=[self.token])

    def grant(self, hours=2):
        url = reverse("student_profile_access", args=[self.ali.pk])
        self.teacher.post(url, {"action": str(hours)})
        self.ali.refresh_from_db()

    def allow(self, *topics):
        self.teacher.post(
            reverse("student_allowed_topics", args=[self.ali.pk]), {"topics": [t.pk for t in topics]}
        )

    def ask(self, topic, kind=""):
        url = reverse("portal_test_request", args=[self.token, topic.pk])
        return self.client.post(url, {"kind": kind}, follow=True)

    def test_locked_until_teacher_grants_hours(self, notify):
        page = self.client.get(self.portal)
        self.assertContains(page, "Ali Valiyev")
        self.assertContains(page, "Profilga kirish uchun ruxsat so‘rash")
        self.assertNotContains(page, "Test topshirish")
        self.client.post(reverse("portal_access_request", args=[self.token]))
        self.client.post(reverse("portal_access_request", args=[self.token]))
        notify.assert_called_once()
        self.assertContains(self.client.get(self.portal), "So‘rov ustozingizga yuborildi")
        requests_page = self.teacher.get(reverse("quiz_review_requests"))
        self.assertContains(requests_page, "Profilga kirish so‘rovlari")
        self.assertContains(requests_page, "3 soat")

        self.grant(3)
        self.assertIsNone(self.ali.profile_requested_at)
        left = self.ali.profile_until - timezone.now()
        self.assertTrue(timedelta(hours=2, minutes=59) < left <= timedelta(hours=3))
        page = self.client.get(self.portal)
        self.assertContains(page, "Test topshirish")
        self.assertContains(page, "Hozircha ustozingiz test uchun mavzu belgilamagan")

        # Vaqt tugadi — profil yana yopiq.
        type(self.ali).objects.filter(pk=self.ali.pk).update(profile_until=timezone.now() - timedelta(seconds=1))
        self.assertContains(self.client.get(self.portal), "ruxsat so‘rash")

    def test_wrong_hours_rejected(self, notify):
        self.teacher.post(reverse("student_profile_access", args=[self.ali.pk]), {"action": "24"})
        self.ali.refresh_from_db()
        self.assertIsNone(self.ali.profile_until)

    def test_full_test_flow(self, notify):
        self.grant()
        self.allow(self.topic)
        page = self.client.get(self.portal)
        self.assertContains(page, "Sikllar")
        self.assertNotContains(page, "Funksiyalar")
        # Ruxsat etilmagan mavzu.
        self.assertContains(self.ask(self.other), "ruxsat berilmagan")
        response = self.ask(self.topic)
        self.assertContains(response, "So‘rov ustozga yuborildi")
        self.assertContains(self.ask(self.topic), "allaqachon bor")
        req = TestRequest.objects.get()
        self.assertEqual(req.status, TestRequest.Status.PENDING)
        start_url = reverse("portal_test_start", args=[self.token, req.pk])
        back = f"{self.portal}#t{self.topic.pk}"
        self.assertRedirects(self.client.get(start_url), back, fetch_redirect_response=False)

        self.teacher.post(reverse("test_request_decide", args=[req.pk]), {"action": "approve"})
        self.assertContains(self.client.get(self.portal), start_url)
        page = self.client.get(start_url)
        self.assertContains(page, "12 ta savol")
        self.assertContains(page, "5 daqiqa")
        self.assertEqual(self.client.post(start_url, {"questions": "7", "minutes": "10"}).status_code, 422)
        response = self.client.post(start_url, {"questions": "12", "minutes": "5"})
        attempt = QuizAttempt.objects.get()
        self.assertRedirects(response, attempt.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual((attempt.batch.question_count, attempt.batch.time_limit_minutes), (12, 5))
        self.assertTrue(attempt.batch.from_profile)
        req.refresh_from_db()
        self.assertEqual((req.status, req.attempt), (TestRequest.Status.USED, attempt))
        # Qayta bosish — yangi test yaratilmaydi, o'sha testga olib boradi.
        self.client.post(start_url, {"questions": "10", "minutes": "10"})
        self.assertEqual(QuizAttempt.objects.count(), 1)
        self.assertContains(self.client.get(attempt.get_absolute_url()), "Testni boshlash")

    def test_daily_limit_two_per_topic(self, notify):
        self.grant()
        self.allow(self.topic)
        self.ask(self.topic)
        req = TestRequest.objects.get()
        profiles.decide_test(req, False)  # rad etilgani hisoblanmaydi
        for _ in range(2):
            self.ask(self.topic)
            r = TestRequest.objects.filter(status=TestRequest.Status.PENDING).get()
            profiles.decide_test(r, True)
            profiles.start_test(r, 10, 10)
        self.assertContains(self.ask(self.topic), "Bugun bu mavzudan 2 ta test")
        self.assertContains(self.client.get(self.portal), "bugungi limit tugadi")
        # Ertasiga yana mumkin.
        TestRequest.objects.update(created_at=timezone.now() - timedelta(days=1))
        self.assertContains(self.ask(self.topic), "So‘rov ustozga yuborildi")

    def test_low_result_shows_study_and_retake(self, notify):
        self.grant()
        self.allow(self.topic)
        self.ask(self.topic)
        req = TestRequest.objects.get()
        profiles.decide_test(req, True)
        attempt = profiles.start_test(req, 10, 10)
        attempt.start("k")
        attempt.finish({})  # 0%
        page = self.client.get(self.portal)
        study_url = reverse("portal_study", args=[self.token, self.topic.pk])
        self.assertContains(page, study_url)
        self.assertContains(page, "avval mavzuni takrorlang")
        study = self.client.get(study_url)
        self.assertContains(study, "<h3>Sikl nima?</h3>")
        self.assertContains(study, "<strong>muhim</strong>")
        self.assertContains(study, "Mustahkamladim")
        self.client.post(reverse("portal_test_request", args=[self.token, self.topic.pk]), {"kind": "retake"})
        retake = TestRequest.objects.exclude(pk=req.pk).get()
        self.assertEqual(retake.kind, TestRequest.Kind.RETAKE)
        self.assertContains(self.teacher.get(reverse("quiz_review_requests")), "qayta topshirish")
        # Ruxsat etilmagan mavzuning materiali ochilmaydi.
        self.assertEqual(self.client.get(reverse("portal_study", args=[self.token, self.other.pk])).status_code, 404)

    def test_teacher_adds_taught_topics(self, notify):
        SyllabusItem.objects.create(group=self.group, topic=self.other, status=SyllabusItem.Status.TAUGHT)
        page = self.teacher.get(self.ali.get_absolute_url())
        self.assertContains(page, "O‘tilgan mavzularni qo‘shish (1)")
        self.teacher.post(reverse("student_allowed_topics", args=[self.ali.pk]), {"action": "taught"})
        self.assertEqual(list(self.ali.allowed_topics.all()), [self.other])

    def test_teacher_endpoints_require_login(self, notify):
        anon = self.client_class()
        anon.post(reverse("student_profile_access", args=[self.ali.pk]), {"action": "4"})
        self.ali.refresh_from_db()
        self.assertIsNone(self.ali.profile_until)


class StudyMarkdownTests(TestCase):
    def test_escapes_html_and_renders_blocks(self):
        html = study_md("## T\n<script>x</script> `a<b>`\n- bir\n1. ikki\n> eslatma\n```\n<i>\n```")
        self.assertIn("<h3>T</h3>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("<code>a&lt;b&gt;</code>", html)
        self.assertIn("<ul><li>bir</li></ul><ol><li>ikki</li></ol>", html)
        self.assertIn('<div class="study-note">eslatma</div>', html)
        self.assertIn("<code>&lt;i&gt;</code></pre>", html)
