 
import node
from collections import deque
from heapq import * #need: heappush, heappop & heapify, heappushpop maybe

class AStar:

    # def return_result(self):
    #     grid = []
    #     for row in range(10):
    #         grid.append([])
    #         for column in range(10):
    #             grid[row].append(0)  # Append a cell
    #     grid[1][5] = 1

    #     return grid

    def __init__(self, grid, method='BFS'):
   
        ######### ToDo ##########
        # getGoal(), getStart() & getMethod()

        self.positions = createPosMatrix(grid)
        self.start = grid.start
        self.goal = grid.goal    
        self.method = method #button event on window

        aStarSearch(self.start, self.goal)

    
    # create a node for each tile in the grid. Maybe doing that in the grid.py?
    def createPosMatrix(self, grid):
        posMatrix = []
        for x in xrange(grid.width-1):
            posMatrix.append([])
            for y in xrange(grid.height-1):
                posMatrix[x].append(y)
        return posMatrix
        
    def createNode(self, x, y):
        return node.Node(x, y)


    #Handling of openList
    #extracts successor with min. f value for best-first-search, lifo for DFS, fifo for BFS
    def extractMin(self, li):

        if self.method == 'BFS':
            return li.popleft()

        elif self.method == 'DFS':
            return li.pop()

        #else: best_first, returns
        return sorted(list(li), key=lambda x: x.f, reverse=True).pop()
    
    def cost(self, a, b):
        if a.state[0] == b.state[0] and a.state[1] == b.state[1]:
            return 0 
        return 1

    def computeHeuristic(self, node):
        # Manhatan distance
        node.h = abs(goal.x - node.x) + abs(goal.y - node.y)
    
    def attachAndEval(self, child, parent, cost):
        self.child.parent = self.parent
        self.child.g = parent.g + cost(parent, child)
        computeHeuristic(child)
        child.f = child.g + child.h

    def improvePath(self, p):
        for k in p.kids:
            gNew = p.g + cost(p, k)
            if gNew < k.g:
                k.parent = p
                k.g = gNew
                k.f = k.g + k.h
                improvePath(k)

    def generateSucc(self, node):
        succ = []
        x = node.state[0]
        y = node.state[1]
        neig = [[1,0], [0,1], [-1, 0], [0,-1]]
        for i in range(len(neig)-1):
            for j in range(2):
                k = x + neig[i][0]
                l = y + i[i][1]
                if  k >= self.grid.width and  l >= self.grid.height:
                    succ.append(createNode(k, l))
        return succ


    def aStarSearch(self, start, goal):
        openList = collections.deque([])
        closed = []
        newNode = start # start node is the initial state
        countNodes = 1 # the initial state is the first generated search node.
        computeHeuristic(newNode)
        newNode.f = newNode.g + newNode.h
        openList.append(newNode)
        limit = 1000
        solution = 'The solution is '

        #Agenda loop
        while newNode != goal:

            if len(openList) == 0:
                print (solution = solution + 'FAILED. No more nodes left in agenda to expand. \n')
                return countNodes

            #Returns if the alg. have created nodes over the limit
            if countNodes > 1000:
                print (solution + 'FAILED. A maximum number of nodes is reached. \n', 'Number of nodes is ')
                return countNodes

            newNode = extractMin(openList)
            closed.append(newNode)

            if newNode == goal:
                countNodes += 1
                bestPath = []
                #backtrack to get the choosen path to the goal
                while newNode.parent:
                    bestPath.append(newNode)
                    newNode = newNode.parent
                bestPath.append(newNode)    
                print (solution + 'FOUND.', '\n', 'Number of nodes is ', countNodes, '\n', 'Path: ')
                # return the reverse bestPath list 
                return bestPath.reverse()

            succ = generateSucc(newNode)
            for s in succ:
                # Cheching in a list of nodes? check the node.state?
                if s in closed:
                    continue
                if s in openList:
                    newCost = newNode.g + cost(newNode, s)
                    if newCost < s.g:
                        attachAndEval(s, newNode)

                # if s has a uniqe state do attachAndEval & propagate path improvment
                if s not in openList and s not in closed:
                    countNodes += 1
                    attachAndEval(s, newNode)
                    openList.append(s)
                elif newNode.g + cost(newNode, s) < s.g:
                    attachAndEval(s, newNode)
                    if s in closed:
                        improvePath(newNode)
                #appends s to current node kids list regardless of s's uniqueness                       
                newNode.kids.append(s)