import pygame.locals as pgl
import py2d.Math

GAME_NAME = 'Crowd'
SCREEN_SIZE = (640, 480)
TARGET_FPS = 30

MODAL_PADDING = 20

NOMODE_BACKGROUND = (0, 0, 128)

URL_BASE = 'http://localhost:5000/'
URL_REPLAYS_GET  = URL_BASE + 'replays/{challenge}'
URL_REPLAYS_POST = URL_BASE + 'replays'


VALID_ACTIONS = ['up', 'right', 'down', 'left', 'a', 'b']
KEY_MAPPING = {
    pgl.K_UP: 'up',
    pgl.K_RIGHT: 'right',
    pgl.K_DOWN: 'down',
    pgl.K_LEFT: 'left',

    pgl.K_x: 'a',
    pgl.K_c: 'b',

    pgl.K_j: 'a',   # Dvorak support
    pgl.K_k: 'b'    # Dvorak support
}


RES_IMAGES = {
    'cursor': 'data/images/cursor.png',
    'pointer': 'data/images/pointer.png',
    'coin': 'data/images/coin.png'

}


RES_MUSIC = {

}

RES_SOUNDS = {

}

RES_FONTS = {
    'default': ('data/fonts/Audiowide-Regular.ttf', 12),
    'big_gui': ('data/fonts/PressStart2P-Regular.ttf', 72),
    'med_gui': ('data/fonts/PressStart2P-Regular.ttf', 36)
}


GATHER_PLAYER_SPEED = 0.0002
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
RACE_PLAYER_SPEED = 10
RACE_PLAYER_TURN_SPEED = 0.1

CAVE_SCALING = 2
CAVE_SPEED = 0.5
CAVE_BOOST_SPEED = 0.008
CAVE_GRAVITY = 0.008
