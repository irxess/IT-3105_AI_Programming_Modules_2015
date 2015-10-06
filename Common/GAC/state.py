import os, sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/AStar') )
import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *
from abc import ABCMeta, abstractmethod


class State(AbstractNode):
    __metaclass__ = ABCMeta

    def __init__(self, variables, constraints):
        super(State, self).__init__()
        self.constraintList = constraints
        self.viList = variables
        self.id = uuid.uuid4()
        self.g = 0 # we don't care about the distance walked
        self.parent = None
        self.state = 'unvisited'
        self.undecidedVariables = []
        self.updateCIList()


    def __repr__(self):
        string = 'State: ID:%s, f:%s, constraints:%s, variables:\n%s\n' %(self.id, self.f, len(self.ciList), len(self.viList))
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


    def estimateDistance(self, goal):
        self.h = 0
        for v in self.viList:
            self.h += len(v.domain) - 1 
        super(State, self).estimateDistance()


    def getID(self):
        return self.id


    @abstractmethod
    def isContradictory(self):
        pass


    @abstractmethod
    def isSolution(self):
        pass


    def tieBreaking(self, goal):
        countVarLowestDomainLength = 0
        for variable in self.viList:
            if len(variable.domain) == 1:
                countVarLowestDomainLength += 1
        return countVarLowestDomainLength
