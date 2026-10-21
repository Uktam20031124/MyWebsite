from django.test import TestCase
from django.urls import reverse
from django.utils.translation import override

from academy import coins, motivation, profiles
from academy.models import CoinTransaction, Quiz, SyllabusItem, TestRequest, TopicUnlock
from academy.services import parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 7))


class UnlockTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        self.topics = []
        for i, status in enumerate(["taught", "planned", "planned", "planned", "planned"], 1):
            topic = f.topic(title=f"Mavzu {i}", study=f"Mavzu {i} materiali")
            Quiz.objects.create(topic=topic).replace_questions(parse_quiz(TEXT)[0])
            SyllabusItem.objects.create(group=self.group, topic=topic, order=i, status=status)
            self.topics.append(topic)
        motivation.portal_url(self.ali)
        profiles.grant_access(self.ali, 2)
        self.ali.refresh_from_db()
        CoinTransaction.objects.create(student=self.ali, amount=100, reason="Test: 100%")
        self.portal = reverse("student_portal", args=[self.ali.portal_token])

    def unlock(self, topic):
        return self.client.post(reverse("portal_unlock", args=[self.ali.portal_token, topic.pk]))

    def test_offers_are_next_planned_topics(self):
        self.assertEqual(profiles.unlock_offers(self.ali), self.topics[1:4])
        page = self.client.get(self.portal)
        self.assertContains(page, "Yangi mavzularni ochish")
        self.assertContains(page, "Ochish · 30 ⚡️")

    def test_unlock_spends_and_opens_material_and_test(self):
        response = self.unlock(self.topics[1])
        study_url = reverse("portal_study", args=[self.ali.portal_token, self.topics[1].pk])
        self.assertRedirects(response, study_url, fetch_redirect_response=False)
        self.assertEqual(coins.balance(self.ali), 70)
        self.assertTrue(TopicUnlock.objects.filter(student=self.ali, topic=self.topics[1], cost=30).exists())
        study = self.client.get(response["Location"])
        self.assertContains(study, "Mavzu 2 materiali")
        row = profiles.row_for(self.ali, self.topics[1])
        self.assertTrue(row.unlocked and row.can_start)
        page = self.client.get(self.portal)
        self.assertContains(page, "quvvat bilan ochilgan")
        self.assertContains(page, "📘 Material")
        self.assertEqual(profiles.unlock_offers(self.ali), [self.topics[2], self.topics[3], self.topics[4]])
        # Oldindan ochilgan mavzu testi — "oldindan o'zlashtirdi" bonusi uchun.
        self.assertEqual(profiles.begin_test(self.ali, self.topics[1]).kind, TestRequest.Kind.PREVIEW)

    def test_not_enough_energy(self):
        CoinTransaction.objects.create(student=self.ali, amount=-80, reason="Test: 0%")
        response = self.client.post(
            reverse("portal_unlock", args=[self.ali.portal_token, self.topics[1].pk]), follow=True
        )
        self.assertContains(response, "Quvvat yetmaydi")
        self.assertFalse(TopicUnlock.objects.exists())
        self.assertContains(self.client.get(self.portal), "yana 10 ⚡️ kerak")

    def test_only_offered_topics_and_once(self):
        self.unlock(self.topics[4])  # navbatda 4-o'rinda — hali taklif qilinmaydi
        self.unlock(self.topics[0])  # allaqachon o'tilgan
        self.assertFalse(TopicUnlock.objects.exists())
        self.unlock(self.topics[1])
        self.unlock(self.topics[1])
        self.assertEqual(TopicUnlock.objects.count(), 1)
        self.assertEqual(coins.balance(self.ali), 70)

    def test_closed_profile_cannot_unlock(self):
        profiles.close_access(self.ali)
        self.unlock(self.topics[1])
        self.assertFalse(TopicUnlock.objects.exists())

    def test_teacher_sees_unlocked_topics_and_reason_translated(self):
        self.unlock(self.topics[1])
        teacher = self.client_class()
        teacher.force_login(f.user())
        page = teacher.get(self.ali.get_absolute_url())
        self.assertContains(page, "Quvvat bilan ochgan mavzulari")
        tx = CoinTransaction.objects.get(amount=-30)
        with override("ru"):
            self.assertEqual(tx.display_reason, "🔓 Тема открыта: Mavzu 2")
