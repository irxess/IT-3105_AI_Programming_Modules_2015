from abc import ABCMeta, abstractmethod
import boardcontroller as bc
from copy import deepcopy, copy
import random
# from collection import deque

def calculateHeuristic(board, merges):
    """ Inspired by the method on stack overflow
    factors:
    1. The location of the (current) largest tile on the board. Is it in a corner/edge?
    2. The number of free cells
    3. Are the high numbers in a "snake-pattern"
    4. How many merges occur in this move
    5. Consecutive chain. If score diff. is a fixed value """

    heuristic \
        = 50 * edgeScore(board) \
        + 30 * openCellScore(board)(board)\
        + 10 * evalBestCorner(board) \
        +  5 * merges \
        +  5 * consecutiveChain(board)    
    return heuristic

def generateMAXSuccessors(board):
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """
    print 'max', board
    successors = []
    merges = []
    directions = ['up', 'down', 'left', 'right']
    for direction in directions:
        succ = deepcopy(board)
        print board, succ
        succ, nofMerges = bc.slide(direction, succ)
        print board, succ

        # if succ == parent means no move, no changes after sliding therfore don't append as successor
        if succ != board:
            successors.append(succ)
            merges.append(nofMerges)
    print 'max returned', successors
    return successors, merges


def generateCHANCESuccessors(board):
    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """
    print 'chance', board

    successors = []
    probabilities = []

    for i in xrange( len(board) ):
        if board[i] == 0:
            succ1 = deepcopy(board)
            succ2 = deepcopy(board)

            succ1[i] = 2
            successors.append(succ1)
            probabilities.append(0.9)
            succ2[i] = 4
            successors.append(succ2)
            probabilities.append(0.1)
    outcomes = len(probabilities)
    # Hva betyr dette og hvorfor gjoer du dette?
    for i in xrange(outcomes):
        probabilities[i] /= (outcomes/2)

    print 'chance returned', probabilities
    return successors, probabilities


def generateSuccessorsBiased(board):
    # Using biased stochastics
    successors = []
    probabilities = []
    for i in xrange( len(board) ):
        succ = deepcopy(board)
        if board[i] == 0:
            succ[i] = flip()
            probabilities.append( (succ[i] == 2) and 0.9 or 0.1 )
            successors.append(succ)
    nofFree = len(probabilities)
    probabilities = [p*(1/nofFree) for p in probabilities]
    return successors, probabilities


def flip():
    # choice of 2 or 4 with p = {0.9, 0.1}
    if random.random() > 0.9 :
            return 2
    return 4    


def edgeScore(grid):
    scoreCorner = 0
    scoreEdge = 0
    corner = set(0, 3, 12, 15)
    edge = set(grid).difference( set(5, 6, 9, 10) )#edge cells = (all cells) - (center cells)
    maxTile = max(grid)
    count = grid.count(maxTile) 
    #should I check if we have more than one maxTile?
    if maxTile in grid and grid.index(maxTile) in corner:
        #should i score more?
        score += 2**4
    elif maxTile in grid and grid.index(maxTile) in edge:
        score += 2**2 
    return score


def openCellScore(board):
    count = 0
    for cell in board:
            if cell == 0:
                count += 1
    return count


def consecutiveChain(grid):
    score = 0
    pattern = 0
    for i in xrange( len(grid) ):
        diff = abs( grid[i] - grid[i+1] )
        if  diff == grid[i]/2 or diff == grid[i+1]/2:
            pattern += 1
            score += pattern**2 + 4
    return score


def monotonicityScore(grid):
    # snake pattern, starts from 1 corner 

    #left & right
    increasingRight = 0
    inreasingLeft = 0
    last = 0

    # d = deque(grid)
    # d = d.rotate(4)

    for k in xrange(2):

        for y in xrange(3):
            i = last + y
            if grid[i] < grid[i+1] :
                increasingRight += 1
                scoreRight += increasingRight**2 #+ 4
            else:
                scoreRight -= abs( grid[i] - grid[i+1] ) 
                increasingRight = 0

        last = y
        i = 0
        for y in xrange(3):
            i = last + y 
            if grid[i+1] < grid[i]:
                increasingLeft += 1
                scoreLeft += increasingLeft**2 #+ 4
            else :
                scoreLeft -= abs( grid[i+1] - grid[i] ) 
                increasingLeft = 0
    last = i      
        
    #Up and down 
    increasingUp = 0
    increasingDown = 0
    last = 0  

    for j in xrange(2):

        for x in xrange(3):
            i = last + x
            if grid[i] < grid[i+4] :
                increasingDown += 1
                scoreDown += increasingDown**2 #+ 4
            else:
                scoreDown -= abs( grid[i] - grid[i+4] )
                increasingDown = 0

        last = x
        i = 0
        for x in xrange(3):
            i = x + last
            if grid[i+1] < grid[i]:
                increasingUp += 1
                scoreUp += increasingUp**2 #+ 4
            else :
                scoreUp -= abs( grid[i+1] - grid[i] )
                increasingUp = 0

    leftRight = max( scoreLeft, scoreRight)
    upDown = max( scoreUp, scoreDown)

    return leftRight + upDown


def evalBestCorner(board):
    # i: corner0, corner1, corner2, corner3
    maxMonotScore = 0
    b = deepcopy(board)
    for i in xrange(4):
        score = monotonicityScore(b)
        maxMonotScore = max(score, maxMonotScore)
        b = rotateLeft(b)
    return maxMonotScore


def rotateLeft(board):
    rotated = []
    l = 16
    for i in range(3, -1, -1):
        rotated.append( board[i:l:4] )
        l -= 1
    return rotated

    # the for-loop above does this: 
        # rotated.append( board[3:16:4] )
        # rotated.append( board[2:15:4] ) 
        # rotated.append( board[1:14:4] ) 
        # rotated.append( board[0:13:4] ) 

# do i need to rotate i diff. directions at all? Maybe rotating left is sufficient!
def rotateRight(board):
    rotated = []
    return rotated

# // TODO
def getNofMerges(board):
    # return nof. merges.
    pass
