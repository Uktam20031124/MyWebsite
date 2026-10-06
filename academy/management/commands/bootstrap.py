import os

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from academy.models import Group

DEFAULT_PASSWORD = "darsxona2026"


class Command(BaseCommand):
    help = (
        "Ustoz hisobini yaratadi va bo'sh bazaga o'quv markazi ma'lumotlarini "
        "(academy/school_data: guruhlar, o'quvchilar, mavzular) yozadi. "
        "Parol: --password yoki DARSXONA_PASSWORD (aks holda dev paroli)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--username", default="ustoz")
        parser.add_argument("--password", default=None)
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="Mavjud foydalanuvchi parolini ham qayta o'rnatish",
        )
        parser.add_argument(
            "--no-demo", action="store_true", help="Faqat ustoz hisobi (guruh/o'quvchilarsiz)"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options["username"]
        password = (
            options["password"] or os.environ.get("DARSXONA_PASSWORD") or DEFAULT_PASSWORD
        )
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": "Oktam",
                "last_name": "Mustafoyev",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created or options["reset_password"]:
            user.set_password(password)
            user.save()
            shown = password if password == DEFAULT_PASSWORD else "********"
            self.stdout.write(self.style.SUCCESS(f"Kirish: {username} / {shown}"))
        else:
            self.stdout.write(f"“{username}” allaqachon bor — parol o'zgartirilmadi.")
        if password == DEFAULT_PASSWORD and (created or options["reset_password"]):
            self.stdout.write(
                self.style.WARNING("Diqqat: dev paroli ishlatildi. Production'da almashtiring!")
            )

        if options["no_demo"]:
            return
        if Group.objects.exists():
            self.stdout.write("Bazada guruhlar bor — o'quv ma'lumotlari yozilmadi.")
            return

        call_command("load_school", stdout=self.stdout)
