"""Contains a Game class that can handle chessgames b/w two players"""

from .chessboard import Chessboard

class Game:
    def __init__(self, uuid):
        self.uuid = uuid
        self.chessboard = Chessboard()
        self.player1 = None
        self.player2 = None
        self.spectators = []