from ..tile import Tile
from .level import Level
from ..settings import *
from ..camera import Camera
from ..player import Player
from pygame.event import Event as Event


class OtherDevLevel(Level):
    def __init__(self, game) -> None:
        from ..main import Game

        self.game: Game = game

        self.camera = Camera()

        self.player = Player(self, display_width / 2, display_height / 2)
        self.camera.follow = self.player.rect

        self.tiles = [Tile(2, 2)]

    def handle_events(self, events: list[pg.Event]):
        self.player.handle_events(events)

    def update(self, dt: float):
        self.player.update(dt)

    def fixed_update(self, dt: float):
        self.player.fixed_update(dt)

    def draw(self, target: pg.Surface):
        self.camera.update(target)

        # ? draw origin
        pg.draw.line(
            target,
            pg.Color(80, 80, 86),
            vector(0, display_height - self.camera.scroll.y),
            vector(display_width, display_height - self.camera.scroll.y),
        )

        pg.draw.line(
            target,
            pg.Color(80, 80, 86),
            vector(-self.camera.scroll.x, 0),
            vector(-self.camera.scroll.x, display_height),
        )
        # ? end draw origin

        [tile.draw(target, self.camera.scroll) for tile in self.tiles]
        self.player.draw(target, self.camera.scroll)
