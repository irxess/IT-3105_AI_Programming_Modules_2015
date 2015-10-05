import os
import sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/AStar') )
sys.path.append( os.path.abspath('../Common/GAC') )
from astar import AStar
from cnet import CNET
from gac import GAC
from graph import Graph
from variableInstance import VI
from constraintInstance import CI
import itertools
from abc import ABCMeta, abstractmethod

class Astar_GAC(Graph): 
    """Astar_GAC integrates Astar and GAC"""
    #both
    def __init__(self, variables, domains, expressions):
        super(Astar_GAC, self).__init__()
        self.cnet = CNET(variables, domains, expressions)
        self.currentState = self.initializeState(self.cnet)
        self.gac = GAC(self.currentState)
        self.Astar = AStar(self)


    @abstractmethod
    def createNewState( self, variables, constraints):
        pass 


    def initializeState(self, cnet):
        """in initState each variable has its full domain. It will be set as root node
        initilizes cnet"""
        s = self.createNewState( cnet.variables, cnet.constraints )
        s.update('start')
        self.startNode = s
        self.stateCounter = 0
        self.nofAssumption = 0
        self.nofExpanded = 0
        return s 


    def search(self):
        self.currentState = self.gac.domainFiltering(self.currentState)
        self.stateCounter += 1
        
        if self.currentState.isSolution():
            self.printStatistics(self.currentState)
            return self.currentState

        return self.iterateSearch()


    def iterateSearch(self):
            prev = self.currentState 
            if prev.isSolution():
                return prev

            self.currentState = self.Astar.iterateAStar()
            # self.currentState.updateColors()
            self.stateCounter += 1
            self.currentState.parent = prev #used for backtracking to find 'shortest path' for statistics
            self.nofExpanded = self.Astar.nofExpandedNodes
            if self.currentState.isSolution():
                self.printStatistics(self.currentState)
                return self.currentState

            self.currentState = self.gac.domainFiltering(self.currentState)
            return self.currentState


    def makeAssumption(self, newVI, parentState):
        """Generate one successor, and make sure all pointers are correct"""

        newVertices = {}
        newVIList = []
        for vi in parentState.viList:
            viID = vi.getID()
            tmpVI = VI(viID, vi.domain.copy())
            newVertices[viID] = tmpVI
            newVIList.append( tmpVI )

        for vi in parentState.viList:
            viID = vi.getID()
            for neighbor in vi.neighbors:
                n = newVertices[ neighbor.getID() ]
                newVertices[viID].add_neighbor( n )

        for vi in newVIList:
            if vi.getID() == newVI.getID():
                newVIList.remove(vi)
                newVIList.append(newVI)
            else:
                for vi_n in vi.neighbors:
                    if vi_n.getID() == newVI.getID():
                        vi.neighbors.remove(vi_n)
                        vi.neighbors.append(newVI)

        succ = self.createNewState(newVIList, parentState.constraintList)
        succ.parent = parentState
        succ.updateUndecided() # maybe not needed

        succ.ciList = []
        constraints = self.cnet.getConstraints()
        for v in succ.undecidedVariables:
            for n in v.neighbors:
                for c in constraints:
                    succ.ciList.append( CI(c,[v,n]) )

        return succ


    def generateSucc(self, state):
        """ make a guess. start gussing value for variables with min. domain length"""
        succStates = []
        finishedVIs = []
        varsCopy = state.undecidedVariables.copy()

        if not len(varsCopy):
            return []

        otherVIs = sorted(varsCopy, key=lambda v: len(v.domain), reverse=True)
        betterVI = otherVIs.pop()

        if betterVI.domain:
            initID = betterVI.getID()
            for d in betterVI.domain:
                newVI = VI( initID, [d])
                newVI.neighbors = betterVI.neighbors.copy()
                successor = self.makeAssumption(newVI, state)

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


    def countColorLess(self, state):
        nofColorLess = 0
        for vi in state.viList:
            if len(vi.domain) != 1:
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


    # Needed for Graph
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


