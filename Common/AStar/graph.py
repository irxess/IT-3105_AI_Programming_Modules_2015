from abc import ABCMeta, abstractmethod

class Graph:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.startNode = None
        self.goalNode = None
        self.limit = 2000


    def update_cell(self, state):
        if state=='start':
            self.startNode.g = 0


    def getStart(self):
        return self.startNode


    def getGoal(self):
        return self.goalNode


    @abstractmethod
    def isGoal(self, node):
        pass


    @abstractmethod
    def generateSucc(self, node):
        pass


