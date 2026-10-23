"""IQ — mantiqiy fikrlash darajasini aniqlash: 5 ta yo'nalish, har birida 15 ta savol.

Testlar istalgan guruhga (yoki ochiq havola orqali) yuboriladi. Natija — klinik IQ emas,
mantiqiy fikrlash darajasining taxminiy bahosi (shkala har bir mavzu tavsifida).
"""

from . import ModuleData as M
from . import TopicData as T

TIME_LIMIT = 15  # daqiqa, har bir test uchun

SCALE = (
    "\n\nNatija bo'yicha daraja:\n"
    "- 90–100% — juda yuqori\n"
    "- 75–89% — yuqori\n"
    "- 50–74% — o'rtacha\n"
    "- 50% dan past — rivojlantirish kerak\n\n"
    "Eslatma: bu klinik IQ o'lchovi emas — mantiqiy fikrlash darajasining taxminiy bahosi. "
    "5 ta testning o'rtacha foizi umumiy darajani ko'rsatadi."
)


def about(goal: str, skills: str) -> str:
    return f"Maqsad: {goal}\n\nNimani tekshiradi: {skills}\n\nVaqt: {TIME_LIMIT} daqiqa, 15 ta savol.{SCALE}"


MODULES = [
    M(
        "IQ · Mantiqiy fikrlash",
        "Mantiqiy fikrlash darajasini aniqlash uchun 5 ta yo'nalish: sonli ketma-ketliklar, mantiqiy "
        "xulosalar, so'z o'xshatmalari, fazoviy tasavvur va tez hisob. Har bir test — 15 savol, 15 daqiqa.",
        [
            T(
                "IQ01",
                "IQ test 1: Sonli ketma-ketliklar",
                about(
                    "sonlar orasidagi qonuniyatni topish qobiliyatini aniqlash.",
                    "arifmetik va geometrik progressiya, kvadrat va kub sonlar, Fibonachchi, almashinib "
                    "keluvchi amallar, tub sonlar, ortiqcha sonni topish.",
                ),
                "Har bir ketma-ketlik uchun qonuniyatni bir gap bilan yozing (masalan: “har safar ×2”).",
                minutes=30,
            ),
            T(
                "IQ02",
                "IQ test 2: Mantiqiy xulosalar",
                about(
                    "berilgan shartlardan to'g'ri xulosa chiqarish qobiliyatini aniqlash.",
                    "sillogizmlar, “agar … bo'lsa” xulosalari, tartiblash (kim baland/katta), kalendar "
                    "va soat masalalari, kombinatorika.",
                ),
                "Har bir masalada qaysi shart xulosaga olib kelganini yozing.",
                minutes=30,
            ),
            T(
                "IQ03",
                "IQ test 3: So‘z o‘xshatmalari va tushunchalar",
                about(
                    "tushunchalar orasidagi bog'liqlikni ko'rish qobiliyatini aniqlash.",
                    "o'xshatmalar (A : B = C : ?), antonimlar, ortiqcha so'zni topish, umumlashtirish.",
                ),
                "O'zingiz 5 ta “A : B = C : ?” o'xshatma tuzing va javobini yozing.",
                minutes=30,
            ),
            T(
                "IQ04",
                "IQ test 4: Shakl va fazoviy tasavvur",
                about(
                    "narsalarni ko'z oldiga keltirish va aylantirish qobiliyatini aniqlash.",
                    "kub va piramida elementlari, burilish va ko'zgudagi aks, buklangan qog'oz, "
                    "yo'nalishlar, bo'yalgan kub masalalari.",
                ),
                "Qog'ozdan kub yasang va har bir tomoniga 1 dan 6 gacha son yozib, qarama-qarshi "
                "tomonlarni tekshiring.",
                minutes=30,
            ),
            T(
                "IQ05",
                "IQ test 5: Tez hisob va masalalar",
                about(
                    "hisoblash tezligi va matnli masalani tez tushunib yechish qobiliyatini aniqlash.",
                    "amallar tartibi, foiz va kasrlar, tezlik–vaqt, ish unumi, “tuzoqli” masalalar.",
                ),
                "Testdagi 3 ta eng qiyin masalani qayta yechib, yechimini bosqichma-bosqich yozing.",
                minutes=30,
            ),
        ],
    )
]

TRACK = [t.key for m in MODULES for t in m.topics]
