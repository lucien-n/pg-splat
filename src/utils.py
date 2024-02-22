from .settings import *


def apply_scroll(
    rect: pg.Rect, scroll: vector, expects: str = "vector"
) -> vector | pg.Rect:
    scrolled = vector(rect.x - scroll.x, rect.y - scroll.y)

    if expects == "rect":
        return pg.Rect(scrolled.x, scrolled.y, rect.w, rect.h)

    return scrolled
