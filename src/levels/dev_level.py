from .level import Level
from ..settings import *


class DevLevel(Level):
    def __init__(self, game) -> None:
        super().__init__(game, "dev")
        from ..main import Game

        self.game: Game = game

    def handle_events(self, events: list[pg.Event]):
        super().handle_events(events)

    def update(self, dt: float):
        super().update(dt)

    def fixed_update(self, dt: float):
        super().fixed_update(dt)

    def draw(self, target: pg.Surface):
        super().draw(target)

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
