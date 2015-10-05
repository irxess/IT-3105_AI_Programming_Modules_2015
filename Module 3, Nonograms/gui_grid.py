import pygame

class GUIGrid():

    def __init__(self, w, h, r, c, screen):
        self.height = h
        self.width = w
        self.rows = r
        self.columns = c
        self.display = screen

        self.cellheight = self.height // self.rows
        self.cellwidth = self.width // self.columns

        self.celltype = {}
        for i in ['white', 'gray', 'black']:
            icon = pygame.image.load(i + '.png').convert()
            icon = pygame.transform.scale(icon, (self.cellwidth, self.cellheight))
            self.celltype[i] = icon

        self.grid = []
        for x in range(self.rows):
            self.grid.append([])
            for y in range(self.columns):
                self.grid[x].append('white')


    def draw(self):
        for row in range(self.rows):
            for column in range(self.columns):
                icon = self.celltype[ self.grid[row][column] ]
                self.display.blit( icon, (self.cellwidth*column, self.cellheight*row) )


    def updateCell(self, x, y, state):
        if x >= 0 and x < self.rows:
            if y >= 0 and y < self.columns:
                self.grid[x][y] = state

    def reset(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.grid[x][y] = 'white'
