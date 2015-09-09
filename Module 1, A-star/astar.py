from collections import deque
from heapq import * #need: heappush, heappop & heapify, heappushpop maybe
import node
import grid


class AStar:

    def __init__(self, grid, method):
   
        self.positions = grid
        self.grid = grid
        self.start = grid.getStart()
        self.goal = grid.getGoal()
        self.method = method #button event on window
        self.aStarSearch(self.start, self.goal)

    #Handling of openList
    #extracts successor with min. f value for best-first-search, lifo for DFS, fifo for BFS
    def extractMin(self, li):
        if self.method == 'BFS':
            return li.popleft()

        elif self.method == 'DFS':
            return li.pop()

        else: #best_first, returns
            return sorted(list(li), key=lambda x: x.f, reverse=True).pop()
    
    def cost(self, a, b):
        if a.position[0] == b.position[0] and a.position[1] == b.position[1]:
            return 0 
        return 1

    def openNode(self, node):
    	self.openList.append(node)
    	node.update('active')

    def closeNode(self, node):
    	self.closed.append(node)
    	node.update('visited')

    def computeHeuristic(self, node):
        # Manhatan distance
        node.h = abs(self.goal.x - node.x) + abs(self.goal.y - node.y)
        #node.h = abs(goal.state[0] - node.state[0]) + abs(goal.state[1] - node.state[1])
    
    def attachAndEval(self, child, parent):
        #self.child.parent = self.parent
        child.parent = parent
        child.g = parent.g + self.cost(parent, child)
        self.computeHeuristic(child)
        child.f = child.g + child.h

    def improvePath(self, p):
        for k in p.kids:
            gNew = p.g + cost(p, k)
            if gNew < k.g:
                k.parent = p
                k.g = gNew
                k.f = k.g + k.h
                improvePath(k)

######## Grid used ########
    def generateSucc(self, node):
        succ = []
        x = node.position[0]
        y = node.position[1]
        neig = [[1,0], [0,1], [-1, 0], [0,-1]]
        for i in range(len(neig)-1):
            for j in range(2):
                k = x + neig[i][0]
                #l = y + i[i][1]
                l = y + neig[i][1]
                #if  k >= self.grid.width and  l >= self.grid.height:
                if  k < self.grid.rows and  l < self.grid.columns:
                    #succ.append( self.createNode(k, l) )
                    succ.append( self.grid.getNode(k,l) )
        return succ


    def aStarSearch(self, start, goal):
        self.openList = deque([])
        self.closed = []

        self.startNode = self.grid.getStart()
        self.newNode = self.startNode # start node is the initial state
        self.countNodes = 1 # the initial state is the first generated search node.
        
        self.computeHeuristic(self.newNode)
        self.newNode.f = self.newNode.g + self.newNode.h
        self.openNode(self.newNode)
        self.limit = 1000
        self.solution = 'The solution is '

    def iterateAStar(self):
        #Agenda loop
        if self.newNode != self.goal:

            if len(self.openList) == 0:
                print (self.solution + 'FAILED. No more nodes left in agenda to expand. \n')
                return self.countNodes

            #Returns if the alg. have created nodes over the limit
            if self.countNodes > 1000:
                print (self.solution + 'FAILED. A maximum number of nodes is reached. \n', 'Number of nodes is ')
                return self.countNodes

            self.newNode = self.extractMin(self.openList)
            self.closeNode(self.newNode)

            if self.newNode == self.goal:
                self.countNodes += 1
                self.bestPath = []
                #backtrack to get the choosen path to the goal
                while self.newNode.parent:
                    self.bestPath.append(self.newNode)
                    self.newNode = self.newNode.parent
                self.bestPath.append(self.newNode)    
                print (self.solution + 'FOUND.', '\n', 'Number of nodes is ', self.countNodes, '\n', 'Path: ')
                # return the reverse bestPath list 
                return self.bestPath.reverse()

            succ = self.generateSucc(self.newNode)
            for s in succ:
                # Cheching in a list of nodes? check the node.position?
                if s in self.closed:
                    continue
                if s in self.openList:
                    self.newCost = self.newNode.g + self.cost(self.newNode, s)
                    if self.newCost < s.g:
                        self.attachAndEval(s, self.newNode)

                # if s has a uniqe position do attachAndEval & propagate path improvment
                if s not in self.openList and s not in self.closed:
                    self.countNodes += 1
                    self.attachAndEval(s, self.newNode)
                    self.openNode(s)
                elif self.newNode.g + self.cost(self.newNode, s) < s.g:
                    self.attachAndEval(s, self.newNode)
                    if s in closed:
                        self.improvePath(self.newNode)
                #appends s to current node kids list regardless of s's uniqueness                       
                self.newNode.kids.append(s)