from crowd.entity_component.base import Component

class Angle(Component):

    def __init__(self, angle):
        super(Angle, self).__init__()
        self.angle = angle

        self.register_handler(self.get_angle)
        self.register_handler(self.set_angle)

    def get_angle(self, component, entity, event):
        return self.angle

    def set_angle(self, component, entity, event, value):
        self.angle = value


