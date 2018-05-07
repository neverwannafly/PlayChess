# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.

class Piece:
    # Initialises the basic component of every piece
    def __init__(self):
        self.points = 0
        self.legal_moves = []
        self.current_position = ""
        self.color = ""
        self.isPieceCaptured = False
    
    def makeMove(self, move):    
        self.current_position = move
    
    def pieceCaptured(self):
        self.isPieceCaptured = True
    
class Pawn(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Rook(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass

# Defines the final layout of the chessboard!
class Chessboard():
    pass
