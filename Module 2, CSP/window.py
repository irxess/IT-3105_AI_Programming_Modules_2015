import pygame
import sys
from AStarGAC import Astar_GAC
from cnetGraph import CNETGraph
from cnet import CNET

class Window:

    def __init__(self, width=600,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.WHITE = (255, 255, 255)


    def initialize_problem(self, vertices, constraints, colors):
        self.set_vertices(vertices)
        for vertex in vertices:
            for c in constraints:
                vertex.addConstraint(c)
        # self.currentCNet = CNET( vertices, colors )
        # self.currentCNet.update('start')
        self.state = State( vertices, constraints )
        self.state.update('start')
        self.astarGAC = Astar_GAC( self.graph, self.currentCNet )
        self.astarGAC.search()


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
        self.screen.fill(self.WHITE)

        while True:
            pygame.event.pump()
            currentState = self.astarGAC.iterateSearch()
            self.vertices = currentState.getVerticesToDraw()
            self.draw_vertices( self.vertices )

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()


            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
            pygame.display.update()

 
            # --- Limit to 60 frames per second
            clock.tick(60)
        