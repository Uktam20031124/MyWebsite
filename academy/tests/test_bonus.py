from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import bonus, coins, motivation
from academy.models import BonusAnswer, Mistake, Question, Quiz, SyllabusItem
from academy.services import parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 4))


def _choice(question, correct):
    return question.choices.get(is_correct=correct)


class BonusTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        self.ali.profile_until = timezone.now() + timedelta(hours=2)
        self.ali.save()
        motivation.portal_url(self.ali)
        self.taught = f.topic(title="O'tilgan")
        Quiz.objects.create(topic=self.taught, bonus_quvvat=4).replace_questions(parse_quiz(TEXT)[0])
        SyllabusItem.objects.create(group=self.group, topic=self.taught, order=1, status=SyllabusItem.Status.TAUGHT)
        self.planned = f.topic(title="Rejada")
        Quiz.objects.create(topic=self.planned).replace_questions(parse_quiz(TEXT)[0])
        SyllabusItem.objects.create(group=self.group, topic=self.planned, order=2)

    def test_only_taught_topics_and_stable_next(self):
        self.assertEqual(bonus.questions(self.ali).count(), 3)
        self.assertTrue(all(q.quiz.topic_id == self.taught.pk for q in bonus.questions(self.ali)))
        self.assertEqual(bonus.next_question(self.ali), bonus.next_question(self.ali))  # yangilash almashtirmaydi

    def test_correct_answer_gives_quiz_bonus_once(self):
        q = bonus.next_question(self.ali)
        result = bonus.answer(self.ali, q.pk, _choice(q, True).pk)
        self.assertTrue(result.correct)
        self.assertEqual(result.coins, 4)
        self.assertEqual(coins.balance(self.ali), 4)
        self.assertEqual(self.ali.coins.get().display_reason, "➕ Qo‘shimcha savol: O'tilgan")
        with self.assertRaises(bonus.BonusError):
            bonus.answer(self.ali, q.pk, _choice(q, True).pk)
        self.assertEqual(coins.balance(self.ali), 4)
        self.assertEqual(bonus.questions(self.ali).count(), 2)

    def test_wrong_answer_goes_to_mistakes(self):
        q = bonus.next_question(self.ali)
        result = bonus.answer(self.ali, q.pk, _choice(q, False).pk)
        self.assertFalse(result.correct)
        self.assertEqual(coins.balance(self.ali), 0)
        self.assertTrue(Mistake.objects.filter(student=self.ali, question=q, resolved_at__isnull=True).exists())
        self.assertEqual(bonus.summary(self.ali)["answered"], 1)

    def test_rejects_untaught_question_and_foreign_choice(self):
        other = Question.objects.filter(quiz__topic=self.planned).first()
        with self.assertRaises(bonus.BonusError):
            bonus.answer(self.ali, other.pk, _choice(other, True).pk)
        q = bonus.next_question(self.ali)
        with self.assertRaises(bonus.BonusError):
            bonus.answer(self.ali, q.pk, _choice(other, True).pk)
        self.assertFalse(BonusAnswer.objects.exists())

    def test_daily_limit(self):
        with mock.patch.object(bonus, "DAILY_LIMIT", 1):
            q = bonus.next_question(self.ali)
            bonus.answer(self.ali, q.pk, _choice(q, True).pk)
            q2 = bonus.next_question(self.ali)
            with self.assertRaisesMessage(bonus.BonusError, "limit"):
                bonus.answer(self.ali, q2.pk, _choice(q2, True).pk)
            self.assertEqual(bonus.summary(self.ali)["left_today"], 0)

    # --- Sahifalar -------------------------------------------------------------

    def test_portal_tab_and_bonus_page(self):
        token = self.ali.portal_token
        url = reverse("portal_bonus", args=[token])
        self.assertContains(self.client.get(reverse("student_portal", args=[token])), url)
        r = self.client.get(url)
        self.assertContains(r, "+4 ⚡️")
        q = r.context["question"]
        self.assertNotContains(r, "is_correct")
        r = self.client.post(url, {"question": q.pk, "choice": _choice(q, True).pk})
        self.assertRedirects(r, url, fetch_redirect_response=False)
        self.assertContains(self.client.get(url), "+4 ⚡️ quvvat")
        self.assertEqual(coins.balance(self.ali), 4)

    def test_closed_profile_redirects(self):
        self.ali.profile_until = None
        self.ali.save()
        r = self.client.get(reverse("portal_bonus", args=[self.ali.portal_token]))
        self.assertRedirects(r, reverse("student_portal", args=[self.ali.portal_token]), fetch_redirect_response=False)

    def test_qr_cards(self):
        bob = f.student(self.group, full_name="Bob Karimov")
        self.assertEqual(bob.portal_token, "")
        self.assertEqual(self.client.get(reverse("group_qr", args=[self.group.pk])).status_code, 302)  # login kerak
        self.client.force_login(f.user())
        r = self.client.get(reverse("group_qr", args=[self.group.pk]))
        self.assertContains(r, 'class="qr-code"', count=2)
        self.assertNotContains(r, "qr-path")
        self.assertContains(r, "Bob Karimov")
        bob.refresh_from_db()
        self.assertTrue(bob.portal_token)  # kalit yaratildi
        self.assertContains(r, reverse("portal_bonus", args=[bob.portal_token]))
        r = self.client.get(reverse("student_qr", args=[self.ali.pk]))
        self.assertContains(r, 'class="qr-code"', count=1)

    def test_teacher_sets_bonus_on_quiz(self):
        self.client.force_login(f.user())
        r = self.client.post(
            reverse("quiz_edit", args=[self.taught.pk]), {"time_limit_minutes": 10, "bonus_quvvat": 5, "text": TEXT}
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Quiz.objects.get(topic=self.taught).bonus_quvvat, 5)
        r = self.client.post(
            reverse("quiz_edit", args=[self.taught.pk]), {"time_limit_minutes": 10, "bonus_quvvat": 9, "text": TEXT}
        )
        self.assertEqual(r.status_code, 200)  # 1–5 dan tashqari — xato
