import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *

class State(AbstractNode):

    def __init__(self, variables, domainList):
        super(State, self).__init__()
        self.ciList = 
        self.viList = 
        self.id = uuid.uuid4()
        self.g = 0 # we don't care about the distance walked


    # return an ID unique for this state
    def getID(self):
        return self.id


    def cost(self, node):
        nodeID = node.getID()
        if self.id == nodeID:
            return 0
        return 1


    def estimateDistance(self, g):
        # find heuristic
        self.h = 0
        for v in self.viList:
            self.h += len(v.domain())
        super(State, self).estimateDistance()