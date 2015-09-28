from graph import Graph

    def __init__(self):
        self.startNode = None
        self.goalNode = None
        activeCNet = None # TODO, give initial state


    def update_cell(self, state):
        if state=='start':
            self.startNode.g = 0


    def getStart(self):
        return self.startNode


    @abstractmethod
    def generateNeighbors(self, node):
        pass
        # find the vertex with fewest variable options left
        # create new cnet's with all guesses
        # return list of created cnet's


    def updateActiveCNet(self, cnet):
        activeCNet = cnet


    def draw(self):
        activeCNet.draw()