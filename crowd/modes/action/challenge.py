import py2d.Math

import crowd.constants
import crowd.resource
import math

class Challenge(object):

    name = 'untitled'

    def __init__(self, mode, input_sources):

        self.mode = mode
        self.input_sources = input_sources

        self.camera = py2d.Math.Vector(0, 0)

        self.countdown = 10000
        self.countdown_font = crowd.resource.font.big_gui

    def update(self, time_elapsed):
        self.countdown = max(0, self.countdown - time_elapsed)

        if self.countdown == 0:
            self.countdown_expired()

    def render(self):
        self.mode.game.screen.fill((0,0,0))

        countdown = self.countdown_font.render( "{0:.1f}".format(self.countdown / 1000.0), True, (64, 64, 64))

        size = py2d.Math.Vector(*countdown.get_size())
        screen = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        self.mode.game.screen.blit(countdown, (screen / 2 - size / 2).as_tuple())


    def countdown_expired(self):
        self.mode.next_challenge()

    def enter(self):
        pass

    def leave(self):
        for input_source in self.input_sources:
            input_source.leave()


class ChallengePlayer(object):
    def __init__(self, challenge, input_source):
        self.challenge = challenge
        self.input_source = input_source
        self.input = None

    def next_frame(self):
        self.input = self.input_source.next_frame()
