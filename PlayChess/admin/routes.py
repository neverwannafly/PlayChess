from flask import Blueprint, render_template, url_for, request, session, redirect
import bcrypt as hash_pass

mod = Blueprint('admin', __name__, template_folder='admin_templates')

from .. import database
db = database.db

from . import classes
current_admin = classes.Admin(db) # initialise an admin object!

# login_required and logout_required decorators that ensure certain url's confront to 
# respective wanted behaviors!

# Custom login_required decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        if admin_username:
            # if there's a user in session, set the current_user to that user!
            current_admin.loadAdmin(session['admin_username'])
            return view_function(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return wrapper

# logout required decorator to access register and login page!
def logout_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        if admin_username:
            return redirect(url_for('admin.dashboard'))
        else:
            return view_function(*args, **kwargs)
    return wrapper


# Make users to be logged in for 5 days!
@mod.before_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)

@mod.route('/', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        if admin.loadAdmin(request.form['admin_username'].lower()):
            
        return render_template('admin_login.html', error_code=1)
    return render_template('admin_login.html', error_code=0)

# A tabular view of the database exclusively available to admins of the page!
@mod.route('/dashboard')
def dashboard():
    return "you're in !"