from ..settings import *


class Level:
    def __init__(self, game) -> None:
        from ..main import Game

        self.game: Game = game

    def handle_events(self, events: list[pg.Event]):
        pass

    def update(self, dt: float):
        pass

    def fixed_update(self, dt: float):
        pass

    def draw(self, target: surface):
        pass
