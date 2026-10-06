import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from academy.models import Attendance, Group, Lesson, Module, Student, SyllabusItem, Topic
from academy.school_data import GroupData, ModuleData, all_groups, all_modules


def validate(modules: list[ModuleData], groups: list[GroupData]) -> list[str]:
    """Ma'lumotlardagi xatolar ro'yxati (bo'sh — hammasi joyida)."""
    errors = []
    keys: dict[str, str] = {}
    titles: set[tuple[str, str]] = set()
    module_titles: set[str] = set()
    for module in modules:
        if module.title.lower() in module_titles:
            errors.append(f"Bo'lim takrorlangan: {module.title}")
        module_titles.add(module.title.lower())
        for topic in module.topics:
            if topic.key in keys:
                errors.append(f"Mavzu kaliti takrorlangan: {topic.key}")
            keys[topic.key] = topic.title
            if (module.title, topic.title.lower()) in titles:
                errors.append(f"{module.title}: mavzu takrorlangan: {topic.title}")
            titles.add((module.title, topic.title.lower()))
            if len(topic.title) > Topic._meta.get_field("title").max_length:
                errors.append(f"{topic.key}: nom juda uzun")

    codes: set[str] = set()
    for group in groups:
        if group.code.upper() in codes:
            errors.append(f"Guruh kodi takrorlangan: {group.code}")
        codes.add(group.code.upper())
        syllabus = [*group.taught, *group.planned]
        for key in syllabus:
            if key not in keys:
                errors.append(f"{group.code}: noma'lum mavzu kaliti {key}")
        duplicates = sorted({k for k in syllabus if syllabus.count(k) > 1})
        if duplicates:
            errors.append(f"{group.code}: dasturda takrorlangan mavzular: {', '.join(duplicates)}")
        names = [" ".join(n.split()) for n in group.students]
        if len(set(names)) != len(names):
            errors.append(f"{group.code}: o'quvchi ismi takrorlangan")
    return errors


class Command(BaseCommand):
    help = (
        "O'quv markazi ma'lumotlarini (academy/school_data) bazaga yozadi: mavzular katalogi, "
        "guruhlar, o'quvchilar va guruh dasturlari. Qayta ishga tushirish xavfsiz. "
        "--reset avval barcha o'quv ma'lumotlarini o'chiradi (foydalanuvchilar qoladi)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Avval guruh, o'quvchi, mavzu, dars va yo'qlamalarni o'chirish",
        )
        parser.add_argument("--yes", action="store_true", help="--reset uchun tasdiq so'ramaslik")

    def handle(self, *args, reset, yes, **options):
        modules, groups = all_modules(), all_groups()
        errors = validate(modules, groups)
        if errors:
            raise CommandError("Ma'lumotlarda xato:\n  " + "\n  ".join(errors))

        if reset and not yes:
            self.confirm_reset()

        with transaction.atomic():
            if reset:
                self.reset()
            topics = self.load_topics(modules)
            for group in groups:
                self.load_group(group, topics)

        self.stdout.write(
            self.style.SUCCESS(
                f"Tayyor: {len(modules)} bo'lim, {len(topics)} mavzu, {len(groups)} guruh, "
                f"{sum(len(g.students) for g in groups)} o'quvchi."
            )
        )

    def confirm_reset(self):
        if not sys.stdin.isatty():
            raise CommandError("--reset tasdiq talab qiladi: --yes qo'shing.")
        counts = ", ".join(
            f"{model._meta.verbose_name_plural}: {model.objects.count()}"
            for model in (Group, Student, Topic, Lesson, Attendance)
        )
        self.stdout.write(self.style.WARNING(f"O'chiriladi — {counts}."))
        if input("Davom etilsinmi? [ha/yo'q] ").strip().lower() not in ("ha", "h", "yes", "y"):
            raise CommandError("Bekor qilindi.")

    def reset(self):
        # Tartib muhim emas (CASCADE), lekin aniq bo'lsin: avval bog'liq yozuvlar.
        for model in (Attendance, Lesson, SyllabusItem, Student, Group, Topic, Module):
            model.objects.all().delete()
        self.stdout.write("Eski o'quv ma'lumotlari o'chirildi.")

    def load_topics(self, modules: list[ModuleData]) -> dict[str, Topic]:
        topics: dict[str, Topic] = {}
        for m_order, data in enumerate(modules, start=1):
            module = Module.objects.filter(title__iexact=data.title).first() or Module(title=data.title)
            module.description = data.description
            module.order = m_order * 10
            module.save()
            for t_order, t in enumerate(data.topics, start=1):
                topic = (
                    Topic.objects.filter(module=module, title__iexact=t.title).first()
                    or Topic(module=module, title=t.title)
                )
                topic.description = t.description
                topic.homework = t.homework
                topic.resources = t.resources
                topic.duration_minutes = t.minutes
                topic.order = t_order * 10
                topic.is_active = True
                topic.save()
                topics[t.key] = topic
        return topics

    def load_group(self, data: GroupData, topics: dict[str, Topic]):
        group = Group.objects.filter(code__iexact=data.code).first() or Group(code=data.code)
        group.name = data.name
        group.schedule = data.schedule or group.schedule
        group.notes = data.notes or group.notes
        group.status = Group.Status.ACTIVE
        group.save()

        for full_name in data.students:
            Student.objects.get_or_create(group=group, full_name=" ".join(full_name.split()))

        taught = set(data.taught)
        # Dastur tartibi har safar fayldagi tartibga keltiriladi; holatlar esa
        # faqat oldinga siljiydi (darslar orqali "o'tildi" bo'lganlari saqlanadi).
        for order, key in enumerate([*data.taught, *data.planned], start=1):
            item, _ = SyllabusItem.objects.get_or_create(
                group=group, topic=topics[key], defaults={"order": order}
            )
            item.order = order
            if key in taught and item.status == SyllabusItem.Status.PLANNED:
                item.status = SyllabusItem.Status.TAUGHT
            item.save(update_fields=["order", "status"])

        self.stdout.write(
            f"  {group.code}: {len(data.students)} o'quvchi, "
            f"{len(taught)} o'tilgan + {len(data.planned)} rejadagi mavzu"
        )
