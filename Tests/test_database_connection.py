from PlayChess import db
from .client import client

def test_find_user(client):
    obj = db.users.find_one({
        'username' : 'test_user_'
    })
    assert obj['username']=='test_user_'
    assert obj['first_name']=='Test'
    