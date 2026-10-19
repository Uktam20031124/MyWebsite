from types import SimpleNamespace
from unittest import mock

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from telethon import errors

from academy import telegram_sender as tg
from academy.models import Quiz, QuizAttempt, QuizBatch
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f
from .test_quiz import QUIZ_TEXT

SENDER = 7730996406


class FakeClient:
    """Telethon TelegramClient'ning yuborish uchun kerakli qismi."""

    def __init__(self, me_id=SENDER, authorized=True, flood=None, unknown=()):
        self.me_id, self.authorized, self.flood, self.unknown = me_id, authorized, flood, set(unknown)
        self.sent = []

    async def connect(self):
        self.connected = True

    async def disconnect(self):
        self.connected = False

    async def is_user_authorized(self):
        return self.authorized

    async def get_me(self):
        return SimpleNamespace(id=self.me_id, first_name="Ustoz", last_name="", username="ustoz")

    async def get_input_entity(self, username):
        if username in self.unknown:
            raise errors.UsernameNotOccupiedError(request=None)
        return f"user:{username}"

    async def __call__(self, request):  # ImportContactsRequest
        phone = request.contacts[0].phone
        users = [] if phone in self.unknown else [f"phone:{phone}"]
        return SimpleNamespace(users=users)

    async def send_message(self, entity, text, link_preview=True):
        if self.flood:
            seconds, self.flood = self.flood, None
            raise errors.FloodWaitError(request=None, capture=seconds)
        self.sent.append((entity, text))


def item(key, username="", phone=""):
    return tg.Outgoing(key=key, username=username, phone=phone, first_name="Ali", text=f"t{key}")


@override_settings(TELEGRAM_SENDER_ID=SENDER)
class SenderTests(SimpleTestCase):
    def send(self, items, client):
        with mock.patch("asyncio.sleep", new=mock.AsyncMock()):
            return tg.send_messages(items, client_factory=lambda: client, delay=0)

    def test_normalizers(self):
        self.assertEqual(tg.normalize_username("@ali_01"), "ali_01")
        self.assertEqual(tg.normalize_username("https://t.me/Sardor_x"), "Sardor_x")
        self.assertEqual(tg.normalize_username("12ab"), "")
        self.assertEqual(tg.normalize_phone("90 123 45 67"), "+998901234567")
        self.assertEqual(tg.normalize_phone("+998 (90) 123-45-67"), "+998901234567")
        self.assertEqual(tg.normalize_phone("123"), "")

    def test_sends_by_username_and_phone(self):
        client = FakeClient()
        results = self.send([item(1, username="ali"), item(2, phone="+998901234567")], client)
        self.assertEqual([r.ok for r in results], [True, True])
        self.assertEqual(client.sent, [("user:ali", "t1"), ("phone:+998901234567", "t2")])

    def test_only_allowed_account_can_send(self):
        client = FakeClient(me_id=111)
        with self.assertRaisesMessage(tg.TelegramError, "7730996406"):
            self.send([item(1, username="ali")], client)
        self.assertEqual(client.sent, [])

    def test_expired_session(self):
        with self.assertRaisesMessage(tg.TelegramError, "eskirgan"):
            self.send([item(1, username="ali")], FakeClient(authorized=False))

    def test_per_student_errors(self):
        client = FakeClient(unknown={"yoq", "+998900000000"})
        results = self.send(
            [item(1), item(2, username="yoq"), item(3, phone="+998900000000"), item(4, username="ok")],
            client,
        )
        self.assertEqual([r.ok for r in results], [False, False, False, True])
        self.assertIn("username ham, telefon ham yo‘q", results[0].error)
        self.assertIn("username topilmadi", results[1].error)
        self.assertIn("Telegram yo‘q", results[2].error)

    def test_short_flood_wait_is_retried_long_stops(self):
        client = FakeClient(flood=5)
        self.assertTrue(self.send([item(1, username="ali")], client)[0].ok)
        client = FakeClient(flood=600)
        results = self.send([item(1, username="ali"), item(2, username="vali")], client)
        self.assertEqual([r.ok for r in results], [False, False])
        self.assertIn("600 soniyadan", results[1].error)

    @override_settings(TELEGRAM_API_ID=0, TELEGRAM_API_HASH="")
    def test_not_configured(self):
        self.assertFalse(tg.is_configured())
        with self.assertRaisesMessage(tg.TelegramError, "TELEGRAM_API_ID"):
            tg.send_messages([item(1, username="ali")])


def ok_results(items, **kwargs):
    return [tg.Result(i.key, bool(i.username or i.phone), "" if i.username or i.phone else "yo‘q") for i in items]


class TelegramViewTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.group = f.group()
        self.ali = f.student(self.group, full_name="Ali Valiyev", telegram="@ali_v")
        self.nocontact = f.student(self.group, full_name="Kontaktsiz")
        self.topic = f.topic(title="Sikllar")
        quiz = Quiz.objects.create(topic=self.topic)
        quiz.replace_questions(parse_quiz(QUIZ_TEXT)[0])
        self.quiz = quiz

    def post_send(self):
        return self.client.post(
            f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}",
            {
                "students": [self.ali.pk, self.nocontact.pk],
                "question_count": 3,
                "time_limit_minutes": 5,
                "channels": ["telegram"],
            },
        )

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_send_flow_delivers_via_telegram(self, send, _):
        response = self.post_send()
        batch = QuizBatch.objects.get()
        self.assertRedirects(response, batch.get_absolute_url(), fetch_redirect_response=False)
        items = send.call_args.args[0]
        ali_item = next(i for i in items if i.username)
        self.assertEqual(ali_item.username, "ali_v")
        self.assertIn("Salom, Ali Valiyev!", ali_item.text)
        self.assertIn("3 ta savol, 5 daqiqa", ali_item.text)
        self.assertIn("http://testserver/t/", ali_item.text)
        ali = QuizAttempt.objects.get(student=self.ali)
        other = QuizAttempt.objects.get(student=self.nocontact)
        self.assertIsNotNone(ali.sent_at)
        self.assertIsNone(other.sent_at)
        self.assertTrue(other.send_error)
        page = self.client.get(batch.get_absolute_url())
        self.assertContains(page, "Yuborildi ·")
        self.assertContains(page, "Telegram username / telefon yo‘q")
        self.assertNotContains(page, "t.me/share")
        self.assertNotContains(page, "data-copy")

    @mock.patch("academy.telegram_sender.is_configured", return_value=False)
    @mock.patch("academy.telegram_sender.send_messages")
    def test_not_configured_shows_setup_and_sends_nothing(self, send, _):
        self.post_send()
        send.assert_not_called()
        page = self.client.get(QuizBatch.objects.get().get_absolute_url())
        self.assertContains(page, "Telegram ulanmagan")
        self.assertContains(page, "7730996406")
        self.assertNotContains(page, "t.me/share")

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch(
        "academy.telegram_sender.send_messages",
        side_effect=tg.TelegramError("Ulangan akkaunt (1) ruxsat etilganidan (7730996406) farq qiladi"),
    )
    def test_wrong_account_error_is_shown(self, send, _):
        batch = create_quiz_batch(self.quiz, [self.ali], 3, 5)
        response = self.client.post(reverse("quiz_batch_send", args=[batch.pk]), follow=True)
        self.assertContains(response, "farq qiladi")
        self.assertIsNone(batch.attempts.get().sent_at)

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_send_all_unsent_and_resend_one(self, send, _):
        batch = create_quiz_batch(self.quiz, [self.ali, self.nocontact], 3, 5)
        url = reverse("quiz_batch_send", args=[batch.pk])
        self.client.post(url)
        self.assertEqual(len(send.call_args.args[0]), 2)
        ali = batch.attempts.get(student=self.ali)
        self.assertIsNotNone(ali.sent_at)
        # Yuborilganlarga "hammasiga" qayta ketmaydi; bittasini qayta yuborish mumkin.
        self.client.post(url)
        self.assertEqual([i.key for i in send.call_args.args[0]], [batch.attempts.get(student=self.nocontact).pk])
        self.client.post(url, {"attempt": ali.pk})
        self.assertEqual([i.key for i in send.call_args.args[0]], [ali.pk])

    def test_renew_clears_sent_state(self):
        batch = create_quiz_batch(self.quiz, [self.ali], 3, 5)
        attempt = batch.attempts.get()
        QuizAttempt.objects.filter(pk=attempt.pk).update(sent_at="2026-10-15T10:00:00Z")
        self.client.post(reverse("quiz_attempt_renew", args=[attempt.pk]))
        attempt.refresh_from_db()
        self.assertIsNone(attempt.sent_at)


class FakeLoginClient(FakeClient):
    """telegram_login uchun: kod yuborish, kirish va sessiya."""

    def __init__(self, session="", me_id=SENDER, needs_password=False):
        super().__init__(me_id=me_id)
        self.session = SimpleNamespace(save=lambda: f"session-{session or 'new'}")
        self.needs_password = needs_password
        self.logged_out = False

    async def send_code_request(self, phone):
        return SimpleNamespace(phone_code_hash="hash123")

    async def sign_in(self, phone=None, code=None, phone_code_hash=None, password=None):
        if code and self.needs_password:
            raise errors.SessionPasswordNeededError(request=None)
        if code and (code != "12345" or phone_code_hash != "hash123"):
            raise errors.PhoneCodeInvalidError(request=None)

    async def log_out(self):
        self.logged_out = True


