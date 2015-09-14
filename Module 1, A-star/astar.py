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
            l = list(li).sort(key=lambda x: x.f, reverse=True)
            return l.pop()
    
    def cost(self, a, b):
        if a.position[0] == b.position[0] and a.position[1] == b.position[1]:
            return 0 
        return 1

    def openNode(self, node):
        self.openList.append(node)
        node.update('open')

    def closeNode(self, node):
        self.closed.append(node)
        node.update('closed')

    def isOpen(self, node):
        # if node.state is 'open':
        #     return True
        # return False
        for n in self.openList:
            if n.getPosition() == node.getPosition() and n.state == node.state:
                # node.state = 'open'
                return True
        return False


    def isClosed(self, node):
        # if node.state is 'closed':
        #     return True
        # return False

        for n in self.closed:
            if n.position == node.position and node.state == n.state:
                return True
        return False

    def acceptNodes(self):
        for node in self.bestPath:
            node.update('start')

    def computeHeuristic(self, node):
        # Manhatan distance
        node.h = abs(self.goal.x - node.x) + abs(self.goal.y - node.y)
    
    # def attachAndEval(self, child, parent):
    #     child.parent = parent
    #     child.g = parent.g + self.cost(parent, child)
    #     self.computeHeuristic(child)
    #     child.f = child.g + child.h

    def attachAndEval(self, child, parent):
        print('attachAndEval is running')
        child.parent = parent
        print('before child.g: ', child.g)
        child.g = parent.g + self.cost(parent, child)
        print('child.g after:', child.g)
        print('before heuristic', child.h)
        self.computeHeuristic(child)
        print('after heuristic', child.h)
        child.f = child.g + child.h
        print('child.f:', child.f)

    def improvePath(self, p):
        print('improvePath')
        for k in p.kids:
            gNew = p.g + cost(p, k)
            if gNew < k.g:
                k.parent = p
                k.g = gNew
                k.f = k.g + k.h
                improvePath(k)


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
        print('///////////////////////////////////////////')
        #Agenda loop
        #if self.newNode != self.goal:
        if self.newNode.state != 'goal':

            if len(self.openList) == 0:
                print (self.solution + 'FAILED. No more nodes left in agenda to expand. \n')
                return self.countNodes

            #Returns if the alg. have created nodes over the limit
            if self.countNodes > 1000:
                print (self.solution + 'FAILED. A maximum number of nodes is reached. \n', 'Number of nodes is ')
                return self.countNodes

            self.newNode = self.extractMin(self.openList)
            print('extracted node with min f', self.newNode)
            self.closeNode(self.newNode)
            print('after close:', self.newNode)

            #if self.newNode == self.goal:
            if self.newNode.state == 'goal':
                print('goal condition', self.newNode)
                self.countNodes += 1
                self.bestPath = []
                #backtrack to get the choosen path to the goal
                while self.newNode.parent:
                    self.bestPath.append(self.newNode)
                    self.newNode = self.newNode.parent
                self.bestPath.append(self.newNode)    
                print (self.solution + 'FOUND.', '\n', 'Number of nodes is ', self.countNodes, '\n', 'Path: ')
                # return the bestPath list 
                self.acceptNodes()
                return len(self.bestPath)

# should use node to check?
            neighbors = self.grid.generateNeighbors(self.newNode)
            print(neighbors)
            for s in neighbors:
                if self.isClosed(s):
                    print('closed neighbor:', s)
                    if self.newNode.g + self.cost(self.newNode, s) < s.g:
                        print('improvePath must run on', self.node)
                        self.improvePath(self.newNode)
                    self.newNode.kids.append(s) 
                    continue

                elif self.isOpen(s):
                # elif s.state == 'open':
                    newCost = self.newNode.g + self.cost(self.newNode, s)
                    if newCost < s.g:
                        self.attachAndEval(s, newNode)
                    self.newNode.kids.append(s) 

                # s not in openList and s not in closed
                # if not self.isOpen(s) and not self.isClosed(s) :
                else:
                    print('newNode not already created:', s)
                    self.countNodes += 1
                    self.attachAndEval(s, self.newNode)
                    self.openNode(s)
                    print('node after eval:', s)
                    self.newNode.kids.append(s) 



                # # Cheching in a list of nodes? check the node.position?
                # #if s in self.closed:
                # if s.state == 'visited':
                #     continue
                # #if s in self.openList:
                # if s.state == 'active':
                #     self.newCost = self.newNode.g + self.cost(self.newNode, s)
                #     if self.newCost < s.g:
                #         self.attachAndEval(s, self.newNode)

                # # if s has a uniqe position do attachAndEval & propagate path improvment
                # if s not in self.openList and s not in self.closed:
                #     self.countNodes += 1
                #     self.attachAndEval(s, self.newNode)
                #     self.openNode(s)
                # elif self.newNode.g + self.cost(self.newNode, s) < s.g:
                #     self.attachAndEval(s, self.newNode)
                #     if s in closed:
                #         self.improvePath(self.newNode)
                # #appends s to current node kids list regardless of s's uniqueness                       
                # self.newNode.kids.append(s)