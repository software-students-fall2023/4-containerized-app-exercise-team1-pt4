"""Module providing routing."""
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, jsonify
import requests
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
user = os.environ["MONGO_INITDB_ROOT_USERNAME"]
passw = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
uri = f"mongodb://{user}:{passw}@mongo:27017/db?authSource=admin"

mongo = MongoClient(uri, server_api=ServerApi("1"))

try:
    mongo.admin.command("ping")
    print("successfully connected to mongo")
except pymongo.errors.ConnectionFailure as e:
    print(e)


app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

app.config["uploads"] = "./uploads"


@app.route("/")
def home():
    """Render home page."""

    transcriptions = list(mongo.db.transcriptions.find())

    return render_template("home.html", transcriptions=transcriptions)


@app.route("/transcribe", methods=["POST"])
def upload():
    """Upload file and send to API."""
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    file.save(os.path.join(app.config["uploads"], file.filename))
    # or temp api url
    res = requests.post(
        "http://localhost:30001/api",
        data=file.read(),
        headers={"Content-Type": file.content_type},
        timeout=20,
    )

    if res.status_code == 200:
        return res.json()

    return (
        jsonify(
            {
                "error": "Something went wrong while trying to transcribe. Please try again."
            }
        ),
        res.status_code,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
