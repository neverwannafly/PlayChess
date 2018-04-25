"""

Makes the web application modular!

"""

from flask import Flask

app = Flask(__name__)

from PlayChess.site import routes

app.register_blueprint(routes.mod)