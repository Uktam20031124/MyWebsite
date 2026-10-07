// Darsxona — progressive enhancement. Barcha sahifalar JS'siz ham to'liq ishlaydi.
(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const isMac = /Mac|iPhone|iPad/.test(navigator.platform);
  const typing = (el) =>
    el && (["INPUT", "TEXTAREA", "SELECT"].includes(el.tagName) || el.isContentEditable);

  const store = {
    get(key) {
      try { return localStorage.getItem(key); } catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(key, value); } catch { /* private rejim */ }
    },
  };

  $$("[data-mod-key]").forEach((el) => (el.textContent = isMac ? "⌘" : "Ctrl"));

  // --- Mavzu: kunduzgi / tungi -------------------------------------------
  const root = document.documentElement;
  const renderTheme = () => {
    const dark = root.dataset.theme === "dark";
    $$("[data-theme-icon]").forEach((el) => (el.hidden = el.dataset.themeIcon !== (dark ? "dark" : "light")));
    $$("[data-theme-label]").forEach((el) => (el.textContent = dark ? "Kunduzgi rejim" : "Tungi rejim"));
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
  renderTheme();

  // --- Mobil menyu ---------------------------------------------------------
  const navToggle = $("[data-nav-toggle]");
  const setNav = (open) => {
    document.body.classList.toggle("nav-open", open);
    navToggle?.setAttribute("aria-expanded", String(open));
  };
  navToggle?.addEventListener("click", () => setNav(!document.body.classList.contains("nav-open")));
  $("[data-nav-close]")?.addEventListener("click", () => setNav(false));

  // --- Toast xabarlar --------------------------------------------------------
  const dismiss = (toast) => {
    if (!toast || toast.classList.contains("leaving")) return;
    toast.classList.add("leaving");
    toast.addEventListener("animationend", () => toast.remove(), { once: true });
    setTimeout(() => toast.remove(), 400);
  };
  $$("[data-toast]").forEach((toast, i) => {
    const keep = toast.classList.contains("error") || toast.classList.contains("warning");
    if (!keep) setTimeout(() => dismiss(toast), 4500 + i * 600);
  });
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-toast-close]");
    if (btn) dismiss(btn.closest("[data-toast]"));
  });

  // --- Xavfli amallar uchun tasdiq: <button data-confirm="..."> ------------
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-confirm]");
    if (el && !window.confirm(el.getAttribute("data-confirm"))) e.preventDefault();
  });

  // Nusxa olish: <button data-copy="matn">
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-copy]");
    if (!btn) return;
    const text = btn.getAttribute("data-copy");
    const done = () => {
      const label = btn.textContent;
      btn.textContent = "Nusxalandi ✓";
      setTimeout(() => (btn.textContent = label), 1500);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, () => window.prompt("Nusxa oling:", text));
    } else {
      window.prompt("Nusxa oling:", text);
    }
  });

  // --- Filtr o'zgarganda formani yuborish ----------------------------------
  document.addEventListener("change", (e) => {
    if (e.target.matches("[data-autosubmit]")) e.target.form?.requestSubmit();
  });

  // --- Buyruqlar paneli (Ctrl+K, /) -----------------------------------------
  const palette = $("#palette");
  if (palette && typeof palette.showModal === "function") {
    const input = $("[data-palette-input]", palette);
    const list = $("[data-palette-list]", palette);
    const commands = JSON.parse($("#palette-commands")?.textContent || "[]");
    const kindIcon = { student: "user", group: "layers", topic: "book", lesson: "lesson" };
    const kindLabel = { student: "Shogirdlar", group: "Guruhlar", topic: "Mavzular", lesson: "Darslar" };
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
            `<a href="${esc(row.url)}" tabindex="-1"><span class="pi-icon">${icon(row.icon)}</span>` +
            `<span class="truncate">${esc(row.title)}</span>` +
            `<span class="pi-meta">${esc(row.meta || "")}</span></a></li>`;
        }
      }
      list.innerHTML = html || `<li class="palette-empty">Hech narsa topilmadi</li>`;
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
      if (!q) return render([["Tezkor o‘tish", commands]]);
      render([["Buyruqlar", localMatches(q)]]);
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
            ["Buyruqlar", localMatches(q)],
          ]);
        } catch (err) {
          if (err.name !== "AbortError") console.warn(err);
        }
      }, 140);
    };

    const open = () => {
      if (palette.open) return;
      setNav(false);
      palette.showModal();
      input.value = "";
      search("");
      input.focus();
    };
    const close = () => palette.open && palette.close();

    $$("[data-palette-open]").forEach((el) => el.addEventListener("click", open));
    input.addEventListener("input", () => search(input.value.trim()));
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); select(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); select(active - 1); }
      else if (e.key === "Enter" && items[active]) { e.preventDefault(); window.location.href = items[active].url; }
    });
    list.addEventListener("mousemove", (e) => {
      const li = e.target.closest(".palette-item");
      if (li) select($$(".palette-item", list).indexOf(li));
    });
    palette.addEventListener("click", (e) => { if (e.target === palette) close(); });

    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        palette.open ? close() : open();
      } else if (e.key === "/" && !e.ctrlKey && !e.metaKey && !e.altKey && !typing(document.activeElement)) {
        e.preventDefault();
        open();
      }
    });
  }

  // --- Yo'qlama -------------------------------------------------------------
  const attForm = $("[data-attendance-form]");
  if (attForm) {
    const counter = $("[data-attendance-count]");
    const labels = { present: ["keldi", "ok"], late: ["kechikdi", "warn"], absent: ["kelmadi", "bad"], excused: ["sababli", "info"] };

    const render = () => {
      if (!counter) return;
      const counts = {};
      $$('input[type="radio"]:checked', attForm).forEach((el) => (counts[el.value] = (counts[el.value] || 0) + 1));
      counter.innerHTML = Object.keys(labels)
        .filter((k) => counts[k])
        .map((k) => `<span class="badge ${labels[k][1]}">${counts[k]} ${labels[k][0]}</span>`)
        .join("");
    };
    attForm.addEventListener("change", render);
    render();

    document.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-mark-all]");
      if (!btn) return;
      $$(`input[type="radio"][value="${CSS.escape(btn.dataset.markAll)}"]`, attForm).forEach((el) => (el.checked = true));
      attForm.dispatchEvent(new Event("change", { bubbles: true }));
    });

    // 1–4 tugmalari: fokusdagi qatorda N-chi holatni tanlaydi (ekrandagi raqam bilan bir xil)
    // va keyingi shogirdga o'tadi.
    attForm.addEventListener("keydown", (e) => {
      const row = e.target.closest(".att-row");
      if (!/^[1-9]$/.test(e.key) || !row || e.target.matches('input[type="number"], input[type="text"], input:not([type])')) return;
      const radio = $$('input[type="radio"]', row)[Number(e.key) - 1];
      if (!radio) return;
      e.preventDefault();
      radio.checked = true;
      attForm.dispatchEvent(new Event("change", { bubbles: true }));
      const rows = $$(".att-row", attForm);
      const next = rows[rows.indexOf(row) + 1];
      $('input[type="radio"]:checked', next || row)?.focus();
    });
  }

  // --- Ro'yxatni matn bo'yicha filtrlash: [data-filter-input="x"] → [data-filter-item="x"] --
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

  // --- Test jo'natish: shogirdlarni belgilash, tez tanlash, vaqt maslahati ----
  const updateCheckCount = (name) => {
    const boxes = $$(`input[type="checkbox"][name="${name}"]`);
    const counter = $(`[data-check-count="${name}"]`);
    if (counter) {
      const n = boxes.filter((b) => b.checked).length;
      counter.innerHTML = `<span class="badge ${n ? "ok" : "bad"}">${n} / ${boxes.length} tanlandi</span>`;
    }
  };
  $$("[data-check-count]").forEach((el) => updateCheckCount(el.dataset.checkCount));
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

  const renderPresets = (input) => {
    $$(`[data-preset="${input.id}"]`).forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.value === input.value))
    );
  };
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-preset]");
    if (!btn) return;
    const input = document.getElementById(btn.dataset.preset);
    input.value = btn.dataset.value;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  });

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
      const label = sec >= 60 ? `${Math.floor(sec / 60)} daq. ${sec % 60 ? `${sec % 60} s` : ""}` : `${sec} s`;
      pace.textContent = `Har bir savolga ≈ ${label.trim()}.` + (sec < 30 ? " Vaqt juda kam bo‘lishi mumkin." : "");
      pace.classList.toggle("warn", sec < 30);
    };
    [count, time].forEach((el) => el.addEventListener("input", render));
    render();
  });

  // --- Saqlanmagan o'zgarishlar haqida ogohlantirish -------------------------
  $$("[data-dirty-guard]").forEach((form) => {
    let dirty = false;
    const mark = () => (dirty = true);
    form.addEventListener("change", mark);
    form.addEventListener("input", mark);
    form.addEventListener("submit", () => (dirty = false));
    window.addEventListener("beforeunload", (e) => {
      if (dirty) e.preventDefault();
    });
  });

  // --- Kalendar: bugungi kunga avtomatik aylantirish (mobil) -----------------
  const today = $(".tt-col.today");
  if (today) today.closest(".table-wrap")?.scrollTo({ left: Math.max(0, today.offsetLeft - 70) });
})();
