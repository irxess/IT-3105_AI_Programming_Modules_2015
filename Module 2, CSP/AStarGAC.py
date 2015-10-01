import os
import sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/') )
from astar import AStar
from cnet import CNET
from gac import GAC
from state import State

class Astar_GAC(Graph): 
    """Astar_GAC integrates Astar and GAC"""
    def __init__(self, csp):
        # cnet : cnet of searh problem
        # Do we initialize the state in this class? if not what do we do with initializeState()
        self.cnet = CNET(csp.domains, csp.expression)
        self.currentState = initializeState(self.cnet)
        self.GAC = self.createGAC(self.currentState)
        # how do we represent csp as graph as an argument to AStar?
        # we use best_first method in Astar:
        self.AStar = self.createAstar(self.graph, 'best_first')
        
    def createGAC(self, state):
        return GAC(self.initilizeState(self.cnet))

    def createAstar(self, graph, method):
        return AStar(graph, method)
  
    def initializeState(self, cnet):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""
        return State(cnet.variables, cnet.constraints)        

    def search(self):
        # refine initState
        self.GAC.initialize()
        self.GAC.filterDomain()

        if isSolution(self.currentState):
            return self.currentState

        elif isContradictory(self.currentState):
            print( 'Dismissed. There is no solution!')
            return False

        self.iterateSearch(self.currentState)


    def iterateSearch(self, newState):

        if not isContradictory(newState) and not isSolution(newState):
            
            # AStar må returnere den noden vi popper
            # − Popping search nodes from the agenda 
            newState = self.AStar.iterateAStar()
            
            # assumption: a "logical" guess for assignment
            assumption = self.makeAssumption(newState)

            # − Generating their successor states (by making assumptions)
            self.generateSucc(assumption)

            # − Enforcing the assumption in each successor state by reducing
            # the domain of the assumed variable to a singleton set − Calling GAC−Rerun on each newly−generated state
            self.GAC.rerun(newState)

            # − Computing the f , g and h values for each new state ,
            # where h is based on the state of the CSP after the call to GAC−Rerun.
            return newState.viList          

    def isContradictory(self, state):
        for d in state.domains:
            if len(d[1]) == 0:
                return True
        return False
                

    def isSolution(self, state):
        for vi in state.viList:
            if len( state.getDomain(vi) ) > 1:
                return False
        return True


    def computeHeuristic(self, state):
        heuristic = 0
        for vi in state.viList:
            l = len(vi.domain) - 1
            heuristic += l
        return heuristic

    def makeAssumption(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        betterVI = sorted(state.variables, key=lambda v: len(v.domain), reverse=True).pop()
        if betterVI.domain:
            # pick an arbitary domain value
            assignment = betterVI.domain[0]
            state.setDomain(betterVI, assignment)
        return state
        
##### TODO : implement generateSucc
# Should this be defined here or in cnetGraph?
    def generateSucc(self, assumption):
        # generate succ. states by assumptions->
        pass



