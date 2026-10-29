"""Interfeys yordamchilari: ikonka, progress halqasi, mini-grafik, rang tonlari."""

import math
import re
import secrets
import zlib

from django import template
from django.utils.html import escape, format_html, json_script
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, gettext, gettext_noop

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
def intspace(value) -> str:
    """Butun son minglik ajratuvchi bilan: 1500000 → "1 500 000" (bo'shliq — ajralmas)."""
    try:
        return f"{int(value):,}".replace(",", " ")
    except (TypeError, ValueError):
        return ""


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


# JS (app.js) dagi interfeys matnlari: kalit — o'zbekcha matn, qiymat — joriy tildagi tarjima.
JS_STRINGS = [
    gettext_noop("Tungi rejim"),
    gettext_noop("Kunduzgi rejim"),
    gettext_noop("Nusxalandi ✓"),
    gettext_noop("Nusxa oling:"),
    gettext_noop("{n} / {total} tanlandi"),
    gettext_noop("Saqlanmagan o‘zgarishlar bor. Sahifadan chiqilsinmi?"),
    gettext_noop("Shogirdlar"),
    gettext_noop("Guruhlar"),
    gettext_noop("Mavzular"),
    gettext_noop("Darslar"),
    gettext_noop("Hech narsa topilmadi"),
    gettext_noop("Tezkor o‘tish"),
    gettext_noop("Buyruqlar"),
    gettext_noop("keldi"),
    gettext_noop("kechikdi"),
    gettext_noop("kelmadi"),
    gettext_noop("sababli"),
    gettext_noop("daq."),
    gettext_noop("s"),
    gettext_noop("Har bir savolga ≈ {label}."),
    gettext_noop("Vaqt juda kam bo‘lishi mumkin."),
]


@register.simple_tag
def js_i18n():
    """<script id="js-i18n" type="application/json"> — app.js shu lug'atdan o'qiydi (o'zbekchada bo'sh)."""
    data = {} if get_language() == "uz" else {k: gettext(k) for k in JS_STRINGS}
    return json_script(data, "js-i18n")


# "A'lochi" unvoni: oltin medal (ism yonida) — inline SVG, hamma joyda bir xil.
_MEDAL = (
    '<svg class="honor-medal" viewBox="0 0 24 24" width="{s}" height="{s}" role="img" aria-label="{label}">'
    "<title>{label}</title>"
    '<path d="M7 2h4l2 6H9z" fill="#2a5fa8"/><path d="M13 2h4l-2 6h-4z" fill="#c0392b"/>'
    '<circle cx="12" cy="14.5" r="7" fill="url(#honor-g)" stroke="#9c6a12" stroke-width="1"/>'
    '<path d="m12 10.4 1.25 2.55 2.8.4-2.03 1.98.48 2.79L12 16.8l-2.5 1.32.48-2.79-2.03-1.98 2.8-.4z" '
    'fill="#fff6d6"/></svg>'
)


@register.simple_tag
def honor_medal(size: int = 16):
    return format_html(_MEDAL, s=size, label=gettext("A’lochi"))


PODIUM_TITLES = {
    1: gettext_noop("Guruh reytingida 1-o‘rin"),
    2: gettext_noop("Guruh reytingida 2-o‘rin"),
    3: gettext_noop("Guruh reytingida 3-o‘rin"),
}


@register.filter
def person_name(person):
    """O'quvchi ismi. "A'lochi" — medal bilan; guruh quvvat reytingida 1–3-o'rin — oltin,
    kumush, bronza rangda (bo'lmasa "A'lochi" oltini). Hamma ko'radigan joylarda bir xil."""
    from academy.engagement import podium_places

    if isinstance(person, dict):
        name, honor, pk = person.get("full_name", ""), person.get("honor_since"), person.get("id")
    else:
        name = getattr(person, "full_name", "") or str(person or "")
        honor = getattr(person, "honor_since", None)
        pk = getattr(person, "pk", None) if hasattr(person, "group_id") else None
    place = podium_places().get(pk) if pk else None
    medal = honor_medal(15) if honor else ""
    if place:
        title = gettext(PODIUM_TITLES[place])
        classes = f"{'honor-name ' if honor else ''}podium-name podium-{place}"
        return format_html('{}<span class="{}" title="{}">{}</span>', medal, classes, title, name)
    if not honor:
        return name
    # Medal ism oldida: uzun ism qisqartirilganda (…) ham ko'rinib turadi.
    return format_html('{}<span class="honor-name">{}</span>', medal, name)


@register.simple_tag
def form_nonce():
    """Bir martalik forma kaliti (takroriy yuborishdan himoya, ``profile_views._fresh_nonce``)."""
    return format_html('<input type="hidden" name="nonce" value="{}">', secrets.token_hex(8))
