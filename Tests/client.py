import PlayChess
import pytest

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client