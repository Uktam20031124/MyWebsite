"""Dasturchi 9-oy · 1-sayt: Portfolio (HTML, CSS, JS) — WB01–WB12 "Dars kodi".

Sayt fayllari har dars bosqichi uchun ``index_html(n)``, ``style_css(n)``, ``script_js(n)`` dan yig'iladi.
Har bosqich Playwright bilan brauzerda ochilib tekshirilgan; "Brauzerda natija" kadri — o'sha skrinshot.
"""

from .lesson_kit import lesson, step

M = "9-oy · 1-sayt: Portfolio"

SKILLS = '''      <ul>
        <li>Python</li>
        <li>aiogram 3</li>
        <li>Git va GitHub</li>
      </ul>'''

FORM = '''      <form id="contact-form">
        <label for="name">Ismingiz</label>
        <input id="name" name="name" required>
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required>
        <label for="message">Xabar</label>
        <textarea id="message" name="message" rows="4" required></textarea>
        <button type="submit" class="btn">Yuborish</button>
      </form>'''

CARDS = '''      <div class="grid">
        <article class="card">
          <h3>QuizBot</h3>
          <p>Telegram test boti: aiogram 3, SQLite, admin panel.</p>
          <span class="tag">Python</span>
          <a href="https://github.com/ali/quizbot">GitHub</a>
        </article>
        <article class="card">
          <h3>Kundalik</h3>
          <p>Konsol vazifalar ro'yxati: OOP va JSON.</p>
          <span class="tag">Python</span>
          <a href="https://github.com/ali/kundalik">GitHub</a>
        </article>
        <article class="card">
          <h3>Portfolio</h3>
          <p>Shu sayt: HTML, CSS va JavaScript.</p>
          <span class="tag">Web</span>
          <a href="https://github.com/ali/ali.github.io">GitHub</a>
        </article>
      </div>'''


