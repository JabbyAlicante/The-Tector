import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv  # Make sure to import this
import asyncio
import aiohttp
import logging
import re
from discord_spam_module  import is_spam
from discord_fakeh_module import check

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("DISCORD_TOKEN")  # Reads token from .env

# Enable intents to read messages
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.add_command(check)

#=======================EVENTS======================================
@bot.event
async def on_ready():
    print("We are ready to go")
    # logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(name='Fake News Detector'))

@bot.event
async def on_message(message):
    print("Received message:", message.content)
    if message.author == bot.user:
        return
    
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"Watch your language, {message.author.name}!")

    if await is_spam(message, bot):
        await message.channel.send(f"{message.author.name}, please stop spamming!")

    await bot.process_commands(message)


#--------------------------BASIC COMMANDS-----------------------
@bot.command()
async def hello(ctx):
    print("hi")
    await ctx.send(f"Hello {ctx.author.name}!") # "!hello"
    


#--------------------------DETECTION FUNCTION-----------------------

    
if __name__ == "__main__":
    bot.run(TOKEN)
