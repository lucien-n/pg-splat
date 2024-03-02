from .settings import *
from .sprite import Sprite
from .utils import apply_scroll


class Tile(Sprite):
    def __init__(self, x: float, y: float, surf: pg.Surface) -> None:
        super().__init__(vector(x, y), surf)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.rect.w
        self.rect.y = y * self.rect.h
        self.old_rect = self.rect.copy()

    def update(self):
        self.old_rect = self.rect.copy()

    def draw(self, target: pg.Surface, scroll: vector):
        target.blit(self.image, apply_scroll(self.rect, scroll))
