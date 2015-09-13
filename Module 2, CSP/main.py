import window
import sys
from vertex import Vertex

def main():
    w = window.Window(700,700)

    stdin = []
    for line in sys.stdin:
        stdin.append(line.rstrip().split(' '))
        # print(stdin[-1])
        stdin[-1] = [ float(x) for x in stdin[-1] ]

    number_of_vertices = int(stdin[0][0])
    number_of_edges = int(stdin[0][1])
    vertices = [0]*number_of_vertices

    highest_x = float("-inf")
    highest_y = float("-inf")
    lowest_x = float("inf")
    lowest_y = float("inf")
    for v in range(number_of_vertices):
        line = stdin[v+1]
        vertices[ int(line[0]) ] = Vertex( line[1], line[2])
        if line[1] > highest_x:
            highest_x = line[1]
        if line[2] > highest_y:
            highest_y = line[2]
        if line[1] < lowest_x:
            lowest_x = line[1]
        if line[2] < lowest_y:
            lowest_y = line[2]

    for e in range(number_of_edges):
        line = stdin[e+1+number_of_vertices]
        vertex1 = vertices[ int(line[0]) ]
        vertex2 = vertices[ int(line[1]) ]
        vertex2.add_neighbor( vertex1 )
        vertex1.add_neighbor( vertex2 )

    w.set_coordinates( highest_x, highest_y, lowest_x, lowest_y )

    #w.create_astar()
    w.set_vertices( vertices )
    w.loop()

if __name__ == "__main__":
    main()