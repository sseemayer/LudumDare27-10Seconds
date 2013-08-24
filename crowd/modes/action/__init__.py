import crowd.modes
import crowd.resource
import crowd.input
import crowd.web

import collections

class ActionMode(crowd.modes.GameMode):

    def __init__(self, game, queue):
        super(ActionMode, self).__init__(game)

        self.queue = collections.deque(queue)
        self.challenge = None

        self.next_challenge()


        self.on_finish = None

    def get_input_sources(self, challenge):

        input_sources = crowd.web.get_challenge_replays(self.game, challenge.name)

        live = crowd.input.LiveInputSource(self.game, self.game.player_name, self.game.player_color, challenge.name)

        def leave_live(live):
            crowd.web.post_challenge_replay(live)

        live.on_leave = leave_live

        input_sources.append(live)

        return input_sources

    def next_challenge(self):

        if self.challenge:
            self.challenge.leave()


        if self.queue:

            challenge_args = self.queue.popleft()
            challenge, extra_args = challenge_args[0], challenge_args[1:]

            input_sources = self.get_input_sources(challenge)

            self.challenge = challenge(self, input_sources, *extra_args)
            self.challenge.enter()

        else:

            self.challenge = None

            if self.on_finish:
                self.on_finish()

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
        for input_source in self.input_sources:
            input_source.leave()

class DebugChallenge(Challenge):

    name = 'debug'

    def __init__(self, mode, input_sources):
        super(DebugChallenge, self).__init__(mode, input_sources)

        self.font = crowd.resource.font.default

        self.blah = []

    def update(self, time_elapsed):


        states = [(ins, ins.next_frame()) for ins in self.input_sources]

        def list_buttons(state):
            return ", ".join( k for k, v in state.keys.items() if v )

        self.blah = [
            (ins.player + ": " + list_buttons(state) , ins.color)
            for ins, state in states
        ]


        for ins, state in states:
            if state.a and state.b and state.up and state.down:
                self.mode.next_challenge()

    def render(self):

        self.mode.game.screen.fill((64, 64, 64))

        for i, b in enumerate(self.blah):
            txt, clr = b

            fr = self.font.render(txt, True, clr)
            self.mode.game.screen.blit(fr, (0,i * 20))

