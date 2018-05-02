from flask import Blueprint, render_template, url_for, request, session, redirect
from datetime import timedelta
from functools import wraps
import bcrypt as hash_pass
import re as regex
import random

mod = Blueprint('site', __name__, template_folder='templates')

# Regex expression for email verification
EMAIL_PATTERN_COMPILED = regex.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")

# Relative imports
from .. import database
from . import classes

# Database initialisation
db = database.db
users = db.users # object pointing to users database!

obj = users.find_one({
    'username':'neverwannafly'
})

#initialises a class object, current user that can load, update, read and delete a user data!
current_user = classes.User(users)

# Custom login_required decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
            # if there's a user in session, set the current_user to that user!
            current_user.loadUser(session['username'])
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('site.login'))
    return wrapper

# logout required decorator to access register and login page!
def logout_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
            return redirect(url_for('site.index'))
        else:
            return view_function(*args, **kwargs)
    return wrapper

# Make users to be logged in for 5 days!
@mod.before_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)

### View functions start ###

@mod.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@mod.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method=='POST':
        isLoadSuccessful = current_user.loadUser(request.form['username'].lower())
        if isLoadSuccessful==1:
            if hash_pass.hashpw(request.form['password'], current_user.password)==current_user.password:
                session['username'] = request.form['username'].lower()
                return redirect(url_for('site.index'))
            else:
                return render_template('login.html', error_code=-3, script=None)
        elif isLoadSuccessful==0:
            return redirect(url_for('site.verify', username=current_user.username))
        return render_template('login.html', error_code=-1, script=None)
    return render_template('login.html', error_code=0, script=None)

from . import mailing

@mod.route('/register', methods=['POST'])
@logout_required
def register():
    # Script adds a little js code to login.html so as in to keep registration form
    # in view after template is rendered again due to invalid register attempt!
    script = """
    <script>
        $(document).ready(function(){
            $("#register-form").show();
            $("#login-form").hide();
        })
    </script>
    """
    existing_user = users.find_one({
        'username' : request.form['username'].lower()
    })
    existing_email = users.find_one({
        'email' : request.form['email']
    })
    if existing_email is None and existing_user is None:
        valid_email = bool(regex.match(EMAIL_PATTERN_COMPILED, request.form['email']))
        if valid_email:
            if request.form['password']==request.form['confirm_password']:
                # Code to randomly assign an image for the user! 
                # Later add an interface for the users to be able to select their own profile pictures!
                random_image = "{{ url_for('static', filename='Images/" + str(random.randint(1, 17)) + ".png') }}"
                hash_password = hash_pass.hashpw(request.form['password'], hash_pass.gensalt())
                # This method adds an user to database and sends a verification mail!
                response = current_user.addNewUserToDatabase(
                    request.form['username'].lower(), 
                    hash_password, 
                    request.form['email'], 
                    random_image, 
                    request.form['first_name'], 
                    request.form['last_name'], 
                )
                #Send email verification
                response = mailing.sendMail(current_user._id, current_user.email, current_user.username)
                if response:
                    return redirect(url_for('site.verify', username=current_user.username))
                else:
                    current_user.deleteUser()
                    return render_template('login.html', error_code=5, script=script)
            else:
                return render_template('login.html', error_code=4, script=script)
        else:
            return render_template('login.html', error_code=3, script=script)
    elif existing_email:
        return render_template('login.html', error_code=2, script=script)
    elif existing_user:
        return render_template('login.html', error_code=1, script=script)

# Link user for verification!
@mod.route('/verify/<username>', methods=['GET', 'POST'])
@logout_required
def verify(username):
    if request.method=='POST':
        current_user.updateUserVerificationStatus(username)
        if request.form['activation_link']==current_user._id:
            session['username'] = current_user.username
            return redirect(url_for('site.index'))
        return render_template('verify.html', username=username ,error_code=1)
    return render_template('verify.html', username=username, error_code=0)

# logout routine
@mod.route('/logout')
@login_required
def logout():
    session.pop('username')
    return redirect(url_for('site.login'))