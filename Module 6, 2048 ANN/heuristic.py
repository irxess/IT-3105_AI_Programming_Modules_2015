from abc import ABCMeta, abstractmethod
import boardcontroller as bc
from copy import deepcopy, copy
import sys, random
from math import *
import numpy as np
import settings as s
import operator
if (sys.version_info > (3, 0)):
    xrange = range

directions = ('up', 'down', 'left', 'right')

def calculate_heuristics(board, mergeCount, maxMerging, highestMerg):
    # create a 14-length array, containing all results of other heuristic functions
    # should be a numpy array
    # x = np.array()
    # lbls = np.zeros((len(x),n))
    # lbls[np.arange(len(x)),x] = 1
    h_index = 0

    heuristics = np.empty(15, dtype=float)
    heuristics[h_index] = edgeScore(board)
    h_index += 1

    merges = mergeScore(mergeCount)
    for i in range(len(merges)):
        heuristics[h_index] = merges[i]
        h_index += 1

    openCells = openCellScore(board)
    for i in range(len(openCells)):
        heuristics[h_index] = openCells[i]
        h_index += 1

    heuristics[h_index] = gradient(board)
    h_index += 1

    snakeLength = snake(board)
    for i in range(len(snakeLength)):
        heuristics[h_index] = snakeLength[i]
        h_index += 1

    heuristics[h_index] = nearness(board)
    heuristics[h_index+1] = smoothness(board)

    return heuristics

def edgeScore(grid):
    scoreCorner = 0
    scoreEdge = 0
    score = 0
    corner = frozenset([0, 3, 12, 15])
    center = frozenset([5, 6, 9, 10])
    edge = frozenset(grid).difference(center) # edge cells = (all cells) - (center cells)
    maxTile = max(grid)
    if maxTile in (grid[i] for i in corner):
        return 1.0 # highest tile in corner is good
    if maxTile in (grid[i] for i in edge):
        return 0.4 # highest tile on edge is not that bad
    else:
        return 0.0

def mergeScore(nofMerges):
    if nofMerges > 5:
        return [1., 1., 1.]
    elif nofMerges > 3:
        return [1., 1., 0.]
    elif nofMerges > 0:
        return [1., 0., 0.]
    else:
        return [0., 0., 0.]

def openCellScore(board):
    count = 0
    for cell in board:
        if cell == 0:
            count += 1
    if count > 12:
        return [1, 1, 1, 1]
    elif count > 8:
        return [1, 1, 1, 0]
    elif count > 5:
        return [1, 1, 0, 0]
    elif count > 2:
        return [1, 0, 0, 0]
    else:
        return [0, 0, 0, 0]
 

 # rotated = []
 #    l = 16
 #    for i in xrange(3, -1, -1):
 #        rotated.extend( board[i:l:4] )
 #        l -= 1
 #    return rotated
def smoothness(board):
    diff = 0
    for col in range(3):
        for row in range(3):
            i = row + 4*col;
            diff -= abs(board[i]-board[i+1]) / 15 
    return diff

def gradient(board):
    b = copy(board)
    maxScore = 0

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
    r = maxScore/2.8
    if r > 1:
        r = 1.
    return r

# def smoothness(board):
#     score = 0
#     for rotation in xrange(2):
#         for i in xrange(4):
#             for j in xrange(3):
#                 val1 = board[4*i + j]
#                 val2 = board[4*i + j+1]
#                 diff = (abs(val1 - val2) )
#                 if diff > 1:
#                     score -= diff
#         board = rotateLeft(board)
#     scoreInRange = 1 + (score/100.0)
#     return scoreInRange

# should test if this calculates score correctly
def snake(board):
    b = copy(board)
    maxScore = 0

    for j in xrange(4):
        # left to right snake pattern
        score = 0
        broke = False
        for i in [0,1,2]:
            if b[i] >= b[i+1]:
                score += 1
            else:
                broke = True
                break
        if broke == False:
            if b[3] >= b[7]:
                score += 1
                for i in [7,6,5]:
                    if b[i] >= b[i-1]:
                        score += 1
                    else:
                        break
        maxScore = max(score, maxScore)

        # up-down snake pattern
        score = 0
        broke = False
        for i in [0,4,8]:
            if b[i] >= b[i+4]:
                score += 1
            else:
                broke = True
                break
        if broke == False:
            if b[12] >= b[13]:
                score += 1
                for i in [13,9,5]:
                    if b[i] >= b[i-4]:
                        score += 1
                    else:
                        break
        maxScore = max(score, maxScore)

        b = rotateLeft(b)
    if score > 6:
        return [1., 1., 1., 1.]
    elif score > 4:
        return [1., 1., 1., 0.]
    elif score > 3:
        return [1., 1., 0., 0.]
    elif score > 2:
        return [1., 0., 0., 0.]
    else:
        return [0., 0., 0., 0.]
    # x =  maxScore/504.0 # 504 is the max score possible
    # return 2**x - 1


# def evalBestCorner(board):
#     # i: corner0, corner1, corner2, corner3
#     maxMonotScore = 0
#     b = deepcopy(board)
#     for i in xrange(4):
#         score = monotonicityScore(b)
#         maxMonotScore = max(score, maxMonotScore)
#         b = rotateLeft(b)
#     return maxMonotScore

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
