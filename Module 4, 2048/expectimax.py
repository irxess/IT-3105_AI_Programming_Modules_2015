import state, pdb



def expectimax( node, depth, nextPlayer, nofMerges, maxMerging, highestMerg ):
    if depth == 0:
        h = state.calculateHeuristic(node, nofMerges, maxMerging, highestMerg)
        return h

    if nextPlayer == 'ai':
        return findBestSuccessor( node, depth, nofMerges, maxMerging, highestMerg)
    if nextPlayer == 'board':
        return findBestAverageSuccessor( node, depth, nofMerges, maxMerging, highestMerg)


def findBestSuccessor( node, depth, nofMerges, maxMerging, highestMerg):
    bestHeuristic = float('-inf')
    successors, merges, maxMergings, highestMerges = state.generateMAXSuccessors(node) 
    if len(successors) == 0:
        return state.calculateHeuristic(node, nofMerges, maxMerging, highestMerg)

    for i in xrange( len(successors) ):
       succHeuristic = expectimax( successors[i], depth-1, 'board', merges[i], maxMergings[i], highestMerges[i])
       if succHeuristic > bestHeuristic:
           bestHeuristic = succHeuristic
    return bestHeuristic


def findBestAverageSuccessor( node, depth, nofMerges, maxMerging, highestMerg):
    weightedAverage = 0
    # successors, probabilities = state.generateSuccessorsBiased(node) #C
    successors, probabilities = state.generateCHANCESuccessors(node) #2C
    if len(successors) == 0:
        return state.calculateHeuristic(node, nofMerges, maxMerging, highestMerg)

    for i in xrange(len(successors)):
        if probabilities[i] < 0.0001:
            continue
        successorH = expectimax( successors[i], depth-1, 'ai', nofMerges , maxMerging, highestMerg)
        weightedAverage += (probabilities[i] * successorH)
    return weightedAverage
