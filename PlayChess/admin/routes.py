### IMPORTANT NOTE ###
# Admins should only be created through command line!

from flask import Blueprint, render_template, url_for, request, session, redirect
import bcrypt as hash_pass
from functools import wraps

mod = Blueprint('admin', __name__, template_folder='admin_templates')

from .. import database
db = database.db

from . import classes
current_admin = classes.Admin(db) # initialise an admin object to be able to load admin!
new_admin = classes.Admin(db) # initialise an admin object to be able to make a new admin!

# login_required and logout_required decorators that ensure certain url's confront to 
# respective wanted behaviors!

# Custom login_required decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        if admin_username:
            # if there's an admin in session, set the current_admin to that admin!
            current_admin.loadAdmin(session['admin_username'])
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return wrapper

# logout required decorator to access admin login!
def logout_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        if admin_username:
            return redirect(url_for('admin.dashboard'))
        else:
            return view_function(*args, **kwargs)
    return wrapper


# Makes session for an admin expire as soon as he closes down the browser!
@mod.before_request
def make_session_permanent():
    session.permanent = False

@mod.route('/', methods=['POST', 'GET'])
@logout_required
def login():
    if request.method=='POST':
        if current_admin.loadAdmin(request.form['admin_username'].lower()):
            if hash_pass.hashpw(request.form['admin_password'], current_admin.admin_password)==current_admin.admin_password:
                session['admin_username'] = current_admin.admin_username
                return redirect(url_for('admin.dashboard'))
            return render_template('admin_login.html', error_code=2)
        return render_template('admin_login.html', error_code=1)
    return render_template('admin_login.html', error_code=0)

# A tabular view of the database exclusively available to admins of the page!
@mod.route('/dashboard')
@login_required
def dashboard():
    user_data = current_admin.loadAllUsers()
    return render_template('dashboard.html', user_data=user_data, admin=current_admin.admin_username)

@mod.route('/logout')
@login_required
def logout():
    session.pop('admin_username')
    return redirect(url_for('admin.login'))