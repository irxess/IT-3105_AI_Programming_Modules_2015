import sys
import os
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/AStar') )
import window


def main():
    w = window.Window()

    stdin = []
    translation_table = dict.fromkeys(map(ord, '() \n'), None)
    for line in sys.stdin:
        # translate )( to ,
        line = line.replace(') (', ',')
        line = line.replace(')(', ',')
        stdin.append(line.translate(translation_table).split(','))
        stdin[-1] = [ int(x) for x in stdin[-1] ]

    rows = stdin[0][0]
    columns = stdin[0][1]
    w.create_grid(rows, columns)
    w.update_cell(stdin[1][0], stdin[1][1], 'start')
    w.update_cell(stdin[2][0], stdin[2][1], 'goal')

    # for each wall
    for i in range(0, len(stdin[3])-1, 4):
        # for each piece in row
        for row_offset in range(stdin[3][i+2]):
        	# for each piece in column
            for col_offset in range(stdin[3][i+3]):
                x = stdin[3][i] + row_offset
                y = stdin[3][i + 1] + col_offset
                w.update_cell(x, y, 'blocked')

    w.create_astar()
    w.loop()


if __name__ == "__main__":
    main()
