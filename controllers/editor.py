

from .tilemap import TileMap


class EditorController:
    def __init__(self, view):
        self.view = view
        self.tilemap = TileMap()

    def place_tile(self, coord, ttype):
        self.tilemap.add_tile(coord, ttype)
        self.view.board.update_tiles({coord: ttype})

    def get_tiles(self):
        layers = self.tilemap.layers
        tiles = layers['ground'].copy()
        tiles.update(layers['util'])
        tiles.update(layers['powerup'])
        tiles.update(layers['wall'])
        return tiles

    def save(self):
        self.tilemap.save()

    def load(self, map_path):
        self.tilemap.load(map_path)
        self.view.board.update_tiles(self.get_tiles())
