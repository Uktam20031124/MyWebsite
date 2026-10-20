from datetime import timedelta

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from academy.forms import parse_emails
from academy.models import OpenAttempt, OpenQuiz, OpenQuizInvite, Quiz, name_key
from academy.services import parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 7))


class OpenQuizTestCase(TestCase):
    def setUp(self):
        self.topic = f.topic(title="Sikllar", title_ru="Циклы")
        self.quiz = Quiz.objects.create(topic=self.topic)
        self.quiz.replace_questions(parse_quiz(TEXT)[0])
        self.oq = OpenQuiz.objects.create(quiz=self.quiz, question_count=4, time_limit_minutes=10)
        self.public = reverse("open_quiz_public", args=[self.oq.token])

    def begin(self, client, name="Aliyev Vali Karimovich", **extra):
        return client.post(self.public, {"full_name": name, **extra})

    def answer_all_correct(self, client, attempt):
        data = {}
        for q in attempt.questions().prefetch_related("choices"):
            data[f"q{q.pk}"] = next(c.pk for c in q.choices.all() if c.is_correct)
        return client.post(reverse("open_quiz_submit", args=[self.oq.token, attempt.token]), data)


class ParticipantFlowTests(OpenQuizTestCase):
    def test_landing_asks_for_full_name_and_creates_nothing(self):
        response = self.client.get(self.public)
        self.assertContains(response, "familiya, ism va sharifingizni kiriting")
        self.assertContains(response, 'name="full_name"')
        self.assertContains(response, "4 ta savol")
        self.assertEqual(OpenAttempt.objects.count(), 0)
        self.assertEqual(response["X-Robots-Tag"], "noindex, nofollow")

    def test_full_name_must_have_at_least_two_words(self):
        for bad in ["", "Vali", "Vali 123", "<script> alert"]:
            response = self.begin(self.client, bad)
            self.assertEqual(response.status_code, 400, bad)
            self.assertContains(response, "F.I.Sh.ni to‘liq kiriting", status_code=400)
        self.assertEqual(OpenAttempt.objects.count(), 0)

    def test_start_take_submit_shows_score_without_answers(self):
        response = self.begin(self.client, "  Aliyev   Vali  ")
        attempt = OpenAttempt.objects.get()
        self.assertRedirects(response, attempt.get_absolute_url())
        self.assertEqual(attempt.full_name, "Aliyev Vali")
        self.assertEqual(len(attempt.question_ids), 4)
        self.assertEqual(attempt.status, OpenAttempt.Status.ACTIVE)

        page = self.client.get(attempt.get_absolute_url())
        self.assertContains(page, "Aliyev Vali")
        self.assertContains(page, 'type="radio"', count=8)
        self.assertContains(page, reverse("open_quiz_submit", args=[self.oq.token, attempt.token]))

        self.client.post(
            reverse("open_quiz_save", args=[self.oq.token, attempt.token]), {"leave_count": "2", "away_seconds": "5"}
        )
        self.answer_all_correct(self.client, attempt)
        attempt.refresh_from_db()
        self.assertEqual((attempt.status, attempt.correct, attempt.total), ("finished", 4, 4))
        self.assertEqual(attempt.leave_count, 2)

        result = self.client.get(attempt.get_absolute_url())
        self.assertContains(result, "100%")
        self.assertContains(result, "Natijangiz ustozga yuborildi")
        self.assertNotContains(result, "ruxsat so‘rash")  # umumiy havolada javob ko'rish so'rovi yo'q

    def test_same_browser_returns_to_its_attempt(self):
        self.begin(self.client)
        attempt = OpenAttempt.objects.get()
        self.assertRedirects(self.client.get(self.public), attempt.get_absolute_url())

    def test_same_name_cannot_take_twice_from_another_browser(self):
        self.begin(self.client, "Aliyev Vali")
        other = Client()
        response = self.begin(other, "aliyev   VALI")
        self.assertContains(response, "allaqachon topshirilgan", status_code=400)
        self.assertEqual(OpenAttempt.objects.count(), 1)

    def test_attempt_link_does_not_open_in_another_browser(self):
        self.begin(self.client)
        attempt = OpenAttempt.objects.get()
        stranger = Client()
        self.assertEqual(stranger.get(attempt.get_absolute_url()).status_code, 410)
        response = stranger.post(reverse("open_quiz_submit", args=[self.oq.token, attempt.token]), {})
        self.assertEqual(response.status_code, 302)
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, OpenAttempt.Status.ACTIVE)

    def test_closed_or_expired_link_does_not_start(self):
        self.oq.is_active = False
        self.oq.save()
        response = self.begin(self.client)
        self.assertContains(response, "Test yopilgan", status_code=410)
        self.oq.is_active = True
        self.oq.closes_at = timezone.now() - timedelta(minutes=1)
        self.oq.save()
        self.assertEqual(self.client.get(self.public).status_code, 410)
        self.assertEqual(OpenAttempt.objects.count(), 0)

    def test_russian_choice_on_landing(self):
        response = self.client.get(self.public, {"til": "ru"})
        self.assertContains(response, "введите фамилию, имя и отчество")
        self.assertContains(response, "Циклы")
        self.begin(self.client, til="ru")
        self.assertEqual(OpenAttempt.objects.get().language, "ru")

    def test_expired_attempt_is_graded_with_saved_answers(self):
        self.begin(self.client)
        attempt = OpenAttempt.objects.get()
        OpenAttempt.objects.filter(pk=attempt.pk).update(deadline=timezone.now() - timedelta(minutes=5))
        page = self.client.get(attempt.get_absolute_url())
        self.assertContains(page, "Vaqt tugadi")
        attempt.refresh_from_db()
        self.assertTrue(attempt.timed_out)
        self.assertEqual(attempt.status, OpenAttempt.Status.FINISHED)


