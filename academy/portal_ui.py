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
    return [
        Achievement("🎯", _("Birinchi test"), _("1 ta test yeching"), n >= 1),
        Achievement("📚", _("5 ta test"), _("{n}/5").format(n=min(n, 5)), n >= 5),
        Achievement("🏅", _("10 ta test"), _("{n}/10").format(n=min(n, 10)), n >= 10),
        Achievement("⭐", _("80%+ natija"),
                    _("eng yaxshisi: {p}%").format(p=best) if best is not None else _("hali yo‘q"),
                    best is not None and best >= 80),
        Achievement("💯", _("Mukammal test"), _("100% natija"), best == 100),
        Achievement("🔥", _("7 kunlik streak"), _("{d}/7 kun").format(d=min(streak.days, 7)), streak.days >= 7),
        Achievement("✅", _("Xatolarsiz"), _("ochiq xato savol yo‘q"), n >= 1 and not open_mistakes_n),
        Achievement("🎖", _("A’lochi"), _("ustoz beradi"), bool(student.honor_since)),
    ]


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
    return {"w": width, "h": height, "points": points, "line": line, "area": area, "y50": y(50), "y80": y(80),
            "y50l": y(50) + 4, "y80l": y(80) + 4,
            "last": points[-1], "delta": delta, "pad": pad}
