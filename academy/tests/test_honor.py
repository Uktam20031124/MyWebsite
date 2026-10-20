import importlib
from datetime import timedelta

from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import engagement, motivation, profiles
from academy.engagement import EngagementError
from academy.models import CoinTransaction, Purchase, Reward, Student

from . import factories as f


class HonorTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.ali = f.student(self.group, full_name="Ibrahimov Muxammadali")
        self.vali = f.student(self.group, full_name="Valiyev Sardor")
        CoinTransaction.objects.create(student=self.ali, amount=400, reason="Test: 100%")
        self.honor = Reward.objects.create(title="Sertifikatga «A’lochi» belgisi", cost=300, perk=Reward.Perk.HONOR)
        self.teacher = self.client_class()
        self.teacher.force_login(f.user())

    def buy_and_approve(self):
        p = engagement.buy(self.ali, self.honor.pk)
        response = self.teacher.post(reverse("purchase_decide", args=[p.pk]), {"action": "approve"}, follow=True)
        self.ali.refresh_from_db()
        return response

    def test_approving_honor_reward_grants_title_everywhere(self):
        response = self.buy_and_approve()
        self.assertIsNotNone(self.ali.honor_since)
        self.assertContains(response, "“A’lochi” unvoni berildi")
        students = self.teacher.get(reverse("student_list"))
        self.assertContains(students, '<span class="honor-name">Ibrahimov Muxammadali</span>')
        self.assertContains(students, "honor-medal")
        self.assertNotContains(students, '<span class="honor-name">Valiyev Sardor</span>')
        self.assertContains(self.teacher.get(self.ali.get_absolute_url()), "honor-badge")
        group_page = self.teacher.get(self.group.get_absolute_url())
        self.assertContains(group_page, '<span class="honor-name">Ibrahimov Muxammadali</span>')

        motivation.portal_url(self.ali)
        profiles.grant_access(self.ali, 2)
        self.ali.refresh_from_db()
        portal = self.client_class().get(reverse("student_portal", args=[self.ali.portal_token]))
        self.assertContains(portal, "honor-pill")
        self.assertContains(portal, "✓ sizda bor")

    def test_cannot_buy_honor_twice(self):
        self.buy_and_approve()
        with self.assertRaises(EngagementError):
            engagement.buy(self.ali, self.honor.pk)

    def test_rejected_purchase_gives_nothing(self):
        p = engagement.buy(self.ali, self.honor.pk)
        engagement.decide_purchase(p, approve=False)
        self.ali.refresh_from_db()
        self.assertIsNone(self.ali.honor_since)

    def test_ordinary_reward_gives_no_title(self):
        plain = Reward.objects.create(title="Uyga vazifadan ozod", cost=50)
        p = engagement.buy(self.ali, plain.pk)
        engagement.decide_purchase(p, approve=True)
        self.ali.refresh_from_db()
        self.assertIsNone(self.ali.honor_since)

    def test_teacher_can_give_and_remove(self):
        url = reverse("student_honor", args=[self.vali.pk])
        self.teacher.post(url, {"action": "give"})
        self.assertIsNotNone(Student.objects.get(pk=self.vali.pk).honor_since)
        self.teacher.post(url, {"action": "remove"})
        self.assertIsNone(Student.objects.get(pk=self.vali.pk).honor_since)
        self.assertEqual(self.client_class().post(url, {"action": "give"}).status_code, 302)  # login kerak
        self.assertIsNone(Student.objects.get(pk=self.vali.pk).honor_since)

    def test_certificate_has_seal(self):
        engagement.grant_honor(self.ali)
        pdf = motivation.certificate_pdf(self.ali, "Python Pro", "Ustoz")
        self.assertTrue(pdf.startswith(b"%PDF"))
        self.assertGreater(len(pdf), len(motivation.certificate_pdf(self.vali, "Python Pro", "Ustoz")))

    def test_migration_backfills_earlier_approved_purchase(self):
        old = Reward.objects.create(title="Sertifikatga «A’lochi» belgisi", cost=300)  # perk belgilanmagan
        decided = timezone.now() - timedelta(days=1)
        Purchase.objects.create(
            student=self.vali, reward=old, title=old.title, cost=300,
            status=Purchase.Status.APPROVED, decided_at=decided,
        )
        migration = importlib.import_module("academy.migrations.0029_honor")
        migration.mark_honor_rewards(apps, None)
        old.refresh_from_db()
        self.vali.refresh_from_db()
        self.assertEqual(old.perk, Reward.Perk.HONOR)
        self.assertEqual(self.vali.honor_since, decided)
