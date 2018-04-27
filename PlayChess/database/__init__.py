from . import config
from pymongo import MongoClient

configurations = config.configurations

client = MongoClient('mongodb://' + configurations['_USERNAME'] + ':' + configurations['_PASSWORD'] + '@ds151169.mlab.com:51169/chess_database')
db = client.chess_database # Establishes connection to mlab database!