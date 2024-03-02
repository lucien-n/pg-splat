from .tile import Tile
from .settings import *
from .sprite import Sprite
from .utils import apply_scroll


class Player(Sprite):
    def __init__(self, level, x: float, y: float) -> None:
        super().__init__((x, y))
        from .levels.level import Level

        self.level: Level = level

        self.speed = 140
        self.jump_force = 320
        self.gravity = 1200

        self.velocity = vector(0, 0)
        self.max_velocity = 5000
        self.jump = False
        self.jump_counter = 0
        self.max_jumps = 9999 if DEV else 2
        self.jump_cooldown = 1 / 5  # ? cooldown or on spacebar repress
        self.last_jump_at = 0
        self.is_grounded = False

        self.sprites = {
            "idle": pg.image.load("assets/player/idle.png").convert_alpha(),
            "run": pg.image.load("assets/player/run.png").convert_alpha(),
            "jump": pg.image.load("assets/player/jump.png").convert_alpha(),
            "double_jump": pg.image.load(
                "assets/player/double_jump.png"
            ).convert_alpha(),
            "fall": pg.image.load("assets/player/fall.png").convert_alpha(),
        }
        self.animation_sprite = self.sprites["idle"]
        self.image = pg.Surface((32, 32))
        self.image.set_colorkey(Color.BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.draw_outline = False
        self.flipped = False

        self.last_frame_at = 0
        self.frame_interval = 1 / 20
        self.current_frame = 0

        self.movement_binds = settings["keybinds"]["movements"]

        self.hit_rect = self.rect.inflate(-12, -8)

    def handle_events(self, events: list[pg.Event]):
        keys = pg.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[ord(self.movement_binds["left"])]:
            input_vector.x -= 1
            self.flipped = True

        if keys[ord(self.movement_binds["right"])]:
            input_vector.x += 1
            self.flipped = False

        if keys[ord(self.movement_binds["jump"])]:
            self.jump = True

        self.velocity.x = input_vector.normalize().x if input_vector else input_vector.x

    def land(self):
        self.jump_counter = 0
        self.is_grounded = True
        if not self.jump:
            self.velocity.y = 0

    def collide(self, tiles: list[Tile]):
        for tile in tiles:
            if (
                self.hit_rect.bottom < tile.rect.top
                or self.hit_rect.top > tile.rect.bottom
                or self.hit_rect.left > tile.rect.right
                or self.hit_rect.right < tile.rect.left
            ):
                continue

            # bottom
            if (
                self.hit_rect.bottom >= tile.rect.top
                and self.old_rect.bottom < tile.old_rect.top
            ):
                self.hit_rect.bottom = tile.rect.top - 0.1
                self.land()
            # top
            elif (
                self.hit_rect.top <= tile.rect.bottom
                and self.old_rect.top > tile.old_rect.bottom
            ):
                self.hit_rect.top = tile.rect.bottom + 0.1
            # right
            elif (
                self.hit_rect.right >= tile.rect.left
                and self.old_rect.right < tile.old_rect.left
            ):
                self.hit_rect.right = tile.rect.left - 0.1
            # left
            elif (
                self.hit_rect.left <= tile.rect.right
                and self.old_rect.left > tile.old_rect.right
            ):
                self.hit_rect.left = tile.rect.right + 0.1

    def move(self, dt: float):
        # horizontal
        self.hit_rect.x += self.velocity.x * self.speed * dt
        self.velocity.x = pg.math.clamp(
            self.velocity.x, -self.max_velocity, self.max_velocity
        )

        # vertical
        self.velocity.y += self.gravity / 2 * dt
        self.hit_rect.y += self.velocity.y * dt
        self.velocity.y += self.gravity / 2 * dt
        self.velocity.y = pg.math.clamp(
            self.velocity.y, -self.max_velocity, self.max_velocity
        )

        if self.jump:
            if (
                self.level.game.now - self.last_jump_at > self.jump_cooldown
                and self.jump_counter < self.max_jumps
            ):
                self.is_grounded = False
                self.jump_counter += 1

                self.velocity.y = -self.jump_force
                self.last_jump_at = self.level.game.now
            self.jump = False

    def update(self, dt: float = 0, tiles: list[Tile] = []):
        self.old_rect = self.hit_rect.copy()

        self.move(dt)
        self.collide(tiles)

        self.hit_rect.y = int(self.hit_rect.y)
        self.rect.topleft = (
            self.hit_rect.x - 6,
            self.hit_rect.y - 8,
        )  # adjust based on rect inflation

    def fixed_update(self, dt: float = 0, tiles=[]):
        # debug pos
        self.level.game.hud.debug_lines["pos"] = {
            "label": "\u0040",
            "value": f"{self.rect.x:.1f} {self.rect.y:.1f} | {self.hit_rect.x:.1f} {self.hit_rect.y:.1f} ",
            "bg_color": (69, 92, 123),
        }

        self.level.game.hud.debug_lines["direction"] = {
            "label": "V",
            "value": f"{self.velocity.x:.1f} {self.velocity.y:.1f}",
            "bg_color": (80, 150, 150),
        }

        self.level.game.hud.debug_lines["player_debug"] = {
            "label": "P",
            "value": f"{self.is_grounded} {self.jump} {self.jump_counter}",
            "bg_color": (180, 124, 170),
        }

    def animate(self):
        is_running = self.velocity.x != 0
        is_falling = not self.is_grounded and self.velocity.y > 0
        is_ascending = not self.is_grounded and self.velocity.y < 0

        if is_running:
            self.animation_sprite = self.sprites["run"]
        else:
            self.animation_sprite = self.sprites["idle"]

        if is_falling:
            self.animation_sprite = self.sprites["fall"]
        elif is_ascending:
            if self.jump_counter > 1:
                self.animation_sprite = self.sprites["double_jump"]
            else:
                self.animation_sprite = self.sprites["jump"]

        if self.level.game.now - self.last_frame_at > self.frame_interval:
            self.current_frame += 1
            self.last_frame_at = self.level.game.now

        if self.current_frame + 1 > self.animation_sprite.get_width() / self.rect.w:
            self.current_frame = 0

        self.image = self.animation_sprite.subsurface(
            pg.Rect(self.current_frame * self.rect.w, 0, self.rect.w, self.rect.h)
        )
        self.image = (
            pg.transform.flip(self.image, True, False) if self.flipped else self.image
        )
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, target: pg.Surface, scroll: vector):
        self.animate()

        target.blit(self.image, (display_width - self.rect.w, 0))
        target.blit(self.image, apply_scroll(self.rect, scroll))

        if self.draw_outline:
            pg.draw.lines(
                target,
                Color.WHITE,
                False,
                [
                    (x + self.rect.x - scroll.x, y + self.rect.y - scroll.y)
                    for x, y in self.mask.outline(every=1)
                ],
            )

        if DRAW_RECTS:
            pg.draw.rect(
                target, Color.GREEN, apply_scroll(self.hit_rect, scroll, "rect"), 1
            )
