"""Dars taqdimoti: ``Topic.slides`` matnini slaydlarga ajratish va xavfsiz HTML'ga aylantirish.

Format: slaydlar orasida ``---`` qatori; ``# `` — sarlavha slaydi (katta, markazda); ``!! `` — katta
ibora; ``:: timer N`` — N daqiqalik taymer; qolgan qatorlar — ``study_md`` (## / ###, ro'yxat, > eslatma,
``` kod ```, `kod`, **qalin**). Kod bloki ichidagi ``---`` ajratuvchi hisoblanmaydi.
"""

import re

from django.utils.safestring import mark_safe

from .templatetags.ui import _inline, study_md

_TIMER = re.compile(r"^::\s*timer\s+(\d{1,3})\s*$", re.I)
MAX_TIMER = 180


def split_slides(text: str) -> list[str]:
    chunks, current, in_code = [], [], False
    for line in (text or "").splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and line.strip() == "---":
            chunks.append("\n".join(current))
            current = []
        else:
            current.append(line)
    chunks.append("\n".join(current))
    return [c.strip("\n") for c in chunks if c.strip()]


def render_slide(text: str) -> dict:
    lines = text.splitlines()
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines.pop(0)[2:].strip()
    timer, parts, buffer, in_code = 0, [], [], False

    def flush():
        if buffer:
            parts.append(str(study_md("\n".join(buffer))))
            buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
        if not in_code and (m := _TIMER.match(stripped)):
            timer = min(int(m.group(1)), MAX_TIMER)
        elif not in_code and stripped.startswith("!! "):
            flush()
            parts.append(f'<p class="slide-big">{_inline(stripped[3:])}</p>')
        else:
            buffer.append(line)
    flush()
    return {
        "is_title": bool(title),
        "title": mark_safe(_inline(title)) if title else "",  # noqa: S308 — _inline escape qiladi
        "html": mark_safe("".join(parts)),  # noqa: S308 — study_md va _inline escape qiladi
        "timer": timer,
    }


def deck(text: str) -> list[dict]:
    return [render_slide(chunk) for chunk in split_slides(text)]
