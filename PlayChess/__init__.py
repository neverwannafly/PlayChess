"""

Makes the web application modular!

"""

from flask import Flask
from flask_socketio import SocketIO, send

from .config import configurations

app = Flask(__name__)

# Add configurations

app.secret_key = configurations['_SECRET_KEY']
app.config['JSON_SORT_KEYS'] = configurations['JSON_AUTO_SORT']
app.config['TEST_USERNAME'] = configurations['TEST_USERNAME']
app.config['TEST_PASSWORD'] = configurations['TEST_PASSWORD']

from PlayChess.site.routes import mod
from PlayChess.admin.routes import mod
from PlayChess.blog.routes import mod
from PlayChess.chat.routes import mod

# makes an instance of admin class that can be used to add new admins!

from PlayChess.admin.admins import create_admin

# Register the blueprints!

app.register_blueprint(site.routes.mod)
app.register_blueprint(admin.routes.mod, url_prefix='/admin')
app.register_blueprint(blog.routes.mod, url_prefix='/blog')
app.register_blueprint(chat.routes.mod, url_prefix='/chat')

## Socket IO connection for chat and playing chess game.

socketio = SocketIO(app)

# Makes chess board easily accessible thorugh terminal

from PlayChess.site.chessboard import Chessboard

# Make database accessible for unit testing

from PlayChess.database import db