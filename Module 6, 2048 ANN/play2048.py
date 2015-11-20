import sys
sys.path.append("../Module 4, 2048/")
import boardcontroller as bc
from copy import copy
import random
import time

def playRandom():
    board = bc.BoardController()
    while True:
        moveRandom(board)
        board.window.update_view(board.board)

def moveRandom(b):
    bestDirection = 'none'
    valid_moves = []
    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, nofMerges, maxMerging, highestMerg = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:
            bestHeuristic = 1
            valid_moves.append(direction)
    if len(valid_moves)!=0:
        b.move( random.choice(valid_moves) )
    else:
        print('----------------------------------')
        print('game over')
        print('Running time: ', time.clock())
        print(2**max(b.board))
        while True:
            b.window.update_view(b.board)

def playANN(functions, layer_sizes, learning_rate):
    pass

if __name__ == "__main__":
    if (sys.argv[1] == 'ai'):
        playANN( sys.argv[2], sys.argv[3], sys.argv[4])
    elif (sys.argv[1] == 'random'):
        playRandom()
    else:
        print("Argument one should be 'ai' or 'random'")
