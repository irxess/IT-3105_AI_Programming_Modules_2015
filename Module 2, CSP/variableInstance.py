class VI():
    """docstring for VI"""
    def __init__(self, x, y, domain):
        self.x = x
        self.y = y
        self.neighbors = []
        self.color = (0,0,0)
        self.variable = (self.x, self.y) # pointer to a vertex?
        self.domain = domain


    def __eq__(self, vi):
        return (self.x == vi.x and self.y == vi.y)
        # return (self.variable.x == vi.variable.x and self.variable.y == vi.variable.y and self.comp(self.domain, vi.domain))


    def __repr__(self):
        # print_string = ('VI %s,%s: %s' %(x,y,self.domain))
        # for color in self.domain:
        #     print_string += '(%s,%s,%s),' %(color[0],color[1],color[2])
        return 'vertex(x=%s, y=%s, color=%s, domain=%s)' %(self.x, self.y, self.color,self.domain)


    def comp(self, x, y):
        for i in x:
            if i not in y:
                return False
        return True


    def setDomain(self, value):
        self.domain = value


    def add_neighbor(self, vertex):
        self.neighbors.append(vertex)


    def getNeighbors(self):
        return self.neighbors


    def getPosition(self):
        return (self.x,self.y)

    def getColor(self):
        if len(self.domain) == 1:
            return self.domain[0]
        return (0,0,0)

    
    def getPosition(self):
        return (self.x, self.y)
