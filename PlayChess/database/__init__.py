from . import config
from pymongo import MongoClient

URL = os.environ.get("DATABASE_URL", None)
if URL:
    client = MongoClient(URL)
else:
    configurations = config.configurations
    client = MongoClient('mongodb://' + configurations['_USERNAME'] + ':' + configurations['_PASSWORD'] + '@ds151169.mlab.com:51169/chess_database', serverSelectionTimeoutMS=10000)
    
db = client.chess_database # Establishes connection to mlab database!