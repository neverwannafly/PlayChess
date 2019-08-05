"""

Makes the web application modular!

"""

import os

from flask import Flask
from flask_socketio import SocketIO

from .config import configurations

app = Flask(__name__)

# Read from environment file and load local env variables
if not os.environ.get('Production', False) and not os.environ.get('TRAVIS', False):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, '.env')) as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Add configurations
app.secret_key = configurations['_SECRET_KEY']
app.config['JSON_SORT_KEYS'] = configurations['JSON_AUTO_SORT']

app.config['TEST_PASSWORD'] = os.environ.get('TEST_PASSWORD', None)
app.config['TEST_USERNAME'] = os.environ.get('TEST_USERNAME', None)

# Socket IO connection.
socketio = SocketIO(app)

# Imports
from PlayChess.site.routes import mod
from PlayChess.admin.routes import mod
from PlayChess.blog.routes import mod
from PlayChess.chat.routes import mod
from PlayChess.game.routes import mod
from PlayChess.api.routes import mod

# makes an instance of admin class that can be used to add new admins!
from PlayChess.admin.admins import create_admin

# Register the blueprints!
app.register_blueprint(site.routes.mod)
app.register_blueprint(admin.routes.mod, url_prefix='/admin')
app.register_blueprint(blog.routes.mod, url_prefix='/blog')
app.register_blueprint(chat.routes.mod, url_prefix='/chat')
app.register_blueprint(game.routes.mod, url_prefix='/game')
app.register_blueprint(api.routes.mod, url_prefix='/api')

# Makes chess board and state classes easily accessible thorugh terminal
from PlayChess.utils.chessboard import Chessboard
from PlayChess.utils.chessboard import Branch
from PlayChess.utils.chessboard import StateManager

# Make database accessible for unit testing
from PlayChess.database import db