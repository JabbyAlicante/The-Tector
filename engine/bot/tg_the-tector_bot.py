from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio
import aiohttp
from telegram.ext import MessageHandler, filters
from tg_fake_module import run_fakeh_module
from tg_spam_module import handle_message as spam_handler

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")
#====================================================
TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_BOT_USERNAME = "@the_tector_bot"
print("TOKEN: ", TOKEN)



#======================COMMANDS=================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your The-Tector bot 🤖")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start\n/help")

# app = ApplicationBuilder().token(TOKEN).build()

# app.add_handler(CommandHandler("start", start))
# app.add_handler(CommandHandler("help", help_command))

# print("Bot is running...")
# app.run_polling()



async def check_command(update, context):
    if update.message.reply_to_message:
        text = update.message.reply_to_message.text
    else:
        text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "⚠️ Use /check <text> or reply with /check"
        )
        return

    await update.message.chat.send_action("typing")
    result = await run_fakeh_module(text)
    await update.message.reply_text(result)
    
    
    
# async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = update.message
#     user_id = message.from_user.id
    

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spam_handler))

    print("🤖 Telegram bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()