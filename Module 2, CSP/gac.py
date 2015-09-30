from copy import deepcopy

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
        for c in self.constraints:
            for x in c.variables:
                # (x,c): request
                self.queue.append((x, c))

    def filterDomain(self):         
        while len(self.queue):
            request = self.queue.pop()
            (x, c) = request
            if self.reviseStar(x, c.variables):
                if len( x.domain ) == 0:
                    return False
                # 
                for k in self.constarints.difference(c):
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
    def reviseStar(self, x, y):
        revised = False
        pairs = self.getPairs(i, j)
        for k in self.domains[i]:
            pairs = [(k, m) for m in self.domains[j]]
            # endre på condition
            if len( set(self.cnet.constraints[i][j]).intersection(pairs) ) == 0:
                self.domains[j].pop(k)
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
        # if apply(self.cnet.):
        #     pass
    def getPairs(self, x, y):
        return itertools.product(x.domain, y.domain)

    
    # def getConstraints(self, variable):
    #     constraints = []
    #     for c in self.constraints:
    #         if variable in c.variables:
    #             constraints.append(c)
    #     return constraints