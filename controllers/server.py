

from kivy.clock import Clock


class Server:
    TICK_LENGTH = 1 / 10  # 10 times per second

    def __init__(self):
        self.paused = False
        self.players = {}
        self.entities = {}

    def start(self, map_path):
        for euid, entity in self.entities.items():
            player = self.players[entity.controller]
            player.set_entity(euid)
        Clock.schedule_once(self.tick)

    def tick(self, dt):
        if not self.paused:
            Clock.schedule_once(self.tick, self.TICK_LENGTH)

    def move_entity(self, issuer, euid, x, y):
        entity = self.entities[euid]
        entity.move(x * entity.speed, y * entity.speed)
