from crowd.entity_component.base import Component
import crowd.resource

import math

import pygame
from pygame.locals import *

import py2d.Math

class Sprite(Component):

    def __init__(self, sprite, hide_owner=False):
        super(Sprite, self).__init__()
        self.sprite = sprite
        self.font = crowd.resource.font.default
        self.hide_owner = hide_owner

        self.register_handler(self.get_sprite)
        self.register_handler(self.set_sprite)
        self.register_handler(self.render)

    def get_sprite(self, component, entity, event):
        return self.sprite

    def set_sprite(self, component, entity, event, value):
        self.sprite = value

    def render(self, component, entity, event):

        position = entity.handle('get_position')
        angle = entity.handle('get_angle')
        owner = entity.handle('get_owner')

        sprite = self.sprite

        if angle:
            sprite = pygame.transform.rotozoom(sprite, -angle / math.pi * 180, 1.0)

        size = py2d.Math.Vector(*sprite.get_size())

        camera = entity.challenge.camera
        camera_pos = position - camera - size / 2

        if owner:
            sprite = sprite.copy()
            sprite.fill(owner.input_source.color, special_flags=BLEND_RGB_MULT)

            if not self.hide_owner:
                owner_name = self.font.render(owner.input_source.player, True, owner.input_source.color)
                entity.challenge.mode.game.screen.blit(owner_name, (camera_pos + size/2).as_tuple())

        entity.challenge.mode.game.screen.blit(sprite, camera_pos.as_tuple())


