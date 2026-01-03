from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import BadRequest, Forbidden
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

API_URL_PREDICT = "http://127.0.0.1:8000/api/v1/predict"
API_URL_PREDICT_LINK = "http://127.0.0.1:8000/api/v1/extract?url={}"


# ------------------- API CALLS -------------------
async def fn_api(payload: dict):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(API_URL_PREDICT, json=payload) as response:
            if response.status != 200:
                return {"error": f"predict api error {response.status}"}
            return await response.json()


async def call_extract(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_PREDICT_LINK.format(url)) as response:
            if response.status != 200:
                return {"error": f"extract api error {response.status}"}
            return await response.json()


# ----------------- COMMANDS -------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id  # safer than update.message.chat.id
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Hello! Send me text or a link and I'll check if it's fake news."
        )
    except (BadRequest, Forbidden) as e:
        print(f"Failed to send /start message: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "Just send text or a link and I'll check if it's real or fake."
        )
    except (BadRequest, Forbidden) as e:
        print(f"Failed to send /help message: {e}")


# ----------------- MESSAGE HANDLER -------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    try:
        # LINK INPUT
        if text.startswith("http"):
            extract_response = await call_extract(text)
            if "error" in extract_response:
                await update.message.reply_text(f"API ERROR: {extract_response['error']}")
                return
            user_input = f"{extract_response['original'].get('title','')}\n{extract_response['original'].get('body','')}"
            payload = {"text": user_input}
        else:
            payload = {"text": text}

        # CALL PREDICTION API
        data = await fn_api(payload)
        if "error" in data:
            await update.message.reply_text(f"API ERROR: {data['error']}")
            return

        prediction_class = data.get("prediction_class", "unknown").lower()
        if prediction_class == "real":
            confidence = round(data.get("real_percentage", 0), 2)
            msg = f"✅ REAL\nConfidence: {confidence}%"
        elif prediction_class == "fake":
            confidence = round(data.get("fake_percentage", 0), 2)
            msg = f"⚠️ FAKE\nConfidence: {confidence}%"
        else:
            msg = "🤔 Unable to classify this content."

        await update.message.reply_text(msg)

    except (BadRequest, Forbidden) as e:
        print(f"Failed to send message: {e}")
    except Exception as e:
        await update.message.reply_text(f"Internal error:\n{str(e)}")


# ----------------- ERROR HANDLER -------------------
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# ------------------- SETUP BOT -------------------
def setup_webhook_bot():
    """Return an ApplicationBuilder app object for webhook mode."""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)
    return app
