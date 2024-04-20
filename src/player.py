from .settings import *
from .sprite import Sprite
from .utils import apply_scroll
from .tiles import Wall, Collectible


class Player(Sprite):
    def __init__(self, level, x: float, y: float) -> None:
        super().__init__(vector(x, y))
        from .levels.level import Level

        self.level: Level = level
        self.hud = self.level.game.hud

        self.speed = 140
        self.jump_force = 320
        self.gravity = 1200

        self.velocity = vector(0, 0)
        self.max_velocity = 5000
        self.jump = False
        self.jump_counter = 0
        self.max_jumps = 9999 if DEV else 2
        self.jump_cooldown = 1 / 4
        self.last_jump_at = 0
        self.is_grounded = False

        self.image = pg.Surface((32, 32))
        self.image.set_colorkey(Color.BLACK)
        self.rect = self.image.get_frect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.hit_rect = self.rect.inflate(-12, -8)

        self.debug = False
        self.flipped = False

        self.movement_binds = settings["keybinds"]["movements"]

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

        self.last_frame_at = 0
        self.frame_interval = 1 / 20
        self.current_frame = 0

        self.score = 0

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

        if pg.key.get_just_pressed()[settings["keybinds"]["misc"]["debug"]]:
            self.debug = not self.debug

        self.velocity.x = input_vector.normalize().x if input_vector else input_vector.x

    def land(self):
        self.jump_counter = 0
        self.is_grounded = True
        if not self.jump:
            self.velocity.y = 0

    def collide(self, walls: list[Wall]):
        for wall in walls:
            if not wall.rect.colliderect(self.hit_rect):
                continue

            # bottom
            if (
                self.hit_rect.bottom >= wall.rect.top
                and self.old_rect.bottom < wall.old_rect.top + 1
            ):
                self.hit_rect.bottom = wall.rect.top
                self.land()
            # top
            elif (
                self.hit_rect.top <= wall.rect.bottom
                and self.old_rect.top >= wall.old_rect.bottom - 1
            ):
                self.hit_rect.top = wall.rect.bottom
                self.velocity.y = 0
            # right
            elif (
                self.hit_rect.right >= wall.rect.left
                and self.old_rect.right < wall.old_rect.left + 1
            ):
                self.hit_rect.right = wall.rect.left
            # left
            elif (
                self.hit_rect.left <= wall.rect.right
                and self.old_rect.left > wall.old_rect.right - 1
            ):
                self.hit_rect.left = wall.rect.right

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

    def collide_collectibles(self, collectibles: list[Collectible] = []):
        for i, collectible in enumerate(collectibles):
            if collectible.rect.colliderect(self.hit_rect):
                collectibles.pop(i)
                self.score += collectible.value

    def update(
        self,
        dt: float = 0,
        walls: list[Wall] = [],
        collectibles: list[Collectible] = [],
    ):
        self.old_rect = self.hit_rect.copy()

        self.move(dt)
        self.collide(walls)
        self.collide_collectibles(collectibles)

        self.hit_rect.y = int(self.hit_rect.y)
        self.rect.topleft = (
            self.hit_rect.x - 6,
            self.hit_rect.y - 8,
        )  # adjust based on rect inflation

    def fixed_update(self, dt: float = 0, tiles=[]):
        # debug pos
        self.hud.debug(
            "pos",
            "\u0040",
            f"{self.rect.x:.1f} {self.rect.y:.1f} | {self.hit_rect.x:.1f} {self.hit_rect.y:.1f} ",
            (69, 92, 123),
        )

        self.hud.debug(
            "direction",
            "V",
            f"{self.velocity.x:.1f} {self.velocity.y:.1f}",
            (80, 150, 150),
        )

        self.hud.debug(
            "player_debug",
            "P",
            f"{self.is_grounded} {self.jump_counter}",
            (180, 124, 170),
        )

        self.hud.debug(
            "player_score",
            "S",
            f"{self.score}",
            (44, 197, 246),
        )

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

        # draw outline
        # pg.draw.lines(
        #         target,
        #         Color.WHITE,
        #         False,
        #         [
        #             (x + self.rect.x - scroll.x, y + self.rect.y - scroll.y)
        #             for x, y in self.mask.outline(every=1)
        #         ],
        #     )

        if self.debug:
            pg.draw.rect(
                target, Color.GREEN, apply_scroll(self.hit_rect, scroll, "rect"), 1
            )
            pg.draw.rect(
                target, Color.RED, apply_scroll(self.old_rect, scroll, "rect"), 1
            )
