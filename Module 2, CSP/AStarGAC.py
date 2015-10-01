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
    def __init__(self, domains, expression):
        # cnet : cnet of searh problem
        self.cnet = CNET(csp.domains, csp.expression)
        self.currentState = self.initializeState(self.cnet)
        self.gac = GAC(self.currentState)
        self.Astar = AStar(self.currentState)
        self.stateCounter = 0

    def initializeState(self, cnet):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""
        return State(cnet.variables, cnet.constraints)        

    def search(self):
        # refine initState
        self.gac.initialize()
        self.currentState = self.gac.filterDomain()
        self.stateCounter += 1
        if isSolution(self.currentState):
            return self.currentState

        elif isContradictory(self.currentState):
            print( 'Dismissed. There is no solution!')
            return False
        self.iterateSearch()

    def iterateSearch(self):
        # if not isContradictory(newState) and not isSolution(newState):
            curr = self.currentState 
            self.currentState = self.Astar.iterateAStar()
            self.stateCounter += 1
            self.currentState.parent = curr#er det nødvendig?
            return self.currentState.viList          

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
                betterVI.domain = [d]
                succ = state.setDomain(betterVI, assignment)
                # runs gac.rerun on newly guessed state before adding 
                succStates.append(self.gac.rerun(succ))
        return succStates



