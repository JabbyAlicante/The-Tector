import { setScanMode } from "./scanState.js";

export function setupSidebarMode() {
  const buttons = document.querySelectorAll(".sidebar button");
  const textarea = document.getElementById("detectorInput");
  const linkInput = document.getElementById("linkInput");
  const scanBtn = document.getElementById("detectBtn");
  const resultBox = document.getElementById("resultBox");
  const integrationSection = document.querySelector(".icons-integration");
  const badwordsInstructions = document.getElementById("badwordsInstructions");

  if (!textarea || !linkInput || !scanBtn || !resultBox || !integrationSection || !badwordsInstructions) return;

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;
      setScanMode(mode);

      textarea.style.display = "none";
      linkInput.style.display = "none";
      scanBtn.style.display = "none";
      resultBox.style.display = "none";
      integrationSection.style.display = "none";
      badwordsInstructions.style.display = "none";

      if (mode === "spam") {
        textarea.style.display = "flex";
        scanBtn.style.display = "flex";
        resultBox.style.display = "flex";
        integrationSection.style.display = "flex";
        textarea.placeholder = "Paste text here...";

      } else if (mode === "fake") {
        textarea.style.display = "flex";
        linkInput.style.display = "flex";
        scanBtn.style.display = "flex";
        resultBox.style.display = "flex";
        integrationSection.style.display = "flex";
        textarea.placeholder = "Input text article...";

      } else if (mode === "badwords") {
        badwordsInstructions.style.display = "block";
        integrationSection.style.display = "flex";
      }

      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
    });
  });
}
