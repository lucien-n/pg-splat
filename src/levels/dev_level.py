from ..tile import Tile
from .level import Level
from ..settings import *
from ..camera import Camera
from ..player import Player


class DevLevel(Level):
    def __init__(self, game) -> None:
        super().__init__(game, "dev")
        from ..main import Game

        self.game: Game = game

        self.camera = Camera()

        self.player = Player(self, self.spawn_point.x, self.spawn_point.y)
        self.camera.follow = self.player.rect

        
    def handle_events(self, events: list[pg.Event]):
        self.player.handle_events(events)

    def update(self, dt: float):
        self.player.update(dt, self.tiles)

    def fixed_update(self, dt: float):
        self.player.fixed_update(dt)

    def draw(self, target: pg.Surface):
        self.camera.update(target, self.game.dt)

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
