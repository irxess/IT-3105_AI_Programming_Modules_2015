from abc import ABCMeta, abstractmethod
import boardcontroller as BC
from copy import deepcopy

class State():
    __metaclass__ = ABCMeta

    def __init__(self, grid):

        self.grid = []
        self.value = self.calculateHeuristic()
        self.successors = []

# use that method on stack overflow
# factors:
# 1. The location of the (current) largest tile on the board. Is it in a corner?
# 2. The number of free cells ?
# 3. ?
# 4. ?
    def calculateHeuristic(self):
        self.heuristic = 0

    @abstractmethod
    def generateSuccessors(self):
        pass


class MAX(State):
    def __init__(self, grid):
        super(MAX, self).__init__(grid)
        self.value = grid.calculateHeuristic() #Correct?
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    
    def generateSuccessors(self):
        successors = []
        for direction in ['up', 'down', 'left', 'right']:

            bc = BC( deepcopy(self.grid) )
            succ = bc.slide(self.grid, direction)
            # if succ == parent means no move, no changes after sliding therfore don't append as successor
            if succ != self.grid:
                successors.append(succ)
        return successors


class CHANCE(State):
    def __init__(self, grid):
        super(CHANCE, self).__init__(grid)
        self.expectedValue = 0.0

    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """

    def generateSuccessors(self): #generates all successors
    # len(successors) = count(2C cases)
        successors = []

        for i in range( len(self.grid) ):

            succ1 = deepcopy(self.grid)
            succ2 = deepcopy(self.grid)

            if self.grid[i] == 0:
                succ1[i] = 2
                successors.append(succ1)
                succ2[i] = 4
                successors.append(succ2)

        return successors
    def generateSuccessorsBiased(self):
        # how to use biasStochastic? 
        for i in range( len(self.grid) ):
            succ1 = deepcopy(self.grid)
            if self.grid[i] == 0:
                succ[i] = self.flip()

    def flip(self):
        # calculate bias stochastic choice of 2 or 4 with p = {0.9, 0.1}
        if random.random() > 0.9 :
                return 2
        return 4    