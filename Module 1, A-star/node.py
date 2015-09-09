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
        if self.state is not 'goal' and self.state is not 'start':
            self.state = state

    def getPosition(self):
        return self.position
n1 = Node(1,2)
n2 = Node(4,5)
n3 = Node(4,5)

n1.f = 5
n2.f = 7
n3.f = 6
n_list = [n3, n2, n1]
n_list.sort(key=lambda x: x.f, reverse=True)
print (n_list)
n=n_list.pop()
print (n.f, n.position)
