import window
import sys

def main():
    w = window.Window()

    stdin = []
    translation_table = dict.fromkeys(map(ord, '() \n'), None)
    for line in sys.stdin:
    	stdin.append(line.translate(translation_table).split(','))

    rows = stdin[0][0]
    columns = stdin[0][1]
    grid = w.create_grid(int(rows), int(columns))
    grid.update_cell(int(stdin[1][0]), int(stdin[1][1]), 'start')
    grid.update_cell(int(stdin[2][0]), int(stdin[2][1]), 'goal')



    w.loop()



if __name__ == "__main__":
    main()