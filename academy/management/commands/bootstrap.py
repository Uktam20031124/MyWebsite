import os
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from academy.models import (
    Attendance,
    Group,
    Lesson,
    Student,
    SyllabusItem,
)
from academy.services import import_topics, parse_topics

DEFAULT_PASSWORD = "darsxona2026"

# Import formatidagi demo katalog (ommaviy import bilan bir xil yo'ldan o'tadi).
DEMO_TOPICS = """
# Python asoslari
1. Kirish va muhit — Kompyuter, terminal, VS Code, dasturlash nima.
2. O'zgaruvchilar va turlar — int, str, bool, input/print.
3. Shart operatorlari — if / elif / else, mantiqiy ifodalar.
4. Sikllar — for, while, range, break/continue.
5. Funksiyalar — def, argumentlar, return, scope.
6. Ro'yxat va lug'at — list, dict, tuple, set.
7. Xatolar va fayllar — try/except, ochish/yozish.
8. OOP asoslari — class, obyekt, metodlar.

# Veb asoslari
1. Git va GitHub — commit, branch, push, PR.
2. HTML asoslari — semantik markup, formalar.
3. CSS asoslari — layout, flex, responsive.
4. JavaScript asoslari — DOM, hodisalar, fetch.

# Django
1. Django kirish — loyiha, app, url, view, template.
2. Django modellar — ORM, migratsiya, admin.
3. Mini loyiha — Yakuniy amaliy ish.
"""


STUDENTS = {
    "PY-01": [
        ("Aliyev Sardor", "+998 90 111 22 33", "sardor_dev"),
        ("Karimova Madina", "+998 91 222 33 44", "madina_k"),
        ("Tursunov Javohir", "+998 93 333 44 55", "javohir_t"),
        ("Nazarova Sevinch", "+998 94 444 55 66", "sevinch_n"),
        ("Rahimov Behruz", "+998 95 555 66 77", "behruz_r"),
        ("Usmonova Dilnoza", "+998 97 666 77 88", "dilnoza_u"),
        ("Ergashev Aziz", "+998 88 777 88 99", "aziz_e"),
        ("Saidova Nigora", "+998 99 888 99 00", "nigora_s"),
    ],
    "FE-02": [
        ("Ismoilov Diyor", "+998 90 121 21 21", "diyor_iso"),
        ("Qodirova Laylo", "+998 91 131 31 31", "laylo_q"),
        ("Mamatov Umid", "+998 93 141 41 41", "umid_m"),
        ("Xolmatova Malika", "+998 94 151 51 51", "malika_x"),
        ("Sobirov Jasur", "+998 95 161 61 61", "jasur_s"),
        ("To‘xtayeva Sabina", "+998 97 171 71 71", "sabina_t"),
    ],
    "DJ-01": [
        ("Abdullayev Kamron", "+998 90 181 81 81", "kamron_a"),
        ("Yunusova Parizoda", "+998 91 191 91 91", "parizoda_y"),
        ("Hasanov Shohruh", "+998 93 202 02 02", "shohruh_h"),
        ("Olimova Rayhona", "+998 94 212 12 12", "rayhona_o"),
        ("Mirzayev Farrux", "+998 95 222 22 22", "farrux_m"),
    ],
}


class Command(BaseCommand):
    help = (
        "Ustoz hisobini yaratadi va bo'sh bazaga namuna ma'lumot yozadi. "
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
            "--no-demo", action="store_true", help="Namuna guruh/shogird/darslarsiz"
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
            self.stdout.write("Bazada guruhlar bor — namuna ma'lumotlar yozilmadi.")
            return

        topics = import_topics(parse_topics(DEMO_TOPICS)).topics

        groups_spec = [
            ("Python asoslari N1", "PY-01", "Du / Chor 18:00–20:00", "Xona 3"),
            ("Frontend N2", "FE-02", "Se / Pay 17:30–19:30", "Xona 1"),
            ("Django N1", "DJ-01", "Shanba 10:00–13:00", "Xona 2"),
        ]
        today = timezone.localdate()
        groups = {}
        for name, code, schedule, room in groups_spec:
            g, _ = Group.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "schedule": schedule,
                    "room": room,
                    "start_date": today.replace(day=1) if today.day > 1 else today,
                    "status": Group.Status.ACTIVE,
                },
            )
            groups[code] = g
            for i, topic in enumerate(topics, start=1):
                SyllabusItem.objects.get_or_create(
                    group=g, topic=topic, defaults={"order": i}
                )

        for code, people in STUDENTS.items():
            g = groups[code]
            for full_name, phone, tg in people:
                Student.objects.get_or_create(
                    group=g,
                    full_name=full_name,
                    defaults={"phone": phone, "telegram": tg},
                )

        # Past lessons + attendance for PY-01
        py = groups["PY-01"]
        py_students = list(py.students.filter(status=Student.Status.ACTIVE))
        for offset, topic in enumerate(topics[:4]):
            day = today - timedelta(days=(4 - offset) * 2)
            lesson, _ = Lesson.objects.get_or_create(
                group=py,
                held_on=day,
                topic=topic,
                defaults={
                    "starts_at": datetime.strptime("18:00", "%H:%M").time(),
                    "status": Lesson.Status.COMPLETED,
                    "homework": "Mavzu bo‘yicha 5 ta mashq.",
                },
            )
            SyllabusItem.objects.filter(group=py, topic=topic).update(
                status=SyllabusItem.Status.TAUGHT, taught_on=day
            )
            for i, st in enumerate(py_students):
                status = Attendance.Status.PRESENT
                if i == offset:
                    status = Attendance.Status.ABSENT
                elif i == offset + 1:
                    status = Attendance.Status.LATE
                Attendance.objects.get_or_create(
                    lesson=lesson, student=st, defaults={"status": status}
                )

        Lesson.objects.get_or_create(
            group=py,
            held_on=today,
            defaults={
                "topic": topics[4],
                "starts_at": datetime.strptime("18:00", "%H:%M").time(),
                "status": Lesson.Status.PLANNED,
                "notes": "Bugungi dars — funksiyalar.",
            },
        )
        Lesson.objects.get_or_create(
            group=groups["FE-02"],
            held_on=today + timedelta(days=1),
            defaults={
                "topic": topics[9],
                "starts_at": datetime.strptime("17:30", "%H:%M").time(),
                "status": Lesson.Status.PLANNED,
            },
        )
        Lesson.objects.get_or_create(
            group=groups["DJ-01"],
            held_on=today + timedelta(days=2),
            defaults={
                "topic": topics[12],
                "starts_at": datetime.strptime("10:00", "%H:%M").time(),
                "status": Lesson.Status.PLANNED,
            },
        )

        self.stdout.write(self.style.SUCCESS("Namuna ma'lumotlar tayyor."))
