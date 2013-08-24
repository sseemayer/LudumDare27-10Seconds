from crowd.entity_component.base import Component
import crowd.resource

from pygame.locals import *
import py2d.Math

class Sprite(Component):

    def __init__(self, sprite):
        super(Sprite, self).__init__()
        self.sprite = sprite
        self.font = crowd.resource.font.default

        self.register_handler(self.get_sprite)
        self.register_handler(self.set_sprite)
        self.register_handler(self.render)

    def get_sprite(self, component, entity, event):
        return self.sprite

    def set_sprite(self, component, entity, event, value):
        self.sprite = value

    def render(self, component, entity, event):

        size = py2d.Math.Vector(*self.sprite.get_size())

        position = entity.handle('get_position')
        owner = entity.handle('get_owner')

        camera = entity.challenge.camera

        camera_pos = position - camera - size / 2

        sprite = self.sprite
        if owner:
            sprite = self.sprite.copy()
            sprite.fill(owner.input_source.color, special_flags=BLEND_RGB_MULT)

            owner_name = self.font.render(owner.input_source.player, True, owner.input_source.color)
            entity.challenge.mode.game.screen.blit(owner_name, (camera_pos + size/2).as_tuple())

        entity.challenge.mode.game.screen.blit(sprite, camera_pos.as_tuple())


