

from .tiles import TILES


class TileMap:
    def __init__(self):
        self.layers = {
            'ground': {},
            'util': {},
            'powerup': {},
            'wall': {},
        }

    def add_tile(self, coord, ttype):
        ltype = TILES[ttype].LTYPE
        self.layers[ltype][coord] = ttype
