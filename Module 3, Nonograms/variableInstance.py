class VI():
    def __init__(self, ID, domain):
        (isRow, index) = ID
        self.isRow = isRow
        self.index = index
        self.neighbors = []
        self.domain = domain
        self.length = len(domain[0])


    def __eq__(self, vi):
        return (self.getID() == vi.getID())
        # return (self.variable.x == vi.variable.x and self.variable.y == vi.variable.y and self.comp(self.domain, vi.domain))


    def __repr__(self):
        # print_string = ('VI %s,%s: %s' %(x,y,self.domain))
        # for color in self.domain:
        #     print_string += '(%s,%s,%s),' %(color[0],color[1],color[2])
        if self.isRow:
            r = 'Row:'
        else:
            r = 'Column:'
        return 'vertex(%s, index=%s, domain=%s)' %(r, self.index, self.domain)


    # def comp(self, x, y):
    #     for i in x:
    #         if i not in y:
    #             return False
    #     return True


    def add_neighbor(self, vertex):
        self.neighbors.append(vertex)


    def getPosition(self):
        return (self.isRow,self.index)


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
