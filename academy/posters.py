"""Dars rasmlari: har bir mavzu uchun proyektorga mo'ljallangan 16:9 poster (``Topic.poster``).

Ma'lumot — ``school_data/posters_*.py`` (kalit — mavzu kaliti), migratsiya bazaga yozadi. Sahifa —
``/mavzular/<pk>/rasm/`` (to'liq ekran, PNG yuklab olish, ustoz uchun javoblar). PNG fayllar —
``static/posters/<kalit>.png`` (shu sahifadan Playwright bilan olinadi).

Markaziy ko'rgazma turlari (``VISUALS``):
- ``keyboard`` — barmoqlar xaritasi (ma'lumotsiz);
- ``window`` — ilova oynasi sxemasi: {"app": nom, "parts": [(nomi, izoh, ko'rinish), ...]},
  ko'rinish: field | button | area | list | tabs;
- ``code`` — kod va natija: {"code": python, "output": matn, "lang": "python"|"text"};
- ``flow`` — qadamlar: [(sarlavha, izoh), ...];
- ``compare`` — yomon/yaxshi: {"bad": (sarlavha, [bandlar]), "good": (sarlavha, [bandlar])};
- ``tiles`` — tushunchalar: [(katta belgi, nomi, izoh), ...];
- ``anatomy`` — rangli qismlarga ajratilgan jumla/prompt: [(qism nomi, matn), ...].
"""

import keyword
import re

from django.utils.html import escape
from django.utils.safestring import mark_safe

VISUALS = {"keyboard", "window", "code", "flow", "compare", "tiles", "anatomy"}
OPS = "÷×=+−→≥≤≠"
_OP = re.compile(f"[{OPS}]")


def bank() -> dict[str, dict]:
    from .school_data.posters_ai import POSTERS as AI
    from .school_data.posters_iq import POSTERS as IQ
    from .school_data.posters_python import POSTERS as PYTHON
    from .school_data.posters_starter import POSTERS as STARTER

    return {**STARTER, **PYTHON, **AI, **IQ}


def formula_html(text: str):
    """"a ÷ 5 = [WPM]" → amallar rangli, [..] — natija nishoni. Matn avval escape qilinadi."""
    out = []
    for part in re.split(r"(\[[^\]]+\])", text):
        if part.startswith("[") and part.endswith("]"):
            out.append(f'<span class="eq">{escape(part[1:-1])}</span>')
            continue
        out.append(_OP.sub(r'<span class="op">\g<0></span>', str(escape(part))))
    return mark_safe("".join(out))  # noqa: S308 — matn escape qilingan


_TOKEN = re.compile(
    r"(?P<comment>#[^\n]*)|(?P<string>f?\"[^\"\n]*\"|f?'[^'\n]*')|(?P<number>\b\d+(?:\.\d+)?\b)|(?P<word>\b[A-Za-z_]\w*\b)"
)
BUILTINS = set(
    "print input len range int str float bool list dict set tuple type sum min max sorted map filter open round abs "
    "enumerate zip".split()
)


def code_html(code: str, lang: str = "python"):
    """Oddiy rang berish: kalit so'zlar, satrlar, sonlar, izohlar, standart funksiyalar."""
    if lang != "python":
        return mark_safe(str(escape(code)))  # noqa: S308
    out, pos = [], 0
    for m in _TOKEN.finditer(code):
        out.append(str(escape(code[pos : m.start()])))
        text, kind = m.group(0), m.lastgroup
        if kind == "word":
            css = "kw" if keyword.iskeyword(text) else "bi" if text in BUILTINS else ""
        else:
            css = {"comment": "cm", "string": "st", "number": "nu"}[kind]
        out.append(f'<span class="{css}">{escape(text)}</span>' if css else str(escape(text)))
        pos = m.end()
    out.append(str(escape(code[pos:])))
    return mark_safe("".join(out))  # noqa: S308 — har bir bo'lak escape qilingan


def validate(key: str, p: dict) -> list[str]:
    errors = []
    if p["visual"]["kind"] not in VISUALS:
        errors.append(f"{key}: noma'lum ko'rgazma {p['visual']['kind']}")
    if len(p["cards"]) != 3:
        errors.append(f"{key}: 3 ta karta kerak ({len(p['cards'])})")
    if len(p["questions"]) != 3:
        errors.append(f"{key}: 3 ta savol kerak ({len(p['questions'])})")
    return errors


RAW_FIELDS = {"code", "output", "keys", "lang", "kind", "image", "key"}
_APOS = re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])")


def typeset(value, field: str = ""):
    """O'zbekcha apostrofni tipografik ‘ ga almashtiradi (o'z → o‘z); kod va tugmalarga tegmaydi."""
    if isinstance(value, str):
        return value if field in RAW_FIELDS else _APOS.sub("\u2018", value)
    if isinstance(value, dict):
        return {k: typeset(v, k if k in RAW_FIELDS else field) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [typeset(v, field) for v in value]
    return value


def seed_posters(Topic, only=None) -> int:
    """Postelarni katalog mavzulariga yozadi (mavzu nomi va bo'limi bo'yicha). Natija: yozilganlar soni."""
    from .school_data import all_modules

    if not any(f.name == "poster" for f in Topic._meta.get_fields()):
        return 0
    data = bank()
    done = 0
    for module in all_modules():
        for t in module.topics:
            if t.key not in data or (only is not None and t.key not in only):
                continue
            value = {**typeset(data[t.key]), "key": t.key, "image": f"posters/{t.key}.png"}
            done += Topic.objects.filter(module__title__iexact=module.title, title__iexact=t.title).update(
                poster=value
            )
    return done
