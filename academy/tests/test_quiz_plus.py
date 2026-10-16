import shutil
import tempfile
from datetime import timedelta
from io import StringIO
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy import telegram_sender as tg
from academy.automation import send_scheduled
from academy.models import Question, Quiz, QuizAttempt, QuizBatch
from academy.motivation import group_rank, leaderboard_text, weekly_leaderboard
from academy.services import create_quiz_batch, parse_quiz, question_quality

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 7))
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64


def finish(attempt, correct: int):
    attempt.start(f"k{attempt.pk}")
    attempt.refresh_from_db()
    answers = {}
    for i, q in enumerate(attempt.questions().prefetch_related("choices")):
        answers[str(q.pk)] = q.choices.get(is_correct=i < correct).pk
    attempt.finish(answers)
    return attempt


def ok_results(items, **kw):
    return [tg.Result(i.key, True) for i in items]


class Base(TestCase):
    def setUp(self):
        self.group = f.group(name="S-009 · Starter", code="S-009")
        self.ali = f.student(self.group, full_name="Ali Valiyev", telegram="ali_v")
        self.bek = f.student(self.group, full_name="Bek Toshev", telegram="bek_t")
        self.topic = f.topic(title="Sikllar")
        self.quiz = Quiz.objects.create(topic=self.topic)
        self.quiz.replace_questions(parse_quiz(TEXT)[0])
        self.client.force_login(f.user(first_name="Oktam", last_name="Mustafoyev"))

    def batch(self, students=None, **kw):
        return create_quiz_batch(self.quiz, students or [self.ali, self.bek], 6, 10, **kw)


class LeaveTrackingTests(Base):
    def test_leaves_recorded_monotonic_and_shown(self):
        attempt = self.batch([self.ali]).attempts.get()
        student = self.client_class()
        url = attempt.get_absolute_url()
        self.assertContains(student.get(url), "boshqa oyna yoki ilovaga o‘tish qayd qilinadi")
        student.post(url)
        save = reverse("quiz_save", args=[attempt.token])
        student.post(save, {"leave_count": "3", "away_seconds": "40"})
        student.post(save, {"leave_count": "1", "away_seconds": "5"})  # kamaytirib bo'lmaydi
        attempt.refresh_from_db()
        self.assertEqual((attempt.leave_count, attempt.away_seconds), (3, 40))
        student.post(reverse("quiz_submit", args=[attempt.token]), {"leave_count": "4", "away_seconds": "99999"})
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, "finished")
        self.assertEqual((attempt.leave_count, attempt.away_seconds), (4, 600))  # vaqt chegarasi
        review = self.client.get(reverse("quiz_attempt_review", args=[attempt.pk]))
        self.assertContains(review, "4 marta boshqa oyna yoki ilovaga o‘tgan")
        self.assertContains(self.client.get(attempt.batch.get_absolute_url()), "⚠️ 4")

    def test_take_page_has_hidden_fields(self):
        attempt = self.batch([self.ali]).attempts.get()
        student = self.client_class()
        student.post(attempt.get_absolute_url())
        page = student.get(attempt.get_absolute_url())
        self.assertContains(page, 'name="leave_count"')
        self.assertContains(page, "data-quiz-leave-notice")


