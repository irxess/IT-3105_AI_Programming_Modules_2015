class VI():
    """docstring for VI"""
    def __init__(self, variable, domain):
        self.variable = variable # pointer to a vertex?
        self.domain = domain

    def __repr__(self):
        x = self.variable.x
        y = self.variable.y
        return ('VI ' + x + ',' + y + ': ' + self.domain )

