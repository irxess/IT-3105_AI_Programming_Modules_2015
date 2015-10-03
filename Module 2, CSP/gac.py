from copy import deepcopy
import itertools
from state import *
from constraintInstance import CI
import pdb
import sys

class GAC():
    def __init__(self, state):
        """
        Push all valid combinations of x,c onto the queue
        """
        state.updateCIList()
        self.queue = []
        for ci in state.ciList:
            # for i in range( len(ci.variables) ):
            #     queue.append( (i, ci) )
            self.queue.append( (0, ci) )
        # return queue
        self.state = state


    def revise(self, x, c):
        """
        Retain all x in the domain if there exists an y in the other domain
        that satisfies the constraint. Remove all others.
        """
        # call this for each variable in state.undecidedVariables
        # call for each constraint
        revised = False
        toBeRemovedFromDomain = []
        vi = c.variables[x]
        for value_i in vi.domain:
            satisfied = False
            if len(vi.neighbors)==0:
                satisfied = True
            for y in vi.neighbors:
                print('comparing', value_i, 'with', y)
                satisfied = False
                for value_j in y.domain:
                    if self.isSatisfied( (value_i, value_j), c.constraint ):
                        satisfied = True
                if not satisfied:
                    revised = True
                    toBeRemovedFromDomain.append( value_i )
        for ele in toBeRemovedFromDomain:
            print('Remove', ele, 'from', vi.domain, 'after comparing it')
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
                print('adding stuff to queue')
                # assume all variables are in all constraints
                for c in state.constraintList:
                    for vi in ci.variables[index].neighbors:
                        newCI = CI(c, [vi, ci.variables[index]])
                        self.queue.append( (0,newCI) )
                print(self.queue)
        return state



    def isSatisfied(self, pair, constraint):
            # useless comment
            return constraint(pair[0], pair[1])


    def rerun(self, state):
        # assume all variables are in all constraints
        self.state = state
        self.queue = []
        print(len(state.viList))
        for vi in state.viList:
        # for vi in state.undecidedVariables:
            print(vi.neighbors)
            for vi_n in vi.neighbors:
                for c in state.constraintList:
                    newCI = CI( c, [vi,vi_n] )
                    self.queue.append( (0,newCI) )
        return self.domainFiltering( state )
        