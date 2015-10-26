from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy
import time, timeit
import settings, sys
import state

# measure process time
t0 = time.clock()
stop = minutes = seconds = 0


# settings.init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
settings.init(0.05, 0.2, 0.2, 0.05, 0, 0.5)

# b = bc.BoardController()
b = window()
b.window.update_view(b.board)


def emptyTiles(board):
    count = 0
    for cell in board:
        if cell == 0:
            count += 1
    return count


def logic():
    bestHeuristic = 0
    bestDirection = 'none'

    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, nofMerges = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:
            nofEmpty = emptyTiles(nextBoard)
            if nofEmpty > 10:
                heuristic = expectimax( nextBoard, 2, 'board', nofMerges)
            elif nofEmpty > 5:
                heuristic = expectimax( nextBoard, 4, 'board', nofMerges)
            else:
                heuristic = expectimax( nextBoard, 6, 'board', nofMerges)
            if heuristic > bestHeuristic:
                bestHeuristic = heuristic
                bestDirection = direction

    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        print 'game over'
        # stop =  float(time.clock())
        # minutes = (stop - t0)/60
        # seconds = (stop - t0)%60
        print 'Running time: ', time.clock()
        print 2**max(b.board)
        while True:
            b.window.update_view(b.board)
        # sys.exit(0)

while True:
    logic()


