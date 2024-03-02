from typing import Any
from .settings import *


class Sprite(pg.sprite.Sprite):
    def __init__(
        self,
        position: vector,
        surface: pg.Surface = pg.Surface((TILE_SIZE, TILE_SIZE)),
        *groups,
    ) -> None:
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.old_rect = self.rect.copy()
