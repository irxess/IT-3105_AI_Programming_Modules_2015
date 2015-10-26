from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy
import time


# measure process time
t0 = time.clock()
stop = minutes = seconds = 0

# b = bc.BoardController()
b = window()
b.window.update_view(b.board)


def logic():
    bestHeuristic = 0
    bestDirection = 'none'

    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, nofMerges, maxMerging, highestMerg = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:

            heuristic = expectimax( nextBoard, 6, 'board', nofMerges, maxMerging, highestMerg)
            if heuristic > bestHeuristic:
                bestHeuristic = heuristic
                bestDirection = direction

    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        print 'game over'
        stop =  float(time.clock())
        # minutes = (stop - t0)/60
        # seconds = (stop - t0)%60
        print 'Running time: ', time.clock()
        while True:
            b.window.update_view(b.board)

while True:
    logic()
