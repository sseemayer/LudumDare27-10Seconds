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
                ec.Position(startpos.clone())
            ])
            for _ in range(100)
        ]

        self.entities = self.player_entities + self.coin_entities

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

