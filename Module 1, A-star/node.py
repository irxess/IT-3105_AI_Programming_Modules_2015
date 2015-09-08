import pygame

class Node(object):

    # int x, y #position/state
    # float f, g, h 
    # g:cost of tile to next node, h: heuristic, f=g+h
    # string status 
    # state =(x,y) the position of the node 
    def __init__(self, x, y):
        super(Node, self).__init__()
        self.position = (x, y)
        self.x = x
        self.y =y
        self.g = float('inf')
        self.f = float('inf')
        self.h = float('inf')
        self.parent = None #pointer to best parent node
        self.kids = [] #list of succesors
        self.state = 'unvisited'

    def update(self, state):
        self.state = state

    def getPosition(self):
        return self.position
