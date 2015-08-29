
import node
from collections import deque

class AStar:

    # def return_result(self):
    #     grid = []
    #     for row in range(10):
    #         grid.append([])
    #         for column in range(10):
    #             grid[row].append(0)  # Append a cell
    #     grid[1][5] = 1

    #     return grid

   

    def __init__(self, method, grid):
    	this.method = method
    	self.grid = grid
    	# ToDo getGoal and getStart
    	# self.goal = node.Node(grid.goal.x, grid.goal.y)
    	# self.start = node.Node(grid.start.x, grid.start.y)
    	self.positions = createPosMatrix(grid)
   	
   	# create a node for each tile in the grid
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
    #extract minimum successor for best-first-search
    # using minheap might be better?
	def extractMin(self, li):
		li.sort(key=node.f, reverse=True)
		return li.pop()

	#for DFS, popleft. Use a stack
	# new kids to front of OpenList
	#for BFS, pop. Use a queue
	# new succ. to the end of OpenList
	
	def cost(self, a, b):
		return 0 if a.state == a.state else 1

	def computeHeuristic(node):
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

	def generateSucc(node):
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

	# temperary aStarSearch: best_first_serach
	# ToDo: add queue and stack for bfs & dfs

	def aStarSearch(start, goal):
		openList = []
    	closeList = []
    	newNode = start # start nod is the initial state
    	computeHeuristic(newNode)
    	newNode.f = newNode.g + newNode.h
    	openlist.append(newNode)

    	#Agenda loop
    	while newNode != goal:
			if len(openlist) == 0:
				print ('FAIL')
				return False

			newNode = extractMin(openlist)
			closeList.append(newNode)
	
			if newNode == goal:
				bestPath = []
				#backtrack to get the choosen path to the goal
				while newNode.parent:
					bestPath.append(newNode)
					newNode = newNode.parent
				bestPath.append(newNode)	
				# return the reverse bestPath list 
				return bestPath.reverse()

			succ = generateSucc(newNode)
			for s in succ:
				# check if node s has already been created(in open or in closed)
				if s in closeList:
					continue
				if s in openlist:
					newCost = newNode.g + cost(newNode, s)
					if newCost < s.g:
						attachAndEval(s, newNode)

				# if s has a uniqe state do attachAndEval & propagate path improvment
				if s not in openlist and s not in closeList:
					attachAndEval(s, newNode)
					openlist.append(s)
				elif newNode.g + cost(newNode, s) < s.g:
					attachAndEval(s, newNode)
					if s in closeList:
						improvePath(newNode)
				#appends s to current node kids list regardless of s's uniqueness						
				newNode.kids.append(s)