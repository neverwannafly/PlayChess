import os
import re as regex

from .utils import game_queue

# Contains username, pass for mongodb server here and also the secret key 
configurations = {
    '_SECRET_KEY' : os.urandom(64),
    'JSON_AUTO_SORT': False,
    'TEST_USERNAME': "test",
    'TEST_PASSWORD': "tets",
}

## Server Global variables

USER_DICT = {}
GAMES = {}
ADMIN_DICT = {}

# Keeps track of players finding matches.
PLAYERS_QUEUE = game_queue.GameQueue()

# Regex expression for email and username verification
EMAIL_PATTERN_COMPILED = regex.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")
# Username regex also limits the string to be b/w 5 and 30!
USERNAME_REGEX = regex.compile("^[a-zA-Z0-9_]{5,30}$")