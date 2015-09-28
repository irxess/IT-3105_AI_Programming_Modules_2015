import pygame
import node
from graph import Graph

class Grid(Graph):
    def __init__(self, width, height, rows, columns, display):
        self.display = display
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns

        self.cellheight = self.height // self.rows
        self.cellwidth = self.width // self.columns

        self.celltype = {}
        for i in ['start', 'goal', 'unvisited', 'closed', 'open', 'blocked', 'path']:
            icon = pygame.image.load(i + '.png').convert()
            icon = pygame.transform.scale(icon, (self.cellwidth, self.cellheight))
            self.celltype[i] = icon

        self.grid = []
        for row in range(rows):
            self.grid.append([])
            for column in range(columns):
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
        super(Grid, self).update_cell(state)


    def getNode(self, position):
        (x,y) = position
        if x >= 0 and y >= 0:
            if x < self.rows and y < self.columns:
                return self.grid[x][y]
        else:
            return None


    def generateNeighbors(self, node):
        listToCheck = []
        (x,y,s) = node.getID()
        directions = [[-1, 0], [0,-1], [1,0], [0,1]]
        for i in range(len(directions)):
            k = x + directions[i][0]
            l = y + directions[i][1]    

            if  k < self.rows and  l < self.columns:
                neighbornode = self.getNode( (k,l) )
                listToCheck.append( neighbornode )

        neighbors = []
        for neighbornode in listToCheck:
            if neighbornode and neighbornode.getState() != 'blocked':
                if neighbornode.getG() > node.getG() + 1 :
                    neighbornode.setG( node.getG() + 1 )
                neighbors.append( neighbornode )
        return neighbors

