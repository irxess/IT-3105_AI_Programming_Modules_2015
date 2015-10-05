from abc import ABCMeta, abstractmethod

class AbstractNode:
    __metaclass__ = ABCMeta

    def __init__(self):
        # super(Node, self).__init__()
        self.g = float('inf')
        self.f = float('inf')
        self.h = float('inf')
        self.parent = None #pointer to best parent node
        self.children = [] #list of succesors
        self.state = 'unvisited'


    def __repr__(self):
        return 'node(id=%s, fValue=%s, h=%s, g=%s state=%s)' %(self.getID(), self.f, self.h, self.g, self.state)


    def update(self, state):
        if self.state is not 'goal' and self.state is not 'start':
            self.state = state


    @abstractmethod
    def getID(self):
        pass


    def getF(self):
        self.f = self.g + self.h
        return self.f


    def getG(self):
        return self.g


    def setG(self, gValue):
        self.g = gValue
        self.f = self.g + self.h


    def getState(self):
        return self.state

    # def updateF(self, g, h):
    #     self.f = g + h


    def setParent(self, parentNode):
        parentG = parentNode.getG()
        if self.g + self.cost(parentNode) > parentG:
            self.setG(parentG + self.cost(parentNode))
            self.parent = parentNode


    def getParent(self):
        return self.parent


    def getChildren(self):
        return self.children


    def addChild(self, node):
        self.children.append(node)


    def improvePath(self, node):
        cost = self.cost(node)
        for child in self.children:
            gNew = self.g + cost
            if gNew < child.g:
                child.setParent(self)
                # child.setG(gNew)
                child.improvePath(node)
    @abstractmethod
    def tieBreaking(self, goal=None):
        pass


    @abstractmethod
    def cost(self, node):
        pass


    @abstractmethod
    def estimateDistance(self):
        self.f = self.g + self.h

