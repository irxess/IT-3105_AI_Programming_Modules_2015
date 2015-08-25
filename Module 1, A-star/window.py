import pygame
import sys
import astar

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
        a = astar.AStar()
        self.grid = a.return_result()

        background = pygame.Surface((self.width, self.height*2//3))
        background.fill(self.BLACK) # fill white
        background = background.convert()

        while 1:
        	# First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(self.WHITE)
            self.screen.blit(background,(0,0))


            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

	
 
            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
        

    # pygame.Rect's contain images, which are "blitted" onto the screen