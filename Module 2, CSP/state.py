import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *

class State(AbstractNode):

    def __init__(self, variables, constraints):
        super(State, self).__init__()
        self.ciList = constraints
        self.viList = variables
        self.id = uuid.uuid4()
        self.g = 0 # we don't care about the distance walked
        self.parent = None #not sure if needed
        self.state = 'open'


    def getDomain(self, vi):
        return vi.domain


    def setDomain(self, value):
        vi.domain = value

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


    def getVerticesToDraw():
        vertices = []
        for vi in self.viList:
            if len(vi.domain) == 1:
                vi.variable.color = vi.domain[0]
            else:
                vi.variable.coolor = (0,0,0)
            vertices.append(vi.variable)

