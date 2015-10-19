from abc import ABCMeta, abstractmethod
import boardcontroller as bc
from copy import deepcopy, copy
import random


# use that method on stack overflow
# factors:
# 1. The location of the (current) largest tile on the board. Is it in a corner?
# 2. The number of free cells
# 3. Are the high numbers in a "snake-pattern"
# 4. How many merges occur in this move
def calculateHeuristic(board):
        heuristic = 0
        return heuristic

def countOpenCells(board):
    count = 0
    for cell in board:
            if cell == 0:
                count += 1
    return count
def generateMAXSuccessors(board):
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    print 'max', board
    successors = []
    merges = []
    directions = ['up', 'down', 'left', 'right']
    for direction in directions:
        succ = copy(board)
        print board, succ
        succ, merges = bc.slide(direction, succ)
        print board, succ

        # if succ == parent means no move, no changes after sliding therfore don't append as successor
        if succ != board:
            successors.append(succ)
    print 'max returned', successors
    return (successors, ['up', 'down', 'left', 'right'])


def generateCHANCESuccessors(board):
    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """
    print 'chance', board

    successors = []
    probabilities = []

    for i in range( len(board) ):
        if board[i] == 0:
            succ1 = deepcopy(board)
            succ2 = deepcopy(board)

            succ1[i] = 2
            successors.append(succ1)
            probabilities.append(0.9)
            succ2[i] = 4
            successors.append(succ2)
            probabilities.append(0.1)
    outcomes = len(probabilities)
    # HVa betyr dette?
    for i in range(outcomes):
        probabilities[i] /= (outcomes/2)

    print 'chance returned', probabilities
    return (successors, probabilities)


    def generateSuccessorsBiased(board):
        # Using biased stochastics
        successors = []
        for i in range( len(board) ):
            succ1 = deepcopy(board)
            if board[i] == 0:
                succ[i] = self.flip()
                successors.append(succ)
        return successors

    def flip(self):
        # choice of 2 or 4 with p = {0.9, 0.1}
        if random.random() > 0.9 :
                return 2
        return 4    

