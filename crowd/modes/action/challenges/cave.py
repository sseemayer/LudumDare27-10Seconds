import crowd.constants
from crowd.modes.action.challenge import Challenge, ChallengePlayer
import crowd.entity_component as ec
import crowd.resource

from crowd.modes.action.challenges.gather import CoinComponent

import math
import itertools

import py2d.Math
import py2d.SVG
import pygame

class CaveChallenge(Challenge):
    name = 'cave'
    modal_msg = 'Avoid the walls!'

    def __init__(self, mode, input_sources):
        super(CaveChallenge, self).__init__(mode, input_sources)

        transform = py2d.Math.Transform.scale(crowd.constants.CAVE_SCALING, crowd.constants.CAVE_SCALING)
        self.cave = py2d.SVG.convert_svg('data/images/cave.svg', transform, bezier_max_divisions=2)

        startpos = self.cave['start'][0].points[0]
        coinspos = self.cave['coins'][0].points


        del self.cave['start']
        del self.cave['coins']


        self.camera = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / -2 + startpos

        self.players = [
            ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]

        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                Flyer(list(itertools.chain(self.cave.values()))),
                ec.Physics(decay_factor=crowd.constants.JUMP_PLAYER_SPEED_DECAY),
                ec.Owner(player),
                ec.Sprite(crowd.resource.image.cursor)
            ])

            for player in self.players
        ]


        self.cave_entity = ec.Entity( self, [
            Cave(list(itertools.chain(self.cave.values())))
        ])

        self.coin_entities = [
            ec.Entity(self, [
                ec.Position(pos),
                CoinComponent(gather_distance = crowd.constants.JUMP_GATHER_DISTANCE),
                ec.Sprite(crowd.resource.image.coin)
            ])

            for pos in coinspos
        ]

        self.entities = [self.cave_entity] + self.coin_entities + self.player_entities

    def update(self, time_elapsed):
        super(CaveChallenge, self).update(time_elapsed)

        if self.modal: return

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)


        self.camera = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / -2 + self.player_entities[-1].handle('get_position')

    def render(self):

        for entity in self.entities:
            entity.render()

        super(CaveChallenge, self).render()



class Flyer(ec.Component):
    def __init__(self, polys, speed=crowd.constants.CAVE_SPEED, boost_speed=crowd.constants.CAVE_BOOST_SPEED, gravity=crowd.constants.CAVE_GRAVITY):
        super(Flyer, self).__init__()
        self.polys = list(itertools.chain(*polys))

        self.speed = speed
        self.boost_speed = boost_speed
        self.gravity = gravity

        self.register_handler(self.update)
        self.register_handler(self.try_position)

    def update(self, component, entity, event, time_elapsed):
        owner = entity.handle('get_owner')
        acceleration = entity.handle('get_acceleration')
        velocity = entity.handle('get_velocity')

        acceleration.y = self.gravity

        if owner.input.up:
            acceleration.y = -self.boost_speed

        velocity.x = self.speed * (1.3-(entity.challenge.countdown / 10000))

        entity.handle('set_acceleration', acceleration)
        entity.handle('set_velocity', velocity)


    def try_position(self, component, entity, event, newpos):

        for poly in self.polys:
            if poly.contains_point(newpos):

                entity.challenge.entities.remove(entity)

                owner = entity.handle('get_owner')
                if owner.input_source.is_live:
                    entity.challenge.countdown = 0



class Cave(ec.Component):
    def __init__(self, polys):
        super(Cave, self).__init__()
        self.polys = list(itertools.chain(*polys))

        self.register_handler(self.render)

    def render(self, component, entity, event):

        transform = py2d.Math.Transform.move(*(entity.challenge.camera * -1).as_tuple())

        for poly in self.polys:
            pygame.draw.polygon(entity.challenge.mode.game.screen, (32, 32, 32), [(transform * p).as_tuple() for p in poly.points])


