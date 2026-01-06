# tg_fake_module.py
import aiohttp

API_URL_PREDICT = "http://127.0.0.1:8000/api/v1/predict"
API_URL_PREDICT_LINK = "http://127.0.0.1:8000/api/v1/extract?url={}"

async def run_fakeh_module(text: str):
    """
    Runs fake news detection on text or link.
    Returns a formatted result string.
    """

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        # If link → extract content first
        if text.startswith("http"):
            async with session.get(API_URL_PREDICT_LINK.format(text)) as r:
                extract = await r.json()

            if "error" in extract:
                return f"⚠️ Extract API error: {extract['error']}"

            content = (
                extract.get("original", {}).get("title", "") + "\n" +
                extract.get("original", {}).get("body", "")
            )
            payload = {"text": content}

        else:
            payload = {"text": text}

        # Predict
        async with session.post(API_URL_PREDICT, json=payload) as r:
            data = await r.json()

    if "error" in data:
        return f"⚠️ Predict API error: {data['error']}"

    prediction = data.get("prediction_class", "unknown")
    recommendations = data.get("recommendations", "None")
    
    if isinstance(recommendations, list) and recommendations:
      
        rec_text = "\n \n".join(f"✅ {r}" for r in recommendations[:3])  # top 3 links
    else:
        rec_text = f"💡 ALWAYS CHECK YOUR NEWS IN:\n✅ {recommendations}"
    confidence = (
        data.get("real_percentage", 0)
        if prediction.lower() == "real"
        else data.get("fake_percentage", 0)
    )

    confidence = round(confidence, 2)

    if prediction.lower() == "real":
        return f"✅ REAL news ({confidence}%)\n \n ============================================== \n 🟢VERIFIED, but it’s good to stay cautious, fact-check on this websites when possible\n \n {rec_text}"
    elif prediction.lower() == "fake":
        return f"⚠️FAKE news ({confidence}%)\n \n ============================================== \n📌 This info seems unreliable. Cross-check here:\n \n {rec_text}"
    else:
        return "⚠️ Unable to determine authenticity"
