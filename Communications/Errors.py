class OutOfBoundsError(Exception):
    """Custom exception for moves that are out of bounds on the game board."""
    def __init__(self, message="Selected position is out of bounds."):
        self.message = message
        super().__init__(self.message)

class InvalidPosition(Exception): 
    def __init__(self, message="Selected position is already used."):
        self.message = message
        super().__init__(self.message)
class win(Exception):
    def __init__(self, message="Won"):
        self.message = message
        super().__init__(self.message)