from dotenv import load_dotenv
import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from spam_classifier import classify_message as classify
load_dotenv()

tg_bot_token = os.getenv('TG_BOT_TOKEN')
tg_bot_username = os.getenv('TG_BOT_USERNAME')
SPAM_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "spam_logs", "telegram_logs", "detected_spam.txt")
SPAM_LOG_FILE = os.path.abspath(SPAM_LOG_FILE)
os.makedirs(os.path.dirname(SPAM_LOG_FILE), exist_ok=True)


# AVOID DUPLICATEE
flagged_spam_ids = set()
if os.path.exists(SPAM_LOG_FILE):
    with open(SPAM_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ID:"):
                flagged_spam_ids.add(line.replace("ID:", "").strip())

#for saving spam logss
def save_spam(update: Update):
    message_id = str(update.message.message_id)
    if message_id in flagged_spam_ids:
        return

    flagged_spam_ids.add(message_id)
    with open(SPAM_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"ID: {message_id}\n")
        f.write(f"Author: {update.message.from_user.username or update.message.from_user.full_name} "
                f"(ID: {update.message.from_user.id})\n")
        f.write(f"Message: {update.message.text}\n")
        f.write("----------------------------------------\n\n")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    
    text = update.message.text
    print(f"Received message: {text}")
    
    result = classify(text)

    if result == "spam":
        response = f"🚫 message from you classified as SPAM(～￣▽￣)～."
        await update.message.reply_text(response)
        save_spam(update)
    else:
        return

def main():
    application = ApplicationBuilder().token(tg_bot_token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(f"Bot @{tg_bot_username} is running...")
    application.run_polling()   

if __name__ == "__main__":
    main()