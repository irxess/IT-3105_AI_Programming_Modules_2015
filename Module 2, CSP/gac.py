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
        self.constraints = deepcopy(state.ciList)
        self.variables = deepcopy(state.viList)

    def initialize(self):
        print('Put all constraints + variables in the GAC queue')
        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))

    def filterDomain(self): 
        print(self.constraints)        
        while len(self.queue):
            (x, c) = self.queue.pop()
            if self.reviseStar(x, c):
                if len( x.domain ) == 0:
<<<<<<< HEAD
                    return False
            # check the other variable in the constraint
            for k in c.variables:
                if k != x:
                    self.queue.append((k, self.getConstraints(k)))
=======
                    return None
            # # check the other variable in the constraint
            # don't think we need this
            # for k in c.variables:
            #     if k != x:
            #         for c in self.getConstraints(k):
            #             self.queue.append( (k, c) )
>>>>>>> 8d4d9d8224c3028e2186679070dbfcd6642666e6
        return State(self.variables, self.constraints)

# reduce x's domain
    def reviseStar(self, x, c):
        revised = False
<<<<<<< HEAD
        print('-------')
        print(x)
        pairs = self.getPairs(x, c.variables)
        for pair in pairs:
            if not self.isSatisfied(pair, c):
                x.domain.pop(pair[0])
                # self.reduceDomain(x, pair[0])
=======
        pairs = self.getPairs(x, c.variables)
        for listOfPairs in pairs:
            satisfiedCount = 0
            for pair in listOfPairs:
                if self.isSatisfied(pair, c):
                    satisfiedCount += 1

            if satisfiedCount == 0:
                # remove the variable from the domain,
                # as there is no combination with the variable 
                # where the constraint is satisfied
                print('remove', pair[0], 'from the domain of', x)
                x.domain.remove(pair[0])
                self.reduceDomain(x, pair[0])
>>>>>>> 8d4d9d8224c3028e2186679070dbfcd6642666e6
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
        return constraint.constraint(pair[0], pair[1])

        
    def getPairs(self, x, y):
        pairs = []
        for k in y:
            if k != x:
                for var in x.domain:
                    pairs.append( list(itertools.product([var], k.domain)) )
        return pairs


    def getConstraints(self, variable):
        constraints = []
        for c in self.constraints:
            print(c)
            if variable in c.variables:
                constraints.append(c)
        return constraints

# updates self.variables after reducing 
    def reduceDomain(self, vi, item):
        for v in self.variables:
            if v == vi:
                print(v.domain)
                print(item)
                vi.domain.remove(item)
