class Node(object):

    def __init__(self, x, y):
        super(Node, self).__init__()
        #self.position = (x, y)
        self.x = x
        self.y =y
        self.g = float('inf')
        self.f = float('inf')
        self.h = float('inf')
        self.parent = None #pointer to best parent node
        self.children = [] #list of succesors
        self.state = 'unvisited'


    def __repr__(self):
        return 'node(pos=%s, fValue=%s, h=%s, g=%s state=%s)' %(self.getPosition(), self.f, self.h, self.g, self.state)


    def update(self, state):
        if self.state is not 'goal' and self.state is not 'start':
            self.state = state


    def getPosition(self):
        return (self.x, self.y)


    def getF(self):
        self.f = self.g + self.h
        return self.f


    def getG(self):
        return self.g


    def setG(self, g):
        self.g = g
        self.f = self.g + self.h


    def getState(self):
        return self.state


    def getPosition(self):
        return (self.x, self.y)
    

    def setParent(self, parentNode):
        parentG = parentNode.getG()
        if self.g + 1 > parentG:
            self.g = parentG + 1
            self.parent = parentNode


    def getParent(self):
        return self.parent


    def getChildren(self):
        return self.children


    def addChild(self, node):
        self.children.append(node)


    def updateChildren(self, node):
        # TODO not sure if if-test needed
        if self.g + 1 < node.getG():
            for child in self.children:
                gNew = self.g + self.cost(child)
                if gNew < child.g:
                    child.setParent(self)
                    child.setG(gNew)
                    child.updateChildren(node)


    def cost(self, node):
        (nodeX,nodeY) = node.getPosition()
        if self.x == nodeX and self.y == nodeY:
            return 0 
        return 1


    def estimateDistanceFrom(self, goal):
        (goalX,goalY) = goal.getPosition()
        # Manhatan distance
        self.h = abs(goalX - self.x) + abs(goalY - self.y)
        self.f = self.g + self.h

