import itertools
from abstractnode import AbstractNode
import uuid

class CNET(AbstractNode):
    """CNET is a representation of 
        constraints with components (variabels, domain, constraints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domainList):
        super(CNET, self).__init__()
        self.variables = variables # a list with vertex class instances
        self.domains = dict() # A dictionary with key as a variable x with value as x's domain
        for v in variables:
            self.domains[v] = domainList
        # self.constrains = constraints # A list with functions
        self.id = uuid.uuid4()
        self.g = 0 # we don't care about the distance walked

# modified addVariable to add a list of values + list of ther domains
    # def constraint(self, variables):
    #     pass
    #     # self.constraints = 


    def getConstraintList(self):
        pass
        # create dict with v and f
        # not sure if needed

    # def initDomains(self, variables, domain):
    #     self.variables = variables
    #     for v in variables:
    #             self.domains[v] = domain
    #     # for x in variables:
        #     self.constraints[x] = []


    def updateDomain(self, x, domain):
        self.domains[x] = domain


    def getAllArcs(self):
        allArcs = []
        for i in self.constraints:
            for j in self.constraints:
                if i != j:
                    allArcs.append((i, j))
        return allArcs
    

    def getArcsOf(self, x):
        return [ (i, x) for i in self.constraints[x] ]
    

    # def getConstraints(self):
    #     return self.constraints


    def getDomains(self):

        return self.domains


    # return an ID unique for this cnet
    def getID(self):
        return self.id


    def cost(self, node):
        nodeID = node.getID()
        if self.id == nodeID:
            return 0
        return 1


    def draw(self):
        pass
        # iterate over variables in the cnet, draw them

    def estimateDistance(self, g):
        # find heuristic
        self.h = 0
        for v in self.variables:
            self.h += len(v.getDomain())
        super(CNET, self).estimateDistance()