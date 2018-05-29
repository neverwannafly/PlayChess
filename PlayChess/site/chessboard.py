# Defines a blank class to identify blank sqaures on chessboard

# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.

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
        self.label = "_"

class Square:
    def __init__(self):
        self.html_class = "square"
        self.html_id = "notation"
        self.label = "square"
        self.piece = Piece()
        self.css = ""

    def __str__(self):
        return self.html_id

    __repr__ = __str__
    
class DarkSquare(Square):
    def __init__(self):
        super().__init__()
        self.html_class += " dark "

    def set_html_id(self, html_id):
        self.html_id = html_id

class LightSquare(Square):
    def __init__(self):
        super().__init__()
        self.html_class += " light "

    def set_html_id(self, html_id):
        self.html_id = html_id 

# Defines the final layout of the chessboard!
class Chessboard:
    def __init__(self):
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

    def swap_board(self):
        if self.configuration == 1:
            return self.draw_chessboard_for_black()
        else:
            return self.draw_chessboard_for_white()

    def convert_to_index(self, notation):
        return self.chessboard[ord('8')-ord(notation[1])][ord(notation[0])-ord('a')]

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

    def make_move(self, initial_pos, final_pos):
        obj = self.convert_to_index(initial_pos)
        temp_piece = obj.piece
        obj.piece = Blank(initial_pos)
        obj.html_class = obj.html_class.strip("white-K white-Q white-R white-B white-N white-p black-K black-Q black-R black-B black-N black-p")
        obj = self.convert_to_index(final_pos)
        obj.piece = temp_piece
        obj.html_class += " " + obj.piece.label

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
