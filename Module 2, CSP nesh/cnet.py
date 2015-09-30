import itertools
from abstractnode import AbstractNode
from constraintInstance import *
from variableInstance import *
import uuid

class CNET(object):
    """CNET is a representation of 
        constraints with components (variabels, domain, constarints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domains, expression):
        super(CNET, self).__init__()
        self.variables = variables
        self.domains = domains
        self.constraints = self.addConstarints(self.variables, self.expression)

        self.id = uuid.uuid4()

    def addVariable(self, domains):
        for d in domains.items():
            self.variables.extend(VIs.variables)

    def updateDomain(self, x, domain):
        self.domains[x] = domain


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
        # iterate over vertices in the cnet, draw them
