import { setScanMode } from "./scanState.js";

export function setupSidebarMode() {
  const buttons = document.querySelectorAll(".sidebar button");
  const textarea = document.getElementById("detectorInput");

  if (!textarea) return;

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;
      setScanMode(mode);

      if (mode === "spam") {
        textarea.placeholder = "Paste text here...";
      } else if (mode === "fake") {
        textarea.placeholder = "Paste text or link here...";
      }

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
    });
  }
  );
}
