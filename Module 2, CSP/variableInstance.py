from abstractVariable import AbstractVariable

class VI(AbstractVariable):
    def __init__(self, position, domain):
        self.x,self.y = position
        self.color = (0,0,0)
        super(VI, self).__init__(domain)


    def __repr__(self):
        return 'vertex(x=%s, y=%s, color=%s, domain=%s)' %(self.x, self.y, self.color,self.domain)


    def getID(self):
        return (self.x,self.y)


    def getColor(self):
        if len(self.domain) == 1:
            self.color = self.domain[0]
        return self.color


    def getPosition(self):
        return self.getID()
