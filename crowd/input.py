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
    def __init__(self, game, player, color, challenge, is_live, on_leave=None):
        self.game = game
        self.player = player
        self.color = color
        self.challenge = challenge
        self.is_live = is_live
        self.on_leave = on_leave

    def next_frame(self):
        raise NotImplemented()

    def leave(self):
        if self.on_leave:
            self.on_leave(self)

class LiveInputSource(InputSource):

    def __init__(self, game, player, color, challenge, on_leave=None):
        super(LiveInputSource, self).__init__(game, player, color, challenge, True, on_leave)
        self.last_state = {k: False for k in crowd.constants.VALID_ACTIONS}

        self.updates = []

    def next_frame(self):

        state = self.game.input.keys.copy()

        updates = { k: v for k, v in state.items() if v != self.last_state[k] }
        self.updates.append(updates)

        self.last_state = state

        return InputState(state, True)

class CachedInputSource(InputSource):
    def __init__(self, game, player, color, challenge, cache, on_leave=None):
        super(CachedInputSource, self).__init__(game, player, color, challenge, False, on_leave)
        self.cache = collections.deque(cache)
        self.state = {k: False for k in crowd.constants.VALID_ACTIONS}

    def next_frame(self):
        if self.cache:
            update = self.cache.popleft()
            self.state.update(update)

        return InputState(self.state, False)

