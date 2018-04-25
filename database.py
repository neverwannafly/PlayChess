from pymongo import MongoClient

client = MongoClient('mongodb://neverwannafly:Shubham123@ds151169.mlab.com:51169/chess_database')
db = client.chess_database # Establishes connection to mlab database!