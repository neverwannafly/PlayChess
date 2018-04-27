from flask import Blueprint, render_template, url_for, request, session, redirect
import bcrypt as hash_pass
import re as regex

mod = Blueprint('site', __name__, template_folder='templates')

# Regex expression for email verification!
EMAIL_PATTERN_COMPILED = regex.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")

# Relative imports!
from .. import database
from . import classes

#initialisation
db = database.db
users = db.users # object pointing to users database!

# Custom login_required decorator!

@mod.route('/')
def index():
    return "You're in"

@mod.route('/login', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        existing_user = users.find_one({
            'username' : request.form['username']
        })
        existing_email = users.find_one({
            'email' : request.form['email']
        })
        if existing_email is None and existing_user is None:
            valid_email = bool(regex.match(EMAIL_PATTERN_COMPILED, request.form['email']))
            if valid_email:
                if request.form['password']==request.form['confirm_password']:
                    random_image = "use a random_image_url_generator!"
                    hash_password = hash_pass.hashpw(request.form['password'], hash_pass.gensalt())
                    new_user = classes.User(request.form['username'], hash_password, request.form['email'], random_image, request.form['first_name'], request.form['last_name'], 1200, users)
                    new_user.addUserToDatabase()
                    session['username'] = request.form['username']
                    return redirect(url_for('site.index'))
                else:
                    return render_template('login.html', error_code=4)
            else:
                return render_template('login.html', error_code=3)
        elif existing_email:
            return render_template('login.html', error_code=2)
        elif existing_user:
            return render_template('login.html', error_code=1)

    return render_template('login.html', error_code=0)

@mod.route('/login', methods=['POST'])
def login():
    find_user = users.find_one({
        'username' : request.form['username'],
        'password' : request.form['password']
    })
    if find_user:
        session['username'] = request.form['username']
        return redirect(url_for('site.index'))
    else: 
        return render_template('login.html', error_code=-1)

@mod.route('logout')
def logout():
    session.pop('username')
    return redirect(url_for('site.register'))