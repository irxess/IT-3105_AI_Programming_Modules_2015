import window
import sys
from variableInstance import VI

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def main():
    w = window.Window(700,700)

    input_constraint = ""
    # lamba x: return (x.1 == x.2)
    # lambda v1, v2: v1.color != v2.color
    number_of_colors = int(sys.argv[1])
    colorList = [
         (255,107,107), # red 
         (216,107,255), # purple
         (107,255,110), # green
         (107,228,255), # light blue 
         (255,169,107), # orange
         (255,208,107), # light orange
         (107,255,188), # cyan
         (107,124,255), # blue
         (255,107,186), # pink
         (223,255,107)] # yellow green

    colors = colorList[:number_of_colors]

    inputFile = sys.argv[2]
    f = open(inputFile, 'r')

    vertexList = []
    for line in f:
        vertexList.append(line.rstrip().split(' '))
        vertexList[-1] = [ float(x) for x in vertexList[-1] ]

    number_of_vertices = int(vertexList[0][0])
    number_of_edges = int(vertexList[0][1])
    vertices = [0]*number_of_vertices

    highest_x = float("-inf")
    highest_y = float("-inf")
    lowest_x = float("inf")
    lowest_y = float("inf")
    for v in range(number_of_vertices):
        line = vertexList[v+1]
        vertices[ int(line[0]) ] = VI( (line[1], line[2]), [])
        if line[1] > highest_x:
            highest_x = line[1]
        if line[2] > highest_y:
            highest_y = line[2]
        if line[1] < lowest_x:
            lowest_x = line[1]
        if line[2] < lowest_y:
            lowest_y = line[2]

    for e in range(number_of_edges):
        line = vertexList[e+1+number_of_vertices]
        vertex1 = vertices[ int(line[0]) ]
        vertex2 = vertices[ int(line[1]) ]
        vertex2.add_neighbor( vertex1 )
        vertex1.add_neighbor( vertex2 )

    w.set_coordinates( highest_x, highest_y, lowest_x, lowest_y )

    constraints = []
    for variables,expression in pairwise( sys.argv[3:] ):
        constraints.append( (variables,expression) )
    w.initialize_problem( vertices, constraints, colors )
    w.loop()

if __name__ == "__main__":
    main()
