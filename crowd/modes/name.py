
import crowd.modes
import crowd.resource
import crowd.input

import collections

import sys
import py2d.Math
import crowd.modes.action
import crowd.resource

import pygame
from pygame.locals import *

class NameEnterMode(crowd.modes.GameMode):

    def __init__(self, game):
        super(NameEnterMode, self).__init__(game)


        self.game.player_name = ''
        self.game.score = 0

        self.last_keys = collections.defaultdict(bool)

        self.prompt_font = crowd.resource.font.menu
        self.name_font = crowd.resource.font.menu
        self.manual_font = crowd.resource.font.default

        self.on_finish = None


        self.prompt = self.prompt_font.render('Please enter your name:', True, (128, 128, 128))
        self.prompt_size = py2d.Math.Vector(*self.prompt.get_size())

        self.manual = ['In game, use the ARROW KEYS or WSAD to control.', 'Now press ENTER to start the game.']

        self.manual = [self.manual_font.render(line, True, (128, 128, 128)) for line in self.manual]


    def update(self, time_elapsed):

        valid_keys = [ord(c) for c in 'abcdefghijklmnopqrstuvwxyz_.']
        full_keys = self.game.input.full_keys.copy()

        new_presses = set(k for k, v in full_keys.items() if v != self.last_keys[k] and v)

        for k in valid_keys:
            if k in new_presses:

                c = chr(k)

                if full_keys[pygame.K_LSHIFT] or full_keys[K_RSHIFT]:
                    c = c.upper()

                if len(self.game.player_name) < 15:
                    self.game.player_name += c
                    crowd.resource.sound.select.play()

        if full_keys[K_BACKSPACE]:
            self.game.player_name = self.game.player_name[:-1]
            crowd.resource.sound.select.play()

        if full_keys[K_RETURN] and len(self.game.player_name) >= 3 and len(self.game.player_name) <= 15:
            if self.on_finish:
                crowd.resource.sound.coin.play()
                self.on_finish()

        self.last_keys = full_keys


    def render(self):
        screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        self.game.screen.fill((0,0,0))

        name = self.name_font.render(self.game.player_name + "_", True, (255, 255, 255))
        name_size = py2d.Math.Vector(*name.get_size())

        self.game.screen.blit(name, (screen_size / 2 - name_size / 2).as_tuple())


        self.game.screen.blit(self.prompt, (screen_size.x / 2 - self.prompt_size.x / 2, 100))

        for i, man in enumerate(self.manual):
            self.game.screen.blit(man, (50, i * 30 + 350))


