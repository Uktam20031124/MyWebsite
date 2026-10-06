"""Interfeys yordamchilari: ikonka, progress halqasi, mini-grafik, rang tonlari."""

import math
import zlib

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

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
def weekday_short(day) -> str:
    return _SHORT[day.weekday()]


@register.filter
def weekday_full(day) -> str:
    return _FULL[day.weekday()]


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
