import importlib

from django.apps import apps
from django.test import TestCase

from academy.models import Group, Question, SyllabusItem, Topic
from academy.school_data.ai import MODULES, TRACK

from . import factories as f

migration = importlib.import_module("academy.migrations.0032_ai_course")


class AiCourseMigrationTests(TestCase):
    def test_loads_course_for_ai_group_once(self):
        group = f.group(code="AI 00-1", name="Suniy intelekt AI")
        other = f.group(code="S-1")
        SyllabusItem.objects.create(group=other, topic=f.topic(title="Boshqa"), order=1)

        migration.forwards(apps, None)
        items = list(SyllabusItem.objects.filter(group=group).order_by("order").select_related("topic"))
        self.assertEqual(len(items), 24)
        self.assertEqual(items[0].topic.title, MODULES[0].topics[0].title)
        self.assertTrue(all(i.status == SyllabusItem.Status.PLANNED for i in items))
        ai_topics = Topic.objects.filter(pk__in=[i.topic_id for i in items])
        self.assertEqual(ai_topics.exclude(title_ru="").count(), 24)
        self.assertEqual(ai_topics.exclude(study="").exclude(study_ru="").count(), 24)
        questions = Question.objects.filter(quiz__topic__in=ai_topics)
        self.assertEqual(questions.count(), 24 * 12)
        self.assertEqual(questions.exclude(text_ru="").count(), 24 * 12)

        # Qayta ishga tushirish: hech narsa takrorlanmaydi, guruhdagi holatlar saqlanadi.
        items[0].status = SyllabusItem.Status.TAUGHT
        items[0].save()
        migration.forwards(apps, None)
        self.assertEqual(SyllabusItem.objects.filter(group=group).count(), 24)
        self.assertEqual(Question.objects.filter(quiz__topic__in=ai_topics).count(), 24 * 12)
        items[0].refresh_from_db()
        self.assertEqual(items[0].status, SyllabusItem.Status.TAUGHT)
        self.assertEqual(SyllabusItem.objects.filter(group=other).count(), 1)  # boshqa guruhga tegilmaydi

    def test_without_ai_group_nothing_is_created(self):
        migration.forwards(apps, None)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Group.objects.exists())

    def test_track_matches_modules(self):
        self.assertEqual(TRACK, [t.key for m in MODULES for t in m.topics])
        self.assertEqual(len(TRACK), 24)
        self.assertTrue(all(t.minutes == 60 for m in MODULES for t in m.topics))
