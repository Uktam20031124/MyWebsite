/* Dars taqdimoti: ← → / Space / PageUp-Down / Home-End, F — to'liq ekran, Esc — chiqish,
   barmoq bilan surish, URL'da #5 — 5-slayd. Taymer: ▶/⏸, ↺; tugaganda ovozli signal. */
(function () {
  "use strict";

  function init() {
    var deck = document.getElementById("deck");
    if (!deck || deck.dataset.ready) return;
    deck.dataset.ready = "1";

    var slides = Array.prototype.slice.call(deck.querySelectorAll(".slide"));
    var current = deck.querySelector("[data-current]");
    var progress = deck.querySelector("[data-progress]");
    var prevBtn = deck.querySelector("[data-prev]");
    var nextBtn = deck.querySelector("[data-next]");
    var labels = { start: deck.dataset.labelStart, pause: deck.dataset.labelPause, done: deck.dataset.labelDone };
    var index = -1;

    function fromHash() {
      var n = parseInt((location.hash || "").replace(/^#s?/, ""), 10);
      return n >= 1 && n <= slides.length ? n - 1 : 0;
    }

    function show(i, back) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      if (i === index) return;
      slides.forEach(function (s, k) {
        var on = k === i;
        s.hidden = !on;
        s.classList.toggle("is-active", on);
        s.classList.toggle("is-back", on && !!back);
      });
      index = i;
      current.textContent = i + 1;
      progress.style.width = ((i + 1) / slides.length) * 100 + "%";
      prevBtn.disabled = i === 0;
      nextBtn.disabled = i === slides.length - 1;
      if (history.replaceState) history.replaceState(null, "", "#" + (i + 1));
    }

    function go(step) { show(index + step, step < 0); }

    function toggleFullscreen() {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (deck.requestFullscreen) deck.requestFullscreen().catch(function () {});
    }

    document.addEventListener("fullscreenchange", function () {
      deck.classList.toggle("is-fullscreen", document.fullscreenElement === deck);
    });

    var uiTimer;
    deck.addEventListener("mousemove", function () {
      deck.classList.add("show-ui");
      clearTimeout(uiTimer);
      uiTimer = setTimeout(function () { deck.classList.remove("show-ui"); }, 1800);
    });

    document.addEventListener("keydown", function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.target.closest && e.target.closest("button, a") && (e.key === " " || e.key === "Enter")) return;
      switch (e.key) {
        case "ArrowRight": case "ArrowDown": case "PageDown": case " ":
          go(1); break;
        case "ArrowLeft": case "ArrowUp": case "PageUp": case "Backspace":
          go(-1); break;
        case "Home": show(0, true); break;
        case "End": show(slides.length - 1); break;
        case "f": case "F": toggleFullscreen(); break;
        case "t": case "T": {
          var btn = slides[index].querySelector("[data-timer-toggle]");
          if (btn) btn.click();
          break;
        }
        case "Escape":
          if (!document.fullscreenElement) location.href = deck.querySelector(".deck-brand").href;
          return;
        default: return;
      }
      e.preventDefault();
    });

    prevBtn.addEventListener("click", function () { go(-1); });
    nextBtn.addEventListener("click", function () { go(1); });
    deck.querySelector("[data-fullscreen]").addEventListener("click", toggleFullscreen);

    var touchX = null, touchY = null;
    deck.addEventListener("touchstart", function (e) { touchX = e.touches[0].clientX; touchY = e.touches[0].clientY; }, { passive: true });
    deck.addEventListener("touchend", function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX, dy = e.changedTouches[0].clientY - touchY;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1);
      touchX = null;
    });

    window.addEventListener("hashchange", function () { show(fromHash()); });

    deck.querySelectorAll(".timer").forEach(function (el) { setupTimer(el, labels); });

    show(fromHash());
    deck.focus({ preventScroll: true });
  }

  function beep() {
    try {
      var Ctx = window.AudioContext || window.webkitAudioContext;
      var ctx = new Ctx();
      [0, 0.35, 0.7].forEach(function (t) {
        var o = ctx.createOscillator(), g = ctx.createGain();
        o.frequency.value = 880;
        g.gain.setValueAtTime(0.0001, ctx.currentTime + t);
        g.gain.exponentialRampToValueAtTime(0.25, ctx.currentTime + t + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + t + 0.28);
        o.connect(g).connect(ctx.destination);
        o.start(ctx.currentTime + t);
        o.stop(ctx.currentTime + t + 0.3);
      });
    } catch (e) { /* ovoz bo'lmasa ham taymer ishlaydi */ }
  }

  function setupTimer(el, labels) {
    var total = parseInt(el.dataset.seconds, 10) * 60;
    var left = total, endAt = null, tick = null;
    var out = el.querySelector(".timer-time");
    var bar = el.querySelector(".bar");
    var toggle = el.querySelector("[data-timer-toggle]");

    function fmt(s) {
      var m = Math.floor(s / 60), r = s % 60;
      return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r;
    }
    function render() {
      out.textContent = fmt(left);
      bar.style.strokeDashoffset = String(100 - (left / total) * 100);
      el.classList.toggle("is-low", left > 0 && left <= 60);
      el.classList.toggle("is-done", left === 0);
      toggle.textContent = tick ? "⏸ " + labels.pause : "▶ " + labels.start;
      if (left === 0) toggle.textContent = "⏰ " + labels.done;
    }
    function stop() { clearInterval(tick); tick = null; }
    function step() {
      left = Math.max(0, Math.round((endAt - Date.now()) / 1000));
      if (left === 0) { stop(); beep(); }
      render();
    }

    toggle.addEventListener("click", function () {
      if (tick) { stop(); render(); return; }
      if (left === 0) left = total;
      endAt = Date.now() + left * 1000;
      tick = setInterval(step, 250);
      render();
    });
    el.querySelector("[data-timer-reset]").addEventListener("click", function () {
      stop(); left = total; render();
    });
    render();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
