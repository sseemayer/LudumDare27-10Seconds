import crowd.modes
import crowd.resource
import crowd.input
import crowd.web

import collections

from crowd.modes.action.challenge import Challenge, ChallengePlayer

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

        if self.game.upload:
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

