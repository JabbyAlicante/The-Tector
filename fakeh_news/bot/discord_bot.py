import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

API_URL_PREDICT = "http://127.0.0.1:8000/api/v1/predict"
API_URL_PREDICT_LINK = "http://127.0.0.1:8000/api/v1/extract?url={}"

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ----------------- EVENTS -------------------
@bot.event
async def on_ready():
    print("We are ready to go")
    # logging.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(name='Fake News Detector'))


# @bot.event
# async def on_member_join(member):
#     await member.send(f"Welcome to the server, {member.name}!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"Watch your language, {message.author.name}!")

    await bot.process_commands(message) # continue handling other messages


# ----------------- FUNCTIONS -------------------
async def fn_api(payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL_PREDICT, json=payload) as response:
            if response.status != 200:
                return {"error": f"api error {response.status}"}
            return await response.json()

async def call_extract(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL_PREDICT_LINK.format(url)) as response:
            if response.status != 200:
                return {"error": f"extract api error {response.status}"}
            return await response.json()

# ----------------- COMMANDS -------------------
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!") # "!hello"


@bot.command()
async def check(ctx, *, input_text: str = None):
    contentt = None

    # pag reply
    if ctx.message.reference:
        try:
            original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            contentt = original_message.content
        except discord.NotFound:
            await ctx.send("⚠️ could not find reply message")

    elif input_text:
        contentt = input_text.strip()

    else:
        await ctx.send("⚠️ provide text/link or reply to a message with `!check`")
        return
    

    # payload = {"link": contentt} if contentt.startswith("http") else {"text": contentt}
    
    # await ctx.send("Analyzing...")

    try:
        if contentt.startswith("http"):
            extract_response = await call_extract(contentt)
            if "error" in extract_response:
                await ctx.send(f"API ERROR: {extract_response["error"]}")
                return
            
            user_input = f"{extract_response['original'].get('title', '')}\n{extract_response['original'].get('body', '')}"
            payload = {"text": user_input}

            print("INPUT:", user_input)

            # snippet = user_input[:200]
            # await ctx.send(f"Extracted snippet:\n```{snippet}```")
        else:
            payload = {"text": contentt}


        data = await fn_api(payload)

        if "error" in data:
            await ctx.send(f"API ERROR: {data["error"]}")
            return
        
        prediction_class = data.get("prediction_class", "Unkown")
        confidence = (
                data.get("real_percentage", 0)
                if prediction_class.lower() == "real"
                else data.get("fake_percentage", 0)
            )
        roun_confidence = round(confidence, 2)


        # if "user_input" in data and payload.get("link"):
        #     extracted = data["user_input"][:200]  
        #     await ctx.send(
        #         f" Extracted snippet:\n```{extracted}```"
        #     )

        if prediction_class.lower() == "real":
            msg = f"✅ REYAL: {roun_confidence}% confidence"
        else: 
            msg = f"⚠️ FAKEH: {roun_confidence}% confidence"

        await ctx.send(msg)

        # await ctx.send(
        #     f"Prediction: **{prediction_class.upper()}** news "
        #     f"with {roun_confidence}% confidence."

        #     if prediction_class.lower() == "real":
        #         f"✅ REAL: {roun_confidence}% confidence"
        #     else:
        #         f"⚠️ FAKE: {roun_confidence}% confidence"

        # )

    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")  



# def run_discord_bot():
#     bot.run(token, log_handler=handler, log_level=logging.DEBUG)
async def run_discord_bot():
    await bot.start(token)