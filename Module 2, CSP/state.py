import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *

class State(AbstractNode):

    def __init__(self, variables, ciList, constraints):
        super(State, self).__init__()
        self.constraintList = constraints
        self.ciList = ciList
        self.viList = variables
        self.id = uuid.uuid4()
        self.g = 0 # we don't care about the distance walked
        self.parent = None
        self.state = 'unvisited'
        self.undecidedVariables = []
        # self.updateUndecided()
        self.updateCIList()


    def __repr__(self):
        string = 'State: ID:%s, f:%s, constraints:%s, variables:%s\n' %(self.id, self.f, len(self.ciList), len(self.viList))
        for vi in self.viList:
            string += vi.__repr__() + '\n'
        return string


    def updateUndecided(self):
        self.undecidedVariables = []
        for v in self.viList:
            if len(v.domain) != 1:
                self.undecidedVariables.append(v)


    def updateCIList(self):
        self.updateUndecided()
        self.ciList = []
        for c in self.constraintList:
            for v in self.undecidedVariables:
                for n in v.neighbors:
                    self.ciList.append( CI(c, [v,n]) )


    # return an ID unique for this state
    def getID(self):
        return self.id


    def cost(self, node):
        nodeID = node.getID()
        if self.id == nodeID:
            return 0
        return 1


    def estimateDistance(self, goal):
        # find heuristic
        self.h = 0
        for v in self.viList:
            self.h += len(v.domain) - 1 
        super(State, self).estimateDistance()


    def getVerticesToDraw(self):
        vertices = []
        for vi in self.viList:
            if len(vi.domain) == 1:
                vi.color = vi.domain[0]
            else:
                vi.color = (0,0,0)
            vertices.append(vi)
        return vertices


