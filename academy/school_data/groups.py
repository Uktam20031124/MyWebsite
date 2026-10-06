"""Guruhlar, o'quvchilar va har bir guruhning dasturi (mavzu kalitlari tartibda).

``taught`` — allaqachon o'tilgan mavzular, ``planned`` — qolganlari. Kalitlar
starter.py / python.py dagi mavzularga mos keladi.
"""

from . import GroupData as G

# Barcha guruhlar seshanba, juma va shanba kunlari, ketma-ket soatlarda.
TUE_FRI_SAT = (1, 4, 5)

# Starter bitiruvchilari uchun Python kursi (10 mavzulik modul rejasi bo'yicha):
# kirish → turlar → operatorlar → shartlar → tuzilmalar → sikllar → funksiyalar →
# modullar → fayllar/xatolar → loyihalar. OOP va os — Python Pro bosqichida.
PYTHON_TRACK = [
    "PY01", "PY02", "PY03", "PY04", "PY05", "PY06", "PY07", "PY08",
    "PY09", "PY10", "PY11", "PY12", "PY13",
    "PY14", "PY15", "PY16", "PY17", "PY18", "PY19",
    "PY20", "PY21", "PY22", "PY24", "PY25", "PY26",
    "PY30", "PY31", "PY32", "PY33", "PY34",
]  # fmt: skip

GROUPS = [
    G(
        code="S-009",
        name="S-009 · Starter",
        days=TUE_FRI_SAT,
        starts="14:00",
        ends="15:00",
        students=[
            "Karimov Laziz",
            "Karimova Nigina",
            "Muxlisov Umarbek",
            "Maxmudov Xasan",
            "Maxmudov Xusan",
            "Imomaliyev Xusantoy",
            "Farmonov Firdavs",
            "Shavkatov Akmal",
            "Axmedov Aliakbar",
            "Baxtiyorov Mironshox",
            "Oripov Oybek",
            "Muxammadov Imron",
        ],
        taught=["ST01", "ST02", "ST03", "ST04"],
        planned=[
            "ST06", "ST07", "ST08",  # Sheets, 1-oy yakuniy
            "ST09", "ST10",  # Canva
            "ST11", "ST12", "ST13",  # Figma
            "ST15", "ST16",  # Scratch
            "ST17", "ST18", "ST19",  # Meet/Calendar, xavfsizlik, yakuniy loyiha
            *PYTHON_TRACK,
        ],  # fmt: skip
        notes="Starter kursidan so'ng Python kursiga o'tadi (dasturda Python mavzulari ham bor).",
    ),
    G(
        code="S005",
        name="S005 · Starter",
        days=TUE_FRI_SAT,
        starts="15:00",
        ends="16:00",
        students=[
            "Ibrahimov Muxammad ali",
            "Meymonov Murodbek",
            "Sharipov Mirali",
            "Nurulayev Saidjon",
            "Yo'ldashev Firdavs",
            "Davlatov Mirfayz",
            "Muxammadov Imron",
        ],
        taught=[
            "ST01", "ST02", "ST03", "ST04",  # Monkeytype, Gmail, Docs, Slides
            "ST09", "ST10",  # Canva
            "ST11", "ST12", "ST13",  # Figma
            "ST14",  # Terminal
        ],  # fmt: skip
        planned=[
            "ST05", "ST06", "ST07",  # Drive, Sheets
            "ST15", "ST16",  # Scratch
            "ST17", "ST18", "ST19",  # Meet/Calendar, xavfsizlik, yakuniy loyiha
            *PYTHON_TRACK,
        ],  # fmt: skip
        notes="Starter kursidan so'ng Python kursiga o'tadi (dasturda Python mavzulari ham bor).",
    ),
    G(
        code="P-006",
        name="P-006 · Python Pro",
        days=TUE_FRI_SAT,
        starts="16:00",
        ends="17:00",
        students=[
            "Odilov Saidamir",
            "Xudoynazarov Javoxir",
            "Qudratov Firdavs",
            "Yo'ldoshev Farxod",
            "Asrorov Hamrobek",
        ],
        taught=["PY02", "PY04", "PY20", "PY22", "PY09", "PY10"],
        planned=[
            "PY11",  # 1. Tuple va Set
            "PY12", "PY13",  # 2. Dictionary
            "PY06", "PY07", "PY08",  # 3. Shartlar (+ RegEx)
            "PY14", "PY15", "PY16",  # 4. Sikllar
            "PY17", "PY18", "PY19",  # 5. Funksiyalar
            "PY24",  # 6. Xatoliklar
            "PY25", "PY26",  # 7. Fayllar (txt, json)
            "PY21", "PY23",  # 8. math, datetime, os
            "PY27", "PY28", "PY29",  # 9. OOP
            "PY31", "PY32", "PY33", "PY34",  # 10. Yakuniy loyihalar
        ],  # fmt: skip
    ),
]
