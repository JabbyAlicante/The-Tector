import { getScanMode } from "./scanState.js";

export function setupScanHandler() {
  const btn = document.getElementById("detectBtn");
  const input = document.getElementById("detectorInput");
  const resultBox = document.getElementById("resultBox");
  const resultText = document.getElementById("resultText");

  btn.addEventListener("click", async () => {
    const mode = getScanMode();
    const value = input.value.trim();

    if (!value) {
      alert("Input is empty");
      return;
    }

    resultBox.hidden = false;

    if (mode === "spam") {
      resultText.textContent = "Scanning message for spam...";

      try {
        const res = await fetch("http://localhost:5000/classify", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: value }),
        });
        const data = await res.json();

        const messages = {
          spam: " Alert!! This is a Spam",
          ham: "This message is Safe",
          unknown: " Unable to classify the message"
        };

        resultText.textContent = messages[data.prediction] || " Unknown result";

      } catch (err) {
        console.error(err);
        resultText.textContent = "Error connecting to spam classifier.";
      }

    } else {
      resultText.textContent = "Scanning content for fake news...";
    }
  });
}
