# Blog application could be accessed by both admins and the users!

from flask import Blueprint, session
from functools import wraps

mod = Blueprint('blog', __name__, template_folder='blog_templates')

from .. import database
db = database.db

# initiate below references to required database entities such as posts, comments etc.

# Define decorators so both admin and users can access the blog!
# All the views here are strictly to be under login_required!
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        admin_username = session.get('admin_username')
        user_username = session.get('username')
        if admin_username:
            # Do something!
            pass
        elif user_username:
            # Do something!
            pass
        else:
            # Do something!
            pass
    return wrapper


### View functions ###
@mod.route('/')
def index():
    return "this would become a really good blog!"