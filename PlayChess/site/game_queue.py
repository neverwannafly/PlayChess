## A rudimentary game queueing class.

from .message import ComprehensiveMessage

class GameQueue:

    def __init__(self):
        self._queue = []

    def _add(self, player):
        if len(self._queue) == 0:
            self._queue.append(player)
            return ComprehensiveMessage("Player Added Successfully!", 1, success=True)

        elif len(self._queue) == 1:
            self._queue.append(player)
            return ComprehensiveMessage("2 Players in the Queue!", 2, success=True)

        else:
            return ComprehensiveMessage("Game Queue Full!", -1)

    def _generate_url(self):
        self._queue.sort()
        url = "{0}-{1}".format(_queue[0], _queue[1])
        return url

    def add_to_queue(self, player):
        addition = self._add(player)
        if addition.code == 2:
            print(addition.message)
            url = self._generate_url()
            del self._queue[:]
            return url

        print(addition.message)
        return None
