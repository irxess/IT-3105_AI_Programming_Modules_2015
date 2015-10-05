from AStarGAC import Astar_GAC
from coloringState import ColoringState


class VertexColoring(Astar_GAC): 
    """Astar_GAC integrates Astar and GAC"""
    #both
    def __init__(self, variables, domains, expressions):
        super(VertexColoring, self).__init__(variables, domains, expressions)


    def createNewState( self, variables, constraints):
        return ColoringState(variables, constraints)
