import sys
sys.path.append("../Module 4, 2048/")
sys.path.append("../Module 5, deeplearning/")
import boardcontroller as bc
import construct_ann as ann
from copy import copy
import random
import time
import pickle

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
        game_over(b)

def playANN(functions, layer_sizes, learning_rate):
    with open('training_data.pkl', 'rb') as f:
        tr_data, tr_labels = pickle.load(f)
    network = ann.Construct_ANN(layer_sizes, functions, learning_rate, input_units=64, output_units=4)
    for i in range(len(tr_data)):
        boardstate = tr_data[i]
        label = tr_labels[i]
        input_layer = preprocess(boardstate)
        correct_output = generate_output_layer(label)
        # tr_sig should be numpy array with inputs as numpy arrays
        # <class 'numpy.ndarray'> <class 'numpy.ndarray'>
        # tr_lbl should be numpy array with correct outputs as numpy arrays
        ann.train(tr_sig[start:end], tr_lbl[start:end])

    # start game
    b = bc.BoardController()
    while True:
        new_board = moveANN(ann, copy(b.board))
        if new_board == board: # should implement a better check
            game_over(b)
        b.board = new_board

def moveANN(ann, board):
    input_layer = preprocess(board)
    move = ann.predict(input_layer)
    print(move)
    print('implement moving')
    sys.exit(0)

def preprocess(state):
    input_layer = [] # should be numpy array
    for direction in ['up', 'down', 'left', 'right']:
        board = bc.slide(direction, copy(state))
        if board != state:
            input_layer += calculate_heuristics(board)
        else:
            input_layer += [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return input_layer

def game_over(b):
    print('----------------------------------')
    print('game over')
    print('Running time: ', time.clock())
    print(2**max(b.board))
    while True:
        b.window.update_view(b.board)

if __name__ == "__main__":
    if (sys.argv[1] == 'ai'):
        playANN( sys.argv[2], sys.argv[3], sys.argv[4])
    elif (sys.argv[1] == 'random'):
        playRandom()
    else:
        print("Argument one should be 'ai' or 'random'")