class TeacherTests(OpenQuizTestCase):
    def setUp(self):
        super().setUp()
        self.teacher = Client()
        self.teacher.force_login(f.user())

    def test_pages_require_login(self):
        for url in [reverse("open_quiz_list"), reverse("open_quiz_create"), self.oq.get_absolute_url()]:
            self.assertEqual(self.client.get(url).status_code, 302, url)

    def test_create_and_send_to_many_emails_at_once(self):
        response = self.teacher.post(
            reverse("open_quiz_create"),
            {
                "quiz": self.quiz.pk,
                "title": "Saralash bosqichi",
                "language": "uz",
                "question_count": 5,
                "time_limit_minutes": 15,
                "emails": "ali@gmail.com, vali@mail.ru\nALI@gmail.com; sami@inbox.uz",
            },
        )
        oq = OpenQuiz.objects.latest("pk")
        self.assertRedirects(response, oq.get_absolute_url())
        self.assertEqual(
            sorted(m.to[0] for m in mail.outbox), ["ali@gmail.com", "sami@inbox.uz", "vali@mail.ru"]
        )
        self.assertTrue(all(len(m.to) == 1 for m in mail.outbox))  # manzillar bir-biriga ko'rinmaydi
        link = "http://testserver" + oq.get_public_url()
        self.assertIn(link, mail.outbox[0].body)
        self.assertIn("Saralash bosqichi", mail.outbox[0].subject)
        self.assertEqual(OpenQuizInvite.objects.filter(open_quiz=oq, sent_at__isnull=False).count(), 3)

    def test_invalid_emails_and_too_many_questions_are_rejected(self):
        response = self.teacher.post(
            reverse("open_quiz_create"),
            {"quiz": self.quiz.pk, "language": "uz", "question_count": 50, "time_limit_minutes": 10,
             "emails": "ali@gmail.com, noto'g'ri"},
        )
        self.assertContains(response, "Noto‘g‘ri email: noto&#x27;g&#x27;ri", status_code=200)
        self.assertContains(response, "Bu testda 6 ta savol bor")
        self.assertFalse(OpenQuiz.objects.exclude(pk=self.oq.pk).exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_invite_more_later(self):
        response = self.teacher.post(reverse("open_quiz_invite", args=[self.oq.pk]), {"emails": "a@b.uz b@c.uz"})
        self.assertRedirects(response, self.oq.get_absolute_url() + "#invite", fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 2)

    def test_results_page_lists_participants_by_name(self):
        self.begin(self.client, "Aliyev Vali")
        done = OpenAttempt.objects.get()
        self.answer_all_correct(self.client, done)
        self.begin(Client(), "Karimova Nodira")
        page = self.teacher.get(self.oq.get_absolute_url())
        self.assertContains(page, "Aliyev Vali")
        self.assertContains(page, "Karimova Nodira")
        self.assertContains(page, "4/4 · 100%")
        self.assertContains(page, "yechmoqda")
        self.assertEqual((page.context["joined_n"], page.context["done_n"], page.context["avg"]), (2, 1, 100))
        found = self.teacher.get(self.oq.get_absolute_url(), {"q": "karimova"})
        self.assertNotContains(found, "Aliyev Vali")

    def test_teacher_sees_expired_attempts_graded(self):
        self.begin(self.client)
        OpenAttempt.objects.update(deadline=timezone.now() - timedelta(minutes=5))
        self.teacher.get(self.oq.get_absolute_url())
        self.assertEqual(OpenAttempt.objects.get().status, OpenAttempt.Status.FINISHED)

    def test_review_csv_and_delete_allows_retake(self):
        self.begin(self.client, "Aliyev Vali")
        attempt = OpenAttempt.objects.get()
        self.answer_all_correct(self.client, attempt)
        review = self.teacher.get(reverse("open_attempt_review", args=[self.oq.pk, attempt.pk]))
        self.assertContains(review, "to‘g‘ri javob")
        csv = self.teacher.get(reverse("open_quiz_export", args=[self.oq.pk])).content.decode()
        self.assertIn("Aliyev Vali;Tugatgan;4;4;100", csv)

        self.teacher.post(reverse("open_attempt_delete", args=[self.oq.pk, attempt.pk]))
        self.assertFalse(OpenAttempt.objects.exists())
        self.begin(Client(), "Aliyev Vali")
        self.assertEqual(OpenAttempt.objects.count(), 1)

    def test_toggle_and_delete(self):
        self.teacher.post(reverse("open_quiz_toggle", args=[self.oq.pk]))
        self.oq.refresh_from_db()
        self.assertFalse(self.oq.is_active)
        self.teacher.post(reverse("open_quiz_delete", args=[self.oq.pk]))
        self.assertFalse(OpenQuiz.objects.exists())

    def test_list_page_and_tabs(self):
        page = self.teacher.get(reverse("open_quiz_list"))
        self.assertContains(page, "Sikllar")
        self.assertContains(page, "Umumiy havolalar")
        self.assertContains(self.teacher.get(reverse("quiz_batches")), reverse("open_quiz_list"))


class HelperTests(TestCase):
    def test_parse_emails(self):
        good, bad = parse_emails("Ali@Gmail.com, <vali@mail.ru>; ali@gmail.com\nyomon\n\n")
        self.assertEqual(good, ["ali@gmail.com", "vali@mail.ru"])
        self.assertEqual(bad, ["yomon"])

    def test_name_key_ignores_case_spaces_and_apostrophes(self):
        self.assertEqual(name_key("  O‘ktamov   Sardor "), name_key("oʻktamov sardor"))
