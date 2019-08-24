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
    pass

### View functions start ###

@mod.route('/<contest_code>')
@decorators.login_required
def main(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        cntst = contest.loadContest(db, contest_code)
        if cntst is None:
            return render_template('info.html', info='Contest Doesnt exist', title='404')
        else:
            CONTESTS[contest_code] = cntst
    return render_template('info.html', info=cntst.info, title=cntst.title)

@mod.route('/<contest_code>/register')
@decorators.login_required
def register_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        cntst = contest.loadContest(db, contest_code)
        if cntst is None:
            return jsonify({'error': 'contest not found!'})
        else:
            CONTESTS[contest_code] = cntst
    if not cntst.has_user_session_ended(USER_DICT['current_user_'+str(session['username'])]):
        redirect(url_for('contest.main_contest', contest_code=contest_code))
    try:
        cntst.register_user(db, USER_DICT['current_user_'+str(session['username'])])
    except exceptions.ContestEnded:
        return render_template('info.html', info=cntst.info, title=cntst.title, error_code=1)
    return redirect(url_for('contest.main_contest', contest_code=contest_code))

@mod.route('/<contest_code>/start')
@decorators.login_required
def main_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        cntst = contest.loadContest(db, contest_code)
        if cntst is None:
            return jsonify({'error': 'contest not found!'})
        else:
            CONTESTS[contest_code] = cntst
    if cntst.has_user_session_ended(USER_DICT['current_user_'+str(session['username'])]):
        return render_template('info.html', info=cntst.info, title=cntst.title, error_code=1)
    return render_template('contest.html', title=cntst.title)

@mod.route('/<contest_code>/fetchPuzzle')
@decorators.login_required
def fetch_puzzle(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    if USER_DICT['current_user_'+str(session['username'])].puzzle is not None:
        color = USER_DICT['current_user_'+str(session['username'])].puzzle.board.check_color()
        if color==1:
            board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_white()
        else:
            board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_black()
        return jsonify({'success': True, 'board': board})
    puzzle_index = request.args.get('index', 0)
    puzzle = cntst.get_puzzle(db, int(puzzle_index), USER_DICT['current_user_'+str(session['username'])])
    if puzzle is None:
        return jsonify({'contest_ended': True})
    USER_DICT['current_user_'+str(session['username'])].puzzle = puzzle
    color = USER_DICT['current_user_'+str(session['username'])].puzzle.board.check_color()
    if color==1:
        board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_white()
    else:
        board = USER_DICT['current_user_'+str(session['username'])].puzzle.board.draw_chessboard_for_black()
    return jsonify({'success': True, 'board': board})

@mod.route('/<contest_code>/makemove/<move>')
def make_move(contest_code, move):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'move': False})
    puzzle = USER_DICT['current_user_'+str(session['username'])].puzzle
    index = int(request.args.get('index'))
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
    success = move_info['success']
    puzzleOver = move_info['puzzleOver']
    changes = move_info['changes']

    if puzzleOver and success:
        score = puzzle.get_score()
        cntst.submit_ans(db, index, USER_DICT['current_user_'+str(session['username'])], score)
        USER_DICT['current_user_'+str(session['username'])].puzzle = None
        return jsonify({'move': True, 'success': True, 'puzzleOver': True, 'changes': changes})
    
    if success:
        return jsonify({'move': True, 'success': True, 'puzzleOver': False, 'changes': changes})
        
    score = puzzle.get_score()
    cntst.submit_ans(db, index, USER_DICT['current_user_'+str(session['username'])], score)
    USER_DICT['current_user_'+str(session['username'])].puzzle = None
    return jsonify({'move': True, 'success': False, 'puzzleOver': True, 'changes': changes})


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

@mod.route('/<contest_code>/leaderboards')
def get_leaderboards(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    data = cntst.players
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    rankings = [{'name': rank[0], 'team': 'DTU', 'gap': round(rank[1], 2)} for rank in sorted_data]
    return render_template('leaderboard.html', rankings=rankings, title=cntst.title)

@mod.route('/<contest_code>/end_contest')
@decorators.login_required
def end_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    cntst.finish_user_session(db, contest_code, USER_DICT['current_user_' + str(session['username'])])
    USER_DICT['current_user_' + str(session['username'])].puzzle = None
    return jsonify({'success': True})
    
@mod.route('/<contest_code>/finish_contest')
@decorators.login_required
def finish_contest(contest_code):
    cntst = CONTESTS.get(contest_code, None)
    if cntst is None:
        return jsonify({'success': False})
    cntst.end_contest(db)
    USER_DICT['current_user_' + str(session['username'])].puzzle = None
    return jsonify({'success': True})