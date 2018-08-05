"""Contains a Game class that can handle chessgames b/w two players"""

from .chessboard import Chessboard

class Game:
    
    def __init__(self):
        self.chessboard = Chessboard()

        # Player1 would be white and Player2 would be black!

        self.player1 = None
        self.player2 = None
        self.spectators = []