"""IQ testlari (har bir yo'nalishga 15 ta savol). Format: "?" savol, "+" to'g'ri, "-" noto'g'ri.

Sonli javoblar ``academy/tests/test_iq.py`` da hisoblab tekshiriladi.
"""

QUIZZES = {
    "IQ01": """
? Keyingi sonni toping: 2, 4, 8, 16, ?
+ 32
- 24
- 30
- 64

? Keyingi sonni toping: 3, 7, 11, 15, ?
+ 19
- 18
- 21
- 17

? Keyingi sonni toping: 1, 4, 9, 16, 25, ?
+ 36
- 30
- 35
- 49

? Keyingi sonni toping: 1, 1, 2, 3, 5, 8, ?
+ 13
- 11
- 12
- 16

? Keyingi sonni toping: 81, 27, 9, 3, ?
+ 1
- 0
- 2
- 6

? Keyingi sonni toping: 2, 6, 12, 20, 30, ?
+ 42
- 40
- 36
- 44

? Keyingi sonni toping: 5, 10, 8, 16, 14, ?
+ 28
- 12
- 26
- 30

? Keyingi sonni toping: 1, 8, 27, 64, ?
+ 125
- 100
- 81
- 216

? Keyingi sonni toping: 100, 95, 85, 70, 50, ?
+ 25
- 30
- 20
- 35

? Keyingi sonni toping: 2, 3, 5, 7, 11, 13, ?
+ 17
- 15
- 19
- 16

? Keyingi sonni toping: 1, 2, 6, 24, 120, ?
+ 720
- 240
- 600
- 144

? Keyingi sonni toping: 4, 9, 7, 12, 10, ?
+ 15
- 13
- 8
- 14

? Keyingi sonni toping: 3, 6, 18, 72, ?
+ 360
- 144
- 216
- 288

? Keyingi sonni toping: 1, 3, 7, 15, 31, ?
+ 63
- 62
- 47
- 64

? Qaysi son qatorga mos emas: 2, 5, 10, 17, 26, 35?
+ 35
- 2
- 17
- 26
""",
    "IQ02": """
? Barcha mushuklar — hayvon. Barcha hayvonlar nafas oladi. Qaysi xulosa to'g'ri?
+ Barcha mushuklar nafas oladi
- Nafas oladigan hamma narsa mushuk
- Ba'zi mushuklar nafas olmaydi
- Barcha hayvonlar mushuk

? Ali Validan baland, Vali Sardordan baland. Eng past kim?
+ Sardor
- Ali
- Vali
- Aniqlab bo'lmaydi

? Agar yomg'ir yog'sa, yer ho'l bo'ladi. Yer ho'l emas. Qaysi xulosa to'g'ri?
+ Yomg'ir yog'magan
- Yomg'ir yog'gan
- Yer ho'l bo'lishi kerak edi
- Hech narsa deb bo'lmaydi

? Ba'zi o'quvchilar shaxmat o'ynaydi. Barcha shaxmatchilar sabrli. Qaysi xulosa to'g'ri?
+ Ba'zi o'quvchilar sabrli
- Barcha o'quvchilar sabrli
- Hech bir o'quvchi sabrli emas
- Barcha sabrli odamlar o'quvchi

? Bugun chorshanba. 10 kundan keyin haftaning qaysi kuni bo'ladi?
+ Shanba
- Juma
- Yakshanba
- Payshanba

? 5 kishi bir-biri bilan bir martadan qo'l berib ko'rishdi. Jami necha marta qo'l berishildi?
+ 10
- 20
- 25
- 5

? Ota o'g'lidan 24 yosh katta. 6 yildan keyin ota o'g'lidan 3 baravar katta bo'ladi. O'g'il hozir necha yoshda?
+ 6
- 8
- 12
- 4

? Qutida 3 ta qizil va 3 ta ko'k paypoq bor. Qorong'ida kamida nechta paypoq olsangiz, bir xil rangli juft aniq bo'ladi?
+ 3
- 2
- 4
- 6

? Lola Maryamdan katta. Maryam Nigoradan kichik. Nigora Loladan kichik. Eng kattasi kim?
+ Lola
- Maryam
- Nigora
- Aniqlab bo'lmaydi

? Hech bir baliq qush emas. Ba'zi qushlar ucha oladi. Qaysi xulosa to'g'ri?
+ Ucha oladiganlarning ba'zilari baliq emas
- Hech bir baliq ucha olmaydi
- Barcha qushlar ucha oladi
- Ba'zi baliqlar qush

? A, B, C, D navbatda turibdi. D — birinchi, B darhol A dan keyin, C oxirgi emas. Navbat tartibi qanday?
+ D, C, A, B
- D, A, B, C
- A, B, D, C
- D, A, C, B

? Soat roppa-rosa 3:00 ni ko'rsatyapti. Soat va minut strelkalari orasidagi burchak necha gradus?
+ 90°
- 45°
- 60°
- 180°

? 6 ta mushuk 6 ta sichqonni 6 daqiqada tutadi. 100 ta sichqonni 100 daqiqada tutish uchun nechta mushuk kerak?
+ 6
- 100
- 60
- 12

? Barcha A — B. Ba'zi B — C. Qaysi xulosa aniq to'g'ri?
+ Ba'zi A ning C ekani aniq emas
- Ba'zi A — C
- Barcha A — C
- Hech bir A — C emas

? Oyning 1-sanasi dushanba. Shu oyning 15-sanasi haftaning qaysi kuni?
+ Dushanba
- Seshanba
- Yakshanba
- Juma
""",
    "IQ03": """
? Qush : uchish = Baliq : ?
+ suzish
- yurish
- sakrash
- uxlash

? Shifokor : kasalxona = O'qituvchi : ?
+ maktab
- kitob
- dars
- o'quvchi

? Issiq : sovuq = Baland : ?
+ past
- uzun
- katta
- tor

? Qalam : yozish = Qaychi : ?
+ kesish
- qog'oz
- o'tkir
- tikish

? Ortiqcha so'zni toping: olma, nok, sabzi, o'rik
+ sabzi
- olma
- nok
- o'rik

? Ortiqcha shaklni toping: uchburchak, kvadrat, doira, to'rtburchak
+ doira
- uchburchak
- kvadrat
- to'rtburchak

? Ortiqcha so'zni toping: Toshkent, Samarqand, Buxoro, O'zbekiston
+ O'zbekiston
- Toshkent
- Samarqand
- Buxoro

? Kitob : sahifa = Daraxt : ?
+ barg
- o'rmon
- soya
- bog'

? Soat : vaqt = Termometr : ?
+ harorat
- bosim
- og'irlik
- uzunlik

? “Tez” so'zining zid ma'noli so'zi (antonimi) qaysi?
+ sekin
- chaqqon
- shoshilinch
- jadal

? G'ildirak : mashina = Qanot : ?
+ samolyot
- havo
- uchuvchi
- osmon

? Qatorni davom ettiring: bahor, yoz, kuz, ?
+ qish
- dekabr
- sovuq
- yil

? Ortiqcha so'zni toping: qizil, ko'k, yashil, katta
+ katta
- qizil
- ko'k
- yashil

? Dushanba : seshanba = Yanvar : ?
+ fevral
- dekabr
- mart
- oy

? “It, mushuk, sigir, ot” — bularni bitta so'z bilan qanday atash mumkin?
+ uy hayvonlari
- yovvoyi hayvonlar
- qushlar
- yirtqichlar
""",
    "IQ04": """
? Kubning nechta yog'i (tomoni) bor?
+ 6
- 4
- 8
- 12

? Kubning nechta qirrasi bor?
+ 12
- 6
- 8
- 10

? Kubning nechta uchi bor?
+ 8
- 6
- 4
- 12

? Yuqoriga qaragan “↑” strelka soat mili yo'nalishida 90° burildi. Endi u qaysi tomonga qaraydi?
+ →
- ←
- ↓
- ↑

? “b” harfi yonidagi tik ko'zguda qanday ko'rinadi?
+ d
- p
- q
- b

? Kvadrat qog'oz ikki marta buklanib (to'rt qavat), o'rtasidan bitta teshik ochildi. Qog'oz yoyilganda nechta teshik bo'ladi?
+ 4
- 2
- 1
- 8

? 3×3 katakli kvadratda jami nechta kvadrat bor (barcha o'lchamdagi)?
+ 14
- 9
- 10
- 13

? Shimolga qarab turibsiz. O'ngga burilasiz, yana o'ngga, keyin chapga. Endi qaysi tomonga qarab turibsiz?
+ Sharq
- G'arb
- Shimol
- Janub

? O'yin soqqasida qarama-qarshi tomonlardagi sonlar yig'indisi 7 ga teng. 2 ning qarshisida qaysi son?
+ 5
- 4
- 6
- 3

? Doira shaklidagi pirogni 3 ta to'g'ri kesim bilan eng ko'pi bilan nechta bo'lakka bo'lish mumkin?
+ 7
- 6
- 8
- 9

? To'rtburchak stolning bitta burchagini to'g'ri chiziq bo'ylab kesib olsangiz, stolda nechta burchak bo'ladi?
+ 5
- 3
- 4
- 6

? Ko'zguda devor soati 3:00 ni ko'rsatyapti. Haqiqiy vaqt qancha?
+ 9:00
- 3:00
- 6:00
- 12:00

? 27 ta kichik kubdan (3×3×3) katta kub yig'ilib, sirti bo'yaldi. Nechta kichik kubning hech bir tomoni bo'yalmagan?
+ 1
- 0
- 8
- 6

? Xuddi shu 3×3×3 kubda nechta kichik kubning aynan 3 ta tomoni bo'yalgan?
+ 8
- 6
- 12
- 4

? Asosi kvadrat bo'lgan piramidaning nechta yog'i bor?
+ 5
- 4
- 6
- 8
""",
    "IQ05": """
? Hisoblang: 25 × 4 + 50 : 2
+ 125
- 75
- 150
- 100

? Olma 1500 so'm, nok 2000 so'm. 7 ta olma va 3 ta nok qancha turadi?
+ 16500 so'm
- 15500 so'm
- 17500 so'm
- 16000 so'm

? Mashina soatiga 60 km yuradi. 150 km ni qancha vaqtda bosib o'tadi?
+ 2,5 soat
- 2 soat
- 3 soat
- 2 soat 15 daqiqa

? Kitobning 1/4 qismi 30 bet. Butun kitob necha bet?
+ 120
- 90
- 100
- 150

? Sinfda 30 o'quvchi bor, ularning 40% i qizlar. Sinfda nechta o'g'il bola bor?
+ 18
- 12
- 20
- 15

? Ikki sonning yig'indisi 20, ayirmasi 4. Kattasi qaysi?
+ 12
- 8
- 14
- 16

? 3 ishchi devorni 12 kunda quradi. 6 ishchi shu devorni necha kunda quradi?
+ 6
- 24
- 4
- 9

? Narx avval 20% oshdi, keyin 20% kamaydi. Boshlang'ich narxga nisbatan nima bo'ldi?
+ 4% arzonlashdi
- O'zgarmadi
- 4% qimmatlashdi
- 2% arzonlashdi

? G'isht 1 kg va yana yarim g'isht og'irligida. Bitta g'isht necha kg?
+ 2 kg
- 1,5 kg
- 1 kg
- 3 kg

? Ko'ldagi nilufarlar har kuni 2 baravar ko'payadi va 30 kunda ko'lni to'liq qoplaydi. Ko'lning yarmini necha kunda qoplagan?
+ 29
- 15
- 20
- 28

? Raketka va to'p birga 1100 so'm. Raketka to'pdan 1000 so'm qimmat. To'p necha so'm?
+ 50 so'm
- 100 so'm
- 10 so'm
- 150 so'm

? Dastlabki 10 ta juft sonning (2, 4, 6, …) yig'indisi nechaga teng?
+ 110
- 100
- 90
- 120

? Soat 14:45. 2 soat 30 daqiqadan keyin soat necha bo'ladi?
+ 17:15
- 16:15
- 17:45
- 16:45

? Ota 40 yoshda, o'g'li 10 yoshda. Necha yildan keyin ota o'g'lidan 3 baravar katta bo'ladi?
+ 5
- 10
- 3
- 15

? Hisoblang: 0,5 × 0,5
+ 0,25
- 2,5
- 1
- 0,025
""",
}
