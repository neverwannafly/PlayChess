# Defines a blank class to identify blank sqaures on chessboard!
class Blank:
    def __init__(self):
        self.label = "Blank"

    def returnLabel(self):
        return self.label

# Define a class for chessboard pieces with necessary members and methods.
# This would serve as the parent class for other pieces.
class Piece:
    # Initialises the basic component of every piece
    def __init__(self):
        self.points = 0
        self.current_position = ""
        self.color = ""
        self.legal_moves = []
        self.label = ""
    
    def makeMove(self, move):    
        self.current_position = move

    def returnLabel(self):
        return self.label
    
class Pawn(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 1
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.label = "p"

    def generate_legal_moves(self, position):
        pass

class Knight(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.label = "N"

    def generate_legal_moves(self, position):
        pass

class Bishop(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 3
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.lable = "B"

    def generate_legal_moves(self, position):
        pass

class Rook(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 5
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.label = "R"

    def generate_legal_moves(self, position):
        pass

class Queen(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 9
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.label = "Q"

    def generate_legal_moves(self, position):
        pass

class King(Piece):
    def __init__(self, current_position, color):
        super.__init__()
        self.points = 100
        self.current_position = current_position
        self.color = color
        self.legal_moves = self.generate_legal_moves(current_position)
        self.label = "K"

    def generate_legal_moves(self, position):
        pass

# Defines the final layout of the chessboard!
class Chessboard:
    def __init__(self):
        self.board = ""
        self.id = 0

    def swapBoard(self):
        if self.id == 2:
            self.id =1
            return self.createBoardForBlack()
        else:
            self.id = 2
            return self.createBoardForWhite()

    def createBoardForBlack(self):
        self.board = ""
        for row in range(8):
            self.board = self.board + "<tr>"
            first = "h"
            for column in range(8):
                if (column+row)%2==0:
                    self.board = self.board + """
                    <td>
                        <div class="square light" id="{id}">

                        </div>
                    </td>
                    """.format(id=first+str(row+1))
                else:
                    self.board = self.board + """
                    <td>
                        <div class="square dark" id="{id}">

                        </div>
                    </td>
                    """.format(id=first+str(row+1))
                first = chr(ord(first)-1)
            self.board = self.board + "</tr>"
        self.id = 1
        return self.board

    def createBoardForWhite(self):
        self.board = ""
        for row in range(8):
            first = "a"
            self.board = self.board + "<tr>"
            for column in range(8):
                if (column+row)%2==0:
                    self.board = self.board + """
                    <td>
                        <div class="square light" id="{id}">

                        </div>
                    </td>
                    """.format(id=first+str(8-row))
                else:
                    self.board = self.board + """
                    <td>
                        <div class="square dark" id="{id}">

                        </div>
                    </td>
                    """.format(id=first+str(8-row))
                first = chr(ord(first)+1)
            self.board = self.board + "</tr>"
        self.id = 2
        return self.board
