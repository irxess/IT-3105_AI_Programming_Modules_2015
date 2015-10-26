from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy
import time
import settings, sys


# measure process time
t0 = time.clock()
stop = minutes = seconds = 0


# settings.init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

nearness = 0.00
smooth   = 0.00
merge    = 0.25
gradient = 0.00
edge     = 0.25
opencell = 0.50

settings.init( nearness, smooth, merge, gradient, edge, opencell )

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
        nextBoard, nofMerges, maxMerging, highestMerg = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:

            # heuristic = expectimax( nextBoard, 6, 'board', nofMerges, maxMerging, highestMerg)
            nofEmpty = emptyTiles(nextBoard)
            if nofEmpty >= 10:
                heuristic = expectimax( nextBoard, 3, 'board', nofMerges, maxMerging, highestMerg)
            elif nofEmpty >= 5:
                heuristic = expectimax( nextBoard, 4, 'board', nofMerges, maxMerging, highestMerg)
            else:
                heuristic = expectimax( nextBoard, 6, 'board', nofMerges, maxMerging, highestMerg)
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
        print nearness, smooth, merge, gradient, edge, opencell
        while True:
            b.window.update_view(b.board)
        # sys.exit(0)

while True:
    logic()
