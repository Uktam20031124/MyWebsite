document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-mark-all]");
  if (!btn) return;
  const value = btn.getAttribute("data-mark-all");
  document.querySelectorAll(`input[type="radio"][value="${value}"]`).forEach((el) => {
    el.checked = true;
  });
});
