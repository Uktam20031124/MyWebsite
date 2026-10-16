import gzip
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.utils import timezone

from academy import telegram_sender as tg

PREFIX = "darsxona-"
SUFFIX = ".sqlite3.gz"


class Command(BaseCommand):
    help = (
        "Bazaning zaxira nusxasi: sayt ishlab turganda ham xavfsiz (SQLite backup API), "
        "yaxlitligi tekshiriladi, gzip bilan siqiladi; eski nusxalar o'chiriladi. "
        "--telegram — nusxa ustozning Telegram 'Saqlangan xabarlar'iga ham yuboriladi."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dir", help=f"Katalog (standart: {settings.BACKUP_DIR})")
        parser.add_argument(
            "--keep-days",
            type=int,
            default=settings.BACKUP_KEEP_DAYS,
            help="Shundan eski nusxalar o'chiriladi (0 — o'chirmaslik)",
        )
        parser.add_argument(
            "--telegram", action="store_true", help="Nusxani Telegram'ga ham yuborish (server tashqarisida)"
        )

    def handle(self, *args, dir, keep_days, telegram, **options):
        if connection.vendor != "sqlite":
            raise CommandError("backup_db faqat SQLite bazasi uchun.")
        target_dir = Path(dir or settings.BACKUP_DIR)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_dir.chmod(0o700)  # baza — shaxsiy ma'lumotlar
        stamp = timezone.localtime().strftime("%Y%m%d-%H%M%S")
        target = target_dir / f"{PREFIX}{stamp}{SUFFIX}"

        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "backup.sqlite3"
            self.copy_database(raw)
            with open(raw, "rb") as src, gzip.open(target, "wb", compresslevel=9) as dst:
                shutil.copyfileobj(src, dst)
        target.chmod(0o600)
        size_kb = target.stat().st_size / 1024
        self.stdout.write(self.style.SUCCESS(f"Zaxira: {target} ({size_kb:.0f} KB)"))

        removed = self.prune(target_dir, keep_days, keep=target)
        if removed:
            self.stdout.write(f"Eski nusxalar o'chirildi: {removed} ta (>{keep_days} kun).")

        if telegram:
            try:
                tg.send_file_to_self(
                    target, caption=f"Darsxona zaxira nusxasi · {timezone.localtime():%d.%m.%Y %H:%M}"
                )
            except tg.TelegramError as exc:
                # Lokal nusxa tayyor — Telegram xatosi uni bekor qilmaydi, lekin xabar beriladi.
                raise CommandError(f"Lokal nusxa saqlandi, Telegram'ga yuborilmadi: {exc}") from exc
            self.stdout.write("Telegram'ga ('Saqlangan xabarlar') yuborildi.")

    @staticmethod
    def copy_database(dest: Path) -> None:
        """Onlayn nusxa (WAL'dagi yozuvlar ham) va yaxlitlik tekshiruvi.

        Django'ning o'z ulanishi orqali: sayt yozayotgan paytda ham izchil nusxa olinadi.
        """
        connection.ensure_connection()
        out = sqlite3.connect(dest)
        try:
            connection.connection.backup(out)
            result = out.execute("PRAGMA integrity_check").fetchone()[0]
        finally:
            out.close()
        if result != "ok":
            raise CommandError(f"Nusxa yaxlitlik tekshiruvidan o'tmadi: {result}")

    @staticmethod
    def prune(directory: Path, keep_days: int, keep: Path) -> int:
        if keep_days <= 0:
            return 0
        cutoff = time.time() - keep_days * 86400
        removed = 0
        for path in directory.glob(f"{PREFIX}*{SUFFIX}"):
            if path != keep and path.stat().st_mtime < cutoff:
                path.unlink()
                removed += 1
        return removed
