from state import MAX, CHANCE

class Expectimax():
    def __init__(self):
        self.nextPlayer = 'ai'
        self.treeDepth = 8
        self.rootNode = MAX()


    """
    Use pseudocode from Wikipedia
    """
    def expectimax( node, depth ):
        if len(node.childNodes) == 0 or depth == 0:
            if node.heuristic == 0:
                node.calculateHeuristic()
                print "forgot to calculate heuristic at init?"
            return node.heuristic
        # should check if nodetype is MAX or CHANCE instead
        if self.nextPlayer == 'ai':
            self.findBestSuccessor( node, depth )
        if self.nextPlayer == 'board':
            self.findBestAverageSuccessor( node, depth )


    def findBestSuccessor( node, depth ):
       bestHeuristic = -float(inf)
       for child in node.childNodes:
           childH = expectimax( child, depth-1 )
           if childH > bestHeuristic:
               bestHeuristic = childH
       return bestHeuristic

    def findBestAverageSuccessor( node, depth ):
        weightedAverage = 0
        for child in node.childNodes:
            weightedAverage += (child.probability * expectimax( child, depth-1 ))
            if child.probability == 0:
                print "forgot to init probability"
        return weightedAverage


