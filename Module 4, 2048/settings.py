def init(near, smooth, merge, grad, edge, op, snake):
    global nearWeight
    global smoothnessWeigth
    global mergeWeight
    global gradientWeight
    global edgeWeight
    global openCellWeigth
    global snakeWeight

    nearWeight = float(near)
    smoothnessWeigth = float(smooth)
    mergeWeight = float(merge)
    gradientWeight = float(grad)
    edgeWeight = float(edge)
    openCellWeigth = float(op)
    snakeWeight = float(snake)
