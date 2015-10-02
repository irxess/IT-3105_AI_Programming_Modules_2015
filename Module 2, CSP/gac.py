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
        # print('GAC.state', self.state)
        # print('GAC.constraints:' , self.constraints)
        # self.state = state

        print('Put all constraints + variables in the GAC queue')
        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))
        state.pairs = self.queue


    def filterDomain(self, state):  
        print('call to filterDomain--------------------')         
        while len(self.queue):
            (x, c) = self.queue.pop()
        #     if self.reviseStar(x, c):
        #         if len( x.domain ) == 0:
        #             print ("inconsistency", x.domain, "reduced to empty")
        #             return None
        #         print('domlengde til x: ', len(x.domain))
        #         self.rerun(state)
        # print("vars in currState after filterDomain:", self.variables)
            (revised, updatedStete) = self.reviseStar(x, c, state)
            state = updatedStete
            if revised :
                if len( x.domain ) == 0:
                    print ("inconsistency", x.domain, "reduced to empty")
                    print ('self.state.variables:', state.viList)

                    return False
                print('domlengde til x: ', len(x.domain))
                print('x:', x)
                for k in c.variables:
                    print('k:  ',(k.variable.x, k.variable.y), 'x:  ', (x.variable.x, x.variable.y))

                    print(c.variables)
                    print('k',k)
                    if k != x:
                    # if not cmp(k.domain, x.domain) and not k.variable.x == x.variable.x and not k.variable.y==x.variable.y:

                        for c in self.getConstraints(k):
                            self.queue.append( (k, c) )

        print("vars in currState after filterDomain:", state.viList)
        # do we though return the self.state???

        print ('self.state.variables:', self.state.viList)
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
    def reviseStar(self, x, c, state):
        print("call to revise **********************")
        revised = False
        print('Starting REVISE*')
        print(x)

        print('c.variables',c.variables)
        pairs = self.getPairs(x, c.variables)
        for listOfPairs in pairs:
            satisfiedCount = 0
            # print(listOfPairs)
            for pair in listOfPairs:
                if self.isSatisfied(pair, c):
                    satisfiedCount += 1
            if satisfiedCount == 0:
                print("Satisfied:",self.isSatisfied(pair, c))
                # remove the variable from the domain,
                # as there is no combination with the variable 
                # where the constraint is satisfied
                print('should remove stuff')
                print(listOfPairs)
                print('x.domain',x.domain)
                # print('Remove', pair[0], 'from the domain of', x)
                # x.domain.remove(pair[0])
                # print('x.domain',x.domain)
                # self.reduceDomain(state, x, pair[0])
                revised = True
        return (revised, state)

 
    # def rerun(self, assumptionState):
    def rerun(self, assumptionState, guessedVI):
        # pdb.set_trace()
        print('starting rerun')
        print('guessedVI:', guessedVI)
        for c in self.getConstraints(assumptionState.ciList) :
        # for c in assumptionState.ciList:
            for x in c.variables:
                if x != guessedVI:
                    self.queue.append((x, self.getConstraints(k)))
                    # self.queue.append( (x,c) )
                    print('x', k)
        print('length', len(self.queue))
        return self.filterDomain(assumptionState)


    def isSatisfied(self, pair, constraint):
        return constraint.constraint(pair[0], pair[1])
        

    def getPairs(self, x, y):
        pairs = [] 
        for k in y:
            # if not cmp(x.domain, k.domain) and not k.variable.x == x.variable.x and not k.variable.y==x.variable.y:
            if k != x:
                print('k:',(k.variable.x, k.variable.y), 'x:', (x.variable.x, x.variable.y))
                print('k != x  :', k != x, (k,x))
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
        print('call to reduceDomain################################')
        for v in self.variables:
            if v == vi:
            # if not cmp(v.domain, vi.domain) and not k.variable.x == x.variable.x and not k.variable.y==x.variable.y:

                print("vi.domain", vi.domain)
                print(item)
                print('v.domain', v.domain)
                v.domain.remove(item)

        