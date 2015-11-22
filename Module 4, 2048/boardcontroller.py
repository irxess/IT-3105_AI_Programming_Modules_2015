import visuals
import random
from copy import copy
import sys
if (sys.version_info < (3, 0)):
    from expectimax import *
else:
    xrange = range


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
        return self.board[x * 4 + y]


    def setGrid(self, x, y, v):
        """
        Update the value of a position of the board.
        0,0 is the top left corner.
        """
        self.board[x * 4 + y] = v



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
    maxMerging = highestMerg = 0
    maxTile = max(board)

    for i in xrange(3): # move as much as possible
        for pos in xrange(4,16):
            if board[pos-4] == 0:
                board[pos-4] = board[pos]
                board[pos] = 0
            elif board[pos-4] == board[pos]:
                if not merged[pos] and not merged[pos-4]:
                    # merge tiles

                    if board[pos] == maxTile:
                        maxMerging = board[pos]+1
                    board[pos-4] += 1
                    highestMerg = max( board[pos-4] , highestMerg)
                    board[pos] = 0
                    mergeCount += 1
                    merged[pos-4] = True
    return board, mergeCount, maxMerging, highestMerg


def slideDown(board):
    #mergeCount = 0

    # for row in xrange(3, 0, -1):
    #     for col in xrange(4):
    #         if board[row, col] == 0:
    #             board[row, col] = board[row-1, col]
    #             board[row-1, col] = 0
            #elif board[row, col] == board[row-1, col]:
            #    board[row, col] = board[row-1, col] + board[row, col]
            #    mergeCount += 1
            #else:
            #    board[row, col] = board[row, col]

    merged = [False] * 4*4
    mergeCount = 0
    maxMerging = highestMerg= 0
    maxTile = max(board)

    for i in xrange(3):
        for pos in range(11,-1,-1):
            if board[pos+4] == 0:
                board[pos+4] = board[pos]
                board[pos] = 0
            elif board[pos+4] == board[pos]:
                if not merged[pos] and not merged[pos+4]:
                    # merge tiles

                    if board[pos] == maxTile:
                        maxMerging = board[pos]+1
                    board[pos+4] += 1
                    highestMerg = max( board[pos+4] , highestMerg)
                    board[pos] = 0
                    mergeCount += 1
                    merged[pos+4] = True
    return board, mergeCount, maxMerging, highestMerg


def slideLeft(board):
    merged = [False] * 4*4
    mergeCount = 0
    maxMerging = highestMerg = 0
    maxTile = max(board)

    for i in xrange(3):
        for pos in [1,2,3,5,6,7,9,10,11,13,14,15]:
            if board[pos-1] == 0:
                board[pos-1] = board[pos]
                board[pos] = 0
            elif board[pos-1] == board[pos]:
                if not merged[pos] and not merged[pos-1]:
                    # merge tiles
                    if board[pos] == maxTile:
                        maxMerging = board[pos]+1

                    board[pos-1] += 1
                    highestMerg = max( board[pos-4] , highestMerg)
                    board[pos] = 0
                    mergeCount += 1
                    merged[pos-1] = True
    return board, mergeCount, maxMerging, highestMerg


def slideRight(board):
    merged = [False] * 4*4
    mergeCount = 0
    maxMerging = highestMerg=0
    maxTile = max(board)
    for i in xrange(3):
        for pos in [2,1,0,6,5,4,10,9,8,14,13,12]:
            if board[pos+1] == 0:
                board[pos+1] = board[pos]
                board[pos] = 0
            elif board[pos+1] == board[pos]:
                if not merged[pos] and not merged[pos+1]:
                    # merge tiles
                    if board[pos] == maxTile:
                        maxMerging = board[pos]+1

                    board[pos+1] += 1
                    highestMerg = max( board[pos+1] , highestMerg)
                    board[pos] = 0
                    mergeCount += 1
                    merged[pos+1] = True
    return board, mergeCount, maxMerging, highestMerg


def findEmptyTiles(board):
    #return np.array(np.where(board == 0))
    empty = []
    for i in xrange( len(board) ):
        if board[i] == 0:
            empty.append(i)
    return empty


#def createAllPossibleNeighbors(board):
#    emptyList = findEmptyTiles()
#    neighbors = []
#    for pos in emptyList:
#        neighbor = board.copy()
#        insertTile(pos, 2, neighbor)
#        neighbors.append(neighbor)


def spawnRandomTile(board):
    listWithEmptyTiles = findEmptyTiles(board)
    randomPosition = random.choice( listWithEmptyTiles )
    #randomPosition = tuple(listWithEmptyTiles.T[np.random.randint(0, listWithEmptyTiles.shape[1])])
    randomValue = 1
    if random.random() > 0.9:
        randomValue = 2
    insertTile( randomPosition, randomValue, board )


def insertTile( position, value, board ):
    board[position] = value
