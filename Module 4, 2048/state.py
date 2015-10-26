from abc import ABCMeta, abstractmethod
import boardcontroller as bc
from copy import deepcopy, copy
import random
from math import *
import numpy as np
import settings as s
import operator

# from collection import deque

def calculateHeuristic(board, nofMerges, maxMerging, highestMerg):

    """ Inspired by the method on stack overflow factors:
    1. The location of the (current) largest tile on the board. Is it in a corner/edge?
    2. The number of free cells
    3. Are the high numbers in a "snake-pattern" 
    4. How many merges occur in this move
    5. Consecutive chain. If score diff. is a fixed value """

    heuristic = 0

    heuristic += s.edgeWeight * edgeScore(board)
    heuristic += s.openCellWeigth * openCellScore(board) 
    heuristic += s.snakeWeight * snake(board) 
    heuristic += s.mergeWeight * mergeScore(nofMerges, maxMerging, highestMerg, max(board))
    heuristic += s.gradientWeight * gradient(board) 
    heuristic += s.smoothnessWeigth * smoothness(board)
    heuristic += s.nearWeight * nearness(board)

    # spaceAround2Tiles()
    # edge around highest
    # distance between two largest tiles

    return heuristic

directions = ('up', 'down', 'left', 'right')

def generateMAXSuccessors(board):
    """
    Generate the boards that happen
    when pressing arrow up, down, left, right.
    Do not insert a new tile, only merge.
    """

    successors = []
    merges = []
    maxMergings = []
    highestMerges = []
    #directions = ['up', 'down', 'left', 'right']
    for direction in directions:
        succ = deepcopy(board)
        succ, nofMerges, maxMerging, highestMerg = bc.slide(direction, succ)

        # if succ == parent means no move, no changes after sliding therfore don't append as successor
        if succ != board:
            successors.append(succ)
            merges.append(nofMerges)
            maxMergings.append(maxMerging)
            highestMerges.append(highestMerg)

    return successors, merges, maxMergings, highestMerges


def generateCHANCESuccessors(board):
    """
    Generate new boards by inserting a new
    tile in all possible locations.
    Maybe two tiles(2C), with values 2 and 4. Try with only C later
    """

    successors = []
    probabilities = []

    for i in xrange( len(board) ):
        if board[i] == 0:
            succ1 = deepcopy(board)
            succ2 = deepcopy(board)

            succ1[i] = 1
            successors.append(succ1)
            probabilities.append(0.9)
            succ2[i] = 2
            successors.append(succ2)
            probabilities.append(0.1)
    outcomes = len(probabilities)

    for i in xrange(outcomes):
        probabilities[i] /= (outcomes/2)

    return successors, probabilities


def generateSuccessorsBiased(board):
    # Using biased stochastics
    successors = []
    probabilities = []
    for i in xrange( len(board) ):
        succ = deepcopy(board)
        if board[i] == 0:
            succ[i] = flip()
            probabilities.append( (succ[i] == 1) and 0.9 or 0.1 )
            successors.append(succ)

    nofSuccs = float( len(probabilities) )

    for i in xrange(len(probabilities)-1):
        p = probabilities[i]
        probabilities[i] = p * (1/nofSuccs)

    # probabilities = [(p*(1/nofSuccs)) for p in probabilities]
    return successors, probabilities


def flip():
    # choice of 2 or 4 with p = {0.9, 0.1}
    if random.random() < 0.9 :
            return 1
    return 2    


def edgeScore(grid):
    scoreCorner = 0
    scoreEdge = 0
    score = 0
    corner = frozenset([0, 3, 12, 15])
    center = frozenset([5, 6, 9, 10])
    edge = frozenset(grid).difference(center) # edge cells = (all cells) - (center cells)
    maxTile = max(grid)
    if maxTile in (grid[i] for i in corner):
        return 1 # highest tile in corner is good
    if maxTile in (grid[i] for i in edge):
        return 0.5 # highest tile on edge is not that bad
    else:
        return 0


def mergeScore(nofMerges, maxMerging, highestMerge, maxTile):
    if maxMerging > 0:
        return 1 # we always want to merge the highest tile
    if highestMerge + 2>= maxTile:
        return 0.9

    x = nofMerges / 8.0 # max 8 merges possible
    bestMergeScore = highestMerge / float(maxTile)

    h = x * bestMergeScore 
    if h < 0.9:
        return h
    return 0.9
    # return sin(x*5/pi)
    # return log(x)/4 + 1


