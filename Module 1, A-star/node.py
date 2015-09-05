class Node(object):

	# int x, y #position/state
	# float f, g, h 
	# g:cost of tile to next node, h: heuristic, f=g+h
	# string status 
	# state =(x,y) the position of the node 
	def __init__(self, x, y):
		super(Node, self).__init__()
		self.state = (x, y)
		self.g = None
		self.f = None
		self.h = None
		self.parent = None #pointer to best parent node
		self.kids = [] #list of succesors
