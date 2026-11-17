import contextlib
import importlib
import io
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy.models import Topic
from academy.posters import VISUALS, bank, code_html, formula_html, seed_posters, typeset, validate
from academy.school_data import all_modules
from academy.templatetags.posters import poster_keys

from . import factories as f

migration = importlib.import_module("academy.migrations.0042_topic_poster")


def catalog_topic(key):
    for module in all_modules():
        for t in module.topics:
            if t.key == key:
                return f.topic(module=f.module(title=module.title), title=t.title, order=1)
    raise KeyError(key)


class PosterDataTests(TestCase):
    def test_every_catalog_topic_has_valid_poster_and_png(self):
        data = bank()
        keys = [t.key for m in all_modules() for t in m.topics]
        self.assertEqual(sorted(data), sorted(keys))
        for key, p in data.items():
            self.assertEqual(validate(key, p), [])
            self.assertIn(p["visual"]["kind"], VISUALS)
            self.assertTrue(all(q["q"] and q["a"] for q in p["questions"]), key)
            png = Path(settings.BASE_DIR) / "static" / "posters" / f"{key}.png"
            self.assertTrue(png.is_file(), png)

    def test_code_outputs_are_real(self):
        """"Natija" bloklari — kodni ishga tushirib olingan haqiqiy chiqish."""
        checked = 0
        for key, p in bank().items():
            v = p["visual"]
            if v["kind"] != "code" or not v["data"].get("run", True) or v["data"]["lang"] != "python":
                continue
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                exec(v["data"]["code"], {})  # noqa: S102 — o'zimizning o'quv kodi
            self.assertEqual(out.getvalue().strip("\n"), v["data"]["output"], key)
            checked += 1
        self.assertGreaterEqual(checked, 25)


class PosterHelpersTests(TestCase):
    def test_formula_escapes_and_highlights(self):
        html = formula_html("<b>a</b> ÷ 5 = [WPM]")
        self.assertIn("&lt;b&gt;", html)
        self.assertIn('<span class="op">÷</span>', html)
        self.assertIn('<span class="eq">WPM</span>', html)
        self.assertNotIn('class=<span', html)  # "=" amalni class="..." ichida almashtirmaydi

    def test_code_highlight_escapes(self):
        html = code_html('if x < 3:\n    print("<i>")  # izoh')
        self.assertIn('<span class="kw">if</span>', html)
        self.assertIn('<span class="bi">print</span>', html)
        self.assertIn("&lt;i&gt;", html)
        self.assertIn('<span class="cm"># izoh</span>', html)

    def test_typeset_skips_code(self):
        value = typeset({"goal": "o'z", "visual": {"data": {"code": "print('a')", "title": "g'oya"}}})
        self.assertEqual(value["goal"], "o‘z")
        self.assertEqual(value["visual"]["data"]["code"], "print('a')")
        self.assertEqual(value["visual"]["data"]["title"], "g‘oya")

    def test_keys_marks_home_row(self):
        html = poster_keys("FJ")
        self.assertIn('class="pp-k il home bump"', html)
        self.assertIn('class="pp-k ir home bump"', html)


class PosterSeedTests(TestCase):
    def test_migration_fills_catalog_topics(self):
        topic = catalog_topic("ST01")
        other = f.topic(title="Boshqa mavzu")
        migration.forwards(apps, None)
        topic.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(topic.poster["key"], "ST01")
        self.assertEqual(topic.poster["image"], "posters/ST01.png")
        self.assertIn("o‘z barmog‘i", topic.poster["goal"])
        self.assertEqual(other.poster, {})
        self.assertEqual(seed_posters(Topic, only={"PY01"}), 0)


class PosterViewTests(TestCase):
    def setUp(self):
        self.topic = catalog_topic("PY04")
        seed_posters(Topic)
        self.url = reverse("topic_poster", args=[self.topic.pk])

    def test_page_shows_poster_answers_and_png(self):
        self.client.force_login(f.user())
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "pp-frame")
        self.assertContains(r, "Test oldidan")
        self.assertContains(r, "Javoblar")
        self.assertContains(r, "posters/PY04.png")
        self.assertContains(r, "&#x27;molas&#x27;")  # javob ustoz uchun yashirin blokda
        self.assertContains(self.client.get(self.topic.get_absolute_url()), self.url)

    def test_png_mode_is_clean(self):
        self.client.force_login(f.user())
        r = self.client.get(self.url + "?png=1")
        self.assertContains(r, "poster-body png")
        self.assertNotContains(r, "pp-answers")

    def test_topic_without_poster_404(self):
        self.client.force_login(f.user())
        bare = f.topic()
        self.assertEqual(self.client.get(reverse("topic_poster", args=[bare.pk])).status_code, 404)
        self.assertNotContains(self.client.get(bare.get_absolute_url()), "rasm/")

    def test_login_required(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 302)

    def test_teacher_with_topics_permission(self):
        teacher = f.user(username="malika")
        account = teachers.account_of(teacher)
        account.permissions = ["topics"]
        account.telegram_id, account.linked_at = 555, timezone.now()  # Telegram ulangan
        account.save()
        self.client.force_login(teacher)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        account.permissions = ["students"]
        account.save()
        self.assertNotEqual(self.client.get(self.url).status_code, 200)
