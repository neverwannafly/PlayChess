# Blog application could be accessed by both admins and the users!

import os

from flask import Blueprint, request, jsonify
from ..utils import token

import chess, chess.uci

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
            engine = chess.uci.popen_engine(os.path.join(__location__, 'stockfish-prod'))
            print("Found")
        else:
            engine = chess.uci.popen_engine(os.path.join(__location__, 'stockfish-dev'))
            print("Not Found")
        engine.uci()
        engine.ucinewgame()
        # Assign an info handler
        info_handler = chess.uci.InfoHandler()
        engine.info_handlers.append(info_handler)
        # Assign game Position
        try:
            fen_notation = request.args.get('fen_notation', "")
            engine.position(chess.Board(fen=fen_notation))
        except ValueError:
            return jsonify({
                "fen_notation_error": "Please supply a valid fen notation",
            })
        res = engine.go(movetime=1000)
        return jsonify({
            "best_move": res[0].__str__(), 
            "ponder": res[1].__str__(),
            "evaluation": {
                "centipawn_score": info_handler.info['score'][1][0],
                "mate_in": info_handler.info['score'][1][1],
            }
        })
    return jsonify({
        "access_token_error": "There seems to be a problem with your access token",
    })