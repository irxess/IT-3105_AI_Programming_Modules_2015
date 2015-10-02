class CI(object):
    def __init__(self, constraint, variables):
        self.constraint = constraint
        self.variables = variables # list of variableInstances that the constraint function needs
        
    def __repr__(self):
    	return '(constraint:=%s, dependentVariables:=%s)' %(self.constraint, self.variables)
