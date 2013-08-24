import crowd.modes
import collections

class ActionMode(crowd.modes.GameMode):

    def __init__(self, game, queue):
        super(ActionMode, self).__init__(self, game)

        self.queue = collections.deque(queue)
        self.challenge = None

        self.next_game()

    def next_game(self):

        if self.challenge:
            self.challenge.leave()

        self.challenge = self.queue.popleft()
        self.challenge.enter()

    def update(self, time_elapsed):
        if self.challenge:
            self.challenge.update(time_elapsed)

    def render(self):
        if self.challenge:
            self.challenge.render()

class Challenge(object):

    name = 'untitled'

    def __init__(self, mode):

        self.mode = mode

    def update(self, time_elapsed):
        pass

    def render(self):
        pass

    def enter(self):
        pass

    def leave(self):
        pass
