from flask import Flask, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import gridfs
import requests
import os

app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

# Setup MongoDB connection
uri = os.getenv("URI")
mongo_client = MongoClient(uri, server_api=ServerApi("1"))
db = mongo_client.get_default_database()  # Accessing the default database from URI
fs = gridfs.GridFS(db)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if 'audioFile' in request.files:
        audio_file = request.files['audioFile']
        audio_id = fs.put(audio_file)  # Storing the audio file in GridFS

        # Prepare to send the file to the ML client
        ml_response = requests.post(
            "http://localhost:5001/api",  # Adjust the URL as needed
            files={'file': (audio_file.filename, audio_file, audio_file.mimetype)}
        )

        # Process ML response (e.g., transcription)
        transcription = ml_response.json()

        # Optionally send transcription back to the frontend or store it
        return {'status': 'success', 'audio_id': str(audio_id), 'transcription': transcription}, 200

    return {'status': 'error', 'message': 'No audio file provided'}, 400

if __name__ == "__main__":
    app.run(debug=True)
