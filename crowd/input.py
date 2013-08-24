import pygame
from pygame.locals import *

import crowd.constants
import json
import collections

class Input(object):

    def __init__(self, game, keymap = crowd.constants.KEY_MAPPING):
        self.game = game
        self.keymap = keymap

        self.keys = {k: False for k in crowd.constants.VALID_ACTIONS}

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.game.running = False

            elif event.type == KEYDOWN and event.key in self.keymap:
                self.keys[self.keymap[event.key]] = True

            elif event.type == KEYUP and event.key in self.keymap:
                self.keys[self.keymap[event.key]] = False

    @property
    def state(self):
        return InputState(self.keys.copy(), True)

class InputState(object):

    def __init__(self, keys, is_live):
        self.keys = keys
        self.is_live = is_live


    def __getattr__(self, name):
        if name in self.keys:
            return self.keys[name]
        else:
            raise AttributeError(name)

class InputSource(object):
    def __init__(self, game, player, color, is_live):
        self.game = game
        self.player = player
        self.color = color
        self.is_live = is_live

    def next_frame(self):
        raise NotImplemented()

class LiveInputSource(InputSource):

    def __init__(self, game, player, color):
        super(LiveInputSource, self).__init__(game, player, color, True)
        self.last_state = self.game.input.state

        self.updates = []

    def next_frame(self):

        state = self.game.input.state

        updates = { k: v for k, v in state.keys.items() if v != self.last_state.keys[k] }
        self.updates.append(updates)

        self.last_state = state

        return state

class CachedInputSource(InputSource):
    def __init__(self, game, player, color, cache):
        super(CachedInputSource, self).__init__(game, player, color, False)
        self.cache = collections.deque(cache)
        self.state = {k: False for k in crowd.constants.VALID_ACTIONS}

    def next_frame(self):

        update = self.cache.popleft()
        self.state.update(update)

        return self.state

