from flask import Flask, render_template, request
from pymongo import MongoClient
import gridfs

app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

# Setup MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.our_database_name  #  Replace with our database name
fs = gridfs.GridFS(db)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if 'audioFile' in request.files:
        audio_file = request.files['audioFile']
        audio_id = fs.put(audio_file)  # Storing the audio file in GridFS
        return {'status': 'success', 'audio_id': str(audio_id)}, 200
    return {'status': 'error', 'message': 'No audio file provided'}, 400

if __name__ == "__main__":
    app.run(debug=True)
