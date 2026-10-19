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

  // --- Test oynasidan chiqib ketishlar (boshqa tab, oyna yoki ilova) — ustozga ko'rinadi.
  const leavesInput = form.querySelector("[data-quiz-leaves]");
  const awayInput = form.querySelector("[data-quiz-away]");
  const leaveNotice = document.querySelector("[data-quiz-leave-notice]");
  let leaves = Number(leavesInput?.value || 0);
  let awayMs = Number(awayInput?.value || 0) * 1000;
  let awaySince = null;
  let ownDialog = false; // o'zimizning confirm() oynamiz chiqib ketish hisoblanmaydi

  const syncLeaveInputs = () => {
    if (leavesInput) leavesInput.value = String(leaves);
    if (awayInput) awayInput.value = String(Math.round(awayMs / 1000));
  };
  const leave = () => {
    if (awaySince !== null || submitted || ownDialog) return;
    awaySince = Date.now();
    leaves += 1;
    syncLeaveInputs();
    save();
  };
  const back = () => {
    if (awaySince === null) return;
    awayMs += Date.now() - awaySince;
    awaySince = null;
    syncLeaveInputs();
    if (leaveNotice) {
      leaveNotice.hidden = false;
      leaveNotice.querySelector("[data-count]").textContent = String(leaves);
    }
    save();
  };
  document.addEventListener("visibilitychange", () => (document.hidden ? leave() : back()));
  window.addEventListener("blur", leave);
  window.addEventListener("focus", back);

  const answered = () => form.querySelectorAll('input[type="radio"]:checked').length;

  const renderProgress = () => {
    if (progress) progress.textContent = (form.dataset.progressText || "{answered} / {total}").replace("{answered}", answered()).replace("{total}", total);
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
    ownDialog = true;
    const ok = left === 0 || window.confirm((form.dataset.confirmText || "{left}?").replace("{left}", left));
    ownDialog = false;
    if (!ok) {
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
