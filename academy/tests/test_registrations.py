from unittest import mock

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from academy.models import Registration, RegistrationLink, Student

from . import factories as f

FORM = {"full_name": "Aliyev Sardor Akmalovich", "phone": "90 123 45 67", "telegram": "@sardor_a"}


@mock.patch("academy.registrations.notify_teacher")
class PublicFormTests(TestCase):
    def setUp(self):
        cache.clear()
        self.group = f.group(name="S-009")
        self.link = RegistrationLink.objects.create(title="S-009 chat", group=self.group)
        self.url = self.link.get_absolute_url()

    def test_submit_creates_pending_registration(self, notify):
        page = self.client.get(self.url)
        self.assertContains(page, "Ro‘yxatdan o‘tish")
        response = self.client.post(self.url, FORM)
        self.assertContains(response, "Rahmat, Aliyev Sardor Akmalovich!")
        reg = Registration.objects.get()
        self.assertEqual(
            (reg.full_name, reg.phone, reg.telegram, reg.status, reg.link),
            ("Aliyev Sardor Akmalovich", "+998901234567", "sardor_a", "pending", self.link),
        )
        notify.assert_called_once_with(reg)
        self.assertFalse(Student.objects.exists())  # bazaga o'z-o'zidan yozilmaydi

    def test_validation(self, notify):
        response = self.client.post(self.url, {"full_name": "Ali", "phone": "123", "telegram": "@ab"})
        self.assertContains(response, "Familiya va ismingizni to‘liq yozing.")
        self.assertContains(response, "Telefon raqami noto‘g‘ri")
        self.assertContains(response, "Username noto‘g‘ri")
        self.assertFalse(Registration.objects.exists())

    def test_name_case_is_fixed(self, notify):
        self.client.post(self.url, {**FORM, "full_name": "aliyev  sardor"})
        self.assertEqual(Registration.objects.get().full_name, "Aliyev Sardor")

    def test_resubmit_with_same_phone_updates(self, notify):
        self.client.post(self.url, FORM)
        self.client.post(self.url, {**FORM, "telegram": "sardor_new"})
        self.assertEqual(Registration.objects.count(), 1)
        self.assertEqual(Registration.objects.get().telegram, "sardor_new")
        self.assertEqual(notify.call_count, 1)

    def test_inactive_link_and_unknown_token(self, notify):
        self.link.is_active = False
        self.link.save()
        response = self.client.post(self.url, FORM)
        self.assertContains(response, "Ro‘yxat yopilgan", status_code=410)
        self.assertFalse(Registration.objects.exists())
        self.assertEqual(self.client.get(reverse("registration_public", args=["yoq"])).status_code, 404)

    def test_throttle(self, notify):
        with mock.patch("academy.views.REGISTRATION_LIMIT", 1):
            self.client.post(self.url, FORM)
            response = self.client.post(self.url, {**FORM, "phone": "901112233"})
        self.assertContains(response, "Juda ko‘p urinish")
        self.assertEqual(Registration.objects.count(), 1)


class ReviewTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.group = f.group(name="S-009")
        self.other_group = f.group(name="P-006")
        self.sardor = f.student(self.group, full_name="Aliyev Sardor", telegram="old")
        self.link = RegistrationLink.objects.create(title="S-009 chat", group=self.group)

    def reg(self, name="Sardor Aliyev", link=None, **kw):
        return Registration.objects.create(
            link=link or self.link, full_name=name,
            phone=kw.get("phone", "+998901234567"), telegram=kw.get("telegram", "sardor_a"),
        )

    def act(self, reg, **data):
        return self.client.post(reverse("registration_action", args=[reg.pk]), data)

    def test_list_shows_suggestion_and_counts(self):
        self.reg()
        self.reg("Yangi Bola", phone="+998907777777", telegram="yangi_b")
        page = self.client.get(reverse("registrations"))
        self.assertContains(page, "Bazada bor:")
        self.assertContains(page, "Bazada topilmadi")
        self.assertContains(page, "Ishonchlilarni tasdiqlash (2)")
        self.assertContains(page, self.link.get_absolute_url())
        self.assertEqual(page.context["nav_registrations"], 2)

    def test_attach_to_existing(self):
        reg = self.reg()
        self.act(reg, action="attach", student=self.sardor.pk)
        self.sardor.refresh_from_db()
        reg.refresh_from_db()
        self.assertEqual((self.sardor.telegram, self.sardor.phone), ("sardor_a", "+998901234567"))
        self.assertEqual((reg.status, reg.student), ("approved", self.sardor))
        self.assertIsNotNone(reg.reviewed_at)

    def test_create_new_student(self):
        reg = self.reg("Yangi Bola", telegram="yangi_b")
        self.act(reg, action="create", group=self.other_group.pk)
        student = Student.objects.get(full_name="Yangi Bola")
        self.assertEqual((student.group, student.telegram), (self.other_group, "yangi_b"))
        reg.refresh_from_db()
        self.assertEqual(reg.student, student)

    def test_reject_and_missing_choice(self):
        reg = self.reg()
        response = self.act(reg, action="attach", student="")
        self.assertEqual(Registration.objects.get().status, "pending")
        self.act(reg, action="reject")
        reg.refresh_from_db()
        self.assertEqual(reg.status, "rejected")
        self.sardor.refresh_from_db()
        self.assertEqual(self.sardor.telegram, "old")
        self.assertEqual(self.act(reg, action="reject").status_code, 404)  # qayta ko'rib bo'lmaydi
        self.assertEqual(response.status_code, 302)

    def test_approve_all_only_confident(self):
        attach = self.reg()  # yagona mos → biriktiriladi
        new = self.reg("Yangi Bola", phone="+998907777777", telegram="yangi_b")  # mos yo'q + guruh → yangi
        f.student(self.group, full_name="Aliyev Sanjar")
        ambiguous = self.reg("Aliyev S", phone="+998905555555", telegram="aliyev_s")  # 2 ta mos → qoladi
        nogroup = RegistrationLink.objects.create(title="Umumiy")
        manual = self.reg("Boshqa Odam", link=nogroup, phone="+998904444444", telegram="boshqa_o")
        self.client.post(reverse("registration_approve_all"))
        statuses = {r.pk: r.status for r in Registration.objects.all()}
        self.assertEqual(statuses[attach.pk], "approved")
        self.assertEqual(statuses[new.pk], "approved")
        self.assertEqual(statuses[ambiguous.pk], "pending")
        self.assertEqual(statuses[manual.pk], "pending")
        self.assertTrue(Student.objects.filter(full_name="Yangi Bola", group=self.group).exists())

    def test_link_create_toggle_delete(self):
        response = self.client.post(reverse("registrations"), {"title": "P-006 chat", "group": self.other_group.pk})
        self.assertRedirects(response, f"{reverse('registrations')}#links")
        link = RegistrationLink.objects.get(title="P-006 chat")
        self.assertTrue(link.token)
        url = reverse("registration_link_action", args=[link.pk])
        self.client.post(url, {"action": "off"})
        link.refresh_from_db()
        self.assertFalse(link.is_active)
        reg = self.reg(link=link)
        self.client.post(url, {"action": "delete"})
        self.assertFalse(RegistrationLink.objects.filter(pk=link.pk).exists())
        reg.refresh_from_db()
        self.assertIsNone(reg.link)  # ariza saqlanadi

    def test_tabs_render(self):
        reg = self.reg()
        self.act(reg, action="attach", student=self.sardor.pk)
        for status in ("pending", "approved", "rejected"):
            with self.subTest(status=status):
                self.assertEqual(self.client.get(reverse("registrations"), {"status": status}).status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("registrations")).status_code, 302)
        reg = self.reg()
        self.act(reg, action="reject")
        self.assertEqual(Registration.objects.get().status, "pending")


class NotifyTests(TestCase):
    def test_notify_sends_in_background_when_configured(self):
        from academy.registrations import notify_teacher

        link = RegistrationLink.objects.create(title="S-009 chat")
        reg = Registration.objects.create(link=link, full_name="Ali Vali", phone="+998901234567", telegram="ali_v")
        with mock.patch("academy.telegram_sender.is_configured", return_value=True), mock.patch(
            "academy.telegram_sender.send_text_to_self"
        ) as send, mock.patch("threading.Thread") as thread:
            notify_teacher(reg)
            thread.call_args.kwargs["target"]()
        text = send.call_args.args[0]
        self.assertIn("Ali Vali", text)
        self.assertIn("@ali_v", text)
        self.assertIn("S-009 chat", text)

    def test_notify_skipped_without_telegram(self):
        from academy.registrations import notify_teacher

        reg = Registration.objects.create(full_name="Ali Vali", phone="+998901234567", telegram="ali_v")
        with mock.patch("academy.telegram_sender.is_configured", return_value=False), mock.patch(
            "threading.Thread"
        ) as thread:
            notify_teacher(reg)
        thread.assert_not_called()
