import pygame
import sys
from grid import Grid
import pygbutton
import time
from astar import AStar


class Window:
    
    def create_grid(self, rows, columns):
        self.bfs_grid = Grid(self.width, self.height*2//3, rows, columns, self.screen)
        self.dfs_grid = Grid(self.width, self.height*2//3, rows, columns, self.screen)
        self.astar_grid = Grid(self.width, self.height*2//3, rows, columns, self.screen)

    def update_cell(self, row, column, state):
    	self.bfs_grid.update_cell(row, column, state)
    	self.dfs_grid.update_cell(row, column, state)
    	self.astar_grid.update_cell(row, column, state)        

    def create_astar(self):
        self.bfs = AStar(self.bfs_grid, 'BFS')
        self.dfs = AStar(self.dfs_grid, 'DFS')
        self.astar = AStar(self.astar_grid, 'AStar')

        self.active_search = self.bfs
        self.active_grid = self.bfs_grid

    def create_buttons(self):
        l = 10
        h = 25
        t = self.height*2//3 + 10
        w = (self.width-l*4)//3

        p = [(l,t,w,h),(l*2 + w,t, w,h),(l*3 + w*2, t,w, h)]

        self.buttons = [pygbutton.PygButton(p[0], "BFS"), pygbutton.PygButton(p[1], "DFS"),
           pygbutton.PygButton(p[2], "A*")]


    def __init__(self, width=500,height=750):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.create_buttons()
        # self.font = pygame.font.SysFont('Arial', 25)
        self.font = pygame.font.Font('freesansbold.ttf', 16)


        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

    def show_text(self):
        x = 10
        y = self.height*2//3 + 50
        text = self.bfs.getStats()
        self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))
        y += 25
        text = self.dfs.getStats()
        self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))
        y += 25
        text = self.astar.getStats()
        self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))


    def loop(self):
        clock = pygame.time.Clock()
        results = [None, None, None]
        active_result_index = 0
        active_result = results[active_result_index]

        while True:
            pygame.event.pump()

            active_result = results[active_result_index]
            if active_result == None:
                active_result = self.active_search.iterateAStar()
                if active_result != None:
                    results[active_result_index] = active_result
                    # print(active_result)
            self.screen.fill(self.WHITE)
            self.active_grid.draw()
            self.show_text()

            for event in pygame.event.get():
                if 'click' in self.buttons[0].handleEvent(event):
                    self.active_search = self.bfs
                    self.active_grid = self.bfs_grid
                    active_result_index = 0
                if 'click' in self.buttons[1].handleEvent(event):
                    self.active_search = self.dfs
                    self.active_grid = self.dfs_grid
                    active_result_index = 1
                if 'click' in self.buttons[2].handleEvent(event):
                    self.active_search = self.astar
                    self.active_grid = self.astar_grid
                    active_result_index = 2
                if event.type == pygame.QUIT: 
                    sys.exit()

            for button in self.buttons:
                button.draw(self.screen)

            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
            # time.sleep(3)
        