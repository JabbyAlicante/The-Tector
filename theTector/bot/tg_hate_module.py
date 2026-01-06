# from ngrams import *
import os
from typing import Final
from datetime import datetime, timedelta, timezone
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import ChatPermissions
# from tgbe import *
import json
import re
from datetime import datetime, timedelta
# from main import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
violators_f = os.path.join(BASE_DIR, '../..','hate_speech','datasets', 'violators.json')
bad_words_f = os.path.join(BASE_DIR, '../..','hate_speech','datasets', 'bad_words.json')




async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, seconds: int = 10):
    until = datetime.now(timezone.utc) + timedelta(seconds=seconds)

    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
        # other permissions left as None
    )

    try:
        result = await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=permissions,
            until_date=until
        )

        if result: 
            await update.message.reply_text(
                f"⚠️ User has been muted for {seconds} seconds."
            )
        else:
            await update.message.reply_text(
                "Could not mute the user. Check if they are an admin or owner."
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error muting user: {e}"
        )
async def temporary_mute(update, context, user_id, seconds=10):
    # Step 1: Restrict sending messages
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=False,
        )
    )

    # Notify user muted
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"⚠️ User muted for {seconds} seconds."
    )

    # Step 2: Wait
    await asyncio.sleep(seconds)

    # Step 3: Restore normal permissions
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
        )
    )

    # Notify user unmuted
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"✅ User unmuted after {seconds} seconds."
    )

    
# RESPONSES
def handle_response(text: str, user) -> str | None:
    text = text.lower()

    return reply_message(text, user)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    print(f"User {user.id} in {update.effective_chat.type}: {text}")

    # Check response for bad words
    response = handle_response(text, user)

    if response:  # Only if there’s a warning
        await update.message.reply_text(response)

        # Temporarily mute if warnings are enough
        ban_until = check_warnings(user.id)
        if ban_until:
            # Use the temporary_mute function instead
            asyncio.create_task(temporary_mute(update, context, user.id, seconds=10))
        # Delete only the offending message
        try:
            await update.message.delete()
        except Exception:
            pass

# Sabi sa YT pang error message lang this
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"UPDATE {update} | caused error: {context.error}")


bw = None

def check_violator_exists(user_id, violators):
    return any(v["id"] == user_id for v in violators["violators"])

def add_violator(violator_id, first_name, last_name):
    violators = get_violators_log()

    violators["violators"].append({
        "id": violator_id,
        "full_name": f"{first_name} {last_name}",
        "warnings": 0,
        "banned_until": None
    })

    with open(violators_f, "w", encoding="utf-8") as f:
        json.dump(violators, f, indent=4)

def compute_ban_duration():
    now = datetime.now()
    ban_duration = now + timedelta(hours=2)

    # print(ban_duration.strftime("%Y-%m-%d %H:%M:%S"))
    return ban_duration

def check_warnings(user_id):
    violators = get_violators_log()

    for vltr in violators["violators"]:
        if vltr["id"] == user_id and vltr["warnings"] > 1:
            # Reset warnings
            vltr["warnings"] = 0
            with open(violators_f, "w", encoding="utf-8") as f:
                json.dump(violators, f, indent=4)

            # Return True to indicate mute should happen
            return True

    # Not enough warnings
    return False

    
    # print(violators["violators"])
    # for key, val in violators.items():
    #     print(val)
    # pass

def get_violators_log():
    with open(violators_f, "r", encoding="utf-8") as v_f:
        violators = json.load(v_f)

    # print("get violators log: ", violators)

    # check_warnings(violators)
    return violators

def update_violator(id):
    log = get_violators_log()

    for vltr in log["violators"]:
        if vltr["id"] == id:
            vltr["warnings"] += 1
            break
    
    with open(violators_f, "w", encoding="utf-8") as updated_log_f:
        json.dump(log, updated_log_f, indent = 4)
    # pass

# def get_users_log():
#     with open("./hate_speech/datasets/users.json", "r", encoding="utf-8") as users_f:
#         users = json.load(users_f)

    # print("get users log: ", users)

    # check_users(users)
    # return users

def log_user():
    pass

def reply_message(rcved_mssg, user):
    tknz = tokenize(rcved_mssg)
    print(f"Tokens: {tknz}")

    violators = get_violators_log()

    if any(token in bw for token in tknz):
        if not check_violator_exists(user.id, violators):
            add_violator(user.id, user.first_name, user.last_name)
        else:
            update_violator(user.id)

        return f"⚠️ Warning: {user.full_name}"
    
    return None

def get_bad_words():
    global bw

    # if bw is None:
    #     bw = get_bad_words()

    print("get_bad_words")
    with open(bad_words_f, "r", encoding="utf-8") as f:
        bw = json.load(f)

    return bw

def normalize(text):
    text = text.lower()
    text = re.sub(r"\W", '', text)
    text = re.sub(r"\s+", '', text)
    return text

def tokenize(text, special_tokens = True):
    # TODO: exclude multi-word
    # tokens = re.split('[—\-\s\']', text)
    tokens = re.split(r"[—\-\s']", text)

    tokens = list(map(normalize, tokens))

    # This one is optional, depending on your use case
    # if special_tokens:
    #     tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]
    return tokens
bw = get_bad_words()
print(f"Loaded {len(bw)} bad words")

# if __name__ == "__main__":
#     # m = main("bastard", "sample_violator")
#     # print(m)

#     # get_violators_log()

#     # check_warnings()
    
#     compute_ban_duration()

# =======================================
# if __name__ == "__main__":
#     usrs = get_violators_log()
#     print("users log retrieved")

#     bw = get_bad_words()
#     print("bad wprds retrieved")
#     # print(bw[0])

#     # check_users()
#     # print("users checked")
#     print("The bot is starting...")
#     app = Application.builder().token(TOKEN).build()


#     # COMMANDS
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('custom', custom_command))

#     # MESSAGES
#     app.add_handler(
#         MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
#     )
#     #  ERRORS
#     app.add_error_handler(error)

#     # POLLS THE BOT
#     print("Polling...")
    
#     app.run_polling(poll_interval=5, drop_pending_updates=True)

