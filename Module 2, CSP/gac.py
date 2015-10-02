from copy import deepcopy
import itertools
from state import *
from constraintInstance import CI
import pdb

class GAC():

    """GAC is a generalazied arc consistency algoritm that
        outputs arc-consistent doamins for each variable v in given variable set
        cnet is given to GAC as a representation of 
        constraints with components (variables, domain, constarints)
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
        print(self.constraints)

    def initialize(self):
        print('Put all constraints + variables in the GAC queue')
        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))


    def filterDomain(self): 
        print('queue:' , self.queue)         
        while len(self.queue):

            (x, c) = self.queue.pop()
            print("todoRevise var:", (x, c))
            # er x.domain en liste?
            # pdb.set_trace()

            # print(hasattr(c, 'variables'))#false
            # print(hasattr(c, 'constraint'))#false
            # print(hasattr(x, 'domain'))#true

            if hasattr(c, 'variables'):
                v = c.variables
                print(v)
            
            if self.reviseStar(x, c):
                if len( x.domain ) == 0:
                    print ("inconsistency", x.domain, "reduced to empty")
                    return False
                print('domlengde til x: ', len(x.domain))
                self.rerun(x)
        print("vars in currState after filterDomain:", self.variables)
        return self.variables
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
        # pdb.set_trace()
        print('c.variables',c.variables)
        pairs = self.getPairs(x, c.variables)
        for listOfPairs in pairs:
            satisfiedCount = 0
            print("pairList in revise:", listOfPairs)
            for pair in listOfPairs:
                print("checking pair: ", pair)
                if self.isSatisfied(pair, c):
                    print("satisfied:",self.isSatisfied(pair, c))
                    satisfiedCount += 1
                # else: 
                if satisfiedCount == 0:
                    print("notSatisfied:",self.isSatisfied(pair, c))

                # remove the variable from the domain,
                # as there is no combination with the variable 
                # where the constraint is satisfied
                    print('x.domain',x.domain)
                    print('Remove', pair[0], 'from the domain of', x)
                    x.domain.remove(pair[0])
                    print('x.domain',x.domain)
                    # self.reduceDomain(state, x, pair[0])
                    revised = True
                    return revised

        return revised

# assumption: a variable assignment/singleton domain
    def rerun(self, assumption):
        for c in self.getConstraints(assumption):
            for k in c.variables:
                print('k != assumption',k != assumption)
                if k != assumption:
                    self.queue.append((k, self.getConstraints(k)))
        return self.filterDomain()

    def isSatisfied(self, pair, constraint):
        return constraint.constraint(pair[0], pair[1])
        
    def getPairs(self, x, y):
        # pdb.set_trace()
        pairs = [] 
        for k in y:
            if k != x:
                for value in x.domain:
                    pairs.append( list(itertools.product([value], k.domain)) )
        return pairs


    def getConstraints(self, variable):
        constraints = []
        for c in self.constraints:
            # print(c)
            if variable in c.variables:
                constraints.append(c)
        return constraints

# updates self.variables after reducing 
    def reduceDomain(self, state, vi, item):
        for v in state.viList:
            if v == vi:
                print("vi.domain", vi.domain)
                print(item)
                print('v.domain', v.domain)
                v.domain.remove(item)

        