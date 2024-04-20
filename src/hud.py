import numpy as np
from .settings import *
import pygame.freetype as pgft
import typing


class Hud:
    pgft.init()

    def __init__(self, game) -> None:
        from .main import Game

        self.game: Game = game

        self.font = pgft.Font(r"assets/fonts/default.ttf", 12, False, False)

        self.last_update_at = 0
        self.update_interval = 1 / 10

        self.debug_lines = {}
        self.rendered_lines = []

        self.fps_list = []

    def update(self, dt: float):
        if self.game.now - self.last_update_at < self.update_interval:
            return
        self.last_update_at = self.game.now

        self.debug_lines["dt"] = {
            "value": f"{(dt * 1_000):.2f}",
            "label": "\u0394",
            "unit": "ms",
        }

        self.fps_list.append(math.floor(self.game.clock.get_fps()))
        self.fps_list = self.fps_list[-30:]

        self.debug_lines["fps"] = {
            "label": "\u2211",
            "value": math.floor(np.mean(self.fps_list)),
            "bg_color": (218, 113, 127),
        }

        self.redraw()

    def redraw(self):
        self.rendered_lines.clear()
        for rendered_line in self.debug_lines.values():
            rendered_line = self.render_font(
                f'{rendered_line["label"]} {rendered_line["value"]}{rendered_line.get("unit", "")}',
                20,
                rendered_line.get("fg_color", (255, 255, 255)),
                rendered_line.get("bg_color", (253, 187, 109)),
                5,
            )
            self.rendered_lines.append(rendered_line)

    def draw(self, surface: pg.Surface, *args):
        h = 0
        for rendered_line in self.rendered_lines:
            surface.blit(rendered_line, (0, h))
            h += rendered_line.get_height()

    def debug(
        self,
        key: str,
        value: typing.Any,
        label: str,
        bg_color: pg.Color | None = None,
        fg_color: pg.Color | None = None,
    ):
        self.debug_lines[key] = {
            "label": label,
            "value": str(value),
        }

        if bg_color:
            self.debug_lines[key]["bg_color"] = bg_color
        if fg_color:
            self.debug_lines[key]["fg_color"] = fg_color

    def render_font(
        self,
        content: str = "Placeholder",
        size: int = 20,
        color: tuple = (255, 255, 255),
        bgcolor: tuple = None,
        padding: int = 4,
    ) -> pg.Surface:
        """Render text with font

        Args:
            content (str, optional): Rendered text. Defaults to "Placeholder".
            size (int, optional): Font size. Defaults to 20.
            color (tuple, optional): Font color. Defaults to (255, 255, 255).
            bgcolor (tuple, optional): Background color. Defaults to None.
            padding (int, optional): Padding. Defaults to 4.

        Returns:
            pygame.Surface: Rendered text surface
        """
        rendered_text = self.font.render(
            str(content), color, None, pgft.STYLE_DEFAULT, 0, size
        )[0]

        padded_rendered_text = pg.Surface(
            (
                rendered_text.get_width() + padding * 2,
                rendered_text.get_height() + padding * 2,
            )
        )
        padded_rendered_text.convert_alpha()

        if bgcolor:
            padded_rendered_text.fill(bgcolor)

        padded_rendered_text.blit(rendered_text, (padding, padding))

        return padded_rendered_text
