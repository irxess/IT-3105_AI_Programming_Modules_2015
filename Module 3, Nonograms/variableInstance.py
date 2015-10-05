from abstractVariable import AbstractVariable

class VI(AbstractVariable):
    def __init__(self, ID, domain):
        (isRow, index) = ID
        self.isRow = isRow
        self.index = index
        self.length = len(domain[0])
        super(VI, self).__init__(domain)


    def __repr__(self):
        if self.isRow:
            r = 'Row:'
        else:
            r = 'Column:'
        return 'vertex(%s, index=%s, domain=%s)' %(r, self.index, self.domain)


    def drawColorsToGUI(self, gui):
        if len(self.domain)==1:
            if self.isRow:
                for i in range( self.length ):
                    gui.grid[self.index][i] = self.domain[0][i]
            else: # is column
                for i in range( self.length ):
                    gui.grid[i][self.index] = self.domain[0][i]


    def getID(self):
        return (self.isRow, self.index)


    def isSatisfied(self, pair, neighbor, constraint):
            viCell = pair[0][neighbor.index]
            nCell = pair[1][self.index]
            return constraint(viCell, nCell)
