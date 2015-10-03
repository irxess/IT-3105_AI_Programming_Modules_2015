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
import time


class Astar_GAC(Graph): 
    """Astar_GAC integrates Astar and GAC"""

    def __init__(self, variables, domains, expressions):
        self.cnet = CNET(variables, domains, expressions)
        self.currentState = self.initializeState(self.cnet)
        self.gac = GAC(self.currentState)
        self.Astar = AStar(self)
        self.startNode = None
        self.goalNode = None


    def initializeState(self, cnet):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""

        s = State(cnet.variables, cnet.ciList, cnet.constraints)  
        s.update('start')
        self.startNode = s
        self.stateCounter = 0
        return s 


    def search(self):
        self.currentState = self.gac.domainFiltering(self.currentState)
        self.stateCounter += 1
        # if not self.currentState:
        #     print("Inconsistent")
        #     return False

        # if self.isSolution(self.currentState):
        #     return self.currentState
        # self.currentState = self.gac.filterDomain()
        self.stateCounter += 1
        return self.iterateSearch()


    def iterateSearch(self):
        # if not isContradictory(newState) and not isSolution(newState):
            # pdb.set_trace()

            curr = self.currentState 
            # if not curr:
            #     print("Inconsistent")
            #     return None

            if self.isSolution(curr):
                return curr


            self.currentState = self.Astar.iterateAStar()
            self.currentState.updateColors()
            print('Iteration', self.stateCounter, 'of Astar done')
            self.stateCounter += 1
            self.currentState.parent = curr #used for backtracking to find 'shortest path' for statistics

            if self.isSolution(curr):
                return curr
            # if not self.gac.domainFiltering(self.currentState):
            #     self.currentState = curr
            self.currentState = self.gac.domainFiltering(self.currentState)
            return self.currentState          


    def isContradictory(self, state):
        for vi in state.viList:
            if len( vi.domain ) == 0:
                return True
            if len( vi.domain ) == 1:
                for nb in vi.neighbors:
                    if vi.color == nb.color and vi.color != (0,0,0):
                        return True
        return False            


    def isSolution(self, state):
        for vi in state.viList:
            if len( vi.domain ) != 1:
                return False
            for nb in vi.neighbors:
                if vi.color == nb.color:
                    return False
        print('found solution')
        return True


    def makeAssumption(self, newVI, parentState):
        # newVIList = parentState.viList.copy()

        # lage dict av nye vertices
        newVertices = {}
        newVIList = []
        for vi in parentState.viList:
            tmpVI = VI(vi.x, vi.y, vi.domain.copy())
            newVertices[(vi.x,vi.y)] = tmpVI
            newVIList.append( tmpVI )

        # gå gjennom neighbors, pek til nye vertices
        # for i in range( (len(parentState.viList)) ):
        #     for neighbor in parentState.viList[i]:
        #         n = newVertices[ (neighbors.x, neighbors.y) ]
        #         newVIList[i].neighbors.append( n )

        for vi in parentState.viList:
            for neighbor in vi.getNeighbors():
                n = newVertices[ (neighbor.x, neighbor.y) ]
                newVertices[vi.x,vi.y].add_neighbor( n )


        for vi in newVIList:
            if vi.x == newVI.x and vi.y == newVI.y:
                newVIList.remove(vi)
                newVIList.append(newVI)
            else:
                for vi_n in vi.neighbors:
                    if vi_n.x == newVI.x and vi_n.y == newVI.y:
                        vi.neighbors.remove(vi_n)
                        vi.neighbors.append(newVI)

        succ = State(newVIList, [], parentState.constraintList)
        succ.parent = parentState
        succ.updateUndecided() # maybe not needed

        succ.ciList = []
        constraints = self.cnet.getConstraints()
        for v in succ.undecidedVariables:
            for n in v.neighbors:
                for c in constraints:
                    # succ.ciList.append( CI(c,[v,n.currentVI]) )
                    succ.ciList.append( CI(c,[v,n]) )

        succ.updateColors()
        return succ


    # making successor list by assumptions.
    def generateSucc(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        state.updateColors()
        if self.isContradictory(state):
            return []
        if self.isSolution(state):
            return []
        
        succStates = []
        finishedVIs = []
        varsCopy = state.undecidedVariables.copy()
        otherVIs = sorted(varsCopy, key=lambda v: len(v.domain), reverse=True)
        betterVI = otherVIs.pop()

        if betterVI.domain:
            # how many assumption should I make? 
            for d in betterVI.domain:
                newVI = VI( betterVI.x, betterVI.y, [d])
                newVI.neighbors = betterVI.neighbors.copy()
                # betterVI.currentVI = newVI
                successor = self.makeAssumption(newVI, state)

                # runs gac.rerun on newly guessed state before adding
                succStates.append( self.gac.rerun(successor) )
        return succStates


    def getGoal(self):
        return None

