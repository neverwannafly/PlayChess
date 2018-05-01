"""

Makes the web application modular!

"""

from flask import Flask

app = Flask(__name__)

from PlayChess.site.routes import mod
from PlayChess.admin.routes import mod

# makes an instance of admin class that can be used to add new admins!

from PlayChess.admin.routes import new_admin
create_new_admin = new_admin

# Register the blueprints!

app.register_blueprint(site.routes.mod)
app.register_blueprint(admin.routes.mod, url_prefix='/admin')