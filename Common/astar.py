from collections import deque
from heapq import * 
# import node
# import grid


class AStar:

    def __init__(self, graph, method):
        self.graph = graph
        self.startNode = graph.getStart()
        self.goalNode = graph.getGoal()
        self.method = method #BFS, DFS or AStar
        self.limit = 1000

        self.openList = deque([])
        self.closed = set()

        self.newNode = self.startNode
        self.countNodes = 1
        self.newNode.estimateDistance(self.goalNode)
        self.openNode(self.newNode)
        self.solution = 'The solution is '
        self.pathLength = 1
        self.failed = False


    def getStats(self):
        if self.failed == True:
            if self.countNodes > self.limit:
                return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Search failed, went over limit."
            else:
                return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Search failed, no path found."
        return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Path length: " + str(self.pathLength)


    def extractMin(self, li):
        if self.method == 'BFS':
            return li.popleft()

        elif self.method == 'DFS':
            return li.pop()

        else:
            n = sorted(list(li), key=lambda x: x.f, reverse=True).pop()
            li.remove(n)
            return n
 

    def openNode(self, node):
        self.openList.append(node)
        node.update('open')


    def closeNode(self, node):
        self.closed.add(node)
        node.update('closed')


    def isOpen(self, node):
        for n in self.openList:
            if n.getID()== node.getID():
                return True
        return False


    def isClosed(self, node):
        for n in self.closed:
            if n.getID()== node.getID():
                return True
        return False


    def updatePath(self):
        for node in self.bestPath:
            node.update('path')


    def attachAndEval(self, child, parent):
        child.setParent(parent)
        child.estimateDistance(self.goalNode)


    def backtrackPath(self):
        # print('goal condition', self.newNode)
        self.countNodes += 1
        self.bestPath = []

        while self.newNode.getParent() != None:
            self.pathLength += 1
            self.bestPath.append(self.newNode)
            self.newNode = self.newNode.getParent()
        self.bestPath.append(self.newNode)   

        self.updatePath()
        return self.goalNode


    def betterPathFound(self, new, old):
        if new.getG() + 1 < old.getG():
            return True
        else:
            return False


    def iterateAStar(self):
        if self.newNode.state != 'goal':

            if len(self.openList) == 0:
                # print (self.solution + 'FAILED. No more nodes left in agenda to expand. \n')
                self.failed = True
                return self.newNode

            if self.countNodes > self.limit:
                # print (self.solution + 'FAILED. A maximum number of nodes is reached. \n', 'Number of nodes is ')
                self.failed = True
                return self.newNode

            self.newNode = self.extractMin(self.openList)
            self.closeNode(self.newNode)

            if self.newNode.getState() == 'goal':
                r = self.newNode
                self.backtrackPath()
                return r

            succ = self.graph.generateSucc(self.newNode)

            for s in succ:

                if self.isClosed(s):
                    if self.betterPathFound(self.newNode, s):
                        self.newNode.updateChildren(s)
                    self.newNode.addChild(s) 
                    continue

                elif self.isOpen(s):
                    if self.betterPathFound(self.newNode, s):
                        self.attachAndEval(s, self.newNode)
                    self.newNode.addChild(s) 

                else:
                    self.countNodes += 1
                    self.attachAndEval(s, self.newNode)
                    self.openNode(s)
                    self.newNode.addChild(s) 
        return self.newNode
