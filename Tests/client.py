import PlayChess
import pytest

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client

def login(client):
    return_login_status = client.post('/login', data={"username": "unittest", "password": "unittest"})