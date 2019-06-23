"""Contains a Game class that can handle chessgames b/w two players"""

import random

from flask import jsonify

from ..utils import chessboard, exceptions

class Game:
    
    def __init__(self, game_name):
        self.chessboard = chessboard.Chessboard()

        # Player1 would be white and Player2 would be black!
        self.player1 = None
        self.player2 = None
        self.moves = 0
        self.prev_move = None
        self.spectators = []

        self.game_name = game_name
        self.assign_players()

    def assign_players(self):
        index = random.randint(0,1)
        player1, player2 = self.game_name.split('-')[index], self.game_name.split('-')[int(not index)]
        self.player1 = player1
        self.player2 = player2

    def generate_legal_moves(self, init_pos, sender):
        try:
            self.verify_move_origin(init_pos, sender)
        except exceptions.SenderCannotBeVerified as error:
            print(error)
            return jsonify({'moves': []})
        moves = self.chessboard.generate_legal_moves(init_pos);
        return jsonify({'moves': moves})

    def make_move(self, init_pos, final_pos, sender):
        try:
            self.verify_move_origin(init_pos, sender)
        except exceptions.SenderCannotBeVerified as error:
            print(error)
            move = {'success': False}
            self.prev_move = move
            return move
        try:
            changes = self.chessboard.make_move(init_pos, final_pos)
        except exceptions.InvalidMoveError as error:
            print(error)
            move = {'success': False}
            self.prev_move = move
            return move
        self.moves += 1
        move = {'success': True, 'changes': changes}
        self.prev_move = move
        return move

    def fetch_game_status(self):
        return self.chessboard.fetch_game_status()

    def verify_move_origin(self, init_pos, sender):
        self.verify_sender(sender)
        self.verify_piece_color(init_pos, sender)

    def verify_sender(self, sender):
        def check_sender(sender, moves, player1, player2):
            if moves%2 == 0:
                return sender==player1
            else:
                return sender==player2
        if not check_sender(sender, self.moves, self.player1, self.player2):
            raise exceptions.SenderCannotBeVerified("Sender Cannot be verified!")

    def verify_piece_color(self, init_pos, sender):
        def check_color(chessboard, init_pos, player1, player2, sender):
            color = chessboard.convert_to_index(init_pos).piece.color
            if sender == player1:
                return color=="white"
            elif sender == player2:
                return color=="black"
            else:
                return 0
        if not check_color(self.chessboard, init_pos, self.player1, self.player2, sender):
            raise exceptions.SenderCannotBeVerified("Sender doesnt have valid access!")

## Helper functions
def make_game(session, players_queue, ongoing_games):
    if session.get('username'):
        username = session['username']
        while True:
            message = players_queue.add_to_queue(username)
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