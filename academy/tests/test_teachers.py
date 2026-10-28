import asyncio
import tempfile
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy import telegram_sender as tg
from academy.models import Group, Quiz, QuizBatch, TeacherAccount
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 6))
PASSWORD = "Qulupnay-2026!"


def ok_results(items, **kw):
    return [tg.Result(i.key, True) for i in items]


class TeacherTestsMixin:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = override_settings(TELEGRAM_SESSIONS_DIR=self.tmp.name, TELEGRAM_API_ID=1, TELEGRAM_API_HASH="h")
        patcher.enable()
        self.addCleanup(patcher.disable)
        self.admin = f.user(username="ustoz", is_superuser=True, is_staff=True)
        self.mine = f.group(code="M-1", name="Mening guruhim")
        self.other = f.group(code="O-1", name="Boshqa guruh")
        self.ali = f.student(self.mine, full_name="Ali Valiyev", telegram="ali_v")
        self.zuh = f.student(self.other, full_name="Zuhra Begim", telegram="zuhra_b")
        self.topic = f.topic(title="Sikllar")
        Quiz.objects.create(topic=self.topic).replace_questions(parse_quiz(TEXT)[0])

    def make_teacher(self, linked=True):
        teacher = f.user(username="malika", first_name="Malika", password=PASSWORD)
        Group.objects.filter(pk=self.mine.pk).update(teacher=teacher)
        account = teachers.account_of(teacher)
        if linked:
            account.telegram_id, account.linked_at, account.telegram_name = 555, timezone.now(), "Malika"
            account.save()
            tg.save_teacher_session(teacher.pk, "teacher-session")
        return teacher


