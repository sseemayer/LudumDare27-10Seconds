from crowd.entity_component.base import Component

import py2d.Math

class Physics(Component):

    def __init__(self, decay_factor=1, velocity=None):
        super(Physics, self).__init__()

        self.decay_factor = decay_factor


        if velocity:
            self.velocity = velocity.clone()
        else:
            self.velocity = py2d.Math.Vector(0, 0)

        self.register_handler(self.update)

        self.register_handler(self.get_velocity)
        self.register_handler(self.set_velocity)

        self.register_handler(self.get_acceleration)
        self.register_handler(self.set_acceleration)

    def get_velocity(self, component, entity, event):
        return self.velocity

    def set_velocity(self, component, entity, event, value):
        self.velocity = value


    def get_acceleration(self, component, entity, event):
        return self.acceleration

    def set_acceleration(self, component, entity, event, value):
        self.acceleration = value

    def update(self, component, entity, event, time_elapsed):

        position = entity.handle('get_position')
        velocity = entity.handle('get_velocity')

        acceleration = entity.handle('get_acceleration')

        velocity += acceleration * time_elapsed

        if self.decay_factor != 1:
            velocity = velocity * self.decay_factor

        entity.handle('set_velocity', velocity)

        new_position = position + velocity * time_elapsed
        npos = entity.handle('try_position', new_position)

        if npos:
            new_position = npos

        entity.handle('set_position', new_position)


