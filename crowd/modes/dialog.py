import crowd.modes
import crowd.resource
import crowd.input

import collections

import sys
import py2d.Math
import crowd.modes.action

import pygame

class DialogMode(crowd.modes.GameMode):

    def __init__(self, game, title, messages):
        super(DialogMode, self).__init__(game)

        self.logo = crowd.resource.image.logo
        self.logo_size = py2d.Math.Vector(*self.logo.get_size())

        self.font_big = crowd.resource.font.med_gui
        self.font_message = crowd.resource.font.menu


        self.on_finish = None

        self.last_state = self.game.input.state.keys.copy()

        self.messages = messages

        def render_message(msg):

            color = (128, 128, 128)
            if isinstance(msg, tuple):
                msg, color = msg

            return self.font_message.render(msg, True, color)

        self.messages = [ render_message(msg) for msg in self.messages]
        self.message_sizes = [ py2d.Math.Vector(*msg.get_size()) for msg in self.messages]

        self.title = self.font_big.render(title, True, (255, 255, 255))
        self.title_size = py2d.Math.Vector(*self.title.get_size())


    def update(self, time_elapsed):

        state = self.game.input.state.keys.copy()
        if not self.last_state['a'] and state['a']:
            if self.on_finish:
                self.on_finish()

        self.last_state = state

    def render(self):
        screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)
        self.game.screen.fill((0,0,0))


        self.game.screen.blit(self.title, (screen_size.x / 2 - self.title_size.x / 2, 50))

        for i, msg, msg_size in zip(range(len(self.messages)), self.messages, self.message_sizes):
            self.game.screen.blit(msg, (screen_size.x / 2 - msg_size.x / 2, 50 + self.title_size.y + 50 + 35 * i))




