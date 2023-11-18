import json
from deepgram import Deepgram
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort, make_response
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

load_dotenv()
uri=os.getenv('URI')

deepgram = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))

mongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo.admin.command('ping')
    print("successfully connected to mongo")
except Exception as e:
    print(e)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api", methods=["POST"])
async def transcribe():
    files = request.files
    form = request.form
    features = form.get("features")
    model = form.get("model")
    version = form.get("version")
    tier = form.get("tier")

    dgFeatures = json.loads(features)
    dgRequest = None

    try:
        if "file" in files:
            file = files.get("file")
            file_content = file.read()
            dgRequest = {"mimetype": file.mimetype, "buffer": file_content}


        if not dgRequest:
            raise Exception("Error: No file provided for transcription.")

        transcription = await deepgram.transcription.prerecorded(dgRequest, dgFeatures)

        return jsonify(
            {
                "model": model,
                "version": version,
                "tier": tier,
                "dgFeatures": dgFeatures,
                "transcription": transcription,
            }
        )
    except Exception as error:
        return json_abort(error)
    
def json_abort(message):
    print(message)
    return abort(make_response(jsonify(err=str(message)), 500))