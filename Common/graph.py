from abc import ABCMeta, abstractmethod

class Graph:
    __metaclass__ = ABCMeta

    def __init__(self, width, height, rows, columns, display):
        self.startNode = None
        self.goalNode = None


    def update_cell(self, state):
        if state=='start':
            self.startNode.g = 0


    def getStart(self):
        return self.startNode


    def getGoal(self):
        return self.goalNode


    @abstractmethod
    def getNode(self, position):
        pass


    @abstractmethod
    def generateNeighbors(self, node, neighborlist):
        neighbors = []
        for neighbornode in neighborlist:
            if neighbornode and neighbornode.getState() != 'blocked':
                if neighbornode.getG() > node.getG() + 1 :
                    neighbornode.setG( node.getG() + 1 )
                neighbors.append( neighbornode )
        return neighbors

