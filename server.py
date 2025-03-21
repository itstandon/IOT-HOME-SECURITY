from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# 🔹 Replace with your MongoDB Atlas URI
#MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/fingerprintDB?retryWrites=true&w=majority"
MONGO_URI = "mongodb+srv://iarushitandon:AUtDrxD9eo8422EK@cluster0.5pntn.mongodb.net/fingerprintDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.fingerprintDB
collection = db.fingerprints

# 🔹 API to receive fingerprint data from ESP32
@app.route("/add-fingerprint", methods=["POST"])
def add_fingerprint():
    try:
        data = request.json
        finger_id = data.get("fingerID")
        confidence = data.get("confidence")

        if finger_id is None or confidence is None:
            return jsonify({"error": "Missing fingerprint data"}), 400

        fingerprint_data = {
            "fingerID": finger_id,
            "confidence": confidence,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(fingerprint_data)
        return jsonify({"message": "✅ Fingerprint stored successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 API to fetch all stored fingerprints
@app.route("/get-fingerprints", methods=["GET"])
def get_fingerprints():
    try:
        fingerprints = list(collection.find({}, {"_id": 0}))  # Exclude _id field
        return jsonify(fingerprints), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
