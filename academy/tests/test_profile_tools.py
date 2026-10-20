from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from academy import motivation, profiles
from academy.middleware import PORTAL_LANG_COOKIE
from academy.models import Quiz, QuizAttempt, Student
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 4))


class PortalLanguageTests(TestCase):
    def setUp(self):
        group = f.group()
        self.ali = f.student(group, full_name="Ali Valiyev")
        self.vali = f.student(group, full_name="Vali Aliyev")
        for s in (self.ali, self.vali):
            motivation.portal_url(s)
            profiles.grant_access(s, 2)
            s.refresh_from_db()

    def portal(self, s):
        return reverse("student_portal", args=[s.portal_token])

    def test_switch_is_scoped_to_one_profile(self):
        response = self.client.post(
            reverse("portal_language", args=[self.ali.portal_token]),
            {"language": "ru", "next": self.portal(self.ali)},
        )
        self.assertRedirects(response, self.portal(self.ali), fetch_redirect_response=False)
        cookie = response.cookies[PORTAL_LANG_COOKIE]
        self.assertEqual((cookie.value, cookie["path"]), ("ru", self.portal(self.ali)))
        self.assertNotIn("django_language", response.cookies)  # sayt (ustoz) tili o'zgarmaydi
        self.assertContains(self.client.get(self.portal(self.ali)), 'lang="ru"')

    def test_site_language_does_not_leak_into_profile(self):
        self.client.cookies["django_language"] = "ru"  # ustoz shu brauzerda rus tilini tanlagan
        page = self.client.get(self.portal(self.vali))
        self.assertContains(page, 'lang="uz"')  # profil — o'quvchining o'z tilida
        self.assertContains(page, reverse("portal_language", args=[self.vali.portal_token]))

    def test_next_outside_profile_is_ignored(self):
        response = self.client.post(
            reverse("portal_language", args=[self.ali.portal_token]),
            {"language": "ru", "next": "https://evil.example/"},
        )
        self.assertRedirects(response, self.portal(self.ali), fetch_redirect_response=False)


class InTestLanguageSwitchTests(TestCase):
    def setUp(self):
        student = f.student(full_name="Ali Valiyev")
        quiz = Quiz.objects.create(topic=f.topic(title="Sikllar"))
        quiz.replace_questions(parse_quiz(TEXT)[0])
        self.attempt = create_quiz_batch(quiz, [student], 3, 5).attempts.get()
        self.client.post(self.attempt.get_absolute_url())  # boshlash (cookie)
        self.attempt.refresh_from_db()

    def test_switch_keeps_answers_and_is_not_a_leave(self):
        q = self.attempt.questions().first()
        picked = q.choices.get(is_correct=True).pk
        page = self.client.get(self.attempt.get_absolute_url())
        self.assertContains(page, reverse("quiz_language", args=[self.attempt.token]))
        self.assertContains(page, "data-quiz-lang")
        response = self.client.post(
            reverse("quiz_language", args=[self.attempt.token]),
            {"language": "ru", f"q{q.pk}": picked, "leave_count": "0", "away_seconds": "0"},
        )
        self.assertRedirects(response, self.attempt.get_absolute_url(), fetch_redirect_response=False)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.language, "ru")
        self.assertEqual(self.attempt.answers, {str(q.pk): picked})
        self.assertEqual(self.attempt.leave_count, 0)
        self.assertEqual(self.attempt.status, QuizAttempt.Status.ACTIVE)
        self.assertContains(self.client.get(self.attempt.get_absolute_url()), "Завершить тест")

    def test_stranger_cannot_switch(self):
        Client().post(reverse("quiz_language", args=[self.attempt.token]), {"language": "ru"})
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.language, "uz")


class PreviewTests(TestCase):
    def test_preview_is_given_once_then_request(self):
        student = f.student()
        quiz = Quiz.objects.create(topic=f.topic())
        quiz.replace_questions(parse_quiz(TEXT)[0])
        attempt = create_quiz_batch(quiz, [student], 3, 5).attempts.get()
        attempt.finish({})
        self.assertEqual(attempt.ask_reveal(), "preview")
        self.assertTrue(attempt.can_see_answers)
        self.assertEqual(attempt.ask_reveal(), "")  # 1 daqiqa ichida — o'zgarmaydi
        QuizAttempt.objects.filter(pk=attempt.pk).update(reveal_until=timezone.now() - timedelta(seconds=1))
        attempt.refresh_from_db()
        self.assertFalse(attempt.can_see_answers)
        self.assertEqual(attempt.ask_reveal(), "requested")
        self.assertEqual(attempt.ask_reveal(), "")


class StudentListProfileMenuTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.ali = f.student(full_name="Ali Valiyev", telegram="ali_v", email="ali@gmail.com")
        self.list_url = reverse("student_list")

    def test_menu_shows_status_and_actions(self):
        page = self.client.get(self.list_url)
        self.assertContains(page, f'popovertarget="pm-{self.ali.pk}"')
        self.assertContains(page, "Profilga kirish")
        self.assertContains(page, "Telegram’da yuborish")
        self.assertContains(page, "Emailga yuborish")
        self.assertContains(page, "2 soatga ochish")
        self.assertContains(page, "yopiq")
        self.assertNotContains(page, "Profilni o‘chirib qo‘yish")
        self.ali.portal_token = ""
        self.ali.save()
        self.client.get(self.list_url)
        self.ali.refresh_from_db()
        self.assertEqual(self.ali.portal_token, "")  # ro'yxat bazaga yozmaydi

    def test_open_creates_token_and_redirects_to_profile(self):
        response = self.client.get(reverse("student_portal_open", args=[self.ali.pk]))
        self.ali.refresh_from_db()
        self.assertRedirects(
            response, reverse("student_portal", args=[self.ali.portal_token]), fetch_redirect_response=False
        )

    def test_activate_and_close_return_to_list(self):
        back = f"{self.list_url}?group={self.ali.group_id}"
        url = reverse("student_profile_access", args=[self.ali.pk])
        self.assertRedirects(self.client.post(url, {"action": "3", "next": back}), back, fetch_redirect_response=False)
        self.ali.refresh_from_db()
        self.assertTrue(self.ali.profile_is_open())
        self.assertContains(self.client.get(self.list_url), "Profilni o‘chirib qo‘yish")
        self.client.post(url, {"action": "close", "next": back})
        self.ali.refresh_from_db()
        self.assertFalse(self.ali.profile_is_open())

    def test_unsafe_next_falls_back_to_student_page(self):
        response = self.client.post(
            reverse("student_profile_access", args=[self.ali.pk]), {"action": "2", "next": "//evil.example/x"}
        )
        self.assertEqual(response["Location"], f"{self.ali.get_absolute_url()}#profile")

    def test_requires_login(self):
        self.assertEqual(Client().get(reverse("student_portal_open", args=[self.ali.pk])).status_code, 302)
        self.assertEqual(Student.objects.get(pk=self.ali.pk).portal_token, self.ali.portal_token)
