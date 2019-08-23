from .chessboard import Chessboard
from ..config import Worker

clry = Worker.worker

class Puzzle:
    def __init__(puzzle_obj):
        self._id = puzzle_obj.id
        self.attemps = puzzle_obj.attempts
        self.solved = puzzle_obj.solved
        self.rating = puzzle_obj.rating
        self.public = puzzle_obj.public
        self.start_pos = puzzle_obj.start_pos
        self.solution = puzzle_obj.solution
        self.moves = 0
        self.tags = puzzle_obj.tags
        self.board = Chessboard(puzzle_obj.start_pos)

    def get_board(self):
        return self.board.draw_chessboard_for_white()

    def generate_legal_moves(self, initial_pos):
        return self.board.generate_legal_moves(initial_pos)

    def make_move(self, initial_pos, final_pos, dest_piece=None):
        res = { changes: [], success: False, puzzleOver: False }

        res.changes.append(self.board.make_move(initial_pos, final_pos, dest_piece=dest_piece))
        notation = initial_pos + "-" + final_pos if dest_piece is None else initial_pos + "-" + final_pos + "-" + dest_piece

        if self.moves < len(self.solution) and self.solution[self.moves] ==  notation:
            self.moves += 1
            res['changes'].append(self.board.make_move(self.solution[self.moves]))
            res['success'] = True
        elif self.moves == len(self.solution):
            res['puzzleOver'] = True
        return res

    def getScore():
        return self.moves / len(self.solution)

def pushPuzzleResult(db_object, puzzle_id, username, result):
    puzzle = db_object.puzzle.update_one(
        {'_id': puzzle_id},
        {'$inc': {
            "attempts": 1,
            "solved": result,
        }}
    )
    db_object.users.update_one(
        {'username': username},
        {"$push": {"puzzles": {
                "_id" : puzzle.updated_id,
                "success": result,
            }
        }}
    )

def addTag(db_object, puzzle_id, tag):
    db_object.update_one(
        {'_id': puzzle_id},
        {"$push": {'tags': tag}},
    )

def createPuzzle(db_object, start_pos, solution, tags=[]):
    db_object.puzzle.insert_one({
        'attempts': 0,
        'solved': 0,
        'rating': 1200,
        'public': False,
        'start_pos': start_pos,
        'solution': solution,
        'tags': tags
    })

def fetch_puzzle(db_object, puzzle_id):
    puzzle = db_object.puzzle.find_one(
        {'_id': puzzle_id}
    )
    return Puzzle(puzzle)