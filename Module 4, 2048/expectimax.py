import state 

# depth should be an odd number if player is 'ai', maybe?
# The depth must be a fixed number not over 6, the AI has to stop searching when reaching depth=6
def expectimax( node, depth, nextPlayer ):
    print 'expectimax', node
    merges = state.getNofMerges(node)
    if depth == 0:
        h = state.calculateHeuristic(node, merges)
        if h == 0:
            print "forgot to implement heuristic?"
        return h
    # should check if nodetype is MAX or CHANCE instead
    if nextPlayer == 'ai':
        return findBestSuccessor( node, depth )
    if nextPlayer == 'board':
        return findBestAverageSuccessor( node, depth )


def findBestSuccessor( node, depth ):
   bestHeuristic = float('-inf')
   successors, merges = state.generateMAXSuccessors(node) 
   if len(successors) == 0:
    return state.calculateHeuristic(node, merges)

   for i in range( len(successors) ):
       succHeuristic = expectimax( successors[i], depth-1, 'board' )
       if succHeuristic > bestHeuristic:
           bestHeuristic = succHeuristic
           # bestDirection = directions[i]
   return bestHeuristic

def findBestAverageSuccessor( node, depth ):
    weightedAverage = 0
    successors, probabilities = state.generateSuccessorsBiased(node) #C
    # successors, probabilities = state.generateCHANCESuccessors(node) #2C
    if len(successors) == 0:
     return state.calculateHeuristic(node)

    for i in range(len(successors)):
        successorH, move = expectimax( successors[i], depth-1, 'ai' )
        weightedAverage += (probabilities[i] * successorH)
        if probabilities[i] == 0:
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
