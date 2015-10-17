from abc import ABCMeta, abstractmethod

class State():
    __metaclass__ = ABCMeta

    def __init__(self, grid):
        self.grid = grid
        calculateHeuristic()
        self.childNodes = []


# use that method on stack overflow
    def calculateHeuristic(self):
        self.heuristic = 0


    @abstractmethod
    def generateSuccessors(self):
        pass




class MAX(State):
    def __init__(self, grid):
        super(MAX, self).__init__(grid)


    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    def generateSuccessors(self):
        pass



class CHANCE(State):
    def __init__(self, grid):
        super(CHANCE, self).__init__(grid)
        self.probability = 0.0


    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles, with values 2 and 4.
    """
    def generateSuccessors(self):
        pass
