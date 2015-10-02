from copy import deepcopy
import itertools
from state import *
from constraintInstance import CI
import pdb
import sys

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
        # self.state = state

        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))
        state.pairs = self.queue


    def filterDomain(self, state):           
        while len(self.queue):
            (x, c) = self.queue.pop()

            if self.reviseStar(x, c):
                if len( x.domain ) == 0:
                    print ("inconsistency", x.domain, "reduced to empty")
                    return None
                print('domlengde til x: ', len(x.domain))
                self.rerun(state)
        print("vars in currState after filterDomain:", self.variables)
        return state
            # # check the other variable in the constraint
            # do we need this?
            # for k in c.variables:
            #     if k != x:
            #         for c in self.getConstraints(k):
            #             self.queue.append( (k, c) )
            
        # assumption.variables = self.variables
        # assumption.constraints = self.constraints
        # print('Domain filtered:\n', self.variables)
        # return assumption


# reduce x's domain
    def reviseStar(self, x, c):
        revised = False
        print('Starting REVISE*')
        print(x)
        print(c)
        pairs = self.getPairs(x, c.variables)

        for listOfPairs in pairs:
            satisfiedCount = 0
            # print('""""""""""""""""""""""""""""""""""""""""""""""')
            # print(listOfPairs)
            for pair in listOfPairs:
                if self.isSatisfied(pair, c):
                    satisfiedCount += 1
                # else:

                #     state.pairs.remove(pair)
            if satisfiedCount == 0:
                # remove the variable from the domain,
                # as there is no combination with the variable 
                # where the constraint is satisfied
                print('should remove stuff')
                print(listOfPairs)
                sys.exit()
                # print('Remove', pair[0], 'from the domain of', x)
                # x.domain.remove(pair[0])
                # self.reduceDomain(x, pair[0])
                revised = True
        return revised

# assumptionState: state with a variable assignment/singleton domain
    # add todoRevise's to the queue,
    # should discover it 
    def rerun(self, assumptionState):
        # pdb.set_trace()
        print('starting rerun')
        # for c in self.getConstraints(assumptionState.ciList):
        for c in assumptionState.ciList:
            for x in c.variables:
                # print('x != assumption',x != assumption)
                # if x != assumptionState:
                #     # does this code run at all?
                #     self.queue.append((k, self.getConstraints(k)))
                print(x)
                self.queue.append( (x,c) )
        print('length', len(self.queue))
        # sys.exit()
        return self.filterDomain(assumptionState)


    def isSatisfied(self, pair, constraint):
        return constraint.constraint(pair[0], pair[1])
        

    def getPairs(self, x, y):
        pairs = [] 
        for k in y:
            if k != x:
                for value in x.domain:
                    pairs.append( list(itertools.product([value], k.domain)) )
        return pairs

# get all constraints applying to a certain variable
    def getConstraints(self, variable):
        constraints = []
        for c in self.constraints:
            # print(c)
            if variable in c.variables:
                constraints.append(c)
        return constraints


# updates self.variables after reducing 
    def reduceDomain(self, vi, item):
        for v in self.variables:
            if v == vi:
                print("vi.domain", vi.domain)
                print(item)
                print('v.domain', v.domain)
                v.domain.remove(item)

        