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

        self.direction = vector(0, 0)
        self.jump = False
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

        self.direction.x = (
            input_vector.normalize().x if input_vector else input_vector.x
        )

    def collide(self, axis, tiles: list[Tile]):
        for tile in tiles:
            if tile.rect.colliderect(self.hit_rect):
                if axis == "horizontal":
                    # left
                    if self.hit_rect.left <= tile.rect.right and int(
                        self.old_rect.left
                    ) >= int(tile.old_rect.right):
                        self.hit_rect.left = tile.rect.right

                    # right
                    if self.hit_rect.right >= tile.rect.left and int(
                        self.old_rect.right
                    ) <= int(tile.old_rect.left):
                        self.hit_rect.right = tile.rect.left
                else:
                    # top
                    if self.hit_rect.top <= tile.rect.bottom and int(
                        self.old_rect.top
                    ) >= int(tile.old_rect.bottom):
                        self.hit_rect.top = tile.rect.bottom

                    # bottom
                    if self.hit_rect.bottom >= tile.rect.top and int(
                        self.old_rect.bottom
                    ) <= int(tile.old_rect.top):
                        self.hit_rect.bottom = tile.rect.top

                    self.direction.y = 0
                    self.jump_counter = 0

    def move(self, dt: float, tiles: list[Tile]):
        # horizontal
        self.hit_rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal", tiles)

        # vertical
        self.direction.y += self.gravity / 2 * dt
        self.hit_rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt

        if self.jump:
            if (
                self.level.game.now - self.last_jump_at > self.jump_cooldown
                and self.jump_counter < self.max_jumps
            ):
                self.jump_counter += 1

                self.direction.y = -self.jump_force
                self.last_jump_at = self.level.game.now
            self.jump = False

        self.collide("vertical", tiles)

    def update(self, dt: float = 0, tiles: list[Tile] = []):
        self.old_rect = self.hit_rect.copy()
        self.move(dt, tiles)

        self.rect.topleft = (
            self.hit_rect.x - 6,
            self.hit_rect.y - 8,
        )  # adjust based on rect inflation

    def fixed_update(self, dt: float = 0):
        # debug pos
        self.level.game.hud.debug_lines["pos"] = {
            "label": "\u0040",
            "value": f"{self.rect.x:.1f} {self.rect.y:.1f}",
            "bg_color": (69, 92, 123),
        }

    def animate(self):
        is_running = self.direction.x != 0
        is_falling = self.direction.y > 0
        is_ascending = self.direction.y < 0

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

        scrolled = apply_scroll(self.hit_rect, scroll, "rect")
        print(scrolled)
        if DRAW_RECTS:
            pg.draw.rect(target, Color.GREEN, scrolled, 1)
