import pygame
import os, sys
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/GAC') )
from vertexColoring import VertexColoring

class Window:

    def __init__(self, width=600,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.WHITE = (255, 255, 255)
        self.screen.fill(self.WHITE)
        self.prevState = None


    def initialize_problem(self, vertices, constraints, colors):
        self.set_vertices(vertices)
        self.draw_state(vertices)
        domains = colors
        for vertex in vertices:
            vertex.domain = colors

        self.astarGAC = VertexColoring( vertices, domains, constraints )
        self.currentState = self.astarGAC.search()
        self.vertices = self.currentState.getVerticesToDraw()
        self.draw_vertices( self.vertices )


    def set_coordinates( self, max_x, max_y, min_x, min_y ):
        self.x_diff = min_x
        self.y_diff = min_y
        self.scale_x = (self.width  - 20) / (max_x - min_x)
        self.scale_y = (self.height - 20) / (max_y - min_y)


    def draw_state(self, vertices):
        for v in vertices:
            start_pos = self.getAndFitPosition(v)
            for n in v.neighbors:
                end_pos = self.getAndFitPosition(n)
                pygame.draw.line(self.screen, (90,90,90), start_pos, end_pos, 1)
            color = v.getColor()
            pygame.draw.circle(self.screen, color, start_pos, 5)


    def draw_vertices(self, vertices):
        for v in vertices:
            start_pos = self.getAndFitPosition(v)
            color = v.getColor()
            pygame.draw.circle(self.screen, color, start_pos, 5)


    def getAndFitPosition(self, vertex):
        (x,y) = vertex.getPosition()
        x = int((x - self.x_diff) * self.scale_x) + 10
        y = int((y - self.y_diff) * self.scale_y) + 10
        return (x,y)


    def set_vertices( self, v ):
        self.vertices = v


    def loop(self):
        clock = pygame.time.Clock()
        printedStatistics = False

        while True:
            pygame.event.pump()

            if not self.currentState.isSolution():
                self.prevState = self.currentState
                self.currentState = self.astarGAC.iterateSearch()
                self.currentState.updateColors()
                self.vertices = self.currentState.getVerticesToDraw()
                self.draw_vertices( self.vertices )
            else:
                if not printedStatistics:
                    self.astarGAC.printStatistics( self.currentState )
                    printedStatistics = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()


            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
            pygame.display.update()

 
            # --- Limit to 60 frames per second
            clock.tick(60)
        
