from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_BOT_USERNAME = "@fakenewz_detector_bot"

API_URL_PREDICT = "http://127.0.0.1:8000/api/v1/predict"
API_URL_PREDICT_LINK = "http://127.0.0.1:8000/api/v1/extract?url={}"


# ----------------- FUNCTIONS -------------------
async def fn_api(payload: dict):
    async with aiohttp.ClientSession() as session:
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
    await update.message.reply_text(
        "Hello! Send me text or a link and Ill check if its fake news."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just send text or a link and ill check if its real or fake."
    )


# ----------------- MESSAGE HANDLER -------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message_type = update.message.chat.type
    text = update.message.text.strip()

    try:
        # INPUT IF LINK
        if text.startswith("http"):
            extract_response = await call_extract(text)
            if "error" in extract_response:
                await update.message.reply_text(
                    f"API ERROR: {extract_response['error']}"
                )
                return
            user_input = f"{extract_response['original'].get('title','')}\n{extract_response['original'].get('body','')}"
            payload = {"text": user_input}
        else:
            payload = {"text": text}

        # CALL API
        data = await fn_api(payload)
        if "error" in data:
            await update.message.reply_text(f"API ERROR: {data['error']}")
            return

        prediction_class = data.get("prediction_class", "Unknown")
        confidence = (
            data.get("real_percentage", 0)
            if prediction_class.lower() == "real"
            else data.get("fake_percentage", 0)
        )
        confidence = round(confidence, 2)


        #PREDCTION
        if prediction_class.lower() == "real":
            msg = f"✅ REAL: {confidence}% confidence"
        elif prediction_class.lower() == "fake":
            msg = f"⚠️ FAKE: {confidence}% confidence"
        else:
            msg = "I "

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


# ----------------- ERROR HANDLER -------------------
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# ----------------- RUNNER -------------------
async def run_telegram_bot():
    print("Starting Telegram bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