def index_html(n: int) -> str:
    head = [
        "<!DOCTYPE html>",
        '<html lang="uz">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    ]
    if n >= 12:
        head += [
            '  <meta name="description" content="Ali Valiyev — Python dasturchi: Telegram botlar va saytlar">',
            '  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 '
            'viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚀</text></svg>">',
        ]
    head.append("  <title>Ali Valiyev — Portfolio</title>")
    if n >= 4:
        head.append('  <link rel="stylesheet" href="style.css">')
    if n >= 9:
        head.append('  <script src="script.js" defer></script>')
    head += ["</head>", "<body>"]
    if n == 1:
        body = ["  <h1>Ali Valiyev</h1>", "  <p>Men 14 yoshdaman va Python dasturchisiman.</p>"]
    elif n == 2:
        body = [
            "  <h1>Ali Valiyev</h1>",
            "  <p>Men 14 yoshdaman va Python dasturchisiman.</p>",
            '  <img src="images/ali.jpg" alt="Ali Valiyev surati" width="200">',
            "  <h2>Men haqimda</h2>",
            "  <p>Minar Dasturchi kursida <strong>Telegram bot</strong> va saytlar yaratishni o'rganyapman.</p>",
            "  <h2>Ko'nikmalarim</h2>",
            SKILLS.replace("      ", "  ", 1).replace("\n        ", "\n    ").replace("\n      </ul>", "\n  </ul>"),
            '  <a href="https://github.com/ali" target="_blank">GitHub profilim</a>',
        ]
    else:
        nav = ["  <header>", "    <nav>", '      <a href="#" class="logo">AV</a>']
        if n >= 7:
            nav.append('      <button class="burger" aria-label="Menyu" aria-expanded="false">☰</button>')
        nav += [
            '      <ul class="menu">',
            '        <li><a href="#about">Men haqimda</a></li>',
            '        <li><a href="#projects">Loyihalar</a></li>',
            '        <li><a href="#contact">Aloqa</a></li>',
            "      </ul>",
        ]
        if n >= 10:
            nav.append('      <button class="theme-toggle" aria-label="Tungi rejim">🌙</button>')
        nav += ["    </nav>", "  </header>", ""]
        hero = ['    <section class="hero">', '      <img src="images/ali.jpg" alt="Ali Valiyev surati" width="160">',
                "      <h1>Ali Valiyev</h1>"]
        if n >= 9:
            hero.append('      <p id="greeting"></p>')
        hero.append("      <p>14 yoshli Python dasturchi · Telegram botlar va saytlar</p>")
        if n >= 5:
            hero += [
                '      <div class="actions">',
                '        <a href="#projects" class="btn">Loyihalar</a>',
                '        <a href="#contact" class="btn btn-outline">Bog\'lanish</a>',
                "      </div>",
            ]
        hero.append("    </section>")
        about = [
            "",
            '    <section id="about">',
            "      <h2>Men haqimda</h2>",
            "      <p>Minar Dasturchi kursida <strong>Telegram bot</strong> va saytlar yaratishni o'rganyapman.</p>",
            SKILLS,
            "    </section>",
        ]
        projects = ["", '    <section id="projects">', "      <h2>Loyihalarim</h2>"]
        if n >= 11:
            projects += [
                '      <div class="filters">',
                '        <button data-filter="all">Hammasi</button>',
                '        <button data-filter="python">Python</button>',
                '        <button data-filter="bot">Bot</button>',
                '        <button data-filter="web">Web</button>',
                "      </div>",
                '      <div class="grid" id="project-list"></div>',
            ]
        elif n >= 6:
            projects.append(CARDS)
        else:
            projects += [
                '      <article class="card">',
                "        <h3>QuizBot</h3>",
                "        <p>Telegram test boti: aiogram 3, SQLite, admin panel.</p>",
                '        <a href="https://github.com/ali/quizbot">GitHub</a>',
                "      </article>",
            ]
        projects.append("    </section>")
        contact = ["", '    <section id="contact">', "      <h2>Aloqa</h2>", FORM]
        if n >= 10:
            contact.append('      <p class="form-msg" role="status"></p>')
        contact.append("    </section>")
        footer = ["  </main>", "", "  <footer>", '    <p>© <span id="year">2026</span> Ali Valiyev</p>', "  </footer>"]
        body = nav + ["  <main>"] + hero + about + projects + contact + footer
    return "\n".join(head + body + ["</body>", "</html>", ""])


CSS_BASE = '''* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Segoe UI", system-ui, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background: #f8fafc;
}

section {
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 20px;
}

h2 {
  color: #0f766e;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
}

form {
  display: grid;
  gap: 8px;
  max-width: 480px;
}

input,
textarea {
  font: inherit;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}
'''

CSS_FLEX = '''
header {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 960px;
  margin: 0 auto;
  padding: 16px 20px;
}

.logo {
  font-weight: 700;
  color: #0f766e;
  text-decoration: none;
}

.menu {
  display: flex;
  gap: 24px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu a {
  color: inherit;
  text-decoration: none;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero img {
  border-radius: 50%;
}

.actions {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 20px;
  border: 2px solid #0f766e;
  border-radius: 8px;
  background: #0f766e;
  color: #ffffff;
  font: inherit;
  text-decoration: none;
  cursor: pointer;
}

.btn-outline {
  background: transparent;
  color: #0f766e;
}
'''

CSS_GRID = '''
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.card h3 {
  margin-top: 0;
}

.tag {
  display: inline-block;
  margin-right: 8px;
  padding: 2px 10px;
  border-radius: 999px;
  background: #ccfbf1;
  color: #115e59;
  font-size: 13px;
}
'''

CSS_RESPONSIVE = '''
header {
  position: relative;
}

.burger {
  display: none;
  font-size: 24px;
  background: none;
  border: 0;
  cursor: pointer;
}

@media (max-width: 700px) {
  .burger {
    display: block;
  }

  .menu {
    display: none;
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
  }

  .menu.open {
    display: flex;
  }

  .menu a {
    display: block;
    padding: 14px 20px;
  }

  section {
    padding: 32px 16px;
  }
}
'''

CSS_VARS = '''
:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --text: #1f2937;
  --accent: #0f766e;
  --border: #e5e7eb;
}

[data-theme="dark"] {
  --bg: #0f172a;
  --surface: #1e293b;
  --text: #e2e8f0;
  --accent: #5eead4;
  --border: #334155;
}

body,
header,
.menu {
  background: var(--bg);
  color: var(--text);
}

header,
.card {
  border-color: var(--border);
}

.card {
  background: var(--surface);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}

h2,
.logo,
.btn-outline {
  color: var(--accent);
}

.btn,
.btn-outline {
  border-color: var(--accent);
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
'''

CSS_JS = '''
.theme-toggle {
  font-size: 20px;
  background: none;
  border: 0;
  cursor: pointer;
}

.form-msg {
  min-height: 1.6em;
  color: var(--accent);
  font-weight: 600;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.filters button {
  font: inherit;
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
'''


def style_css(n: int) -> str:
    css = CSS_BASE
    if n >= 5:
        css += CSS_FLEX
    if n >= 6:
        css += CSS_GRID
    if n >= 7:
        css += CSS_RESPONSIVE
    if n >= 8:
        css += CSS_VARS
    if n >= 10:
        css += CSS_JS
    return css


JS_BASICS = '''const year = document.querySelector("#year");
year.textContent = new Date().getFullYear();

const greeting = document.querySelector("#greeting");
const hour = new Date().getHours();
let text = "Xayrli kech";
if (hour < 12) {
  text = "Xayrli tong";
} else if (hour < 18) {
  text = "Xayrli kun";
}
greeting.textContent = `${text}! Saytimga xush kelibsiz 👋`;
'''

JS_MENU = '''
const burger = document.querySelector(".burger");
const menu = document.querySelector(".menu");
burger.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  burger.setAttribute("aria-expanded", open);
});
'''

JS_THEME_10 = '''
const themeBtn = document.querySelector(".theme-toggle");
themeBtn.addEventListener("click", () => {
  const dark = document.documentElement.dataset.theme === "dark";
  document.documentElement.dataset.theme = dark ? "light" : "dark";
  themeBtn.textContent = dark ? "🌙" : "☀️";
});
'''

JS_THEME_11 = '''
const themeBtn = document.querySelector(".theme-toggle");

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeBtn.textContent = theme === "dark" ? "☀️" : "🌙";
  localStorage.setItem("theme", theme);
}

setTheme(localStorage.getItem("theme") || "light");
themeBtn.addEventListener("click", () => {
  setTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
});
'''

JS_FORM = '''
const form = document.querySelector("#contact-form");
const formMsg = document.querySelector(".form-msg");
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = form.elements.name.value.trim();
  if (name.length < 2) {
    formMsg.textContent = "Ism kamida 2 harf bo'lsin";
    return;
  }
  formMsg.textContent = `Rahmat, ${name}! Xabaringiz qabul qilindi.`;
  form.reset();
});
'''

JS_PROJECTS = '''
const projects = [
  { title: "QuizBot", text: "Telegram test boti: aiogram 3, SQLite.", tags: ["python", "bot"] },
  { title: "Kundalik", text: "Konsol vazifalar ro'yxati: OOP va JSON.", tags: ["python"] },
  { title: "Portfolio", text: "Shu sayt: HTML, CSS va JavaScript.", tags: ["web"] },
];

const list = document.querySelector("#project-list");

function render(filter) {
  const items = filter === "all" ? projects : projects.filter((p) => p.tags.includes(filter));
  list.innerHTML = items
    .map((p) => `<article class="card"><h3>${p.title}</h3><p>${p.text}</p></article>`)
    .join("");
}

document.querySelectorAll("[data-filter]").forEach((btn) => {
  btn.addEventListener("click", () => render(btn.dataset.filter));
});
render("all");
'''


def script_js(n: int) -> str:
    js = JS_BASICS
    if n >= 10:
        js += JS_MENU + (JS_THEME_11 if n >= 11 else JS_THEME_10) + JS_FORM
    if n >= 11:
        js += JS_PROJECTS
    return js


README = '''# Ali Valiyev — Portfolio

Shaxsiy sayt: men haqimda, loyihalarim va aloqa formasi. HTML, CSS va JavaScript.

🔗 https://ali.github.io

## Imkoniyatlar
- Moslashuvchan dizayn (telefon va kompyuter)
- Tungi rejim (localStorage'da eslab qolinadi)
- Loyihalarni filtrlash
'''


def files(n: int) -> dict:
    out = {"index.html": index_html(n)}
    if n >= 4:
        out["style.css"] = style_css(n)
    if n >= 9:
        out["script.js"] = script_js(n)
    if n >= 12:
        out["README.md"] = README
    return out


def preview(n: int, checks: list, url: str = "index.html") -> dict:
    return {"image": f"lessons/WB{n:02}/site.png", "title": "Brauzerda natija", "sub": "chapda — kompyuter, o'ngda — telefon",
            "url": url, "checks": checks}


def tree(n: int, changed: dict) -> list:
    rows = [("portfolio/", "")]
    names = list(files(n)) + ["images/ali.jpg"]
    for i, name in enumerate(names):
        rows.append((("└── " if i == len(names) - 1 else "├── ") + name, changed.get(name, "")))
    return rows


LESSONS = {
    "WB01": lesson(
        M, 1, "Veb qanday ishlaydi va HTML skelet",
        "Brauzer, server va HTML'ni tushunamiz; birinchi veb-sahifamizni yozamiz.",
        "6–8-oylarda: bot va server; Starter'da: brauzer va Google xizmatlari.",
        "Sayt ochilganda nima sodir bo'ladi? Brauzer serverdan nimani so'raydi?",
        "Brauzer ↔ server; HTML — sahifa tuzilmasi; teg, ochiluvchi va yopiluvchi teg; head va body; lang, charset, viewport.",
        "Sahifaga sarlavha va o'zingiz haqingizda 2 jumla qo'shing.",
        [("💻", "Brauzer", "manzil yoziladi", ""),
         ("🌐", "Server", "HTML faylni beradi", ""),
         ("📄", "HTML", "teglar daraxti", "mem"),
         ("🎨", "Sahifa", "ekranda chiziladi", "")],
        [
            step("index.html", "Hujjat skeleti", '''<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ali Valiyev — Portfolio</title>
</head>''',
                 [("<!DOCTYPE html>", "brauzerga: bu zamonaviy HTML5 hujjat."),
                  ("lang=\"uz\"", "sahifa tili — ekran o'quvchi dasturlar va qidiruv uchun."),
                  ("charset UTF-8", "o‘, g‘ va boshqa harflar to'g'ri chiqadi."),
                  ("viewport", "telefonda sahifa to'g'ri kattalikda ochiladi.")],
                 "Brauzer tabida: Ali Valiyev — Portfolio"),
            step("index.html", "Sahifa mazmuni", '''<body>
  <h1>Ali Valiyev</h1>
  <p>Men 14 yoshdaman va Python dasturchisiman.</p>
</body>
</html>''',
                 [("<body>", "ekranda ko'rinadigan hamma narsa shu yerda."),
                  ("<h1>", "eng katta sarlavha — sahifada bitta."),
                  ("<p>", "oddiy matn abzatsi."),
                  ("yopiluvchi teg", "</h1> — teg qayerda tugashini bildiradi.")],
                 "Ali Valiyev\nMen 14 yoshdaman va Python dasturchisiman."),
        ],
        files(1),
        tree(1, {"index.html": "yangi"}),
        ["Brauzer va server", "HTML teglari", "head va body", "charset va viewport"],
        ["Majburiy: sarlavha va o'zingiz haqingizda 2 jumla qo'shing.",
         "Qo'shimcha: brauzerda F12 → Elements bilan sahifa daraxtini ko'ring."],
        "9.2 · HTML teglar: matn, rasm, havola, ro'yxat.",
        preview=preview(1, ["Fayl brauzerda ochildimi (index.html ni ikki marta bosing)?", "Tab nomi to'g'ri chiqdimi?"]),
    ),
    "WB02": lesson(
        M, 2, "HTML teglar: matn, rasm, havola, ro'yxat",
        "“Men haqimda” sahifasini to'ldiramiz: rasm, sarlavhalar, ro'yxat va havola.",
        "O'tgan darsda: HTML skelet, h1 va p.",
        "<head> va <body> farqi nima?",
        "h2, strong, img (src, alt), a (href, target), ul/li; atributlar; nisbiy yo'l images/ali.jpg.",
        "Sevimli 5 ta kitob yoki film ro'yxatini qo'shing.",
        [("🖼", "<img>", "src + alt", ""),
         ("🔠", "<h2>", "bo'lim sarlavhasi", ""),
         ("📋", "<ul><li>", "ro'yxat", "mem"),
         ("🔗", "<a href>", "havola", "")],
        [
            step("index.html", "Rasm va sarlavhalar", '''  <img src="images/ali.jpg" alt="Ali Valiyev surati" width="200">
  <h2>Men haqimda</h2>
  <p>Minar Dasturchi kursida <strong>Telegram bot</strong> va saytlar yaratishni o'rganyapman.</p>''',
                 [("src", "rasm fayli yo'li — images papkasida."),
                  ("alt", "rasm ochilmasa yoki ko'rmaydigan foydalanuvchi uchun matn."),
                  ("<strong>", "muhim so'z — qalin.")],
                 "🖼 + Men haqimda"),
            step("index.html", "Ro'yxat va havola", '''  <h2>Ko'nikmalarim</h2>
  <ul>
    <li>Python</li>
    <li>aiogram 3</li>
    <li>Git va GitHub</li>
  </ul>
  <a href="https://github.com/ali" target="_blank">GitHub profilim</a>''',
                 [("<ul> / <li>", "nuqtali ro'yxat; <ol> — raqamli."),
                  ("href", "havola manzili."),
                  ("target=\"_blank\"", "yangi tabda ochiladi.")],
                 "• Python • aiogram 3 • Git va GitHub\nGitHub profilim"),
        ],
        files(2),
        tree(2, {"index.html": "o‘zgardi", "images/ali.jpg": "yangi"}),
        ["Sarlavhalar darajasi", "img: src va alt", "Ro'yxatlar", "Havolalar va atributlar"],
        ["Majburiy: sevimli 5 ta kitob/film ro'yxatini qo'shing.",
         "Qo'shimcha: <ol> bilan “Bu yilgi maqsadlarim” ro'yxati."],
        "9.3 · Semantik HTML va forma.",
        preview=preview(2, ["Rasm chiqdimi (fayl yo'li to'g'rimi)?", "Havola yangi tabda ochildimi?"]),
    ),
    "WB03": lesson(
        M, 3, "Semantik HTML va forma",
        "Sahifani ma'noli qismlarga bo'lamiz va aloqa formasini qo'shamiz.",
        "O'tgan darsda: img, h2, ul, a.",
        "alt atributi nima uchun kerak?",
        "Semantik teglar: header, nav, main, section, article, footer; id va #havola; form, label, input, textarea, required.",
        "Formaga “Mavzu” tanlash maydonini (select) qo'shing.",
        [("🔝", "header + nav", "menyu", ""),
         ("📰", "main", "section'lar", "mem"),
         ("🃏", "article", "loyiha kartasi", ""),
         ("✉", "form", "label + input", ""),
         ("⬇", "footer", "pastki qism", "")],
        [
            step("index.html", "Menyu va bo'limlar", '''  <header>
    <nav>
      <a href="#" class="logo">AV</a>
      <ul class="menu">
        <li><a href="#about">Men haqimda</a></li>
        <li><a href="#projects">Loyihalar</a></li>
        <li><a href="#contact">Aloqa</a></li>
      </ul>
    </nav>
  </header>''',
                 [("<header>, <nav>", "sahifa boshi va navigatsiya — qidiruv tizimlari ham tushunadi."),
                  ("href=\"#about\"", "shu sahifadagi id=\"about\" bo'limiga sakrash."),
                  ("class", "keyin CSS bilan bezash uchun nom.")],
                 "AV · Men haqimda · Loyihalar · Aloqa"),
            step("index.html", "Loyiha kartasi", '''    <section id="projects">
      <h2>Loyihalarim</h2>
      <article class="card">
        <h3>QuizBot</h3>
        <p>Telegram test boti: aiogram 3, SQLite, admin panel.</p>
        <a href="https://github.com/ali/quizbot">GitHub</a>
      </article>
    </section>''',
                 [("<section id>", "mavzuli bo'lim; id — havola uchun."),
                  ("<article>", "mustaqil mazmun — bitta loyiha.")],
                 "Loyihalarim → QuizBot kartasi"),
            step("index.html", "Aloqa formasi", FORM,
                 [("<label for>", "yozuvni bosganda maydon faollashadi — kirish oson."),
                  ("type=\"email\"", "brauzer email formatini tekshiradi."),
                  ("required", "bo'sh qoldirib yuborib bo'lmaydi.")],
                 "Ismingiz [ ] Email [ ] Xabar [ ] [Yuborish]"),
        ],
        files(3),
        tree(3, {"index.html": "o‘zgardi"}),
        ["Semantik teglar", "id va ichki havolalar", "article va section", "Forma va label"],
        ["Majburiy: formaga “Mavzu” select maydonini qo'shing.",
         "Qo'shimcha: footer'ga Telegram havolasini qo'shing."],
        "9.4 · CSS asoslari va box model.",
        preview=preview(3, ["Menyu havolalari bo'limlarga sakradimi?", "Bo'sh forma yuborilmadimi (required)?"]),
    ),
    "WB04": lesson(
        M, 4, "CSS asoslari va box model",
        "Sahifaga uslub beramiz: shrift, rang, oraliqlar va kartalar.",
        "O'tgan darsda: semantik HTML va forma.",
        "<section> va <article> farqi nima?",
        "CSS ulash (link), selektorlar (teg, .class), xususiyatlar; box model: content, padding, border, margin; box-sizing.",
        "O'z rang palitrangizni bering (3 ta rang).",
        [("🔗", "<link>", "style.css ulanadi", ""),
         ("🎯", "Selektor", "body, .card", ""),
         ("📦", "Box model", "padding · border · margin", "mem"),
         ("🎨", "Natija", "toza sahifa", "")],
        [
            step("index.html", "CSS faylni ulaymiz", '''  <link rel="stylesheet" href="style.css">''',
                 [("<link>", "head ichida — uslublar sahifa chizilishidan oldin yuklanadi."),
                  ("href", "index.html yonidagi style.css.")],
                 "style.css ulandi"),
            step("style.css", "Umumiy uslublar", '''* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Segoe UI", system-ui, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background: #f8fafc;
}''',
                 [("*", "hamma elementlar."),
                  ("box-sizing: border-box", "kenglikka padding va border ham kiradi — hisoblash oson."),
                  ("line-height", "qatorlar orasi — matn o'qishga qulay.")],
                 "shrift va fon o'zgardi"),
            step("style.css", "Bo'lim va karta", '''section {
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 20px;
}

h2 {
  color: #0f766e;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
}''',
                 [("margin: 0 auto", "blokni markazga qo'yadi."),
                  ("padding", "ichki bo'shliq; margin — tashqi."),
                  (".card", "nuqta bilan — class selektori.")],
                 "markazlangan bo'limlar, oq karta"),
        ],
        files(4),
        tree(4, {"index.html": "o‘zgardi", "style.css": "yangi"}),
        ["CSS ulash", "Selektorlar", "Box model", "box-sizing"],
        ["Majburiy: 3 ta rangdan iborat palitrangizni bering.",
         "Qo'shimcha: F12 → Computed bilan kartaning box model'ini ko'ring."],
        "9.5 · Flexbox: navigatsiya va hero.",
        preview=preview(4, ["Fon va shrift o'zgardimi?", "Bo'limlar markazda va kengligi cheklanganmi?"]),
    ),
    "WB05": lesson(
        M, 5, "Flexbox: navigatsiya va hero",
        "Menyuni bir qatorga, bosh blokni markazga joylaymiz va tugmalar qo'shamiz.",
        "O'tgan darsda: CSS asoslari va box model.",
        "padding va margin farqi?",
        "display: flex; justify-content, align-items, gap, flex-direction; tugma uslubi (.btn, .btn-outline).",
        "Hero'ga ikkinchi qator tugma qo'shib, ularni yonma-yon joylang.",
        [("↔", "nav: flex", "space-between", "mem"),
         ("📋", ".menu: flex", "gap: 24px", ""),
         ("⬇", ".hero: column", "markazda", ""),
         ("🔘", ".btn", "tugmalar", "")],
        [
            step("style.css", "Menyu bir qatorda", '''nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 960px;
  margin: 0 auto;
  padding: 16px 20px;
}

.menu {
  display: flex;
  gap: 24px;
  list-style: none;
  margin: 0;
  padding: 0;
}''',
                 [("display: flex", "ichki elementlar bir qatorga tiziladi."),
                  ("space-between", "logo chapda, menyu o'ngda."),
                  ("gap", "elementlar orasidagi masofa.")],
                 "AV ··········· Men haqimda  Loyihalar  Aloqa"),
            step("style.css", "Bosh blok (hero)", '''.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero img {
  border-radius: 50%;
}''',
                 [("flex-direction: column", "elementlar ustma-ust."),
                  ("align-items: center", "gorizontal markaz."),
                  ("border-radius: 50%", "dumaloq rasm.")],
                 "markazda dumaloq rasm va ism"),
            step("index.html · style.css", "Tugmalar", '''      <div class="actions">
        <a href="#projects" class="btn">Loyihalar</a>
        <a href="#contact" class="btn btn-outline">Bog'lanish</a>
      </div>''',
                 [("ikki class", "btn — umumiy, btn-outline — farqi."),
                  (".actions: flex", "tugmalar yonma-yon, gap bilan.")],
                 "[Loyihalar] [Bog'lanish]"),
        ],
        files(5),
        tree(5, {"index.html": "o‘zgardi", "style.css": "o‘zgardi"}),
        ["display: flex", "justify-content va align-items", "flex-direction", "Tugma uslublari"],
        ["Majburiy: hero'ga ikkinchi qator tugma qo'shing.",
         "Qo'shimcha: menyuda faol bo'limni boshqa rang bilan belgilang."],
        "9.6 · Grid: loyihalar kartalari.",
        preview=preview(5, ["Menyu bir qatordami?", "Hero markazda, tugmalar yonma-yonmi?"]),
    ),
    "WB06": lesson(
        M, 6, "Grid: loyihalar kartalari",
        "Loyihalarni chiroyli to'rga joylaymiz — ekran kengligiga qarab ustunlar soni o'zgaradi.",
        "O'tgan darsda: Flexbox menyu va hero.",
        "justify-content: space-between nima qiladi?",
        "display: grid; grid-template-columns; repeat(auto-fit, minmax(240px, 1fr)); gap; teg-yorliqlar.",
        "Kartaga rasm va “Ko'rish” havolasini qo'shing.",
        [("🔲", "display: grid", "to'r", "mem"),
         ("📏", "minmax(240px, 1fr)", "eng kami 240 px", ""),
         ("🔁", "auto-fit", "ustunlar o'zi", ""),
         ("🏷", ".tag", "yorliq", "")],
        [
            step("index.html", "Uchta karta", CARDS.split("\n        <article class=\"card\">\n          <h3>Kundalik</h3>")[0],
                 [("<div class=\"grid\">", "kartalar uchun konteyner."),
                  ("<span class=\"tag\">", "texnologiya yorlig'i.")],
                 "3 ta loyiha kartasi"),
            step("style.css", "Grid to'ri", '''.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}''',
                 [("auto-fit", "sig'gancha ustun — kompyuterda 3, telefonda 1."),
                  ("minmax(240px, 1fr)", "karta 240 px dan torroq bo'lmaydi."),
                  ("media query'siz", "moslashuv o'zi.")],
                 "kompyuter: 3 ustun · telefon: 1 ustun"),
            step("style.css", "Yorliq", '''.tag {
  display: inline-block;
  margin-right: 8px;
  padding: 2px 10px;
  border-radius: 999px;
  background: #ccfbf1;
  color: #115e59;
  font-size: 13px;
}''',
                 [("inline-block", "matn ichida, lekin padding oladi."),
                  ("999px", "to'liq yumaloq chetlar.")],
                 "[Python] yorlig'i"),
        ],
        files(6),
        tree(6, {"index.html": "o‘zgardi", "style.css": "o‘zgardi"}),
        ["display: grid", "repeat va minmax", "auto-fit", "Yorliqlar"],
        ["Majburiy: kartaga rasm va “Ko'rish” havolasini qo'shing.",
         "Qo'shimcha: grid-template-areas bilan “Men haqimda” bo'limini 2 ustun qiling."],
        "9.7 · Responsive dizayn: media query.",
        preview=preview(6, ["Kompyuterda kartalar 3 ustundami?", "Oyna toraytirilganda ustunlar kamaydimi?"]),
    ),
    "WB07": lesson(
        M, 7, "Responsive dizayn: media query",
        "Telefonda menyu ☰ tugmasi ostiga yashirinadi, bo'limlar ixchamlashadi.",
        "O'tgan darsda: Grid kartalar.",
        "auto-fit va minmax nima qiladi?",
        "@media (max-width: 700px); mobil menyu (position: absolute); .open klassi; telefonda tekshirish (F12 → qurilma rejimi).",
        "Planshet (768–1024 px) uchun alohida ko'rinish qo'shing.",
        [("📱", "max-width: 700px", "telefon", "mem"),
         ("☰", ".burger", "faqat telefonda", ""),
         ("🙈", ".menu", "yashirin", ""),
         ("👁", ".menu.open", "ochiladi (10-dars JS)", "")],
        [
            step("index.html", "Menyu tugmasi", '''      <button class="burger" aria-label="Menyu" aria-expanded="false">☰</button>''',
                 [("<button>", "bosiladigan element — havola emas."),
                  ("aria-label", "ekran o'quvchi “Menyu” deb o'qiydi."),
                  ("aria-expanded", "menyu ochiq yoki yopiqligi.")],
                 "☰ tugmasi"),
            step("style.css", "Telefon uchun qoidalar", '''@media (max-width: 700px) {
  .burger {
    display: block;
  }

  .menu {
    display: none;
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    flex-direction: column;
    gap: 0;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
  }''',
                 [("@media", "ekran 700 px dan tor bo'lsa ichidagi qoidalar ishlaydi."),
                  ("display: none", "telefonda menyu boshida yashirin."),
                  ("position: absolute", "header ostidan ochiladi (header — relative).")],
                 "telefonda: AV ··· ☰"),
            step("style.css", "Ochilgan menyu va ixcham bo'limlar", '''  .menu.open {
    display: flex;
  }

  .menu a {
    display: block;
    padding: 14px 20px;
  }

  section {
    padding: 32px 16px;
  }
}''',
                 [(".menu.open", "JS bu klassni qo'shganda menyu ko'rinadi (10-dars)."),
                  ("14px padding", "barmoq bilan bosishga qulay katta maydon.")],
                 "telefonda bo'limlar ixcham"),
        ],
        files(7),
        tree(7, {"index.html": "o‘zgardi", "style.css": "o‘zgardi"}),
        ["Media query", "Mobil menyu", "position: absolute", "Qurilma rejimida tekshirish"],
        ["Majburiy: planshet uchun alohida ko'rinish qo'shing.",
         "Qo'shimcha: telefonda hero rasmini kichikroq qiling."],
        "9.8 · CSS o'zgaruvchilari va animatsiya.",
        preview=preview(7, ["Telefonda menyu yashirinib, ☰ chiqdimi?", "Gorizontal aylantirish paydo bo'lmadimi?"]),
    ),
    "WB08": lesson(
        M, 8, "CSS o'zgaruvchilari va animatsiya",
        "Ranglarni o'zgaruvchilarga olamiz — tungi rejim uchun tayyorlanamiz; kartalarga yumshoq harakat beramiz.",
        "O'tgan darsda: media query va mobil menyu.",
        "@media (max-width: 700px) qachon ishlaydi?",
        ":root va --o'zgaruvchi, var(); [data-theme=\"dark\"]; transition, :hover, transform; prefers-reduced-motion.",
        "Kartalarga sahifa ochilganda paydo bo'lish animatsiyasini qo'shing.",
        [("🎨", ":root", "--bg, --text ...", "mem"),
         ("🌙", "[data-theme=dark]", "boshqa qiymatlar", ""),
         ("🔁", "var(--bg)", "hamma joyda", ""),
         ("✨", ":hover", "transition", "")],
        [
            step("style.css", "Rang o'zgaruvchilari", CSS_VARS.split("\n\nbody,\nheader,")[0].lstrip("\n"),
                 [("--bg", "o'zgaruvchi — bir joyda o'zgartirsangiz hamma joyda o'zgaradi."),
                  ("[data-theme=\"dark\"]", "html'ga shu atribut qo'yilsa — tungi ranglar."),
                  ("rejim JS bilan", "almashtirishni 10-darsda yozamiz.")],
                 "ranglar bitta joyda"),
            step("style.css", "var() bilan ishlatish", '''body,
header,
.menu {
  background: var(--bg);
  color: var(--text);
}''',
                 [("var(--bg)", "o'zgaruvchi qiymatini oladi."),
                  ("vergul bilan", "bir qoida bir nechta selektorga.")],
                 "fon va matn o'zgaruvchidan"),
            step("style.css", "Hover animatsiyasi", '''.card {
  background: var(--surface);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}''',
                 [("transition", "o'zgarish 0.2 soniyada silliq bo'ladi."),
                  ("translateY(-4px)", "karta biroz ko'tariladi."),
                  ("reduced-motion", "harakatni yoqtirmaydiganlar uchun animatsiya o'chiriladi.")],
                 "sichqoncha kelganda karta ko'tariladi"),
        ],
        files(8),
        tree(8, {"style.css": "o‘zgardi"}),
        ["CSS o'zgaruvchilari", "[data-theme] atributi", "transition va :hover", "prefers-reduced-motion"],
        ["Majburiy: kartalarga paydo bo'lish animatsiyasi (@keyframes).",
         "Qo'shimcha: F12'da html'ga data-theme=\"dark\" yozib, tungi ranglarni sinang."],
        "9.9 · JavaScript asoslari va DOM.",
        preview=preview(8, ["Kartaga sichqoncha kelganda ko'tariladimi?", "Ranglar o'zgaruvchilardan olindimi?"]),
    ),
    "WB09": lesson(
        M, 9, "JavaScript asoslari va DOM",
        "Sahifaga jon kiritamiz: joriy yil va kun vaqtiga qarab salomlashish.",
        "O'tgan darsda: CSS o'zgaruvchilari.",
        "Python'dagi if/elif/else ni eslang — JS'da qanday bo'ladi?",
        "JS ulash (script defer); const, let; document.querySelector; textContent; Date; if / else if; shablon satr `${}`.",
        "Sahifada bugungi sanani “19-noyabr” ko'rinishida chiqaring.",
        [("📜", "script.js", "defer", ""),
         ("🔍", "querySelector", "elementni topish", "mem"),
         ("✏", "textContent", "matnni o'zgartirish", ""),
         ("🕐", "Date", "soat va yil", "")],
        [
            step("index.html", "Skriptni ulash va joy", '''  <script src="script.js" defer></script>''',
                 [("defer", "skript sahifa to'liq yuklangach ishlaydi — elementlar tayyor."),
                  ("<p id=\"greeting\">", "hero'da salom uchun bo'sh joy.")],
                 "script.js ulandi"),
            step("script.js", "Joriy yil", '''const year = document.querySelector("#year");
year.textContent = new Date().getFullYear();''',
                 [("const", "qayta tayinlanmaydigan o'zgaruvchi (Python'dagi o'zgaruvchiga o'xshash)."),
                  ("querySelector(\"#year\")", "CSS selektori bilan elementni topadi."),
                  ("textContent", "element ichidagi matn.")],
                 "© 2026 Ali Valiyev (yil o'zi yangilanadi)"),
            step("script.js", "Vaqtga qarab salom", '''const greeting = document.querySelector("#greeting");
const hour = new Date().getHours();
let text = "Xayrli kech";
if (hour < 12) {
  text = "Xayrli tong";
} else if (hour < 18) {
  text = "Xayrli kun";
}
greeting.textContent = `${text}! Saytimga xush kelibsiz 👋`;''',
                 [("let", "qiymati o'zgaradigan o'zgaruvchi."),
                  ("{ }", "JS'da blok chekinish bilan emas, qavs bilan."),
                  ("`${text}`", "shablon satr — Python f-string kabi.")],
                 "Xayrli kun! Saytimga xush kelibsiz 👋"),
        ],
        files(9),
        tree(9, {"index.html": "o‘zgardi", "script.js": "yangi"}),
        ["JS ulash va defer", "const va let", "querySelector va textContent", "if / else if, shablon satr"],
        ["Majburiy: bugungi sanani “19-noyabr” ko'rinishida chiqaring.",
         "Qo'shimcha: F12 → Console'da console.log bilan o'zgaruvchilarni ko'ring."],
        "9.10 · JS hodisalar: tungi rejim, menyu, forma.",
        preview=preview(9, ["Salom matni vaqtga mos chiqdimi?", "Footer'da joriy yil chiqdimi?", "Console'da xato yo'qmi?"]),
    ),
    "WB10": lesson(
        M, 10, "JS hodisalar: tungi rejim, menyu, forma",
        "Tugmalar ishlaydi: mobil menyu ochiladi, tungi rejim yoqiladi, forma tekshiriladi.",
        "O'tgan darsda: DOM, textContent, Date.",
        "querySelector nima qaytaradi?",
        "addEventListener(\"click\" / \"submit\"); arrow funksiya; classList.toggle; dataset; event.preventDefault(); forma qiymatlari.",
        "Forma yuborilgach 3 soniyadan keyin xabarni yashiring (setTimeout).",
        [("👆", "click", "hodisa", ""),
         ("☰", "classList.toggle", "menyu open", ""),
         ("🌙", "dataset.theme", "dark / light", "mem"),
         ("✉", "submit", "preventDefault + tekshiruv", "")],
        [
            step("script.js", "Mobil menyu", JS_MENU.strip("\n"),
                 [("addEventListener", "hodisa bo'lganda funksiyani chaqiradi."),
                  ("() => { }", "arrow funksiya — qisqa yozuv."),
                  ("classList.toggle", "klass bo'lsa olib tashlaydi, yo'q bo'lsa qo'shadi; true/false qaytaradi.")],
                 "☰ bosilganda menyu ochiladi"),
            step("script.js", "Tungi rejim", JS_THEME_10.strip("\n"),
                 [("dataset.theme", "html'dagi data-theme atributi — CSS o'zgaruvchilari ishga tushadi."),
                  ("? :", "qisqa shart (Python'dagi A if shart else B)."),
                  ("8-dars", "ranglar tayyor edi — endi faqat almashtiramiz.")],
                 "🌙 → ☀️ tungi rejim"),
            step("script.js", "Formani tekshirish", JS_FORM.strip("\n"),
                 [("preventDefault()", "sahifa qayta yuklanmaydi."),
                  ("form.elements.name", "maydonni name orqali olish."),
                  ("role=\"status\"", "ekran o'quvchi xabarni o'qib beradi.")],
                 "Rahmat, Ali! Xabaringiz qabul qilindi."),
        ],
        files(10),
        tree(10, {"index.html": "o‘zgardi", "style.css": "o‘zgardi", "script.js": "o‘zgardi"}),
        ["addEventListener", "classList.toggle", "dataset va tungi rejim", "preventDefault va forma"],
        ["Majburiy: xabarni 3 soniyadan keyin yashiring (setTimeout).",
         "Qo'shimcha: menyudagi havola bosilganda menyu yopilsin."],
        "9.11 · JS massivlar va localStorage.",
        preview=preview(10, ["☰ telefonda menyuni ochdimi?", "🌙 tungi rejimni yoqdimi?", "Forma yuborilgach “Rahmat” chiqdimi?"]),
    ),
    "WB11": lesson(
        M, 11, "JS massivlar va localStorage",
        "Loyihalarni ma'lumotdan chiqaramiz, filtrlaymiz va tanlangan rejimni eslab qolamiz.",
        "O'tgan darsda: hodisalar, tungi rejim, forma.",
        "classList.toggle nima qaytaradi?",
        "Massiv va obyektlar; filter, map, join; innerHTML; data-* atributlari; localStorage.getItem / setItem.",
        "Loyihalarga “Yangi” belgisini qo'shing (eng oxirgi qo'shilgan).",
        [("📋", "projects", "massiv", "mem"),
         ("🔍", "filter", "teg bo'yicha", ""),
         ("🗺", "map + join", "HTML satr", ""),
         ("💾", "localStorage", "rejim eslab qolinadi", "")],
        [
            step("script.js", "Loyihalar massivi va chizish", '''const list = document.querySelector("#project-list");

function render(filter) {
  const items = filter === "all" ? projects : projects.filter((p) => p.tags.includes(filter));
  list.innerHTML = items
    .map((p) => `<article class="card"><h3>${p.title}</h3><p>${p.text}</p></article>`)
    .join("");
}''',
                 [("filter", "shartga mos elementlar (Python list comprehension'dagi if kabi)."),
                  ("map", "har elementdan HTML satr yasaydi."),
                  ("innerHTML", "element ichini yangi HTML bilan almashtiradi.")],
                 "3 ta karta ma'lumotdan chizildi"),
            step("script.js", "Filtr tugmalari", '''document.querySelectorAll("[data-filter]").forEach((btn) => {
  btn.addEventListener("click", () => render(btn.dataset.filter));
});
render("all");''',
                 [("querySelectorAll", "hamma mos elementlar."),
                  ("data-filter", "tugmadagi ma'lumot: python, bot, web."),
                  ("render(\"all\")", "sahifa ochilganda hammasi.")],
                 "[Bot] → faqat QuizBot"),
            step("script.js", "Rejimni eslab qolish", JS_THEME_11.strip("\n"),
                 [("localStorage", "brauzerda saqlanadi — sahifa yangilansa ham qoladi."),
                  ("|| \"light\"", "saqlanmagan bo'lsa — kunduzgi."),
                  ("setTheme", "bitta funksiya: atribut, tugma belgisi va saqlash.")],
                 "tungi rejim F5'dan keyin ham saqlandi"),
        ],
        files(11),
        tree(11, {"index.html": "o‘zgardi", "script.js": "o‘zgardi"}),
        ["Massiv va obyektlar", "filter, map, join", "innerHTML va data-*", "localStorage"],
        ["Majburiy: loyihalarga “Yangi” belgisi qo'shing.",
         "Qo'shimcha: faol filtr tugmasini boshqa rang bilan belgilang."],
        "9.12 · GitHub Pages'ga joylash va himoya.",
        preview=preview(11, ["Filtr tugmalari kartalarni saraladimi?", "Tungi rejim F5'dan keyin ham saqlandimi?"]),
    ),
    "WB12": lesson(
        M, 12, "GitHub Pages'ga joylash va himoya",
        "Saytni bepul internetga chiqaramiz: username.github.io — va himoya qilamiz.",
        "9-oyda: HTML, CSS (flex, grid, media), JS (DOM, hodisalar, massiv, localStorage).",
        "localStorage nima uchun kerak edi?",
        "GitHub Pages — statik sayt hosting; repo nomi username.github.io; meta description va favicon; README; Lighthouse tekshiruvi.",
        "Saytni Lighthouse bilan tekshirib, 90+ ball oling.",
        [("🐙", "Repo", "ali.github.io", ""),
         ("⬆", "git push", "main", ""),
         ("⚙", "Settings → Pages", "yoqish", "mem"),
         ("🌐", "https://ali.github.io", "internetda", "")],
        [
            step("index.html", "Qidiruv va tab belgisi", '''  <meta name="description" content="Ali Valiyev — Python dasturchi: Telegram botlar va saytlar">''',
                 [("description", "Google natijasida sahifa ostidagi matn."),
                  ("favicon", "tabdagi kichik belgi — data: SVG bilan alohida faylsiz.")],
                 "🚀 Ali Valiyev — Portfolio"),
            step("Terminal", "GitHub'ga yuklash", '''$ git init
$ git add .
$ git commit -m "Portfolio sayti"
$ git branch -M main
$ git remote add origin https://github.com/ali/ali.github.io.git
$ git push -u origin main''',
                 [("ali.github.io", "repo nomi username.github.io bo'lsa — manzil shu."),
                  ("index.html", "repo ildizida bo'lishi shart.")],
                 "* [new branch] main -> main"),
            step("Telegram · GitHub", "Pages'ni yoqish va tekshirish", '''Settings → Pages → Branch: main / (root) → Save
✅ Your site is live at https://ali.github.io
F12 → Lighthouse → Analyze page load''',
                 [("1–2 daqiqa", "birinchi joylash biroz vaqt oladi."),
                  ("Lighthouse", "tezlik, qulaylik va SEO bahosi."),
                  ("har push", "sayt avtomatik yangilanadi.")],
                 "https://ali.github.io — ishlayapti"),
        ],
        files(12),
        tree(12, {"index.html": "o‘zgardi", "README.md": "yangi"}),
        ["GitHub Pages", "meta description va favicon", "README", "Lighthouse"],
        ["Majburiy: Lighthouse'da 90+ ball oling.",
         "Qo'shimcha: saytga o'z domeningizni ulang (CNAME)."],
        "10.1 · Django nima: MVT va birinchi loyiha.",
        preview=preview(12, ["Sayt https://username.github.io da ochildimi?", "Telefonda ham to'g'ri ko'rindimi?"], url="https://ali.github.io"),
    ),
}
