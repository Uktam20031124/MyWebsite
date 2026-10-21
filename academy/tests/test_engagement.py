from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import coins, engagement, profiles
from academy.models import CoinTransaction, DailyActivity, Mistake, Purchase, Quiz, Reward
from academy.services import create_quiz_batch, parse_quiz

from . import factories as f

TEXT = "\n\n".join(f"? Savol {i}\n+ to'g'ri {i}\n- xato {i}" for i in range(1, 13))


def solve(attempt, right: int):
    """Birinchi `right` ta savolga to'g'ri, qolganlariga xato javob."""
    attempt.start("k")
    attempt.refresh_from_db()
    qs = list(attempt.questions().order_by("pk"))
    answers = {str(q.pk): q.choices.get(is_correct=i < right).pk for i, q in enumerate(qs)}
    attempt.finish(answers)
    attempt.refresh_from_db()
    return attempt


@mock.patch("academy.profiles.notify")
class EngagementTests(TestCase):
    def setUp(self):
        self.group = f.group(code="P-1")
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        self.vali = f.student(self.group, full_name="Vali Karimov")
        self.quiz = Quiz.objects.create(topic=f.topic(title="Sikllar"))
        self.quiz.replace_questions(parse_quiz(TEXT)[0])
        self.teacher = self.client_class()
        self.teacher.force_login(f.user())
        self.teacher.get(self.ali.get_absolute_url())
        self.ali.refresh_from_db()
        self.token = self.ali.portal_token
        profiles.grant_access(self.ali, 2)

    def attempt(self, student=None, n=10):
        return create_quiz_batch(self.quiz, [student or self.ali], n, 10).attempts.get()

    # --- Xatolar ustida ishlash ---------------------------------------------------

    def test_wrong_answers_become_mistakes_and_practice_fixes_them(self, notify):
        solve(self.attempt(), right=7)  # 3 ta xato
        self.assertEqual(engagement.open_mistakes(self.ali).count(), 3)
        page = self.client.get(reverse("student_portal", args=[self.token]))
        self.assertContains(page, "Mashqni boshlash")
        url = reverse("portal_practice", args=[self.token])
        practice = self.client.get(url)
        self.assertContains(practice, "Qoldi: <strong>3</strong>")
        m = engagement.next_mistake(self.ali)
        right = m.question.choices.get(is_correct=True)
        wrong = m.question.choices.get(is_correct=False)
        # To'g'ri variant sahifada ajratib ko'rsatilmaydi (ikkalasi ham oddiy variant).
        self.assertContains(practice, f'value="{right.pk}"')
        self.client.post(url, {"mistake": m.pk, "choice": right.pk})
        self.assertContains(self.client.get(url), "To‘g‘ri!")
        self.client.post(url, {"mistake": m.pk, "choice": wrong.pk})  # xato — ketma-ketlik nollanadi
        self.assertContains(self.client.get(url), "Xato.")
        m.refresh_from_db()
        self.assertEqual(m.streak, 0)
        before = coins.balance(self.ali)
        for _ in range(3):
            self.client.post(url, {"mistake": m.pk, "choice": right.pk})
        m.refresh_from_db()
        self.assertIsNotNone(m.resolved_at)
        self.assertEqual(coins.balance(self.ali), before + engagement.MISTAKE_FIXED_COINS)
        self.assertEqual(engagement.open_mistakes(self.ali).count(), 2)
        self.assertTrue(DailyActivity.objects.filter(student=self.ali).exists())

    def test_mistakes_come_back_in_next_test(self, notify):
        solve(self.attempt(n=12), right=6)  # 6 ta xato
        mistakes = set(engagement.open_mistakes(self.ali).values_list("question_id", flat=True))
        nxt = self.attempt(n=10)
        nxt.start("k2")
        nxt.refresh_from_db()
        # Savollarning kamida yarmi (5 ta) — xato qilinganlardan; qolgani bankdan tasodifiy.
        self.assertGreaterEqual(len(mistakes & set(nxt.question_ids)), 5)

    def test_correct_in_test_counts_and_wrong_reopens(self, notify):
        first = solve(self.attempt(n=12), right=11)
        m = Mistake.objects.get(student=self.ali)
        qid = m.question_id
        # Testda shu savolga to'g'ri javob — ketma-ketlik +1.
        a = self.attempt(n=12)
        a.start("k")
        a.refresh_from_db()
        answers = {str(q.pk): q.choices.get(is_correct=True).pk for q in a.questions()}
        a.finish(answers)
        m.refresh_from_db()
        self.assertEqual(m.streak, 1)
        self.assertNotEqual(first.pk, a.pk)
        # Keyin yana xato — ochiq, ketma-ketlik 0, xato soni 2.
        b = self.attempt(n=12)
        b.start("k")
        b.refresh_from_db()
        answers = {str(q.pk): q.choices.get(is_correct=q.pk != qid).pk for q in b.questions()}
        b.finish(answers)
        m.refresh_from_db()
        self.assertEqual((m.streak, m.wrong_count, m.resolved_at), (0, 2, None))

    # --- Streak ---------------------------------------------------------------------

    def test_streak_and_weekly_bonus(self, notify):
        today = engagement.today()
        for i in range(1, 7):
            DailyActivity.objects.create(student=self.ali, day=today - timedelta(days=i))
        self.assertEqual(engagement.streak(self.ali), 6)  # bugun hali faol emas — kechagacha
        self.assertEqual(engagement.streak_info(self.ali).to_bonus, 1)
        solve(self.attempt(), right=10)  # bugun faol → 7 kun
        self.assertEqual(engagement.streak(self.ali), 7)
        self.assertTrue(CoinTransaction.objects.filter(student=self.ali, reason="🔥 7 kun ketma-ket faol").exists())
        solve(self.attempt(), right=10)  # shu kunning o'zida — bonus takrorlanmaydi
        self.assertEqual(CoinTransaction.objects.filter(reason__startswith="🔥").count(), 1)
        page = self.client.get(reverse("student_portal", args=[self.token]))
        self.assertContains(page, "🔥 7 <small>kun</small>")
        self.assertContains(page, "Bugun faolsiz")

    def test_streak_breaks_after_missed_day(self, notify):
        today = engagement.today()
        DailyActivity.objects.create(student=self.ali, day=today - timedelta(days=2))
        DailyActivity.objects.create(student=self.ali, day=today - timedelta(days=3))
        self.assertEqual(engagement.streak(self.ali), 0)

    # --- Haftalik reyting -----------------------------------------------------------

    def test_weekly_board_counts_only_this_week_earnings(self, notify):
        CoinTransaction.objects.create(student=self.ali, amount=20, reason="test")
        CoinTransaction.objects.create(student=self.vali, amount=30, reason="test")
        CoinTransaction.objects.create(student=self.vali, amount=-25, reason="Do‘kon")  # sarflash hisoblanmaydi
        old = CoinTransaction.objects.create(student=self.ali, amount=100, reason="eski")
        CoinTransaction.objects.filter(pk=old.pk).update(created_at=engagement.week_start() - timedelta(days=1))
        board = engagement.weekly_board(self.group.pk)
        self.assertEqual([(r["student"].full_name, r["coins"], r["place"]) for r in board],
                         [("Vali Karimov", 30, 1), ("Ali Valiyev", 20, 2)])
        page = self.client.get(reverse("student_portal", args=[self.token]))
        self.assertContains(page, "Haftaning eng faollari")
        self.assertContains(self.teacher.get(self.group.get_absolute_url()), "Haftaning eng faollari")

    # --- Coin do'koni ---------------------------------------------------------------

    def test_shop_flow(self, notify):
        reward = Reward.objects.create(title="Uyga vazifadan ozod", cost=50)
        Reward.objects.create(title="Yashirin", cost=1, is_active=False)
        portal = reverse("student_portal", args=[self.token])
        page = self.client.get(portal)
        self.assertContains(page, "Uyga vazifadan ozod")
        self.assertNotContains(page, "Yashirin")
        self.assertContains(page, "quvvat yetmaydi")
        buy = reverse("portal_buy", args=[self.token, reward.pk])
        self.assertContains(self.client.post(buy, follow=True), "Quvvat yetmaydi")
        CoinTransaction.objects.create(student=self.ali, amount=60, reason="test")
        self.client.post(buy)
        self.assertContains(self.client.post(buy, follow=True), "kutilmoqda")  # ikkinchi so'rov yo'q
        p = Purchase.objects.get()
        self.assertEqual(engagement.available(self.ali), 10)
        self.assertEqual(coins.balance(self.ali), 60)  # tasdiqlanmaguncha yechilmaydi
        self.assertContains(self.teacher.get(reverse("quiz_review_requests")), "Mukofot so‘rovlari")
        self.teacher.post(reverse("purchase_decide", args=[p.pk]), {"action": "approve"})
        p.refresh_from_db()
        self.assertEqual(p.status, Purchase.Status.APPROVED)
        self.assertEqual(coins.balance(self.ali), 10)
        self.assertContains(self.client.get(portal), "Berildi")
        # Teacher sahifasi
        shop = self.teacher.get(reverse("rewards"))
        self.assertContains(shop, "berilgan: 1")
        data = {"title": "Yangi", "cost": 5, "description": "", "order": 3, "is_active": "on"}
        self.teacher.post(reverse("rewards"), data)
        self.assertTrue(Reward.objects.filter(title="Yangi").exists())

    def test_reject_keeps_coins(self, notify):
        reward = Reward.objects.create(title="Sovg'a", cost=10)
        CoinTransaction.objects.create(student=self.ali, amount=10, reason="test")
        p = engagement.buy(self.ali, reward.pk)
        engagement.decide_purchase(p, False)
        self.assertEqual(coins.balance(self.ali), 10)
        self.assertEqual(engagement.available(self.ali), 10)

    def test_shop_requires_open_profile(self, notify):
        reward = Reward.objects.create(title="Sovg'a", cost=1)
        CoinTransaction.objects.create(student=self.ali, amount=5, reason="test")
        type(self.ali).objects.filter(pk=self.ali.pk).update(profile_until=timezone.now() - timedelta(minutes=1))
        self.client.post(reverse("portal_buy", args=[self.token, reward.pk]))
        self.assertFalse(Purchase.objects.exists())
