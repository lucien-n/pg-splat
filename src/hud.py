import numpy as np
from .settings import *
import pygame.freetype as pgft
import random


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

        self.debug(
            "dt",
            f"{(dt * 1_000):.2f}",
            "\u0394",
            unit="ms",
        )

        self.fps_list.append(math.floor(self.game.clock.get_fps()))
        self.fps_list = self.fps_list[-30:]

        self.debug(
            "fps",
            math.floor(np.mean(self.fps_list)),
            "\u2211",
            (218, 113, 127),
        )

        self.debug_separator()
        # draw movement keybinds
        self.debug("bindc_movements", "MOVEMENTS")
        for bind in settings["keybinds"]["movements"]:
            key = settings["keybinds"]["movements"][bind]
            self.debug(
                f"bind_{bind}",
                f"{bind.upper()}: {"SPACE" if key == " " else key.upper()}",
            )

        self.debug_separator()
        # draw misc keybinds
        self.debug("bindc_misc", "MISC", bg_color=(83, 191, 92))
        for bind in settings["keybinds"]["misc"]:
            key = settings["keybinds"]["misc"][bind]
            self.debug(
                f"bind_{bind}",
                f"{bind.upper()}: {"SPACE" if key == " " else str(key).upper()}",
                bg_color=(83, 191, 92),
            )

        self.redraw()

    def redraw(self):
        self.rendered_lines.clear()

        for debug_line in self.debug_lines.values():
            if debug_line is None:
                rendered_line = None
            else:
                value = debug_line.get("value")
                label = debug_line.get("label")
                unit = debug_line.get("unit")
                fg_color = debug_line.get("fg_color", (255, 255, 255))
                bg_color = debug_line.get("bg_color", (253, 187, 109))

                rendered_line = self.render_font(
                    f'{label + " " if label else ""}{value}{unit if unit else ""}',
                    20,
                    fg_color,
                    bg_color,
                    5,
                )
            self.rendered_lines.append(rendered_line)

    def draw(self, surface: pg.Surface, *args):
        h = 0
        for rendered_line in self.rendered_lines:
            if rendered_line is None:
                h += 20
            else:
                surface.blit(rendered_line, (0, h))
                h += rendered_line.get_height()

    def debug(
        self,
        key: str,
        value: str | int | float | object,
        label: str | None = None,
        bg_color: pg.Color | None = None,
        fg_color: pg.Color | None = None,
        unit: str | None = None,
    ):
        self.debug_lines[key] = {
            "value": str(value),
        }

        if label:
            self.debug_lines[key]["label"] = label
        if unit:
            self.debug_lines[key]["unit"] = unit
        if bg_color:
            self.debug_lines[key]["bg_color"] = bg_color
        if fg_color:
            self.debug_lines[key]["fg_color"] = fg_color

    def debug_separator(self):
        self.debug_lines[f"sep_{random.randint(100, 999)}"] = None

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
