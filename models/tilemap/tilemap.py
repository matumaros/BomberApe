

import yaml

from .tiles import TILES


class TileMap:
    def __init__(self, path=''):
        self.version = 1
        self.layers = {
            'ground': {},
            'util': {},
            'powerup': {},
            'wall': {},
        }
        self.spawns = {}
        self.path = path
        self.load(path)

    def add_tile(self, coord, ttype):
        ltype = TILES[ttype].LTYPE
        self.layers[ltype][coord] = ttype

    def add_spawn(self, coord):
        self.spawns[coord] = None

    def get_free_spawns(self):
        spawns = []
        for coord, euid in self.spawns.items():
            if not euid:
                spawns.append(coord)
        return spawns

    def save(self):
        if not self.path:
            self.path = 'content/maps/new.map'  # ToDo: replace with dialog
        else:
            self.version += 1
        content = {
            'version': self.version,
            'layers': self.layers,
            'spawns': self.spawns,
        }
        with open(self.path, 'w') as f:
            f.write(yaml.dump(content, default_flow_style=False))

    def load(self, map_path):
        with open(map_path, 'r') as f:
            content = yaml.load(f.read())
        self.version = content.get('version', self.version)
        self.layers = content.get('layers', self.layers)
        self.spawns = content.get('spawns', self.spawns)
        self.path = map_path
