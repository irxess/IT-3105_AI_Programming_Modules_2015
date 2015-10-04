import itertools
from constraintInstance import *
from variableInstance import *
# import uuid

class CNET():
    """CNET is a representation of 
        constraints with components (variabels, domain, constraints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domains, expression):
        self.variables = variables
        self.constraints = []
        self.ciList = []
        self.domains = domains
        # self.addVariables(domains) # a list with variable class instances

        for e in expression:
            (args, func) = e
            constraint = self.makeConstraint(args, func)
            self.constraints.append(constraint)
            for v in self.variables:
                for n in v.neighbors:
                    ci = CI(constraint, [v,n])
                    self.ciList.append(ci)
        # self.id = uuid.uuid4()


    # def addVariables(self, domains):
    #     for d in domains.items():
    #         vi = VI(d[0], d[1])
    #         d[0].initialVI = vi
    #         d[0].currentVI = vi
    #         self.variables.append(vi)


    def getConstraints(self):
        return self.constraints


    def getDomains(self):
        return self.domains


    # def addConstraint(self, variables, constraint):
    #     ci = CI(constraint, variables)
    #     self.ciList.append(ci)


    def makeConstraint(self, variables, expression, envir=globals()):
        # expression is a  string of mathematical/logical representation of a constraint
        function = "(lambda " + variables + ": " + expression + ")"
        return eval(function, envir)
