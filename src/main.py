import time


from .hud import Hud
from .settings import *
from .levels.dev_level import DevLevel
from .levels.other_dev_level import OtherDevLevel


class Game:
    pg.init()

    def __init__(self, vsync=False) -> None:
        self.window = pg.display.set_mode(window_size, vsync=vsync)
        self.clock = pg.time.Clock()

        self.target = surface(display_size)

        self.now = 0
        self.dt = 0
        self.prev_time = 0

        self.last_fixed_update_at = 0
        self.fixed_update_rate = 1 / 50

        self.running = True

        self.hud = Hud(self)

        self.level = DevLevel(self)

    def handle_events(self):
        events = pg.event.get()

        for e in events:
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:  # !temp
                    self.running = False
                if e.key == pg.K_l:  # !temp
                    self.level = OtherDevLevel(self)

        self.level.handle_events(events)

    def update_dt(self):
        self.now = time.time()
        self.dt = self.now - self.prev_time
        self.prev_time = self.now

    def update(self):
        self.level.update(self.dt)

    def fixed_update(self):
        if not self.now - self.last_fixed_update_at > self.fixed_update_rate:
            return
        self.last_fixed_update_at = self.now

        self.level.fixed_update(self.dt)
        self.hud.update(self.dt)

    def draw(self):
        self.target.fill(pg.Color(26, 26, 32))
        pg.display.set_caption(f"{self.clock.get_fps():.1f}")

        self.level.draw(self.target)

        pg.transform.scale(self.target, window_size, self.window)

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
