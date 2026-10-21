import importlib

from django.apps import apps
from django.test import TestCase
from django.urls import reverse

from academy.models import Topic
from academy.quiz_bank import seed_slides
from academy.school_data.ai import MODULES, TRACK
from academy.school_data.slides_ai import SLIDES
from academy.slides import deck, split_slides

from . import factories as f

course = importlib.import_module("academy.migrations.0032_ai_course")
migration = importlib.import_module("academy.migrations.0033_topic_slides")

DECK = """# Salom <b>dunyo</b>
Kichik izoh
---
## Amaliyot
1. Birinchi
2. **Ikkinchi**
:: timer 25
---
```
a = 1
---
b = 2
```
!! Katta `ibora`
"""


class DeckParserTests(TestCase):
    def test_split_ignores_separator_inside_code(self):
        self.assertEqual(len(split_slides(DECK)), 3)
        self.assertEqual(split_slides(""), [])
        self.assertEqual(split_slides("---\n\n---"), [])

    def test_render(self):
        title, practice, code = deck(DECK)
        self.assertTrue(title["is_title"])
        self.assertEqual(title["title"], "Salom &lt;b&gt;dunyo&lt;/b&gt;")  # HTML kiritib bo'lmaydi
        self.assertIn("<p>Kichik izoh</p>", title["html"])
        self.assertFalse(practice["is_title"])
        self.assertEqual(practice["timer"], 25)
        self.assertIn("<ol>", practice["html"])
        self.assertIn("<strong>Ikkinchi</strong>", practice["html"])
        self.assertNotIn("timer", practice["html"])
        self.assertIn("---\nb = 2", code["html"])
        self.assertIn('<p class="slide-big">Katta <code>ibora</code></p>', code["html"])
        self.assertEqual(code["timer"], 0)

    def test_timer_is_capped(self):
        self.assertEqual(deck("## A\n:: timer 999")[0]["timer"], 180)


class AiSlidesDataTests(TestCase):
    def test_every_lesson_has_full_deck(self):
        self.assertEqual(list(SLIDES), TRACK)
        for key, text in SLIDES.items():
            slides = deck(text)
            self.assertEqual(len(slides), 11, key)
            self.assertTrue(slides[0]["is_title"] and slides[-1]["is_title"], key)
            self.assertEqual([s["timer"] for s in slides if s["timer"]], [25, 5], key)
            self.assertTrue(all(s["html"] for s in slides), key)


class SlidesViewTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())

    def test_shows_deck(self):
        topic = f.topic(slides=DECK)
        url = reverse("topic_slides", args=[topic.pk])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'aria-roledescription="slayd"', count=3)
        self.assertContains(r, 'data-timer="25"')
        self.assertContains(r, "deck.js")
        self.assertContains(self.client.get(topic.get_absolute_url()), url)

    def test_empty_deck_redirects_to_edit(self):
        topic = f.topic()
        r = self.client.get(reverse("topic_slides", args=[topic.pk]))
        self.assertRedirects(r, reverse("topic_update", args=[topic.pk]))
        self.assertNotContains(self.client.get(topic.get_absolute_url()), reverse("topic_slides", args=[topic.pk]))

    def test_login_required(self):
        self.client.logout()
        topic = f.topic(slides=DECK)
        r = self.client.get(reverse("topic_slides", args=[topic.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertNotIn("taqdimot", r.url.split("?")[0])


class SeedSlidesTests(TestCase):
    def test_migration_fills_ai_topics_only_when_empty(self):
        f.group(code="AI 00-1", name="Suniy intelekt AI")
        course.forwards(apps, None)
        first = MODULES[0].topics[0]
        Topic.objects.filter(title=first.title).update(slides="# Ustoz varianti")
        other = f.topic(title="Boshqa mavzu")

        migration.forwards(apps, None)
        self.assertEqual(Topic.objects.exclude(slides="").count(), 24)
        self.assertEqual(Topic.objects.get(title=first.title).slides, "# Ustoz varianti")
        second = MODULES[0].topics[1]
        self.assertEqual(Topic.objects.get(title=second.title).slides, SLIDES[second.key])
        other.refresh_from_db()
        self.assertEqual(other.slides, "")
        self.assertEqual(seed_slides(Topic), 0)  # qayta ishga tushirish — o'zgarish yo'q
