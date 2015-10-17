import visuals
import random

class BoardController():

    def __init__(self):
        random.seed()
        self.board = [0] * 4*4
        self.window = visuals.GameWindow()
        self.spawnRandomTile()

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


    def slide(self, direction):
        """
        Move all tiles as far in direction as possible.
        Use merge() if needed.
        """
        pass


    def merge(self, position):
        """
        Merge two tiles.
        """
        pass


    def findEmptyTiles(self):
        empty = []
        for i in range( len(self.board) ):
            if self.board[i] == 0:
                empty.append(i)
        return empty

    def createAllPossibleNeighbors(self, board):
        pass


    def spawnRandomTile(self):
        listWithEmptyTiles = self.findEmptyTiles()
        randomPosition = random.choice( listWithEmptyTiles )
        randomValue = 1
        if random.random() > 0.9:
            randomValue = 2
        self.insertTile( randomPosition, randomValue )


    def insertTile( self, position, value ):
        self.board[position] = value
        self.window.update_view( self.board )


    def move(self, direction):
        """
        Actually move. Slide first, then insertTile.
        Update GUI
        """
        pass

