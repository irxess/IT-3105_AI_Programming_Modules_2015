import pygame
import os, sys
import time
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/GAC') )
from gui_grid import GUIGrid
from nonogramSolver import NonogramSolver
from variableInstance import VI


class Window:

    def update_cell(self, row, column, state):
        self.grid.update_cell(row, column, state)        


    def __init__(self, width=500, height=750):
        pygame.init()
        self.WHITE = (255,255,255)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.prevState = None
        # self.font = pygame.font.Font('freesansbold.ttf', 16)
        # self.grid = CNET(variables, domainList)
        # self.astar = AStar(self.astar_grid, 'AStar')

    def initialize_problem(self, row_domains, column_domains, constraints):
        rows = len(row_domains)
        columns = len(column_domains)
        self.guigrid = GUIGrid(self.width, self.height*2//3, rows, columns, self.screen)

        rowVIs = []
        for i in range(rows):
            v = VI((True,i), row_domains[i])
            rowVIs.append(v)
        colVIs = []
        for i in range(columns):
            v = VI((False,i), column_domains[i])
            v.neighbors = rowVIs
            colVIs.append(v)
        for vi in rowVIs:
            vi.neighbors = colVIs

        self.astarGAC = NonogramSolver(rowVIs + colVIs, row_domains + column_domains, constraints)
        self.currentState = self.astarGAC.search()
        self.guigrid.reset()
        for var in self.currentState.viList:
            var.drawColorsToGUI(self.guigrid)


    def loop(self):
        clock = pygame.time.Clock()
        results = [None, None, None]
        active_result_index = 0
        active_result = results[active_result_index]

        while True:
            pygame.event.pump()

            self.screen.fill(self.WHITE)

            if not self.currentState.isSolution():
                self.prevState = self.currentState
                self.currentState = self.astarGAC.iterateSearch()
                self.guigrid.reset()
                for var in self.currentState.viList:
                    var.drawColorsToGUI(self.guigrid)
            self.guigrid.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
            time.sleep(1)
