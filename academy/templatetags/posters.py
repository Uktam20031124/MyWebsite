"""Dars rasmlari (poster) uchun shablon filtrlari: formula, kod va klaviatura tugmalari."""

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from academy.posters import code_html, formula_html, typeset

register = template.Library()

FINGER_OF = {
    **dict.fromkeys("`1QAZ0P;/-=['", "p"),
    **dict.fromkeys("2WSX9OL.", "r"),
    **dict.fromkeys("3EDC8IK,", "m"),
    **dict.fromkeys("45RTFGVB", "il"),
    **dict.fromkeys("67YUHJNM", "ir"),
}
HOME_KEYS = set("ASDFJKL;")


@register.filter
def poster_formula(text: str):
    return formula_html(text or "")


@register.filter
def poster_code(code: str, lang: str = "python"):
    return code_html(code or "", lang or "python")


@register.filter
def poster_keys(keys: str):
    """"ASDF JKL;" → klaviatura tugmalari (barmoq rangi, uy qatori, F/J bo'rtig'i); bo'shliq — oraliq."""
    out = []
    for ch in keys or "":
        if ch == " ":
            out.append('<span class="sep"></span>')
            continue
        up = ch.upper()
        classes = ["pp-k", FINGER_OF.get(up, "")]
        if up in HOME_KEYS:
            classes.append("home")
        if up in "FJ":
            classes.append("bump")
        out.append(f'<span class="{" ".join(c for c in classes if c)}">{escape(ch)}</span>')
    return mark_safe("".join(out))  # noqa: S308 — har bir belgi escape qilingan


@register.filter
def poster_seg_class(index: int) -> str:
    return f"c{int(index) % 6}"


@register.filter
def poster_typeset(text: str) -> str:
    return typeset(text or "")
