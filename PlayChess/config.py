import os
import re as regex

from .utils import game_queue

# Contains secret key 
configurations = {
    '_SECRET_KEY' : os.urandom(64),
    'JSON_AUTO_SORT': False,
}

## Server Global variables

USER_DICT = {}
GAMES = {}
ADMIN_DICT = {}

# Keeps track of players finding matches.
PLAYERS_QUEUE = game_queue.GameQueue()

# Regex expression for email and username verification
EMAIL_PATTERN_COMPILED = regex.compile(r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$")
# Username regex also limits the string to be b/w 5 and 30!
USERNAME_REGEX = regex.compile("^[a-zA-Z0-9_]{5,30}$")

FEN_NOTATION_REGEX = regex.compile(r"\s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s*")

# Codes for terminal colors
TERMINAL_COLORS = {
    'CBOLD': '\33[1m',
    'CURL': '\33[4m',
    'CRED': '\33[31m',
    'CGREEN': '\33[32m',
    'CYELLOW': '\33[33m',
    'CBLUE': '\33[34m',
    'CVIOLET': '\33[35m',
    'CBEIGE': '\33[36m',
    'CWHITE': '\33[37m',
    'CEND': '\033[0m',
}

# Map chess piece label to fen notation
CHESS_PIECES = {
    'white-p': 'P',
    'white-K': 'K',
    'white-Q': 'Q',
    'white-R': 'R',
    'white-B': 'B',
    'white-N': 'N',
    'black-p': 'p',
    'black-K': 'k',
    'black-Q': 'q',
    'black-R': 'r',
    'black-B': 'b',
    'black-N': 'n',
}

# Map fen-notation to chess piece class name
CHESS_PIECE_CLASS = {
    'P': ('Pawn', 'white'),
    'p': ('Pawn', 'black'),
    'K': ('King', 'white'),
    'k': ('King', 'black'),
    'Q': ('Queen', 'white'),
    'q': ('Queen', 'black'),
    'R': ('Rook', 'white'),
    'r': ('Rook', 'black'),
    'B': ('Bishop', 'white'),
    'b': ('Bishop', 'black'),
    'N': ('Knight', 'white'),
    'n': ('Knight', 'black'),
}

# Starting Position Notation
START_POSITION_NOTATION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# Branching Limit
BRANCHING_LIMIT = 1000