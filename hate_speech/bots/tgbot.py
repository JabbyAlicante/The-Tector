# from ngrams import *
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from main import *


# Here po yung flow
# sa COMMANDS, bali commands sa tgbot na pwede i-setup sa tg
# kapag ni run ang code, mag wait na si tg bot for responses sa tg
# and kapag nag message na sa tg, papasok muna sa function na handle_message
# then mag reply na si bot using the handle_response na function

# NOTE: (NO NEED TO WORRY NAMAN SA NAKA NOTE PERO NAG INCLUDE AKO JUST IN CASE NA MAG ASK U) 
# kaya may logic na mag check if sa GC or in private nag message ang user
# kasi sa private, every message mag reply si bot pero kapag nasa gc siya, that
# means na mag reply siya sa users. kaya need lang i-mention si bot sa gc tsaka
# lang mag reply. Included kasi ang logic na 'to sa YT tutorial so ni add ko na rin
# YT LINK: https://www.youtube.com/watch?v=vZtm1wuA2yc

TOKEN: Final = '8558133241:AAG-fVtqsubFZYQVNbmPaEItNZjmpBNzY8I'
BOT_USERNAME: Final = '@HateSpeechDTCTR_bot'

# COMMANDS : ito yung nakikita natin na "/start" and "/help" commands
async def start_command(update = Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, this is a bot for school purposes only")

async def help_command(update = Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I will detect if there is a bad word or a hate speech in your sentence base on my dataset.")

# pwede mag custom ng command so if may naisip ka lang na idadagdag, ganito syntax niya
async def custom_command(update = Update, context = ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

# RESPONSES
def handle_response(text: str, user) -> str:
    text = text.lower()

    if user.last_name:
        full_name = f"{user.first_name} {user.last_name}"
    else:
        full_name = user.first_name

    return f"Hi, {full_name}"


# Here mag check if yung nag message ay sa private nag message or in a GC
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user = update.effective_user  # ✅ get the user

    print(f"User: {update.message.chat.id} in {message_type} >>> {text}")

    if message_type == 'group':
        # Group chat
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text, user)
        else:
            return
    else:
        # Private chat
        response: str = handle_response(text, user)

    print('BOT:', response)
    await update.message.reply_text(response)

# Sabi sa YT pang error message lang this
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"UPDATE {update} | caused error: {context.error}")


if __name__ == "__main__":
    print("The bot is starting...")
    app = Application.builder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # MESSAGES
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #  ERRORS
    app.add_error_handler(error)

    # POLLS THE BOT
    print("Polling...")
    app.run_polling(poll_interval=5, drop_pending_updates=True)