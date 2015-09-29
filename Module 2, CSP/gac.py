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
        self.cnet = deepcopy(cnet) # copy of constraint network
        self.variables = deepcopy(cnet.variables)
        self.domains = deepcopy(cnet.domains)
        self.queue = [] #queue of requests(focal variable, their constraints), initially all requests


    def initialize(self):
        for x in self.variables:
            for c in self.cnet.getConstraint(x):
                self.queue.append((x, c))


    def filterDomain(self):         
        while len(self.queue):
            (i, j) = self.queue.pop()
            if self.reviseStar(i, j):
                if len( self.domains[i] ) == 0:
                    return False
                for k in set(self.cnet.getArcsOf(i).difference(i, j)):
                    self.queue.append(k[0], i)
        return True


    def reviseStar(self, i, j):
        revised = False
        for k in self.domains[i]:
            pairs = [(k, m) for m in self.domains[j]]
            # use constriant function here
            if len( set(self.cnet.constraints[i][j]).intersection(pairs) ) == 0:
                self.domains[j].pop(k)
                revised = True
        return revised


    def rerun(self, assumption):
        for c in self.cnet.getConstraint(assumption):
            for y in c.keys():
                if y != assumption:
                    yConst = self.cnet.getConstraint(y)
                    self.queue.append((y, yConst))
        self.filterDomain()
        
    
