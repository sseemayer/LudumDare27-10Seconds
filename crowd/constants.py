import pygame.locals as pgl
import py2d.Math

GAME_NAME = 'Crowd'
SCREEN_SIZE = (640, 480)
TARGET_FPS = 30

MODAL_PADDING = 20

NOMODE_BACKGROUND = (0, 0, 128)

URL_BASE = 'http://localhost:5000/'
URL_HIGHSCORES   = URL_BASE + 'highscores'
URL_REPLAYS_GET  = URL_BASE + 'replays/{challenge}'
URL_REPLAYS_POST = URL_BASE + 'replays'


VALID_ACTIONS = ['up', 'right', 'down', 'left', 'a', 'b']
KEY_MAPPING = {
    pgl.K_UP: 'up',
    pgl.K_RIGHT: 'right',
    pgl.K_DOWN: 'down',
    pgl.K_LEFT: 'left',

    pgl.K_w: 'up',
    pgl.K_d: 'right',
    pgl.K_s: 'down',
    pgl.K_a: 'left',

    pgl.K_x: 'a',
    pgl.K_c: 'b',

    pgl.K_j: 'a',   # Dvorak support
    pgl.K_k: 'b',   # Dvorak support

    pgl.K_RETURN: 'a',
    pgl.K_SPACE: 'a'
}


RES_IMAGES = {
    'logo': 'data/images/logo.png',

    'cursor': 'data/images/cursor.png',
    'pointer': 'data/images/pointer.png',
    'coin': 'data/images/coin.png',

    'rainbow': 'data/images/rainbow.png',

    'alien': 'data/images/alien.png',
    'projectile': 'data/images/projectile.png'
}


RES_MUSIC = {
    'main': 'data/audio/music.ogg'
}

RES_SOUNDS = {
    'coin': ('data/audio/coin.wav', 0.2),
    'explosion': ('data/audio/explosion.wav', 0.7),
    'jump': ('data/audio/jump.wav', 0.2),
    'select': ('data/audio/select.wav', 0.6),
    'shoot': ('data/audio/shoot.wav', 0.6),
}

RES_FONTS = {
    'default': ('data/fonts/Audiowide-Regular.ttf', 12),
    'big_gui': ('data/fonts/PressStart2P-Regular.ttf', 72),
    'med_gui': ('data/fonts/PressStart2P-Regular.ttf', 36),
    'menu': ('data/fonts/ProggySmall.ttf', 48)
}


GATHER_PLAYER_SPEED = 0.001
GATHER_PLAYER_SPEED_DECAY = 0.8
GATHER_DISTANCE = 16
GATHER_SCORE = 10
GATHER_COINS_X = 20
GATHER_COINS_Y = 15

JUMP_COIN_OFFSET = py2d.Math.Vector(0, -20)
JUMP_GRAVITY = 0.003
JUMP_STRENGTH = 2
JUMP_PLAYER_SPEED = 0.01
JUMP_PLAYER_SPEED_DECAY = 0.6
JUMP_GATHER_DISTANCE = 32

JUMP_PLATFORMS_PER_PHASE = 10

JUMP_PLATFORM_AMPLITUDE = 300
JUMP_PLATFORM_STEP = 30
JUMP_PLATFORM_WIDTH = 60


RACE_TRACK_SCALING = 6
RACE_TRACK_WIDTH = 200
RACE_PLAYER_SPEED = 20
RACE_PLAYER_TURN_SPEED = 0.2

CAVE_SCALING = 2
CAVE_SPEED = 0.5
CAVE_BOOST_SPEED = 0.008
CAVE_GRAVITY = 0.008

SHOOTER_PLAYER_SPEED = 0.005
SHOOTER_PLAYER_SPEED_DECAY = 0.7
SHOOTER_PLAYER_BULLET_DISTANCE = 5
SHOOTER_PLAYER_FIRE_RATE=200
SHOOTER_BULLET_LIFE=1000
SHOOTER_PLAYER_BULLET_SPEED=py2d.Math.Vector(0, -20)
SHOOTER_BULLET_DIST=10
SHOOTER_TARGET_SCORE=10

SHOOTER_TARGETS_X = 20
SHOOTER_TARGETS_Y = 8
