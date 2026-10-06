from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from academy.models import (
    Attendance,
    Group,
    Lesson,
    Student,
    SyllabusItem,
    Topic,
)

TOPICS = [
    ("Kirish va muhit", "Kompyuter, terminal, VS Code, dasturlash nima."),
    ("O'zgaruvchilar va turlar", "int, str, bool, input/print."),
    ("Shart operatorlari", "if / elif / else, mantiqiy ifodalar."),
    ("Sikllar", "for, while, range, break/continue."),
    ("Funksiyalar", "def, argumentlar, return, scope."),
    ("Ro'yxat va lug'at", "list, dict, tuple, set."),
    ("Xatolar va fayllar", "try/except, ochish/yozish."),
    ("OOP asoslari", "class, obyekt, metodlar."),
    ("Git va GitHub", "commit, branch, push, PR."),
    ("HTML asoslari", "semantik markup, formalar."),
    ("CSS asoslari", "layout, flex, responsive."),
    ("JavaScript asoslari", "DOM, hodisalar, fetch."),
    ("Django kirish", "loyiha, app, url, view, template."),
    ("Django modellar", "ORM, migratsiya, admin."),
    ("Mini loyiha", "Yakuniy amaliy ish."),
]


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
    help = "Ustoz hisobi va namuna ma'lumotlarini yaratadi."

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="ustoz",
            defaults={
                "first_name": "Oktam",
                "last_name": "Mustafoyev",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.set_password("darsxona2026")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                "Kirish: ustoz / darsxona2026"
                if created
                else "Ustoz paroli yangilandi: ustoz / darsxona2026"
            )
        )

        topics = []
        for i, (title, desc) in enumerate(TOPICS, start=1):
            t, _ = Topic.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "order": i * 10,
                    "duration_minutes": 90,
                },
            )
            topics.append(t)

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
