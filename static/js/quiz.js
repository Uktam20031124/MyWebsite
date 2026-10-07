// Darsxona — test sahifasi: teskari sanoq, javoblarni oraliq saqlash, vaqt tugaganda avto-yakun.
// Vaqt server tomonida ham tekshiriladi; bu skript faqat qulaylik uchun.
(() => {
  "use strict";

  const form = document.querySelector("[data-quiz-form]");
  const timer = document.querySelector("[data-quiz-timer]");
  if (!form || !timer) return;

  const progress = document.querySelector("[data-quiz-progress]");
  const overlay = document.querySelector("[data-quiz-overlay]");
  const timeoutInput = form.querySelector("[data-quiz-timeout]");
  const total = form.querySelectorAll("fieldset").length;
  // Qurilma soati noto'g'ri bo'lishi mumkin — serverdan kelgan "qolgan soniya"dan hisoblaymiz.
  let endAt = Date.now() + Number(timer.dataset.seconds) * 1000;
  let submitted = false;

  const answered = () => form.querySelectorAll('input[type="radio"]:checked').length;

  const renderProgress = () => {
    if (progress) progress.textContent = `${answered()} / ${total} ta savolga javob berildi`;
  };

  const submit = (timedOut) => {
    if (submitted) return;
    submitted = true;
    if (timedOut) {
      timeoutInput.value = "1";
      if (overlay) overlay.hidden = false;
    }
    window.removeEventListener("beforeunload", guard);
    form.submit();
  };

  const tick = () => {
    const left = Math.max(0, Math.round((endAt - Date.now()) / 1000));
    const m = Math.floor(left / 60);
    const s = String(left % 60).padStart(2, "0");
    timer.textContent = `${m}:${s}`;
    timer.classList.toggle("warn", left <= 60 && left > 15);
    timer.classList.toggle("danger", left <= 15);
    if (left === 0) submit(true);
  };

  const save = () => {
    fetch(form.dataset.saveUrl, {
      method: "POST",
      body: new FormData(form),
      credentials: "same-origin",
      headers: { "X-Requested-With": "fetch" },
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        // Server soatiga moslash (masalan, telefon uyqu rejimidan chiqqanda).
        if (data && typeof data.seconds_left === "number") {
          endAt = Date.now() + data.seconds_left * 1000;
        }
      })
      .catch(() => {});
  };

  function guard(e) {
    if (!submitted) e.preventDefault();
  }

  form.addEventListener("change", () => {
    renderProgress();
    save();
  });

  form.addEventListener("submit", (e) => {
    const left = total - answered();
    if (left > 0 && !window.confirm(`${left} ta savolga javob berilmagan. Testni yakunlaysizmi?`)) {
      e.preventDefault();
      return;
    }
    submitted = true;
    window.removeEventListener("beforeunload", guard);
  });

  window.addEventListener("beforeunload", guard);
  renderProgress();
  tick();
  setInterval(tick, 250);
})();
