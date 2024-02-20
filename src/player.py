from .settings import *
from .utils import apply_scroll


class Player(pg.sprite.Sprite):
    def __init__(self, level, x: float, y: float) -> None:
        super().__init__()
        from .levels.level import Level

        self.level: Level = level

        self.rect = pg.FRect(0, 0, 32, 32)
        self.rect.x = x
        self.rect.y = y

        self.speed = 140
        self.jump_force = 320
        self.gravity = 1200

        self.velocity = vector(0, 0)
        self.is_grounded = False
        self.is_running = False
        self.jump_counter = 0
        self.max_jumps = 9999 if DEV else 2
        self.jump_cooldown = 1 / 5  # ? cooldown or on spacebar repress
        self.last_jump_at = 0

        self.sprites = {
            "idle": pg.image.load("assets/player/idle.png").convert_alpha(),
            "run": pg.image.load("assets/player/run.png").convert_alpha(),
            "jump": pg.image.load("assets/player/jump.png").convert_alpha(),
            "double_jump": pg.image.load(
                "assets/player/double_jump.png"
            ).convert_alpha(),
            "fall": pg.image.load("assets/player/fall.png").convert_alpha(),
        }
        self.sprite = self.sprites["idle"]
        self.last_frame_at = 0
        self.frame_interval = 1 / 20
        self.current_frame = 0
        self.flipped = False

        self.keys = set()
        self.movement_binds = settings["keybinds"]["movements"]

    def handle_events(self, events: list[pg.Event]):
        for e in events:
            if e.type == pg.KEYDOWN:
                self.keys.add(e.key)
            elif e.type == pg.KEYUP:
                self.keys.remove(e.key)

    def update(self, dt: float = 0):
        if ord(self.movement_binds["left"]) in self.keys:
            self.velocity.x = -self.speed
            self.flipped = True
        elif ord(self.movement_binds["right"]) in self.keys:
            self.velocity.x = self.speed
            self.flipped = False
        else:
            self.velocity.x = 0

        if ord(self.movement_binds["jump"]) in self.keys:
            if self.is_grounded or (
                self.jump_counter < self.max_jumps
                and self.level.game.now - self.last_jump_at > self.jump_cooldown
            ):
                self.is_grounded = False
                self.jump_counter += 1
                self.last_jump_at = self.level.game.now
                self.velocity.y = -self.jump_force

        new_pos = vector(
            self.rect.x + self.velocity.x * dt, self.rect.y + self.velocity.y * dt
        )

        if not self.is_grounded:
            self.velocity.y += self.gravity * dt

        if new_pos.y > self.level.game.height - self.rect.h:
            self.is_grounded = True
            self.jump_counter = 0
            self.velocity.y = 0
            new_pos.y = self.level.game.height - self.rect.h

        self.is_running = self.velocity.x != 0

        self.rect.x = new_pos.x
        self.rect.y = new_pos.y

    def fixed_update(self, dt: float = 0):
        if self.velocity.x != 0:
            self.sprite = self.sprites["run"]
        else:
            self.sprite = self.sprites["idle"]

        if self.velocity.y > 0:
            self.sprite = self.sprites["fall"]
        elif self.velocity.y < 0:
            if self.jump_counter > 1:
                self.sprite = self.sprites["double_jump"]
            else:
                self.sprite = self.sprites["jump"]

        self.level.game.hud.debug_lines["pos"] = {
            "label": "\u0040",
            "value": f"{self.rect.x:.1f} {self.rect.y:.1f}",
            "bg_color": (69, 92, 123),
        }

    def draw(self, target: surface, scroll: vector):
        if self.level.game.now - self.last_frame_at > self.frame_interval:
            self.current_frame += 1
            self.last_frame_at = self.level.game.now

        if self.current_frame + 1 > self.sprite.get_width() / self.rect.w:
            self.current_frame = 0

        target.blit(
            (
                pg.transform.flip(self.sprite, True, False)
                if self.flipped
                else self.sprite
            ),
            apply_scroll(self.rect, scroll),
            pg.Rect(self.current_frame * self.rect.w, 0, self.rect.w, self.rect.h),
        )
