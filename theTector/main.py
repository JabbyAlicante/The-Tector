from flask import Flask, request, jsonify
from flask_cors import CORS  
from fastapi import FastAPI, Query

import os,sys
from threading import Thread
from multiprocessing import Process
import uvicorn
import asyncio
from pathlib import Path


# ==================PATHS==================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../spam")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../fakeh_news/app")))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend")))

from spam.spam_apitry import app as spam_app
from fakeh_app import app as fake_app
# from theTector.bot.discord_the_tector_bot import run_discord_bot
# from theTector.bot.tg_the_tector_bot import main as tg_main
# ========================================

#BACKENDS

# def run_spam():
#     spam_app.run(  host="127.0.0.1",port=5000, debug=False, use_reloader=False)

#     #async
# async def run_fake():
    
#     config = uvicorn.Config(fake_app, host="0.0.0.0", port=8000, reload=False)
#     server = uvicorn.Server(config)
#     await server.serve()

def run_spam():
    spam_app.run(host="127.0.0.1", port=5000, debug=False)

def run_fake():
    uvicorn.run(fake_app, host="0.0.0.0", port=8000, reload=False)

    

# -------------------- bots -----------------

# def run_telegram():
#     # from theTector.bot.tg_the_tector_bot import main as tg_main
#     tg_main()

# async def run_discord():
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(None,run_discord_bot)
    
# async def run_telegram():
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(None,tg_main)


#=================================================== 
    
# async def main():
#     threading.Thread(target=run_spam, daemon = True).start()
    
    
#     await asyncio.gather(
#         run_fake(),
#         # run_discord_bot(),
#         tg_main()
#     )
        

# ==============================================
if __name__ == "__main__":
    spam_thread = Thread(target=run_spam, daemon=True)
    fake_thread = Thread(target=run_fake, daemon=True)

    spam_thread.start()
    fake_thread.start()

    # Keep main thread alive
    spam_thread.join()
    fake_thread.join()
   

# if __name__ == "__main__":
#     # Run the imported Flask app on a different port if you want
#     spam_app.run(port=5000, debug=True)
    
