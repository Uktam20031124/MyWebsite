from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from academy.management.commands.load_school import validate
from academy.models import Group, Lesson, Student, SyllabusItem, Topic
from academy.school_data import GroupData, ModuleData, TopicData, all_groups, all_modules

from . import factories as f


def load(**kw):
    out = StringIO()
    call_command("load_school", stdout=out, **kw)
    return out.getvalue()


class SchoolDataTests(TestCase):
    def test_bundled_data_is_valid(self):
        self.assertEqual(validate(all_modules(), all_groups()), [])

    def test_every_topic_has_lesson_plan_and_homework(self):
        for module in all_modules():
            for topic in module.topics:
                with self.subTest(topic=topic.key):
                    self.assertIn("Maqsad:", topic.description)
                    self.assertTrue(topic.homework.strip())

    def test_validate_reports_problems(self):
        t = TopicData("K1", "Mavzu", "Maqsad: x", "vazifa")
        modules = [ModuleData("B", "", [t, t])]
        groups = [GroupData("G-1", "G", ["Ali", "Ali"], taught=["K1"], planned=["K1", "NOPE"])]
        errors = "\n".join(validate(modules, groups))
        for fragment in ("kaliti takrorlangan: K1", "noma'lum mavzu kaliti NOPE",
                         "dasturda takrorlangan", "ismi takrorlangan"):
            self.assertIn(fragment, errors)


class LoadSchoolCommandTests(TestCase):
    def test_loads_groups_students_and_syllabus(self):
        load()
        self.assertEqual(
            {g.code: g.students.count() for g in Group.objects.all()},
            {"S-009": 12, "S005": 7, "P-006": 5},
        )
        # Bir xil ismli o'quvchi ikki guruhda — ikki alohida yozuv.
        self.assertEqual(Student.objects.filter(full_name="Muxammadov Imron").count(), 2)

        p006 = Group.objects.get(code="P-006")
        taught = p006.syllabus.filter(status=SyllabusItem.Status.TAUGHT)
        self.assertEqual(taught.count(), 6)
        self.assertEqual(p006.next_syllabus_item().topic.title, "Tuple va Set: o'zgarmas ro'yxat va to'plamlar")

        s005 = Group.objects.get(code="S005")
        self.assertEqual(s005.next_syllabus_item().topic.title, "Google Drive — asoslar va hamkorlik")
        self.assertEqual(Topic.objects.count(), sum(len(m.topics) for m in all_modules()))

    def test_rerun_is_idempotent_and_keeps_lesson_progress(self):
        load()
        group = Group.objects.get(code="S-009")
        item = group.next_syllabus_item()
        f.lesson(group, days=-1, topic=item.topic, status=Lesson.Status.COMPLETED)
        counts = (Topic.objects.count(), Student.objects.count(), SyllabusItem.objects.count())

        load()

        self.assertEqual(
            (Topic.objects.count(), Student.objects.count(), SyllabusItem.objects.count()), counts
        )
        item.refresh_from_db()
        self.assertEqual(item.status, SyllabusItem.Status.TAUGHT)

    def test_reset_removes_old_data_but_keeps_users(self):
        call_command("bootstrap", no_demo=True, stdout=StringIO())
        old = f.group(code="OLD-1")
        f.student(old, full_name="Begona O'quvchi")
        f.lesson(old, days=-1)
        users = get_user_model().objects.count()
        load(reset=True, yes=True)
        self.assertEqual(set(Group.objects.values_list("code", flat=True)), {"S-009", "S005", "P-006"})
        self.assertFalse(Student.objects.filter(full_name="Begona O'quvchi").exists())
        self.assertFalse(Lesson.objects.exists())
        self.assertEqual(get_user_model().objects.count(), users)

    def test_reset_requires_confirmation_when_not_interactive(self):
        f.group(code="OLD-1")
        with mock.patch("sys.stdin.isatty", return_value=False), self.assertRaises(CommandError):
            load(reset=True)
        self.assertTrue(Group.objects.filter(code="OLD-1").exists())
