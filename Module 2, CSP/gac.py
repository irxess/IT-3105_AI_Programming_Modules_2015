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
        self.queue = [] # queue of reque
        # sts(focal variable, its constraints), initially all requests
        self.constraints = (state.ciList)
        self.variables = (state.viList)
        self.state = state
        # print('GAC.state', self.state)
        # print('GAC.constraints:' , self.constraints)

        print('Put all constraints + variables in the GAC queue')
        for c in self.constraints:
            for x in c.variables:
                self.queue.append((x, c))
        state.pairs = self.queue
        # self.queueModification = False
    
    # def guess(self, queue):
    #     arbitaryTodoDom = queue[0][0].domain
    #     queue[0][0].domain = [arbitaryTodoDom[0]]


    def reduceDomain(self, x, domValue):
        for v in self.state.viList:
            if v == x:
                # pdb.set_trace()
                v.domain.pop(domValue)

                
    def filterDomain(self):  
        print('call to filterDomain--------------------')   
        # if (self.queueModification) == False:
        #     self.guess(self.queue)

        self.queueModification = True
        # pdb.set_trace()      
        while len(self.queue):
            (x, c) = self.queue.pop()
            print(x)
            arcVIs = self.getArcs(x, c)
            if self.reviseStar(x, c):
                if len( x.domain ) == 0:
                    return False
                for k in arcVIs:
                    for c in self.getConstraints(k):
                        self.queue.append( (k, c) )
        return self.state

    def reviseStar(self, x, c):
        print("call to revise **********************")
        # pdb.set_trace()      
        revised = False
        pairslist = []
        arcVIs = self.getArcs(x, c)
        pairs = []
        for dx in x.domain:
            for v in c.variables:
                pairs.extend( itertools.product(dx, v.domain) )
            satCount = 0
            for p in pairs:
                if c.constraint(p[0], p[1]) :
                    satCount += 1
            if satCount == 0:
                x.domain.remove(dx)
                self.state.reduceDomain(x, dx)

                revised = True
        return revised

    def getAllArc(self, a, b):
        itertools.product(a, b)

        # for arcVI in arcVIs:
        #     pairslist.extend( self.getPairs(x, arcVI) )
        # print(pairslist)
        # # pdb.set_trace()
        # notSatPairs = []
        # for pairs in pairslist:
        #     for pair in pairs:

        #         print('checking pair',pair)
        #         print('x.domain', x.domain)
        #         if self.isSatisfied(pair, c):
        #             satCount += 1
        #         else:
        #             notSatPairs.append(pair)
        #             # pairslist.pop(pairs)

        #         print('satisf:',self.isSatisfied(pair, c))

        #     if satCount == 0:

        #         print('/////////////////////////////////////////////////')
        #         print('toRemove:', pairs[0])
        #         self.reduceDomain(x, pair[0])
        #         revised = True
        #         return revised
        # print(notSatPairs)
        # for i in range(len(pairslist)-1):
        #     for y in notSatPairs:
        #         if y in pairslist[i]:
        #             pairslist[i].remove(y)
          
        # print('satList:', pairslist)
        # pdb.set_trace() 


            # if len(x.domain) == 1:
            #     break
        # return revised
    
    def rerun(self, assumption, guessedVI):
        for c in assumption.ciList:
            if guessedVI in c.variables:
                diff = self.getArcs(guessedVI, c)
                for kVar in diff:
                    self.queue.append( (kVar, c) )
        return self.filterDomain()
                

    # def filterDomain(self):  
    #     print('call to filterDomain--------------------')         
    #     while len(self.queue):
    #         (x, c) = self.queue.pop()
    #         # revised, updatedState = self.reviseStar(x, c, state)
    #         # self.state  = updatedState
    #         # if revised :
    #         if self.reviseStar(x, c):
    #             if len( x.domain ) == 0:
    #                 print ("inconsistency", x.domain, "reduced to empty")
    #                 print ('self.state.variables:', self.state.viList)
    #                 return None
    #             # self.rerun(state, x)
    #             # print('domlengde til x: ', len(x.domain))
    #             # print('x:', x)
    #             for k in c.variables:
    #                 print('k:  ',(k.variable.x, k.variable.y), 'x:  ', (x.variable.x, x.variable.y))
    #                 print(c.variables)
    #                 print('k',k)
    #                 if k != x:
    #                     for c in self.getConstraints(k):
    #                         self.queue.append( (k, c) )
    #     print("vars in currState after filterDomain:", self.variables)
    #     # do we though return the self.state???
    #     # print ('self.state.variables:', self.state.viList)
    #     return self.state


