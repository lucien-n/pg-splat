from ..settings import *
from ..player import Player
from ..camera import Camera
from ..tiles import Wall, Collectible
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self, game, name: str) -> None:
        from ..main import Game

        self.game: Game = game
        self.name = name

        self.walls = []
        self.collectibles = []
        self.player: Player | None = None
        self.load()

        self.camera = Camera()
        self.camera.follow = self.player.rect

    def load(self):
        map = load_pygame(f"assets/levels/{self.name}.tmx")
        for x, y, surf in map.get_layer_by_name("walls").tiles():
            self.walls.append(Wall(x, y, surf))

        for obj in map.get_layer_by_name("collectibles"):
            print(obj, obj.x, obj.y, obj.image, obj.properties)
            self.collectibles.append(
                Collectible(
                    obj.x,
                    obj.y,
                    obj.image or pg.Surface((16, 16)),
                    obj.properties.get("value", 1),
                )
            )

        for obj in map.get_layer_by_name("objects"):
            print(obj)
            if obj.name == "player":
                self.player = Player(self, obj.x, obj.y)

    def handle_events(self, events: list[pg.Event]):
        self.player.handle_events(events)

    def update(self, dt: float):
        self.player.update(dt, self.walls, self.collectibles)

    def fixed_update(self, dt: float):
        self.player.fixed_update(dt)

    def draw(self, target: pg.Surface):
        self.camera.update(target, self.game.dt)

        [tile.draw(target, self.camera.scroll) for tile in self.walls]
        [
            collectible.draw(target, self.camera.scroll)
            for collectible in self.collectibles
        ]
        self.player.draw(target, self.camera.scroll)
