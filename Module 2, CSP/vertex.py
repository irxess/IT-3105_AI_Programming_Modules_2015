class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.color = (0,0,0)
        self.domain = [] # list of colors
        self.initialVI = None
        # self.constraints = [] # list of functions

    def __repr__(self):
        return 'vertex(x=%s, y=%s, color=%s)' %(self.x, self.y, self.color)

    def setDomain(self, value):
        self.domain = value

    def add_neighbor(self, vertex):
        self.neighbors.append(vertex)

    def getNeighbors(self):
        return self.neighbors

    def setColor(self, color):
        self.color = color


    def getColor(self):
        return self.color


    def getPosition(self):
        return (self.x,self.y)


    def addConstraint(self, expression):
        self.constraints.append(expression)
