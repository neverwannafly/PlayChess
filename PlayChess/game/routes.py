import time

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta, datetime
from flask_socketio import send, emit

from ..utils import decorators, exceptions

# Import global variables
from ..config import *
from .. import socketio

mod = Blueprint('game', __name__, template_folder='templates')

## Game route
@mod.route('/<game_url>')
@decorators.login_required
def game(game_url):
    if GAMES.get(game_url):
        game = GAMES[game_url]
        game_title = "{0} vs {1}".format(game.player1, game.player2)
        board = game.chessboard.draw_chessboard()
        player1 = game.player1
        player2 = game.player2
        return render_template('game.html', game_title=game_title, board=board, player1=player1, player2=player2)
    raise exceptions.GameNotFound("This game doesn't exist!")

@mod.route('/<game_url>/makemove/<move>')
@decorators.login_required
def make_move(game_url, move):
    if GAMES.get(game_url):
        init_pos, final_pos = move.split('-')[0], move.split('-')[1]
        return GAMES[game_url].make_move(init_pos, final_pos, session.get('username'))
    raise exceptions.GameNotFound("This game doesn't exist!")

@mod.route('/<game_url>/generateLegalMoves/<init_pos>')
@decorators.login_required
def generate_legal_moves(game_url, init_pos):
    if GAMES.get(game_url):
        return GAMES[game_url].generate_legal_moves(init_pos, session.get('username'))
    raise exceptions.GameNotFound("This game doesn't exist!")

## Add a cryptographic id so that only server can dissolve games
## Something like /end/<server_id>/<game_url> or better yet 
## encrypt game urls.
@mod.route('/<game_url>/end')
@decorators.login_required
def end_game(game_url):
    if GAMES.get(game_url):
        player1 = GAMES[game_url].player1
        player2 = GAMES[game_url].player2
        USER_DICT['current_user_' + player1].in_game['status'] = False
        USER_DICT['current_user_' + player1].in_game['url'] = None
        USER_DICT['current_user_' + player2].in_game['status'] = False
        USER_DICT['current_user_' + player2].in_game['url'] = None
        GAMES.pop(game_url)
    raise exceptions.GameNotFound("This game doesn't exist!")

@socketio.on('user_connect', namespace='/game/marky-neverwannafly/')
def handle_connection(message):
    print(message)
    emit('user_connect', "Hello!")