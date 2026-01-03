from fastapi import FastAPI, Request,  Query
# from bot.new_tg_bot import setup_webhook_bot
# from bot.discord_bot import run_discord_bot
import sys, os
import threading
import asyncio
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.post_extraction import PostExtractor
from preProcessing.preprocessing import Preprocessing
from src.api.routes.v1 import prediction_route
# from bot.discord_bot import run_discord_bot
# from bot.telegram_bot import run_telegram_bot
from bot.new_tg_bot import setup_webhook_bot


NGROK_URL = "https://rolf-unsatirized-serina.ngrok-free.dev"

bot_app = setup_webhook_bot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔗 Register Telegram webhook
    await bot_app.bot.set_webhook(
        url=f"{NGROK_URL}/telegram_webhook"
    )
    print("✅ Telegram webhook registered")

    # 🚀 START TELEGRAM BOT
    await bot_app.initialize()
    await bot_app.start()
    print("🚀 Telegram bot started")


    # discord_task = asyncio.create_task(run_discord_bot())
    # print("✅ Discord bot started")
    yield

    # 🛑 Shutdown
    # discord_task.cancel()
    await bot_app.stop()
    await bot_app.bot.delete_webhook()
    print("🛑 Telegram bot stopped & webhook removed")


app = FastAPI(
    title="Fake News Detection API",
    lifespan=lifespan
)


app.include_router(prediction_route.router, prefix="/api/v1", tags=["Prediction"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
async def serve_index():
    print("API INITIALIZED")
    return FileResponse(INDEX_PATH)

extractor = PostExtractor()
preprocess = Preprocessing()

  
@app.get("/api/v1/extract")
async def extract_port(url: str = Query(..., description="URL to scrape")):
    try:
        post = extractor.extract_post(url)
        if not post:
            return "Unsupported link"
        
        processed = {
            "titlee": preprocess.tokenize(post["title"]),
            "bodyy": preprocess.tokenize(post["body"])
        }

        return {"original": post, "processed": processed}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    



# 📩 Telegram sends updates here
@app.post("/telegram_webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    from telegram import Update
    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)
    return {"ok": True}