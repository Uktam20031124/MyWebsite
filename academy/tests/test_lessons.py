import importlib
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy.lessons import bank, frame_count, frames, seed_lessons, validate
from academy.models import Module, Quiz, Topic
from academy.quiz_bank import bank_texts, bank_texts_ru, bank_titles_ru
from academy.school_data import all_modules
from academy.school_data.dev import MODULES, TRACK

from . import factories as f

migration = importlib.import_module("academy.migrations.0043_dev_track")


def dev_topic(key):
    for module in MODULES:
        for t in module.topics:
            if t.key == key:
                return f.topic(module=f.module(title=module.title), title=t.title, order=1)
    raise KeyError(key)


class DevCatalogTests(TestCase):
    def test_nine_months_of_twelve_lessons(self):
        self.assertEqual(len(MODULES), 9)
        self.assertTrue(all(len(m.topics) == 12 for m in MODULES))
        self.assertEqual(len(set(TRACK)), 108)
        self.assertTrue(set(TRACK) <= {t.key for m in all_modules() for t in m.topics})
        self.assertTrue(set(TRACK) <= set(bank_titles_ru()))

    def test_quizzes_only_for_dev_keys(self):
        self.assertTrue(set(bank_texts()) >= {"TB10"})
        self.assertEqual({k for k in bank_texts() if k in TRACK}, {k for k in bank_texts_ru() if k in TRACK})


class LessonDataTests(TestCase):
    def test_every_lesson_is_valid_and_has_pngs(self):
        for key, lesson in bank().items():
            self.assertIn(key, TRACK)
            self.assertEqual(validate(key, lesson), [])
            self.assertEqual(len(frames({**lesson, "key": key})), frame_count(lesson))
            for n in range(1, frame_count(lesson) + 1):
                png = Path(settings.BASE_DIR) / "static" / "lessons" / key / f"{n:02}.png"
                self.assertTrue(png.is_file(), png)

    def test_programs_run_and_print_expected_output(self):
        from academy.lessons import run_program

        checked = 0
        for key, lesson in bank().items():
            if "run" not in lesson:
                continue
            out = run_program(lesson)
            for expected in lesson["run"]["expect"]:
                self.assertIn(expected, out, key)
            checked += 1
        self.assertGreaterEqual(checked, 12)

    def test_validate_catches_code_not_in_files(self):
        lesson = {**bank()["TB10"]}
        lesson["steps"] = [{**lesson["steps"][0], "code": "print('yo‘q qator')"}]
        self.assertTrue(validate("TB10", lesson))

    def test_frames_escape_text(self):
        lesson = {**bank()["TB10"], "key": "TB10", "title": "<script>x</script>"}
        self.assertNotIn("<script>x", frames(lesson)[0])

    def test_web_lessons_have_browser_preview_frame(self):
        web = {k: v for k, v in bank().items() if "preview" in v}
        self.assertGreaterEqual(len(web), 23)
        for key, lesson in web.items():
            image = Path(settings.BASE_DIR) / "static" / lesson["preview"]["image"]
            self.assertTrue(image.is_file(), image)
            out = frames({**lesson, "key": key})
            self.assertIn("previewwrap", out[-2])  # yakuniy kadrdan oldin
            self.assertIn(f"lessons/{key}/site", out[-2])


class DevMigrationTests(TestCase):
    def test_skips_empty_database(self):
        migration.forwards(apps, None)
        self.assertFalse(Module.objects.filter(title__startswith="Dasturchi").exists())

    def test_fills_catalog_quiz_and_lesson(self):
        f.module(title="Mavjud bo'lim")
        migration.forwards(apps, None)
        self.assertEqual(Topic.objects.filter(module__title__startswith="Dasturchi").count(), 108)
        topic = Topic.objects.get(title__startswith="Test rejimi, 1-qism")
        self.assertEqual(topic.lesson["key"], "TB10")
        self.assertEqual(topic.lesson["frames"], 9)
        self.assertTrue(topic.title_ru)
        self.assertEqual(Quiz.objects.get(topic=topic).questions.count(), 10)
        migration.forwards(apps, None)  # qayta ishga tushirish — takrorlanmaydi
        self.assertEqual(Topic.objects.filter(module__title__startswith="Dasturchi").count(), 108)


class LessonViewTests(TestCase):
    def setUp(self):
        self.topic = dev_topic("TB10")
        seed_lessons(Topic)
        self.url = reverse("topic_lesson", args=[self.topic.pk])

    def test_page_shows_frames_plan_and_code(self):
        self.client.force_login(f.user())
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'class="lf"', count=9)
        self.assertContains(r, "lessons/TB10/01.png")
        self.assertContains(r, "Dars rejasi")
        self.assertContains(r, "check_answer")
        self.assertContains(self.client.get(self.topic.get_absolute_url()), self.url)

    def test_png_mode_has_only_frames(self):
        self.client.force_login(f.user())
        r = self.client.get(self.url + "?png=1")
        self.assertContains(r, "lesson-body png")
        self.assertNotContains(r, "lp-bar")

    def test_topic_without_lesson_404_and_login_required(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)
        self.client.force_login(f.user())
        bare = f.topic()
        self.assertEqual(self.client.get(reverse("topic_lesson", args=[bare.pk])).status_code, 404)

    def test_teacher_with_topics_permission(self):
        teacher = f.user(username="malika")
        account = teachers.account_of(teacher)
        account.permissions = ["topics"]
        account.telegram_id, account.linked_at = 555, timezone.now()
        account.save()
        self.client.force_login(teacher)
        self.assertEqual(self.client.get(self.url).status_code, 200)
