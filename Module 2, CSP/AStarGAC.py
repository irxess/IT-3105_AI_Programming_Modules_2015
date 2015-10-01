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
        stateCounter = 1
        self.GAC.initialize()
        self.currentState = self.GAC.filterDomain()

        if isSolution(self.currentState):
            return self.currentState

        elif isContradictory(self.currentState):
            print( 'Dismissed. There is no solution!')
            return False

        self.iterateSearch()


    def iterateSearch(self):

        # if not isContradictory(newState) and not isSolution(newState):
            # AStar må returnere den noden vi popper
            # − Popping search nodes from the agenda 
            curr = self.currentState 
            self.currentState = AStar(self.currentState, 'best_first').iterateAStar()
            self.currentState.parent = curr#er det nødvendig?

            
            # − Generating their successor states (by making assumptions)
            successors = self.makeAssumption(self.currentState)
            # − Enforcing the assumption in each successor state by reducing
            for succ in successors:
                # RERUN GAC instead?
                gac = GAC(currentState)
                gac.initialize()
                gac.filterDomain()

            # the domain of the assumed variable to a singleton set − Calling GAC−Rerun on each newly−generated state
            GAC.rerun(newState) #??

            # − Computing the f , g and h values for each new state ,
            # where h is based on the state of the CSP after the call to GAC−Rerun.
            h = newState.computeHeuristic()
            g = newState.

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
    # making successor list by assumptions.
    def makeAssumption(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        succStates = []
        betterVI = sorted(state.variables, key=lambda v: len(v.domain), reverse=True).pop()
        if betterVI.domain:
            # how many assumption should I make? 
            for d in betterVI.domain:
                betterVI.domain = d
                succ = state.setDomain(betterVI, assignment)
                succStates.append(succ)
        return succStates
        
##### TODO : implement generateSucc
# Should this be defined here or in cnetGraph?
    def generateSucc(self, assumption):
        # generate succ. states by assumptions->
        pass



