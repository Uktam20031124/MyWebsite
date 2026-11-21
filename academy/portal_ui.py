"""O'quvchi profili uchun taqdimot qiymatlari: bugungi reja, keyingi mukofot, yutuqlar, o'sish grafigi.

Hammasi mavjud ma'lumotdan hisoblanadi — yangi biznes qoidasi yo'q (quvvat, limit va narxlar o'zgarmaydi).
"""

from dataclasses import dataclass

from django.utils.translation import gettext as _


@dataclass
class Mission:
    key: str
    title: str
    meta: str
    href: str
    done: bool


@dataclass
class Achievement:
    icon: str
    title: str
    hint: str
    got: bool
    pct: int = 0  # olinmaganlarida — maqsadga qancha yaqin (0–100)


def missions(*, pending, homework_open_n, open_mistakes_n, bonus, streak) -> list[Mission]:
    """Bugungi reja: bajarilishi kerak bo'lgan ishlar (bajarilganlari oxirida, ✓ bilan)."""
    items = []
    for a in pending:
        topic = a.quiz.topic.title if a.quiz.topic_id else ""
        meta = _("{topic} · {n} ta savol").format(topic=topic, n=a.question_count) if topic else ""
        items.append(Mission("test", _("Yechilmagan test"), meta, a.get_absolute_url(), False))
    if homework_open_n:
        items.append(Mission("homework", _("Uyga vazifani topshiring"),
                             _("{n} ta vazifa kutmoqda").format(n=homework_open_n), "#homework", False))
    if open_mistakes_n:
        items.append(Mission("mistakes", _("Xatolar ustida ishlang"),
                             _("{n} ta savol · har biri +2 ⚡️").format(n=open_mistakes_n), "#mistakes", False))
    if bonus.get("remaining") and bonus.get("left_today"):
        items.append(Mission("bonus", _("Qo‘shimcha savollar"),
                             _("bugun yana {n} ta").format(n=bonus["left_today"]), "#bonus", False))
    items.append(Mission("streak", _("Streakni saqlang"),
                         _("bugun faolsiz") if streak.active_today else _("bitta test yoki mashq yetarli"),
                         "#topics", streak.active_today))
    return sorted(items, key=lambda m: m.done)


def next_reward(rewards, available: int, owned_honor: bool):
    """Hali yetmaydigan eng arzon mukofot va unga qancha qolgani (progress %)."""
    candidates = [r for r in rewards if r.cost > available and not (r.perk == "honor" and owned_honor)]
    if not candidates:
        return None
    r = min(candidates, key=lambda x: x.cost)
    return {"reward": r, "need": r.cost - available, "pct": max(0, min(100, round(available * 100 / r.cost)))}


def achievements(*, finished, stats, streak, student, open_mistakes_n) -> list[Achievement]:
    best = max((a.percent for a in finished), default=None)
    n = stats.n

    def pct(cur, target):
        return max(0, min(100, round(cur * 100 / target))) if target else 0

    return [
        Achievement("🎯", _("Birinchi test"), _("1 ta test yeching"), n >= 1, pct(n, 1)),
        Achievement("📚", _("5 ta test"), _("{n}/5").format(n=min(n, 5)), n >= 5, pct(n, 5)),
        Achievement("🏅", _("10 ta test"), _("{n}/10").format(n=min(n, 10)), n >= 10, pct(n, 10)),
        Achievement("⭐", _("80%+ natija"),
                    _("eng yaxshisi: {p}%").format(p=best) if best is not None else _("hali yo‘q"),
                    best is not None and best >= 80, pct(best or 0, 80)),
        Achievement("💯", _("Mukammal test"), _("100% natija"), best == 100, pct(best or 0, 100)),
        Achievement("🔥", _("7 kunlik streak"), _("{d}/7 kun").format(d=min(streak.days, 7)), streak.days >= 7,
                    pct(streak.days, 7)),
        Achievement("✅", _("Xatolarsiz"), _("ochiq xato savol yo‘q"), n >= 1 and not open_mistakes_n,
                    100 if n >= 1 and not open_mistakes_n else 0),
        Achievement("🎖", _("A’lochi"), _("ustoz beradi"), bool(student.honor_since), 100 if student.honor_since else 0),
    ]


