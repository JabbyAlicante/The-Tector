import { getScanMode } from "./scanState.js";

export function setupScanHandler() {
  const btn = document.getElementById("detectBtn");
  const input = document.getElementById("detectorInput");
  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");

  btn.addEventListener("click", () => {
    const mode = getScanMode();
    const value = input.value.trim();

    if (!value) {
      alert("Input is empty");
      return;
    }

    resultBox.hidden = false;

    if (mode === "spam") {
      resultText.textContent = "Scanning message for spam...";
    } else {
      resultText.textContent = "Scanning content for fake news...";
    }
  });
}
