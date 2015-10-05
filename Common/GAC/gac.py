from copy import deepcopy
import itertools
from state import *
from constraintInstance import CI

class GAC():
    def __init__(self, state):
        """
        Push all valid combinations of x,c onto the queue
        """
        state.updateCIList()
        self.queue = []
        for ci in state.ciList:
            self.queue.append( (0, ci) )
        self.state = state
        self.unSatisfied = 0


    def revise(self, x, c):
        """
        Retain all x in the domain if there exists an y in the other domain
        that satisfies the constraint. Remove all others.
        """
        revised = False

        toBeRemovedFromDomain = []
        vi = c.variables[x]

        for value_i in vi.domain:
            satisfied = False
            if len(vi.neighbors)==0:
                satisfied = True
            for y in c.variables[1:]:
                satisfied = False
                for value_j in y.domain:
                    if vi.isSatisfied( (value_i, value_j), y, c.constraint ):
                        satisfied = True
                    else:
                        self.unSatisfied += 1
                if not satisfied:
                    revised = True
                    toBeRemovedFromDomain.append( value_i )
        for ele in toBeRemovedFromDomain:
            if ele in vi.domain:
                vi.domain.remove(ele)
        return revised


    def domainFiltering(self, state):
        """
        Queue masse sjekker.
        Kjør revise på alle i queue i rekkefølge.
        Hvis revise fjernet noe: 
            queue alle komboer hvor naboene er hovedvariabelen
        """
        self.state = state
        while len(self.queue) > 0:
            index, ci = self.queue.pop()
            revised = self.revise(index, ci)
            if revised:
                # assume all variables are in all constraints
                for c in state.constraintList:
                    for vi in ci.variables[index].neighbors:
                        newCI = CI(c, [vi, ci.variables[index]])
                        self.queue.append( (0,newCI) )
        return state


    def rerun(self, state):
        # assume all variables are in all constraints
        self.state = state
        self.queue = []
        for vi in state.viList:
            for vi_n in vi.neighbors:
                for c in state.constraintList:
                    newCI = CI( c, [vi,vi_n] )
                    self.queue.append( (0,newCI) )
        return self.domainFiltering( state )
        
