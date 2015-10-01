import os
import sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/') )
from astar import AStar
from cnet import CNET
from gac import GAC
from state import State
from graph import Graph

class Astar_GAC(Graph): 
    """Astar_GAC integrates Astar and GAC"""
    def __init__(self, domains, expressions):
        # cnet : cnet of searh problem
        self.cnet = CNET(csp.domains, csp.expressions)
        self.currentState = initializeState(self.cnet)
        self.gac = GAC(self.currentState)
        self.Astar = AStar(self.currentState)

    def initializeState(self, state):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""
        s = State(state.variables, state.constraints)  
        s.update('start')
        return s 


    def search(self):
        # refine initState
        stateCounter = 1
        self.gac.initialize()
        self.currentState = self.gac.filterDomain()

        if isSolution(self.currentState):
            return self.currentState

        elif isContradictory(self.currentState):
            print( 'Dismissed. There is no solution!')
            return False
        self.iterateSearch()

    def iterateSearch(self):
        # if not isContradictory(newState) and not isSolution(newState):
            # − Popping search nodes from the agenda 
            curr = self.currentState 
            self.currentState = self.Astar.iterateAStar()
            self.currentState.parent = curr#er det nødvendig?

            # − Generating their successor states (by making assumptions)
            successors = self.makeAssumption(self.currentState)

            # − Enforcing the assumption in each successor state by reducing
            for succ in successors:
                succGac = GAC(succ)
                succGac.initialize()
                succGac.filterDomain()

            # the domain of the assumed variable to a singleton set − Calling GAC−Rerun on each newly−generated state
            GAC.rerun(self.currentState) #??
            # − Computing the f , g and h values for each new state ,
            # where h is based on the state of the CSP after the call to GAC−Rerun.
            h = newState.computeHeuristic()

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
    def generateSucc(self, state):
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
    # def generateSucc(self, assumption):
    #     # generate succ. states by assumptions->
    #     pass



