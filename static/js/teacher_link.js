/* O'qituvchi Telegramini QR orqali ulash: holatni har 2 soniyada so'raydi, QR'ni yangilaydi,
   2 bosqichli parolni yuboradi va ulangach o'qituvchi sahifasiga o'tadi. */
(function () {
  "use strict";

  function init() {
    var root = document.querySelector("[data-tg-link]");
    if (!root || root.dataset.ready) return;
    root.dataset.ready = "1";

    var qrBox = root.querySelector("[data-tg-qr]");
    var passForm = root.querySelector("[data-tg-password]");
    var errBox = root.querySelector("[data-tg-error]");
    var errText = root.querySelector("[data-tg-error-text]");
    var restart = root.querySelector("[data-tg-restart]");
    var lastQr = qrBox.innerHTML;
    var timer = null;

    function render(s) {
      if (s.linked) {
        window.location.href = s.next;
        return true;
      }
      if (s.qr && s.qr !== lastQr) {
        qrBox.innerHTML = s.qr;
        lastQr = s.qr;
      }
      qrBox.hidden = s.status === "password" || s.status === "error";
      passForm.hidden = s.status !== "password";
      errBox.hidden = !s.error;
      errText.textContent = s.error || "";
      restart.hidden = s.status !== "error";
      return s.status === "error";
    }

    function poll() {
      fetch(root.dataset.statusUrl, { credentials: "same-origin", headers: { Accept: "application/json" } })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (s) {
          if (s && render(s)) return; // xato — foydalanuvchi "Yangi QR-kod"ni bosadi
          timer = setTimeout(poll, 2000);
        })
        .catch(function () { timer = setTimeout(poll, 4000); });
    }

    passForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(passForm);
      passForm.querySelector("button").disabled = true;
      fetch(root.dataset.passwordUrl, { method: "POST", body: data, credentials: "same-origin" })
        .finally(function () {
          passForm.reset();
          passForm.querySelector("button").disabled = false;
        });
    });

    document.addEventListener("turbo:before-visit", function () { clearTimeout(timer); }, { once: true });
    poll();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
  document.addEventListener("turbo:load", init);
})();
