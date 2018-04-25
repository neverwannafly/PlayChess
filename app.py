from flask import Flask
from database import db

app = Flask(__name__)

@app.route('/')
def index():
    return "working!"

if __name__=='__main__':
    app.run(debug=True)