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


def generateMAXSuccessors():
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    successors = []
    for direction in ['up', 'down', 'left', 'right']:

        bc = BC( deepcopy(self.board) )
        succ = bc.slide(self.board, direction)
        # if succ == parent means no move, no changes after sliding therfore don't append as successor
        if succ != self.board:
            successors.append(succ)
    return successors


def generateCHANCESuccessors():
    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """

    successors = []

    for i in range( len(self.board) ):
        succ1 = deepcopy(self.board)
        succ2 = deepcopy(self.board)

        if self.board[i] == 0:
            succ1[i] = 2
            successors.append(succ1)
            succ2[i] = 4
            successors.append(succ2)

    return successors


def generateSuccessorsC():
    # how to use biasStochastic? 
    pass


def biasStochastic():
    # calculate bias stochastic choice of 2 or 4 with p = {0.9, 0.1}
    pass


    
    

            
