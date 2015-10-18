from state import MAX, CHANCE

class Expectimax():
    def __init__(self):
        self.nextPlayer = 'ai'
        self.treeDepth = 6
        self.rootNode = MAX()


    """
    Use pseudocode from Wikipedia
    """
    def expectimax( state, depth ):
        if self.isTerminal(state) or depth == 0:
            return state.value

        elif self.isMax(state):
            return maxValue(state)

        elif self.isExp(state):
            return expectedValue(state)

    def maxValue(state):
        values = [ succ.value for succ in state.successors ]
        return max(values)

    def expectedValue(state):
        values = [ succ.value for succ in state.successors ]
        probabilities = [ succ.probability for succ in state.successors ]

    def expectation(self, values, probabilities):
        expectedValue = 0
        for v in values:
            for p in probabilities:
                expectedValue += v * pass
        return expectedValue
        
    def isTerminal(self, state):
        pass
        
    def isMax(self, state):
        pass
    # def findBestSuccessor( maxnode ):
    #     pass

    # def findBestAverageSuccessor( chancenode ):
    #     pass


