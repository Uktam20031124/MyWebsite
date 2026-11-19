"""Dars kodi ma'lumotini ixcham yozish yordamchilari (``lessons_*.py`` fayllari uchun).

``run`` — darsning asosiy dasturini sinash: {"file", "input", "randint"?, "expect": [natijada bo'lishi shart qatorlar]}
(``tests/test_lessons.py`` dasturni shu kiritish bilan ishga tushirib tekshiradi).
"""


def step(file: str, title: str, code: str, notes: list, result: str, new=None) -> dict:
    code = code.strip("\n")
    lines = code.count("\n") + 1
    return {
        "file": file,
        "title": title,
        "code": code,
        "new": list(range(1, lines + 1)) if new is None else list(new),
        "notes": notes,
        "result": result.strip("\n"),
    }


def lesson(
    month: str,
    number: int,
    title: str,
    goal: str,
    before: str,
    review: str,
    concept: str,
    practice: str,
    flow: list,
    steps: list,
    files: dict,
    tree: list,
    learned: list,
    homework: list,
    next_: str,
    run: dict | None = None,
    **extra,
) -> dict:
    data = {
        "month": month,
        "number": number,
        "title": title,
        "goal": goal,
        "before": before,
        "plan": [
            ("0–5", "Takrorlash", review),
            ("5–15", "Yangi mavzu", concept),
            ("15–40", "Birga kod yozamiz", f"{len(steps)} qadam: " + " → ".join(s["title"].lower() for s in steps) + "."),
            ("40–50", "Mustaqil ish", practice),
            ("50–60", "Test", "Saytdagi 10 savollik test."),
        ],
        "flow": flow,
        "steps": steps,
        "files": {k: v.strip("\n") + "\n" for k, v in files.items()},
        "tree": tree,
        "learned": learned,
        "homework": homework,
        "next": next_,
    }
    if run:
        data["run"] = run
    data.update(extra)
    return data
