"""O'quv markazining haqiqiy ma'lumotlari: mavzular katalogi va guruhlar.

Bazaga ``python manage.py load_school`` yozadi. Ma'lumotni o'zgartirish uchun
shu papkadagi fayllarni tahrirlang va buyruqni qayta ishga tushiring
(qayta yuklash xavfsiz: mavjud mavzular yangilanadi, takrorlanmaydi).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TopicData:
    key: str  # guruh dasturida mavzuga havola uchun; bazaga yozilmaydi
    title: str
    description: str
    homework: str
    resources: str = ""
    minutes: int = 90


@dataclass(frozen=True)
class ModuleData:
    title: str
    description: str
    topics: list[TopicData]


@dataclass(frozen=True)
class GroupData:
    code: str
    name: str
    students: list[str]
    taught: list[str]  # o'tilgan mavzular kalitlari (dastur tartibida)
    planned: list[str]  # qolgan mavzular kalitlari (dastur tartibida)
    days: tuple[int, ...] = ()  # hafta kunlari, 0 — dushanba
    starts: str = ""  # "14:00"
    ends: str = ""  # "15:00"
    notes: str = ""


def all_modules() -> list[ModuleData]:
    from .python import MODULES as PYTHON
    from .starter import MODULES as STARTER

    return [*STARTER, *PYTHON]


def all_groups() -> list[GroupData]:
    from .groups import GROUPS

    return GROUPS
