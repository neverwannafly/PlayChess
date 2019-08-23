from .puzzle import fetch_puzzle, Puzzle, updatePuzzleResult
from .exceptions import ContestEnded

class Contest:
    def __init__(self, contest_obj):
        self._id = contest_obj._id
        self.puzzles = contest_obj.puzzles
        self.players = contest_obj.players
        self.date = contest_obj.date
        self.time = contest_obj.time
        self.info = ""
        self.title = ""

    def update_details(self, info, title):
        self.info = info
        self.title = title

    def register_user(self, db_object, username):
        user.in_contest['status'] = True
        user.in_contest['contest_id'] = self._id
        register_player(db_object, self._id, username)

    def finish_user_session(self, user):
        user.in_contest['status'] = False
        user.in_contest['contest_id'] = None

    def has_user_session_ended(self, user):
        return user.in_contest['status']==True and user.in_contest['contest_id']==self._id

    def get_puzzle(self, puzzle_index, user):
        if self.has_user_session_ended(user):
            return Puzzle(fetch_puzzle(self.puzzles[puzzle_index])).get_board()
        return None

    def submit_ans(self, user, puzzle_index, score):
        if self.has_user_session_ended(user):

            update_puzzle_score()
            return {'success': True}
        return {'success': False}

def update_puzzle_score(db_object, contest_code, puzzle_id, username, score):
    key = 'players. + username'
    db_object.contest.update_one(
        {'_id': contest_code},
        {'$inc': {
            key: score,
        }}
    )
    updatePuzzleResult(db_object, puzzle_id, username, score)

def register_player(db_object, contest_code, username):
    key = 'players.' + username
    db_object.contest.update_one(
        {'_id': contest_code},
        {'$set': {
            key: 0,
        }}
    )

def loadContest(db_object, contest_code):
    contest = db_object.contests.find_one({
        'contest_code': contest_code,
    })
    if contest is None:
        return None
    return Contest(contest)

def create_contest(db_object, contest_code, puzzles, date, time):
    db_object.contest.insert_one({
        '_id': contest_code,
        'players': {},
        'puzzles': puzzles,
        'date': date,
        'time': time,
    })