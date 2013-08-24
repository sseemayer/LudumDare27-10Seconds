import pygame.locals as pgl

GAME_NAME = 'Crowd'
SCREEN_DIMENSIONS = (640, 480)
TARGET_FPS = 30

NOMODE_BACKGROUND = (0, 0, 128)

VALID_ACTIONS = ['up', 'right', 'down', 'left', 'a', 'b']
KEY_MAPPING = {
    pgl.K_UP: 'up',
    pgl.K_RIGHT: 'right',
    pgl.K_DOWN: 'down',
    pgl.K_LEFT: 'left',

    pgl.K_x: 'a',
    pgl.K_c: 'b'
}
