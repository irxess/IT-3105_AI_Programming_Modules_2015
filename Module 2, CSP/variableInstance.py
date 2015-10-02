class VI():
    """docstring for VI"""
    def __init__(self, variable, domain):
        self.variable = variable # pointer to a vertex?
        variable.currentVI = self
        self.domain = domain

    def __cmp__(self, vi):
        if self.variable.x == vi.variable.x and self.variable.y == vi.variable.y and comp(self.domain, vi.domain):
            return True
        return False

    def __repr__(self):
        x = self.variable.x
        y = self.variable.y
        print_string = ('VI %s,%s: %s' %(x,y,self.domain))
        # for color in self.domain:
        #     print_string += '(%s,%s,%s),' %(color[0],color[1],color[2])
        return print_string
    def comp(self, x, y):
        for i in x:
            # for j in y:
            #     pass
            if i not in y:
                return False
        return True
