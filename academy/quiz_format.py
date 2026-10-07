"""Test matni formati: "?" — savol, "+" — to'g'ri javob, "-" — noto'g'ri javob.

Modellarga bog'liq emas: formada ham, data migratsiyada ham ishlatiladi.
"""

import textwrap

QUIZ_FORMAT_HELP = """? Savol matni
+ To'g'ri javob
- Noto'g'ri javob
- Noto'g'ri javob"""

Parsed = list[tuple[str, list[tuple[str, bool]]]]


def parse_quiz(text: str) -> tuple[Parsed, list[str]]:
    """Test matnini o'qiydi: (savollar, xatolar).

    "?" bilan boshlangan qator — yangi savol, "+" — to'g'ri javob, "-" — noto'g'ri
    javob. Savol va birinchi javob orasidagi qatorlar savolning davomi (masalan, kod) —
    ularning chekinishi saqlanadi.
    """
    drafts: list[tuple[str, list[str], list[tuple[str, bool]]]] = []
    errors: list[str] = []
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            if drafts and drafts[-1][1] and not drafts[-1][2]:
                drafts[-1][1].append("")  # kod ichidagi bo'sh qator
            continue
        mark, rest = line[0], line[1:].strip()
        if mark == "?":
            drafts.append((rest, [], []))
        elif mark in "+-":
            if not drafts:
                errors.append(f"{n}-qator: javobdan oldin savol yozing (“? …”).")
            elif rest:
                drafts[-1][2].append((rest[:500], mark == "+"))
        elif drafts and not drafts[-1][2]:
            drafts[-1][1].append(raw.rstrip().expandtabs(4))
        else:
            errors.append(f"{n}-qator: “?”, “+” yoki “-” bilan boshlanishi kerak.")

    questions: Parsed = []
    for i, (title, body, choices) in enumerate(drafts, start=1):
        body_text = textwrap.dedent("\n".join(body)).strip("\n")
        q_text = f"{title}\n{body_text}".strip() if body_text else title
        if not q_text:
            errors.append(f"{i}-savol: matni bo‘sh.")
        if len(choices) < 2:
            errors.append(f"{i}-savol: kamida 2 ta javob varianti kerak.")
        if sum(ok for _, ok in choices) != 1:
            errors.append(f"{i}-savol: aynan bitta to‘g‘ri javob (“+”) bo‘lishi kerak.")
        if len({c for c, _ in choices}) != len(choices):
            errors.append(f"{i}-savol: javob variantlari takrorlangan.")
        questions.append((q_text, choices))
    return questions, errors
