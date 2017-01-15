

from copy import deepcopy

from kivy.clock import Clock

from models.tilemap import TileMap
from controllers.entities import ENTITIES


CHANGES_TEMPLATE = {
    'change_controller_entity': {},
    'move_entities': {},
    'spawn_entities': {},
    'updated_tiles': {},
}


class Game:
    TICK_LENGTH = 1 / 10  # 1 second / x | x times per second

    def __init__(self):
        self.tilemap = TileMap()
        self.paused = False
        self.scenario = None
        self.players = {}
        self.assignments = {}
        self.changes = deepcopy(CHANGES_TEMPLATE)  # changes since last tick

    def coord_to_pos(self, coord):
        return tuple(map(float, coord.split('|')))

    def setup(self, scenario, players, assignments):
        self.scenario = scenario
        self.players = players
        self.assignments = assignments

    def start(self):
        assert self.scenario
        self.load_map(self.scenario.map_path)
        self.changes['updated_tiles'] = self.get_tiles()
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
        updates = player.update(self.changes)
        for euid, pos in updates['move'].items():
            self.move_entity(player.uid, euid, pos[0], pos[1])

    def spawn_entity(self, etype, euid, puid=None):
        for spawn, entity in self.tilemap.spawns.items():
            if not entity:
                self.tilemap.spawns[spawn] = euid
                entity = ENTITIES[etype](euid, self.coord_to_pos(spawn))
                self.scenario.entities[euid] = entity
                self.changes['change_controller_entity'][puid] = euid
                self.changes['spawn_entities'][euid] = entity
                break

    def load_map(self, path):
        self.scenario.map_path = path
        self.tilemap.load(path)

    def move_entity(self, issuer, euid, x, y):
        entity = self.scenario.entities[euid]
        x, y = x * entity.speed, y * entity.speed
        entity.move(x, y)
        self.changes['move_entities'][euid] = entity.pos
