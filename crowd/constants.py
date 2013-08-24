import pygame.locals as pgl

GAME_NAME = 'Crowd'
SCREEN_SIZE = (640, 480)
TARGET_FPS = 30

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
    pgl.K_c: 'b'
}


RES_IMAGES = {
    'cursor': 'data/images/cursor.png'

}


RES_MUSIC = {

}

RES_SOUNDS = {

}

RES_FONTS = {
    'default': ('data/fonts/Audiowide-Regular.ttf', 12),
    'big_gui': ('data/fonts/PressStart2P-Regular.ttf', 48)
}


GATHER_PLAYER_SPEED = 0.0001
