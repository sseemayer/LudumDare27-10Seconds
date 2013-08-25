import crowd.modes
import crowd.resource
import crowd.input

import collections

import py2d.Math

class MenuMode(crowd.modes.GameMode):

    def __init__(self, game):
        super(MenuMode, self).__init__(game)

        self.logo = crowd.resource.image.logo
        self.logo_size = py2d.Math.Vector(*self.logo.get_size())

        self.last_input = game.input

    def update(self, time_elapsed):
        input = self.game.input

        self.last_input = input

    def render(self):
        screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        self.game.screen.fill((0,0,0))
        self.game.screen.blit(self.logo, (screen_size.x/2 - self.logo_size.x /2, 50))

