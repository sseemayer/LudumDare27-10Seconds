import crowd.constants
import crowd.modes.action as am
import crowd.entity_component as ec
import crowd.resource

from crowd.modes.action.challenges.gather import CoinComponent


import math
import py2d.Math
import pygame

class JumpChallenge(am.Challenge):
    name = 'jump'

    def __init__(self, mode, input_sources):
        super(JumpChallenge, self).__init__(mode, input_sources)

        startpos = py2d.Math.Vector(0, 0)

        self.camera = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE) / -2

        self.players = [
            am.ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]


        self.platform_positions = [
            (
                py2d.Math.Vector(
                    math.sin( float(i) / crowd.constants.JUMP_PLATFORMS_PER_PHASE * math.pi) * crowd.constants.JUMP_PLATFORM_AMPLITUDE,
                    (i+1) * -crowd.constants.JUMP_PLATFORM_STEP
                ),
                crowd.constants.JUMP_PLATFORM_WIDTH
            )
            for i in range(100)
        ]


        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                ec.Movement(vertical=False, speed=crowd.constants.JUMP_PLAYER_SPEED),
                GravityJump(self.platform_positions),
                ec.Physics(decay_factor=crowd.constants.JUMP_PLAYER_SPEED_DECAY),
                ec.Owner(player),
                ec.Sprite(crowd.resource.image.cursor)
            ])

            for player in self.players
        ]

        self.platform_entities = [
            ec.Entity(self, [
                ec.Position(pos),
                Platform(width)
            ])
            for pos, width in self.platform_positions
        ]

        self.coin_entities = [
            ec.Entity(self, [
                ec.Position(pos + crowd.constants.JUMP_COIN_OFFSET),
                CoinComponent(gather_distance = crowd.constants.JUMP_GATHER_DISTANCE),
                ec.Sprite(crowd.resource.image.coin)
            ])

            for pos, width in self.platform_positions
        ]

        self.entities = self.coin_entities + self.platform_entities + self.player_entities

    def update(self, time_elapsed):
        super(JumpChallenge, self).update(time_elapsed)

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)

    def render(self):
        super(JumpChallenge, self).render()

        pygame.draw.rect(self.mode.game.screen, (32, 32, 32), ((0, -self.camera.y ), crowd.constants.SCREEN_SIZE))

        for entity in self.entities:
            entity.render()

class Platform(ec.Component):
    def __init__(self, width):
        super(Platform, self).__init__()
        self.width = width

        self.register_handler(self.render)
        self.register_handler(self.get_width)

    def get_width(self, component, entity, event):
        return self.width

    def render(self, component, entity, event):

        width = entity.handle('get_width')

        position = entity.handle('get_position')
        owner = entity.handle('get_owner')

        camera = entity.challenge.camera

        camera_pos1 = position - camera - py2d.Math.VECTOR_X * (width / 2)
        camera_pos2 = position - camera + py2d.Math.VECTOR_X * (width / 2)

        pygame.draw.line(entity.challenge.mode.game.screen, (128, 128, 128), camera_pos1.as_tuple(), camera_pos2.as_tuple())

class GravityJump(ec.Component):
    def __init__(self, platform_positions, gravity=crowd.constants.JUMP_GRAVITY, jump=crowd.constants.JUMP_STRENGTH):
        super(GravityJump, self).__init__()

        self.platform_positions = platform_positions
        self.gravity = gravity
        self.jump = jump

        self.register_handler(self.update)
        self.register_handler(self.try_position)

    def update(self, component, entity, event, time_elapsed):

        position = entity.handle('get_position')


        acceleration = entity.handle('get_acceleration')
        acceleration.y = self.gravity
        entity.handle('set_acceleration', acceleration)

        entity.challenge.camera.y = position.y - crowd.constants.SCREEN_SIZE[1] / 2

    def try_position(self, component, entity, event, newpos):
        position = entity.handle('get_position')
        velocity = entity.handle('get_velocity')
        owner = entity.handle('get_owner')

        on_platform = False
        if newpos.y > 0:
            on_platform = True
            newpos.y = 0
            velocity.y = 0

        if not on_platform:
            for pos, width in self.platform_positions:
                left = pos.x - width / 2
                right = pos.x + width / 2

                if position.y <= pos.y and newpos.y >= pos.y and position.x >= left and position.x <= right:
                    on_platform = True
                    newpos.y = pos.y
                    velocity.y = 0
                    break

        if on_platform and owner.input.up:
            velocity.y = -crowd.constants.JUMP_STRENGTH


        entity.handle('set_velocity', velocity)
