from PlayChess import db
from .client import client

def test_find_user(client):
    obj = db.users.find_one({
        'username' : 'mpkst4szSX99pwc'
    })
    assert obj['username']=='mpkst4szSX99pwc'
    assert obj['first_name']=='Keeny'
    