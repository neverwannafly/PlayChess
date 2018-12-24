# Contains custom exception classes

class InvalidMoveError(Exception):
    """Is raised when an user makes an invalid move"""
    pass

class SideNotAuthorizedToMakeMove(Exception):
    """Is raised when idle side (currently not having a turn) makes a move"""
    pass

class Checkmate(Exception):
    """Is raised when one of the players is checkmated"""
    def __init__(self):
        self.result = None
    
class Draw(Exception):
    """Is raised when a drawing condition is met"""
    def __init__(self):
        self.cause = None
        self.result = None

class SenderCannotBeVerified(Exception):
    """Is raised when make_move is called by questionable sender"""
    pass

class GameNotFound(Exception):
    """Is raised when a game url cannot be found"""
    pass