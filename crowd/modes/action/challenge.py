import py2d.Math

import crowd.constants
import crowd.resource
import math

class Challenge(object):

    name = 'untitled'
    modal_msg = 'override me!'

    def __init__(self, mode, input_sources):

        self.modal = Modal(self)
        self.mode = mode
        self.input_sources = input_sources

        self.camera = py2d.Math.Vector(0, 0)

        self.countdown = 10000
        self.countdown_font = crowd.resource.font.big_gui

    def update(self, time_elapsed):

        if self.modal:
            self.modal.update(time_elapsed)

        else:
            self.countdown = max(0, self.countdown - time_elapsed)

            if self.countdown == 0:
                self.countdown_expired()

    def render(self):

        if self.modal:
            self.modal.render()
        else:
            countdown = self.countdown_font.render( "{0:.1f}".format(self.countdown / 1000.0), True, (64, 64, 64))

            size = py2d.Math.Vector(*countdown.get_size())
            screen = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

            self.mode.game.screen.blit(countdown, (screen - size).as_tuple())


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


class Modal(object):

    def __init__(self, challenge):
        self.challenge = challenge

        self.countdown = 1000
        self.countdown_font = crowd.resource.font.big_gui
        self.message_font = crowd.resource.font.med_gui

    def update(self, time_elapsed):
        self.countdown = max(0, self.countdown - time_elapsed)

        if self.countdown == 0:
            self.challenge.modal = None

    def render(self):

        msg = self.message_font.render(self.challenge.modal_msg, True, (255, 255, 255))
        countdown = self.countdown_font.render("{0:.1f}".format(self.countdown / 1000.0), True, (128, 128, 128))

        screen = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)
        msg_size = py2d.Math.Vector(*msg.get_size())
        countdown_size = py2d.Math.Vector(*countdown.get_size())

        total_size = py2d.Math.Vector(max(msg_size.x, countdown_size.x), msg_size.y + countdown_size.y + crowd.constants.MODAL_PADDING)

        self.challenge.mode.game.screen.blit(msg, (screen / 2 - msg_size / 2).as_tuple())
        self.challenge.mode.game.screen.blit(countdown, (screen / 2 - countdown_size / 2 + py2d.Math.VECTOR_Y * (msg_size.y + crowd.constants.MODAL_PADDING) ).as_tuple())

