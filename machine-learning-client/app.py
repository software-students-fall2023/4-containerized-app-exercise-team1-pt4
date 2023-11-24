"""ML Client for handling audio transcription using the Deepgram API."""

import os
from flask import Flask, jsonify, request
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from deepgram import Deepgram
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import requests

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
    dg_request = None

    if "file" in files:
        file = files.get("file")
        file_content = file.read()
        dg_request = {"mimetype": file.mimetype, "buffer": file_content}

    if not dg_request:
        raise ValueError("No file provided for transcription.")

    try:
        transcription = await deepgram.transcription.prerecorded(
            dg_request,
            {
                "smart_format": True,
                "model": "nova-2",
            },
        )
        transcript = transcription["results"]["channels"][0]["alternatives"][0][
            "transcript"
        ]
    except requests.ConnectionError:
        print("Connection error: Unable to connect to Deepgram API.")
    except requests.Timeout:
        print("Timeout error: The Deepgram API did not respond in time.")

    transcription = await deepgram.transcription.prerecorded(dg_request, dg_features)

    save = {
        "model": model,
        "version": version,
        "tier": tier,
        "dg_features": dg_features,
        "transcription": transcript,
    }

    mongo.db.transcriptions.insert_one(save)

    return jsonify(save)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
