from .settings import *


class Camera:
    def __init__(self, smoothness: int = 12) -> None:
        self.smoothness = smoothness
        self.scroll = vector(0, 0)
        self.follow: pg.Rect = None

    def update(self, target: pg.Surface):
        if self.follow.x - self.scroll.x != target.get_width() / 2:
            self.scroll.x += (
                self.follow.x - (self.scroll.x + target.get_width() / 2)
            ) / self.smoothness
        if self.follow.y - self.follow.y != target.get_height() / 2:
            self.scroll.y += (
                self.follow.y - (self.scroll.y + target.get_height() / 2)
            ) / self.smoothness
