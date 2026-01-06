from flask import Flask, request, jsonify

from flask_cors import CORS  

import os,sys
import threading
import uvicorn


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../spam")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../fakeh_news/app")))

from spam.spam_apitry import app as spam_app
from fakeh_app import app as fake_app

def run_spam():
    spam_app.run(port=5000, debug=False, use_reloader=False)

    
def run_fake():
    uvicorn.run(
        fake_app,
        host="0.0.0.0",
         port=8000,
         reload=False
        )
    
    
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_spam, daemon=True)
    flask_thread.start()

    run_fake()
    


# if __name__ == "__main__":
#     # Run the imported Flask app on a different port if you want
#     spam_app.run(port=5000, debug=True)
    
