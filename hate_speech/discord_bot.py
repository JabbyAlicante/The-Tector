import os
import sys
import discord
from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import reply_message, get_bad_words, get_users_log

load_dotenv()



# ---------------- CONFIG ---------------- #

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_NAME = "hate-speech-logs"

LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "logs",
    "discord_hate_logs.txt"
)
LOG_FILE = os.path.abspath(LOG_FILE)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

ENABLE_CHANNEL_LOGS = True
flagged_message_ids = set()



if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ID:"):
                flagged_message_ids.add(line.replace("ID:", "").strip())

# ---------------- LOGGING ---------------- #

def save_hate_message(message, reason="Detected"):
    msg_id = str(message.id)

    if msg_id in flagged_message_ids:
        return

    flagged_message_ids.add(msg_id)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"ID: {msg_id}\n"
            f"👤 Author: {message.author} (ID: {message.author.id})\n"
            f"📍 Channel: {message.channel}\n"
            f"📝 Message: {message.content}\n"
            f"📌 Reason: {reason}\n"
            f"{'-'*40}\n"
        )

async def log_to_channel(message, reason="Live Detection"):
    if not ENABLE_CHANNEL_LOGS or not message.guild:
        return

    log_channel = discord.utils.get(
        message.guild.text_channels, name=LOG_CHANNEL_NAME
    )

    if log_channel:
        await log_channel.send(
            f"🚨 **Hate Speech Detected**\n"
            f"👤 Author: {message.author} (ID: {message.author.id})\n"
            f"📍 Channel: {message.channel.mention}\n"
            f"📝 Message: {message.content}\n"
            f"📌 Reason: {reason}"
        )

# ---------------- DISCORD CLIENT ---------------- #

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    # preload data
    get_users_log()
    get_bad_words()

    print("📚 Hate speech dataset loaded")

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.guild:
        if message.channel.name == LOG_CHANNEL_NAME:
            return

    if str(message.id) in flagged_message_ids:
        return

    user = message.author
    full_name = f"{user.name}"

    response = reply_message(
        message.content,
        full_name
    )

    if response:
        await log_to_channel(message)
        save_hate_message(message)

        try:
            await message.delete()
        except Exception:
            pass

        await message.channel.send(
            f"🚫 {user.mention} {response}"
        )

client.run(TOKEN)
