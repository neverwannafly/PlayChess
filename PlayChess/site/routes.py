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

@mod.route('/')
def index():
    return "You're in"

@mod.route('/login')
def login():
    if 'username' in session:
        return "<b>hello " + session['username']
    else:
        return "you aint logged in la!"

@mod.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        users = db.users
        existing_user = users.find_one({
            'username' : request.post['username']
        })
        existing_email = users.find_one({
            'email' : request.post['email']
        })
    
        if existing_email is not None and existing_user is not None:
            valid_email = bool(regex.match(EMAIL_PATTERN_COMPILED, request.post['email']))
            if valid_email:
                random_image = "use a random_image_url_generator!"
                hash_password = hash_pass.hashpw(request.form['password'], hash_pass.gensalt())
                new_user = classes.User(request.post['username'], hash_password, request.post['email'], random_image, request.post['first_name'], request.post['last_name'], 1200)
                new_user.addUserToDatabase()
                session['username'] = request.post['username']
                return redirect(index)
            else:
                return render_template('login.html', error_code=3)
        elif existing_email is None:
            return render_template('login.html', error_code=1)
        elif existing_user is None:
            return render_template('login.html', error_code=2)

    return render_template('login.html', error_code=0)

