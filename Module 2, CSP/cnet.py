import itertools
from constraintInstance import *
from variableInstance import *

class CNET():
    """CNET is a representation of 
        constraints with components (variabels, domain, constraints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, domains, expression):
        super(CNET, self).__init__()
        self.variables = []
        self.addVariables(domains) # a list with variable class instances
        self.domains = domains
        self.constraints = []
        self.addConstarints(self.variables, self.expression)
        self.id = uuid.uuid4()

    def addVariables(self, domains):
        for d in domains.items():
            # d is a tuple of items in domains
            self.variables.append(VI(d[0], d[1]))

    def getConstraints(self):
        return self.constraints

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
