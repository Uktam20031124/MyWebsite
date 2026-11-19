"""Dars kodi: darsning bir nechta 16:9 kadri (``Topic.lesson``) — sxema, kod qadamlari, sinov va yakun.

Ma'lumot — ``school_data/lessons_dev.py`` (kalit — mavzu kaliti), migratsiya bazaga yozadi. Sahifa —
``/mavzular/<pk>/dars/`` (← → bilan almashtirish, to'liq ekran, kadr PNG'si, tayyor kod). PNG fayllar —
``static/lessons/<kalit>/NN.png`` (shu sahifaning ``?png=1`` rejimidan Playwright bilan olinadi).

Kadrlar: 1 — umumiy sxema va reja; har kod qadamiga 1 ta (yangi qatorlar belgilangan, izoh, natija);
sinov (Telegram chat yoki brauzer natijasi, ixtiyoriy); yakun — fayllar, o'rganilganlar, uyga vazifa.
"""

from django.utils.html import escape
from django.utils.safestring import mark_safe

from .posters import RAW_FIELDS, code_html, typeset

TREE_TAGS = {"yangi": "yangi", "o‘zgardi": "ozgardi"}
# Apostrof almashtirilmaydigan maydonlar: kod, natija, fayllar, sinov va bot xabarlari.
RAW = RAW_FIELDS | {"files", "result", "run", "file", "chat", "tree"}
CODE_WIDTH_PX = 900  # kod kartasidagi qator uchun joy (1920 px kadrda, zaxira bilan)


def bank() -> dict[str, dict]:
    from .school_data.lessons_dev import LESSONS as BOT
    from .school_data.lessons_m03 import LESSONS as M03
    from .school_data.lessons_m04 import LESSONS as M04
    from .school_data.lessons_m05 import LESSONS as M05
    from .school_data.lessons_m06 import LESSONS as M06
    from .school_data.lessons_m07 import LESSONS as M07

    return {**M03, **M04, **M05, **M06, **M07, **BOT}


def run_program(lesson: dict) -> str:
    """Darsning ``run`` dasturini kiritish bilan bajaradi (randint — ixtiyoriy belgilangan son); chiqishni qaytaradi."""
    import contextlib
    import io
    import random
    from unittest import mock

    spec = lesson["run"]
    lines = iter(spec.get("input", "").split("\n"))
    out = io.StringIO()

    def fake_input(prompt=""):
        out.write(str(prompt))
        return next(lines)

    patches = [mock.patch("builtins.input", fake_input)]
    if "randint" in spec:
        patches.append(mock.patch.object(random, "randint", return_value=spec["randint"]))
    import os
    import tempfile

    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp, contextlib.ExitStack() as stack, contextlib.redirect_stdout(out):
        os.chdir(tmp)  # dastur yozadigan fayllar (tasks.json va h.k.) vaqtinchalik papkada qoladi
        try:
            for p in patches:
                stack.enter_context(p)
            exec(compile(lesson["files"][spec["file"]], spec["file"], "exec"), {"__name__": "__main__"})  # noqa: S102
        finally:
            os.chdir(cwd)
    return out.getvalue()


def png_urls(lesson: dict) -> list[str]:
    """Har kadrning PNG manzili (manifest hash bilan). PNG hali olinmagan bo'lsa — bo'sh qator."""
    from django.templatetags.static import static

    urls = []
    for n in range(1, frame_count(lesson) + 1):
        try:
            urls.append(static(f"lessons/{lesson['key']}/{n:02}.png"))
        except ValueError:  # manifest'da yo'q
            urls.append("")
    return urls


def frame_count(lesson: dict) -> int:
    return 1 + len(lesson["steps"]) + (1 if lesson.get("chat") else 0) + 1


def code_block(code: str, new, lang: str = "python") -> str:
    lines = code.split("\n")
    widest = max(len(line) for line in lines)
    by_lines = 22 if len(lines) <= 13 else 19 if len(lines) <= 17 else 17
    size = min(by_lines, int(CODE_WIDTH_PX / (0.6 * widest)))
    marked = set(new)
    rows = []
    for i, line in enumerate(lines, 1):
        css = "ln new" if i in marked else "ln"
        rows.append(f'<span class="{css}"><span class="no">{i}</span>{code_html(line, lang) or " "}</span>')
    return f'<pre style="--fs:{size}px">{"".join(rows)}</pre>'


def _foot(n: int, total: int) -> str:
    dots = "".join(f'<i class="{"on" if k <= n else ""}"></i>' for k in range(1, total + 1))
    return (
        f'<div class="foot"><div class="dots">{dots}</div><span>{n} / {total}</span>'
        '<span class="sp"></span><span>MINAR TEST · DARS KODI</span></div>'
    )


def _head(lesson: dict, title: str, sub: str = "", badge: tuple = ()) -> str:
    b = f'<div class="lbadge"><b>{escape(badge[0])}</b><span>{escape(badge[1])}</span></div>' if badge else ""
    s = f'<p class="sub">{escape(sub)}</p>' if sub else ""
    kicker = f"{escape(lesson['month'])} · {lesson['number']}-dars"
    return f'<header><div class="lkicker">{kicker}</div><h1>{escape(title)}</h1>{s}</header>{b}'


