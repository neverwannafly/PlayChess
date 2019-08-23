from .puzzle import fetch_puzzle, Puzzle, pushPuzzleResult, createPuzzle
from .exceptions import ContestEnded

class Contest:
    def __init__(self, contest_obj):
        self._id = contest_obj['_id']
        self.puzzles = contest_obj['puzzles']
        self.players = contest_obj['players']
        self.date = contest_obj['date']
        self.time = contest_obj['time']
        self.info = contest_obj['info']
        self.title = contest_obj['title']

    def update_details(self, db_object, info, title):
        self.info = info
        self.title = title
        db_object.contest.update_one(
            {'_id': self._id},
            {'$set': {
                'info': info,
                'title': title,
            }}
        )

    def register_user(self, db_object, user):
        plyr = db_object.contest.find_one(
            {'players': user.username}
        )
        if plyr is not None:
            user.in_contest['status'] = True
            user.in_contest['contest_id'] = self._id
            self.players[user.username] = 0
            # raise ContestEnded("This user has already given the contests")
        user.in_contest['status'] = True
        user.in_contest['contest_id'] = self._id
        self.players[user.username] = 0
        register_player(db_object, self._id, user.username)

    def finish_user_session(self, user):
        user.in_contest['status'] = False
        user.in_contest['contest_id'] = None

    def has_user_session_ended(self, user):
        return not (user.in_contest['status']==True and user.in_contest['contest_id']==self._id)

    def get_puzzle(self, db_object, puzzle_index, user):
        if (not self.has_user_session_ended(user)) and puzzle_index>=0 and puzzle_index<len(self.puzzles):
            print(self.puzzles[puzzle_index])
            return fetch_puzzle(db_object, self.puzzles[puzzle_index])
        return None

    def submit_ans(self, db_object, puzzle_index, username, score):
        if not self.has_user_session_ended(user):
            update_puzzle_score(db_object, self._id, self.puzzles[puzzle_index], username, score)
            return {'success': True}
        return {'success': False}

    def add_puzzle(self, db_object, puzzle_id):
        if db_object.puzzle.find_one({'_id': puzzle_id}) is None:
            return False
        db_object.contest.update_one(
            {'_id': self._id},
            {'$push': {
                'puzzles': puzzle_id,
            }}
        )
        return True

    def create_puzzle(self, db_object, start_fen, solution):
        puzzle = createPuzzle(db_object, start_fen, solution)
        self.puzzles.append(puzzle.inserted_id)
        db_object.contest.update_one(
            {'_id': self._id},
            {'$push': {
                'puzzles': puzzle.inserted_id,
            }}
        )

def update_puzzle_score(db_object, contest_code, puzzle_id, username, score):
    key = 'players. + username'
    db_object.contest.update_one(
        {'_id': contest_code},
        {'$inc': {
            key: score,
        }}
    )
    pushPuzzleResult(db_object, puzzle_id, username, score)

def register_player(db_object, contest_code, username):
    key = 'players.' + username
    db_object.contest.update_one(
        {'_id': contest_code},
        {'$set': {
            key: 0,
        }}
    )

def loadContest(db_object, contest_code):
    contest = db_object.contest.find_one({
        '_id': contest_code,
    })
    if contest is None:
        return None
    return Contest(contest)

def create_contest(db_object, contest_code, puzzles, date, time):
    db_object.contest.insert_one({
        '_id': contest_code,
        'players': {},
        'puzzles': [],
        'date': date,
        'time': time,
        'info': '',
        'title': '',
    })