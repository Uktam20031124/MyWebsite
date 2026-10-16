import gzip
import os
import sqlite3
import tempfile
import time
from io import StringIO
from pathlib import Path
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.urls import reverse

from academy.contacts import apply_contacts, parse_line, preview_contacts
from academy.models import Student

from . import factories as f


class ParseLineTests(SimpleTestCase):
    def test_formats(self):
        cases = {
            "Aliyev Sardor — @sardor_a — +998 90 123 45 67": ("Aliyev Sardor", "sardor_a", "+998901234567"),
            "2) Karimova Nigina, t.me/nigina_k": ("Karimova Nigina", "nigina_k", ""),
            "Valiyev Ali\t901234567": ("Valiyev Ali", "", "+998901234567"),
            "• Sardor Aliyev | https://t.me/Sardor_A": ("Sardor Aliyev", "Sardor_A", ""),
            "Faqat Ism": ("Faqat Ism", "", ""),
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                self.assertEqual(parse_line(line), expected)


class PreviewTests(TestCase):
    def setUp(self):
        self.group = f.group()
        self.sardor = f.student(self.group, full_name="Aliyev Sardor")
        self.nigina = f.student(self.group, full_name="Karimova Nigina", telegram="old_nick")
        f.student(self.group, full_name="Aliyev Sanjar")

    def preview(self, text):
        return preview_contacts(text, Student.objects.all())

    def test_matching_rules(self):
        rows = self.preview(
            "Sardor Aliyev @sardor_a\n"  # tartib boshqa
            "Karimova Nig @nigina_k\n"  # qisqartirilgan
            "Aliyev S @bir_nechta\n"  # ikki o'quvchiga mos
            "Noma'lum Odam @kimdir\n"
            "Aliyev Sardor\n"  # kontakt yo'q
        )
        self.assertEqual([r.status for r in rows], ["update", "update", "error", "error", "error"])
        self.assertEqual(rows[0].student, self.sardor)
        self.assertEqual(rows[1].changes, {"telegram": ("old_nick", "nigina_k")})
        self.assertEqual(len(rows[2].candidates), 2)
        self.assertIn("topilmadi", rows[3].error)
        self.assertIn("topilmadi", rows[4].error)

    def test_unchanged_and_duplicate_lines(self):
        rows = self.preview("Karimova Nigina @old_nick\nAliyev Sardor @a_one\nAliyev Sardor @a_two")
        self.assertEqual(rows[0].status, "same")
        self.assertEqual(rows[1].status, "error")  # pastdagi qator olinadi
        self.assertEqual(rows[2].changes["telegram"][1], "a_two")

    def test_apply_updates_only_given_fields(self):
        f.student(self.group, full_name="Toshev Bek", phone="+998901111111")
        rows = self.preview("Toshev Bek @bek_t\nKarimova Nigina +998 93 222 33 44")
        self.assertEqual(apply_contacts(rows), 2)
        bek = Student.objects.get(full_name="Toshev Bek")
        self.assertEqual((bek.telegram, bek.phone), ("bek_t", "+998901111111"))
        self.nigina.refresh_from_db()
        self.assertEqual((self.nigina.telegram, self.nigina.phone), ("old_nick", "+998932223344"))


class ContactViewsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.group = f.group(name="S-009")
        self.ali = f.student(self.group, full_name="Ali Valiyev")
        self.has = f.student(self.group, full_name="Bor Kontakt", telegram="bor_kontakt")
        self.other = f.student(f.group(), full_name="Ali Valiyev")  # boshqa guruhda adash
        self.client.force_login(f.user())

    def test_import_preview_then_confirm(self):
        url = reverse("contacts_import")
        data = {"text": "Ali Valiyev @ali_v", "group": self.group.pk}
        response = self.client.post(url, data)
        self.assertContains(response, "Yangilanadi")
        self.ali.refresh_from_db()
        self.assertEqual(self.ali.telegram, "")  # tasdiqsiz hech narsa o'zgarmaydi
        response = self.client.post(url, {**data, "confirm": "1"})
        self.assertRedirects(response, f"{reverse('student_list')}?contact=missing")
        self.ali.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual((self.ali.telegram, self.other.telegram), ("ali_v", ""))

    def test_import_without_group_reports_namesakes(self):
        response = self.client.post(reverse("contacts_import"), {"text": "Ali Valiyev @ali_v"})
        self.assertContains(response, "Bir nechta o‘quvchiga mos keladi")

    def test_student_list_contact_filter(self):
        response = self.client.get(reverse("student_list"), {"contact": "missing"})
        names = [s.full_name for s in response.context["students"]]
        self.assertIn("Ali Valiyev", names)
        self.assertNotIn("Bor Kontakt", names)

    def test_group_page_and_link_lifecycle(self):
        page = self.client.get(self.group.get_absolute_url())
        self.assertContains(page, "1 / 2")
        self.assertContains(page, "Havola yaratish")
        link_url = reverse("group_contact_link", args=[self.group.pk])
        self.client.post(link_url)
        self.group.refresh_from_db()
        old = self.group.contact_token
        self.assertTrue(old)
        self.assertContains(self.client.get(self.group.get_absolute_url()), f"/aloqa/{old}/")
        self.client.post(link_url)  # yangilash
        self.group.refresh_from_db()
        self.assertNotEqual(self.group.contact_token, old)
        self.assertEqual(self.client.get(reverse("contact_self", args=[old])).status_code, 404)
        self.client.post(link_url, {"action": "off"})
        self.group.refresh_from_db()
        self.assertEqual(self.group.contact_token, "")

    def self_url(self):
        self.group.contact_token = "tok123"
        self.group.save()
        return reverse("contact_self", args=["tok123"])

    def test_self_fill_saves_only_empty_fields(self):
        url = self_url = self.self_url()
        self.client.logout()
        page = self.client.get(url)
        self.assertContains(page, "Ali Valiyev")
        self.assertNotContains(page, self.other.group.name)
        response = self.client.post(self_url, {"student": self.ali.pk, "telegram": "@ali_v", "phone": "90 123 45 67"})
        self.assertContains(response, "Rahmat")
        self.ali.refresh_from_db()
        self.assertEqual((self.ali.telegram, self.ali.phone), ("ali_v", "+998901234567"))
        # Boshqaning mavjud username'ini o'zgartirib bo'lmaydi.
        response = self.client.post(url, {"student": self.has.pk, "telegram": "hacker_x"})
        self.assertContains(response, "oldin kiritilgan")
        self.has.refresh_from_db()
        self.assertEqual(self.has.telegram, "bor_kontakt")

    def test_self_fill_validation_and_isolation(self):
        url = self.self_url()
        self.client.logout()
        response = self.client.post(url, {"student": self.ali.pk, "telegram": "@ab"})
        self.assertContains(response, "Username noto‘g‘ri")
        response = self.client.post(url, {"student": self.ali.pk})
        self.assertContains(response, "Telegram username yoki telefon raqamini kiriting")
        response = self.client.post(url, {"student": self.other.pk, "telegram": "@ali_v"})
        self.assertEqual(response.status_code, 200)
        self.other.refresh_from_db()
        self.assertEqual(self.other.telegram, "")  # boshqa guruh o'quvchisi tanlanmaydi

    def test_self_fill_throttle(self):
        url = self.self_url()
        self.client.logout()
        with mock.patch("academy.views.CONTACT_SELF_LIMIT", 1):
            self.client.post(url, {"student": self.ali.pk, "telegram": "@ali_v"})
            response = self.client.post(url, {"student": self.ali.pk, "phone": "901234567"})
        self.assertContains(response, "Juda ko‘p urinish")


class BackupCommandTests(TransactionTestCase):
    """Tranzaksiyasiz: SQLite backup ochiq yozish tranzaksiyasi tugashini kutib qoladi."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        f.student(full_name="Zaxira Tekshiruv")

    def run_backup(self, *args):
        out = StringIO()
        call_command("backup_db", "--dir", str(self.dir), *args, stdout=out)
        return out.getvalue()

    def test_creates_valid_compressed_copy(self):
        out = self.run_backup()
        files = list(self.dir.glob("darsxona-*.sqlite3.gz"))
        self.assertEqual(len(files), 1, out)
        self.assertEqual(files[0].stat().st_mode & 0o777, 0o600)
        raw = self.dir / "check.sqlite3"
        raw.write_bytes(gzip.decompress(files[0].read_bytes()))
        db = sqlite3.connect(raw)
        names = [r[0] for r in db.execute("select full_name from academy_student")]
        db.close()
        self.assertIn("Zaxira Tekshiruv", names)

    def test_prunes_old_copies(self):
        old = self.dir / "darsxona-20200101-000000.sqlite3.gz"
        old.write_bytes(b"x")
        week_ago = time.time() - 30 * 86400
        os.utime(old, (week_ago, week_ago))
        other = self.dir / "boshqa-fayl.txt"
        other.write_text("tegilmaydi")
        out = self.run_backup("--keep-days", "14")
        self.assertFalse(old.exists())
        self.assertTrue(other.exists())
        self.assertIn("1 ta", out)

    @mock.patch("academy.telegram_sender.send_file_to_self")
    def test_telegram_copy(self, send):
        out = self.run_backup("--telegram")
        path = send.call_args.args[0]
        self.assertTrue(str(path).endswith(".sqlite3.gz"))
        self.assertIn("Telegram", out)
