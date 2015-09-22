from abstractnode import AbstractNode

class Node(AbstractNode):

    def __init__(self, x, y):
        super(Node, self).__init__()
        self.x = x
        self.y =y


    def getPosition(self):
        return (self.x, self.y)


    def cost(self, node):
        (nodeX,nodeY) = node.getPosition()
        if self.x == nodeX and self.y == nodeY:
            return 0 
        return 1


    def estimateDistanceFrom(self, goal):
        (goalX,goalY) = goal.getPosition()
        # Manhatan distance
        self.h = abs(goalX - self.x) + abs(goalY - self.y)
        super(Node, self).estimateDistanceFrom(goal)

