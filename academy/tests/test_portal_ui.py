"""O'quvchi profili (Ultra): bugungi reja, keyingi mukofot, yutuqlar, o'sish grafigi va sahifa."""

from datetime import timedelta
from types import SimpleNamespace

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import portal_ui
from academy.models import Reward

from . import factories as f


def streak(days=0, active=False):
    return SimpleNamespace(days=days, active_today=active, week=[])


class PortalUiTests(TestCase):
    def test_missions_pending_work_first_done_last(self):
        bonus = {"remaining": 5, "left_today": 3}
        items = portal_ui.missions(pending=[], homework_open_n=2, open_mistakes_n=0, bonus=bonus,
                                   streak=streak(active=True))
        self.assertEqual([m.key for m in items], ["homework", "bonus", "streak"])
        self.assertTrue(items[-1].done)
        none = portal_ui.missions(pending=[], homework_open_n=0, open_mistakes_n=0, bonus={}, streak=streak())
        self.assertEqual([(m.key, m.done) for m in none], [("streak", False)])

    def test_next_reward_is_cheapest_unaffordable_and_skips_owned_honor(self):
        cheap = Reward(title="A", cost=40)
        honor = Reward(title="H", cost=60, perk="honor")
        dear = Reward(title="B", cost=100)
        r = portal_ui.next_reward([cheap, honor, dear], available=50, owned_honor=True)
        self.assertEqual((r["reward"].title, r["need"], r["pct"]), ("B", 50, 50))
        self.assertIsNone(portal_ui.next_reward([cheap], available=50, owned_honor=False))

    def test_achievements_reflect_existing_stats(self):
        finished = [SimpleNamespace(percent=p) for p in (60, 85)]
        stats = SimpleNamespace(n=5)
        got = {a.title: a.got for a in portal_ui.achievements(
            finished=finished, stats=stats, streak=streak(days=3), student=SimpleNamespace(honor_since=None),
            open_mistakes_n=2)}
        self.assertTrue(got["Birinchi test"] and got["5 ta test"] and got["80%+ natija"])
        self.assertFalse(got["10 ta test"] or got["Mukammal test"] or got["7 kunlik streak"] or got["Xatolarsiz"])

    def test_growth_chart_uses_integer_coordinates(self):
        recent = [SimpleNamespace(percent=p) for p in (40, 55, 90)]
        g = portal_ui.growth_chart(recent)
        self.assertEqual(g["delta"], 50)
        for p in g["points"]:  # lokalizatsiyada "24,0" bo'lib SVG'ni buzmasin
            self.assertIsInstance(p["x"], int)
            self.assertIsInstance(p["y"], int)
        self.assertIsNone(portal_ui.growth_chart(recent[:1]))


    def test_board_view_podium_handles_ties_and_gap(self):
        def row(pk, coins, place):
            return {"student": SimpleNamespace(pk=pk), "coins": coins, "place": place}

        board = [row(1, 50, 1), row(2, 20, 2), row(3, 20, 2), row(4, 5, 4)]
        v = portal_ui.board_view(board, me_pk=4)
        self.assertEqual([r["pos"] for r in v["podium"]], [2, 1, 3])  # vizual: 2-1-3, teng ballarda ham
        self.assertEqual([r["student"].pk for r in v["rest"]], [4])
        self.assertEqual(v["gap"], 15)
        self.assertEqual(portal_ui.board_view([row(1, 0, 1)], me_pk=1)["podium"], [])  # hamma 0 — podium yo'q

    def test_topic_status_and_mistake_bars(self):
        def st(p):
            last = SimpleNamespace(percent=p) if p is not None else None
            return portal_ui.topic_status(SimpleNamespace(last=last), 70)["key"]

        self.assertEqual([st(None), st(40), st(75), st(90)], ["new", "review", "progress", "mastered"])
        bars = portal_ui.mistake_bars([{"n": 4}, {"n": 1}])
        self.assertEqual([b["pct"] for b in bars], [100, 25])


class PortalPageTests(TestCase):
    def test_page_shows_plan_achievements_and_hides_empty_topics(self):
        s = f.student(f.group(), portal_token="tok-ultra", profile_until=timezone.now() + timedelta(hours=2))
        page = self.client.get(reverse("student_portal", args=[s.portal_token]))
        self.assertEqual(page.status_code, 200)
        for marker in ("Bugungi reja", "Yutuqlar", "p-avatar-ring", "Streakni saqlang"):
            self.assertContains(page, marker)
        self.assertContains(page, "0 / 8")  # hali yutuq yo'q
