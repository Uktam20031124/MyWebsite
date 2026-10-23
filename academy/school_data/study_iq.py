"""IQ testlari: yechish usullari (mustahkamlash materiali). Format — ``ui.study_md``."""

STUDY = {
    "IQ01": """
## Qonuniyatni qanday topish kerak
1. Qo'shni sonlar **ayirmasini** yozing: 3, 7, 11, 15 → +4, +4, +4.
2. Ayirma o'zgarsa — **ayirmalarning ayirmasini** qarang: 2, 6, 12, 20 → +4, +6, +8 (har safar +2).
3. Sonlar tez o'ssa — **nisbatini** qarang: 2, 4, 8, 16 → ×2.
4. Taniqli qatorlarni eslang: kvadratlar (1, 4, 9, 16), kublar (1, 8, 27), tub sonlar (2, 3, 5, 7, 11), Fibonachchi (har bir son — oldingi ikkitasining yig'indisi).
5. Ikki amal **almashinib** kelishi mumkin: 5, 10, 8, 16, 14 → ×2, −2, ×2, −2.

## Misol
`1, 3, 7, 15, 31, ?` — har bir son: oldingisi × 2 + 1. Javob: 31 × 2 + 1 = **63**.

> Javobni tanlagach, qonuniyatni butun qatorda tekshiring — faqat oxirgi ikki songa emas.
""",
    "IQ02": """
## Mantiqiy xulosa qoidalari
- **Barcha A — B, barcha B — C** → barcha A — C.
- **Agar P bo'lsa, Q bo'ladi. Q yo'q** → demak, P ham yo'q. (Lekin “Q bor” bo'lsa, P haqida aniq gapirib bo'lmaydi!)
- **Ba'zi** degan so'z “hammasi” degani emas: “ba'zi B — C” dan “ba'zi A — C” kelib chiqmaydi.

## Tartiblash masalalari
Shartlarni qatorga chizing: Ali > Vali > Sardor. Har yangi shartni chizmaga qo'shing.

## Kalendar va soat
- Hafta kunlari har **7** kunda takrorlanadi: 10 kun = 7 + 3 → 3 kun oldinga.
- Soat siferblatida 1 soat oralig'i = **30°**.

## Kombinatorika
n kishi bir-biri bilan bir martadan qo'l bersa: n × (n − 1) : 2. 5 kishi → 5 × 4 : 2 = **10**.
""",
    "IQ03": """
## O'xshatmalarni yechish
1. Birinchi juftlik orasidagi **bog'liqlikni gap bilan ayting**: “Qush — **uchadi**”.
2. Xuddi shu gapni ikkinchi juftlikka qo'ying: “Baliq — **suzadi**”.

## Bog'liqlik turlari
- Vazifa: qalam → yozish, qaychi → kesish.
- Joy: shifokor → kasalxona, o'qituvchi → maktab.
- Qism va butun: sahifa → kitob, barg → daraxt.
- Zid ma'no: issiq → sovuq, baland → past.
- Ketma-ketlik: dushanba → seshanba, yanvar → fevral.

## Ortiqcha so'z
Avval qolgan uchtasini birlashtiradigan **umumiy so'zni** toping (mevalar, ranglar, shaharlar) — unga kirmaydigani ortiqcha.
""",
    "IQ04": """
## Kub va piramida
- Kub: **6** yoq, **12** qirra, **8** uch.
- Asosi kvadrat piramida: 4 ta yon yoq + 1 asos = **5** yoq.

## Bo'yalgan 3×3×3 kub
- 3 tomoni bo'yalgan — burchakdagilar: **8**.
- Hech bo'yalmagan — o'rtadagi bittasi: **1**.

## Burilish va ko'zgu
- Soat mili bo'yicha 90°: yuqori → o'ng → past → chap.
- Tik ko'zguda chap va o'ng almashadi: “b” → “d”, soatdagi 3:00 → 9:00.

## Buklangan qog'oz
Har bir buklash qavatlar sonini **2 baravar** oshiradi; teshik barcha qavatdan o'tadi: 2 marta buklash → 4 qavat → **4** teshik.

> Qiyin bo'lsa — qog'ozga chizing yoki qog'ozni haqiqatan buklab ko'ring.
""",
    "IQ05": """
## Tez hisob qoidalari
- Amallar tartibi: avval **× va :**, keyin **+ va −**. 25 × 4 + 50 : 2 = 100 + 25 = **125**.
- Foiz: 40% = 0,4. 30 ning 40% i = 12.
- Ketma-ket +20% va −20%: 100 → 120 → 96, ya'ni **4% arzon**.

## “Tuzoqli” masalalar
- Raketka va to'p: to'p = x, raketka = x + 1000; 2x + 1000 = 1100 → x = **50**.
- Har kuni 2 baravar ko'payadigan nilufar 30-kuni to'lsa, **29**-kuni yarmi to'lgan.

## Ish unumi
Ishchilar 2 baravar ko'p bo'lsa, ish 2 baravar tez bitadi: 3 ishchi — 12 kun → 6 ishchi — **6** kun.

> Javobni topgach, uni shartga qo'yib tekshiring.
""",
}
