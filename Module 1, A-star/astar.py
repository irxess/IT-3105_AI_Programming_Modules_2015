
class AStar:

    def return_result(self):
        grid = []
        for row in range(10):
            grid.append([])
            for column in range(10):
                grid[row].append(0)  # Append a cell
        grid[1][5] = 1

        return grid
