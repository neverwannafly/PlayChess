import os
from ..utils import exceptions
from ..config import IS_LOCAL

from pymongo import MongoClient

URL_LOCAL = os.environ.get("DATABASE_LOCAL_URI", None)
URL_PROD = os.environ.get("DATABASE_URL", None)
URL_DEV = os.environ.get("DATABASE_URL_DEV", None)

if URL_PROD:
    client = MongoClient(URL_PROD, serverSelectionTimeoutMS=10000)
    db = client.playchesswebsite
elif URL_LOCAL and IS_LOCAL:
    client = MongoClient(URL_LOCAL, serverSelectionTimeoutMS=10000)
    db = client.chess_database
elif URL_DEV:
    client = MongoClient(URL_DEV, serverSelectionTimeoutMS=10000)
    db = client.chess_database
else:
    raise exceptions.InvalidDatabaseURL("Please Check your database URL")