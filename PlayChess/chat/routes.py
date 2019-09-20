from flask import Blueprint, render_template
from flask_socketio import emit

mod = Blueprint('chat', __name__, template_folder='templates')

from .. import socketio

@mod.route('/')
def message():
    return render_template('global-chat.html')

@socketio.on('send_message', namespace='/chat/')
def handle_message(msg):
    print('Message: ' + msg)
    emit('send_message', msg, broadcast=True)