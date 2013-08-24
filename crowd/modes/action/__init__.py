import crowd.modes
import crowd.resource
import crowd.input

import collections

class ActionMode(crowd.modes.GameMode):

    def __init__(self, game, queue):
        super(ActionMode, self).__init__(game)

        self.queue = collections.deque(queue)
        self.challenge = None

        self.next_game()


    def get_input_sources(self, challenge):
        #TODO Get live and cached input sources
        print("TODO: properly get input sources for {0}".format(challenge.name))

        live = crowd.input.LiveInputSource(self.game, 'semi', (255, 128, 0))

        return [live]

    def next_game(self):

        if self.challenge:
            self.challenge.leave()

        challenge_args = self.queue.popleft()
        challenge, extra_args = challenge_args[0], challenge_args[1:]

        input_sources = self.get_input_sources(challenge)

        self.challenge = challenge(self, input_sources, *extra_args)
        self.challenge.enter()

    def update(self, time_elapsed):
        if self.challenge:
            self.challenge.update(time_elapsed)

    def render(self):
        if self.challenge:
            self.challenge.render()

class Challenge(object):

    name = 'untitled'

    def __init__(self, mode, input_sources):

        self.mode = mode
        self.input_sources = input_sources

    def update(self, time_elapsed):
        pass

    def render(self):
        pass

    def enter(self):
        pass

    def leave(self):
        pass

class DebugChallenge(Challenge):

    name = 'debug'

    def __init__(self, mode, input_sources):
        super(DebugChallenge, self).__init__(mode, input_sources)

        self.font = crowd.resource.font.default

        self.blah = []

    def update(self, time_elapsed):

        def list_buttons(state):
            return ", ".join( k for k, v in state.keys.items() if v )

        self.blah = [
            (ins.player + ": " + list_buttons(ins.next_frame()) , ins.color)
            for ins in self.input_sources
        ]

    def render(self):

        self.mode.game.screen.fill((64, 64, 64))

        for i, b in enumerate(self.blah):
            txt, clr = b

            fr = self.font.render(txt, True, clr)
            self.mode.game.screen.blit(fr, (0,i * 20))

