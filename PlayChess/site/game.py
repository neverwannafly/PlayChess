"""Contains a Game class that can handle chessgames b/w two players"""

import random

from .chessboard import Chessboard

class Game:
    
    def __init__(self, game_name):
        self.chessboard = Chessboard()

        # Player1 would be white and Player2 would be black!
        self.player1 = None
        self.player2 = None
        self.spectators = []

        self.game_name = game_name
        self.assign_players()

    def assign_players(self):
        index = random.randint(0,1)
        player1, player2 = self.game_name.split('-')[index], self.game_name.split('-')[int(not index)]
        self.player1 = player1
        self.player2 = player2