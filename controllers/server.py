

from copy import deepcopy

from kivy.clock import Clock

from .tilemap import TileMap


CHANGES_TEMPLATE = {
    'change_controller_entity': {},
    'move_entities': {},
    'spawn_entities': {},
    'updated_tiles': {},
}


class Server:
    TICK_LENGTH = 1 / 10  # 1 second / x | x times per second

    def __init__(self):
        self.tilemap = TileMap()
        self.paused = False
        self.players = {}
        self.entities = {}
        self.map_path = ''
        self.changes = deepcopy(CHANGES_TEMPLATE)  # changes since last tick

    def start(self):
        if self.map_path:
            self.tilemap.load(self.map_path)
        for euid, entity in self.entities.items():
            puid = entity.controller
            self.changes['change_controller_entity'][puid] = euid
        self.changes['updated_tiles'] = self.get_tiles()
        self.changes['spawn_entities'] = self.entities.copy()
        Clock.schedule_once(self.tick)

    def tick(self, dt):
        if not self.paused:
            Clock.schedule_once(self.tick, self.TICK_LENGTH)
        for puid, player in self.players.items():
            self.update_player(player)
        self.changes = deepcopy(CHANGES_TEMPLATE)

    def get_tiles(self):
        layers = self.tilemap.layers
        tiles = layers['ground'].copy()
        tiles.update(layers['util'])
        tiles.update(layers['powerup'])
        tiles.update(layers['wall'])
        return tiles

    def update_player(self, player):
        """Inform player about changes that matter to them"""
        player.update(self.changes)

    def move_entity(self, issuer, euid, x, y):
        entity = self.entities[euid]
        x, y = x * entity.speed, y * entity.speed
        entity.move(x, y)
        self.changes['move_entities'][euid] = entity.pos
