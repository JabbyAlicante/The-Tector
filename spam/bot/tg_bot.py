from dotenv import load_dotenv
import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from spam_classifier import classify_message as classify
load_dotenv()

ENABLE_CHANNELS = True  # Set to False to disable channels
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
def save_spam(msg):
    message_id = str(msg.message_id)
    if message_id in flagged_spam_ids:
        return

    flagged_spam_ids.add(message_id)

    with open(SPAM_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"ID: {message_id}\n")

        if msg.from_user:
            f.write(
                f"Author: {msg.from_user.username or msg.from_user.full_name} "
                f"(ID: {msg.from_user.id})\n"
            )
        else:
            f.write("Author: CHANNEL POST\n")

        f.write(f"Message: {msg.text}\n")
        f.write("----------------------------------------\n\n")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = None

    if update.message:
        msg = update.message
    elif ENABLE_CHANNELS and update.channel_post:
        msg = update.channel_post

    if not msg or not msg.text:
        return
    
     # 🔒 Prevent bot loops
    if msg.from_user and msg.from_user.is_bot:
        return

    text = msg.text
    print(f"Received message: {text}")

    result = classify(text)

    if result == "spam":
        response = "🚫Spam alert!! message from you classified as SPAM (^^ゞ."

        try:
            if msg.chat.type == "channel":
                await msg.delete()
            else:
                await msg.reply_text(response)
        except Exception as e:
            print("Spam action failed:", e)

        save_spam(msg)


def main():
    application = ApplicationBuilder().token(tg_bot_token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(f"Bot @{tg_bot_username} is running...")
    application.run_polling()   

if __name__ == "__main__":
    main()