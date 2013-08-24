import collections
import sys

import pygame
from pygame.locals import *

import crowd.constants
import crowd.input

class Game(object):

    def __init__(self, upload=True):
        pygame.init()

        self.upload = upload

        self.screen = pygame.display.set_mode(crowd.constants.SCREEN_SIZE)

        self.running = False
        self.mode = None

        self.input = crowd.input.Input(self)

        self.tick = 0
        self.total_time = 0

        self.player_name = 'semi'
        self.player_color = (255, 128, 0)
        self.score = 0

        pygame.display.set_caption(crowd.constants.GAME_NAME)


    def loop(self):
        self.running = True
        while self.running:

            # we need fixed timestep to replay with inputs
            pygame.time.wait(1000 / crowd.constants.TARGET_FPS)
            time_elapsed = 1000 / crowd.constants.TARGET_FPS

            self.input.handle_events()
            self.update(time_elapsed)
            self.render()

        self.exit()


    def exit(self):
        self.running = False
        pygame.quit()
        sys.exit()


    def update(self, time_elapsed):
        self.tick += 1
        self.total_time += time_elapsed

        if self.mode:
            self.mode.update(time_elapsed)

    def render(self):
        if self.mode:
            self.mode.render()

        else:

            if self.input.state.a:

                self.screen.fill(crowd.constants.NOMODE_BACKGROUND)
            else:
                self.screen.fill((128,0,0))

        pygame.display.update()




