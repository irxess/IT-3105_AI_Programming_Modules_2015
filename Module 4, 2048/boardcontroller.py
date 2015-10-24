import visuals
import random

class BoardController():


    def __init__(self):
        random.seed()
        self.board = [0] * 4*4
        self.window = visuals.GameWindow()
        spawnRandomTile(self.board)
        self.window.update_view(self.board)


    def move(self, direction):
        """
        Actually move. Slide first, then insertTile.
        Update GUI
        """
        slide(direction, self.board)
        spawnRandomTile(self.board)
        self.window.update_view(self.board)


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


def slide(direction, board):
    """
    Move all tiles as far in direction as possible.
    Use merge() if needed.
    """
    if direction == 'up':
        return slideUp(board)
    elif direction == 'down':
        return slideDown(board)
    elif direction == 'right':
        return slideRight(board)
    elif direction == 'left':
        return slideLeft(board)


def slideUp(board):
    merged = [False] * 4*4
    mergeCount = 0

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
                    mergeCount += 1
                    merged[pos-4] = True

    return board, mergeCount


def slideDown(board):
    merged = [False] * 4*4
    mergeCount = 0

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
                    mergeCount += 1
                    merged[pos+4] = True
    return board, mergeCount


def slideLeft(board):
    merged = [False] * 4*4
    mergeCount = 0

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
                    mergeCount += 1
                    merged[pos-1] = True
    return board, mergeCount


def slideRight(board):
    merged = [False] * 4*4
    mergeCount = 0

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
                    mergeCount += 1
                    merged[pos+1] = True
    return board, mergeCount


def findEmptyTiles(board):
    empty = []
    for i in range( len(board) ):
        if board[i] == 0:
            empty.append(i)
    return empty


def createAllPossibleNeighbors(board):
    emptyList = findEmptyTiles()
    neighbors = []
    for pos in emptyList:
        neighbor = board.copy()
        insertTile(pos, 2, neighbor)
        neighbors.append(neighbor)


def spawnRandomTile(board):
    listWithEmptyTiles = findEmptyTiles(board)
    randomPosition = random.choice( listWithEmptyTiles )
    randomValue = 1
    if random.random() > 0.9:
        randomValue = 2
    insertTile( randomPosition, randomValue, board )


def insertTile( position, value, board ):
    # 
    board[position] = value

