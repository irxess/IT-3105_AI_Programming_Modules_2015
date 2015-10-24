from boardcontroller import BoardController as window
import boardcontroller as bc
from expectimax import *
from copy import copy


b = window()


while True:
    bestHeuristic = 0
    bestDirection = 'none'
    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, mergeCount = bc.slide(direction, copy(b.board) )
        print b.board
        print nextBoard
        if nextBoard != b.board:
            heuristic = expectimax( nextBoard, 5, 'board')
            print 'Heuristic: ', heuristic
            if heuristic > bestHeuristic:
                heuristic = bestHeuristic
                bestDirection = direction
    if bestHeuristic != 0:
        b.move(bestDirection)
    else:
        print 'game over'
        while True:
            b.window.update_view(b.board)
