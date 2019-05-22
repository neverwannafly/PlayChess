# Blog application could be accessed by both admins and the users!

import os

from flask import Blueprint, request, jsonify
from ..utils import token

import chess, chess.engine

mod = Blueprint('api', __name__)

## Api's
@mod.route('/gettoken/', methods=['GET'])
def gettoken():
    return "token: hello"

@mod.route('/bestmove/', methods=['GET'])
def index():
    if token.validate_token(request.args.get('token', None)):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        if os.environ.get("Production", None):
            engine = chess.engine.SimpleEngine.popen_uci(os.path.join(__location__, 'stockfish-prod'))
        else:
            engine = chess.engine.SimpleEngine.popen_uci(os.path.join(__location__, 'stockfish-dev'))
        # Assign game Position
        try:
            fen_notation = request.args.get('fen_notation', "")
            board = chess.Board(fen_notation)
        except ValueError:
            return jsonify({
                "fen_notation_error": "Please supply a valid fen notation",
            })
        res = engine.play(board, chess.engine.Limit(time=1, depth=20))
        info = engine.analyse(board, chess.engine.Limit(time=1, depth=20))

        return jsonify({
            "best_move": str(res.move), 
            "ponder": str(res.ponder),
            "evaluation": str(info["score"]),
        })
    return jsonify({
        "access_token_error": "There seems to be a problem with your access token",
    })