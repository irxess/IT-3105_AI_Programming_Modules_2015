import pygame
import node

class Grid:
    def __init__(self, width, height, rows, columns, display):
        self.display = display
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns

        self.cellheight = self.height // self.rows
        self.cellwidth = self.width // self.columns

        self.celltype = {}
        for i in ['start', 'goal', 'unvisited', 'closed', 'open', 'blocked']:
            icon = pygame.image.load(i + '.png').convert()
            icon = pygame.transform.scale(icon, (self.cellwidth, self.cellheight))
            self.celltype[i] = icon

        self.grid = []
        for row in range(rows):
            self.grid.append([])
            for column in range(columns):
                #self.grid[row].append('unvisited')
                self.grid[row].append( node.Node(row,column) )


    def draw(self):
        for row in range(self.rows):
            for column in range(self.columns):
                icon = self.celltype[ self.grid[row][column].state ]
                self.display.blit( icon, (self.cellwidth*column, self.cellheight*row) )


    def update_cell(self, row, column, state):
        self.grid[row][column].update(state)
        if state=='start':
            self.startNode = self.grid[row][column]
        if state=='goal':
            self.goalNode = self.grid[row][column]

    def getStart(self):
        return self.startNode

    def getGoal(self):
        return self.goalNode

    def getNode(self, x, y):
        if x >= 0 and y >= 0:
            if x < self.rows and y < self.columns:
                return self.grid[x][y]
        else:
            return None

        # find all neighbor nodes
    def generateNeighbors(self, node):
        neighbors = []
        (x,y) = node.getPosition()
        directions = [[1,0], [0,1], [-1, 0], [0,-1]]
        for i in range(len(directions)):
            k = x + directions[i][0]
            #l = y + i[i][1]
            l = y + directions[i][1]
            #if  k >= self.grid.width and  l >= self.grid.height:
            if  k < self.rows and  l < self.columns:
                #neighbors.append( self.createNode(k, l) )
                neighbornode = self.getNode(k,l)
                if neighbornode:
                    if neighbornode.state != 'blocked':
                        neighbors.append( neighbornode )
        return neighbors

