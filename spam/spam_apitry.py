import os, sys


# sys.path.append(os.path.dirname(__file__))



from flask import Flask, request, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../spam")))

from spam_classifier import classify_message
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

@app.route("/classify", methods=["POST"])
def classify():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    prediction = classify_message(message)  
    return jsonify({"prediction": prediction})

# if __name__ == "__main__":
#     app.run(port=5000)
