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

class RaceChallenge(Challenge):
    name = 'race'
    modal_msg = 'Ready, set, go!'

    def __init__(self, mode, input_sources):
        super(RaceChallenge, self).__init__(mode, input_sources)

        transform = py2d.Math.Transform.scale(crowd.constants.RACE_TRACK_SCALING, crowd.constants.RACE_TRACK_SCALING)
        self.racetrack_coords = py2d.SVG.convert_svg('data/images/racetrack.svg', transform, bezier_max_divisions=3)

        self.racetrack_outer = self.racetrack_coords['track-outer']
        self.racetrack_inner = self.racetrack_coords['track-inner']
        self.racetrack_mid = self.racetrack_coords['track-mid']

        startpos = self.racetrack_mid[0].points[52]

        self.camera = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / -2 + startpos

        self.players = [
            ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]

        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                ec.Angle(math.pi / 2),
                Racer(self.racetrack_inner[0], self.racetrack_outer[0]),
                #ec.Physics(decay_factor=crowd.constants.JUMP_PLAYER_SPEED_DECAY),
                ec.Owner(player),
                ec.Sprite(crowd.resource.image.pointer)
            ])

            for player in self.players
        ]


        self.racetrack_entity = ec.Entity( self, [
            Racetrack(self.racetrack_inner, self.racetrack_outer)
        ])

        self.coin_entities = [
            ec.Entity(self, [
                ec.Position(pos),
                CoinComponent(gather_distance = crowd.constants.JUMP_GATHER_DISTANCE),
                ec.Sprite(crowd.resource.image.coin)
            ])

            for pos in self.racetrack_mid[0].points
        ]

        self.entities = [self.racetrack_entity] + self.coin_entities + self.player_entities

    def update(self, time_elapsed):
        super(RaceChallenge, self).update(time_elapsed)

        if self.modal: return

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)


        self.camera = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / -2 + self.player_entities[-1].handle('get_position')

    def render(self):

        for entity in self.entities:
            entity.render()

        super(RaceChallenge, self).render()



class Racer(ec.Component):
    def __init__(self, inner, outer, speed=crowd.constants.RACE_PLAYER_SPEED, turn_speed=crowd.constants.RACE_PLAYER_TURN_SPEED):
        super(Racer, self).__init__()
        self.inner = inner
        self.outer = outer

        self.speed = speed
        self.turn_speed = turn_speed

        self.register_handler(self.update)
        self.register_handler(self.try_position)

    def update(self, component, entity, event, time_elapsed):
        owner = entity.handle('get_owner')
        position = entity.handle('get_position')
        angle = entity.handle('get_angle')

        ds = 0
        da = 0

        if owner.input.left:
            da -= 1

        if owner.input.right:
            da += 1

        if owner.input.up:
            ds -= 1

        if owner.input.down:
            ds += 1

        angle += da * self.turn_speed

        v = py2d.Math.Vector(math.cos(angle), math.sin(angle))

        entity.handle('set_angle', angle)

        newpos = position + v * self.speed * ds
        altpos = entity.handle('try_position', newpos)
        if altpos:
            newpos = altpos

        entity.handle('set_position', newpos)

    def try_position(self, component, entity, event, newpos):

        oldpos = entity.handle('get_position')

        in_outer = self.outer.contains_point(newpos)
        in_inner = self.inner.contains_point(newpos)

        if in_outer and not in_inner:
            return

        if in_outer and in_inner:
            p = py2d.Math.intersect_poly_lineseg(self.inner.points, oldpos, newpos)
            if p:
                return p[0]
        if not in_outer:
            p = py2d.Math.intersect_poly_lineseg(self.outer.points, oldpos, newpos)
            if p:
                return p[0]

class Racetrack(ec.Component):
    def __init__(self, *polys):
        super(Racetrack, self).__init__()
        self.polys = list(itertools.chain(*polys))

        self.register_handler(self.render)

    def render(self, component, entity, event):

        transform = py2d.Math.Transform.move(*(entity.challenge.camera * -1).as_tuple())

        for poly in self.polys:
            for a, b in zip(poly.points, poly.points[1:]) + [(poly.points[-1], poly.points[0])]:
                at = transform * a
                bt = transform * b

                pygame.draw.line(entity.challenge.mode.game.screen, (128, 128, 128), at.as_tuple(), bt.as_tuple())

