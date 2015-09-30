import itertools
from abstractnode import AbstractNode
import uuid
from constraintInstance import *
from variableInstance import *

class CNET(AbstractNode):
    """CNET is a representation of 
        constraints with components (variabels, domain, constraints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domains, expression):
        super(CNET, self).__init__()
        self.variables = self.addVariable(domains) # a list with variable class instances
        self.domains = domains
        self.constraints = self.addConstarints(self.variables, self.expression)
        self.id = uuid.uuid4()
        # self.domains = dict() # A dictionary with key as a variable x with value as x's domain
        # for v in variables:
        #     self.domains[v] = domainList
        # self.g = 0 # we don't care about the distance walked

    def addVariable(self, domains):
        for d in domains.items():
            # d is a tuple of items in domains
            self.variables.extend(VI(d[0], d[1])

    def addConstarints(self, variables, expression):
        constraint = self.makeFunc(variables, expression)
        ci = CI(constraint, variables)
        self.constraints.append(ci)
        
    def makeConstraint(self, variables, expression, envir=globals()):
        # expression is a  string of mathematical/logical representation of a constraint
        args = ""
        for x in variables:
            args += "," + x 
            return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

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

# er denne nødvendig å ha her?
    def estimateDistance(self, g):
        # find heuristic
        self.h = 0
        for v in self.variables:
            self.h += len(v.getDomain())
        super(CNET, self).estimateDistance()

    # def getConstraintList(self):
    #     pass
        # create dict with v and f
        # not sure if needed

    # def initDomains(self, variables, domain):
    #     self.variables = variables
    #     for v in variables:
    #             self.domains[v] = domain
    #     # for x in variables:
        #     self.constraints[x] = []