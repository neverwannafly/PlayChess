from PlayChess import db
from .client import client

def test_find_user(client):
    obj = db.users.find_one({
        'username' : 'unittest'
    })
    assert obj['username']=='unittest'
    assert obj['first_name']=='Alpha'
    