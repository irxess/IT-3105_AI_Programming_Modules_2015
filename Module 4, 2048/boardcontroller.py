import visuals

class BoardController():

    def __init__(self):
        self.board = [0] * 4*4
        self.spawnRandomTile()
        self.window = visuals.GameWindow()

    def grid(self, x, y):
    """
    Get the value of a position of the board.
    0,0 is the top left corner.
    """
        if x < 4 and x >= 0:
            if y < 4 and y >= 0:
                return self.board[ x*4 + y ]


    def setGrid(self, x, y, v):
    """
    Update the value of a position of the board.
    0,0 is the top left corner.
    """
        if x < 4 and x >= 0:
            if y < 4 and y >= 0:
                position = x*4 + y
                self.board[ position ] = v
                self.window.update_view( self.board )


    """
    Move all tiles as far in direction as possible.
    Use merge() if needed.
    """
    def slide(self, direction):
        pass


    """
    Merge two tiles.
    """
    def merge(self, position):
        pass


    def findEmptyTiles(self):
        pass

    def createAllPossibleNeighbors(self, board):
        pass

    def spawnRandomTile(self):
        randomPosition = 4
        randomValue = 2
        self.insertTile( randomPosition, randomValue )


    def insertTile( self, position, value ):
        self.board[position] = value


    """
    Actually move. Slide first, then insertTile.
    Update GUI
    """
    def move(self, direction):
        pass

