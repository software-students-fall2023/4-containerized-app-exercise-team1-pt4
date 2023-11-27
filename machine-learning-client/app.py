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

load_dotenv()
uri = os.getenv("URI")

deepgram = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))

mongo = MongoClient(uri, server_api=ServerApi("1"))

try:
    mongo.admin.command("ping")
    print("Successfully connected to MongoDB.")
except (
    pymongo.errors.ConnectionFailure
) as conn_failure:  
    print(f"MongoDB connection failed: {conn_failure}")

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api", methods=["POST"])
async def transcribe():
    """Transcribe audio file using Deepgram."""
    try:
        files = request.files
        if "file" not in files:
            return jsonify({"error": "No file provided"}), 400

        file = files.get("file")
        file_content = file.read()

        # Check if the mimetype is a valid audio type
        valid_audio_mimetypes = [
            "audio/mp3",
            "audio/mp4",
            "audio/mpeg",
            "audio/aac",
            "audio/wav",
            "audio/flac",
            "audio/pcm",
            "audio/x-m4a",
            "audio/ogg",
            "audio/opus",
            "audio/webm",
        ]

        if file.mimetype not in valid_audio_mimetypes:
            return jsonify({"error": "Invalid file type"}), 400

        dg_request = {"mimetype": file.mimetype, "buffer": file_content}

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

        save = {"transcription": transcript}
        mongo.db.transcriptions.insert_one(save)

        return jsonify(save)

    except ValueError as value_error:  
        return jsonify({"error": str(value_error)}), 400
    except requests.ConnectionError:
        return jsonify({"error": "Unable to connect to Deepgram API"}), 500
    except requests.Timeout:
        return jsonify({"error": "Timeout error with Deepgram API"}), 500
    except (
        requests.HTTPError
    ) as http_error:  
        if http_error.response and http_error.response.status_code == 500:
            return jsonify({"error": "Deepgram API internal server error"}), 500
        
        return (
            jsonify({"error": "An error occurred with the Deepgram API"}),
            http_error.response.status_code,
        )
    except Exception:  # pylint: disable=broad-except
        return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
