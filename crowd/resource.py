
import pygame

import crowd.constants

class ResourceManager(object):

    def __init__(self, resource_def, load_fn):
        self.resource_def = resource_def
        self.load_fn = load_fn
        self.resource_cache = { k: None for k in self.resource_def.keys() }


    def __getattr__(self, name):

        if name in self.resource_def:

            if not self.resource_cache[name]:
                self.resource_cache[name] = self.load_fn(name, self.resource_def[name])

            return self.resource_cache[name]

        else:
            raise AttributeError("I don't know resource {0}!".format(name))

def load_sound(n, sounddef):

    fn, volume = sounddef
    snd = pygame.mixer.Sound(fn)
    snd.set_volume(volume)

    return snd


image = ResourceManager(crowd.constants.RES_IMAGES, lambda n, fn: pygame.image.load(fn))
music = ResourceManager(crowd.constants.RES_MUSIC, lambda n, fn: pygame.mixer.music.load(fn))
sound = ResourceManager(crowd.constants.RES_SOUNDS, load_sound)
font  = ResourceManager(crowd.constants.RES_FONTS, lambda n, fontdef: pygame.font.Font(*fontdef))

