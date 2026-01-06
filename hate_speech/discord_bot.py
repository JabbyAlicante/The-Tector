import os
import sys
import discord
from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from main import reply_message, get_bad_words, get_users_log
from main import reply_message, preload_datasets, get_violators_log, analyze_content


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

def save_hate_message(message, reason="Detected", response_text=None):
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
            f"📝 Analysis:\n{response_text}\n"
            f"{'-'*40}\n"
        )

async def log_to_channel(message, reason="Live Detection", response_text=None):
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
    # get_users_log()
    # get_badwords()

    preload_datasets()
    users_log = get_violators_log()

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

    class DiscordUser:
        def __init__(self, discord_user):
            self.discord_user = discord_user  
            self.id = discord_user.id
            self.first_name = discord_user.name
           
            self.last_name = discord_user.display_name if discord_user.display_name != discord_user.name else ""

        @property
        def full_name(self):
            return f"{self.first_name} {self.last_name}".strip()

        @property
        def mention(self):
            return self.discord_user.mention

    user = DiscordUser(message.author)
    # user = message.author
    # full_name = f"{user.name}"


    response = reply_message(
        message.content,
        user
    )

    if response:
        # await log_to_channel(message)
        # save_hate_message(message)
        
        save_hate_message(message, response_text=response)
        await log_to_channel(message, response_text=response)


        try:
            await message.delete()
        except Exception:
            pass

        analysis = analyze_content(message.content)
        details = []

        if analysis['profanity']['detected']:
            details.append(f"⚠️ Profanity detected: {analysis['profanity']['matched_words']}")

        if analysis['hate_speech']['detected']:
            details.append("🚫 Hate speech detected!")
            details.append(f"Target groups: {analysis['hate_speech']['target_groups']}")
            details.append(f"Slurs: {analysis['hate_speech']['signals']['slurs']['matches']}")


        await message.channel.send(
            f"🚫 {user.mention} {response}"
        )

client.run(TOKEN)
