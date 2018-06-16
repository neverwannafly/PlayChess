from .client import client

def test_check_site(client):
    rv = client.get('/admin')
    print(rv)
    assert 1==1
    