# reduce x's domain
    # def reviseStar(self, x, c):
    #     print("call to revise **********************")
    #     revised = False
    #     print(x)

    #     # print('c.variables',c.variables)
    #     arcs = getArcs(x)
    #     pairs = self.getPairs(x, c.variables)

    #     for listOfPairs in pairs:
    #         satisfiedCount = 0
    #         # print(listOfPairs)
    #         for pair in listOfPairs:
    #             if self.isSatisfied(pair, c):
    #                 satisfiedCount += 1
    #                 # remove the variable from the domain,
    #                 # as there is no combination with the variable 
    #                 # where the constraint is satisfied
    #         if satisfiedCount == 0:
    #             print("Satisfied:",self.isSatisfied(pair, c))    
    #             print('should remove stuff')
    #             print(listOfPairs)
    #             print('x.domain',x.domain)
    #             # print('Remove', pair[0], 'from the domain of', x)
    #             # if pair[0] in x.domain:
    #             getDomain(x).remove(pair[0])
    #             self.reduceDomain(x, pair[0], state)
    #             # print('x.domain',x.domain)
    #             revised = True
    #     return (revised)

 
    # def rerun(self, assumptionState):
    # def rerun(self, assumptionState, guessedVI):
    #     print('///////////////////')
    #     # pdb.set_trace()
    #     print('starting rerun')
    #     print(assumptionState.viList)
    #     print('guessedVI:', guessedVI)
    #     # for c in self.getConstraints(assumptionState.ciList) :
    #     for c in assumptionState.ciList:
    #         for k  in c.variables:
    #             if k != guessedVI:
    #                 # self.queue.append((k, self.getConstraints(c)))
    #                 self.queue.append( (k,self.getConstraints(k)) )
    #                 # print('k', k)
    #     print('length', len(self.queue))
    #     print(self.queue[-1])
    #     # sys.exit()
    #     return self.filterDomain()


    def isSatisfied(self, pair, constraint):
        return constraint.constraint(pair[0], pair[1])

    def getArcs(self, var, c):
        arcs = []
        depVars = []
        for v in c.variables:
            if v != var:
                depVars.append(v) 
                arcs.extend([ i for i in depVars ] )
        return arcs

    # def getPairs(self, x, k):
    #     pairs = []     
    #     pairs.append( itertools.product(x.domain, k.domain) )
    #     return pairs
        

    def getPairs(self, x, k):
        pairs = [] 
        # for k in y:
            # if not cmp(x.domain, k.domain) and not k.variable.x == x.variable.x and not k.variable.y==x.variable.y:
        if k != x:
        # print('k:',(k.variable.x, k.variable.y), 'x:', (x.variable.x, x.variable.y))
        # print('k != x  :', k != x, (k,x))
            for value in x.domain:
                pairs.append( list(itertools.product([value], k.domain)) )
        return pairs

# get all constraints applying to a certain variable
    def getConstraints(self, variable):
        constraints = []
        for c in self.constraints:
            # print(c)
            for v in c.variables:
                if v == variable:
                    constraints.append(c)
        return constraints


# updates self.variables after reducing 

    # def reduceDomain(self, vi, item, state):
    #     print('call to reduceDomain################################')
    #     for v in state.viList:
    #         if v == vi:
    #             print("vi.domain", vi.domain)
    #             print(item)
    #             print('v.domain', v.domain)
    #             v.domain.remove(item)


        