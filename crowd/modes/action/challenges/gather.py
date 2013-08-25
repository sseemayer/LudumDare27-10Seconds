import crowd.constants
from crowd.modes.action.challenge import Challenge, ChallengePlayer
import crowd.entity_component as ec
import crowd.resource

import py2d.Math

class GatherChallenge(Challenge):
    name = 'gather'
    modal_msg = 'Grab all you can!'

    def __init__(self, mode, input_sources):
        super(GatherChallenge, self).__init__(mode, input_sources)

        startpos = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / 2

        self.players = [
            ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]

        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                ec.Movement(speed=crowd.constants.GATHER_PLAYER_SPEED),
                ec.Physics(),
                ec.Owner(player),
                ec.Sprite(crowd.resource.image.cursor)
            ])

            for player in self.players
        ]

        self.coin_entities = [
            ec.Entity(self, [
                ec.Position(py2d.Math.Vector(
                    x * crowd.constants.SCREEN_SIZE[0] / (crowd.constants.GATHER_COINS_X),
                    y * crowd.constants.SCREEN_SIZE[1] / (crowd.constants.GATHER_COINS_Y)
                )),
                CoinComponent(),
                ec.Sprite(crowd.resource.image.coin)
            ])
            for x in range(1, crowd.constants.GATHER_COINS_X)
            for y in range(1, crowd.constants.GATHER_COINS_Y)
        ]

        self.entities = self.coin_entities + self.player_entities

    def update(self, time_elapsed):
        super(GatherChallenge, self).update(time_elapsed)

        if self.modal: return

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)

    def render(self):
        for entity in self.entities:
            entity.render()

        super(GatherChallenge, self).render()

class CoinComponent(ec.Component):
    def __init__(self, gather_distance = crowd.constants.GATHER_DISTANCE):
        super(CoinComponent, self).__init__()

        self.gather_distance = gather_distance
        self.register_handler(self.update)

    def update(self, component, entity, event, time_elapsed):

        position = entity.handle('get_position')

        for player in entity.challenge.player_entities:
            owner = player.handle('get_owner')

            if owner.input_source.is_live:
                plr_position = player.handle('get_position')

                delta = (position - plr_position).length

                if delta < self.gather_distance:

                    crowd.resource.sound.coin.play()
                    entity.challenge.entities.remove(entity)
                    entity.challenge.mode.game.score += crowd.constants.GATHER_SCORE

