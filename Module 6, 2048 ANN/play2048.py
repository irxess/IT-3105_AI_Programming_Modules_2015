import boardcontroller as bc

def playRandom():
    board = new boardcontroller()
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
