"""ML Client for handling audio transcription using the Deepgram API."""

import json
import os
from flask import Flask, jsonify, request
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from deepgram import Deepgram
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("URI")

deepgram = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))

mongo = MongoClient(uri, server_api=ServerApi("1"))

try:
    mongo.admin.command("ping")
    print("Successfully connected to MongoDB.")
except pymongo.errors.ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api", methods=["POST"])
async def transcribe():
    """Transcribe audio file using Deepgram."""
    files = request.files
    form = request.form
    features = form.get("features")
    model = form.get("model")
    version = form.get("version")
    tier = form.get("tier")

    dg_features = json.loads(features)
    dg_request = None

    if "file" in files:
        file = files.get("file")
        file_content = file.read()
        dg_request = {"mimetype": file.mimetype, "buffer": file_content}

    if not dg_request:
        raise ValueError("No file provided for transcription.")

    transcription = await deepgram.transcription.prerecorded(dg_request, dg_features)

    save={
        "model": model,
        "version": version,
        "tier": tier,
        "dg_features": dg_features,
        "transcription": transcription,
    }

    mongo.db.transcriptions.insert_one(save)

    return jsonify(save)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
