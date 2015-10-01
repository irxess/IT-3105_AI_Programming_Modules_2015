import sys
import os
current_directory = sys.path[0]
sys.path.append( os.path.abspath('../Common/') )
import window


def find_box_index( array, box_nr ):
    i = 0
    while i < len(array):
        if array[i] == 'black':
            box_nr -= 1
            if box_nr == 0:
                start = i
                end = i
            i += 1
            while i < len(array):
                if array[i] == 'black':
                    if box_nr == 0:
                        end = i
                    i += 1
                else:
                    break
        else:
            i += 1
        if box_nr == 0:
            return (start,end)


def generateDomain( array, box_nr ):
    r = []
    (i,j) = find_box_index( array, box_nr )
    while j < len(array):
        if box_nr > 1:
            r += ( generateDomain( array.copy(), box_nr-1 ))
        if (j<len(array)-1 and array[j+1] == 'white') and ((j < len(array) - 2 and array[j+2] == 'white') or j==len(array)-2):
                array[i] = 'white'
                array[j+1] = 'black'
                r.append(array.copy())
                i += 1
                j += 1
        else:
            return r
    return r


def main():

    stdin = []
    for line in sys.stdin:
        stdin.append(line.split(' '))
        stdin[-1] = [ int(x) for x in stdin[-1] ]

    print(stdin[0])
    row_length = stdin[0][0]
    column_length = stdin[0][1]
    row_count = column_length
    column_count = row_length

    rows = []
    columns = []

    for r in range(row_count):
        row = ['white']*row_length
        row_offset = 0
        for block in stdin[r+1]:
            for cell in range(block):
                row[row_offset] = 'black'
                row_offset += 1
            row_offset += 1
        rows.append(row.copy())

    for c in range(column_count):
        column = ['white']*column_length
        col_offset = 0
        for block in stdin[c+1+row_count]:
            for cell in range(block):
                column[col_offset] = 'black'
                col_offset += 1
            col_offset += 1
        columns.append(column.copy())

    rows_domain = []
    for i,r in enumerate(rows):
        l = []
        l.append(r)
        l += generateDomain( r.copy(), len(stdin[i+1]))
        rows_domain.append(l.copy())

    column_domain = []
    for i,c in enumerate(columns):
        l = []
        l.append(c)
        l += generateDomain( c.copy(), len(stdin[i+1+row_count]) )
        column_domain.append(l.copy())

    # TODO: None should be variables
    w = window.Window(None, (rows_domain,column_domain), row_count, column_count, 500, 750)

    # w.create_astar()
    w.loop()


if __name__ == "__main__":
    main()