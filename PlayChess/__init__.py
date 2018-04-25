"""

Makes the web application modular!

"""

from flask import Flask

app = Flask(__name__)

from PlayChess.site.routes import mod
from PlayChess.admin.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(admin.routes.mod, url_prefix='/admin')