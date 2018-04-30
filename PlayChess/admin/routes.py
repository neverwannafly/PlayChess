from flask import Blueprint, render_template, url_for, request, session, redirect

mod = Blueprint('admin', __name__, template_folder='admin_templates')

from .. import database
db = database.db

@mod.route('/')
def index():
    return render_template('admin_login.html')