from flask import Flask, request, jsonify
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

if __name__ == "__main__":
    app.run(port=5000)
