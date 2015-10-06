from abc import ABCMeta, abstractmethod

class AbstractVariable():
    __metaclass__ = ABCMeta

    def __init__(self, domain):
        self.domain = domain
        self.neighbors = []


    def __eq__(self, vi):
        return (self.getID() == vi.getID())

    @abstractmethod
    def __repr__(self):
        return 'vertex(x=%s, y=%s, color=%s, domain=%s)' %(self.getID, self.domain)


    def add_neighbor(self, vertex):
        self.neighbors.append(vertex)


    def getNeighbors(self):
        return self.neighbors


    @abstractmethod
    def getID(self):
        pass


    def isSatisfied(self, args, n, constraint):
        return constraint(*args)

    # def isSatisfied(self, pair, n, constraint):
        # return constraint(pair[0], pair[1])
