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
                        <div class="square dark" id="#{id}">

                        </div>
                    </td>
                    """.format(id=first+str(row+1))
                else:
                    self.board = self.board + """
                    <td>
                        <div class="square light" id="#{id}">

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
                        <div class="square light" id="#{id}">

                        </div>
                    </td>
                    """.format(id=first+str(8-row))
                else:
                    self.board = self.board + """
                    <td>
                        <div class="square dark" id="#{id}">

                        </div>
                    </td>
                    """.format(id=first+str(8-row))
                first = chr(ord(first)+1)
            self.board = self.board + "</tr>"
        self.id = 2
        return self.board
