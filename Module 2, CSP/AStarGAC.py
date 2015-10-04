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
import time, itertools

start = time.time()
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
        self.nofAssumption = 0
        self.nofExpanded = 0
        return s 


    def search(self):
        self.currentState = self.gac.domainFiltering(self.currentState)
        self.stateCounter += 1
        
        if self.isSolution(self.currentState):
            self.printStatistics(self.currentState)
            return curr

        

        # if self.isSolution(self.currentState):
        #     return self.currentState
        # self.currentState = self.gac.filterDomain()
        return self.iterateSearch()


    def iterateSearch(self):

            curr = self.currentState 

            self.currentState = self.Astar.iterateAStar()
            self.currentState.updateColors()
            print('Iteration', self.stateCounter, 'of Astar done')
            self.stateCounter += 1
            self.currentState.parent = curr #used for backtracking to find 'shortest path' for statistics
            self.nofExpanded += self.Astar.nofExpandedNodes
            if self.isSolution(curr):
                self.printStatistics(curr)
                return curr

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

        newVertices = {}
        newVIList = []
        for vi in parentState.viList:
            tmpVI = VI(vi.x, vi.y, vi.domain.copy())
            newVertices[(vi.x,vi.y)] = tmpVI
            newVIList.append( tmpVI )

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
                    succ.ciList.append( CI(c,[v,n]) )

        succ.updateColors()
        return succ


    # making successor list by assumptions.
    def generateSucc(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        # state.updateColors()
        # if self.isContradictory(state):
        #     return []
        # if self.isSolution(state):
        #     return []
        
        succStates = []
        finishedVIs = []
        varsCopy = state.undecidedVariables.copy()

        if not len(varsCopy) :
            return []

        otherVIs = sorted(varsCopy, key=lambda v: len(v.domain), reverse=True)
        betterVI = otherVIs.pop()

        if betterVI.domain:
            # how many assumption should I make? 
            for d in betterVI.domain:
                newVI = VI( betterVI.x, betterVI.y, [d])
                newVI.neighbors = betterVI.neighbors.copy()
                # betterVI.currentVI = newVI
                successor = self.makeAssumption(newVI, state)
                self.nofAssumption += 1

                # runs gac.rerun on newly guessed state before adding
                succStates.append( self.gac.rerun(successor) )
            return succStates
        else:
            return []


# Not complete : TODO
    def printStatistics(self, state):
        print ( 'The number of unsatisfied constraints = ', self.countUnsatisfiedConstraints(state), '\n' )
        print ( 'The total number of verticies without color assignment = ', self.countColorLess(state), '\n' )
        print ( 'The total number of nodes in search tree = ', self.stateCounter, '\n' )
        print ( 'The total number of nodes poped from agenda and expanded = ', self.nofExpanded, '\n' )
        print ( 'The length of the path = ', self.nofAssumption ,'\n')
        return


        
    def countColorLess(self, state):
        nofColorLess = 0
        for vi in state.viList:
            if vi.domain == (0, 0, 0):
                nofColorLess += 1
        return nofColorLess
        
                
    def countUnsatisfiedConstraints(self, state):
        unsatisfied = 0
        varList = state.viList
        for c in state.ciList:
            for var in varList: 
                if var in c.variables:
                    if self.countInconsistentDomainValues(var, c) or not len(var.domain):
                        unsatisfied += 1
        return unsatisfied
                    
                    
    def getGoal(self):
        return None

    def countInconsistentDomainValues(self, x, c):
        pairs = []
        nofInconsistency = 0
        for k in c.variables:
            for value in x.domain:
                pairs.extend( list(itertools.product([value], k.domain)) )
        
        for p in pairs :
            if not c.constraint( p[0], p[1] ):
                nofInconsistency += 1

        return nofInconsistency

        
