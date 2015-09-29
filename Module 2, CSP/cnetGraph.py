from graph import Graph
class CNETGraph:

    def __init__(self):
        self.startNode = None
        self.goalNode = None #must be a state with domain length equal to 1 for all variables
        activeCNet = None # TODO, give initial state

#  Define goalNode == isSolution in Astar-GAC
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