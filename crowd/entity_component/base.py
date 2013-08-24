import collections
import inspect

def entity_definition(*components):

    def ensure_instance(comp):
        if inspect.isclass(comp):
            return comp()

        elif type(comp) == tuple:
            comp, args = comp[0], comp[1:]
            return comp(args)

        return comp

    def make_instance(challenge):

        instance_components = [ ensure_instance(comp) for comp in components ]

        return Entity(challenge, instance_components)

    return make_instance

class Entity(object):

    def __init__(self, challenge, components = []):
        self.challenge = challenge
        self.components = components


    def handle(self, event, *extra_args):
        for component in self.components:
            ret = component.handle(self, event, *extra_args)

            if ret:
                return ret

    def update(self, time_elapsed):
        self.handle('update', time_elapsed)

    def render(self):
        self.handle('render')



class Component(object):

    def __init__(self):
        self.handlers = collections.defaultdict(list)

    def handle(self, entity, event, *extra_args):
        for handler in self.handlers[event]:
            ret = handler(self, entity, event, *extra_args)
            if ret:
                return ret

    def register_handler(self, handler, name=None):
        if not name:
            name = handler.func_name

        self.handlers[name].append(handler)





