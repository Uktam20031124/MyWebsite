// Darsxona — kichik progressive enhancement. Sahifalar JS'siz ham to'liq ishlaydi.
(() => {
  "use strict";

  // Yo'qlama: "Hammasi keldi / kelmadi"
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-mark-all]");
    if (!btn) return;
    const value = btn.getAttribute("data-mark-all");
    document
      .querySelectorAll(`input[type="radio"][value="${CSS.escape(value)}"]`)
      .forEach((el) => {
        el.checked = true;
        el.dispatchEvent(new Event("change", { bubbles: true }));
      });
  });

  // Xavfli amallar uchun tasdiq: <button data-confirm="...">
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-confirm]");
    if (el && !window.confirm(el.getAttribute("data-confirm"))) e.preventDefault();
  });

  // Filtr select/checkbox o'zgarganda formani yuborish
  document.addEventListener("change", (e) => {
    if (e.target.matches("[data-autosubmit]")) e.target.form?.requestSubmit();
  });

  // "/" — global qidiruvga fokus
  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
    const tag = document.activeElement?.tagName;
    if (["INPUT", "TEXTAREA", "SELECT"].includes(tag)) return;
    const input = document.querySelector('[data-hotkey="/"]');
    if (input) {
      e.preventDefault();
      input.focus();
      input.select();
    }
  });

  // Mobil menyu
  const toggle = document.querySelector("[data-nav-toggle]");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const sidebar = document.getElementById("sidebar");
      const open = sidebar.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Yo'qlama hisoblagichi
  const form = document.querySelector("[data-attendance-form]");
  const counter = document.querySelector("[data-attendance-count]");
  if (form && counter) {
    const labels = { present: "keldi", late: "kechikdi", absent: "kelmadi", excused: "sababli" };
    const render = () => {
      const counts = {};
      form.querySelectorAll('input[type="radio"]:checked').forEach((el) => {
        counts[el.value] = (counts[el.value] || 0) + 1;
      });
      counter.textContent = Object.keys(labels)
        .filter((k) => counts[k])
        .map((k) => `${counts[k]} ${labels[k]}`)
        .join(" · ");
    };
    form.addEventListener("change", render);
    render();
  }

  // Saqlanmagan o'zgarishlar haqida ogohlantirish
  document.querySelectorAll("[data-dirty-guard]").forEach((guarded) => {
    let dirty = false;
    guarded.addEventListener("change", () => (dirty = true));
    guarded.addEventListener("input", () => (dirty = true));
    guarded.addEventListener("submit", () => (dirty = false));
    window.addEventListener("beforeunload", (e) => {
      if (dirty) e.preventDefault();
    });
  });
})();
