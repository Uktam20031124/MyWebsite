from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from academy.models import Module, SyllabusItem, Topic
from academy.services import export_topics, import_topics, parse_topics

from . import factories as f

SAMPLE = """
# Python asoslari
1. Kirish va muhit — VS Code, terminal
2) O'zgaruvchilar | int, str | 120
- Sikllar
    for, while
    break / continue

# Django
• Modellar - ORM
* Formalar
"""


class ParseTopicsTests(TestCase):
    def test_modules_bullets_and_descriptions(self):
        modules = parse_topics(SAMPLE)
        self.assertEqual([m.title for m in modules], ["Python asoslari", "Django"])
        py, dj = modules
        self.assertEqual(
            [t.title for t in py.topics], ["Kirish va muhit", "O'zgaruvchilar", "Sikllar"]
        )
        self.assertEqual(py.topics[0].description, "VS Code, terminal")
        self.assertEqual(py.topics[1].description, "int, str")
        self.assertEqual(py.topics[1].duration, 120)
        self.assertEqual(py.topics[2].description, "for, while\nbreak / continue")
        self.assertEqual([t.title for t in dj.topics], ["Modellar", "Formalar"])
        self.assertEqual(dj.topics[0].description, "ORM")

    def test_topics_without_heading(self):
        modules = parse_topics("Mavzu A\nMavzu B\n")
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0].title, "")
        self.assertEqual(len(modules[0].topics), 2)

    def test_hyphen_inside_word_is_kept(self):
        (m,) = parse_topics("Wi-Fi va tarmoq")
        self.assertEqual(m.topics[0].title, "Wi-Fi va tarmoq")

    def test_blank_text(self):
        self.assertEqual(parse_topics("  \n\n"), [])


class ImportTopicsTests(TestCase):
    def test_creates_modules_and_topics_in_order(self):
        result = import_topics(parse_topics(SAMPLE))
        self.assertEqual(result.modules_created, 2)
        self.assertEqual(result.topics_created, 5)
        py = Module.objects.get(title="Python asoslari")
        self.assertEqual(
            list(py.topics.order_by("order").values_list("title", flat=True)),
            ["Kirish va muhit", "O'zgaruvchilar", "Sikllar"],
        )
        self.assertEqual(Topic.objects.get(title="O'zgaruvchilar").duration_minutes, 120)

    def test_reimport_is_idempotent_and_updates_description(self):
        import_topics(parse_topics(SAMPLE))
        result = import_topics(parse_topics("# python ASOSLARI\nSikllar — yangi tavsif"))
        self.assertEqual(result.topics_created, 0)
        self.assertEqual(result.modules_created, 0)
        self.assertEqual(result.topics_updated, 1)
        self.assertEqual(Topic.objects.count(), 5)
        self.assertEqual(Topic.objects.get(title="Sikllar").description, "yangi tavsif")

    def test_adds_to_group_syllabus_once(self):
        g = f.group()
        import_topics(parse_topics(SAMPLE), groups=[g])
        import_topics(parse_topics(SAMPLE), groups=[g])
        self.assertEqual(g.syllabus.count(), 5)
        self.assertEqual(
            list(g.syllabus.values_list("order", flat=True)), [1, 2, 3, 4, 5]
        )

    def test_export_roundtrip(self):
        import_topics(parse_topics(SAMPLE + "\n"))
        f.topic(title="Bo'limsiz mavzu")
        text = export_topics()
        self.assertTrue(text.startswith("1. Bo'limsiz mavzu"))
        Topic.objects.all().delete()
        Module.objects.all().delete()
        import_topics(parse_topics(text))
        self.assertEqual(Topic.objects.count(), 6)
        self.assertEqual(Module.objects.count(), 2)
        self.assertEqual(Topic.objects.get(title="O'zgaruvchilar").duration_minutes, 120)


class ImportCommandTests(TestCase):
    def test_command_imports_file_into_group(self):
        g = f.group(code="PY-9")
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "mavzular.txt"
            path.write_text(SAMPLE, encoding="utf-8")
            call_command("import_topics", str(path), group=["py-9"], stdout=StringIO())
        self.assertEqual(Topic.objects.count(), 5)
        self.assertEqual(SyllabusItem.objects.filter(group=g).count(), 5)

    def test_dry_run_writes_nothing(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.txt"
            path.write_text(SAMPLE, encoding="utf-8")
            call_command("import_topics", str(path), dry_run=True, stdout=StringIO())
        self.assertFalse(Topic.objects.exists())

    def test_unknown_group_fails(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.txt"
            path.write_text(SAMPLE, encoding="utf-8")
            with self.assertRaises(CommandError):
                call_command("import_topics", str(path), group=["NOPE"], stdout=StringIO())
        self.assertFalse(Topic.objects.exists())
