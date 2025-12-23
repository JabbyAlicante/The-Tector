import sys, os
import threading
import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from post_extraction import PostExtractor
from preProcessing.preprocessing import Preprocessing
from api.routes.v1 import prediction_route
from bot.discord_bot import run_discord_bot
from bot.telegram_bot import run_telegram_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Launching Discord & Telegram bots...")

    # asyncio.create_task(run_discord_bot())
    asyncio.create_task(run_telegram_bot())

    print("✅ Discord n Telegram bots started in background")
    yield
    print("🛑 Application shutting down")


app = FastAPI(title="Fake News Detection API", version="1.0.0", lifespan = lifespan)


app.include_router(prediction_route.router, prefix="/api/v1", tags=["Prediction"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
async def serve_index():
    print("API INITIALIZED")
    return FileResponse(INDEX_PATH)

# @app.get("/")
# async def root():
#     return {"message": "Welcome to Fake News Detection API 🚀"}


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
    

# ------------- RUN BOT -----------------
# @app.on_event("startup")
# async def startup_event():
#     def start_bot():
#         # discord
#         run_discord_bot()
#         # teltgram
#         run_telegram_bot()

#     thread = threading.Thread(target=start_bot, daemon=True)
#     thread.start()
#     print("Discord n Telegram bot started")

# @app.on_event("startup")
# async def startup_event():
#     print("🚀 Launching Discord & Telegram bots...")

#     loop = asyncio.get_event_loop()
#     loop.create_task(run_discord_bot())   # run discord bot async
#     loop.create_task(run_telegram_bot())  # run telegram bot async

#     print("✅ Discord n Telegram bots started in background")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