@mock.patch("academy.telegram_sender.is_configured", return_value=True)
@mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
class RetakeTests(Base):
    def test_retake_only_weak_students(self, send, _):
        b = self.batch()
        finish(b.attempts.get(student=self.ali), 6)
        finish(b.attempts.get(student=self.bek), 2)
        page = self.client.get(b.get_absolute_url())
        self.assertContains(page, "Qayta topshirish (1)")
        response = self.client.post(reverse("quiz_batch_retake", args=[b.pk]))
        retake = QuizBatch.objects.exclude(pk=b.pk).get()
        self.assertRedirects(response, retake.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(retake.retake_of, b)
        self.assertEqual([a.student for a in retake.attempts.all()], [self.bek])
        self.assertEqual((retake.question_count, retake.time_limit_minutes), (6, 10))
        self.assertEqual(len(send.call_args.args[0]), 1)

    def test_nobody_weak(self, send, _):
        b = self.batch([self.ali])
        finish(b.attempts.get(), 6)
        self.client.post(reverse("quiz_batch_retake", args=[b.pk]))
        self.assertEqual(QuizBatch.objects.count(), 1)


class QualityTests(Base):
    def test_hard_and_easy_flags(self):
        students = [f.student(self.group) for _ in range(5)]
        b = self.batch(students)
        for a in b.attempts.all():
            a.start(f"k{a.pk}")
            a.refresh_from_db()
            answers = {}
            for q in a.questions().prefetch_related("choices"):
                n = int(q.text.split()[-1])
                # 1-savol — hamma xato (qiyin), 2-savol — hamma to'g'ri (oson), qolgani yarim.
                good = n == 2 or (n > 2 and a.student_id % 2)
                answers[str(q.pk)] = q.choices.get(is_correct=good).pk
            a.finish(answers)
        flags = {r["question"].title: r["flag"] for r in question_quality(self.quiz)}
        self.assertEqual(flags["Savol 1"], "hard")
        self.assertEqual(flags["Savol 2"], "easy")
        page = self.client.get(reverse("quiz_edit", args=[self.topic.pk]))
        self.assertContains(page, "Juda qiyin — matnini tekshiring")
        self.assertContains(page, "1 ta juda qiyin")
        self.assertContains(self.client.get(self.topic.get_absolute_url()), "1 ta savol juda qiyin")

    def test_not_enough_answers_no_flag(self):
        b = self.batch([self.ali])
        finish(b.attempts.get(), 0)
        self.assertTrue(all(r["flag"] == "" for r in question_quality(self.quiz)))


class ImageTests(Base):
    def setUp(self):
        super().setUp()
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.question = self.quiz.questions.first()
        self.url = reverse("quiz_question_image", args=[self.question.pk])

    def upload(self, content, name="rasm.png"):
        return self.client.post(self.url, {"image": SimpleUploadedFile(name, content)})

    def test_upload_show_and_remove(self):
        self.upload(PNG)
        self.question.refresh_from_db()
        self.assertTrue(self.question.image.name.startswith("quiz/"))
        self.assertTrue(self.question.image.name.endswith(".png"))
        media = self.client_class().get(self.question.image.url)  # login'siz
        self.assertEqual(media.status_code, 200)
        self.assertEqual(b"".join(media.streaming_content)[:8], PNG[:8])
        self.assertContains(self.client.get(reverse("quiz_edit", args=[self.topic.pk])), self.question.image.url)
        # Test sahifasida va javoblar nusxasida rasm bor.
        attempt = create_quiz_batch(self.quiz, [self.ali], 6, 10).attempts.get()
        student = self.client_class()
        student.post(attempt.get_absolute_url())
        self.assertContains(student.get(attempt.get_absolute_url()), self.question.image.url)
        student.post(reverse("quiz_submit", args=[attempt.token]), {})
        attempt.refresh_from_db()
        self.assertIn(self.question.image.url, [i["image"] for i in attempt.snapshot])
        self.client.post(self.url, {"action": "remove"})
        self.question.refresh_from_db()
        self.assertFalse(self.question.image)

    def test_rejects_non_images_and_big_files(self):
        self.upload(b"<script>alert(1)</script>", name="rasm.png")
        self.question.refresh_from_db()
        self.assertFalse(self.question.image)
        with override_settings(QUIZ_IMAGE_MAX_BYTES=10):
            self.upload(PNG)
        self.question.refresh_from_db()
        self.assertFalse(self.question.image)

    def test_media_only_quiz_folder(self):
        self.assertEqual(self.client.get("/media/../db.sqlite3").status_code, 404)
        self.assertEqual(self.client.get("/media/boshqa/fayl.txt").status_code, 404)


@override_settings(SITE_URL="https://darsxona.test")
class ScheduleTests(Base):
    def post_send(self, when):
        return self.client.post(
            f"{reverse('quiz_send')}?topic={self.topic.pk}&group={self.group.pk}",
            {"students": [self.ali.pk], "question_count": 6, "time_limit_minutes": 10, "scheduled_at": when},
        )

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_scheduled_send_waits_then_sends(self, send, _):
        when = timezone.localtime() + timedelta(hours=2)
        self.post_send(when.strftime("%Y-%m-%dT%H:%M"))
        batch = QuizBatch.objects.get()
        self.assertIsNotNone(batch.scheduled_at)
        send.assert_not_called()
        self.assertContains(self.client.get(batch.get_absolute_url()), "da avtomatik yuboriladi")
        self.assertEqual(send_scheduled(now=timezone.now()).sent, 0)  # hali erta
        result = send_scheduled(now=timezone.now() + timedelta(hours=3), sender=ok_results)
        self.assertEqual(result.sent, 1)
        batch.refresh_from_db()
        self.assertIsNotNone(batch.scheduled_sent_at)
        self.assertIsNotNone(batch.attempts.get().sent_at)

    def test_past_time_rejected(self):
        response = self.post_send((timezone.localtime() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"))
        self.assertContains(response, "Kelajakdagi vaqtni tanlang", status_code=200)
        self.assertFalse(QuizBatch.objects.exists())

    @mock.patch("academy.telegram_sender.is_configured", return_value=True)
    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_manual_send_cancels_schedule(self, send, _):
        b = self.batch([self.ali])
        QuizBatch.objects.filter(pk=b.pk).update(scheduled_at=timezone.now() + timedelta(hours=1))
        self.client.post(reverse("quiz_batch_send", args=[b.pk]))
        b.refresh_from_db()
        self.assertIsNotNone(b.scheduled_sent_at)
        self.assertEqual(send_scheduled(now=timezone.now() + timedelta(hours=2), sender=ok_results).sent, 0)


class LeaderboardTests(Base):
    def test_board_text_and_send(self):
        b = self.batch()
        finish(b.attempts.get(student=self.ali), 6)
        finish(b.attempts.get(student=self.bek), 3)
        board = weekly_leaderboard(self.group)
        self.assertEqual([(r.student, r.pct) for r in board["rows"]], [(self.ali, 100), (self.bek, 50)])
        text = leaderboard_text(self.group, board)
        self.assertIn("🥇 Ali Valiyev — 100% (1 ta test)", text)
        self.assertIn("🥈 Bek Toshev — 50%", text)
        self.assertEqual(group_rank(self.bek), (2, 2))

        url = reverse("group_leaderboard_send", args=[self.group.pk])
        self.client.post(url)  # chat tanlanmagan
        self.group.telegram_chat = "@s009_chat"
        self.group.save()
        with mock.patch("academy.telegram_sender.send_to_chat") as send:
            self.client.post(url)
        self.assertEqual(send.call_args.args[0], "@s009_chat")
        page = self.client.get(self.group.get_absolute_url())
        self.assertContains(page, "Haftalik reyting")
        out = StringIO()
        call_command("weekly_leaderboard", "--dry-run", stdout=out)
        self.assertIn("🥇 Ali Valiyev", out.getvalue())

    def test_old_results_ignored_and_chat_refs(self):
        b = self.batch([self.ali])
        a = finish(b.attempts.get(), 6)
        QuizAttempt.objects.filter(pk=a.pk).update(finished_at=timezone.now() - timedelta(days=10))
        self.assertEqual(leaderboard_text(self.group, weekly_leaderboard(self.group)), "")
        self.assertEqual(tg.chat_ref("https://t.me/s009_chat"), "s009_chat")
        self.assertEqual(tg.chat_ref("-1001234567890"), -1001234567890)

    def test_choose_chat_page(self):
        chats = [{"id": -100123456789, "title": "S-009 guruhi", "username": ""}]
        with mock.patch("academy.telegram_sender.list_chats", return_value=chats):
            page = self.client.get(reverse("group_telegram_chat", args=[self.group.pk]))
        self.assertContains(page, "S-009 guruhi")
        self.client.post(reverse("group_telegram_chat", args=[self.group.pk]), {"chat": "-100123456789"})
        self.group.refresh_from_db()
        self.assertEqual(self.group.telegram_chat, "-100123456789")


class PortalTests(Base):
    def test_portal_shows_progress_without_correct_answers(self):
        b = self.batch()
        finish(b.attempts.get(student=self.ali), 4)
        finish(b.attempts.get(student=self.bek), 6)
        self.batch([self.ali])  # ochilmagan test
        detail = self.client.get(self.ali.get_absolute_url())
        self.ali.refresh_from_db()
        self.assertTrue(self.ali.portal_token)
        url = reverse("student_portal", args=[self.ali.portal_token])
        self.assertContains(detail, url)
        page = self.client_class().get(url)  # login'siz
        self.assertContains(page, "Ali Valiyev")
        self.assertContains(page, "67%")  # 4/6
        self.assertContains(page, "2<small>/2</small>")  # guruhda 2-o'rin
        self.assertContains(page, "Yechilmagan testlar")
        self.assertContains(page, "Javobingiz: <strong>xato 5</strong>")
        self.assertNotContains(page, "to'g'ri 5")  # xato javobda to'g'ri variant ko'rinmaydi
        self.assertEqual(self.client_class().get(reverse("student_portal", args=["yoq"])).status_code, 404)

    @mock.patch("academy.telegram_sender.send_messages", side_effect=ok_results)
    def test_send_and_reset(self, send):
        self.client.get(self.ali.get_absolute_url())
        self.ali.refresh_from_db()
        old = self.ali.portal_token
        self.client.post(reverse("student_portal_action", args=[self.ali.pk]), {"action": "send"})
        self.assertIn(f"/men/{old}/", send.call_args.args[0][0].text)
        self.client.post(reverse("student_portal_action", args=[self.ali.pk]), {"action": "reset"})
        self.ali.refresh_from_db()
        self.assertNotEqual(self.ali.portal_token, old)
        self.client.post(reverse("group_portal_send", args=[self.group.pk]))
        self.assertEqual(len(send.call_args.args[0]), 2)


class CertificateTests(Base):
    def test_pdf(self):
        b = self.batch([self.ali])
        finish(b.attempts.get(), 5)
        response = self.client.get(reverse("student_certificate", args=[self.ali.pk]), {"kurs": "Python asoslari"})
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))
        self.assertGreater(len(response.content), 5000)
        self.assertIn("inline", response["Content-Disposition"])
        response = self.client.post(reverse("student_certificate", args=[self.ali.pk]), {"yuklab": "1"})
        self.assertIn('attachment; filename="sertifikat-Ali-Valiyev.pdf"', response["Content-Disposition"])
        self.assertContains(self.client.get(self.ali.get_absolute_url()), 'value="Starter"')

    def test_send_via_telegram(self):
        with mock.patch("academy.telegram_sender.send_file_to") as send:
            self.client.post(reverse("student_certificate_send", args=[self.ali.pk]), {"kurs": "Starter"})
        item, path = send.call_args.args
        self.assertEqual(item.username, "ali_v")
        self.assertIn("Starter", send.call_args.kwargs["caption"])
        self.assertTrue(str(path).endswith(".pdf"))

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse("student_certificate", args=[self.ali.pk])).status_code, 302)


class QuestionImageCopyTests(Base):
    def test_question_has_image_field(self):
        q = Question.objects.first()
        self.assertFalse(q.image)
