import pygame
import sys
from cnet import CNET
import pygbutton
import time
from astar import AStar
from gui_grid import GUIGrid

class Window:

    def update_cell(self, row, column, state):
        self.grid.update_cell(row, column, state)        


    def __init__(self, variables, domainList, rows, columns, width=500, height=750):
        pygame.init()
        self.WHITE = (255,255,255)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.guigrid = GUIGrid(self.width, self.height*2//3, rows, columns, self.screen)
        # self.font = pygame.font.Font('freesansbold.ttf', 16)
        # self.grid = CNET(variables, domainList)
        # self.astar = AStar(self.astar_grid, 'AStar')

    # def show_text(self):
    #     x = 10
    #     y = self.height*2//3 + 50
    #     text = self.bfs.getStats()
    #     self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))
    #     y += 25
    #     text = self.dfs.getStats()
    #     self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))
    #     y += 25
    #     text = self.astar.getStats()
    #     self.screen.blit(self.font.render(text, True, self.BLACK), (x, y))


    def loop(self):
        clock = pygame.time.Clock()
        results = [None, None, None]
        active_result_index = 0
        active_result = results[active_result_index]

        while True:
            pygame.event.pump()

            self.screen.fill(self.WHITE)
            self.guigrid.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
            # time.sleep(3)
        