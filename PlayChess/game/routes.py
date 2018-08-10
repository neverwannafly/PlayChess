import time

from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta, datetime
from flask_socketio import send

from .game import Game, get_game, make_game
from ..utils import decorators

# Import global variables
from ..config import *
from .. import socketio

mod = Blueprint('game', __name__, template_folder='templates')

# Handle game loading here
@mod.route('/find')
@decorators.login_required
def find_players():
    if not USER_DICT['current_user_' + str(session['username'])].in_game['status']:
        make_game(session, PLAYERS_QUEUE, GAMES)
        end_time = (datetime.now() + timedelta(seconds=10)).time()
        while end_time >= datetime.now().time():
            game = get_game(session, GAMES)
            if game:
                USER_DICT['current_user_' + str(session['username'])].in_game['status'] = True
                USER_DICT['current_user_' + str(session['username'])].in_game['url'] = game
                return jsonify({"url": game})
            time.sleep(1)
        PLAYERS_QUEUE.remove(session['username'])
        return jsonify({"url": None})
    url = USER_DICT['current_user_' + str(session['username'])].in_game['url']
    return jsonify({"url": url})

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
    return jsonify({"BAD_EXCESS": "ABORT 404"})

