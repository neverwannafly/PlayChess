from flask import Blueprint, render_template, url_for, request, session, redirect

mod = Blueprint('admin', __name__, template_folder='admin_templates')

from .. import database
db = database.db

from . import classes
admin = classes.Admin(db) # initialise an admin object!

@mod.route('/', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        return render_template('admin_login.html', error_code=1)
    return render_template('admin_login.html', error_code=0)

@mod.route('/dashboard')
def dashboard():
    return 