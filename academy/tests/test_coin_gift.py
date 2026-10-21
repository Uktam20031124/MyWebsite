from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import override

from academy import coins
from academy.models import CoinTransaction

from . import factories as f


class CoinGiftTests(TestCase):
    def setUp(self):
        self.ali = f.student(full_name="Ibrahimov Muxammadali")
        self.client.force_login(f.user())
        self.url = reverse("student_coin_gift", args=[self.ali.pk])

    def gift(self, amount, nonce="n1", **extra):
        return self.client.post(self.url, {"amount": amount, "nonce": nonce, **extra})

    def test_gift_adds_coins_and_shows_in_history(self):
        page = self.client.get(self.ali.get_absolute_url())
        self.assertContains(page, "Quvvat sovg‘a qilish")
        self.assertContains(page, 'name="nonce"')
        response = self.gift(300, note="  olimpiada   uchun ")
        self.assertRedirects(response, f"{self.ali.get_absolute_url()}#coins", fetch_redirect_response=False)
        self.assertEqual(coins.balance(self.ali), 300)
        tx = CoinTransaction.objects.get()
        self.assertEqual(tx.reason, "🎁 Ustozdan sovg‘a: olimpiada uchun")
        self.assertTrue(tx.is_gift and tx.can_undo)
        self.assertContains(self.client.get(self.ali.get_absolute_url()), "🎁 Ustozdan sovg‘a: olimpiada uchun")

    def test_same_form_twice_gives_once(self):
        self.gift(300, nonce="abc")
        self.gift(300, nonce="abc")  # ikki marta bosish / qayta yuborish
        self.assertEqual(coins.balance(self.ali), 300)
        self.gift(50, nonce="xyz")
        self.assertEqual(coins.balance(self.ali), 350)

    def test_bad_amount_or_missing_nonce_rejected(self):
        for amount in ["0", "-5", "abc", str(coins.GIFT_MAX + 1)]:
            self.gift(amount, nonce=f"n{amount}")
        self.client.post(self.url, {"amount": 10})  # kalitsiz
        self.assertEqual(coins.balance(self.ali), 0)

    def test_quick_gift_from_list_returns_to_list(self):
        back = reverse("student_list") + "?q=Ibrahimov"
        page = self.client.get(back)
        self.assertContains(page, 'name="amount" value="50"')
        response = self.gift(50, next=back)
        self.assertRedirects(response, back, fetch_redirect_response=False)

    def test_undo_recent_gift_only(self):
        self.gift(300)
        tx = CoinTransaction.objects.get()
        undo = reverse("student_coin_undo", args=[self.ali.pk, tx.pk])
        self.client.post(undo)
        self.assertEqual(coins.balance(self.ali), 0)
        # 24 soatdan eski sovg'a bekor qilinmaydi
        old = coins.gift(self.ali, 100)
        CoinTransaction.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(hours=25))
        self.client.post(reverse("student_coin_undo", args=[self.ali.pk, old.pk]))
        self.assertEqual(coins.balance(self.ali), 100)
        # test coinini bekor qilib bo'lmaydi
        earned = CoinTransaction.objects.create(student=self.ali, amount=10, reason="Test: 95%")
        self.client.post(reverse("student_coin_undo", args=[self.ali.pk, earned.pk]))
        self.assertTrue(CoinTransaction.objects.filter(pk=earned.pk).exists())

    def test_requires_login(self):
        Client().post(self.url, {"amount": 100, "nonce": "z"})
        self.assertEqual(coins.balance(self.ali), 0)

    def test_reason_translated(self):
        tx = coins.gift(self.ali, 10, "olimpiada")
        with override("ru"):
            self.assertEqual(tx.display_reason, "🎁 Подарок от учителя: olimpiada")
