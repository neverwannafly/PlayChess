import PlayChess
from .client import client

import string
import random

def test_login_logout(client):
    return_login_status = client.post('/login', data={"username": "unittest", "password": "unittest"})
    # Redirected to home
    assert return_login_status.status_code==302
    # Now that user is logged in, he can access home screen
    home_view = client.get('/')
    assert home_view.status_code==200
    # Making sure logged in user cannot access logged out views by making sure 
    # they have a status of 302
    random_username = "".join(random.choices(string.ascii_lowercase, k=20))
    login_view = client.get('/login')
    verify_view = client.get('/verify/'+random_username)
    retry_verify_view = client.get('/verify/retry')
    assert (login_view.status_code==302 and verify_view.status_code==302 and retry_verify_view.status_code==302)
    # logout (only possible for logged in users)
    return_logout_status = client.get('/logout')
    assert return_logout_status.status_code==302
    # Now home screen should be inaccessbile
    return_home_view = client.get('/')
    assert return_home_view.status_code!=200

