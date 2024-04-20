import math
import time
import pygame as pg
from pygame.math import Vector2 as vector

settings = {
    "display": {"target_fps": 165, "width": 1280, "height": 720},
    "camera": {"smoothness": 180},
    "keybinds": {
        "movements": {"jump": " ", "right": "d", "left": "a"},
        "misc": {"debug": "f3"},
    },
}

display_size = display_width, display_height = 320, 180

DEV = True
DRAW_RECTS = DEV
TILE_SIZE = 16


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
