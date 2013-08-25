import crowd.constants
from crowd.modes.action.challenge import Challenge, ChallengePlayer
import crowd.entity_component as ec
import crowd.resource

import py2d.Math
import math

class ShooterChallenge(Challenge):
    name = 'shooter'
    modal_msg = 'Shoot to kill!!'

    def __init__(self, mode, input_sources):
        super(ShooterChallenge, self).__init__(mode, input_sources)

        startpos = py2d.Math.Vector(crowd.constants.SCREEN_SIZE[0] / 2, crowd.constants.SCREEN_SIZE[1] - 100)

        self.players = [
            ChallengePlayer(self, isrc)
            for isrc in input_sources
        ]

        self.player_entities = [
            ec.Entity( self, [
                ec.Position(startpos.clone()),
                ec.Angle(math.pi / 2),
                ec.Movement(speed=crowd.constants.SHOOTER_PLAYER_SPEED, vertical=False),
                ec.Physics(decay_factor=crowd.constants.SHOOTER_PLAYER_SPEED_DECAY),
                ec.Owner(player),
                Fighter(),
                ec.Sprite(crowd.resource.image.pointer)
            ])

            for player in self.players
        ]

        screen_size = py2d.Math.Vector(*crowd.constants.SCREEN_SIZE)

        target_positions = [
            py2d.Math.Vector(
                (x -  ( -0.25 + 0.5 * ( y % 2 ))) * (screen_size.x / (crowd.constants.SHOOTER_TARGETS_X )),
                y * (300 / crowd.constants.SHOOTER_TARGETS_Y)
            )
            for x in range(1, crowd.constants.SHOOTER_TARGETS_X)
            for y in range(1, crowd.constants.SHOOTER_TARGETS_Y)
        ]

        print(target_positions)

        self.target_entities = [
            ec.Entity( self, [
                ec.Position(pos),
                ec.Sprite(crowd.resource.image.alien)
            ])
            for pos in target_positions
        ]

        self.entities = self.target_entities + self.player_entities

    def update(self, time_elapsed):
        super(ShooterChallenge, self).update(time_elapsed)

        if self.modal: return

        for player in self.players:
            player.next_frame()

        for entity in self.entities:
            entity.update(time_elapsed)

    def render(self):
        for entity in self.entities:
            entity.render()

        super(ShooterChallenge, self).render()

class Fighter(ec.Component):

    def __init__(self, fire_rate=crowd.constants.SHOOTER_PLAYER_FIRE_RATE):
        super(Fighter, self).__init__()

        self.register_handler(self.update)

        self.fire_cooldown = 0
        self.fire_rate = fire_rate

        self.total_time = 0

    def update(self, component, entity, event, time_elapsed):
        self.total_time += time_elapsed

        self.fire_cooldown = max(0, self.fire_cooldown - time_elapsed)

        owner = entity.handle('get_owner')
        position = entity.handle('get_position')
        if (owner.input.up or owner.input.a) and self.fire_cooldown == 0:
            self.fire_cooldown += self.fire_rate
            crowd.resource.sound.shoot.play()

            entity.challenge.entities.append(ec.Entity(entity.challenge, [
                ec.Position(position + py2d.Math.VECTOR_Y * -20 + py2d.Math.VECTOR_X * math.sin(self.total_time / 10.0) * crowd.constants.SHOOTER_PLAYER_BULLET_DISTANCE),
                Projectile(),
                ec.Owner(owner),
                ec.Sprite(crowd.resource.image.projectile, hide_owner = True)
            ]))



class Target(ec.Component):
    def __init__(self):
        super(Target, self).__init__()

        self.register_handler(self.update)

    def update(self, component, entity, event, time_elapsed):
        pass

class Projectile(ec.Component):
    def __init__(self, life=crowd.constants.SHOOTER_BULLET_LIFE, direction=crowd.constants.SHOOTER_PLAYER_BULLET_SPEED):
        super(Projectile, self).__init__()

        self.life = life
        self.direction = direction

        self.register_handler(self.update)

    def update(self, component, entity, event, time_elapsed):
        position = entity.handle('get_position')
        owner = entity.handle('get_owner')

        self.life -= time_elapsed

        if self.life <= 0:
            entity.challenge.entities.remove(entity)


        position += self.direction

        if owner.input_source.is_live:

            for target in entity.challenge.target_entities:
                dist = (target.handle('get_position') - position).length
                if dist < crowd.constants.SHOOTER_BULLET_DIST:
                    crowd.resource.sound.explosion.play()

                    entity.challenge.target_entities.remove(target)
                    entity.challenge.entities.remove(target)
                    entity.challenge.entities.remove(entity)

                    entity.challenge.mode.game.score += crowd.constants.SHOOTER_TARGET_SCORE



        entity.handle('set_position', position)
