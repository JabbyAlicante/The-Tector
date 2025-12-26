import os
import sys
import discord
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from spam_classifier import classify_message

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

LOG_CHANNEL_NAME = "spam-logs"
SPAM_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "spam_logs", "discord_logs", "detected_spam.txt")
SPAM_LOG_FILE = os.path.abspath(SPAM_LOG_FILE)
os.makedirs(os.path.dirname(SPAM_LOG_FILE), exist_ok=True)

#para ma avoid ung double read etc
flagged_spam_ids = set()
if os.path.exists(SPAM_LOG_FILE):
    with open(SPAM_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("ID:"):
                flagged_spam_ids.add(line.replace("ID:", "").strip())

def save_spam(message):
    flagged_spam_ids.add(str(message.id))
    with open(SPAM_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"ID: {message.id}\n"
            f"Author: {message.author} (ID: {message.author.id})\n"
            f"Message: {message.content}\n"
            f"{'-'*40}\n"
        )

#SPAM LOGSS IN DISCORD CHANNEL
async def log_spam(message, reason="Detected during scan"):
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

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == LOG_CHANNEL_NAME:
                continue
            try:
                print(f" Scanning history in #{channel.name} (guild: {guild.name})")
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
                        await message.delete()
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
        await message.delete()
        await message.channel.send(
            f"🚫 {message.author.mention}, your message was removed as spam. Please be mindful. (●'◡'●)"
        )

client.run(TOKEN)
