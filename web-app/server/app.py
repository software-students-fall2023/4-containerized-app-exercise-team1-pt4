"""Module providing routing."""
from flask import Flask, render_template, request, flash, redirect
import os
from dotenv import load_dotenv
import requests

app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)

app.config['uploads'] = './uploads'


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    file.save(os.path.join(app.config['uploads'], file.filename))
    # or temp api url
    res=requests.post('http://localhost:5000/api', data=file.read(), headers={'Content-Type': file.content_type})

if __name__ == "__main__":
    """Function to run app if it's run as a script."""
    app.run(debug=True)
