"""O'quvchilarning Telegram/telefon ma'lumotlarini ommaviy kiritish.

Ro'yxat har qanday ko'rinishda bo'lishi mumkin (Excel, Telegram, Word'dan nusxa):
    Aliyev Sardor — @sardor_a — +998 90 123 45 67
    2) Karimova Nigina, t.me/nigina, 901234567
Har bir qatordan ism, username va telefon ajratiladi, ism mavjud o'quvchiga moslanadi.
"""

import re
from dataclasses import dataclass, field

from django.db import transaction

from .models import Student
from .telegram_sender import normalize_phone, normalize_username

_TELEGRAM_RE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:t|telegram)\.me/([A-Za-z][A-Za-z0-9_]{3,31})|@([A-Za-z][A-Za-z0-9_]{3,31})"
)
_PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{6,}\d")
_NUMBERING_RE = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s*")
_SEPARATORS = " \t-—–|,;:"
_APOSTROPHES = str.maketrans({c: "'" for c in "ʻʼ‘’`´"})


def name_key(name: str) -> tuple[str, ...]:
    """Ismni solishtirish uchun: kichik harf, apostroflar bir xil, so'zlar tartibsiz."""
    words = re.findall(r"[\w']+", name.translate(_APOSTROPHES).lower())
    return tuple(sorted(words))


@dataclass
class ContactLine:
    line_no: int
    raw: str
    name: str = ""
    username: str = ""
    phone: str = ""
    student: Student | None = None
    candidates: list = field(default_factory=list)
    error: str = ""
    changes: dict = field(default_factory=dict)  # maydon -> (eski, yangi)

    @property
    def status(self) -> str:
        if self.error:
            return "error"
        return "update" if self.changes else "same"


def parse_line(raw: str) -> tuple[str, str, str]:
    """Qatordan (ism, username, telefon) — topilmagan qismlar bo'sh."""
    text = _NUMBERING_RE.sub("", raw.strip())
    username = ""
    tg = _TELEGRAM_RE.search(text)
    if tg:
        username = normalize_username(tg.group(1) or tg.group(2))
        text = text[: tg.start()] + " " + text[tg.end() :]
    phone = ""
    ph = _PHONE_RE.search(text)
    if ph:
        phone = normalize_phone(ph.group())
        text = text[: ph.start()] + " " + text[ph.end() :]
    name = " ".join(text.split()).strip(_SEPARATORS)
    return name, username, phone


def match_students(name: str, students: list[Student]) -> list[Student]:
    key = name_key(name)
    if not key:
        return []
    exact = [s for s in students if name_key(s.full_name) == key]
    if exact:
        return exact
    # Qisqartirilgan yoki to'liq bo'lmagan ism: kiritilgan har bir so'z — o'quvchi
    # ismidagi biror so'zning boshi ("Aliyev Sard" → "Aliyev Sardor").
    return [
        s
        for s in students
        if all(any(w.startswith(k) for w in name_key(s.full_name)) for k in key)
    ]


def preview_contacts(text: str, students) -> list[ContactLine]:
    students = list(students)
    rows = []
    for n, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        name, username, phone = parse_line(raw)
        row = ContactLine(n, raw.strip(), name, username, phone)
        rows.append(row)
        if not (username or phone):
            row.error = "Telegram username ham, telefon ham topilmadi"
            continue
        if not name:
            row.error = "Ism yozilmagan"
            continue
        found = match_students(name, students)
        if not found:
            row.error = "Bunday o‘quvchi topilmadi"
            continue
        if len(found) > 1:
            row.candidates = found
            row.error = "Bir nechta o‘quvchiga mos keladi — ismni to‘liqroq yozing"
            continue
        row.student = student = found[0]
        if username and normalize_username(student.telegram) != username:
            row.changes["telegram"] = (student.telegram, username)
        if phone and normalize_phone(student.phone) != phone:
            row.changes["phone"] = (student.phone, phone)
    # Bitta o'quvchi ikki marta yozilgan bo'lsa — oxirgisi hisobga olinadi.
    seen = {}
    for row in rows:
        if row.student is not None:
            if row.student.pk in seen:
                seen[row.student.pk].error = "Bu o‘quvchi pastda yana yozilgan — o‘sha qator olinadi"
                seen[row.student.pk].changes = {}
            seen[row.student.pk] = row
    return rows


def apply_contacts(rows: list[ContactLine]) -> int:
    """Ko'rib chiqilgan o'zgarishlarni saqlaydi; yangilangan o'quvchilar soni."""
    updated = 0
    with transaction.atomic():
        for row in rows:
            if row.status != "update":
                continue
            for name, (_old, new) in row.changes.items():
                setattr(row.student, name, new)
            row.student.save(update_fields=list(row.changes))
            updated += 1
    return updated


def has_contact(student: Student) -> bool:
    return bool(normalize_username(student.telegram) or normalize_phone(student.phone))
