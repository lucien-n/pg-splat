from .settings import *
from .utils import apply_scroll


class Tile(pg.sprite.Sprite):
    def __init__(self, x: float, y: float) -> None:
        self.image = pg.image.load("assets/tiles/debug.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, target: surface, scroll: vector):
        target.blit(
            self.image,
            apply_scroll(
                pg.Rect(
                    self.rect.x,
                    self.rect.y,
                    self.rect.w,
                    self.rect.h,
                ),
                scroll,
            ),
        )
