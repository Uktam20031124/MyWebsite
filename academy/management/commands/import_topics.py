import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from academy.models import Group
from academy.services import import_topics, parse_topics


class Command(BaseCommand):
    help = (
        "Mavzularni matn faylidan import qiladi (# Bo'lim / 1. Mavzu — tavsif). "
        "Faylsiz yoki '-' berilsa, stdin'dan o'qiydi."
    )

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default="-", help="Matn fayli yoki '-'")
        parser.add_argument(
            "--group",
            action="append",
            default=[],
            metavar="KOD",
            help="Mavzularni shu guruh dasturiga ham qo'shish (bir necha marta berish mumkin)",
        )
        parser.add_argument("--duration", type=int, default=90, help="Standart davomiylik (daq.)")
        parser.add_argument("--dry-run", action="store_true", help="Faqat ko'rsatish, yozmaslik")

    def handle(self, path, group, duration, dry_run, **options):
        if path == "-":
            text = sys.stdin.read()
        else:
            file = Path(path)
            if not file.exists():
                raise CommandError(f"Fayl topilmadi: {path}")
            text = file.read_text(encoding="utf-8-sig")

        parsed = parse_topics(text)
        if not any(m.topics for m in parsed):
            raise CommandError("Matndan birorta ham mavzu topilmadi.")

        groups = []
        for code in group:
            g = Group.objects.filter(code__iexact=code).first()
            if g is None:
                raise CommandError(f"Guruh topilmadi: {code}")
            groups.append(g)

        for m in parsed:
            self.stdout.write(self.style.MIGRATE_HEADING(m.title or "(bo'limsiz)"))
            for i, t in enumerate(m.topics, start=1):
                extra = f" — {t.description}" if t.description else ""
                self.stdout.write(f"  {i}. {t.title}{extra}")

        if dry_run:
            self.stdout.write(self.style.WARNING("--dry-run: bazaga hech narsa yozilmadi."))
            return

        result = import_topics(parsed, groups=groups, default_duration=duration)
        self.stdout.write(
            self.style.SUCCESS(
                f"Tayyor: {result.modules_created} bo'lim, {result.topics_created} yangi mavzu, "
                f"{result.topics_updated} yangilandi, {result.added_to_groups} ta dasturga qo'shildi."
            )
        )
