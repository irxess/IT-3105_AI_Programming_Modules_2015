import pygame
import sys
import grid

class Window:
    
    def create_surfaces(self):
    	pass


    def __init__(self, width=500,height=750):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.MARGIN = 2
        self.WIDTH = 20
        self.HEIGHT = 20

        self.create_surfaces()



    def loop(self):
        clock = pygame.time.Clock()
        g = grid.Grid(self.width, self.height*2//3, 10, 10, self.screen)

        while 1:
            self.screen.fill(self.WHITE)
            g.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

	
 
            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
        