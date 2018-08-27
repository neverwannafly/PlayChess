### IMPORTANT NOTE ###
# Admins should only be created through command line!
import random

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
import bcrypt as hash_pass
import re as regex

from datetime import timedelta

mod = Blueprint('admin', __name__, template_folder='admin_templates')

from .admins import Admin, loadAdmin
from .decorators import login_required, logout_required
# Import global vars
from ..config import ADMIN_DICT, EMAIL_PATTERN_COMPILED, USERNAME_REGEX, TERMINAL_COLORS

from .. import database
db = database.db

@mod.before_app_first_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)
    if session.get('admin_username'):
        ADMIN_DICT['current_admin_'+str(session['admin_username'])] = loadAdmin(db, session['admin_username'])

@mod.before_request
def init():
    print(
        TERMINAL_COLORS['CYELLOW'] + 
        TERMINAL_COLORS['CBOLD'] + 
        ADMIN_DICT + 
        TERMINAL_COLORS['CEND'] + 
        TERMINAL_COLORS['CEND']
    )

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
    current_admin.loadAllUsers()
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
    ADMIN_DICT.pop('current_admin_'+str(session['admin_username']))
    session.pop('admin_username')
    return redirect(url_for('admin.login'))
