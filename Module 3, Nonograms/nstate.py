import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *
from state import State

class NonogramState(State):

    def __init__(self, variables, constraints):
        super(NonogramState, self).__init__(variables, constraints)


    def __repr__(self):
        string = 'State: ID:%s, f:%s, constraints:%s, variables:\n%s\n' %(self.id, self.f, len(self.ciList), len(self.viList))
        for vi in self.viList:
            string += vi.__repr__() + '\n'
        return string


    def isContradictory(self):
        for vi in self.viList:
            if len( vi.domain ) == 0:
                return True
            if len( vi.domain ) == 1:
                for nb in vi.neighbors:
                    if nb.domain[0][vi.index] != vi.domain[0][nb.index]:
                        return True
        return False            


    def isSolution(self):
        for vi in self.viList:
            if len( vi.domain ) != 1:
                return False
        return True

