from copy import deepcopy
import itertools
from state import *
from constraintInstance import CI

class GAC():

    """GAC is a generalazied arc consistency algoritm that
        outputs arc-consistent doamins for each variable v in given variable set
        cnet is given to GAC as a representation of 
        constraints with components (variabels, domain, constarints)
        domain is a dictionary and domain[v] returns a list of values(the domain of key v)
        Variable v is a vertex.
        Output: queue consists of arc-consistent domains for each variable
        """

    def __init__(self, state):
        # super(GAC, self).__init__() 
        self.queue = [] # queue of requests(focal variable, its constraints), initially all requests
        self.constraints = state.ciList
        self.variables = state.viList

    def initialize(self):
        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))

    def filterDomain(self):         
        while len(self.queue):
            (x, c) = self.queue.pop()
            if self.reviseStar(x, c):
                if len( x.domain ) == 0:
                    return False
            # check the other variable in the constraint
            for k in c.variables:
                if k != x:
                    self.queue.append(k, getConstraints(k))
        return State(self.variables, self.constraints)


# reduce x's domain
    def reviseStar(self, x, c):
        revised = False
        print('-------')
        print(x)
        print(c.variables)
        pairs = self.getPairs(x, c.variables)
        for pair in pairs:
            if not self.isSatisfied(pair, c):
                x.domain.pop(pair[0])
                self.reduceDomain(x, pair[0])
                revised = True
        return revised

# assumption: a variable assignment/singleton domain
    def rerun(self, assumption):
        for c in getConstraints(assumption):
            for k in c.variables:
                if k != assumption:
                    self.queue.append((k, getConstraints(k)))
        self.filterDomain()
        

    def isSatisfied(self, pair, constraint):
        print(pair)
        return constraint.constraint(pair[0], pair[1])

        
    def getPairs(self, x, y):
        return itertools.product(x.domain, [k.domain for k in y] )


    def getConstraints(self, variable):
        constraints = []
        for c in self.constraints:
            if variable in c.variables:
                constraints.append(c)
        return constraints

# updates self.variables after reducing 
    def reduceDomain(self, vi, item):
        for v in self.variables:
            if v == vi:
                vi.domain.pop(item)

    # for k in set(self.constarints).difference(c):
    #     if x in k.variables:
    #         for v in k.variables:
    #             if v == x :
    #                 continue
    #             self.queue.append(v, k)
    # for k in set(self.cnet.getArcsOf(i).difference(i, j)):
    #     self.queue.append(k[0], i)