def frames(lesson: dict) -> list:
    """Har bir kadr — tayyor HTML (matn escape qilingan, kod ``code_html`` bilan)."""
    steps, total = lesson["steps"], frame_count(lesson)
    out = []
    flow = lesson.get("flow") or [
        ("▶", s["title"], s["file"], "") for s in steps[:6]
    ]
    boxes = "".join(
        f'<div class="box {escape(c)}{" end" if k == len(flow) else ""}"><i>{escape(i)}</i><b>{escape(t)}</b>'
        f"<span>{escape(d)}</span></div>"
        for k, (i, t, d, c) in enumerate(flow, 1)
    )
    loop = f'<div class="loopnote">{escape(lesson["loop"])}</div>' if lesson.get("loop") else ""
    plan = "".join(
        f"<div><b>{escape(a)} daq</b><strong>{escape(t)}</strong><span>{escape(d)}</span></div>"
        for a, t, d in lesson["plan"]
    )
    out.append(
        f'<section class="lf">{_head(lesson, lesson["title"], lesson["goal"], (str(lesson["number"]), "dars"))}'
        f'<div class="overview"><div class="before">{escape(lesson["before"])}</div>'
        f'<div class="flow" style="--n:{len(flow)}">{boxes}{loop}</div><div class="plan">{plan}</div></div>'
        f"{_foot(1, total)}</section>"
    )
    for n, s in enumerate(steps, 1):
        notes = "".join(
            f'<div class="note"><code>{escape(k)}</code><span>{v}</span></div>' for k, v in s["notes"]
        )  # izoh matni — o'zimizning ishonchli ma'lumot (<b>, <code>)
        out.append(
            f'<section class="lf">{_head(lesson, s["title"], "", (str(n), f"qadam / {len(steps)}"))}'
            f'<div class="lmain"><div class="codecard"><div class="tab"><i></i><i></i><i></i>{escape(s["file"])}</div>'
            f'{code_block(s["code"], s["new"], "python" if ".py" in s["file"] else "text")}</div>'
            f'<div class="side"><div class="notes"><h2>Nima qilyapmiz?</h2>{notes}</div>'
            f'<div class="result"><b>Natija</b><pre>{escape(s["result"])}</pre></div></div></div>'
            f"{_foot(n + 1, total)}</section>"
        )
    if lesson.get("chat"):
        chat = []
        for m in lesson["chat"]:
            chat.append(f'<div class="msg {"user" if m[0] == "user" else ""}">{escape(m[1])}</div>')
            if len(m) > 2:
                chat.append('<div class="kb">' + "".join(f"<span>{escape(b)}</span>" for b in m[2]) + "</div>")
        checks = "".join(
            f"<div><b>{i}.</b> {escape(c)}</div>" for i, c in enumerate(lesson.get("checks", []), 1)
        )
        head = _head(lesson, lesson.get("chat_title", "Sinab ko‘ramiz"), lesson.get("chat_sub", ""), ("▶", "sinov"))
        out.append(
            f'<section class="lf">{head}'
            f'<div class="chatwrap"><div class="phone">{"".join(chat)}</div><div class="checks">{checks}</div></div>'
            f"{_foot(total - 1, total)}</section>"
        )
    tree = "\n".join(
        escape(p) + (f'<em class="{TREE_TAGS.get(t, "yangi")}">{escape(t)}</em>' if t else "")
        for p, t in lesson["tree"]
    )
    learned = "".join(f"<li>{escape(x)}</li>" for x in lesson["learned"])
    hw = "".join(f"<li>{escape(x)}</li>" for x in lesson["homework"])
    head = _head(lesson, "Bugun nima qildik?", "Keyingi dars: " + lesson.get("next", ""), ("✓", "yakun"))
    out.append(
        f'<section class="lf">{head}'
        f'<div class="final"><div class="lcard"><h2>Fayllar</h2><div class="tree">{tree}</div></div>'
        f'<div class="lcard"><h2>O‘rgandik</h2><ul>{learned}</ul></div>'
        f'<div class="lcard hw"><h2>Uyga vazifa</h2><ul>{hw}</ul></div></div>{_foot(total, total)}</section>'
    )
    return [mark_safe(f) for f in out]  # noqa: S308 — har bir matn bo'lagi escape qilingan


def validate(key: str, lesson: dict) -> list[str]:
    """Kod qadamlaridagi har bir (izoh bo'lmagan) qator tayyor fayllarda bo'lishi shart."""
    errors = []
    allcode = "\n".join(lesson.get("files", {}).values())
    for s in lesson["steps"]:
        if s["file"].startswith(("Terminal", "Telegram")):  # buyruqlar, chat va natija — faylda emas
            continue
        for line in s["code"].split("\n"):
            text = line.strip()
            if text in ("", "...") or text.startswith(("#", "//", "<!--")):  # bo'sh, qisqartma va izohlar
                continue
            if line not in allcode:
                errors.append(f"{key}: {s['file']}: {text[:60]}")
        if any(n < 1 or n > s["code"].count("\n") + 1 for n in s["new"]):
            errors.append(f"{key}: {s['file']}: noto'g'ri qator raqami")
    return errors


def seed_lessons(Topic, only=None) -> int:
    """Dars kodini katalog mavzulariga yozadi (bo'lim va mavzu nomi bo'yicha). Natija: yozilganlar soni."""
    from .school_data import all_modules

    if not any(f.name == "lesson" for f in Topic._meta.get_fields()):
        return 0
    data = bank()
    done = 0
    for module in all_modules():
        for t in module.topics:
            if t.key not in data or (only is not None and t.key not in only):
                continue
            value = {**typeset(data[t.key], raw=RAW), "key": t.key, "frames": frame_count(data[t.key])}
            done += Topic.objects.filter(module__title__iexact=module.title, title__iexact=t.title).update(
                lesson=value
            )
    return done
