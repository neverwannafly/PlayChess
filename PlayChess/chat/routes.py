from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
from flask_socketio import send

mod = Blueprint('chat', __name__, template_folder='templates')

from .. import socketio

@mod.route('/')
def message():
    return render_template('global-chat.html')

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)