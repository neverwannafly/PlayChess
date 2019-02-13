# Defines a blank class to identify blank sqaures on chessboard

# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.

import sys

from .exceptions import (InvalidMoveError, SideNotAuthorizedToMakeMove, Checkmate, Draw)
from .decorators import deprecated
from .. import config

class Piece:
    # Initialises the basic component of every piece
    def __init__(self):
        self.points = 0
        self.current_position = ""
        self.color = ""
        self.label = ""
        self.name = ""
        
    def __str__(self):
        return self.label + self.current_position

    __repr__=__str__
    
class Pawn(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "Pawn"
        self.points = 1
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "p"

class Knight(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "Knight"
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "N"

class Bishop(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "Bishop"
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "B"

class Rook(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "Rook"
        self.points = 5
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "R"

class Queen(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "Queen"
        self.points = 9
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "Q"

class King(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.name = "King"
        self.points = 100
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "K"

class Blank(Piece):
    def __init__(self, current_position):
        super().__init__()
        self.name = "Blank"
        self.current_position = current_position
        self.color = "none"
        self.label = self.color + "-" + "_"

class Square:
    def __init__(self):
        self.html_class = "square"
        self.html_id = "notation"
        self.label = "square"
        self.piece = Piece()
        self.css = ""

    def __str__(self):
        return self.html_id + "-" + self.piece.label

    __repr__ = __str__
    
class DarkSquare(Square):
    def __init__(self):
        super().__init__()
        self.label = "dark-square"
        self.html_class += " dark "

    def set_html_id(self, html_id):
        self.html_id = html_id

class LightSquare(Square):
    def __init__(self):
        super().__init__()
        self.label = "light-square"
        self.html_class += " light "

    def set_html_id(self, html_id):
        self.html_id = html_id 

# Defines the final layout of the chessboard!
class Chessboard:
    def __init__(self, fen_notation=config.START_POSITION_NOTATION):

        # An array holding recent changes in board position
        self.changes = []

        self.castling_rights_white = {
            "white_side_castled": False,
            "has_white_king_moved": False,
            "has_a1_rook_moved": False,
            "has_h1_rook_moved": False,
        }
        self.castling_rights_black = {
            "black_side_castled": False,
            "has_black_king_moved": False,
            "has_a8_rook_moved": False,
            "has_h8_rook_moved": False,
        }

        self.enpassant_target_square = None
        self.enpassant_flag_life = 0
        self.moves = 0

        # Stores position of black and white pieces for quick checkmate lookup
        self.pieces = {
            'white': {},
            'black': {},
        }

        self.configuration = 1
        # config of 2 means chessboard is drawn for black player at bottom!
        # config of 1 means chessboard is drawn for white player at bottom!
        self.chessboard = self.create_chessboard()

        if fen_notation is None:
            # making chessboard from fen notation should be better
            self.initialise_board()
            self.pieces['white']['King'] = ['e1']
            self.pieces['white']['Queen'] = ['d1']
            self.pieces['white']['Bishop'] = ['c1', 'f1']
            self.pieces['white']['Knight'] = ['b1', 'g1']
            self.pieces['white']['Rook'] = ['a1', 'h1']
            self.pieces['white']['Pawn'] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
            self.pieces['black']['King'] = ['e8']
            self.pieces['black']['Queen'] = ['d8']
            self.pieces['black']['Bishop'] = ['c8', 'f8']
            self.pieces['black']['Knight'] = ['b8', 'g8']
            self.pieces['black']['Rook'] = ['a8', 'h8']
            self.pieces['black']['Pawn'] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        else:
            self.load_position(fen_notation)

    @property
    def can_white_castle(self):
        castling_flag = (self.castling_rights_white["white_side_castled"]^self.castling_rights_white["has_white_king_moved"])^(self.castling_rights_white["has_a1_rook_moved"]&self.castling_rights_white["has_h1_rook_moved"])
        return not castling_flag

    @property
    def can_black_castle(self):
        castling_flag = (self.castling_rights_black["black_side_castled"]^self.castling_rights_black["has_black_king_moved"])^(self.castling_rights_black["has_a8_rook_moved"]&self.castling_rights_black["has_h8_rook_moved"])
        return not castling_flag

    # generates a rudimentary fen notation of a position with placeholders and
    # these placeholders in fen notation would be filled upon by the Game class.
    # A placeholer will be represented by '*'.
    @property
    def fen_notation(self):
        fen_notation = ""
        # Set board position
        for rank in self.chessboard:
            rank_notation = ""
            skips = 0
            for square in rank:
                piece = config.CHESS_PIECES.get(square.piece.label, None)
                if piece == None:
                    skips += 1
                else:
                    if skips is not 0:
                        rank_notation += str(skips)
                        rank_notation += piece
                        skips = 0
                    else:
                        rank_notation += piece
            if skips is not 0:
                rank_notation += str(skips)
            fen_notation += rank_notation + "/"

        # remove trailing slash
        fen_notation = fen_notation[:-1]

        # Create placeholder for player to move
        # A chessboard is an object that doesnt concerns itself with 
        # which player has to make a move. That behavior is handled 
        # By the game class hence unrequired parameters in fen notations
        # are being filled by placeholders
        fen_notation = fen_notation + " * "

        # Castling Parameters
        if not self.castling_rights_white['white_side_castled'] and not self.castling_rights_white['has_white_king_moved']:
            if not self.castling_rights_white['has_h1_rook_moved']:
                fen_notation = fen_notation + "K"
            if not self.castling_rights_white['has_a1_rook_moved']:
                fen_notation = fen_notation + "Q"
        if not self.castling_rights_black['black_side_castled'] and not self.castling_rights_black['has_black_king_moved']:
            if not self.castling_rights_black['has_h8_rook_moved']:
                fen_notation = fen_notation + "k"
            if not self.castling_rights_black['has_a8_rook_moved']:
                fen_notation = fen_notation + "q"

        # Enpassant Target Square
        if self.enpassant_target_square is not None:
            fen_notation = fen_notation + " " + str(self.enpassant_target_square)
        else:
            fen_notation = fen_notation + " - "

        # Halfmove placeholder and full move placeholders. Again a delegate
        # of the Game class and not the chessboard class
        fen_notation = fen_notation + " * *"

        return fen_notation

    def load_position(self, fen_notation):
        # Extract required parameters for the Chessboard class from fen_notation
        fen_components = fen_notation.split(' ')
        game_component = fen_components[0] + "/"
        castling_info = fen_components[2]
        enpassant_target_square = fen_components[3]

        def get_position(file, rank):
            return str(chr(ord('a') + file -1)) + str(rank)

        # Iterate over the board_component and place pieces as you find them
        rank = 8
        file = 1
        temp_board = []
        board_row = []

        for character in game_component:
            if character == '/':
                rank -= 1
                file = 1
                temp_board.append(board_row)
                board_row = []
            else:
                piece = config.CHESS_PIECE_CLASS.get(character, None)
                if piece is None:
                    squares = int(character)
                    while squares >= 1:
                        board_row.append(self.create_piece(get_position(file, rank), 'Blank'))
                        file += 1
                        squares -= 1
                else:

                    board_row.append(self.create_piece(get_position(file, rank), piece[0], piece[1]))
                    file += 1

        # Create the chessboard
        for i in range(8):
            for j in range(8):
                self.chessboard[i][j].piece = temp_board[i][j]
                self.chessboard[i][j].html_class += temp_board[i][j].label
                self.chessboard[i][j].css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
                    html_class = self.chessboard[i][j].html_class,
                    html_id = self.chessboard[i][j].html_id
                )

        # Parse Castling info
        if not "K" in castling_info:
            self.castling_rights_white['has_h1_rook_moved'] = True
        if not "Q" in castling_info:
            self.castling_rights_white['has_a1_rook_moved'] = True
        if not "k" in castling_info:
            self.castling_rights_black['has_h8_rook_moved'] = True
        if not "q" in castling_info:
            self.castling_rights_black['has_a8_rook_moved'] = True
        if "-" in castling_info:
            self.castling_rights_black['has_black_king_moved'] = True
            self.castling_rights_white['has_white_king_moved'] = True

        # Enpassant Setting
        if enpassant_target_square is not None:
            self.enpassant_target_square = enpassant_target_square
            self.enpassant_flag_life = 1

    @deprecated
    def initialise_board(self):
        # White chess pieces
        white_rooks = [Rook("a1", "white"), Rook("h1", "white")]
        white_knights = [Knight("b1", "white"), Knight("g1", "white")]
        white_bishops = [Bishop("c1", "white"), Bishop("f1", "white")]
        white_row1 = [white_rooks[0], white_knights[0], white_bishops[0], Queen("d1", "white"), King("e1", "white"), white_bishops[1], white_knights[1], white_rooks[1]]
        white_row2 = [Pawn(chr(ord("a")+i)+"2", "white") for i in range(0,8)]
        # Black chess pieces
        black_rooks = [Rook("a8", "black"), Rook("h8", "black")]
        black_knights = [Knight("b8", "black"), Knight("g8", "black")]
        black_bishops = [Bishop("c8", "black"), Bishop("f8", "black")]
        black_row7 = [Pawn(chr(ord("a")+i)+"7", "black") for i in range(0,8)]
        black_row8 = [black_rooks[0], black_knights[0], black_bishops[0], Queen("d8", "black"), King("e8", "black"), black_bishops[1], black_knights[1], black_rooks[1]]
        # Blank chess rows
        blank_row3 = [Blank(chr(ord("a")+i)+"3") for i in range(0,8)]
        blank_row4 = [Blank(chr(ord("a")+i)+"4") for i in range(0,8)]
        blank_row5 = [Blank(chr(ord("a")+i)+"5") for i in range(0,8)]
        blank_row6 = [Blank(chr(ord("a")+i)+"6") for i in range(0,8)]
        # Create a board
        temp_board = [black_row8, black_row7, blank_row6, blank_row5, blank_row4, blank_row3, white_row2, white_row1]
        # Assign pieces to visual board
        for i in range(8):
            for j in range(8):
                self.chessboard[i][j].piece = temp_board[i][j]
                self.chessboard[i][j].html_class += temp_board[i][j].label
                self.chessboard[i][j].css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
                    html_class = self.chessboard[i][j].html_class,
                    html_id = self.chessboard[i][j].html_id
                )

    def create_chessboard(self):
        chessboard = []
        for i in range(8):
            chess_row = []
            first = "a"
            for j in range(8):
                if (i+j)%2==0:
                    # Square is white
                    square = LightSquare()
                else:
                    # Square is black
                    square = DarkSquare()
                square.set_html_id(first+str(8-i))
                chess_row.append(square)
                first = chr(ord(first)+1)
            chessboard.append(chess_row)
        return chessboard

    def draw_chessboard(self):
        if self.configuration==1:
            return self.draw_chessboard_for_white()
        else:
            return self.draw_chessboard_for_black()

    def swap_board(self):
        if self.configuration == 1:
            self.configuration = 2
        else:
            self.configuration = 1

    def convert_to_index(self, notation):
        return self.chessboard[ord('8')-ord(notation[1])][ord(notation[0])-ord('a')]

    def return_index_as_touple(self, notation):
        return (ord('8')-ord(notation[1]), ord(notation[0])-ord('a'))

    # Will always be applied to check if a square is attacked or not
    def is_square_under_attack(self, square, piece_color=None):
        indexes = self.return_index_as_touple(square)

        if piece_color == None:
            piece_color = self.convert_to_index(square).piece.color

        def are_colors_opposite(destination_square):
            return destination_square.piece.color != piece_color and destination_square.piece.color != "none"

        def are_colors_same(destination_square):
            return destination_square.piece.color == piece_color

        X, Y = indexes[0], indexes[1]
        
        # Check along horizontal
        for y in range(Y+1, 8):
            destination_square = self.chessboard[X][y]

            if y==Y+1 and destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                return True

            if (destination_square.piece.name == "Rook" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Bishop", "Knight", "Pawn", "King"]:
                break

        for y in range(Y-1, -1, -1):
            destination_square = self.chessboard[X][y]

            if y==Y-1 and destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                return True

            if (destination_square.piece.name == "Rook" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Bishop", "Knight", "Pawn", "King"]:
                break

        # Check along vertcial 
        for x in range(X+1, 8):
            destination_square = self.chessboard[x][Y]

            if x==X+1 and destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                return True

            if (destination_square.piece.name == "Rook" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Bishop", "Knight", "Pawn", "King"]:
                break

        for x in range(X-1, -1, -1):
            destination_square = self.chessboard[x][Y]

            if x==X-1 and destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                return True

            if (destination_square.piece.name == "Rook" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Bishop", "Knight", "Pawn", "King"]:
                break

        # Check on a1-h8 diagonal
        x = X-1
        y = Y+1
        while x>=0 and y<=7:
            destination_square = self.chessboard[x][y]

            if x==X-1 and y==Y+1:
                if destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                    return True

                if piece_color == "white" and destination_square.piece.name == "Pawn" and are_colors_opposite(destination_square):
                    return True

            if (destination_square.piece.name == "Bishop" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Rook", "Knight", "Pawn", "King"]:
                break
            
            x -= 1
            y += 1

        x = X+1
        y = Y-1
        while x<=7 and y>=0:
            destination_square = self.chessboard[x][y]

            if x==X+1 and y==Y-1:
                if destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                    return True

                if piece_color == "black" and destination_square.piece.name == "Pawn" and are_colors_opposite(destination_square):
                    return True

            if (destination_square.piece.name == "Bishop" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Rook", "Knight", "Pawn", "King"]:
                break
            
            x += 1
            y -= 1

        # Check on a8-h1 diagonal
        x = X-1
        y = Y-1
        while x>=0 and y>=0:
            destination_square = self.chessboard[x][y]

            if x==X-1 and y==Y-1:
                if destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                    return True

                if piece_color == "white" and destination_square.piece.name == "Pawn" and are_colors_opposite(destination_square):
                    return True

            if (destination_square.piece.name == "Bishop" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Rook", "Knight", "Pawn", "King"]:
                break
            
            x -= 1
            y -= 1

        x = X+1
        y = Y+1
        while x<=7 and y<=7:
            destination_square = self.chessboard[x][y]

            if x==X+1 and y==Y+1:
                if destination_square.piece.name == "King" and are_colors_opposite(destination_square):
                    return True

                if piece_color == "black" and destination_square.piece.name == "Pawn" and are_colors_opposite(destination_square):
                    return True

            if (destination_square.piece.name == "Bishop" or destination_square.piece.name == "Queen") and are_colors_opposite(destination_square):
                return True

            if are_colors_same(destination_square):
                break

            if destination_square.piece.name in ["Rook", "Knight", "Pawn", "King"]:
                break
            
            x += 1
            y += 1

        # Check skew positions
        possible_skew_moves = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        for move in possible_skew_moves:
            if X+move[0] <=7 and X+move[0]>=0 and Y+move[1] <= 7 and Y+move[1]>=0:
                destination_square = self.chessboard[X+move[0]][Y+move[1]]

                if destination_square.piece.name == "Knight" and are_colors_opposite(destination_square):
                    return True

        return False

    # Need to be used for pawn promotion, en-passant and board editor
    def delete_piece(self, piece_position):
        obj = self.convert_to_index(piece_position)
        self.pieces[obj.piece.color][obj.piece.name].remove(piece_position)
        obj.piece = Blank(piece_position)
        obj.html_class = obj.html_class.strip("white-Kwhite-Qwhite-Rwhite-Bwhite-Nwhite-pblack-Kblack-Qblack-Rblack-Bblack-Nblack-p")
        obj.html_class += " " + obj.piece.label
        obj.css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
            html_class = obj.html_class,
            html_id = obj.html_id
        )
        self.changes.append({'pos': piece_position, 'class': obj.html_class})

    # Can be used for simple Board Editor
    def create_piece(self, piece_position, piece_name, piece_color=None):
        if piece_color == None:
            return getattr(sys.modules[__name__], piece_name)(piece_position)
        if self.pieces[piece_color].get(piece_name, None) == None:
            self.pieces[piece_color][piece_name] = [piece_position]
        else:
            self.pieces[piece_color][piece_name].append(piece_position)
        return getattr(sys.modules[__name__], piece_name)(piece_position, piece_color)

    # This method changes the current state of board, i.e modifies id's and classes of 
    # class members of Sqaure class and also change the values of chessboard array.
    def change_chessboard_state(self, initial_pos, final_pos):
        obj = self.convert_to_index(initial_pos)
        #temporarily delete piece from pieces object
        if obj.piece.name!="Blank":
            self.pieces[obj.piece.color][obj.piece.name].remove(initial_pos)
        temp_piece = obj.piece
        obj.piece = Blank(initial_pos)
        obj.html_class = obj.html_class.strip("white-Kwhite-Qwhite-Rwhite-Bwhite-Nwhite-pblack-Kblack-Qblack-Rblack-Bblack-Nblack-p")
        obj.html_class += " " + obj.piece.label
        obj.css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
            html_class = obj.html_class,
            html_id = obj.html_id
        )
        self.changes.append({'pos': initial_pos, 'class': obj.html_class})
        obj = self.convert_to_index(final_pos)
        if obj.piece.name != "Blank":
            self.pieces[obj.piece.color][obj.piece.name].remove(final_pos)
        obj.html_class = obj.html_class.strip("white-Kwhite-Qwhite-Rwhite-Bwhite-Nwhite-pblack-Kblack-Qblack-Rblack-Bblack-Nblack-pnone_-")
        obj.piece = temp_piece
        obj.html_class += " " + obj.piece.label
        obj.css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
            html_class = obj.html_class,
            html_id = obj.html_id
        )
        # Add the deleted piece back to pieces object
        if obj.piece.name!="Blank":
            self.pieces[obj.piece.color][obj.piece.name].append(final_pos)
        self.changes.append({'pos': final_pos, 'class': obj.html_class})

    def make_move(self, initial_pos, final_pos):

        if self.is_checkmate:
            print("Mate")
            raise Checkmate(self.moves%2)

        draw = self.is_draw()

        if draw[0]:
            raise Draw(draw[1])

        color = self.convert_to_index(initial_pos).piece.color
        if (self.moves % 2 == 0 and color == "black") or (self.moves % 2 != 0 and color == "white"):
            raise SideNotAuthorizedToMakeMove()

        self.changes = []
        try:
            self.make_move_private(initial_pos, final_pos)
            self.moves += 1
            if self.enpassant_flag_life >= 1:
                self.enpassant_flag_life = 0
                self.enpassant_target_square = None
            elif self.enpassant_target_square:
                self.enpassant_flag_life += 1
        except InvalidMoveError:
            raise InvalidMoveError("Invalid Move played", initial_pos, final_pos)

        return self.changes

    def make_move_private(self, initial_pos, final_pos):
        if initial_pos==final_pos:
            raise InvalidMoveError("Initial and Final Positions cannot be same", initial_pos, final_pos)
        if self.convert_to_index(initial_pos).piece.color=="none":
            raise InvalidMoveError("Cannot Move from empty Square", initial_pos, final_pos)

        if self.is_move_legal(initial_pos, final_pos):
            # Check for special king moves!
            if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="K":
                # King side castle
                if initial_pos=="e1" and final_pos=="g1":
                    self.change_chessboard_state("e1", "g1")
                    self.change_chessboard_state("h1", "f1")
                    self.castling_rights_white["white_side_castled"] = True
                # Queen side castle
                elif initial_pos=="e1" and final_pos=="c1":
                    self.change_chessboard_state("e1", "c1")
                    self.change_chessboard_state("a1", "d1")
                    self.castling_rights_white["white_side_castled"] = True
                # King side castle
                elif initial_pos=="e8" and final_pos=="g8":
                    self.change_chessboard_state("e8", "g8")
                    self.change_chessboard_state("h8", "f8")
                    self.castling_rights_black["black_side_castled"] = True
                # Queen side castle
                elif initial_pos=="e8" and final_pos=="c8":
                    self.change_chessboard_state("e8", "c8")
                    self.change_chessboard_state("a8", "d8")
                    self.castling_rights_black["black_side_castled"] = True
                else:
                    self.change_chessboard_state(initial_pos, final_pos)
            # Check for special pawn moves - enpassant
            elif self.convert_to_index(initial_pos).piece.label.split('-')[1]=="p":
                ini_index = self.return_index_as_touple(initial_pos)
                fin_index = self.return_index_as_touple(final_pos)
                diagonal_flag = abs(ini_index[0]-fin_index[0]) & abs(ini_index[1]-fin_index[1])
                if self.enpassant_target_square is not None and diagonal_flag:
                    # Black attacked pawn -> 6, white attacked pawn -> 3
                    if self.enpassant_target_square[1]=="6":
                        direction = -1
                    elif self.enpassant_target_square[1]=="3":
                        direction = 1
                    attacked_pawn = self.enpassant_target_square[0] + str(int(self.enpassant_target_square[1])+direction)
                    self.delete_piece(attacked_pawn)
                self.change_chessboard_state(initial_pos, final_pos)
            else:
                self.change_chessboard_state(initial_pos, final_pos)
        else:
            raise InvalidMoveError("Invalid Move played", initial_pos, final_pos)

        # white_king = self.pieces["white"]["King"][0]
        # if (self.is_square_under_attack(white_king)):
        #     self.changes.append({'pos': white_king, 'class': self.convert_to_index(white_king).html_class + ' check'})

        # black_king = self.pieces["black"]["King"][0]
        # if (self.is_square_under_attack(black_king)):
        #     self.changes.append({'pos': black_king, 'class': self.convert_to_index(black_king).html_class + ' check'})

    @property
    def is_checkmate(self):
        color = "white" if self.moves%2==0 else "black"
        if self.is_square_under_attack(self.pieces[color]["King"][0]):
            moves = []
            for piece in self.pieces[color]:
                for square in self.pieces[color][piece]:
                    moves += self.generate_legal_moves(square)
            # print(moves)
            # print(self.pieces)
            return True if len(moves)==0 else False
        return False

    @property
    def is_stalemate(self):
        color = "white" if self.moves%2==0 else "black"
        if not self.is_square_under_attack(self.pieces[color]["King"]):
            moves = []
            for piece in self.pieces[color]:
                moves += self.generate_legal_moves(self.pieces[color][piece])
            print(moves)
            return True if len(moves)==0 else False
        return True

    def is_draw(self):
        return [False, "stalemate"]

    def move_top(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while X<=7 and X>0 and limit>0:
            X -= 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_bottom(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while X<7 and X>=0 and limit>0:
            X += 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_left(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while Y<=7 and Y>0 and limit>0:
            Y -= 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_right(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while Y<7 and Y>=0 and limit>0:
            Y += 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_top_right(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while X<=7 and X>0 and Y<7 and Y>=0 and limit>0:
            X -= 1
            Y += 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_bottom_right(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while X<7 and X>=0 and Y<7 and Y>=0 and limit>0:
            X += 1
            Y += 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_top_left(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while Y<=7 and Y>0 and X<=7 and X>0 and limit>0:
            Y -= 1
            X -= 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def move_bottom_left(self, initial_pos, limit=10):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        init_piece_color = self.chessboard[X][Y].piece.color
        move_list = []
        while Y<=7 and Y>0 and X<7 and X>=0 and limit>0:
            Y -= 1
            X += 1
            if self.chessboard[X][Y].piece.color == init_piece_color and init_piece_color != "none":
                break
            if self.chessboard[X][Y].piece.color != "none":
                move_list.append(self.chessboard[X][Y].html_id)
                break
            move_list.append(self.chessboard[X][Y].html_id)
            limit -= 1
        return move_list

    def make_diagonal_moves(self, initial_pos, limit=10):
        move_list = []
        move_list += self.move_bottom_left(initial_pos, limit=limit) + self.move_bottom_right(initial_pos, limit=limit) + self.move_top_left(initial_pos, limit=limit) + self.move_top_right(initial_pos, limit=limit)
        return move_list 

    def make_orthogonal_moves(self, initial_pos, limit=10):
        move_list = []
        move_list += self.move_left(initial_pos, limit=limit) + self.move_right(initial_pos, limit=limit) + self.move_top(initial_pos, limit=limit) + self.move_bottom(initial_pos, limit=limit)
        return move_list

    # This could be optimised by excluding the need to check colors!
    def generate_pawn_moves(self, initial_pos):
        move_list = []
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        tempX, tempY = X, Y
        piece_color = self.convert_to_index(initial_pos).piece.color
        if piece_color == "white":
            if int(self.convert_to_index(initial_pos).html_id[1])==2:
                limit=2
            else:
                limit=1
            while tempX<=7 and tempX>0 and limit>0:
                tempX -= 1
                if self.chessboard[tempX][tempY].piece.color !="none":
                    break
                move_list.append(self.chessboard[tempX][tempY].html_id)
                limit -= 1
            # check for captures at top-right and top-left
            if X-1<=7 and Y+1<=7:
                if self.enpassant_target_square==self.chessboard[X-1][Y+1].html_id:
                    move_list.append(self.enpassant_target_square)
                elif self.chessboard[X-1][Y+1].piece.color == "black":
                    move_list.append(self.chessboard[X-1][Y+1].html_id)
            if X-1<=7 and Y-1>=0:
                if self.enpassant_target_square==self.chessboard[X-1][Y-1].html_id:
                    move_list.append(self.enpassant_target_square)
                elif self.chessboard[X-1][Y-1].piece.color == "black":
                    move_list.append(self.chessboard[X-1][Y-1].html_id)
        else:
            if int(self.convert_to_index(initial_pos).html_id[1])==7:
                limit=2
            else:
                limit=1
            while tempX<7 and tempX>=0 and limit>0:
                tempX += 1
                if self.chessboard[tempX][tempY].piece.color !="none":
                    break
                move_list.append(self.chessboard[tempX][tempY].html_id)
                limit -= 1
            # check for captures at bottom-right and bottom-left
            if X+1>=0 and Y-1>=0:
                if self.enpassant_target_square==self.chessboard[X+1][Y-1].html_id:
                    move_list.append(self.enpassant_target_square)
                elif self.chessboard[X+1][Y-1].piece.color == "white":
                    move_list.append(self.chessboard[X+1][Y-1].html_id)
            if X+1>=0 and Y+1<=7:
                if self.enpassant_target_square==self.chessboard[X+1][Y+1].html_id:
                    move_list.append(self.enpassant_target_square)
                elif self.chessboard[X+1][Y+1].piece.color == "white":
                    move_list.append(self.chessboard[X+1][Y+1].html_id)
        return move_list

    def generate_knight_moves(self, initial_pos):
        move_list = []
        possible_skew_moves = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        for move in possible_skew_moves:
            if X+move[0] <=7 and X+move[0]>=0 and Y+move[1] <= 7 and Y+move[1]>=0:
                if self.chessboard[X+move[0]][Y+move[1]].piece.color != self.convert_to_index(initial_pos).piece.color:
                    move_list.append(self.chessboard[X+move[0]][Y+move[1]].html_id)
        return move_list

    def special_king_moves(self, initial_pos):
        move_list = []
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        # Check for special king moves!
        if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="K":
            if self.can_white_castle and self.convert_to_index(initial_pos).piece.color=="white":
                # King side castle
                if initial_pos=="e1" and self.castling_rights_white["has_h1_rook_moved"] is not True:
                    if self.chessboard[X][Y+1].piece.color=="none" and self.chessboard[X][Y+2].piece.color=="none":
                        move_list.append("g1")
                # Queen side castle
                if initial_pos=="e1" and self.castling_rights_white["has_a1_rook_moved"] is not True:
                    if self.chessboard[X][Y-1].piece.color=="none" and self.chessboard[X][Y-2].piece.color=="none":
                        move_list.append("c1")
            if self.can_black_castle and self.convert_to_index(initial_pos).piece.color=="black":
                # King side castle
                if initial_pos=="e8" and self.castling_rights_black["has_h8_rook_moved"] is not True:
                    if self.chessboard[X][Y+1].piece.color=="none" and self.chessboard[X][Y+2].piece.color=="none":
                        move_list.append("g8")
                # Queen side castle
                if initial_pos=="e8" and self.castling_rights_black["has_a8_rook_moved"] is not True:
                    if self.chessboard[X][Y-1].piece.color=="none" and self.chessboard[X][Y-2].piece.color=="none":
                        move_list.append("c8")
        return move_list

    # Sets flags such as of castling rights, enpassant
    def set_flags(self, initial_pos, final_pos):
        # Set Enpassant Flags
        indexes = self.return_index_as_touple(final_pos)
        old_indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        oX, oY = old_indexes[0], old_indexes[1]
        if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="p":
            if abs(int(final_pos[1])-int(initial_pos[1]))==2:
                direction = (int(final_pos[1])-int(initial_pos[1]))//2
                if Y+1<=7:
                    if self.chessboard[X][Y+1].piece.label.split('-')[1]=='p' and self.chessboard[oX][oY].piece.color!=self.chessboard[X][Y+1].piece.color:
                        self.enpassant_target_square = self.chessboard[X+direction][Y].html_id
                if Y-1>=0:
                    if self.chessboard[X][Y-1].piece.label.split('-')[1]=='p' and self.chessboard[oX][oY].piece.color!=self.chessboard[X][Y-1].piece.color:
                        self.enpassant_target_square = self.chessboard[X+direction][Y].html_id

        # Set Castling Flags
        if self.can_white_castle and self.convert_to_index(initial_pos).piece.color=="white":
            # Check if piece moved is king
            if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="K":
                self.castling_rights_white["has_white_king_moved"] = True
            # Check if piece moved is rook
            if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="R":
                if initial_pos=="a1":
                    self.castling_rights_white["has_a1_rook_moved"] = True
                elif initial_pos=="h1":
                    self.castling_rights_white["has_h1_rook_moved"] = True

        if self.can_black_castle and self.convert_to_index(initial_pos).piece.color=="black":
            # Check if piece moved is king
            if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="K":
                self.castling_rights_black["has_black_king_moved"] = True
            # Check if piece moved is rook
            if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="R":
                if initial_pos=="a8":
                    self.castling_rights_white["has_a8_rook_moved"] = True
                elif initial_pos=="h8":
                    self.castling_rights_white["has_h8_rook_moved"] = True
            
    def is_move_legal(self, initial_pos, final_pos):
        # Will make use of generate legal move only.
        if final_pos in self.generate_legal_moves(initial_pos):
            self.set_flags(initial_pos, final_pos)
            return True
        return False

    def make_temp_move(self, initial_pos, final_pos):

        color = "white" if self.moves%2==0 else "black"

        initial_piece = self.convert_to_index(initial_pos).piece
        final_piece = self.convert_to_index(final_pos).piece

        self.convert_to_index(initial_pos).piece = final_piece
        self.convert_to_index(final_pos).piece = initial_piece

        self.pieces[initial_piece.color][initial_piece.name].remove(initial_pos)
        self.pieces[initial_piece.color][initial_piece.name].append(final_pos)
        if final_piece.name != "Blank":
            self.pieces[final_piece.color][final_piece.name].remove(final_pos)

        def reset_pos():
            self.convert_to_index(initial_pos).piece = initial_piece
            self.convert_to_index(final_pos).piece = final_piece
            self.pieces[initial_piece.color][initial_piece.name].remove(final_pos)
            self.pieces[initial_piece.color][initial_piece.name].append(initial_pos)
            if final_piece.name != "Blank":
                self.pieces[final_piece.color][final_piece.name].append(final_pos)

        if self.is_square_under_attack(self.pieces[color]["King"][0]):
            reset_pos()
            return True
        else:
            reset_pos()
            return False


    def generate_legal_moves(self, initial_pos):

        color = "white" if self.moves%2==0 else "black"

        if (self.moves % 2 == 0 and color == "black") or (self.moves % 2 != 0 and color == "white"):
            raise SideNotAuthorizedToMakeMove()

        if self.is_square_under_attack(self.pieces[color]["King"][0]):
            piece_label = self.convert_to_index(initial_pos).piece.label.split('-')[1]
            moveList = []
            if piece_label=="K":
                moveList += self.make_orthogonal_moves(initial_pos, limit=1) + self.make_diagonal_moves(initial_pos, limit=1) + self.special_king_moves(initial_pos)
            elif piece_label=="Q":
                moveList += self.make_diagonal_moves(initial_pos) + self.make_orthogonal_moves(initial_pos)
            elif piece_label=="R":
                moveList += self.make_orthogonal_moves(initial_pos)
            elif piece_label=="B":
                moveList += self.make_diagonal_moves(initial_pos)
            elif piece_label=="N":
                moveList += self.generate_knight_moves(initial_pos)
            elif piece_label=="p":
                moveList += self.generate_pawn_moves(initial_pos)
            else:
                moveList += []

            moveList[:] = [move for move in moveList if not self.make_temp_move(initial_pos, move)]

            return moveList

        piece_label = self.convert_to_index(initial_pos).piece.label.split('-')[1]
        if piece_label=="K":
            return self.make_orthogonal_moves(initial_pos, limit=1) + self.make_diagonal_moves(initial_pos, limit=1) + self.special_king_moves(initial_pos)
        elif piece_label=="Q":
            return self.make_diagonal_moves(initial_pos) + self.make_orthogonal_moves(initial_pos)
        elif piece_label=="R":
            return self.make_orthogonal_moves(initial_pos)
        elif piece_label=="B":
            return self.make_diagonal_moves(initial_pos)
        elif piece_label=="N":
            return self.generate_knight_moves(initial_pos)
        elif piece_label=="p":
            return self.generate_pawn_moves(initial_pos)
        else:
            return []

    def draw_chessboard_for_white(self):
        board_html_view = "<tr>"
        for i in range(8):
            for j in range(8):
                board_html_view += self.chessboard[i][j].css
            board_html_view = board_html_view + "</tr>"
        self.configuration = 1
        return board_html_view

    def draw_chessboard_for_black(self):
        board_html_view = "<tr>"
        for i in range(7,-1,-1):
            for j in range(7, -1, -1):
                board_html_view += self.chessboard[i][j].css
            board_html_view = board_html_view + "</tr>"
        self.configuration = 2
        return board_html_view

    def reset_chessboard(self):
        # Change these settings in accordance with FEN Notation
        self.moves = 0
        self.enpassant_target_square = None
        self.enpassant_flag_life = 0
        self.configuration = 1
        self.changes = []
        
        self.chessboard = self.create_chessboard()
        self.load_position(config.START_POSITION_NOTATION)