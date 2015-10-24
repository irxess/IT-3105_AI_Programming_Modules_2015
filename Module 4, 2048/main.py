from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *


b = window()

while True:
    bestHeuristic = 0
    bestDirection = 'none'
    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, mergeCount = bc.slide(direction, b.board)
        if nextBoard != b.board:
            heuristic = expectimax( nextBoard, 5, 'board')
            if heuristic > bestHeuristic:
                heuristic = bestHeuristic
                bestDirection = direction
    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        print 'game over'
        while True:
            pass
