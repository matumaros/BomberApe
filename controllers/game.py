

from copy import deepcopy

from kivy.clock import Clock

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
        self.tilemap = None
        self.paused = False
        self.scenario = None
        self.players = {}
        self.entities = {}
        self.assignments = {}
        self.changes = deepcopy(CHANGES_TEMPLATE)  # changes since last tick

    def coord_to_pos(self, coord):
        return tuple(map(float, coord.split('|')))

    def setup(self, scenario, tilemap, players, assignments):
        self.scenario = scenario
        self.tilemap = tilemap
        self.players = players
        self.assignments = assignments
        for euid, etype in scenario.entities.items():
            for puid, euid_ in assignments.items():
                if euid_ == euid:
                    break
            else:
                puid = None
            self.spawn_entity(etype, euid, puid)
        self.changes['updated_tiles'] = self.get_tiles()

    def start(self):
        assert self.scenario
        Clock.schedule_once(self.tick)

    def tick(self, dt):
        if not self.paused:
            Clock.schedule_once(self.tick, self.TICK_LENGTH)
        proposals = self.update_players()
        self.changes = deepcopy(CHANGES_TEMPLATE)
        self.validate_proposals(proposals)

    def get_tiles(self):
        layers = self.tilemap.layers
        tiles = layers['ground'].copy()
        tiles.update(layers['util'])
        tiles.update(layers['powerup'])
        tiles.update(layers['wall'])
        return tiles

    def update_players(self):
        proposals = {}
        for puid, player in self.players.items():
            proposal = self.update_player(player)
            proposals[puid] = proposal
        return proposals

    def update_player(self, player):
        """Inform player about changes that matter to them"""
        changes = self.changes  # sort out things the player doesn't care about
        return player.update(changes)

    def validate_proposals(self, proposals):
        for puid, proposal in proposals.items():
            self.validate_proposal(puid, proposal)

    def validate_proposal(self, puid, proposal):
        for euid, pos in proposal['move'].items():
            self.move_entity(puid, euid, pos[0], pos[1])

    def spawn_entity(self, etype, euid, puid=None):
        for spawn, entity in self.tilemap.spawns.items():
            if not entity:
                self.tilemap.spawns[spawn] = euid
                entity = ENTITIES[etype](euid, self.coord_to_pos(spawn))
                self.entities[euid] = entity
                self.changes['change_controller_entity'][puid] = euid
                self.changes['spawn_entities'][euid] = entity
                break

    def move_entity(self, issuer, euid, x, y):
        entity = self.entities[euid]
        x, y = x * entity.speed, y * entity.speed
        entity.move(x, y)
        self.changes['move_entities'][euid] = entity.pos
