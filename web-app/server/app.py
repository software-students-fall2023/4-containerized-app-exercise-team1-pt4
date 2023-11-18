"""Module providing routing."""
from flask import Flask, render_template

app=Flask(__name__, template_folder='../client/templates', static_folder='../client/static')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    """Function to run app if it's run as a script."""
    app.run(debug=True)