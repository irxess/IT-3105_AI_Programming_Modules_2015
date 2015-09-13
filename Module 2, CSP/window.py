import pygame
import sys

class Window:
    
    def create_astar(self):
        pass

    def __init__(self, width=600,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.WHITE = (255, 255, 255)

    def set_coordinates( self, max_x, max_y ):
        self.scale_x = int((self.width  - 20) / max_x)
        self.scale_y = int((self.height - 20) / max_y)

    def draw_vertices(self, vertices):
        for v in vertices:
            start_pos = v.getPosition(self.scale_x, self.scale_y)
            for n in v.neighbors:
                end_pos = n.getPosition(self.scale_x, self.scale_y)
                pygame.draw.line(self.screen, (90,90,90), start_pos, end_pos, 1)
            color = v.getColor()
            pygame.draw.circle(self.screen, color, start_pos, 5)


    def set_vertices( self, v ):
        self.vertices = v

    def loop(self):
        clock = pygame.time.Clock()
        self.screen.fill(self.WHITE)

        while True:
            pygame.event.pump()

            self.draw_vertices( self.vertices )

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()


            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
            pygame.display.update()

 
            # --- Limit to 60 frames per second
            clock.tick(60)
        