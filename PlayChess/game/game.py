"""Contains a Game class that can handle chessgames b/w two players"""

import random

from ..utils import chessboard

class Game:
    
    def __init__(self, game_name):
        self.chessboard = chessboard.Chessboard()

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

## Helper functions
def make_game(session, players_queue, ongoing_games):
    if session.get('username'):
        username = session['username']
        while True:
            message = players_queue.add_to_queue(username)
            players_queue.print_queue()
            if message.code:
                if not ongoing_games.get(message) and message.info:
                    ongoing_games[message.info] = Game(message.info)
                break
            time.sleep(1)

def get_game(session, ongoing_games):
    username = session.get('username')
    game = [games for games in ongoing_games if username in games]
    if len(game) is not 1:
        return None
    return game[0]