import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *
from state import State


class ColoringState(State):

    def __init__(self, variables, constraints):
        super(ColoringState, self).__init__(variables, constraints)


    def __repr__(self):
        string = 'State: ID:%s, f:%s, constraints:%s, variables:\n%s\n' %(self.id, self.f, len(self.ciList), len(self.viList))
        for vi in self.viList:
            string += vi.__repr__() + '\n'
        return string


    def getVerticesToDraw(self):
        self.updateColors()
        return self.viList


    def updateColors(self):
        for vi in self.viList:
            if len(vi.domain) == 1:
                vi.color = vi.domain[0]
            else:
                vi.color = (0,0,0)


    def isContradictory(self):
        for vi in self.viList:
            if len( vi.domain ) == 0:
                return True
            if len( vi.domain ) == 1:
                for nb in vi.neighbors:
                    if vi.color == nb.color and vi.color != (0,0,0):
                        return True
        return False            


    def isSolution(self):
        for vi in self.viList:
            if len( vi.domain ) != 1:
                return False
            for nb in vi.neighbors:
                if vi.color == nb.color:
                    return False
        return True
