import pygame
import sys
import grid

class Window:
    
    def create_grid(self, rows, columns):
    	self.grid = grid.Grid(self.width, self.height*2//3, rows, columns, self.screen)
    	return self.grid

    def __init__(self, width=500,height=750):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.WHITE = (255, 255, 255)
        #self.create_surfaces()


    def loop(self):
        clock = pygame.time.Clock()

        while 1:
            self.screen.fill(self.WHITE)
            self.grid.draw()

            for event in pygame.event.get():
            	# press escape or q to quit the program
                #if event.key in (pygame.K_ESCAPE, pygame.K_q):
                #    pygame.quit()
                if event.type == pygame.QUIT: 
                    sys.exit()

 
            # pygame.display.update(changed_rectangles) is faster
            pygame.display.flip()
 
            # --- Limit to 60 frames per second
            clock.tick(60)
        