from AStarGAC import Astar_GAC
from nstate import NonogramState


class NonogramSolver(Astar_GAC): 
    """NonogramSolver is a specializesd Astar_GAC"""
    #both
    def __init__(self, variables, domains, expressions):
        super(NonogramSolver, self).__init__(variables, domains, expressions)


    def createNewState( self, variables, constraints):
        return NonogramState(variables, constraints)
