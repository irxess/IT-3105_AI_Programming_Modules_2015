import state
import state 
import pdb

def expectimax( node, depth, nextPlayer, nofMerges ):
    if depth == 0:
        h = state.calculateHeuristic(node, nofMerges)
        if h == 0:
            print "forgot to implement heuristic?"
        return h
    if nextPlayer == 'ai':
        return findBestSuccessor( node, depth, nofMerges )
    if nextPlayer == 'board':
        return findBestAverageSuccessor( node, depth, nofMerges )


def findBestSuccessor( node, depth, nofMerges):
   bestHeuristic = float('-inf')
   successors, merges = state.generateMAXSuccessors(node) 
   if len(successors) == 0:
    return state.calculateHeuristic(node, nofMerges)

   for i in range( len(successors) ):
       succHeuristic = expectimax( successors[i], depth-1, 'board', merges[i] )
       if succHeuristic > bestHeuristic:
           bestHeuristic = succHeuristic
   return bestHeuristic


def findBestAverageSuccessor( node, depth, nofMerges ):
    weightedAverage = 0
    successors, probabilities = state.generateSuccessorsBiased(node) #C
    # successors, probabilities = state.generateCHANCESuccessors(node) #2C
    if len(successors) == 0:
     return state.calculateHeuristic(node, nofMerges)

    for i in range(len(successors)):
        successorH = expectimax( successors[i], depth-1, 'ai', nofMerges )
        weightedAverage += (probabilities[i] * successorH)
        if probabilities[i] == 0:
            print "forgot to init probability"
            print probabilities
    return weightedAverage
