import { setScanMode } from "./scanState.js";

export function setupSidebarMode() {
  const buttons = document.querySelectorAll(".sidebar button");
  const textarea = document.getElementById("detectorInput");
  const linkInput = document.getElementById("linkInput");

  if (!textarea || !linkInput) return;

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;
      setScanMode(mode);

      if (mode === "spam") {
        textarea.placeholder = "Paste text here...";
        linkInput.hidden = true;
      }

      if (mode === "fake") {
        textarea.placeholder = "Input text article...";
        linkInput.hidden = false;
      }

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });
}
