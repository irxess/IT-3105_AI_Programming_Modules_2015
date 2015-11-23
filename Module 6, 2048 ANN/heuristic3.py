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

def calculate_heuristics3(board, mergeCount, maxMerging, highestMerg, nof_moves):
    # only look at merges, moved tiles, amount of neighbors near 2's and same tiles near each other
    h_index = 0

    heuristics = np.empty(14, dtype=float)

    merges = mergeScore(mergeCount)
    for i in range(len(merges)):
        heuristics[h_index] = merges[i]
        h_index += 1

    heuristics[h_index] = gradient(board)
    h_index += 1

    snakeLength = snake(board)
    for i in range(len(snakeLength)):
        heuristics[h_index] = snakeLength[i]
        h_index += 1

    heuristics[h_index] = nearness(board)

    return heuristics


def mergeScore(nofMerges):
    if nofMerges > 5:
        return [1., 1., 1., 1., 1., 1.]
    elif nofMerges > 4:
        return [1., 1., 1., 1., 1., 0.]
    elif nofMerges > 3:
        return [1., 1., 1., 1., 0., 0.]
    elif nofMerges > 2:
        return [1., 1., 1., 0., 0., 0.]
    elif nofMerges > 1:
        return [1., 1., 0., 0., 0., 0.]
    elif nofMerges > 0:
        return [1., 0., 0., 0., 0., 0.]
    else:
        return [0., 0., 0., 0., 0., 0.]

def moveScore(moves):
    if nofMerges == 0:
        return [1., 1., 1., 1., 1., 1.]
    elif nofMerges == 1 :
        return [1., 1., 1., 1., 1., 0.]
    elif nofMerges == 2:
        return [1., 1., 1., 1., 0., 0.]
    elif nofMerges == 3:
        return [1., 1., 1., 0., 0., 0.]
    elif nofMerges <= 5:
        return [1., 1., 0., 0., 0., 0.]
    elif nofMerges <= 7:
        return [1., 0., 0., 0., 0., 0.]
    else:
        return [0., 0., 0., 0., 0., 0.]

def rotateLeft(board):
    rotated = []
    l = 16
    for i in xrange(3, -1, -1):
        rotated.extend( board[i:l:4] )
        l -= 1
    return rotated

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
