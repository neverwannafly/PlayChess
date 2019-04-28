import PlayChess
import pytest
import os

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client

def login(client):
    return_login_status = client.post('/login', data={
        "username": os.environ.get('TEST_DB_USER', None), 
        "password": os.environ.get('TEST_DB_PASS', None),
    })