import itertools
from constraintInstance import *
from variableInstance import *

class CNET():
    """CNET is a representation of 
        constraints with components (variabels, domain, constraints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domains, expression):
        self.variables = variables
        self.constraints = []
        self.domains = domains


        for e in expression:
            (args, func) = e
            constraint = self.makeConstraint(args, func)
            self.constraints.append(constraint)


    def getConstraints(self):
        return self.constraints


    def getDomains(self):
        return self.domains


    def makeConstraint(self, variables, expression, envir=globals()):
        function = "(lambda " + variables + ": " + expression + ")"
        return eval(function, envir)
