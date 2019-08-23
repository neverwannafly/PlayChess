import time
import random

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta, datetime

import bcrypt as hash_pass
import re as regex

mod = Blueprint('contest', __name__, template_folder='contest_templates')

# Relative imports
from ..utils import site_user
from ..utils import exceptions
from ..utils import decorators
from ..utils import contest
from ..utils import puzzle

# Import global variables and settings
from ..config import CONTESTS, USER_DICT

# Database initialisation
from .. import database

# Make users to be logged in for 5 days!
@mod.before_app_first_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)
    
@mod.before_app_first_request
def load_user_from_session():
    if session.get('username'):
        USER_DICT['current_user_'+str(session['username'])] = site_user.loadUser(users, session['username'])[0]

@mod.before_request
def show_stats():
    pass

### View functions start ###

@mod.route