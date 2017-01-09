

from .tilemap import TileMap


class EditorController:
    def __init__(self, view):
        self.view = view
        self.tilemap = TileMap()

    def place_tile(self, coord, ttype):
        self.tilemap.add_tile(coord, ttype)
        self.view.board.update_tiles({coord: ttype})

    def save(self):
        self.tilemap.save()
