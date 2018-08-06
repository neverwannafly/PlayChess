"""Contains a Game class that can handle chessgames b/w two players"""

from .chessboard import Chessboard

class Game:
    
    def __init__(self, game_name):
        self.chessboard = Chessboard()

        # Player1 would be white and Player2 would be black!

        self.player1 = game_name.split('-')[0]
        self.player2 = game_name.split('-')[1]
        self.spectators = []

        self.game_name = game_name
