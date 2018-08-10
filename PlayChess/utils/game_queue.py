## A rudimentary game queueing class.

from .message import ComprehensiveMessage

class GameQueue:

    def __init__(self):
        self._queue = []

    def _add(self, player):
        
        if player not in self._queue:

            if len(self._queue) == 0:
                self._queue.append(player)
                return ComprehensiveMessage("Player Added Successfully!", 1, success=True)

            elif len(self._queue) == 1:
                self._queue.append(player)
                return ComprehensiveMessage("2 Players in the Queue!", 2, success=True)

            else:
                return ComprehensiveMessage("Game Queue Full!", 0)

        else:
            return ComprehensiveMessage("Player Already in Game!", 3)

    def _generate_url(self):
        self._queue.sort()
        url = "{0}-{1}".format(self._queue[0], self._queue[1])
        return url

    def add_to_queue(self, player):
        addition = self._add(player)
        if addition.code == 2:
            url = self._generate_url()
            addition.info = url
            del self._queue[:]

        return addition

    def remove(self, username):
        self._queue.remove(username)

    def print_queue(self):
        print(self._queue)