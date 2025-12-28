import os
import sys
import discord
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from spam_classifier import classify_message

load_dotenv()

# Toggle logging to a dedicated channel
ENABLE_CHANNEL_LOGS = True

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_NAME = "spam-logs"
SPAM_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "spam_logs", "discord_logs", "detected_spam.txt")
SPAM_LOG_FILE = os.path.abspath(SPAM_LOG_FILE)
os.makedirs(os.path.dirname(SPAM_LOG_FILE), exist_ok=True)

# Avoid duplicate logging
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
async def log_spam(message, reason="Detected during scan"):
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

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == LOG_CHANNEL_NAME:
                continue
            try:
                print(f"Scanning history in #{channel.name} (guild: {guild.name})")
                async for message in channel.history(limit=100):
                    if str(message.id) in flagged_spam_ids:
                        continue
                    if message.author == client.user:
                        continue
                    if message.content.startswith("🚫"):
                        continue

                    prediction = classify_message(message.content)
                    if prediction == "spam":
                        await log_spam(message, reason="History Scan")
                        save_spam(message)
            except Exception as e:
                print(f"⚠️ Cannot read {channel}: {e}")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.channel.name == LOG_CHANNEL_NAME:
        return

    if str(message.id) in flagged_spam_ids:
        return

    prediction = classify_message(message.content)
    if prediction == "spam":
        await log_spam(message, reason="Live Message")
        save_spam(message)
        await message.channel.send(
            f"🚫 {message.author.mention}, Spam alert!! message from you classified as SPAM (^^ゞ.."
        )

client.run(TOKEN)