class AdminManagesTeachersTests(TeacherTestsMixin, TestCase):
    def test_create_edit_and_unlink(self):
        self.client.force_login(self.admin)
        r = self.client.post(
            reverse("teacher_list"),
            {"first_name": "Malika", "last_name": "Karimova", "username": "malika", "password": PASSWORD,
             "groups": [self.mine.pk], "permissions": ["students", "groups"]},
        )
        self.assertRedirects(r, reverse("teacher_list"))
        teacher = get_user_model().objects.get(username="malika")
        self.assertFalse(teacher.is_superuser or teacher.is_staff)
        self.assertTrue(teacher.check_password(PASSWORD))
        self.assertEqual(teacher.teacher_account.permissions, ["groups", "students"])
        self.assertContains(self.client.get(reverse("teacher_list")), "Ruxsatlar: Guruhlar, Shogirdlar")
        self.mine.refresh_from_db()
        self.assertEqual(self.mine.teacher, teacher)
        self.assertContains(self.client.get(reverse("teacher_list")), "Telegram ulanmagan")

        # Tahrirlash: guruh almashtirildi, parol bo'sh — eskisi qoladi.
        self.client.post(
            reverse("teacher_edit", args=[teacher.pk]),
            {
                "first_name": "Malika",
                "username": "malika",
                "password": "",
                "groups": [self.other.pk],
                "is_active": "on",
            },
        )
        self.mine.refresh_from_db()
        self.other.refresh_from_db()
        self.assertIsNone(self.mine.teacher)
        self.assertEqual(self.other.teacher, teacher)
        teacher.refresh_from_db()
        self.assertTrue(teacher.check_password(PASSWORD))

        # Band login va zaif parol rad etiladi.
        r = self.client.post(reverse("teacher_list"), {"first_name": "X", "username": "ustoz", "password": "123"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("username", r.context["form"].errors)
        self.assertIn("password", r.context["form"].errors)

    def test_unlink_makes_teacher_link_again(self):
        teacher = self.make_teacher()
        self.client.force_login(self.admin)
        self.client.post(reverse("teacher_unlink", args=[teacher.pk]))
        account = TeacherAccount.objects.get(user=teacher)
        self.assertFalse(account.is_linked)
        self.assertFalse(tg.teacher_session_path(teacher.pk).exists())

    def test_teacher_pages_closed_for_non_admin(self):
        teacher = self.make_teacher()
        self.client.force_login(teacher)
        self.assertRedirects(self.client.get(reverse("teacher_list")), reverse("teacher_home"))


@mock.patch("academy.teachers.start_link")
class TeacherAccessTests(TeacherTestsMixin, TestCase):
    def test_first_login_asks_telegram_once(self, start_link):
        teacher = self.make_teacher(linked=False)
        self.client.force_login(teacher)
        self.assertRedirects(self.client.get(reverse("dashboard")), reverse("teacher_telegram"))
        self.assertRedirects(self.client.get(reverse("quiz_send")), reverse("teacher_telegram"))
        page = self.client.get(reverse("teacher_telegram"))
        self.assertContains(page, "Telegramingizni ulang")
        start_link.assert_called()

        # Ulangach — qayta so'ralmaydi.
        account = TeacherAccount.objects.get(user=teacher)
        account.telegram_id, account.linked_at = 555, timezone.now()
        account.save()
        self.assertRedirects(self.client.get(reverse("dashboard")), reverse("teacher_home"))
        self.assertRedirects(self.client.get(reverse("teacher_telegram")), reverse("teacher_home"))

    def test_teacher_sees_only_own_groups(self, start_link):
        teacher = self.make_teacher()
        self.client.force_login(teacher)
        home = self.client.get(reverse("teacher_home"))
        self.assertContains(home, "Mening guruhim")
        self.assertNotContains(home, "Boshqa guruh")
        for name in ("group_list", "student_list", "quiz_batches", "quiz_warnings"):
            self.assertRedirects(self.client.get(reverse(name)), reverse("teacher_home"))
        # Boshqa guruh o'quvchisi — borligini ham bildirmaymiz.
        self.assertEqual(self.client.get(reverse("student_detail", args=[self.zuh.pk])).status_code, 404)
        # Boshqa guruhni so'rasa ham — faqat o'z guruhi.
        page = self.client.get(reverse("quiz_send"), {"topic": self.topic.pk, "group": self.other.pk})
        self.assertContains(page, "Ali Valiyev")
        self.assertNotContains(page, "Zuhra Begim")
        other_batch = create_quiz_batch(self.topic.quiz, [self.zuh], 3, 5)
        self.assertEqual(self.client.get(reverse("quiz_batch", args=[other_batch.pk])).status_code, 404)
        attempt = other_batch.attempts.get()
        self.assertEqual(self.client.get(reverse("quiz_attempt_review", args=[attempt.pk])).status_code, 404)

    def test_granted_sections_show_only_own_groups(self, start_link):
        teacher = self.make_teacher()
        account = teacher.teacher_account
        account.permissions = ["groups", "students", "lessons", "warnings", "requests"]
        account.save()
        f.lesson(self.mine, topic=self.topic)
        f.lesson(self.other, topic=self.topic)
        self.client.force_login(teacher)

        nav = self.client.get(reverse("teacher_home"))
        for label in ("Guruhlar", "Shogirdlar", "Darslar", "Ogohlantirishlar", "So‘rovlar"):
            self.assertContains(nav, label)
        self.assertNotContains(nav, reverse("rewards"))
        self.assertNotContains(nav, reverse("teacher_list"))

        groups = self.client.get(reverse("group_list"))
        self.assertContains(groups, "Mening guruhim")
        self.assertNotContains(groups, "Boshqa guruh")
        self.assertEqual(self.client.get(reverse("group_detail", args=[self.mine.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("group_detail", args=[self.other.pk])).status_code, 404)

        students = self.client.get(reverse("student_list"))
        self.assertContains(students, "Ali Valiyev")
        self.assertNotContains(students, "Zuhra Begim")
        self.assertEqual(self.client.get(reverse("student_detail", args=[self.ali.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("student_detail", args=[self.zuh.pk])).status_code, 404)
        export = self.client.get(reverse("student_export")).content.decode()
        self.assertIn("Ali Valiyev", export)
        self.assertNotIn("Zuhra Begim", export)
        # Shogird qo'shishda — faqat o'z guruhi.
        form = self.client.get(reverse("student_create")).context["form"]
        self.assertEqual(list(form.fields["group"].queryset), [self.mine])

        lessons = self.client.get(reverse("lesson_list"))
        self.assertEqual({lesson.group for lesson in lessons.context["lessons"]}, {self.mine})
        self.assertEqual(self.client.get(reverse("quiz_warnings")).status_code, 200)
        self.assertEqual(self.client.get(reverse("quiz_review_requests")).status_code, 200)

        # Ruxsat berilmagan bo'lim va bosh ustoz bo'limlari — yopiq.
        for name in ("rewards", "topic_list", "registrations", "group_create", "teacher_list", "dashboard"):
            self.assertRedirects(self.client.get(reverse(name)), reverse("teacher_home"))

    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_teacher_sends_from_own_telegram(self, send, start_link):
        teacher = self.make_teacher()
        self.client.force_login(teacher)
        r = self.client.post(
            reverse("quiz_send") + f"?topic={self.topic.pk}&group={self.mine.pk}",
            {"students": [self.ali.pk], "question_count": 3, "time_limit_minutes": 5, "channels": ["telegram"]},
        )
        batch = QuizBatch.objects.get()
        self.assertRedirects(r, batch.get_absolute_url())
        self.assertEqual(batch.sent_by, teacher)
        account = send.call_args.kwargs["account"]
        self.assertEqual((account.session, account.expected_id, account.teacher), ("teacher-session", 555, True))
        self.assertEqual(self.client.get(batch.get_absolute_url()).status_code, 200)
        # Boshqa guruh o'quvchisini qo'shib bo'lmaydi.
        r = self.client.post(
            reverse("quiz_send") + f"?topic={self.topic.pk}&group={self.mine.pk}",
            {"students": [self.zuh.pk], "question_count": 3, "time_limit_minutes": 5},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(QuizBatch.objects.count(), 1)

    def test_accounts(self, start_link):
        teacher = self.make_teacher()
        self.assertEqual(tg.account_for(teacher).expected_id, 555)
        with override_settings(TELEGRAM_SENDER_ID=777):
            self.assertEqual(tg.account_for(self.admin).expected_id, 777)
            self.assertEqual(tg.account_for(None).expected_id, 777)
        fresh = f.user(username="yangi")
        teachers.account_of(fresh)  # o'qituvchi, Telegram hali ulanmagan
        self.assertFalse(tg.is_configured(tg.account_for(fresh)))
        self.assertIn("QR", tg.setup_hint(tg.account_for(fresh)))
        staff = f.user(username="xodim")  # admin panelda qo'shilgan — to'liq ustoz
        self.assertFalse(teachers.is_teacher(staff))
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse("group_list")).status_code, 200)


class FakeQR:
    def __init__(self, outcomes):
        self.url, self.outcomes = "tg://login?token=AAA", list(outcomes)

    async def wait(self, timeout=None):
        outcome = self.outcomes.pop(0)
        if outcome:
            raise outcome

    async def recreate(self):
        self.url = "tg://login?token=BBB"


class FakeClient:
    def __init__(self, qr):
        self.qr, self.passwords = qr, []
        self.session = SimpleNamespace(save=lambda: "new-session")

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def qr_login(self):
        return self.qr

    async def get_me(self):
        return SimpleNamespace(id=4242, first_name="Malika", last_name="K", username="malika_k")

    async def sign_in(self, password):
        self.passwords.append(password)


class LinkFlowTests(TransactionTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = override_settings(TELEGRAM_SESSIONS_DIR=self.tmp.name)
        patcher.enable()
        self.addCleanup(patcher.disable)
        self.teacher = f.user(username="malika")
        self.account = teachers.account_of(self.teacher)

    def test_qr_scanned_after_refresh(self):
        client = FakeClient(FakeQR([asyncio.TimeoutError(), None]))
        teachers.run_link(self.account.pk, client_factory=lambda: client)
        self.account.refresh_from_db()
        self.assertTrue(self.account.is_linked)
        self.assertEqual((self.account.telegram_id, self.account.telegram_username), (4242, "malika_k"))
        self.assertEqual(self.account.link_status, TeacherAccount.Link.DONE)
        self.assertEqual(tg.teacher_session_path(self.teacher.pk).read_text(), "new-session")
        self.assertEqual(tg.teacher_session_path(self.teacher.pk).stat().st_mode & 0o777, 0o600)

    def test_two_step_password(self):
        from telethon import errors

        client = FakeClient(FakeQR([errors.SessionPasswordNeededError(request=None)]))
        TeacherAccount.objects.filter(pk=self.account.pk).update(link_password="sir")
        teachers.run_link(self.account.pk, client_factory=lambda: client)
        self.account.refresh_from_db()
        self.assertEqual(client.passwords, ["sir"])
        self.assertTrue(self.account.is_linked)
        self.assertEqual(self.account.link_password, "")  # parol saqlanib qolmaydi

    def test_error_is_shown(self):
        class Broken(FakeClient):
            async def qr_login(self):
                raise ConnectionError

        teachers.run_link(self.account.pk, client_factory=lambda: Broken(None))
        self.account.refresh_from_db()
        self.assertEqual(self.account.link_status, TeacherAccount.Link.ERROR)
        self.assertIn("ulanib bo‘lmadi", self.account.link_error)
        self.assertFalse(self.account.is_linked)
