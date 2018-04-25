from flask import Blueprint, render_template, url_for, request, session, redirect
import bcrypt as hash_pass

mod = Blueprint('site', __name__, template_folder='templates')

from pymongo import MongoClient

client = MongoClient('mongodb://neverwannafly:Shubham123@ds151169.mlab.com:51169/chess_database')
db = client.chess_database # Establishes connection to mlab database!

@mod.route('/')
def index():
    if 'username' in session:
        return "<b>hello " + session['username']
    else:
        return "you aint logged in la!"

@mod.route('/register', methods=['GET', 'POST'])
def register():
    # if request.method=='POST':
    #     users = db.users
    #     existing_user = users.find_one({
    #         'username' : request.post['username']
    #     })
    #     existing_email = users.find_one({
    #         'email' : request.post['email']
    #     })
    #     if existing_email is None and existing_user is None:
    #         hash_password = hash_pass.hashpw(request.form['password'], hash_pass.gensalt())
            
    return  render_template('login.html')

