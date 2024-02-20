from .settings import *
from .utils import apply_scroll


class Player(pg.sprite.Sprite):
    def __init__(self, level, x: float, y: float) -> None:
        super().__init__()
        from .levels.level import Level

        self.level: Level = level

        self.rect = pg.FRect(0, 0, 32, 32)
        self.rect.topleft = (x, y)
        self.old_rect = self.rect.copy()

        self.speed = 140
        self.jump_force = 320
        self.gravity = 1200

        self.direction = vector(0, 0)
        self.is_grounded = False
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

        self.show_masks = False

    def handle_events(self, events: list[pg.Event]):
        keys = pg.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[ord(self.movement_binds["left"])]:
            input_vector.x -= 1
        if keys[ord(self.movement_binds["right"])]:
            input_vector.x += 1

        self.direction = input_vector.normalize() if input_vector else input_vector

    def collide(self, axis, colliders: list[pg.Rect]):
        for collider in colliders:
            if collider.colliderect(self.rect):
                if axis == "horizontal":
                    # left
                    if (
                        self.rect.left <= collider.right
                        and self.old_rect.left >= collider.right
                    ):  # todo: old collider rect
                        self.rect.left = collider.right

                    # right
                    if (
                        self.rect.right >= collider.left
                        and self.old_rect.right <= collider.left
                    ):  # todo: old collider rect
                        self.rect.right = collider.left
                else:
                    pass

    def move(self, dt: float, colliders: list[pg.Rect]):
        self.rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal", colliders)

        self.rect.y += self.direction.y * self.speed * dt
        self.collide("vertical", colliders)

    def update(self, dt: float = 0, colliders: list[pg.Rect] = []):
        self.old_rect = self.rect.copy()
        self.move(dt, colliders)

    def fixed_update(self, dt: float = 0):

        # debug pos
        self.level.game.hud.debug_lines["pos"] = {
            "label": "\u0040",
            "value": f"{self.rect.x:.1f} {self.rect.y:.1f}",
            "bg_color": (69, 92, 123),
        }

    def animate(self):
        self.flipped = self.direction.x < 0
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

    def draw(self, target: surface, scroll: vector):
        self.animate()

        target.blit(self.image, (display_width - self.rect.w, 0))

        if self.show_masks:
            target.blit(
                self.mask.to_surface(
                    unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)
                ),
                apply_scroll(self.rect, scroll),
            )
        else:
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
