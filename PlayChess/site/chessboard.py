# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.

class Piece:
    # Initialises the basic component of every piece
    def __init__(self):
        self.points = 0
        self.current_position = ""
        self.color = ""
        self.legal_moves = []
        self.isPieceCaptured = False
    
    def makeMove(self, move):    
        self.current_position = move
    
    def pieceCaptured(self):
        self.isPieceCaptured = True
    
class Pawn(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 1
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

class Knight(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

class Bishop(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

class Rook(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 5
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

class Queen(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 9
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

class King(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 100
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.isPieceCaptured = False

    def generate_legal_moves(self, position):
        pass

# Defines the final layout of the chessboard!
class Chessboard():
    pass
