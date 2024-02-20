from .settings import *
from .utils import apply_scroll


class Tile(pg.sprite.Sprite):
    def __init__(self, x: float, y: float) -> None:
        self.pos = vector(x, y)

        self.image = pg.image.load("assets/tiles/debug.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * self.rect.w
        self.rect.y = y * self.rect.h

    def draw(self, target: surface, scroll: vector):
        target.blit(self.image, apply_scroll(self.rect, scroll))
