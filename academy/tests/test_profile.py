from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import coins, profiles
from academy.models import QuizAttempt, StudySession, SyllabusItem, TestRequest
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

    def start(self, topic, questions="10", minutes="10"):
        """Testni boshlash → tanlash → yakunlash; QuizAttempt qaytaradi."""
        self.ask(topic)
        req = TestRequest.objects.filter(status=TestRequest.Status.APPROVED).latest("pk")
        url = reverse("portal_test_start", args=[self.token, req.pk])
        self.client.post(url, {"questions": questions, "minutes": minutes})
        req.refresh_from_db()
        return req.attempt

    def solve(self, attempt, correct=True):
        attempt.start("k")
        attempt.refresh_from_db()
        answers = {str(q.pk): q.choices.get(is_correct=correct).pk for q in attempt.questions()}
        attempt.finish(answers)
        attempt.refresh_from_db()
        return attempt

    def test_full_test_flow_without_approval(self, notify):
        self.grant()
        self.allow(self.topic)
        page = self.client.get(self.portal)
        self.assertContains(page, "Sikllar")
        self.assertContains(page, "Testni boshlash")
        self.assertNotContains(page, "Funksiyalar")
        self.assertContains(self.ask(self.other), "ruxsat berilmagan")
        response = self.ask(self.topic)  # ustoz ruxsatisiz → darhol tanlash sahifasi
        self.assertContains(response, "12 ta savol")
        self.assertContains(response, "5 daqiqa")
        req = TestRequest.objects.get()
        self.assertEqual((req.status, req.kind), (TestRequest.Status.APPROVED, TestRequest.Kind.FIRST))
        start_url = reverse("portal_test_start", args=[self.token, req.pk])
        self.assertEqual(self.client.post(start_url, {"questions": "7", "minutes": "10"}).status_code, 422)
        # Qayta bosish yangi so'rov ochmaydi — o'sha tanlash sahifasi.
        self.ask(self.topic)
        self.assertEqual(TestRequest.objects.count(), 1)
        response = self.client.post(start_url, {"questions": "12", "minutes": "5"})
        attempt = QuizAttempt.objects.get()
        self.assertRedirects(response, attempt.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual((attempt.batch.question_count, attempt.batch.time_limit_minutes), (12, 5))
        self.assertTrue(attempt.batch.from_profile)
        self.assertContains(self.client.get(attempt.get_absolute_url()), "Testni boshlash")
        notify.assert_not_called()  # test uchun ustozga so'rov ketmaydi

    def test_daily_limit_two_per_topic(self, notify):
        self.grant()
        self.allow(self.topic)
        for _ in range(2):
            self.solve(self.start(self.topic))
        self.assertContains(self.ask(self.topic), "Bugun bu mavzudan 2 ta test")
        self.assertContains(self.client.get(self.portal), "bugungi limit tugadi")
        TestRequest.objects.update(created_at=timezone.now() - timedelta(days=1))
        self.assertContains(self.ask(self.topic), "12 ta savol")

    def test_low_result_opens_review_and_retake_after_20_minutes(self, notify):
        self.grant()
        self.allow(self.topic)
        first = self.solve(self.start(self.topic), correct=False)  # 0%
        self.assertEqual(coins.balance(self.ali), 1)
        page = self.client.get(self.portal)
        study_url = reverse("portal_study", args=[self.token, self.topic.pk])
        self.assertContains(page, study_url)
        self.assertContains(page, "📘 Mustahkamlash")
        self.assertNotContains(page, ">Qayta topshirish</button>")
        self.assertContains(self.ask(self.topic), "Avval materialni oching")

        study = self.client.get(study_url)  # mustahkamlash o'zi boshlanadi (so'rovsiz)
        self.assertContains(study, "<h3>Sikl nima?</h3>")
        self.assertContains(study, "Mustahkamlash vaqti: 20 daqiqa")
        self.assertContains(study, "data-countdown")
        session = StudySession.objects.get()
        self.assertEqual(session.kind, StudySession.Kind.REVIEW)
        self.client.get(study_url)
        self.assertEqual(StudySession.objects.count(), 1)  # qayta ochish vaqtni yangilamaydi
        self.assertContains(self.ask(self.topic), "da tugaydi")

        # 21 daqiqa o'tdi (past natija esa undan oldin olingan).
        QuizAttempt.objects.filter(pk=first.pk).update(finished_at=timezone.now() - timedelta(minutes=30))
        StudySession.objects.update(started_at=timezone.now() - timedelta(minutes=21))
        self.assertContains(self.client.get(study_url), "Vaqt tugadi")
        retake = self.solve(self.start(self.topic))  # 100%
        self.assertEqual(retake.test_request.kind, TestRequest.Kind.RETAKE)
        self.assertEqual(coins.balance(self.ali), 1 + 10 + 3)
        # O'tdi — mustahkamlash yopildi, oddiy test.
        self.assertContains(self.client.get(self.portal), "oxirgi natija: <strong>100%</strong>")
        self.assertNotEqual(first.pk, retake.pk)

    def test_next_topic_preview_after_30_minutes(self, notify):
        SyllabusItem.objects.create(group=self.group, topic=self.topic, order=1, status=SyllabusItem.Status.TAUGHT)
        SyllabusItem.objects.create(group=self.group, topic=self.other, order=2)
        self.grant()
        self.allow(self.topic)  # yangi mavzu ruxsatsiz ham ko'rinadi
        page = self.client.get(self.portal)
        self.assertContains(page, "✨ yangi mavzu")
        self.assertContains(page, "Funksiyalar")
        self.assertContains(self.ask(self.other), "Avval materialni oching")
        study_url = reverse("portal_study", args=[self.token, self.other.pk])
        self.assertContains(self.client.get(study_url), "Tayyorlanish vaqti: 30 daqiqa")
        StudySession.objects.update(started_at=timezone.now() - timedelta(minutes=29))
        self.assertContains(self.ask(self.other), "da tugaydi")
        StudySession.objects.update(started_at=timezone.now() - timedelta(minutes=31))
        attempt = self.solve(self.start(self.other))
        self.assertEqual(attempt.test_request.kind, TestRequest.Kind.PREVIEW)
        self.assertEqual(coins.balance(self.ali), 10 + 5)
        card = self.teacher.get(self.ali.get_absolute_url())
        self.assertContains(card, "Coinlar: 15")
        self.assertContains(card, "Yangi mavzuni oldindan o‘zlashtirdi")

    def test_russian_material(self, notify):
        self.ali.quiz_language = "ru"
        self.ali.save()
        self.topic.study_ru = "## Что такое цикл?\nПовторение."
        self.topic.save()
        self.grant()
        self.allow(self.topic)
        page = self.client.get(reverse("portal_study", args=[self.token, self.topic.pk]))
        self.assertContains(page, "<h3>Что такое цикл?</h3>")
        self.assertNotContains(page, "Sikl nima?")

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


class CoinTests(TestCase):
    def test_every_finished_test_gets_coins_once(self):
        from academy.models import Quiz
        from academy.services import create_quiz_batch

        group = f.group()
        ali = f.student(group)
        quiz = Quiz.objects.create(topic=f.topic())
        quiz.replace_questions(parse_quiz(TEXT)[0])
        attempt = create_quiz_batch(quiz, [ali], 10, 5).attempts.get()  # ustoz yuborgan test
        attempt.start("k")
        attempt.refresh_from_db()
        qs = list(attempt.questions())
        answers = {str(q.pk): q.choices.get(is_correct=i < 8).pk for i, q in enumerate(qs)}
        attempt.finish(answers)  # 80%
        attempt.finish(answers)
        self.assertEqual(coins.balance(ali), 7)
        self.assertEqual(ali.coins.count(), 1)
        self.assertEqual([coins.score_coins(p) for p in (95, 80, 60, 59)], [10, 7, 5, 1])
