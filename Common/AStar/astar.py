from collections import *
from heapq import * 
# import node
# import grid
import pdb
from math import sqrt, pow

class AStar:

    def __init__(self, graph, method='Best first'):
        self.graph = graph
        self.startNode = graph.getStart()
        self.goalNode = graph.getGoal()
        self.method = method #BFS, DFS or AStar
        self.limit = 1000

        self.openList = deque()
        self.closed = set()

        self.newNode = self.startNode
        self.newNode.estimateDistance(self.goalNode)
        self.openNode(self.newNode)
        self.countNodes = 1
        self.solution = 'The solution is '
        self.pathLength = 1
        self.nofExpandedNodes = 0
        self.failed = False


    def getStats(self):
        if self.failed == True:
            if self.countNodes > self.limit:
                return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Search failed, went over limit."
            else:
                return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Search failed, no path found."
        return self.method + ":   Nodes opened: " + str(self.countNodes) + "  Path length: " + str(self.pathLength)


    def extractMin(self):
        if self.method == 'BFS':
            return self.openList.popleft()

        elif self.method == 'DFS':
            return self.openList.pop()

        else:
            li = self.openList
            sortedlist = sorted(list(li), key=lambda x: x.f, reverse=True)
            n = sortedlist[ len(sortedlist) - 1 ]
            nodesLowesF = [ n ]
            tie_n = n.tieBreaking(self.goalNode)
            for node in sortedlist:
                if node.f == n.f:
                    nodesLowesF.append(node)
            
            if len(nodesLowesF) == 1:
                self.openList.remove(n)
                return n
           
            for x in nodesLowesF:
                tie_x = x.tieBreaking(self.goalNode)
                if  tie_x  < tie_n:
                    n = x
                    tie_n = tie_x
            self.openList.remove(n)

            return n  

    

    def openNode(self, node):
        self.openList.append(node)
        node.update('open')
        # self.countNodes += 1


    def closeNode(self, node):
        self.closed.add(node)
        node.update('closed')


    def isOpen(self, node):
        for n in self.openList:
            if n.getID() == node.getID():
                return True
        return False


    def isClosed(self, node):
        for n in self.closed:
            if n.getID() == node.getID() :
                return True
        return False


    def updatePath(self):
        for node in self.bestPath:
            node.update('path')


    def attachAndEval(self, child, parent):
        child.setParent(parent)
        child.estimateDistance(self.goalNode)


    def backtrackPath(self):
        self.bestPath = []
        pathNode = self.newNode
        self.pathLength = 1

        while pathNode.getParent() != None:
            self.pathLength += 1
            self.bestPath.append(pathNode)
            pathNode = pathNode.getParent()
        self.bestPath.append(pathNode)   

        # self.updatePath()
        return self.goalNode


    def betterPathFound(self, new, old):
        if new.getG() + 1 < old.getG():
            return True
        else:
            return False


    def iterateAStar(self):
        if self.newNode.state != 'goal':

            if len(self.openList) == 0:
                self.failed = True
                return self.newNode

            if self.countNodes > self.limit:
                self.failed = True
                return self.newNode

            self.newNode = self.extractMin()
            self.closeNode(self.newNode)
            # self.nofExpandedNodes += 1

            if self.newNode.getState() == 'goal':
                # r = self.newNode
                # self.backtrackPath()
                return self.backtrackPath()

            succ = self.graph.generateSucc(self.newNode)

            for s in succ:

                if self.isClosed(s):
                    if self.betterPathFound(self.newNode, s):
                        self.newNode.improvePath(s)

                elif self.isOpen(s):
                    if self.betterPathFound(self.newNode, s):
                        self.attachAndEval(s, self.newNode)

                else:
                    self.attachAndEval(s, self.newNode)
                    self.openNode(s)
                    self.countNodes += 1

                self.newNode.addChild(s) 
        self.nofExpandedNodes += 1
        return self.newNode
