import PlayChess
import pytest

from .config import db_pass, db_user

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client

def login(client):
    client.post('/login', data={
        "username": db_user, 
        "password": db_pass,
    })

def logout(client):
    client.get('/logout')