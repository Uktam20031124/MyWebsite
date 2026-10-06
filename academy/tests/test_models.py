from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from academy.models import Attendance, Group, Lesson, SyllabusItem, Topic
from academy.services import dashboard_payload, groups_with_stats, students_with_stats

from . import factories as f


class LessonSyllabusSyncTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.topic = f.topic()
        self.group.add_topics([self.topic])

    def item(self):
        return SyllabusItem.objects.get(group=self.group, topic=self.topic)

    def test_mark_completed_marks_syllabus_taught(self):
        lesson = f.lesson(self.group, days=-1, topic=self.topic)
        lesson.mark_completed()
        self.assertEqual(self.item().status, SyllabusItem.Status.TAUGHT)
        self.assertEqual(self.item().taught_on, lesson.held_on)

    def test_saving_completed_status_directly_syncs(self):
        # Regressiya: avval faqat "yaratish" formasi dasturni yangilardi.
        lesson = f.lesson(self.group, topic=self.topic)
        lesson.status = Lesson.Status.COMPLETED
        lesson.save()
        self.assertEqual(self.item().status, SyllabusItem.Status.TAUGHT)

    def test_planned_lesson_does_not_touch_syllabus(self):
        f.lesson(self.group, topic=self.topic)
        self.assertEqual(self.item().status, SyllabusItem.Status.PLANNED)


class SyllabusTests(TestCase):
    def test_add_topics_skips_duplicates_and_appends(self):
        g = f.group()
        a, b, c = f.topic(), f.topic(), f.topic()
        self.assertEqual(g.add_topics([a, b]), 2)
        self.assertEqual(g.add_topics([b, c, c]), 1)
        self.assertEqual(
            list(g.syllabus.values_list("topic_id", "order")),
            [(a.pk, 1), (b.pk, 2), (c.pk, 3)],
        )

    def test_move_up_and_down(self):
        g = f.group()
        a, b = f.topic(), f.topic()
        g.add_topics([a, b])
        item_b = g.syllabus.get(topic=b)
        self.assertTrue(item_b.move("up"))
        self.assertEqual(list(g.syllabus.values_list("topic_id", flat=True)), [b.pk, a.pk])
        self.assertFalse(g.syllabus.get(topic=b).move("up"))

    def test_next_syllabus_item(self):
        g = f.group()
        a, b = f.topic(), f.topic()
        g.add_topics([a, b])
        g.syllabus.filter(topic=a).update(status=SyllabusItem.Status.TAUGHT)
        self.assertEqual(g.next_syllabus_item().topic, b)


class StatsTests(TestCase):
    def test_annotations_do_not_multiply_counts(self):
        g = f.group()
        s1, s2 = f.student(g), f.student(g)
        g.add_topics([f.topic(), f.topic()])
        g.syllabus.filter(order=1).update(status=SyllabusItem.Status.TAUGHT)
        for days in (-1, -2):
            lesson = f.lesson(g, days=days)
            Attendance.objects.create(lesson=lesson, student=s1)
            Attendance.objects.create(
                lesson=lesson, student=s2, status=Attendance.Status.ABSENT
            )

        row = groups_with_stats().get(pk=g.pk)
        self.assertEqual((row.student_n, row.syllabus_total, row.syllabus_taught), (2, 2, 1))
        stats = {s.pk: (s.att_present, s.att_total) for s in students_with_stats()}
        self.assertEqual(stats[s1.pk], (2, 2))
        self.assertEqual(stats[s2.pk], (0, 2))

    def test_dashboard_week_ignores_future_lessons(self):
        g = f.group()
        f.lesson(g, days=-1)
        f.lesson(g, days=3)
        payload = dashboard_payload()
        self.assertEqual(payload["stats"]["lessons_week"], 1)

    def test_dashboard_lists_overdue_planned_lessons(self):
        g = f.group()
        old = f.lesson(g, days=-3)
        f.lesson(g, days=-2, status=Lesson.Status.COMPLETED)
        self.assertEqual(list(dashboard_payload()["overdue"]), [old])


class StudentTests(TestCase):
    def test_telegram_at_sign_is_stripped(self):
        s = f.student(telegram=" @ali_dev ")
        self.assertEqual(s.telegram, "ali_dev")

    def test_initials(self):
        self.assertEqual(f.student(full_name="Aliyev Sardor Botir").initials(), "AB")
        self.assertEqual(f.student(full_name="Madina").initials(), "MA")


class TopicTests(TestCase):
    def test_resource_list_detects_links(self):
        t = f.topic(resources="https://docs.python.org\n\nKitob: Python Crash Course")
        self.assertEqual(
            t.resource_list(),
            [
                {"text": "https://docs.python.org", "url": "https://docs.python.org"},
                {"text": "Kitob: Python Crash Course", "url": ""},
            ],
        )


class BootstrapCommandTests(TestCase):
    def test_bootstrap_is_safe_to_rerun(self):
        call_command("bootstrap", stdout=StringIO())
        user = get_user_model().objects.get(username="ustoz")
        user.set_password("my-own-secret-pass")
        user.save()
        topics = Topic.objects.count()

        call_command("bootstrap", stdout=StringIO())

        user.refresh_from_db()
        self.assertTrue(user.check_password("my-own-secret-pass"))
        self.assertEqual(Topic.objects.count(), topics)
        self.assertEqual(Group.objects.count(), 3)
        self.assertTrue(Topic.objects.filter(module__title="Django").exists())

    def test_no_demo(self):
        call_command("bootstrap", no_demo=True, password="x-Strong-pass-1", stdout=StringIO())
        self.assertFalse(Group.objects.exists())
        user = get_user_model().objects.get(username="ustoz")
        self.assertTrue(user.check_password("x-Strong-pass-1"))
