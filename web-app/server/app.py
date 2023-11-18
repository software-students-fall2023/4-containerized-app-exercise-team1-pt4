from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, abort, url_for, make_response

app=Flask(__name__, template_folder='../client/templates', static_folder='../client/static')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
    
