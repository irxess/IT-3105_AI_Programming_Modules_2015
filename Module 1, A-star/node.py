from abstractnode import AbstractNode
from math import sqrt

class Node(AbstractNode):

    def __init__(self, x, y):
        super(Node, self).__init__()
        self.x = x
        self.y = y



    def getID(self):
        return (self.x, self.y, self.state)


    def cost(self, node):
        (nodeX,nodeY,s) = node.getID()
        if self.x == nodeX and self.y == nodeY:
            return 0 
        return 1

    def tieBreaking(self, goal):
        return sqrt( pow((self.x - goal.x), 2) + pow((self.y - goal.y), 2) ) 

    def estimateDistance(self, goal):
        # (goalX,goalY,s) = goal.getID()
        # Manhatan distance
        # self.h = (abs(goalX - self.x) + abs(goalY - self.y))
        self.tieBreaking(goal)
        super(Node, self).estimateDistance()

