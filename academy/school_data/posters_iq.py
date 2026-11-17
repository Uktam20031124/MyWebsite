"""IQ testlari: dars rasmlari (mavzu kaliti bo'yicha). Shakl — ``poster_kit``; manba — ``study_iq``."""

from .poster_kit import card, poster

POSTERS = {
    "IQ01": poster(
        "Sonlar qatoridagi <b>qonuniyatni</b> topamiz: ayirma, nisbat va taniqli qatorlar.",
        ("tiles", [
            ("+4", "Ayirma", "3, 7, 11, 15 → har safar +4 → 19"),
            ("+2", "Ayirmalar ayirmasi", "2, 6, 12, 20 → +4, +6, +8 → 30"),
            ("×2", "Nisbat", "2, 4, 8, 16 → har safar ×2 → 32"),
            ("n²", "Kvadratlar", "1, 4, 9, 16, 25 → 36"),
            ("a+b", "Fibonachchi", "1, 1, 2, 3, 5, 8 → 13"),
            ("×2 −2", "Almashinuvchi", "5, 10, 8, 16, 14 → 28"),
        ]),
        [
            card("1-qadam", formula="qo'shni sonlar ayirmasi = [qadam]", text="Ayirma o'zgarsa — ayirmalarning ayirmasini qarang."),
            card("Misol", formula="1, 3, 7, 15, 31 → 31 × 2 + 1 = [63]", text="Har son: oldingisi × 2 + 1."),
            card("Tub sonlar", text="<b>2, 3, 5, 7, 11, 13</b> — faqat 1 ga va o'ziga bo'linadi."),
        ],
        ("Qoidani butun qatorda tekshiring", "Faqat oxirgi ikki songa qarab xulosa qilmang."),
        [
            ("4, 9, 14, 19, ? — keyingi son?", "24 (+5)."),
            ("3, 6, 12, 24, ? — keyingi son?", "48 (×2)."),
            ("1, 4, 9, 16, ? — keyingi son?", "25 (kvadratlar)."),
        ],
        title="Qonuniyat turlari",
        badge=("?", "keyingi"),
    ),
    "IQ02": poster(
        "Shartlardan <b>to'g'ri xulosa</b> chiqaramiz: mantiq, tartiblash, kalendar va kombinatorika.",
        ("tiles", [
            ("A→C", "Zanjir", "Barcha A — B, barcha B — C → barcha A — C."),
            ("¬Q→¬P", "Agar … bo'lsa", "P bo'lsa Q bo'ladi. Q yo'q → P ham yo'q."),
            ("ba'zi", "Ehtiyot so'z", "“Ba'zi” — “hammasi” degani emas."),
            ("A>B>C", "Tartiblash", "Shartlarni qatorga chizing."),
            ("7", "Hafta", "10 kun = 7 + 3 → 3 kun oldinga."),
            ("30°", "Soat", "Siferblatda 1 soat oralig'i = 30°."),
        ]),
        [
            card("Qo'l berishish", formula="n × (n − 1) ÷ 2", example="5 kishi → 5 × 4 ÷ 2 = <b>10</b> marta"),
            card("Soat burchagi", formula="3:00 → 3 × 30° = [90°]", text=""),
            card("Tuzoq", text="“P bo'lsa Q bo'ladi. <b>Q bor</b>” — P haqida aniq gapirib bo'lmaydi!"),
        ],
        ("Chizing — boshda saqlamang", "Har yangi shartni chizmaga qo'shib boring."),
        [
            ("Bugun dushanba. 10 kundan keyin qaysi kun?", "Payshanba."),
            ("6 kishi bir-biri bilan qo'l bersa, necha marta?", "15 marta."),
            ("Ali Validan baland, Vali Sardordan baland. Eng past kim?", "Sardor."),
        ],
        title="Xulosa qoidalari",
        badge=("∴", "demak"),
    ),
    "IQ03": poster(
        "So'zlar orasidagi <b>bog'liqlikni</b> topamiz va ortiqcha so'zni ajratamiz.",
        ("tiles", [
            ("✎", "Vazifa", "qalam → yozish, qaychi → kesish"),
            ("📍", "Joy", "shifokor → kasalxona, o'qituvchi → maktab"),
            ("🧩", "Qism va butun", "sahifa → kitob, barg → daraxt"),
            ("⇄", "Zid ma'no", "issiq → sovuq, baland → past"),
            ("→", "Ketma-ketlik", "dushanba → seshanba, yanvar → fevral"),
            ("✕", "Ortiqcha so'z", "olma, nok, sabzi, uzum → sabzi"),
        ]),
        [
            card("1-qadam", text="Birinchi juftlik bog'liqligini <b>gap bilan</b> ayting: “Qush — <b>uchadi</b>”."),
            card("2-qadam", formula="Baliq — [suzadi]", text="Xuddi shu gapni ikkinchi juftlikka qo'ying."),
            card("Ortiqcha so'z", text="Qolgan uchtasini birlashtiradigan <b>umumiy so'zni</b> toping: mevalar → sabzi ortiqcha."),
        ],
        ("Bog'liqlikni gap qilib ayting", "Shunda adashish ancha kamayadi."),
        [
            ("Kitob : sahifa = daraxt : ?", "barg"),
            ("Ortiqchasi: qizil, ko'k, Toshkent, yashil", "Toshkent"),
            ("Issiq : sovuq = baland : ?", "past"),
        ],
        title="Bog'liqlik turlari",
        badge=("A:B", "C:?"),
    ),
    "IQ04": poster(
        "Shakllarni <b>ko'z oldimizda aylantiramiz</b>: kub, ko'zgu, burilish va buklangan qog'oz.",
        ("tiles", [
            ("6·12·8", "Kub", "6 yoq, 12 qirra, 8 uch."),
            ("5", "Piramida", "Asosi kvadrat: 4 yon yoq + 1 asos."),
            ("8 / 1", "Bo'yalgan 3×3×3", "3 tomoni bo'yalgan — 8 ta, bo'yalmagan — 1 ta."),
            ("90°", "Burilish", "Soat bo'yicha: yuqori → o'ng → past → chap."),
            ("b↔d", "Ko'zgu", "Chap va o'ng almashadi: 3:00 → 9:00."),
            ("×2", "Buklash", "Har buklash qavatni 2 baravar oshiradi."),
        ]),
        [
            card("Buklangan qog'oz", formula="2 marta buklash → 4 qavat → [4 teshik]", text=""),
            card("3×3×3 kub", formula="3 × 3 × 3 = [27] kubcha", text="Burchaklar — 8, o'rtadagi — 1."),
            card("Ko'zgu", text="Tik ko'zguda <b>chap ↔ o'ng</b>, yuqori va past o'zgarmaydi."),
        ],
        ("Qiyin bo'lsa — chizing yoki buklang", "Qog'oz va qalam — eng yaxshi yordamchi."),
        [
            ("Kubning nechta qirrasi bor?", "12 ta."),
            ("Qog'oz 3 marta buklanib teshilsa, nechta teshik?", "8 ta."),
            ("Ko'zguda soat 3:00 ni ko'rsatsa, aslida necha?", "9:00."),
        ],
        title="Fazoviy tasavvur",
        badge=("◳", "shakl"),
    ),
    "IQ05": poster(
        "Tez va to'g'ri hisoblaymiz: <b>amallar tartibi, foiz</b> va “tuzoqli” masalalar.",
        ("tiles", [
            ("×÷", "Tartib", "25 × 4 + 50 ÷ 2 = 100 + 25 = 125"),
            ("40%", "Foiz", "40% = 0,4; 30 ning 40% i = 12"),
            ("−4%", "+20% va −20%", "100 → 120 → 96: 4% arzon."),
            ("50", "Raketka va to'p", "Jami 1100, farq 1000 → to'p 50."),
            ("29", "Nilufar", "Har kuni ×2, 30-kuni to'ldi → 29-kuni yarmi."),
            ("½", "Ish unumi", "Ishchi 2 baravar → vaqt 2 baravar kam."),
        ]),
        [
            card("Ish unumi", formula="3 ishchi × 12 kun = 6 ishchi × [6 kun]", text=""),
            card("Foiz", formula="200 × 0,15 = [30]", text="200 ning 15% i."),
            card("Tuzoq", text="Birinchi kelgan javob — ko'pincha <b>noto'g'ri</b>: 100 emas, <b>50</b>."),
        ],
        ("Javobni shartga qo'yib tekshiring", "Raketka 1050 + to'p 50 = 1100 ✓, farq 1000 ✓"),
        [
            ("10 + 5 × 2 nechaga teng?", "20"),
            ("80 ning 25% i qancha?", "20"),
            ("4 ishchi devorni 6 kunda quradi. 8 ishchi necha kunda?", "3 kunda."),
        ],
        title="Tez hisob qoidalari",
        badge=("⚡", "hisob"),
    ),
}
