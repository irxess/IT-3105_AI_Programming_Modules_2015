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
from heuristic2 import calculate_heuristics2
from heuristic3 import calculate_heuristics3
import numpy as np
import requests
import time

def playRandom(times_to_play=1):
    b = bc.BoardController()
    games_played = 0
    results = []
    while games_played < times_to_play:
        old_board = copy(b.board)
        result = moveRandom(b)
        b.window.update_view(b.board)
        if result > 0: # game over
            games_played += 1
            results.append(result)
            b.start_new_game()
    return results

def moveRandom(b):
    bestDirection = 'none'
    valid_moves = []
    for direction in ['up', 'down', 'left', 'right']:
        nextBoard, nofMerges, maxMerging, highestMerg, moves = bc.slide( direction, copy(b.board) )
        # count = bc.slide( direction, copy(b.board) )
        if nextBoard != b.board:
            bestHeuristic = 1
            valid_moves.append(direction)
    if len(valid_moves)!=0:
        b.move( random.choice(valid_moves) )
        return 0
    else:
        # game_over(b)
        score = 2**max(b.board)
        print(score)
        return score

def playANN(functions, layer_sizes, learning_rate, epochs=1, training_size=21760, times_to_play=1, prep=1):
    with open('training_data.pkl', 'rb') as f:
        tr_data, tr_labels = pickle.load(f)

    # find input size:
    if prep == 1:
        preprocess_function = preprocess
    elif prep == 2:
        preprocess_function = preprocess2
    else:
        preprocess_function = preprocess3

    input_size = len(preprocess_function(tr_data[0]))

    ann = construct_ann.Construct_ANN(layer_sizes, functions, learning_rate, input_units=input_size, output_units=4, max_of_outputs=False)
    tr_sig = np.zeros([training_size, input_size])
    tr_lbl = np.empty([training_size, 4])
    for i in range(training_size):
        boardstate = tr_data[i]
        label = tr_labels[i]
        input_layer = preprocess_function(boardstate)

        correct_output = generate_output_layer(label)
        for j in range(len(input_layer)):
            tr_sig[i][j] = input_layer[j]
        for j in range(len(correct_output)):
            tr_lbl[i][j] = correct_output[j]

    # tr_sig is a numpy array with inputs as numpy arrays
    # tr_lbl is a numpy array with correct outputs as numpy arrays
    for i in range(epochs):
        for start, end in zip(range(0, len(tr_sig), 128), range(128, len(tr_sig), 128)):
            ann.train(tr_sig[start:end], tr_lbl[start:end])

    # start game
    b = bc.BoardController()
    games_played = 0
    results = []
    while games_played < times_to_play:
        old_board = copy(b.board)
        result = moveANN(ann, b, prep)
        if result > 0: # game over
            games_played += 1
            results.append(result)
            if games_played < times_to_play:
                b.start_new_game()
    return results

def moveANN(ann, b, prep):
    # change max_of_outputs to False is we want to see
    # the rating of all 4 directions
    if prep == 1:
        input_layer = preprocess(b.board)
    elif prep == 2:
        input_layer = preprocess2(b.board)
    else:
        input_layer = preprocess3(b.board)

    weights = ann.predict([input_layer])
    directions = ['up', 'down', 'left', 'right']
    weighted_moves = []
    for i in range(len(directions)):
        weighted_moves.append( (weights[i], directions[i]) )

    # sorted_moves.sort(key = lambda t: t[1])
    weighted_moves.sort(reverse=True)
    for weighted_move in weighted_moves:
        move = weighted_move[1]
        old_board = copy(b.board)
        try:
            # print('Trying to move')
            b.move(move)
            # print(old_board)
            # print(b.board)
            if old_board != b.board:
                return 0
            else:
                b.board = old_board
                print('invalid move')
        except(ValueError, IndexError):
            b.board = old_board
            pass # invalid move, try next value
    # no moves left at this point
    score = 2**max(b.board)
    print(score)
    return score

def preprocess(state):
    input_layer = np.zeros([4, 19], dtype=float)
    i = 0
    for direction in ['up', 'down', 'left', 'right']:
        board, mergeCount, maxMerging, highestMerg, moves = bc.slide(direction, copy(state))
        if board != state:
            input_layer[i] = calculate_heuristics(board, mergeCount, maxMerging, highestMerg)
        # else: keep these values at 0
        i += 1
    return input_layer.flatten()

def preprocess2(state):
    input_layer = calculate_heuristics2(state)
    return input_layer

def preprocess3(state):
    input_layer = np.zeros([4, 14], dtype=float)
    i = 0
    for direction in ['up', 'down', 'left', 'right']:
        board, mergeCount, maxMerging, highestMerg, moves = bc.slide(direction, copy(state))
        if board != state:
            input_layer[i] = calculate_heuristics(board, mergeCount, maxMerging, highestMerg, moves)
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
    print(2**max(b.board))
    while True:
        b.window.update_view(b.board)

def welch(list1, list2):
    params = {"results": str(list1) + " " + str(list2), "raw": "1"}
    resp = requests.post('http://folk.ntnu.no/valerijf/6/', data=params)
    return resp.text

def parse_input(envir=globals()):
    functions = eval('[' + sys.argv[2] + ']', envir)
    layer_sizes = eval('[' + sys.argv[3] + ']', envir)
    learning_rate = eval(sys.argv[4], envir)
    return functions, layer_sizes, learning_rate

if __name__ == "__main__":
    # python3 play2048.py ai "T.tanh, T.tanh, T.nnet.softmax" "100,40" "0.03"
    # python3 play2048.py ai "T.nnet.relu, T.nnet.sigmoid, T.nnet.softmax" "100,40" "0.01"
    # python3 play2048.py both "T.nnet.relu, T.nnet.sigmoid, T.nnet.softmax" "100, 40" "0.01"
    if (sys.argv[1] == 'ai'):
        func, layers, lr = parse_input()
        # results = playANN(func, layers, lr, epochs=10, times_to_play=50, prep=2)
        results = playANN(func, layers, lr, epochs=10, times_to_play=50)
        print('Average: ', sum(results) / float(len(results)))
        # playANN([T.tanh, T.nnet.sigmoid, T.nnet.softmax], [80, 70], 0.006)
        # playANN([T.nnet.relu, T.nnet.softmax], [100], 0.004)
    elif (sys.argv[1] == 'random'):
        playRandom(times_to_play=10)
    elif (sys.argv[1] == 'both'):
        func, layers, lr = parse_input()
        ann_list = playANN(func, layers, lr, 30, times_to_play=50)
        random_list = playRandom(times_to_play=50)
        print(random_list)
        print(ann_list)
        print(welch(random_list, ann_list))
    else:
        print("Argument one should be 'ai', 'random' or 'both'.")
