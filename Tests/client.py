import PlayChess
import pytest
import os

from .config import db_pass, db_user

@pytest.fixture
def client():
    PlayChess.app.config['TESTING'] = True
    client = PlayChess.app.test_client()
    yield client

def login(client):
    return_login_status = client.post('/login', data={
        "username": db_user, 
        "password": db_pass,
    })