import time
import random

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta, datetime

import bcrypt as hash_pass
import re as regex

mod = Blueprint('site', __name__, template_folder='templates')

USER_DICT = {

}

GAMES = {

}

# Regex expression for email and username verification
EMAIL_PATTERN_COMPILED = regex.compile("^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")
# Username regex also limits the string to be b/w 5 and 30!
USERNAME_REGEX = regex.compile("^[a-zA-Z0-9_]{5,30}$")

# Relative imports
from .game import Game
from .users import User, addNewUserToDatabase, loadUser
from .decorators import login_required, logout_required
from .game_queue import GameQueue
from .. import database
from .. import config

from .exceptions import InvalidMoveError

# Keeps track of players finding matches.
PLAYERS_QUEUE = GameQueue()

# Database initialisation
db = database.db
users = db.users # object pointing to users database!

# Make users to be logged in for 5 days!
@mod.before_app_first_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)
    
@mod.before_app_first_request
def load_user_from_session():
    if session.get('username'):
        USER_DICT['current_user_'+str(session['username'])] = loadUser(users, session['username'])[0]

@mod.before_request
def init():
    print(USER_DICT)
    print(GAMES)

### View functions start ###

@mod.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method=='POST':
        user = loadUser(users, request.form['username'])
        if user[0] and user[1]==1:
            if hash_pass.hashpw(request.form['password'].encode('utf-8'), user[0].password)==user[0].password:
                session['username'] = request.form['username']
                USER_DICT['current_user_' + str(session['username'])] = user[0]
                return redirect(url_for('site.index'))
            else:
                return render_template('login.html', error_code=-3, script=None)
        elif user[1]==0:
            return redirect(url_for('site.verify', username=user[0].username))
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

    valid_email = bool(regex.match(EMAIL_PATTERN_COMPILED, request.form['email']))
    valid_username = bool(regex.match(USERNAME_REGEX, request.form['username']))

    if valid_email and valid_username:
        existing_user = users.find_one({
            'username' : request.form['username']
        })
        existing_email = users.find_one({
            'email' : request.form['email']
        })
        if existing_email is None and existing_user is None:
            if request.form['password']==request.form['confirm_password']:
                # Code to randomly assign an image for the user! 
                # Later add an interface for the users to be able to select their own profile pictures!
                random_image = "/static/Images/profile_pics/" + str(random.randint(1, 17)) + ".png"
                hash_password = hash_pass.hashpw(request.form['password'].encode('utf-8'), hash_pass.gensalt())
                # This method adds an user to database and sends a verification mail!
                addNewUserToDatabase(
                    request.form['username'], 
                    hash_password, 
                    request.form['email'], 
                    random_image, 
                    request.form['first_name'], 
                    request.form['last_name'], 
                    users,
                )
                current_user = loadUser(users, request.form['username'])[0]
                #Send email verification
                response = mailing.sendMail(current_user._id, current_user.email, current_user.username)
                if response:
                    return redirect(url_for('site.verify', username=current_user.username))
                else:
                    return render_template('login.html', error_code=6, script=script)
            return render_template('login.html', error_code=5, script=script)
        elif existing_email:
            return render_template('login.html', error_code=4, script=script)
        return render_template('login.html', error_code=3, script=script)
    elif valid_email is None:
        return render_template('login.html', error_code=2, script=script)
    return render_template('login.html', error_code=1, script=script)

# Link user for verification!
@mod.route('/verify/<username>', methods=['GET', 'POST'])
@logout_required
def verify(username):
    current_user = loadUser(users, username)[0]
    if request.method=='POST':
        if request.form['activation_link'].strip(' ')==current_user._id:
            session['username'] = current_user.username
            current_user.updateUserVerificationStatus()
            USER_DICT['current_user_' + str(session['username'])] = current_user
            return redirect(url_for('site.index'))
        return render_template('verify.html', username=username ,error_code=1)
    return render_template('verify.html', username=username, error_code=0)

# Route to resend verification mail to user
@mod.route('/verify/<username>/retry', methods=["POST"])
@logout_required
def retry(username):
    current_user = loadUser(users, username)[0]
    response = mailing.sendMail(current_user._id, current_user.email, current_user.username)
    return jsonify({response: response})

## Index Page

@mod.route('/')
@login_required
def index():
    new_chess_board = USER_DICT['current_user_' + str(session['username'])].chessboard.draw_chessboard()
    current_user = USER_DICT['current_user_' + str(session['username'])]
    return render_template('index.html', user=current_user, board=new_chess_board)

@mod.route('/board/flip')
@login_required
def flipBoard():
    USER_DICT['current_user_' + str(session['username'])].chessboard.swap_board()
    flipped_board = USER_DICT['current_user_' + str(session['username'])].chessboard.draw_chessboard()
    return jsonify({"board": flipped_board})

@mod.route('/board/reset')
@login_required
def resetBoard():
    USER_DICT['current_user_' + str(session['username'])].chessboard.reset_chessboard()
    reset_board = USER_DICT['current_user_' + str(session['username'])].chessboard.draw_chessboard()
    return jsonify({"board": reset_board})

@mod.route('/generateLegalMoves/<init_pos>')
@login_required
def generateLegalMoves(init_pos):
    moves = USER_DICT['current_user_' + str(session['username'])].chessboard.generate_legal_moves(init_pos);
    return jsonify({'moves': moves})

@mod.route('/makemove/<move>')
@login_required
def make_move(move):
    positions = move.split('-')
    try:
        changes = USER_DICT['current_user_' + str(session['username'])].chessboard.make_move(positions[0], positions[1])
    except InvalidMoveError as error:
        print(error)
        return jsonify({'success': False})
    return jsonify({
        'success': True,
        'changes': changes,
    })

# Handle game loading here
@mod.route('/find/game')
@login_required
def find_players():
    if not USER_DICT['current_user_' + str(session['username'])].in_game['status']:
        make_game(session)
        end_time = (datetime.now() + timedelta(seconds=10)).time()
        while end_time >= datetime.now().time():
            game = get_game(session)
            if game:
                USER_DICT['current_user_' + str(session['username'])].in_game['status'] = True
                USER_DICT['current_user_' + str(session['username'])].in_game['url'] = game
                return jsonify({"url": game})
            time.sleep(1)
        return jsonify({"url": None})
    url = USER_DICT['current_user_' + str(session['username'])].in_game['url']
    return jsonify({"url": url})

# logout routine
@mod.route('/logout')
@login_required
def logout():
    USER_DICT.pop('current_user_' + str(session['username']))
    session.pop('username')
    return redirect(url_for('site.login'))

## Helper functions
def make_game(session):
    if session.get('username'):
        username = session['username']
        while True:
            message = PLAYERS_QUEUE.add_to_queue(username)
            PLAYERS_QUEUE.print_queue()
            if message.code:
                if not GAMES.get(message) and message.info:
                    GAMES[message.info] = Game(message.info)
                break
            time.sleep(1)

def get_game(session):
    username = session.get('username')
    print(username)
    game = [games for games in GAMES if username in games]
    if len(game) is not 1:
        return None
    return game[0]
        
        
