// "Olish" kabi tugmalar: data-confirm bo'lsa — tasdiqlash so'raladi.
document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-confirm]");
  if (btn && !window.confirm(btn.dataset.confirm)) e.preventDefault();
});

// O'quvchi profili: mustahkamlash teskari sanog'i.
// <span data-countdown="SONIYA">…</span> — 0 ga yetganda sahifa yangilanadi (tugma ochiladi).
// Vaqt server tomonida ham tekshiriladi; bu faqat qulaylik.
(() => {
  "use strict";
  const items = [...document.querySelectorAll("[data-countdown]")];
  if (!items.length) return;
  const started = Date.now();
  const fmt = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  const tick = () => {
    const passed = Math.floor((Date.now() - started) / 1000);
    let done = false;
    for (const el of items) {
      const left = Math.max(0, Number(el.dataset.countdown) - passed);
      el.textContent = fmt(left);
      if (left === 0) done = true;
    }
    if (done) {
      window.location.reload();
      return;
    }
    window.setTimeout(tick, 1000);
  };
  tick();
})();

// O'quvchi profili: bo'limlar (tab). JS'siz hamma bo'lim ketma-ket ko'rinadi.
// Manzildagi #hash (masalan #coins, #a12, #t5) qaysi bo'limda bo'lsa — o'sha ochiladi.
(() => {
  "use strict";
  const nav = document.querySelector("[data-tabs]");
  if (!nav) return;
  const tabs = [...nav.querySelectorAll('[role="tab"]')];
  const panels = tabs.map((t) => document.getElementById(t.getAttribute("aria-controls")));
  const show = (i, focus = false) => {
    tabs.forEach((t, n) => {
      const on = n === i;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      panels[n].hidden = !on;
    });
    if (focus) tabs[i].focus();
    try { sessionStorage.setItem("portal-tab", panels[i].id); } catch { /* private rejim */ }
  };
  const fromHash = () => {
    const id = decodeURIComponent(window.location.hash.slice(1));
    const target = id && document.getElementById(id);
    const i = target ? panels.findIndex((p) => p === target || p.contains(target)) : -1;
    if (i < 0) return false;
    show(i);
    if (target !== panels[i]) target.scrollIntoView({ block: "start" });
    return true;
  };
  nav.hidden = false;
  tabs.forEach((t, n) => {
    t.id = `${panels[n].id}-tab`;
    panels[n].setAttribute("aria-labelledby", t.id);
  });
  let saved = null;
  try { saved = sessionStorage.getItem("portal-tab"); } catch { /* private rejim */ }
  if (!fromHash()) show(Math.max(0, panels.findIndex((p) => p.id === saved)));
  nav.addEventListener("click", (e) => {
    const tab = e.target.closest('[role="tab"]');
    if (tab) show(tabs.indexOf(tab));
  });
  nav.addEventListener("keydown", (e) => {
    const i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
    if (step) {
      e.preventDefault();
      show((i + step + tabs.length) % tabs.length, true);
    } else if (e.key === "Home" || e.key === "End") {
      e.preventDefault();
      show(e.key === "Home" ? 0 : tabs.length - 1, true);
    }
  });
  window.addEventListener("hashchange", fromHash);
  // Yuqori blokdagi "Coinlaringiz" kabi havolalar — tegishli bo'limni ochib, unga aylantiradi.
  document.addEventListener("click", (e) => {
    const link = e.target.closest("[data-tab-link]");
    if (!link) return;
    e.preventDefault();
    window.history.replaceState(null, "", link.getAttribute("href"));
    fromHash();
    nav.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
