from PlayChess import db
from .client import client

def test_check_site(client):
    obj = db.users.find_one({
        'username' : 'neverwannafly'
    })
    assert obj['username']=='neverwannafly'
    