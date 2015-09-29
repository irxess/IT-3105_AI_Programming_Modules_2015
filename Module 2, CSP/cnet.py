import itertools
from abstractnode import AbstractNode
import uuid

class CNET(object):
    """CNET is a representation of 
        constraints with components (variabels, domain, constarints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self):
        # super(CNET, self).__init__()
        self.variables = []
        self.domains = dict() # A dictionary with key as a variable x with value as x's domain
        self.constarints = dict() # Make constrains?
        self.id = uuid.uuid4()


# modified addVariable to add a list of values + list of ther domains
# 
    def addVariable(self, variables, dom=None):
        self.variables.extend(variables)
        if dom:
            for x in iter(dom):
                self.domains[x] = dom[x]
        # self.domains = {zip([x for x in variables], [d for k, d in domains )
        for x in variables:
            self.constraints[x] = {}



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
    
    def getConstraint(self, x):
        return self.constraints[x]

    def getDomains(self):
        return self.domains

# hvordan blir dette?
    def addConstraint(self, variables, expression):
        # if y not in self.constraints[x]:
        #   self.constraints[x][y] = self.
        valid = True
        for x in variables:
            if x not in self.variables:
                valid = False
        if valid:
            return self.makeFunc(variables, expression)
            # for x in variables:
            #     # Jeg vet ikke om denne er riktig :s
            #     self.constraints[x] = apply(makeConstraint, variables)
        return valid
            

    def makeFunc(self, variables, expression, envir=globals()):
        # expression is a  string of mathematical/logical representation of a constraint
        args = ""
        for x in variables: 
            args += "," + x 
            return eval( "(lambda " + args[1:] + ": " + expression + ") " , envir)

        


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