from ..settings import *
from ..sprite import Sprite
from ..utils import apply_scroll


class Collectible(Sprite):
    def __init__(self, x: float, y: float, surf: pg.Surface, value: int = 10) -> None:
        super().__init__(vector(x, y), surf)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.rect.w
        self.rect.y = y * self.rect.h

        self.value = value

    def draw(self, target: pg.Surface, scroll: vector):
        dest = apply_scroll(self.rect, scroll)
        dest.y += math.sin(time.time() * 5) * 1.2
        target.blit(self.image, dest)
