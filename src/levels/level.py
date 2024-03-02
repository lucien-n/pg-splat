from PIL import Image
from ..tile import Tile
from ..settings import *


class Level:
    def __init__(self, game, name: str) -> None:
        from ..main import Game

        self.game: Game = game
        self.name = name

        self.tiles: list[Tile] = []
        self.spawn_point = vector(0, 0)
        self.load(f"assets/levels/{self.name}.png")

    def load(self, path: str):
        img = Image.open(path)
        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                if pixel == 0:
                    self.tiles.append(Tile(x, y))
                if pixel == 3:
                    self.spawn_point = vector(x * 32, y * 32)

    def handle_events(self, events: list[pg.Event]):
        pass

    def update(self, dt: float):
        pass

    def fixed_update(self, dt: float):
        pass

    def draw(self, target: pg.Surface):
        pass
