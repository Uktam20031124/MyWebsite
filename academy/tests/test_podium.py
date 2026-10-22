from django.test import TestCase
from django.urls import reverse

from academy import coins, engagement
from academy.templatetags.ui import person_name

from . import factories as f


class PodiumTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.a, self.b, self.c, self.d, self.e = (
            f.student(self.group, full_name=n) for n in ("Ali", "Bek", "Dil", "Eli", "Zuh")
        )
        for s, amount in ((self.a, 50), (self.b, 30), (self.c, 30), (self.d, 10)):
            coins.gift(s, amount)
        self.other = f.student(f.group(), full_name="Boshqa")
        coins.gift(self.other, 5)

    def test_places_per_group_with_ties(self):
        places = engagement.podium_places()
        self.assertEqual(places[self.a.pk], 1)
        self.assertEqual(places[self.b.pk], 2)
        self.assertEqual(places[self.c.pk], 2)  # teng balans — bir xil o'rin
        self.assertNotIn(self.d.pk, places)  # 4-o'rin
        self.assertNotIn(self.e.pk, places)  # 0 ⚡️ — o'rin yo'q
        self.assertEqual(places[self.other.pk], 1)  # har guruh alohida
        board = {r["student"].pk: r["place"] for r in engagement.quvvat_board(self.group.pk)}
        self.assertTrue(all(board[pk] == p for pk, p in places.items() if pk in board))  # reyting bilan bir xil

    def test_person_name_colors(self):
        self.assertIn('class="podium-name podium-1"', person_name(self.a))
        self.assertIn("podium-2", person_name(self.b))
        self.assertEqual(person_name(self.d), "Eli")
        self.assertIn("podium-1", person_name({"id": self.a.pk, "full_name": "Ali"}))

    def test_cache_refreshes_when_quvvat_changes(self):
        self.assertNotIn(self.d.pk, engagement.podium_places())
        coins.gift(self.d, 100)
        self.assertEqual(engagement.podium_places()[self.d.pk], 1)
        self.assertEqual(engagement.podium_places()[self.a.pk], 2)

    def test_shown_on_pages(self):
        self.client.force_login(f.user())
        page = self.client.get(reverse("student_list"))
        self.assertContains(page, 'class="podium-name podium-1"')
        self.assertContains(page, "podium-2")
