import crowd.constants
import crowd.modes.action as am
import crowd.entity_component as ec
import crowd.resource

import py2d.Math

class GatherChallenge(am.Challenge):
    name = 'gather'

    def __init__(self, mode, input_sources):
        super(GatherChallenge, self).__init__(mode, input_sources)

        startpos = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / 2

        self.players = [
            am.ChallengePlayer(self, isrc)
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

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)

    def render(self):
        super(GatherChallenge, self).render()


        for entity in self.entities:
            entity.render()


class CoinComponent(ec.Component):
    def __init__(self):
        super(CoinComponent, self).__init__()

        self.register_handler(self.update)

    def update(self, component, entity, event, time_elapsed):

        position = entity.handle('get_position')

        for player in entity.challenge.player_entities:
            owner = player.handle('get_owner')

            if owner.input_source.is_live:
                plr_position = player.handle('get_position')

                delta = (position - plr_position).length

                if delta < crowd.constants.GATHER_DISTANCE:
                    entity.challenge.entities.remove(entity)
                    entity.challenge.mode.game.score += crowd.constants.GATHER_SCORE

