import state

class Expectimax():
    def __init__(self):
        self.nextPlayer = 'ai'
        self.treeDepth = 6
        # self.rootNode = MAX()


    def expectimax( self, node, depth ):
        if depth == 0:
            h = state.calculateHeuristic(node)
            if h == 0:
                print "forgot to implement heuristic?"
            return node.heuristic
        # should check if nodetype is MAX or CHANCE instead
        if self.nextPlayer == 'ai':
            self.findBestSuccessor( node, depth )
        if self.nextPlayer == 'board':
            self.findBestAverageSuccessor( node, depth )


    def findBestSuccessor( self, node, depth ):
       bestHeuristic = -float(inf)
       successors = state.generateMAXSuccessors(node)
       if len(successors==0):
        return state.calculateHeuristic(node)

       for succ in successors:
           succHeuristic = expectimax( succ, depth-1 )
           if succHeuristic > bestHeuristic:
               bestHeuristic = succHeuristic
       return bestHeuristic

    def findBestAverageSuccessor( self, node, depth ):
        weightedAverage = 0
        successors = state.generateCHANCEsuccessors(node)
        if len(successors==0):
         return state.calculateHeuristic(node)

        for succ in successors:
            weightedAverage += (succ.probability * expectimax( succ, depth-1 ))
            if succ.probability == 0:
                print "forgot to init probability"
        return weightedAverage

    # def maxValue(state):
    #     values = [ succ.value for succ in state.successors ]
    #     return max(values)

    # def expectedValue(state):
    #     values = [ succ.value for succ in state.successors ]
    #     probabilities = [ succ.probability for succ in state.successors ]
    #     return expectation(values, probabilities)

    # def expectation(self, values, probabilities):
    #     expectedValue = 0
    #     for v in values:
    #         for p in probabilities:
    #             expectedValue += v * pass
    #     return expectedValue
