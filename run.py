from PlayChess import app
from pymongo import MongoClient
from config import configurations

client = MongoClient('mongodb://' + configurations['_USERNAME'] + ':' + configurations['_PASSWORD'] + '@ds151169.mlab.com:51169/chess_database')
db = client.chess_database # Establishes connection to mlab database!

app.secret_key = configurations['_SECRET_KEY']

app.run(debug=True)
