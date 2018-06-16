# Defines a blank class to identify blank sqaures on chessboard

# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.

from .exceptions import InvalidMoveError

class Piece:
    # Initialises the basic component of every piece
    def __init__(self):
        self.points = 0
        self.current_position = ""
        self.color = ""
        self.label = ""

    def returnLabel(self):
        return self.label
        
    def __str__(self):
        return self.label + self.current_position

    __repr__=__str__
    
class Pawn(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 1
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "p"

class Knight(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "N"

class Bishop(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "B"

class Rook(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 5
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "R"

class Queen(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 9
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "Q"

class King(Piece):
    def __init__(self, current_position, color):
        super().__init__()
        self.points = 100
        self.current_position = current_position
        self.color = color
        self.label = color + "-" + "K"

class Blank(Piece):
    def __init__(self, current_position):
        super().__init__()
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
    def __init__(self):
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
        self.enpassant_target = None
        
        self.configuration = 1
        # config of 2 means chessboard is drawn for white player at bottom!
        # config of 1 means chessboard is drawn for black player at bottom!
        self.chessboard = self.create_chessboard()
        self.initialise_board()

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
            return self.draw_chessboard_for_black()
        else:
            return self.draw_chessboard_for_white()

    def convert_to_index(self, notation):
        return self.chessboard[ord('8')-ord(notation[1])][ord(notation[0])-ord('a')]

    def return_index_as_touple(self, notation):
        return (ord('8')-ord(notation[1]), ord(notation[0])-ord('a'))

    def make_move(self, initial_pos, final_pos):
        indexes = self.return_index_as_touple(initial_pos)
        X, Y = indexes[0], indexes[1]
        # Check for special king moves!
        if self.convert_to_index(initial_pos).piece.label.split('-')[1]=="K":
            if self.castling_rights_white["white_side_castled"] is not True and self.castling_rights_white["has_white_king_moved"] is not True:
                if self.convert_to_index(initial_pos).piece.color=="white":
                    # King side castle
                    if initial_pos=="e1" and final_pos=="g1" and self.castling_rights_white["has_h1_rook_moved"] is not True:
                        if self.chessboard[X][Y+1].piece.color=="none" and self.chessboard[X][Y+2].piece.color=="none":
                            self.force_move_private("e1", "g1")
                            self.force_move_private("h1", "f1")
                            self.castling_rights_white["white_side_castled"] = True
                            self.castling_rights_white["has_white_king_moved"] = True
                            self.castling_rights_white["has_a1_rook_moved"] = True
                            self.castling_rights_white["has_h1_rook_moved"] = True
                    # Queen side castle
                    if initial_pos=="e1" and final_pos=="c1" and self.castling_rights_white["has_a1_rook_moved"] is not True:
                        if self.chessboard[X][Y-1].piece.color=="none" and self.chessboard[X][Y-2].piece.color=="none":
                            self.force_move_private("e1", "c1")
                            self.force_move_private("a1", "d1")
                            self.castling_rights_white["white_side_castled"] = True
                            self.castling_rights_white["has_white_king_moved"] = True
                            self.castling_rights_white["has_a1_rook_moved"] = True
                            self.castling_rights_white["has_h1_rook_moved"] = True
            if self.castling_rights_black["black_side_castled"] is not True and self.castling_rights_black["has_black_king_moved"] is not True:
                if self.convert_to_index(initial_pos).piece.color=="black":
                    # King side castle
                    if initial_pos=="e8" and final_pos=="g8" and self.castling_rights_black["has_h8_rook_moved"] is not True:
                        if self.chessboard[X][Y+1].piece.color=="none" and self.chessboard[X][Y+2].piece.color=="none":
                            self.force_move_private("e8", "g8")
                            self.force_move_private("h8", "f8")
                            self.castling_rights_black["black_side_castled"] = True
                            self.castling_rights_black["has_black_king_moved"] = True
                            self.castling_rights_black["has_a8_rook_moved"] = True
                            self.castling_rights_black["has_h8_rook_moved"] = True
                    # Queen side castle
                    if initial_pos=="e8" and final_pos=="c8" and self.castling_rights_black["has_a8_rook_moved"] is not True:
                        if self.chessboard[X][Y-1].piece.color=="none" and self.chessboard[X][Y-2].piece.color=="none":
                            self.force_move_private("e8", "c8")
                            self.force_move_private("a8", "d8")
                            self.castling_rights_black["black_side_castled"] = True
                            self.castling_rights_black["has_black_king_moved"] = True
                            self.castling_rights_black["has_a8_rook_moved"] = True
                            self.castling_rights_black["has_h8_rook_moved"] = True
        self.make_move_private(initial_pos, final_pos)

    # This method is to override legal moves generated by generate_legal_moves() method so as to innumerate
    # special chess moves like castling, en-passant, pawn promotion.
    def force_move_private(self, initial_pos, final_pos):
        obj = self.convert_to_index(initial_pos)
        temp_piece = obj.piece
        obj.piece = Blank(initial_pos)
        obj.html_class = obj.html_class.strip("white-Kwhite-Qwhite-Rwhite-Bwhite-Nwhite-pblack-Kblack-Qblack-Rblack-Bblack-Nblack-p_")
        obj.css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
            html_class = obj.html_class,
            html_id = obj.html_id
        )
        obj = self.convert_to_index(final_pos)
        obj.html_class = obj.html_class.strip("white-Kwhite-Qwhite-Rwhite-Bwhite-Nwhite-pblack-Kblack-Qblack-Rblack-Bblack-Nblack-p_")
        obj.piece = temp_piece
        obj.html_class += " " + obj.piece.label
        obj.css = """<td><div class="{html_class}" id="{html_id}"></div></td>""".format(
            html_class = obj.html_class,
            html_id = obj.html_id
        )

    def make_move_private(self, initial_pos, final_pos):
        if self.is_move_legal(initial_pos, final_pos):
            self.force_move_private(initial_pos, final_pos)

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
            if self.chessboard[X-1][Y+1].piece.color == "black":
                move_list.append(self.chessboard[X-1][Y+1].html_id)
            if self.chessboard[X-1][Y-1].piece.color == "black":
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
            if self.chessboard[X+1][Y-1].piece.color == "white":
                move_list.append(self.chessboard[X+1][Y-1].html_id)
            if self.chessboard[X+1][Y+1].piece.color == "white":
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

    def is_move_legal(self, initial_pos, final_pos):
        # Will make use of generate legal move only.
        if final_pos in self.generate_legal_moves(initial_pos):
            return True
        return False

    def generate_legal_moves(self, initial_pos):
        piece_label = self.convert_to_index(initial_pos).piece.label.split('-')[1]
        # returns a dictionary of valid final positions for a particular piece
        if piece_label=="K":
            return self.make_orthogonal_moves(initial_pos, limit=1) + self.make_diagonal_moves(initial_pos, limit=1)
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
        self.configuration = 1
        self.chessboard = self.create_chessboard()
        self.initialise_board()


    
    # This Json data could be used as a way to save games!
    # piece = {
    #     "white-K": King("white", notation),
    #     "white-Q": King("white", notation),
    #     "white-R": Rook("white", notation),
    #     "white-B": Rook("white", notation),
    #     "white-N": Rook("white", notation),
    #     "white-p": Pawn("white", notation),
    #     "black-K": King("black", notation),
    #     "black-Q": Queen("black", notation),
    #     "black-R": Rook("black", notation),
    #     "black-B": Bishop("black", notation),
    #     "black-N": Knight("black", notation),
    #     "black-p": Pawn("black", notation),
    # }.get(piece)