import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../spam")))

from spam_classifier import classify_message

from spam_classifier import classify_message
import discord
import os

# Existing logging setup
ENABLE_CHANNEL_LOGS = True
LOG_CHANNEL_NAME = "spam-logs"
SPAM_LOG_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "spam_logs", "discord_logs", "detected_spam.txt")
)
os.makedirs(os.path.dirname(SPAM_LOG_FILE), exist_ok=True)

flagged_spam_ids = set()
if os.path.exists(SPAM_LOG_FILE):
    with open(SPAM_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ID:"):
                flagged_spam_ids.add(line.replace("ID:", "").strip())

# Save spam to file
def save_spam(message):
    msg_id = str(message.id)
    if msg_id in flagged_spam_ids:
        return
    flagged_spam_ids.add(msg_id)
    with open(SPAM_LOG_FILE, "a", encoding="utf-8") as f:
        author_info = "CHANNEL POST" if not message.author else f"{message.author} (ID: {message.author.id})"
        f.write(
            f"ID: {msg_id}\n"
            f"Author: {author_info}\n"
            f"Message: {message.content}\n"
            f"{'-'*40}\n"
        )

# Log spam in a dedicated channel
async def log_spam(message, bot, reason="Detected during scan"):
    if not ENABLE_CHANNEL_LOGS or not message.guild:
        return
    log_channel = discord.utils.get(message.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        await log_channel.send(
            f"🚨 Spam detected ({reason})\n"
            f"👤 Author: {message.author} (ID: {message.author.id})\n"
            f"📍 Channel: {message.channel.mention}\n"
            f"📝 Message: {message.content}"
        )
    else:
        print("⚠️ Log channel not found.")

# The new is_spam function to call in your main bot
async def is_spam(message, bot=None):
    """
    Returns True if the message is spam.
    If 'bot' is provided, logs spam in the spam channel.
    """
    if str(message.id) in flagged_spam_ids:
        return False

    prediction = classify_message(message.content)
    if prediction == "spam":
        save_spam(message)
        if bot:
            await log_spam(message, bot, reason="Live Message")
        return True
    return False
