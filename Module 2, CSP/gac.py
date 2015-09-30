from copy import deepcopy
import itertools

class GAC(object):

    """GAC is a generalazied arc consistency algoritm that
        outputs arc-consistent doamins for each variable v in given variable set
        cnet is given to GAC as a representation of 
        constraints with components (variabels, domain, constarints)
        domain is a dictionary and domain[v] returns a list of values(the domain of key v)
        Variable v is a vertex.
        Output: queue consists of arc-consistent domains for each variable
        """

   def __init__(self, cnet):
        super(GAC, self).__init__() 
        # self.cnet = deepcopy(cnet) # copy of constraint network
        self.variables = deepcopy(cnet.variables)
        self.domains = deepcopy(cnet.domains)
        self.queue = [] # queue of requests(focal variable, their constraints), initially all requests
        self.constraints = deepcopy(cnet.constraints)


    def initialize(self):
        for c in x.constraintInstanceList:
            for x in c.variables:
                self.queue.append((x, c))


    def filterDomain(self):         
        while len(self.queue):
            request = self.queue.pop()
            (x, c) = request
            # check if we can reduce a domain
            if self.reviseStar(x, c.variables):
                if len( x.domain ) == 0:
                    return False
                # check the other variable in the constraint
                for k in set(self.constarints).difference(c):
                    if x in k.variables:
                        for v in k.variables:
                            if v == x :
                                continue
                            self.queue.append(v, k)
                # for k in set(self.cnet.getArcsOf(i).difference(i, j)):
                #     self.queue.append(k[0], i)
        return True

# compare her med constraint isSatisfied
# uncomplete
# reduce x's domain
    def reviseStar(self, x, c):
        revised = False
        pairs = self.getPairs(x, c)

        # This condition is wrong I will edit this later
        # check all pairs found for isSatisfied
        if len( set(self.constraints).intersection(pairs) ) == 0:
                self.domains[j].pop(k)
                # reduced the list
                revised = True
        return revised
# uncomplete
    def rerun(self, assumption):
        for c in self.cnet.getConstraint(assumption):
            for y in c.keys():
                if y != assumption:
                    yConst = self.cnet.getConstraint(y)
                    self.queue.append((y, yConst))
        self.filterDomain()

        
    def isSatisfied(self, i, j, pair):
        return c(v1, v2)
        # use constraint function

        
    def getPairs(self, x, y):
        return itertools.product(x.domain, y.domain)

    
    # def getConstraints(self, variable):
    #     constraints = []
    #     for c in self.constraints:
    #         if variable in c.variables:
    #             constraints.append(c)
    #     return constraints
