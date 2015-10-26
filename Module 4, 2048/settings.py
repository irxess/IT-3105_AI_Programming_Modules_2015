def init(snake, smooth, merge, grad, edge, op):
    global snakeWeight
    global smoothnessWeigth
    global mergeWeight
    global gradientWeight
    global edgeWeight
    global openCellWeigth

    snakeWeight = float(snake)
    smoothnessWeigth = float(smooth)
    mergeWeight = float(merge)
    gradientWeight = float(grad)
    edgeWeight = float(edge)
    openCellWeigth = float(op)
