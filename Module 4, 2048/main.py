from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy
import time, timeit
import settings, sys

# measure process time
# t0 = time.clock()
# stop = minutes = seconds = 0


#def init(snake, smooth, merge, grad, edge, op):
settings.init(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

# b = bc.BoardController()
b = window()
b.window.update_view(b.board)

def logic():
    bestHeuristic = 0
    bestDirection = 'none'

    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, nofMerges = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:

            heuristic = expectimax( nextBoard, 5, 'board', nofMerges)
            if heuristic > bestHeuristic:
                bestHeuristic = heuristic
                bestDirection = direction

    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        # print 'game over'
        # stop =  float(time.clock())
        # minutes = (stop - t0)/60
        # seconds = (stop - t0)%60
        # print 'Running time: ', time.clock()
        # while True:
            # b.window.update_view(b.board)
        print 2**max(b.board)
        sys.exit(0)

while True:
    logic()


