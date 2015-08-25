import pygame

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
        for i in ['start', 'goal', 'unvisited', 'visited', 'active', 'blocked']:
            icon = pygame.image.load(i + '.png').convert()
            icon = pygame.transform.scale(icon, (self.cellwidth, self.cellheight))
            self.celltype[i] = icon

        self.grid = []
        for row in range(rows):
            self.grid.append([])
            for column in range(columns):
                self.grid[row].append('unvisited')

        self.grid[0][0] = 'start'
        self.grid[2][2] = 'visited'
        self.grid[5][5] = 'active'
        self.grid[5][5] = 'active'
        self.grid[5][6] = 'active'
        self.grid[5][7] = 'active'
        self.grid[1][1] = 'blocked'
        self.grid[3][3] = 'goal'

    def draw(self):
        for row in range(self.rows):
            for column in range(self.columns):
                icon = self.celltype[ self.grid[row][column] ]
                self.display.blit( icon, (self.cellwidth*column, self.cellheight*row) )


    def update_cell(self, row, column, state):
        self.grid[row][column] = state