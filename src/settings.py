import math
import time
import pygame as pg
from pygame.math import Vector2 as vector
from pygame.surface import Surface as surface

settings = {
    "camera": {"smoothness": 36, "zoom": 0.5},
    "keybinds": {"movements": {"jump": " ", "right": "d", "left": "a"}},
}

window_size = window_width, window_height = 1280, 720
display_size = display_width, display_height = 320, 180

DEV = True


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
