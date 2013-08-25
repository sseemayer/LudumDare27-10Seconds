import crowd.constants
from crowd.modes.action.challenge import Challenge, ChallengePlayer
import crowd.entity_component as ec
import crowd.resource

import py2d.Math

class RainbowChallenge(Challenge):
    name = 'rainbow'
    modal_msg = 'Pick a color!'

    def __init__(self, mode, input_sources):

        mode.game.player_color = (255, 255, 255)

        super(RainbowChallenge, self).__init__(mode, input_sources)

        startpos = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / 2


        self.rainbow = crowd.resource.image.rainbow
        self.rainbow_size = py2d.Math.Vector(*self.rainbow.get_size())

        self.screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        self.players = [
            ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]

        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                ec.Movement(speed=crowd.constants.GATHER_PLAYER_SPEED),
                ec.Physics(decay_factor=crowd.constants.GATHER_PLAYER_SPEED_DECAY),
                ec.Owner(player),
                ec.Sprite(crowd.resource.image.cursor),
                TakeColor()
            ])

            for player in self.players
        ]

        self.entities = self.player_entities

    def update(self, time_elapsed):
        super(RainbowChallenge, self).update(time_elapsed)

        if self.modal: return

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)


    def render(self):

        self.mode.game.screen.blit(self.rainbow, (self.screen_size / 2 - self.rainbow_size / 2).as_tuple())

        for entity in self.entities:
            entity.render()

        super(RainbowChallenge, self).render()


class TakeColor(ec.Component):

    def __init__(self):
        super(TakeColor, self).__init__()

        self.register_handler(self.update)


    def update(self, component, entity, event, time_elapsed):

        owner = entity.handle('get_owner')
        owner.input_source.color = (0, 0, 0)

        if owner.input_source.is_live:

            owner.input_source.color = (255, 255, 255)

            pos = entity.handle('get_position')

            rainbow_tl = entity.challenge.screen_size / 2 - entity.challenge.rainbow_size / 2

            rainbow_pos = pos - rainbow_tl

            if rainbow_pos.x >= 0 and rainbow_pos.x <= entity.challenge.rainbow_size.x and rainbow_pos.y >= 0 and rainbow_pos.y <= entity.challenge.rainbow_size.y:

                rainbow_color = entity.challenge.rainbow.get_at((int(rainbow_pos.x), int(rainbow_pos.y)))
                entity.challenge.mode.game.player_color = (rainbow_color[0], rainbow_color[1], rainbow_color[2])

