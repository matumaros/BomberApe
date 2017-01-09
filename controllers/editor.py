

from .tilemap import TileMap


class EditorController:
    def __init__(self, view):
        self.view = view
        self.tilemap = TileMap()
