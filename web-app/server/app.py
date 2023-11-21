"""Module providing routing."""
from flask import Flask, render_template
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
uri=os.getenv('URI')

mongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo.admin.command('ping')
    print("successfully connected to mongo")
except Exception as e:
    print(e)

app = Flask(
    __name__, template_folder="../client/templates", static_folder="../client/static"
)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    """Function to run app if it's run as a script."""
    app.run(debug=True)
