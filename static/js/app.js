// Minar Test — progressive enhancement. Barcha sahifalar JS'siz ham to'liq ishlaydi.
//
// Turbo bilan sahifalar to'liq qayta yuklanmaydi: <body> almashtiriladi, bu skript esa
// bir marta ishlaydi. Shuning uchun:
//   - hujjat darajasidagi tinglovchilar bir marta ulanadi (delegatsiya, elementlar har
//     safar qidiriladi);
//   - sahifaga xos sozlash `init()` da — har bir sahifa ko'rsatilganda (turbo:load).
(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const isMac = /Mac|iPhone|iPad/.test(navigator.platform);
  const typing = (el) =>
    el && (["INPUT", "TEXTAREA", "SELECT"].includes(el.tagName) || el.isContentEditable);
  const visit = (url) => (window.Turbo ? window.Turbo.visit(url) : (window.location.href = url));

  // Tarjima: <script id="js-i18n"> (ui.js_i18n) — kalit o'zbekcha matn; {nom} o'rniga qiymat qo'yiladi.
  // Turbo bilan til almashganda <body> ham yangilanadi, shuning uchun lug'at har safar o'qiladi.
  const t = (text, vars = {}) => {
    let dict = {};
    try { dict = JSON.parse($("#js-i18n")?.textContent || "{}"); } catch { /* bo'sh lug'at */ }
    return (dict[text] || text).replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
  };

  const store = {
    get(key) {
      try { return localStorage.getItem(key); } catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(key, value); } catch { /* private rejim */ }
    },
  };

  // ==========================================================================
  // Bir marta: hujjat darajasidagi tinglovchilar
  // ==========================================================================

  // --- Mavzu: kunduzgi / tungi -------------------------------------------
  const root = document.documentElement;
  const renderTheme = () => {
    const dark = root.dataset.theme === "dark";
    $$("[data-theme-icon]").forEach((el) => (el.hidden = el.dataset.themeIcon !== (dark ? "dark" : "light")));
    const label = dark ? t("Kunduzgi rejim") : t("Tungi rejim");
    $$("[data-theme-label]").forEach((el) => (el.textContent = label));
    $$("[data-theme-toggle][aria-label]").forEach((el) => el.setAttribute("aria-label", label));
  };
  document.addEventListener("click", (e) => {
    if (!e.target.closest("[data-theme-toggle]")) return;
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store.set("theme", root.dataset.theme);
    renderTheme();
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", (e) => {
    if (store.get("theme")) return; // foydalanuvchi o'zi tanlagan
    root.dataset.theme = e.matches ? "dark" : "light";
    renderTheme();
  });

  // --- Mobil menyu ---------------------------------------------------------
  const setNav = (open) => {
    document.body.classList.toggle("nav-open", open);
    $("[data-nav-toggle]")?.setAttribute("aria-expanded", String(open));
  };
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-nav-toggle]")) setNav(!document.body.classList.contains("nav-open"));
    else if (e.target.closest("[data-nav-close]")) setNav(false);
  });

  // --- Toast xabarlar --------------------------------------------------------
  const dismiss = (toast) => {
    if (!toast || toast.classList.contains("leaving")) return;
    toast.classList.add("leaving");
    toast.addEventListener("animationend", () => toast.remove(), { once: true });
    setTimeout(() => toast.remove(), 400);
  };
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-toast-close]");
    if (btn) dismiss(btn.closest("[data-toast]"));
  });

  // --- Xavfli amallar uchun tasdiq: <button data-confirm="..."> ------------
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-confirm]");
    if (el && !window.confirm(el.getAttribute("data-confirm"))) e.preventDefault();
  });

  // --- Nusxa olish: <button data-copy="matn"> -------------------------------
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-copy]");
    if (!btn) return;
    const text = btn.getAttribute("data-copy");
    const done = () => {
      const label = btn.textContent;
      btn.textContent = t("Nusxalandi ✓");
      setTimeout(() => (btn.textContent = label), 1500);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, () => window.prompt(t("Nusxa oling:"), text));
    } else {
      window.prompt(t("Nusxa oling:"), text);
    }
  });

  // --- Parol: ko'rsatish/yashirish va Caps Lock ogohlantirishi ---------------
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-password-toggle]");
    if (!btn) return;
    const input = btn.parentElement.querySelector("input");
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    btn.setAttribute("aria-pressed", String(show));
    btn.setAttribute("aria-label", show ? btn.dataset.labelHide : btn.dataset.labelShow);
    $$("[data-eye]", btn).forEach((el) => (el.hidden = el.dataset.eye !== (show ? "hide" : "show")));
    input.focus();
  });
  const capsCheck = (e) => {
    if (!e.target.matches?.('input[type="password"], [data-password-toggle] ~ input, .has-action > input') || !e.getModifierState) return;
    const hint = e.target.closest(".field")?.querySelector("[data-caps-hint]");
    if (hint) hint.hidden = !e.getModifierState("CapsLock");
  };
  document.addEventListener("keydown", capsCheck);
  document.addEventListener("keyup", capsCheck);

  // --- Filtr o'zgarganda formani yuborish ----------------------------------
  document.addEventListener("change", (e) => {
    if (e.target.matches("[data-autosubmit]")) e.target.form?.requestSubmit();
    // Fayl tanlanishi bilan yuklash (savol rasmi).
    else if (e.target.matches("[data-autosubmit-file]") && e.target.files.length) e.target.form?.submit();
  });

  // --- Buyruqlar paneli (Ctrl+K, /) -----------------------------------------
  document.addEventListener("keydown", (e) => {
    const palette = $("#palette");
    if (!palette?._open) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      palette.open ? palette._close() : palette._open();
    } else if (e.key === "/" && !e.ctrlKey && !e.metaKey && !e.altKey && !typing(document.activeElement)) {
      e.preventDefault();
      palette._open();
    }
  });

  // --- Yo'qlama: "hammasi keldi" va 1–4 tugmalari ---------------------------
  const attendanceChanged = (form) => form.dispatchEvent(new Event("change", { bubbles: true }));
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-mark-all]");
    const form = $("[data-attendance-form]");
    if (!btn || !form) return;
    $$(`input[type="radio"][value="${CSS.escape(btn.dataset.markAll)}"]`, form).forEach((el) => (el.checked = true));
    attendanceChanged(form);
  });
  // 1–4: fokusdagi qatorda N-chi holatni tanlaydi (ekrandagi raqam bilan bir xil)
  // va keyingi shogirdga o'tadi.
  document.addEventListener("keydown", (e) => {
    const form = e.target.closest?.("[data-attendance-form]");
    const row = e.target.closest?.(".att-row");
    if (!form || !row || !/^[1-9]$/.test(e.key)) return;
    if (e.target.matches('input[type="number"], input[type="text"], input:not([type])')) return;
    const radio = $$('input[type="radio"]', row)[Number(e.key) - 1];
    if (!radio) return;
    e.preventDefault();
    radio.checked = true;
    attendanceChanged(form);
    const rows = $$(".att-row", form);
    const next = rows[rows.indexOf(row) + 1];
    $('input[type="radio"]:checked', next || row)?.focus();
  });

  // --- Test jo'natish: shogirdlarni belgilash, tez tanlash ------------------
  const updateCheckCount = (name) => {
    const boxes = $$(`input[type="checkbox"][name="${name}"]`);
    const counter = $(`[data-check-count="${name}"]`);
    if (counter) {
      const n = boxes.filter((b) => b.checked).length;
      counter.innerHTML = `<span class="badge ${n ? "ok" : "bad"}">${t("{n} / {total} tanlandi", { n, total: boxes.length })}</span>`;
    }
  };
  document.addEventListener("change", (e) => {
    if (e.target.matches('input[type="checkbox"]')) updateCheckCount(e.target.name);
  });
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-check-all]");
    if (!btn) return;
    const name = btn.dataset.checkAll;
    const mode = btn.dataset.checkValue;
    $$(`input[type="checkbox"][name="${name}"]`).forEach((b) => {
      b.checked = mode === "all" || (mode === "came" && b.hasAttribute("data-came"));
    });
    updateCheckCount(name);
  });
  // Test jo'natish: hamma o'quvchiga bir xil til (UZ / RU).
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-lang-all]");
    if (!btn) return;
    $$(`input[type="radio"][name^="lang_"][value="${btn.dataset.langAll}"]`).forEach((r) => {
      r.checked = true;
    });
  });
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-preset]");
    if (!btn) return;
    const input = document.getElementById(btn.dataset.preset);
    input.value = btn.dataset.value;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  });

  // --- Saqlanmagan o'zgarishlar haqida ogohlantirish -------------------------
  // Turbo bilan sahifadan chiqish "beforeunload"siz bo'ladi — turbo:before-visit ham tekshiriladi.
  const dirtyForm = () => $("form[data-dirty-guard][data-dirty]");
  const markDirty = (e) => {
    const form = e.target.closest?.("form[data-dirty-guard]");
    if (form) form.dataset.dirty = "1";
  };
  document.addEventListener("input", markDirty);
  document.addEventListener("change", markDirty);
  document.addEventListener("submit", (e) => {
    // Forma boshqa joydagi tugma bilan ham yuborilishi mumkin (form="..." atributi).
    if (e.target.matches?.("form")) delete e.target.dataset.dirty;
  });
  window.addEventListener("beforeunload", (e) => {
    if (dirtyForm()) e.preventDefault();
  });
  document.addEventListener("turbo:before-visit", (e) => {
    if (dirtyForm() && !window.confirm(t("Saqlanmagan o‘zgarishlar bor. Sahifadan chiqilsinmi?"))) {
      e.preventDefault();
    }
  });

  // Turbo keshiga sahifa "toza" holda tushsin: orqaga qaytilganda toast, ochiq menyu va
  // buyruqlar paneli qayta ko'rinmasin.
  document.addEventListener("turbo:before-cache", () => {
    $$("[data-toast]").forEach((t) => t.remove());
    setNav(false);
    const palette = $("#palette");
    if (palette?.open) palette.close();
  });

  // ==========================================================================
  // Har bir sahifada: elementga bog'liq sozlash
  // ==========================================================================

  const initPalette = (palette) => {
    if (!palette || palette._open || typeof palette.showModal !== "function") return;
    const input = $("[data-palette-input]", palette);
    const list = $("[data-palette-list]", palette);
    const commands = JSON.parse($("#palette-commands")?.textContent || "[]");
    const kindIcon = { student: "user", group: "layers", topic: "book", lesson: "lesson" };
    const kindLabel = { student: t("Shogirdlar"), group: t("Guruhlar"), topic: t("Mavzular"), lesson: t("Darslar") };
    let items = [];
    let active = 0;
    let timer = null;
    let controller = null;

    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
    const icon = (name) =>
      `<svg class="i" width="16" height="16" aria-hidden="true"><use href="#i-${name}"></use></svg>`;

    const render = (groups) => {
      items = [];
      let html = "";
      for (const [label, rows] of groups) {
        if (!rows.length) continue;
        html += `<li class="palette-group" role="presentation">${esc(label)}</li>`;
        for (const row of rows) {
          const i = items.push(row) - 1;
          html +=
            `<li class="palette-item" role="option" id="pi-${i}" aria-selected="${i === active}">` +
            `<a href="${esc(row.url)}" tabindex="-1"${row.download ? ' data-turbo="false"' : ""}>` +
            `<span class="pi-icon">${icon(row.icon)}</span>` +
            `<span class="truncate">${esc(row.title)}</span>` +
            `<span class="pi-meta">${esc(row.meta || "")}</span></a></li>`;
        }
      }
      list.innerHTML = html || `<li class="palette-empty">${esc(t("Hech narsa topilmadi"))}</li>`;
      input.setAttribute("aria-activedescendant", items.length ? `pi-${active}` : "");
    };

    const select = (i) => {
      if (!items.length) return;
      active = (i + items.length) % items.length;
      $$(".palette-item", list).forEach((el, n) => el.setAttribute("aria-selected", String(n === active)));
      $(`#pi-${active}`, list)?.scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", `pi-${active}`);
    };

    const localMatches = (q) =>
      commands.filter((c) => c.title.toLowerCase().includes(q.toLowerCase()));

    const search = (q) => {
      active = 0;
      if (!q) return render([[t("Tezkor o‘tish"), commands]]);
      render([[t("Buyruqlar"), localMatches(q)]]);
      clearTimeout(timer);
      timer = setTimeout(async () => {
        controller?.abort();
        controller = new AbortController();
        try {
          const url = `${palette.dataset.searchUrl}?format=json&q=${encodeURIComponent(q)}`;
          const res = await fetch(url, { signal: controller.signal, headers: { Accept: "application/json" } });
          if (!res.ok) return;
          const data = await res.json();
          if (input.value.trim() !== q) return;
          const byKind = {};
          for (const r of data.results) (byKind[r.kind] ||= []).push({ ...r, icon: kindIcon[r.kind] });
          render([
            ...Object.keys(kindLabel).map((k) => [kindLabel[k], byKind[k] || []]),
            [t("Buyruqlar"), localMatches(q)],
          ]);
        } catch (err) {
          if (err.name !== "AbortError") console.warn(err);
        }
      }, 140);
    };

    const close = () => palette.open && palette.close();
    palette._open = () => {
      if (palette.open) return;
      setNav(false);
      palette.showModal();
      input.value = "";
      search("");
      input.focus();
    };
    palette._close = close;

    $$("[data-palette-open]").forEach((el) => el.addEventListener("click", palette._open));
    input.addEventListener("input", () => search(input.value.trim()));
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); select(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); select(active - 1); }
      else if (e.key === "Enter" && items[active]) {
        e.preventDefault();
        close();
        // Fayl yuklab olish Turbo orqali emas — oddiy so'rov bilan.
        items[active].download ? (window.location.href = items[active].url) : visit(items[active].url);
      }
    });
    list.addEventListener("mousemove", (e) => {
      const li = e.target.closest(".palette-item");
      if (li) select($$(".palette-item", list).indexOf(li));
    });
    list.addEventListener("click", (e) => { if (e.target.closest("a")) close(); });
    palette.addEventListener("click", (e) => { if (e.target === palette) close(); });
  };

  const initAttendanceCounter = () => {
    const form = $("[data-attendance-form]");
    const counter = $("[data-attendance-count]");
    if (!form || !counter) return;
    const labels = {
      present: [t("keldi"), "ok"],
      late: [t("kechikdi"), "warn"],
      absent: [t("kelmadi"), "bad"],
      excused: [t("sababli"), "info"],
    };
    const render = () => {
      const counts = {};
      $$('input[type="radio"]:checked', form).forEach((el) => (counts[el.value] = (counts[el.value] || 0) + 1));
      counter.innerHTML = Object.keys(labels)
        .filter((k) => counts[k])
        .map((k) => `<span class="badge ${labels[k][1]}">${counts[k]} ${labels[k][0]}</span>`)
        .join("");
    };
    form.addEventListener("change", render);
    render();
  };

  // Ro'yxatni matn bo'yicha filtrlash: [data-filter-input="x"] → [data-filter-item="x"]
  const initFilters = () => {
    $$("[data-filter-input]").forEach((input) => {
      const scope = input.dataset.filterInput;
      const items = $$(`[data-filter-item="${scope}"]`);
      const empty = $(`[data-filter-empty="${scope}"]`);
      input.addEventListener("input", () => {
        const q = input.value.trim().toLowerCase();
        let shown = 0;
        items.forEach((el) => {
          const hit = !q || el.dataset.filterText.includes(q);
          el.hidden = !hit;
          shown += hit;
        });
        // Bo'limda birorta ham mos mavzu qolmasa — bo'limni ham yashiramiz.
        $$("[data-filter-section]").forEach((sec) => {
          sec.hidden = !$$(`[data-filter-item="${scope}"]`, sec).some((el) => !el.hidden);
        });
        if (empty) empty.hidden = shown > 0;
      });
    });
  };

  const renderPresets = (input) => {
    $$(`[data-preset="${input.id}"]`).forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.value === input.value))
    );
  };
  const initQuizPace = () => {
    $$("[data-quiz-pace]").forEach((pace) => {
      const count = document.getElementById(pace.dataset.count);
      const time = document.getElementById(pace.dataset.time);
      const render = () => {
        [count, time].forEach(renderPresets);
        const n = Number(count.value);
        const m = Number(time.value);
        if (!(n > 0 && m > 0)) {
          pace.textContent = "";
          return;
        }
        const sec = Math.round((m * 60) / n);
        const min = t("daq.");
        const s = t("s");
        const label = sec >= 60 ? `${Math.floor(sec / 60)} ${min} ${sec % 60 ? `${sec % 60} ${s}` : ""}` : `${sec} ${s}`;
        pace.textContent = t("Har bir savolga ≈ {label}.", { label: label.trim() }) + (sec < 30 ? ` ${t("Vaqt juda kam bo‘lishi mumkin.")}` : "");
        pace.classList.toggle("warn", sec < 30);
      };
      [count, time].forEach((el) => el.addEventListener("input", render));
      render();
    });
  };

  // Jonli natijalar: [data-autorefresh="20"] bo'lsa sahifa N soniyada qayta yuklanadi (Turbo
  // "morph" — aylantirish joyi saqlanadi). Foydalanuvchi yozayotgan, menyu/panel ochiq yoki
  // sahifa ko'rinmayotgan bo'lsa — kutiladi.
  let refreshTimer = null;
  const initAutoRefresh = () => {
    clearTimeout(refreshTimer);
    const el = $("[data-autorefresh]");
    if (!el) return;
    const seconds = Math.max(5, Number(el.dataset.autorefresh) || 30);
    const tick = () => {
      const busy =
        document.hidden || typing(document.activeElement) || dirtyForm() || $("#palette")?.open ||
        document.body.classList.contains("nav-open") || $("details[open]") !== null;
      if (busy) {
        refreshTimer = setTimeout(tick, 5000);
        return;
      }
      window.Turbo ? window.Turbo.visit(window.location.href, { action: "replace" }) : window.location.reload();
    };
    refreshTimer = setTimeout(tick, seconds * 1000);
  };
  document.addEventListener("turbo:before-visit", () => clearTimeout(refreshTimer));

  const init = () => {
    $$("[data-mod-key]").forEach((el) => (el.textContent = isMac ? "⌘" : "Ctrl"));
    renderTheme();
    setNav(false);
    $$("[data-toast]").forEach((toast, i) => {
      const keep = toast.classList.contains("error") || toast.classList.contains("warning");
      if (!keep) setTimeout(() => dismiss(toast), 4500 + i * 600);
    });
    initPalette($("#palette"));
    initAttendanceCounter();
    initFilters();
    $$("[data-check-count]").forEach((el) => updateCheckCount(el.dataset.checkCount));
    initQuizPace();
    initAutoRefresh();
    // Kalendar: bugungi kunga avtomatik aylantirish (mobil)
    const today = $(".tt-col.today");
    if (today) today.closest(".table-wrap")?.scrollTo({ left: Math.max(0, today.offsetLeft - 70) });
  };

  // Turbo bor sahifalarda turbo:load har bir ko'rinishda (birinchisida ham) keladi.
  if (window.Turbo) document.addEventListener("turbo:load", init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
