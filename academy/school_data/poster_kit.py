"""Dars rasmlari (poster) uchun ma'lumot yozish yordamchilari — ``posters_*.py`` fayllari ishlatadi.

Har bir poster: maqsad, markaziy ko'rgazma (``visual``), 3 ta karta, qoida va "Test oldidan" 3 ta savol
(javoblari faqat ustozga ko'rinadi). Ko'rgazma turlari va ma'lumot shakli — ``academy.posters.VISUALS``.

Formulada ``[...]`` — natija belgisi (oltin nishon), ``÷ × = + − → ≥ ≤`` — rangli amallar.
"""


def card(title: str, text: str = "", formula: str = "", example: str = "", keys: str = "", code: str = "") -> dict:
    return {"title": title, "text": text, "formula": formula, "example": example, "keys": keys, "code": code}


# "Kod va natija" ko'rgazmasi (1920 px poster): belgi sig'imi va qator balandligi shrift o'lchamiga qarab.
CODE_CHARS = {"": 36, "s": 42, "xs": 48}  # kod ustuni yonma-yon; ustma-ust — 1.75 baravar keng
OUT_CHARS = {"": 22, "s": 25, "xs": 29}
LINE_PX = {"": 38.7, "s": 33.3, "xs": 28.2}
HEIGHT_PX = 560


def code_layout(src: str, output: str) -> tuple[str, bool]:
    """Eng katta sig'adigan shrift va joylashuv: yonma-yon yoki natija kod ostida (``stack``)."""
    cw = max(len(line) for line in src.split("\n"))
    ow = max(len(line) for line in output.split("\n"))
    cl, ol = src.count("\n") + 1, output.count("\n") + 1
    for size in ("", "s", "xs"):
        for stack in (False, True):
            wide = CODE_CHARS[size] * (1.75 if stack else 1)
            height = (cl + ol) * LINE_PX[size] + 120 if stack else max(cl, ol) * LINE_PX[size]
            if cw <= wide and ow <= (wide if stack else OUT_CHARS[size]) and height <= HEIGHT_PX:
                return size, stack
    return "xs", True


def code(src: str, output: str, lang: str = "python", run: bool = True) -> tuple:
    """Kod va natija ko'rgazmasi. ``run=False`` — kod bu yerda ishga tushmaydi (masalan, Telegram bot)."""
    src, output = src.strip("\n"), output.strip("\n")
    size, stack = code_layout(src, output)
    return ("code", {"code": src, "output": output, "lang": lang, "run": run, "size": size, "stack": stack})


def poster(
    goal: str, visual: tuple, cards: list, rule: tuple, questions: list, title: str = "", badge: tuple = ()
) -> dict:
    """``visual`` = (tur, ma'lumot); ``rule`` = (sarlavha, izoh); ``questions`` = [(savol, javob), ...];
    ``badge`` = (katta belgi, izoh) — sarlavha yonidagi nishon (ixtiyoriy)."""
    kind, data = visual
    if kind == "code" and "size" not in data:  # xom ("code", {...}) — o'lcham va joylashuvni hisoblash
        data = code(data["code"], data["output"], data.get("lang", "python"), run=data.get("run", False))[1]
    return {
        "badge": list(badge),
        "goal": goal,
        "visual_title": title,
        "visual": {"kind": kind, "data": data},
        "cards": cards,
        "rule": {"title": rule[0], "text": rule[1] if len(rule) > 1 else ""},
        "questions": [{"q": q, "a": a} for q, a in questions],
    }
