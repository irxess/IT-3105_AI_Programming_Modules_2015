from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy
import time
import settings, sys

depth = 7
# measure process time
t0 = time.clock()
stop = minutes = seconds = 0


# settings.init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

nearness = 0.0
smooth   = 0.0
merge    = 0.4
gradient = 0.2
edge     = 0.5
opencell = 0.3

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
                heuristic = expectimax( nextBoard, 2, 'board', nofMerges, maxMerging, highestMerg)
            elif nofEmpty >= 5:
                heuristic = expectimax( nextBoard, 4, 'board', nofMerges, maxMerging, highestMerg)
            else:
                heuristic = expectimax( nextBoard, depth, 'board', nofMerges, maxMerging, highestMerg)
            if heuristic > bestHeuristic:
                bestHeuristic = heuristic
                bestDirection = direction

    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        orig_stdout = sys.stdout
        f = file('testResults.txt', 'w')
        sys.stdout = f

        print '----------------------------------'
        print 'IlseNesh'
        print 'game over'
        # stop =  float(time.clock())
        # minutes = (stop - t0)/60
        # seconds = (stop - t0)%60
        print 'Running time: ', time.clock()
        print 'depth = ', depth
        print 2**max(b.board)
        print nearness, smooth, merge, gradient, edge, opencell

        sys.stdout = orig_stdout
        f.close()
        # print 'game over \t'
        # # stop =  float(time.clock())
        # # minutes = (stop - t0)/60
        # # seconds = (stop - t0)%60
        # print 'IlseNesh'
        # print 'Running time: ', (time.clock())/60
        # print 2**max(b.board)
        # print nearness, smooth, merge, gradient, edge, opencell, ' \n'
        while True:
            b.window.update_view(b.board)
        # sys.exit(0)

while True:
    logic()
