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
        self.cnet = CNET(domains, expressions)
        self.currentState = self.initializeState(self.cnet)
        self.gac = GAC(self.currentState)
        self.Astar = AStar(self)
        self.startNode = None
        self.goalNode = None

    def initializeState(self, cnet):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""

        s = State(cnet.variables, cnet.constraints)  
        s.update('start')
        self.startNode = s
        self.stateCounter = 0
        return s 


    def search(self):
        # refine initState
        print('Starting A* GAC search')
        self.gac.initialize()
        print('Filtering initial domain')
        self.currentState = self.gac.filterDomain()
        self.stateCounter += 1
        if self.isSolution(self.currentState):
            return self.currentState

        elif self.isContradictory(self.currentState):
            print( 'Dismissed. There is no solution!')
            return False
        self.iterateSearch()


    def iterateSearch(self):
        # if not isContradictory(newState) and not isSolution(newState):
            curr = self.currentState 
            print('Starting Astar')
            self.currentState = self.Astar.iterateAStar()
            print('Iteration', stateCounter, 'of Astar done')
            self.stateCounter += 1
            self.currentState.parent = curr #used for backtracking to find 'shortest path' for statistics
            return self.currentState.viList          


    def isContradictory(self, state):
        for vi in state.viList:
            if len(state.getDomain(vi)) == 0:
                return True
        return False
                

    def isSolution(self, state):
        for vi in state.viList:
            if len( state.getDomain(vi) ) != 1:
                return False
        return True

    # making successor list by assumptions.
    def generateSucc(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        succStates = []
        print('Generating successors')
        # betterVI = sorted(state.variables, key=lambda v: len(v.domain), reverse=True).pop()
        otherVIs = sorted(state.variables, key=lambda v: len(v.domain), reverse=True)
        betterVI = otherVIs.pop()

        print('Smallest domain length found', len(betterVI.domain))
        print('')
        if betterVI.domain:
            # how many assumption should I make? 
            for d in betterVI.domain:
                newVI = VI( betterVI.variables, [d])
                # betterVI.domain = [d]
                succ = State([newVI]+otherVIs, state.ciList) # todo: should I copy?
                # succ = state.setDomain(newVI, assignment)

                # runs gac.rerun on newly guessed state before adding 
                succStates.append(self.gac.rerun(succ))
        return succStates


    def getGoal(self):
        return None

