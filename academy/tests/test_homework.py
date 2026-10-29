import tempfile
from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import coins, homework, motivation, teachers
from academy.models import Group, HomeworkSubmission, Lesson

from . import factories as f


class HomeworkTests(TestCase):
    def setUp(self):
        media = tempfile.TemporaryDirectory()
        self.addCleanup(media.cleanup)
        patcher = override_settings(MEDIA_ROOT=media.name)
        patcher.enable()
        self.addCleanup(patcher.disable)
        self.today = timezone.localdate()
        self.group = f.group(code="H-1")
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        self.vali = f.student(self.group, full_name="Vali Karimov")
        for s in (self.ali, self.vali):
            s.profile_until = timezone.now() + timedelta(hours=2)
            s.save()
            motivation.portal_url(s)
        self.lesson = f.lesson(self.group, days=-1, homework="5 ta misol yeching", topic=f.topic(title="Sikllar"))
        self.next = f.lesson(self.group, days=2)
        self.admin = f.user(username="ustoz", is_superuser=True)

    def url(self, student=None):
        return reverse("portal_homework", args=[(student or self.ali).portal_token, self.lesson.pk])

    def test_submit_update_and_due(self):
        self.assertEqual(homework.due_date(self.lesson), self.next.held_on)
        r = self.client.post(
            self.url(), {"text": "Javobim", "file": SimpleUploadedFile("ish.txt", b"salom", "text/plain")}
        )
        self.assertRedirects(r, self.url())
        sub = HomeworkSubmission.objects.get()
        self.assertTrue(sub.on_time)
        self.assertEqual((sub.text, sub.file_name), ("Javobim", "ish.txt"))
        self.assertTrue(sub.file.name.startswith("homework/"))
        # Baholanmaguncha yangilash mumkin; fayl saqlanib qoladi.
        self.client.post(self.url(), {"text": "Yangi javob", "link": "https://docs.google.com/x"})
        sub.refresh_from_db()
        self.assertEqual((sub.text, sub.link, sub.file_name), ("Yangi javob", "https://docs.google.com/x", "ish.txt"))
        self.assertEqual(HomeworkSubmission.objects.count(), 1)
        # Portal tabida ko'rinadi.
        portal = self.client.get(reverse("student_portal", args=[self.ali.portal_token]))
        self.assertContains(portal, "tekshirilmoqda")

    def test_rejects_bad_input(self):
        r = self.client.post(self.url(), {"file": SimpleUploadedFile("virus.exe", b"x")})
        self.assertEqual(r.status_code, 422)
        self.assertContains(r, ".exe", status_code=422)
        r = self.client.post(self.url(), {"text": "  "})
        self.assertEqual(r.status_code, 422)
        other_group_lesson = f.lesson(f.group(), days=-1, homework="boshqa")
        r = self.client.get(reverse("portal_homework", args=[self.ali.portal_token, other_group_lesson.pk]))
        self.assertEqual(r.status_code, 404)
        self.assertFalse(HomeworkSubmission.objects.exists())

    def test_grading_gives_coins_once_and_locks(self):
        self.client.post(self.url(), {"text": "Javob"})
        sub = HomeworkSubmission.objects.get()
        self.client.force_login(self.admin)
        self.client.post(reverse("homework_check", args=[sub.pk]), {"score": "80", "comment": "Barakalla"})
        sub.refresh_from_db()
        self.assertEqual((sub.status, sub.score, sub.coins), ("checked", 80, homework.COINS))
        self.assertEqual(coins.balance(self.ali), homework.COINS)
        self.client.post(reverse("homework_check", args=[sub.pk]), {"score": "95"})  # qayta baholash
        self.assertEqual(coins.balance(self.ali), homework.COINS)
        self.assertEqual(self.ali.coins.get().display_reason, "📝 Uyga vazifa: Sikllar")
        # Baholangandan keyin o'zgartirib bo'lmaydi.
        self.client.logout()
        r = self.client.post(self.url(), {"text": "o‘zgartiraman"})
        self.assertContains(r, "allaqachon baholangan", status_code=422)
        sub.refresh_from_db()
        self.assertEqual(sub.text, "Javob")

    def test_late_or_low_score_no_coins(self):
        Lesson.objects.filter(pk=self.next.pk).update(held_on=self.today - timedelta(days=1), status="completed")
        Lesson.objects.filter(pk=self.lesson.pk).update(held_on=self.today - timedelta(days=5))
        self.client.post(self.url(), {"text": "Kech"})
        sub = HomeworkSubmission.objects.get()
        self.assertFalse(sub.on_time)
        self.assertEqual(homework.grade(sub, 100, "", self.admin), 0)
        self.client.post(self.url(self.vali), {"text": "Vaqtida emas, lekin"})
        low = HomeworkSubmission.objects.get(student=self.vali)
        self.assertEqual(homework.grade(low, 30, "", self.admin), 0)

    def test_file_access_is_private(self):
        self.client.post(self.url(), {"text": "x", "file": SimpleUploadedFile("ish.txt", b"maxfiy", "text/plain")})
        sub = HomeworkSubmission.objects.get()
        own = reverse("portal_homework_file", args=[self.ali.portal_token, sub.pk])
        self.assertEqual(b"".join(self.client.get(own).streaming_content), b"maxfiy")
        stranger = reverse("portal_homework_file", args=[self.vali.portal_token, sub.pk])
        self.assertEqual(self.client.get(stranger).status_code, 404)
        self.assertEqual(self.client.get(reverse("homework_file", args=[sub.pk])).status_code, 302)  # login kerak
        self.assertEqual(self.client.get(f"/media/{sub.file.name}").status_code, 404)  # ochiq media emas
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("homework_file", args=[sub.pk])).status_code, 200)
        page = self.client.get(reverse("homework_list"))
        self.assertContains(page, "Ali Valiyev")
        self.assertContains(self.client.get(self.lesson.get_absolute_url()), "Topshirilgan uyga vazifalar")

    def test_teacher_sees_only_own_groups(self):
        self.client.post(self.url(), {"text": "x"})
        sub = HomeworkSubmission.objects.get()
        teacher = f.user(username="malika")
        account = teachers.account_of(teacher)
        account.telegram_id, account.linked_at, account.permissions = 1, timezone.now(), ["homework"]
        account.save()
        self.client.force_login(teacher)
        self.assertNotContains(self.client.get(reverse("homework_list")), "Ali Valiyev")
        self.assertEqual(self.client.get(reverse("homework_file", args=[sub.pk])).status_code, 404)
        self.assertEqual(self.client.post(reverse("homework_check", args=[sub.pk]), {"score": "90"}).status_code, 404)
        Group.objects.filter(pk=self.group.pk).update(teacher=teacher)
        self.assertContains(self.client.get(reverse("homework_list")), "Ali Valiyev")
        self.client.post(reverse("homework_check", args=[sub.pk]), {"score": "90"})
        sub.refresh_from_db()
        self.assertEqual((sub.score, sub.checked_by), (90, teacher))
