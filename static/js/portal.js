// O'quvchi profili: mustahkamlash / tayyorlanish teskari sanog'i.
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
