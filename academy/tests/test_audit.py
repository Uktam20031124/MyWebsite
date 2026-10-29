from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy.models import ActionLog

from . import factories as f

PASSWORD = "Qulupnay-2026!"


class ActionLogTests(TestCase):
    def setUp(self):
        self.admin = f.user(username="ustoz", is_superuser=True, password=PASSWORD)
        self.ali = f.student(f.group(code="G-1"), full_name="Ali Valiyev")

    def test_login_and_successful_actions_are_logged(self):
        self.assertTrue(self.client.login(username="ustoz", password=PASSWORD))
        self.assertEqual(ActionLog.objects.get().action, "login")

        self.client.post(
            reverse("student_coin_gift", args=[self.ali.pk]), {"amount": "5", "nonce": "n1", "note": "zo‘r"}
        )
        log = ActionLog.objects.filter(action="student_coin_gift").get()
        self.assertEqual((log.user, log.username, log.target), (self.admin, "ustoz", "Ali Valiyev"))

        # Xatoli forma (HTML 200 qayta ko'rsatildi) — yozilmaydi.
        self.client.post(reverse("student_create"), {"full_name": "", "group": ""})
        self.assertFalse(ActionLog.objects.filter(action="student_create").exists())

        # O'chirilgan obyekt nomi jurnalda qoladi.
        self.client.post(reverse("student_delete", args=[self.ali.pk]))
        self.assertEqual(ActionLog.objects.get(action="student_delete").target, "Ali Valiyev")

    def test_passwords_never_stored(self):
        self.client.force_login(self.admin)
        self.client.post(
            reverse("teacher_list"),
            {"first_name": "Malika", "username": "malika", "password": PASSWORD},
        )
        log = ActionLog.objects.get(action="teacher_list")
        self.assertEqual(log.target, "Malika")
        self.assertFalse(ActionLog.objects.filter(target__contains=PASSWORD).exists())

    def test_page_filters_and_access(self):
        self.client.force_login(self.admin)
        self.client.post(
            reverse("student_coin_gift", args=[self.ali.pk]), {"amount": "5", "nonce": "n2"}
        )
        page = self.client.get(reverse("action_log"), {"user": self.admin.pk, "amal": "student_coin_gift"})
        self.assertContains(page, "Quvvat sovg‘a qildi")
        self.assertContains(page, "Ali Valiyev")
        self.assertEqual(page.context["page"].paginator.count, 1)
        self.assertEqual(self.client.get(reverse("action_log"), {"kun": "yomon"}).status_code, 200)

        teacher = f.user(username="malika")
        account = teachers.account_of(teacher)
        account.telegram_id, account.linked_at = 1, timezone.now()
        account.save()
        self.client.force_login(teacher)
        self.assertRedirects(self.client.get(reverse("action_log")), reverse("teacher_home"))

    def test_student_pages_not_logged(self):
        self.client.force_login(self.admin)
        self.client.post(reverse("quiz_save", args=["yoq"]))
        self.assertFalse(ActionLog.objects.exclude(action="login").exists())
