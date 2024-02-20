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
        self.animation_sprite = self.sprites["idle"]
        self.image = pg.Surface((32, 32))
        self.image.fill(Color.BLACK)
        self.image.set_colorkey(Color.BLACK)

        self.last_frame_at = 0
        self.frame_interval = 1 / 20
        self.current_frame = 0
        self.flipped = False

        self.keys = set()
        self.movement_binds = settings["keybinds"]["movements"]

        self.show_masks = False

    def handle_events(self, events: list[pg.Event]):
        for e in events:
            if e.type == pg.KEYDOWN:
                self.keys.add(e.key)
                if e.key == ord("m"):
                    self.show_masks = not self.show_masks
            elif e.type == pg.KEYUP:
                self.keys.remove(e.key)

    def collide(self, new_pos: vector, colliders: list[pg.Rect]):
        mask = pg.mask.from_surface(self.image)

        for collider in colliders:
            collider_surface = pg.Surface(collider.size)
            collider_surface.fill(Color.WHITE)
            collider_mask = pg.mask.from_surface(collider_surface)

            overlap_mask = mask.overlap(
                collider_mask,
                (
                    collider.x - new_pos.x,
                    collider.y - new_pos.y,
                ),
            )

            if overlap_mask:
                collided_pos = new_pos

                print(overlap_mask)

                return collided_pos

        return new_pos

    def update(self, dt: float = 0, rects: list[pg.Rect] = []):
        new_pos = vector(
            self.rect.x + self.velocity.x * dt, self.rect.y + self.velocity.y * dt
        )

        if not self.is_grounded:
            self.velocity.y += self.gravity * dt

        if new_pos.y > display_height - self.rect.h:
            self.is_grounded = True
            self.jump_counter = 0
            self.velocity.y = 0
            new_pos.y = display_height - self.rect.h

        self.is_running = self.velocity.x != 0

        new_pos = self.collide(new_pos, rects)

        self.rect.y = new_pos.y
        self.rect.x = new_pos.x

    def fixed_update(self, dt: float = 0):
        # apply velocity based on inputs
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

        # animation
        if self.velocity.x != 0:
            self.animation_sprite = self.sprites["run"]
        else:
            self.animation_sprite = self.sprites["idle"]

        if self.velocity.y > 0:
            self.animation_sprite = self.sprites["fall"]
        elif self.velocity.y < 0:
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

        # debug pos
        self.level.game.hud.debug_lines["pos"] = {
            "label": "\u0040",
            "value": f"{self.rect.x:.1f} {self.rect.y:.1f}",
            "bg_color": (69, 92, 123),
        }

    def draw(self, target: surface, scroll: vector):
        target.blit(self.image, (display_width - self.rect.w, 0))

        if self.show_masks:
            mask = pg.mask.from_surface(self.image)
            target.blit(
                mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)),
                apply_scroll(self.rect, scroll),
            )
        else:
            target.blit(self.image, apply_scroll(self.rect, scroll))
