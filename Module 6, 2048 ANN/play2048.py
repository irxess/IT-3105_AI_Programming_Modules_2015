import sys
sys.path.append("../Module 4, 2048/")
sys.path.append("../Module 5, deeplearning/")
import boardcontroller as bc
import construct_ann
from copy import copy
import random, time, pickle
import theano
from theano import tensor as T
from heuristic import calculate_heuristics
import numpy as np

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

def playANN(functions, layer_sizes, learning_rate, training_size=21760):
    with open('training_data.pkl', 'rb') as f:
        tr_data, tr_labels = pickle.load(f)
    ann = construct_ann.Construct_ANN(layer_sizes, functions, learning_rate, input_units=56, output_units=4, max_of_outputs=True)
    tr_sig = np.zeros([training_size, 56])
    tr_lbl = np.empty([training_size, 4])
    for i in range(training_size):
        boardstate = tr_data[i]
        label = tr_labels[i]
        input_layer = preprocess(boardstate)
        correct_output = generate_output_layer(label)
        for j in range(len(input_layer)):
            tr_sig[i][j] = input_layer[j]
        for j in range(len(correct_output)):
            tr_lbl[i][j] = correct_output[j]

    # tr_sig is a numpy array with inputs as numpy arrays
    # tr_lbl is a numpy array with correct outputs as numpy arrays
    for start, end in zip(range(0, len(tr_sig), 128), range(128, len(tr_sig), 128)):
        ann.train(tr_sig[start:end], tr_lbl[start:end])

    # start game
    b = bc.BoardController()
    while True:
        old_board = copy(b.board)
        moveANN(ann, b)
        # if old_board == b.board: # should implement a better check
        #     game_over(b)

def moveANN(ann, b):
    # change max_of_outputs to False is we want to see
    # the rating of all 4 directions
    input_layer = preprocess(b.board)
    move = ann.predict([input_layer])
    directions = ['up', 'down', 'left', 'right']
    try:
        b.move(directions[move])
    except(ValueError, IndexError):
        game_over(b)


def preprocess(state):
    input_layer = np.zeros([4, 14], dtype=float)
    i = 0
    for direction in ['up', 'down', 'left', 'right']:
        board, mergeCount, maxMerging, highestMerg = bc.slide(direction, copy(state))
        if board != state:
            input_layer[i] = calculate_heuristics(board, mergeCount, maxMerging, highestMerg)
        # else: keep these values at 0
        i += 1
    return input_layer.flatten()

def generate_output_layer(label):
    if label == 'up':
        return np.array([1.,0.,0.,0.])
    if label == 'down':
        return np.array([0.,1.,0.,0.])
    if label == 'left':
        return np.array([0.,0.,1.,0.])
    if label == 'right':
        return np.array([0.,0.,0.,1.])
    print(label)
    sys.exit(0)

def game_over(b):
    print('----------------------------------')
    print('game over')
    print('Running time: ', time.clock())
    print(2**max(b.board))
    while True:
        b.window.update_view(b.board)

if __name__ == "__main__":
    if (sys.argv[1] == 'ai'):
        # playANN( sys.argv[2], sys.argv[3], sys.argv[4])
        playANN([T.tanh, T.nnet.softmax], [40], 0.02)
    elif (sys.argv[1] == 'random'):
        playRandom()
    else:
        print("Argument one should be 'ai' or 'random'")
