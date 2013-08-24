from crowd.entity_component.base import Component

import py2d.Math

class Movement(Component):

    def __init__(self, speed=1, horizontal=True, vertical=True):
        super(Movement, self).__init__()

        self.speed = speed
        self.horizontal = horizontal
        self.vertical = vertical

        self.register_handler(self.update)

    def update(self, component, entity, event, time_elapsed):

        owner = entity.handle('get_owner')
        position = entity.handle('get_position')

        dx = py2d.Math.Vector(0, 0)

        if self.horizontal:
            if owner.input.left:
                dx.x -= 1

            if owner.input.right:
                dx.x += 1

        if self.vertical:
            if owner.input.up:
                dx.y -= 1

            if owner.input.down:
                dx.y += 1

        entity.handle('set_position', position + dx.clamp() * self.speed)


