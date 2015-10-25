import state
import state 
import pdb

def expectimax( node, depth, nextPlayer, nofMerges ):
    # pdb.set_trace()
    print 'expectimax', node
    if depth == 0:
        print 'leafnode, calculateHeuristic'
        h = state.calculateHeuristic(node, nofMerges)
        if h == 0:
            print "forgot to implement heuristic?"
        return h
    # should check if nodetype is MAX or CHANCE instead
    if nextPlayer == 'ai':
        return findBestSuccessor( node, depth, nofMerges )
    if nextPlayer == 'board':
        return findBestAverageSuccessor( node, depth, nofMerges )


def findBestSuccessor( node, depth, nofMerges):
   print 'finding best successor'
   bestHeuristic = float('-inf')
   successors, merges = state.generateMAXSuccessors(node) 
   if len(successors) == 0:
    return state.calculateHeuristic(node, nofMerges)

   for i in range( len(successors) ):
       succHeuristic = expectimax( successors[i], depth-1, 'board', merges[i] )
       if succHeuristic > bestHeuristic:
           bestHeuristic = succHeuristic
   return bestHeuristic


# def findBestAverageSuccessor( node, depth ):
def findBestAverageSuccessor( node, depth, nofMerges ):
    print 'finding best average'
    weightedAverage = 0
    # successors, probabilities = state.generateSuccessorsBiased(node) #C
    successors, probabilities = state.generateCHANCESuccessors(node) #2C
    if len(successors) == 0:
     return state.calculateHeuristic(node, nofMerges)

    for i in range(len(successors)):
        # successorH = expectimax( successors[i], depth-1, 'ai' )
        successorH = expectimax( successors[i], depth-1, 'ai', nofMerges )
        weightedAverage += (probabilities[i] * successorH)
        if probabilities[i] == 0:
            print "forgot to init probability"
            print probabilities
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
