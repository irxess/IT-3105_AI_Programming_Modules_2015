class Vertex:
    def __init__(self, x, y):
    	self.x = x
    	self.y = y
    	self.neighbors = []
    	self.color = (0,0,0)

    def add_neighbor(self, vertex):
    	self.neighbors.append(vertex)

    def setColor(self, color):
    	self.color = color

    def getColor(self):
    	return self.color

    def getPosition(self, scale_x, scale_y):
    	x = int(self.x * scale_x)
    	y = int(self.y * scale_y)
    	return (x,y)
