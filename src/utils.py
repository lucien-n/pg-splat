from .settings import *


def apply_scroll(rect: pg.Rect, scroll: vector, center=True):
    return vector(
        rect.x - (rect.w / 2 if center else 0) - scroll.x,
        rect.y - (rect.h / 2 if center else 0) - scroll.y,
    )
