from abc import ABCMeta, abstractmethod
import boardcontroller as BC
from copy import deepcopy


# use that method on stack overflow
# factors:
# 1. The location of the (current) largest tile on the board. Is it in a corner?
# 2. The number of free cells
# 3. Are the high numbers in a "snake-pattern"
# 4. How many merges occur in this move
def calculateHeuristic():
        heuristic = 0
        return heuristic


def generateMAXSuccessors(board):
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    successors = []
    for direction in ['up', 'down', 'left', 'right']:

        bc = BC( deepcopy(board) )
        succ = bc.slide(board, direction)
        # if succ == parent means no move, no changes after sliding therfore don't append as successor
        if succ != board:
            successors.append(succ)
    return successors


def generateCHANCESuccessors(board):
    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """

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
    for i in range(outcomes):
        probabilities[i] /= (outcomes/2)

    return (successors, probabilities)


def generateSuccessorsC():
    # how to use biasStochastic? 
    pass


def biasStochastic():
    # calculate bias stochastic choice of 2 or 4 with p = {0.9, 0.1}
    pass


    
    

            
