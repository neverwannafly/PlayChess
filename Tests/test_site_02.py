from .client import client

def test_check_site(client):
    rv = client.get('/login')
    print(rv.status)
    assert 1==2
    