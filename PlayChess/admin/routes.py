### IMPORTANT NOTE ###
# Admins should only be created through command line!

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
import bcrypt as hash_pass
from functools import wraps
import re as regex
import random

mod = Blueprint('admin', __name__, template_folder='admin_templates')

# Global admin dict to keep track of admins
ADMIN_DICT = {

}

# regex to verify email addresses and usernames!
EMAIL_PATTERN_COMPILED = regex.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")
USERNAME_REGEX = regex.compile("^[a-zA-Z0-9_]{5,30}$")

from .. import database
db = database.db

from .classes import Admin, loadAdmin

# login_required and logout_required decorators that ensure certain url's confront to 
# respective wanted behaviors!

# Custom login_required decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        if admin_username:
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

@mod.before_app_first_request
def get_admin():
    if session.get('admin_username'):
        ADMIN_DICT['current_admin_'+str(session['admin_username'])] = loadAdmin(db, session['admin_username'])

@mod.before_request
def init():
    print(ADMIN_DICT)

@mod.route('/', methods=['POST', 'GET'])
@logout_required
def login():
    if request.method=='POST':
        current_admin = loadAdmin(db, request.form['admin_username'])
        if current_admin:
            if hash_pass.hashpw(request.form['admin_password'].encode('utf-8'), current_admin.admin_password)==current_admin.admin_password:
                session['admin_username'] = current_admin.admin_username
                ADMIN_DICT['current_admin_'+str(session['admin_username'])] = current_admin
                return redirect(url_for('admin.dashboard'))
            return render_template('admin_login.html', error_code=2)
        return render_template('admin_login.html', error_code=1)
    return render_template('admin_login.html', error_code=0)

# A tabular view of the database exclusively available to admins of the page!
@mod.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    current_admin = ADMIN_DICT['current_admin_'+str(session['admin_username'])]
    return render_template('dashboard.html', error_code=0, admin=current_admin.admin_username)

@mod.route('/table')
@login_required
def table():
    current_admin = ADMIN_DICT['current_admin_'+str(session['admin_username'])]
    user_data = current_admin.loadAllUsers()
    return render_template('table.html', user_data=user_data)

@mod.route('/add', methods=['POST'])
@login_required
def add():
    current_admin = ADMIN_DICT['current_admin_'+str(session['admin_username'])]
    user_data = current_admin.loadAllUsers()
    if bool(regex.match(EMAIL_PATTERN_COMPILED, request.form['email'])) and bool(regex.match(USERNAME_REGEX, request.form['username'])):
        isUserInsertionSuccessful = current_admin.createUser(
            request.form['username'],
            hash_pass.hashpw(request.form['password'].encode('utf-8'), hash_pass.gensalt()),
            request.form['email'],
            "/static/Images/profile_pics/" + str(random.randint(1, 17)) + ".png",
            request.form['first_name'],
            request.form['last_name']
        )
        if isUserInsertionSuccessful:
            return redirect(url_for('admin.dashboard'))
        return render_template('dashboard.html', error_code=2, admin=current_admin.admin_username)
    return render_template('dashboard.html', error_code=1, admin=current_admin.admin_username)

@mod.route('/delete', methods=['POST'])
@login_required
def delete():
    current_admin = ADMIN_DICT['current_admin_'+str(session['admin_username'])]
    current_admin.deleteUser(request.form['username'])
    return redirect(url_for('admin.table'))

@mod.route('/update', methods=['POST'])
@login_required
def update():
    current_admin = ADMIN_DICT['current_admin_'+str(session['admin_username'])]
    current_admin.updateUserDetails(
        request.form["username"], 
        request.form["email"], 
        "/static/Images/profile_pics/" + str(request.form["image"]), 
        request.form["name"].split(' ')[0], 
        request.form["name"].split(' ')[1],
        request.form["rating"],
        request.form["authentication"]
    )
    return jsonify({
        "name": str(request.form["name"].split(' ')[0]) + " " + str(request.form["name"].split(' ')[1]),
        "username": request.form["username"],
        "email": request.form["email"],
        "rating": request.form["rating"],
        "image": request.form["image"],
        "authentication": request.form["authentication"], 
    })

@mod.route('/logout')
@login_required
def logout():
    session.pop('admin_username')
    ADMIN_DICT.pop('current_admin_'+str(session['admin_username']))
    return redirect(url_for('admin.login'))
