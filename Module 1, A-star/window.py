import pygame
import sys
import astar

class Window:
    
    def create_surfaces(self):
    	pass


    def __init__(self, width=640,height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.MARGIN = 5
        self.WIDTH = 20
        self.HEIGHT = 20

        self.create_surfaces()



    def loop(self):
        clock = pygame.time.Clock()
        a = astar.AStar()
        self.grid = a.return_result()

        while 1:
        	# First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            # Draw stuff
            for row in range(10):
                for column in range(10):
                    color = self.WHITE
                    if self.grid[row][column] == 1:
                        color = self.GREEN
                    pygame.draw.rect(self.screen,
                                 color,
                                 [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                 (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                 self.WIDTH,
                                 self.HEIGHT])
 
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
        

    # pygame.Rect's contain images, which are "blitted" onto the screen