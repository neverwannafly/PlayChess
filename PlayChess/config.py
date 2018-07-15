import os

# Contains username, pass for mongodb server here and also the secret key 
configurations = {
    '_SECRET_KEY' : os.urandom(64),
    'JSON_AUTO_SORT': False,
    'TEST_USERNAME': "test",
    'TEST_PASSWORD': "tets",
}