# Contains custom exception classes

class InvalidMoveError(Exception):
    """Is raised when an user makes an invalid move"""
    pass

class SideNotAuthorizedToMakeMove(Exception):
    """Is raised when idle side (currently not having a turn) makes a move"""
    pass

class Checkmate(Exception):
    """Is raised when one of the players is checkmated"""
    def __init__(self, result):
        self.result = result
    
class Draw(Exception):
    """Is raised when a drawing condition is met"""
    def __init__(self, cause):
        self.cause = cause

class SenderCannotBeVerified(Exception):
    """Is raised when make_move is called by questionable sender"""
    pass

class GameNotFound(Exception):
    """Is raised when a game url cannot be found"""
    pass

class InvalidDatabaseURL(Exception):
    """Is raised when database url cannot be located"""
    pass

class InvalidFenNotation(Exception):
    """Is raised when an invalid fen notation is provided"""

class DefenderColorNotSpecified(Exception):
    """Is raised when you check for attack on a square without specifying defender color"""

class BranchingLimitReached(Exception):
    """Is raised when branching limit of chessboard class is reached"""