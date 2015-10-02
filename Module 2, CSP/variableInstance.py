class VI():
    """docstring for VI"""
    def __init__(self, variable, domain):
        self.variable = variable # pointer to a vertex?
        self.domain = domain
        
    def __cmp__(self, variable, domain):
        if self.variable.x == variable.x and self.variable.y == variable.y:
            return True
        return False

    def __repr__(self):
        x = self.variable.x
        y = self.variable.y
        print_string = ('VI ' + str(x) + ',' + str(y) + ': ')
        for color in self.domain:
            print_string += '(%s,%s,%s) ' %(color[0],color[1],color[2])
        return print_string

