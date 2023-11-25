"""Module providing routing."""
import os
from flask import Flask, render_template, request, flash, redirect, jsonify
import requests

app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

app.config["uploads"] = "./uploads"


@app.route("/")
def home():
    """Render home page."""
    return render_template("home.html")


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
        "http://localhost:5000/api",
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
    app.run(debug=True, port=3000)
