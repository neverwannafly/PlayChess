from flask import Blueprint

mod = Blueprint('admin', __name__, template_folder='templates')

from .. import database
db = database.db