class LoginCommandTests(SimpleTestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path

        self.tmp = Path(tempfile.mkdtemp())
        self.settings = override_settings(
            TELEGRAM_API_ID=1, TELEGRAM_API_HASH="x", TELEGRAM_SENDER_ID=SENDER,
            TELEGRAM_SESSION_FILE=self.tmp / "session",
        )
        self.settings.enable()
        self.addCleanup(self.settings.disable)

    def run_cmd(self, client, *args):
        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        with mock.patch("academy.telegram_sender.make_client", return_value=client):
            call_command("telegram_login", *args, stdout=out)
        return out.getvalue()

    def test_two_step_login_saves_session_for_allowed_account(self):
        out = self.run_cmd(FakeLoginClient(), "--phone", "90 123 45 67")
        self.assertIn("+998901234567", out)
        self.assertFalse(tg.is_configured())
        out = self.run_cmd(FakeLoginClient(session="pending"), "--code", "12345")
        self.assertIn("Ulandi", out)
        self.assertEqual(tg.load_session(), "session-pending")
        self.assertTrue(tg.is_configured())
        self.assertFalse((self.tmp / "session.pending").exists())
        self.assertEqual((self.tmp / "session").stat().st_mode & 0o777, 0o600)

    def test_other_account_is_rejected(self):
        from django.core.management import CommandError

        self.run_cmd(FakeLoginClient(), "--phone", "+998901234567")
        client = FakeLoginClient(me_id=42)
        with self.assertRaisesMessage(CommandError, "ruxsat etilmagan"):
            self.run_cmd(client, "--code", "12345")
        self.assertTrue(client.logged_out)
        self.assertEqual(tg.load_session(), "")

    def test_two_factor_password_step(self):
        from django.core.management import CommandError

        self.run_cmd(FakeLoginClient(), "--phone", "+998901234567")
        with self.assertRaisesMessage(CommandError, "--password"):
            self.run_cmd(FakeLoginClient(needs_password=True), "--code", "12345")
        out = self.run_cmd(FakeLoginClient(session="2fa"), "--password", "sir")
        self.assertIn("Ulandi", out)
        self.assertEqual(tg.load_session(), "session-2fa")

    def test_wrong_code(self):
        from django.core.management import CommandError

        self.run_cmd(FakeLoginClient(), "--phone", "+998901234567")
        with self.assertRaisesMessage(CommandError, "Kod noto'g'ri"):
            self.run_cmd(FakeLoginClient(), "--code", "00000")


class FakeQR:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)  # "timeout" | "ok" | "password"
        self.url = "tg://login?token=abc"
        self.recreated = 0

    async def wait(self, timeout=None):
        import asyncio

        outcome = self.outcomes.pop(0)
        if outcome == "timeout":
            raise asyncio.TimeoutError
        if outcome == "password":
            raise errors.SessionPasswordNeededError(request=None)

    async def recreate(self):
        self.recreated += 1
        self.url = f"tg://login?token=new{self.recreated}"


class QrLoginTests(LoginCommandTests):
    def qr_client(self, outcomes, **kwargs):
        client = FakeLoginClient(**kwargs)
        client.qr = FakeQR(outcomes)

        async def qr_login():
            return client.qr

        client.qr_login = qr_login
        return client

    def test_qr_login_refreshes_expired_code(self):
        client = self.qr_client(["timeout", "ok"], session="qr")
        out = self.run_cmd(client, "--qr")
        self.assertEqual(client.qr.recreated, 1)
        self.assertIn("Kompyuterni ulash", out)
        self.assertIn("Ulandi", out)
        self.assertEqual(tg.load_session(), "session-qr")

    def test_qr_login_with_two_factor(self):
        from django.core.management import CommandError

        with self.assertRaisesMessage(CommandError, "--password"):
            self.run_cmd(self.qr_client(["password"]), "--qr")
        out = self.run_cmd(FakeLoginClient(session="2fa"), "--password", "sir")
        self.assertIn("Ulandi", out)
        out = self.run_cmd(self.qr_client(["password"], session="direct"), "--qr", "--password", "sir")
        self.assertEqual(tg.load_session(), "session-direct")

    def test_qr_other_account_rejected(self):
        from django.core.management import CommandError

        client = self.qr_client(["ok"], me_id=42)
        with self.assertRaisesMessage(CommandError, "ruxsat etilmagan"):
            self.run_cmd(client, "--qr")
        self.assertEqual(tg.load_session(), "")
