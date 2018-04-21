from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import InputRequired, Length
from wtforms import StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime
from markupsafe import Markup

from os.path import abspath
from os import getcwd

app = Flask(__name__)

file_path = abspath(getcwd()) + '/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SECRET_KEY'] = 'Secret_Key'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Yay!"

if __name__=='__main__':
    app.run(debug=True)