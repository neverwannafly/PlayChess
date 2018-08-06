## A rudimentary game queueing class.

class GameQueue:
    
    def __init__(self):
        
        self._queue = []
        self._limit = 2 
