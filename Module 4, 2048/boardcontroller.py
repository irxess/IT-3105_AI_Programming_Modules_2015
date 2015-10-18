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


    def slide(self, direction, board):
        """
        Move all tiles as far in direction as possible.
        Use merge() if needed.
        """
        if direction == 'up':
            self.slideUp(board)
        elif direction == 'down':
            self.slideDown(board)
        elif direction == 'right':
            self.slideRight(board)
        elif direction == 'left':
            self.slideLeft(board)
        self.window.update_view( self.board )


    def slideUp(self, board):
        merged = [False] * 4*4
        for i in range(3): # move as much as possible
            for pos in range(4,16):
                if board[pos-4] == 0:
                    board[pos-4] = board[pos]
                    board[pos] = 0
                elif board[pos-4] == board[pos]:
                    if not merged[pos] and not merged[pos-4]:
                        # merge tiles
                        board[pos-4] += 1
                        board[pos] = 0
                        merged[pos-4] = True
        return len(merged)


    def slideDown(self, board):
        merged = [False] * 4*4
        for i in range(3):
            for pos in range(11,-1,-1):
                if board[pos+4] == 0:
                    board[pos+4] = board[pos]
                    board[pos] = 0
                elif board[pos+4] == board[pos]:
                    if not merged[pos] and not merged[pos+4]:
                        # merge tiles
                        board[pos+4] += 1
                        board[pos] = 0
                        merged[pos+4] = True
        return len(merged)


    def slideLeft(self, board):
        merged = [False] * 4*4
        for i in range(3):
            for pos in [1,2,3,5,6,7,9,10,11,13,14,15]:
                if board[pos-1] == 0:
                    board[pos-1] = board[pos]
                    board[pos] = 0
                elif board[pos-1] == board[pos]:
                    if not merged[pos] and not merged[pos-1]:
                        # merge tiles
                        board[pos-1] += 1
                        board[pos] = 0
                        merged[pos-1] = True
        return len(merged)


    def slideRight(self, board):
        merged = [False] * 4*4
        for i in range(3):
            for pos in [0,1,2,4,5,6,8,9,10,12,13,14]:
                if board[pos+1] == 0:
                    board[pos+1] = board[pos]
                    board[pos] = 0
                elif board[pos+1] == board[pos]:
                    if not merged[pos] and not merged[pos+1]:
                        # merge tiles
                        board[pos+1] += 1
                        board[pos] = 0
                        merged[pos+1] = True
        return len(merged)


    def findEmptyTiles(self):
        empty = []
        for i in range( len(self.board) ):
            if self.board[i] == 0:
                empty.append(i)
        return empty


    def createAllPossibleNeighbors(self, board):
        emptyList = self.findEmptyTiles()
        neighbors = []
        for pos in emptyList:
            neighbor = board.copy()
            self.insertTile(pos, 2, neighbor)
            neighbors.append(neighbor)


    def spawnRandomTile(self):
        listWithEmptyTiles = self.findEmptyTiles()
        randomPosition = random.choice( listWithEmptyTiles )
        randomValue = 1
        if random.random() > 0.9:
            randomValue = 2
        self.insertTile( randomPosition, randomValue, self.board )


    def insertTile( self, position, value, board ):
        board[position] = value
        self.window.update_view( board )


    def move(self, direction):
        """
        Actually move. Slide first, then insertTile.
        Update GUI
        """
        pass

