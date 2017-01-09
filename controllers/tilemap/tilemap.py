

import yaml

from .tiles import TILES


class TileMap:
    def __init__(self):
        self.version = 1
        self.layers = {
            'ground': {},
            'util': {},
            'powerup': {},
            'wall': {},
        }
        self.path = ''

    def add_tile(self, coord, ttype):
        ltype = TILES[ttype].LTYPE
        self.layers[ltype][coord] = ttype

    def save(self):
        if not self.path:
            self.path = 'content/maps/new.map'  # ToDo: replace with dialog
        else:
            self.version += 1
        content = {
            'version': self.version,
            'layers': self.layers,
        }
        with open(self.path, 'w') as f:
            f.write(yaml.dump(content, default_flow_style=False))

    def load(self, map_path):
        with open(map_path, 'r') as f:
            content = yaml.load(f.read())

        self.version = content['version']
        self.layers = content['layers']
        self.path = map_path