def openCellScore(board):
    count = 0
    for cell in board:
        if cell == 0:
            count += 1
    return count/16.0


def gradient(board):
    b = copy(board)
    maxScore = 0
    # grad = [10, 9, 8, 7, 9, 6, 5, 4, 8, 5, 3, 2, 7, 4, 2, 1]

    grad = [8, 5, 2, 1, 5, 3, -1, -2, 2, -1, -3, -5, 1, -2, -5, -8]
  # [ 8,  5,  2,  1,
  #   5,  3, -1, -2,
  #   2, -1, -3, -5,
  #   1, -2, -5, -8 ]

    grad[:] = [x / 8.0 for x in grad]
    maxTile = max(board)
    for j in xrange(4):
        for i in xrange( len(board)-1 ):
            b[i] =  grad[i] * b[i] / maxTile
        maxScore = max(sum(b), maxScore)
        b = rotateLeft(b)

    # 2.6 is awesome, 1 is bad
    return maxScore/2.8
    # return maxScore


def smoothness(board):
    score = 0
    for rotation in xrange(2):
        for i in xrange(4):
            for j in xrange(3):
                val1 = board[4*i + j]
                val2 = board[4*i + j+1]
                diff = (abs(val1 - val2) )
                if diff > 1:
                    score -= diff
        board = rotateLeft(board)
    scoreInRange = 1 + (score/100.0)
    return scoreInRange

    
def snake(board):
    b = copy(board)
    maxScore = 0

    for j in xrange(4):

        # left to right snake pattern
        score = 0
        importance = 256
        broke = False
        for i in [0,1,2]:
            if b[i] >= b[i+1]:
                score += importance
            else:
                broke = True
                break
            importance /= 2
        if broke == False:
            for i in [7,6,5]:
                if b[i] >= b[i-1]:
                    score += importance
                else:
                    break
                importance /= 2
        maxScore = max(score, maxScore)

        # up-down snake pattern
        score = 0
        importance = 256
        broke = False
        for i in [0,4,8]:
            if b[i] >= b[i+4]:
                score += importance
            else:
                broke = True
                break
            importance /= 2
        if broke == False:
            for i in [13,9,5]:
                if b[i] >= b[i-4]:
                    score += importance
                else:
                    break
                importance /= 2
        maxScore = max(score, maxScore)

        b = rotateLeft(b)

    x =  maxScore/504.0 # 504 is the max score possible
    return 2**x - 1


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
    for i in xrange(3, -1, -1):
        rotated.extend( board[i:l:4] )
        l -= 1
    return rotated


def nearness(board):
    # positions with two larges tiles
    largest, secLargest = second_largest(board)
    lX = largest % 4
    lY = largest / 4
    sX = secLargest % 4
    sY = secLargest / 4
    distance = abs(lX - sX) + abs(lY - sY)
    return 1 - distance/6.0


def second_largest(numbers):
    count = 0
    m1 = m2 = float('-inf')
    p1 = p2 = 0
    for x in numbers:
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1
                p1, p2 = count-1, p1
            else:
                m2 = x
                p2 = count-1
    return p1, p2 if count >= 2 else None

# def smoothness(board):
#     score = 0
#     highestDiff = 0.0
#     for i in xrange( len(board) -1 ):
#         difference = abs(board[i] - board[i+1])
#         score -= ( difference )
#         highestDiff = max(highestDiff, difference)
#     return score/highestDiff

# def snake(board):
#     b = copy(board)
#     maxScore = 0
#     maxTile = max(board)

#     pattern = [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
#     # pattern = [16, 15, 14, 13, 9, 10, 11, 12, 5, 6, 7, 8, 4, 3, 2, 1]
#     pattern[:] = [x / 16.0 for x in pattern]
#     for j in xrange(4):
#         for i in xrange( len(board)-1 ):
#             b[i] =  pattern[i] * b[i] / maxTile
#         # maxScore = max(sum(x for x in b), maxScore)
#         maxScore = max(sum(b), maxScore)
#         b = rotateLeft(b)
#     return maxScore
