import itertools

class CNET(object):
    """CNET is a representation of 
        constraints with components (variabels, domain, constarints)
        Domain is a function. domain(x) returns the domain of given variable x
        Each variable x is a vertex"""

    def __init__(self, variables, domain, constarints):
        super(CNET, self).__init__()
        self.variables = []
        self.domains = dict() # A dictionary with key as a variable x with value as x's domain
        self.constarints = dict() # Make constrains?

    def addVariable(self, x):
        self.variables.append(x)
        self.domains[x] = x.getDomain
        self.constraints[x] = {}

    def updateDomain(self, x, domain):
        self.domains[x] = domain

    def getAllArcs(self):
        allArcs = []
        # for x in self.variables:
        #     allArcs.extend(getArcsOf(v))
        # return allArcs
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

# hvordn blir dette?
    def addConstraint(self, variables, constraint):
        # if y not in self.constraints[x]:
        #   self.constraints[x][y] = self.
        valid = True
        for x in variables:
            if x not in self.variables:
                valid = False
        if valid:
            return self.makeFunc(variables, constraint)
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


