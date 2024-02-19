import math
import time
import pygame as pg
from pygame.math import Vector2 as vector
from pygame.surface import Surface as surface

settings = {
    "camera": {"smoothness": 36, "zoom": 0.5},
    "keybinds": {"movements": {"jump": " ", "right": "d", "left": "a"}},
}

DEV = True
