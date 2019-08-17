# Blog application could be accessed by both admins and the users!

import os

from flask import Blueprint, request, jsonify
from ..utils import token
from ..config import Worker

import chess, chess.engine

mod = Blueprint('api', __name__)
clry = Worker.worker

## Api's
@mod.route('/gettoken/', methods=['GET'])
def getToken():
    return "token: hello"

@mod.route('/stockfish/', methods=['GET'])
def getEngineEval():
    if token.validate_token(request.args.get('token', False)):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __filename__ = 'stockfish-prod' if os.environ.get("Production", False) else 'stockfish-dev'

        # Assign game Position
        with chess.engine.SimpleEngine.popen_uci(os.path.join(__location__, __filename__)) as engine:
            try:
                fen_notation = request.args.get('fen_notation', "")
                board = chess.Board(fen_notation)
            except ValueError:
                return jsonify({
                    "fen_notation_error": "Please supply a valid fen notation",
                })
            strength = request.args.get('strength', 1)
            time = min(1, 0.01 * 10 ** int(strength))
            res = engine.play(board, chess.engine.Limit(time=time, depth=20))
            info = engine.analyse(board, chess.engine.Limit(time=time, depth=20))

            engine.close()

            return jsonify({
                "best_move": str(res.move), 
                "ponder": str(res.ponder),
                "evaluation": str(info["score"].white()),
            })
    return jsonify({
        "access_token_error": "There seems to be a problem with your access token",
    })

# Send start date and end date as the string "None" if you want to fetch all events
@mod.route('/events', methods=['GET'])
def getAicfEvents():
    pass

@mod.route('/long', methods=['GET'])
def long_task():
    i = _long_task.apply_async(args=[])
    return jsonify({"success": str(i)})

@clry.task
def _long_task():
    i = 0
    while i<100000000:
        i += 1
    return i