import itertools
from constraintInstance import *
from variableInstance import *

class CNET():
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

    def getArcsOf(self, x):
        return [ (i, x) for i in self.constraints[x] ]
    

    def getConstraints(self):
        return self.constraints


    def getDomains(self):
        return self.domains


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
