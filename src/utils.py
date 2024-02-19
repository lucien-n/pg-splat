from .settings import *


def apply_scroll(rect: pg.Rect, scroll: vector):
    return vector(
        rect.x - scroll.x,
        rect.y - scroll.y,
    )
