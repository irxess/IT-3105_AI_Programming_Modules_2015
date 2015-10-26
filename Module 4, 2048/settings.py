def init(near, smooth, merge, grad, edge, op):
    global nearWeight
    global smoothnessWeigth
    global mergeWeight
    global gradientWeight
    global edgeWeight
    global openCellWeigth

    nearWeight = float(near)
    smoothnessWeigth = float(smooth)
    mergeWeight = float(merge)
    gradientWeight = float(grad)
    edgeWeight = float(edge)
    openCellWeigth = float(op)