def greeting(now) -> str:
    """Mahalliy vaqtga qarab salomlashuv."""
    h = now.hour
    if 5 <= h < 12:
        return _("Xayrli tong")
    if 12 <= h < 18:
        return _("Xayrli kun")
    return _("Xayrli kech")


def topic_status(row, pass_percent: int) -> dict:
    """Mavzu holati (oxirgi natijadan): o'zlashtirildi / mustahkamlash kerak / jarayonda / boshlanmagan."""
    last = row.last
    if last is None:
        return {"key": "new", "label": _("Boshlanmagan"), "pct": 0}
    p = last.percent or 0
    if p >= 80:
        return {"key": "mastered", "label": _("O‘zlashtirildi"), "pct": p}
    if p < pass_percent:
        return {"key": "review", "label": _("Mustahkamlash kerak"), "pct": p}
    return {"key": "progress", "label": _("Yaxshi, 80% ga yaqin"), "pct": p}


def homework_view(rows, today) -> list[dict]:
    """Vazifalar vaqt chizig'i: holat va muddatgacha kunlar."""
    out = []
    for r in rows:
        days = (r.due - today).days
        if r.submission is not None and r.submission.status == "checked":
            key = "checked"
        elif r.submission is not None:
            key = "submitted"
        elif r.overdue:
            key = "overdue"
        else:
            key = "open"
        out.append({"row": r, "key": key, "days": days})
    return out


def mistake_bars(topics) -> list[dict]:
    top = max((t["n"] for t in topics), default=0)
    return [{**t, "pct": round(t["n"] * 100 / top) if top else 0} for t in topics]


def board_view(board, me_pk: int) -> dict:
    """Reyting: podium (top-3), qolganlar, o'quvchining o'rni va yuqoridagigacha farq."""
    # Teng ballarda ham podium 3 pozitsiya: balandlik tartibdan (pos), medal esa haqiqiy o'rindan (place).
    podium = [{**r, "pos": i} for i, r in enumerate(board[:3], start=1)] if board and board[0]["coins"] > 0 else []
    rest = board[len(podium):]
    me = next((r for r in board if r["student"].pk == me_pk), None)
    gap = None
    if me and me["place"] > 1:
        above = [r for r in board if r["coins"] > me["coins"]]
        if above:
            gap = min(r["coins"] for r in above) - me["coins"]
    # Vizual tartib: 2-pozitsiya, 1-pozitsiya, 3-pozitsiya.
    order = {2: 0, 1: 1, 3: 2}
    return {"podium": sorted(podium, key=lambda r: order[r["pos"]]), "rest": rest, "me": me, "gap": gap}


def coin_days(history) -> list[dict]:
    """Quvvat tarixi kunlar bo'yicha (yangi kun birinchi): yozuvlar va kunlik yig'indi."""
    from django.utils import timezone

    days: list[dict] = []
    for c in history:
        d = timezone.localtime(c.created_at).date()
        if not days or days[-1]["day"] != d:
            days.append({"day": d, "items": [], "total": 0})
        days[-1]["items"].append(c)
        days[-1]["total"] += c.amount
    return days


def growth_chart(recent, width: int = 640, height: int = 180, pad: int = 24) -> dict | None:
    """Oxirgi testlar foizi — SVG nuqtalari va 50/80 chegaralari (y o'qi 0–100)."""
    values = [a.percent for a in recent]
    if len(values) < 2:
        return None
    step = (width - 2 * pad) / (len(values) - 1)

    def y(v):
        # Butun son: shablonda lokalizatsiya (o'nlik vergul) SVG atributini buzmasin.
        return round(height - pad - v * (height - 2 * pad) / 100)

    points = [
        {"x": round(pad + i * step), "y": y(v), "v": v, "a": a}
        for i, (v, a) in enumerate(zip(values, recent, strict=True))
    ]
    line = " ".join(f"{p['x']},{p['y']}" for p in points)
    area = f"{points[0]['x']},{height - pad} {line} {points[-1]['x']},{height - pad}"
    delta = values[-1] - values[0]
    best, avg = max(values), round(sum(values) / len(values))
    return {"w": width, "h": height, "points": points, "line": line, "area": area, "y50": y(50), "y80": y(80),
            "y50l": y(50) + 4, "y80l": y(80) + 4, "best": best, "avg": avg,
            "last": points[-1], "delta": delta, "pad": pad}
