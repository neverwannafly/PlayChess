# Contains custom exception classes

class InvalidMoveError(Exception):
    """Is raised when an user makes an invalid move"""
    pass

class SenderCannotBeVerified(Exception):
    "Is raised when make_move is called by questionable sender"

class GameNotFound(Exception):
    "Is raised when a game url cannot be found"