import time


from .hud import Hud
from .utils import rtm
from .tile import Tile
from .settings import *
from .camera import Camera
from .player import Player


class Game:
    pg.init()

    def __init__(self, vsync=False) -> None:
        self.win_size = self.win_width, self.win_height = (1280, 720)
        self.size = self.width, self.height = (
            320 / settings["camera"]["zoom"],
            180 / settings["camera"]["zoom"],
        )

        self.window = pg.display.set_mode(self.win_size, vsync=vsync)
        self.clock = pg.time.Clock()

        self.target = surface(self.size)

        self.now = 0
        self.dt = 0
        self.prev_time = 0

        self.last_fixed_update_at = 0
        self.fixed_update_rate = 1 / 50

        self.running = True

        self.camera = Camera()

        self.player = Player(self, self.width / 2, self.height / 2)
        self.camera.follow = self.player.rect

        self.hud = Hud(self)

        self.tiles = [Tile(0, 0)]

    def handle_events(self):
        events = pg.event.get()

        for e in events:
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.running = False

        self.player.handle_events(events)

    def update_dt(self):
        self.now = time.time()
        self.dt = self.now - self.prev_time
        self.prev_time = self.now

    def update(self):
        self.player.update(self.dt)
        self.camera.update(self.target)

    def fixed_update(self):
        if not self.now - self.last_fixed_update_at > self.fixed_update_rate:
            return
        self.last_fixed_update_at = self.now

        self.player.fixed_update(self.dt)
        self.hud.update(self.dt)

    def draw(self):
        self.target.fill(pg.Color(26, 26, 32))
        pg.display.set_caption(f"{self.clock.get_fps():.1f}")

        # ? draw origin
        pg.draw.line(
            self.target,
            pg.Color(80, 80, 86),
            vector(0, self.height - self.camera.scroll.y),
            vector(self.width, self.height - self.camera.scroll.y),
        )

        pg.draw.line(
            self.target,
            pg.Color(80, 80, 86),
            vector(-self.camera.scroll.x, 0),
            vector(-self.camera.scroll.x, self.height),
        )
        # ? end draw origin

        [tile.draw(self.target, self.camera.scroll) for tile in self.tiles]
        self.player.draw(self.target, self.camera.scroll)

        pg.transform.scale(self.target, self.win_size, self.window)

        self.hud.draw(self.window)

        pg.display.update()
        self.clock.tick()

    def run(self):
        self.prev_time = time.time()  # avoids out of world dt on first frame

        while self.running:
            self.handle_events()
            self.update_dt()
            self.update()
            self.fixed_update()
            self.draw()
