"""Contains a Game class that can handle chessgames b/w two players"""

import random

from functools import wraps
from flask import jsonify

from ..utils import chessboard, exceptions

class Game:
    
    def __init__(self, game_name):
        self.chessboard = chessboard.Chessboard()

        # Player1 would be white and Player2 would be black!
        self.player1 = None
        self.player2 = None
        self.moves = 0
        self.spectators = []

        self.game_name = game_name
        self.assign_players()

    def assign_players(self):
        index = random.randint(0,1)
        player1, player2 = self.game_name.split('-')[index], self.game_name.split('-')[int(not index)]
        self.player1 = player1
        self.player2 = player2

    def generate_legal_moves(self, init_pos, sender):
        self.verify_sender(sender)
        moves = self.chessboard.generate_legal_moves(init_pos);
        return jsonify({'moves': moves})

    def make_move(self, init_pos, final_pos, sender):
        self.verify_sender(sender)
        try:
            changes = self.chessboard.make_move(init_pos, final_pos)
        except exceptions.InvalidMoveError as error:
            print(error)
            return jsonify({'success': False})
        return jsonify({
        'success': True,
        'changes': changes,
    })

    def verify_sender(self, sender):
        def check_sender(sender, moves, player1, player2):
            if moves%2 == 0:
                return sender==player1
            else:
                return sender==player2
        if not check_sender(sender, self.moves, self.player1, self.player2):
            raise exceptions.SenderCannotBeVerified("Sender Cannot be verified!")

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