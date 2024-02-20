from .settings import *


class Camera:
    def __init__(self) -> None:
        self.smoothness = settings["camera"]["smoothness"]
        self.scroll = vector(0, 0)
        self.follow: pg.Rect = None

    def update(self, target: surface):
        if (
            self.follow.x - (self.follow.w / 2) - self.scroll.x
            != target.get_width() / 2
        ):
            self.scroll.x += (
                self.follow.x
                + (self.follow.w / 2)
                - (self.scroll.x + target.get_width() / 2)
            ) / self.smoothness
        if (
            self.follow.y - (self.follow.h / 2) - self.follow.y
            != target.get_height() / 2
        ):
            self.scroll.y += (
                self.follow.y
                + (self.follow.h / 2)
                - (self.scroll.y + target.get_height() / 2)
            ) / self.smoothness
