import numpy as np
from copy import copy

def calculate_heuristics2(board):
    h_index = 0
    heuristics = np.empty(24, dtype=float)

    score = snakeUpDown(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    score = snakeLeftRight(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    score = mergeLeftRight(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    score = mergeUpDown(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    score = edgeScore(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    score = downFilled(board)
    for i in range(len(score)):
        heuristics[h_index] = score[i]
        h_index += 1

    return heuristics

def snakeUpDown(board):
    b = copy(board)
    maxScore = 0

    for j in range(2):
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

def snakeLeftRight(board):
    b = copy(board)
    maxScore = 0

    for j in range(2):
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

def mergeLeftRight(board):
    score = 0
    for i in [0,1,2,4,5,6,8,9,10,12,13,14]:
        if board[i] == board[i+1]:
            score += 1
    if score >= 4:
        return [1., 1., 1., 1.]
    elif score == 3:
        return [1., 1., 1., 0.]
    elif score == 2:
        return [1., 1., 0., 0.]
    elif score == 1:
        return [1., 0., 0., 0.]
    else:
        return [0., 0., 0., 0.]

def mergeUpDown(board):
    score = 0
    for i in [0,1,2,3,4,5,6,7,8,9,10]:
        if board[i] == board[i+4]:
            score += 1
    if score >= 4:
        return [1., 1., 1., 1.]
    elif score == 3:
        return [1., 1., 1., 0.]
    elif score == 2:
        return [1., 1., 0., 0.]
    elif score == 1:
        return [1., 0., 0., 0.]
    else:
        return [0., 0., 0., 0.]

def edgeScore(grid):
    score = [0.,0.,0.,0.]
    maxTile = max(grid)
    if maxTile == grid[0]:
        score[0] = 1.
    if maxTile == grid[3]:
        score[1] = 1.
    if maxTile == grid[12]:
        score[2] = 1.
    if maxTile == grid[15]:
        score[3] = 1.
    return score

def downFilled(board):
    score = [0.,0.,0.,0.]
    if board[12]!=0:
        score[0] = 1
    if board[13]!=0:
        score[1] = 1
    if board[14]!=0:
        score[2] = 1
    if board[15]!=0:
        score[3] = 1
    return score

def rotateLeft(board):
    rotated = []
    l = 16
    for i in range(3, -1, -1):
        rotated.extend( board[i:l:4] )
        l -= 1
    return rotated
