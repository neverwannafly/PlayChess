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
db = database.db

# Make users to be logged in for 5 days!
@mod.before_app_first_request
def make_session_permanent():
    session.permanent = True
    mod.permanent_session_lifetime = timedelta(days=5)
    
@mod.before_app_first_request
def load_session_vars():
    if session.get('username'):
        USER_DICT['current_user_'+str(session['username'])] = site_user.loadUser(users, session['username'])[0]

@mod.before_request
def show_stats():
    print(CONTESTS)

### View functions start ###

@mod.route('/<contest_code>')
def main(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        cntst = contest.loadContest(db, contest_code)
        if cntst is None:
            return render_template('info.html', info='Contest Doesnt exist', title='404')
        else:
            CONTESTS[contest_code] = cntst
    return render_template('info.html', info=cntst.info, title=cntst.title)

@mod.route('/<contest_code>/start')
@decorators.login_required
def main_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        cntst = contest.loadContest(db, contest_code)
        if cntst is None:
            return url_for('contest.main')
        else:
            CONTESTS[contest_code] = cntst
    try:
        cntst.register_user(db, USER_DICT['current_user_'+str(session['username'])])
    except exceptions.ContestEnded:
        return render_template('info.html', info=cntst.info, title=cntst.title, error_code=1)
    return render_template('contest.html')

@mod.route('/<contest_code>/fetchPuzzle')
@decorators.login_required
def fetch_puzzle(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    print(cntst, "Hello")
    if cntst is None:
        return jsonify({'success': False})
    puzzle_index = request.args.get('index', 0)
    puzzle = cntst.get_puzzle(db, int(puzzle_index), USER_DICT['current_user_'+str(session['username'])])
    USER_DICT['current_user_'+str(session['username'])].puzzle = puzzle
    color = USER_DICT['current_user_'+str(session['username'])].puzzle.board.check_color()
    if color==1:
        board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_black()
    else:
        board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_white()
    return jsonify({'success': True, 'board': board})

@mod.route('/<contest_code>/makemove/<move>')
def make_move(contest_code, move):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    puzzle = USER_DICT['current_user_'+str(session['username'])].puzzle
    squares = move.split('-')
    dest_square = squares[2] if len(squares)==3 else None
    try:
        move_info = puzzle.make_move(squares[0], squares[1], dest_square)
    except exceptions.InvalidMoveError as error:
        return jsonify({'move': False})
    except exceptions.SideNotAuthorizedToMakeMove as error:
        return jsonify({
            'move': False,
            'auth': False,
            })
    return jsonify({
        'move': True,
        'move_info': move_info,
    })

@mod.route('/<contest_code>/generateLegalMoves/<init_pos>')
def generate_legal_moves(contest_code, init_pos):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    puzzle = USER_DICT['current_user_'+str(session['username'])].puzzle
    try:
        moves = puzzle.generate_legal_moves(init_pos)
    except exceptions.SideNotAuthorizedToMakeMove as error:
        return jsonify({'moves': []})
    return jsonify({'moves': moves})

@mod.route('/<contest_code>/end_contest')
@decorators.login_required
def end_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    cntst.finish_user_session(USER_DICT['current_user_' + str(session['username'])])
    USER_DICT['current_user_' + str(session['username'])].puzzle = None
    return jsonify({'success': True})
    