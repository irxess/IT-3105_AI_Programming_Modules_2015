class BoardController():
    
    def __init__(self):
        self.board = [0] * 4*4
        randomPosition = 4
        randomValue = 2
        self.insertTile( randomPosition, randomValue )
        # TODO:initialize GUI using visuals


    """
    Move all tiles as far in direction as possible.
    Use merge() if needed.
    """
    def slide(self, direction):
        pass


    """
    Merge two tiles.
    """
    def merge(self, position):
        pass


    def insertTile( self, position, value ):
        self.board[position] = value


    """
    Actually move. Slide first, then insertTile.
    Update GUI
    """
    def move(self, direction):
        pass

