"""Interfeys yordamchilari: ikonka, progress halqasi, mini-grafik, rang tonlari."""

import math
import re
import zlib

from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, gettext

from academy.models import WEEKDAYS

register = template.Library()

_FULL = {n: full for n, full, _ in WEEKDAYS}
_SHORT = {n: short for n, _, short in WEEKDAYS}


@register.simple_tag
def icon(name: str, size: int = 18, cls: str = ""):
    """SVG sprite'dagi ikonka (base.html ichidagi <symbol id="i-...">)."""
    return format_html(
        '<svg class="i {}" width="{}" height="{}" aria-hidden="true" focusable="false">'
        '<use href="#i-{}"></use></svg>',
        cls,
        size,
        size,
        name,
    )


@register.filter
def hue(value) -> int:
    """Barqaror rang tusi (0–359): avatar/guruh har safar bir xil rangda.

    Model obyekti uchun — id bo'yicha "oltin burchak" (137.5°): ketma-ket guruhlar
    har doim aniq farqli rangda. Matn uchun — hash.
    """
    if getattr(value, "pk", None) is not None:
        return round(value.pk * 137.508 + 150) % 360
    return zlib.crc32(str(value).encode()) % 360


@register.filter
def tone(pct) -> str:
    """Foiz/ball uchun semantik ton: ok | warn | bad ("" — ma'lumot yo'q)."""
    if pct is None or pct == "":
        return ""
    pct = float(pct)
    return "ok" if pct >= 85 else "warn" if pct >= 70 else "bad"


@register.filter
def quiz_tone(pct) -> str:
    """Test foizi uchun ton — test sahifalaridagi bilan bir xil: 80+ ok, 50+ warn."""
    if pct is None or pct == "":
        return ""
    pct = float(pct)
    return "ok" if pct >= 80 else "warn" if pct >= 50 else "bad"


@register.filter
def weekday_short(day) -> str:
    return gettext(_SHORT[day.weekday()])


@register.filter
def weekday_full(day) -> str:
    return gettext(_FULL[day.weekday()])


@register.simple_tag
def ring(pct, size: int = 64, stroke: int = 6, label: str = ""):
    """Aylana progress (0–100). Markazda foiz yoki berilgan yozuv."""
    pct = max(0, min(100, int(pct or 0)))
    r = (size - stroke) / 2
    c = 2 * math.pi * r
    return format_html(
        '<svg class="ring" width="{s}" height="{s}" viewBox="0 0 {s} {s}" role="img" '
        'aria-label="{p}%">'
        '<circle class="ring-track" cx="{h}" cy="{h}" r="{r}" stroke-width="{w}"/>'
        '<circle class="ring-value" cx="{h}" cy="{h}" r="{r}" stroke-width="{w}" '
        'stroke-dasharray="{c}" stroke-dashoffset="{o}" '
        'transform="rotate(-90 {h} {h})"/>'
        '<text x="50%" y="50%" dominant-baseline="central" text-anchor="middle">{t}</text>'
        "</svg>",
        s=size,
        h=size / 2,
        r=r,
        w=stroke,
        # format_html argumentlarni matnga aylantiradi — sonlar oldindan formatlanadi.
        c=f"{c:.2f}",
        o=f"{c * (1 - pct / 100):.2f}",
        p=pct,
        t=label or f"{pct}%",
    )


@register.simple_tag
def sparkline(values, width: int = 220, height: int = 56):
    """0–100 oralig'idagi qiymatlar uchun mini-grafik. None — uzilish (ma'lumot yo'q)."""
    values = list(values)
    if sum(v is not None for v in values) < 2:
        return mark_safe('<div class="spark-empty">Grafik uchun ma’lumot yetarli emas</div>')
    pad = 4
    step = (width - pad * 2) / max(1, len(values) - 1)

    def xy(i, v):
        return pad + i * step, pad + (100 - v) / 100 * (height - pad * 2)

    runs, run = [], []
    for i, v in enumerate(values):
        if v is None:
            if run:
                runs.append(run)
            run = []
        else:
            run.append(xy(i, v))
    if run:
        runs.append(run)

    lines, areas = [], []
    for pts in runs:
        coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        lines.append(f'<polyline class="spark-line" points="{coords}"/>')
        if len(pts) > 1:
            base = height - pad
            areas.append(
                f'<path class="spark-area" d="M{pts[0][0]:.1f},{base} L{coords.replace(" ", " L")} '
                f'L{pts[-1][0]:.1f},{base} Z"/>'
            )
    lx, ly = runs[-1][-1]
    return mark_safe(
        f'<svg class="spark" viewBox="0 0 {width} {height}" aria-hidden="true">'
        f'{"".join(areas)}{"".join(lines)}'
        f'<circle class="spark-dot" cx="{lx:.1f}" cy="{ly:.1f}" r="3.2"/></svg>'
    )


_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _inline(text: str) -> str:
    """Bitta qator: avval escape, keyin `kod` va **qalin** (kod ichida qalin ishlamaydi)."""
    parts = _INLINE_CODE.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(f"<code>{escape(part)}</code>")
        else:
            out.append(_BOLD.sub(r"<strong>\1</strong>", str(escape(part))))
    return "".join(out)


@register.filter
def study_md(text: str):
    """Mustahkamlash materiali uchun kichik, xavfsiz Markdown: ## / ### sarlavha,
    - va 1. ro'yxat, > eslatma, ``` kod bloki, `kod`, **qalin**. HTML kiritib bo'lmaydi."""
    html, para, items, list_tag = [], [], [], ""
    code = None

    def flush():
        nonlocal list_tag
        if para:
            html.append(f"<p>{' '.join(_inline(p) for p in para)}</p>")
            para.clear()
        if items:
            html.append(f"<{list_tag}>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + f"</{list_tag}>")
            items.clear()
            list_tag = ""

    for raw in (text or "").splitlines():
        if code is not None:
            if raw.strip().startswith("```"):
                html.append(f'<pre class="quiz-code study-code"><code>{escape(chr(10).join(code))}</code></pre>')
                code = None
            else:
                code.append(raw)
            continue
        line = raw.strip()
        if line.startswith("```"):
            flush()
            code = []
        elif not line:
            flush()
        elif line.startswith("### "):
            flush()
            html.append(f"<h4>{_inline(line[4:])}</h4>")
        elif line.startswith("## "):
            flush()
            html.append(f"<h3>{_inline(line[3:])}</h3>")
        elif line.startswith("> "):
            flush()
            html.append(f'<div class="study-note">{_inline(line[2:])}</div>')
        elif re.match(r"^(- |\d+\. )", line):
            tag = "ul" if line.startswith("- ") else "ol"
            if para or (items and tag != list_tag):
                flush()
            list_tag = tag
            items.append(re.sub(r"^(- |\d+\. )", "", line))
        else:
            if items:
                flush()
            para.append(line)
    if code is not None:
        html.append(f'<pre class="quiz-code study-code"><code>{escape(chr(10).join(code))}</code></pre>')
    flush()
    return mark_safe("".join(html))  # noqa: S308 — hamma matn escape qilingan


@register.filter
def topic_title(topic) -> str:
    """Mavzu nomi joriy interfeys tilida (ruschasi bo'lmasa — o'zbekcha); mavzu yo'q — ""."""
    return topic.title_in(get_language()) if topic else ""
