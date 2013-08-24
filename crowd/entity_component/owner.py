from crowd.entity_component.base import Component

class Owner(Component):

    def __init__(self, owner):
        super(Owner, self).__init__()
        self.owner = owner

        self.register_handler(self.get_owner)
        self.register_handler(self.set_owner)

    def get_owner(self, component, entity, event):
        return self.owner

    def set_owner(self, component, entity, event, value):
        self.owner = value


