from .settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x: float, y: float) -> None:
        super().__init__()
        from .main import Game

        self.game: Game = game

        self.rect = pg.FRect(0, 0, 32, 32)
        self.rect.x = x
        self.rect.y = y

        self.speed = 140
        self.jump_force = 320
        self.gravity = 1200

        self.velocity = vector(0, 0)
        self.is_grounded = True
        self.is_running = False

        self.idle_sprite = pg.image.load("assets/player/idle.png").convert_alpha()
        self.run_sprite = pg.image.load("assets/player/run.png").convert_alpha()

        self.last_frame_at = 0
        self.frame_interval = 1 / 15

        self.sprite = self.idle_sprite
        self.current_frame = 0
        self.flipped = False

        self.keys = set()

    def handle_events(self, events: list[pg.Event]):
        for e in events:
            if e.type == pg.KEYDOWN:
                self.keys.add(e.key)
            elif e.type == pg.KEYUP:
                self.keys.remove(e.key)

    def update(self, dt: float = 0):
        if pg.K_a in self.keys:
            self.velocity.x = -self.speed
            self.flipped = True
        elif pg.K_d in self.keys:
            self.velocity.x = self.speed
            self.flipped = False
        else:
            self.velocity.x = 0

        if pg.K_SPACE in self.keys and self.is_grounded:
            self.is_grounded = False
            self.velocity.y = -self.jump_force

        new_pos = vector(
            self.rect.x + self.velocity.x * dt, self.rect.y + self.velocity.y * dt
        )

        if not self.is_grounded:
            self.velocity.y += self.gravity * dt

        if new_pos.y > self.game.height - self.rect.h:
            self.is_grounded = True
            new_pos.y = self.game.height - self.rect.h

        if new_pos.x < -self.rect.w:
            new_pos.x = self.game.width

        if new_pos.x > self.game.width:
            new_pos.x = -self.rect.w

        self.is_running = self.velocity.x != 0

        self.rect.x = new_pos.x
        self.rect.y = new_pos.y

    def fixed_update(self, dt: float = 0):
        if self.velocity.x != 0:
            self.sprite = self.run_sprite
        else:
            self.sprite = self.idle_sprite

    def draw(self, target: pg.Surface):
        if self.game.now - self.last_frame_at > self.frame_interval:
            self.current_frame += 1
            self.last_frame_at = self.game.now

        if self.current_frame + 1 > self.sprite.get_width() / self.rect.w:
            self.current_frame = 0

        target.blit(
            (
                pg.transform.flip(self.sprite, True, False)
                if self.flipped
                else self.sprite
            ),
            self.rect,
            pg.Rect(self.current_frame * self.rect.w, 0, self.rect.w, self.rect.h),
        )
