import pytest
import PlayChess

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client

def test_check(client):
    """Start with a blank database."""
    rv = client.get('/')
    print(rv)
    assert 1==1
    