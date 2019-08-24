from flask import session, redirect, url_for
from functools import wraps

from ..config import TERMINAL_COLORS

# Custom login_required decorator
def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if username:
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

def deprecated(func):
    @wraps(func)
    def wrapper(*args):
        print(
            TERMINAL_COLORS['CYELLOW'] +  
            TERMINAL_COLORS['CBOLD'] + 
            "This method has been deprecated" + 
            TERMINAL_COLORS['CEND'] + 
            TERMINAL_COLORS['CEND']
        )
        return func(args[0])
    return wrapper

def disable(func):
    @wraps(func)
    def wrapper(*args):
        return None
    return wrapper