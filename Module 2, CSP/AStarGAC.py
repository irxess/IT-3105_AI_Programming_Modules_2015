import os
import sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/') )
from astar import AStar
from cnet import CNET
from gac import GAC
from state import State
from graph import Graph
from variableInstance import VI
from constraintInstance import CI
import pdb


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

        s = State(cnet.variables, cnet.ciList)  
        s.update('start')
        self.startNode = s
        self.stateCounter = 0
        return s 


    def search(self):
        # refine initState
        print('Starting A* GAC search')
        # self.gac.initialize()
        print('Filtering initial domain')
        self.currentState = self.gac.filterDomain(self.currentState)
        self.stateCounter += 1
        # if not self.currentState:
        #     print("Inconsistent")
        #     return False

        # if self.isSolution(self.currentState):
        #     return self.currentState

        # elif self.isContradictory(self.currentState):
        #     print( 'Dismissed. There is no solution!')
        #     return False
        return self.iterateSearch()


    def iterateSearch(self):
        # if not isContradictory(newState) and not isSolution(newState):
            curr = self.currentState 
            # pdb.set_trace()
            if not curr:
                print("Inconsistent")
                return False

            if self.isSolution(curr):
                return curr

            elif self.isContradictory(curr):
                print( 'Dismissed. There is no solution!')
                return False

            print('\n\nStarting Astar iteration')
            self.currentState = self.Astar.iterateAStar()
            print('Iteration', self.stateCounter, 'of Astar done')
            self.stateCounter += 1
            self.currentState.parent = curr #used for backtracking to find 'shortest path' for statistics
            print('A* found', self.currentState)            
            return self.currentState          


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


    def makeAssumption(self, VIs, parentState):
        succ = State(VIs, []) # todo: should I copy?
        succ.parent = parentState
        succ.pairs = []

        constraints = self.cnet.getConstraints()
        for v in succ.viList:
            for n in v.variable.neighbors:
                for c in constraints:
                    succ.ciList.append( CI(c,[v,n.currentVI]) )
                    
        return succ


    # making successor list by assumptions.
    def generateSucc(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        succStates = []
        print('Generating successors')

        finishedVIs = []
        otherVIs = sorted(state.viList, key=lambda v: len(v.domain), reverse=True)
        betterVI = otherVIs.pop()
        while len( betterVI.domain ) == 1:
            finishedVIs.append(betterVI)
            betterVI = otherVIs.pop()

        if betterVI.domain:
            # how many assumption should I make? 
            for d in betterVI.domain:
                # print('entry in domain', d)
                newVI = VI( betterVI.variable, [d])
                successor = self.makeAssumption([newVI]+otherVIs+finishedVIs, state)

                # runs gac.rerun on newly guessed state before adding
                print( 'successor before gac rerun', successor)
                succStates.append( self.gac.rerun(successor, newVI) )
                print( 'successor after gac rerun', succStates[-1])
        # print("succStates",[succVar for succVar in succStates])
        return succStates


    def getGoal(self):
        return None

