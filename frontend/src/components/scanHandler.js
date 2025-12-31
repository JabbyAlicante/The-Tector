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

    }
    else if (mode== "fake"){
      resultText.textContent = "Scanning content if FAKE NEWS...";

        console.log(value)


       try {
                const response = await fetch("/api/v1/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: value, link: value})
                });

                if (!response.ok) {
                    let errText;
                    try { errText = await response.text(); } catch { errText = response.statusText; }
                    throw new Error(`${response.status} ${errText}`);
                }

                const data = await response.json();


                // RESULT (prediction class lang and pecentage)
                console.log("DATA:", data)
                if (data.prediction_class) {
                    const predictionClass = data.prediction_class;
                    const isReyal = predictionClass.toLowerCase() === "real";
                    const percentage = isReyal ? data.real_percentage : data.fake_percentage;
                    // console.log("PERCENTAGE:", percentage)
                    const roundPercent = Math.round(percentage);
                    const resultClass = isReyal ? "real-news" : "fake-news";


                    resultText.textContent = `"${roundPercent}% ${resultClass}"`
                }



              }catch (error) {
                console.log("Error:", error);
               resultText.textContent = `Error: ${error.message}`;

            }}
      
    

     else {
      resultText.textContent = "Scanning content for HATE SPEECH...";
    }
  });
}

