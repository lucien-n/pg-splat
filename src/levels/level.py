from ..tile import Tile
from ..settings import *
from ..player import Player
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, game, name: str) -> None:
        from ..main import Game

        self.game: Game = game
        self.name = name

        self.tiles = []
        self.player: Player | None = None
        self.load()

    def load(self):
        map = load_pygame(f"assets/levels/{self.name}.tmx")
        for x, y, surf in map.get_layer_by_name("walls").tiles():
            self.tiles.append(Tile(x, y, surf))

        for obj in map.get_layer_by_name("objects"):
            if obj.name == "player":
                self.player = Player(self, obj.x, obj.y)

    def handle_events(self, events: list[pg.Event]):
        pass

    def update(self, dt: float):
        pass

    def fixed_update(self, dt: float):
        pass

    def draw(self, target: pg.Surface):
        pass
