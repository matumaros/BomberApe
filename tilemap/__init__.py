

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
import yaml

from .tile import Tile


class TileMap(RelativeLayout):
    Builder.load_file('tilemap/tilemap.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tiles = {}
        self.focused_pos = 0, 0  # x, y of focus
        self.scale = (64, 64)

    def update_tiles(self, tiles):
        for pos, tile_type in tiles.items():
            try:
                tile = self.tiles[pos]
            except KeyError:
                pass
            else:
                self.remove_widget(tile)
            tile = Tile(
                source='atlas://atlases/tiles/{}'.format(tile_type),
                pos=pos,
                size=self.scale,
            )
            self.tiles[pos] = tile
            self.add_widget(tile)

    def load_map(self, name):
        return  # needs to be moved to loading module
        self.clear_children()
        with open('content/maps/' + name, 'r') as f:
            content = yaml.load(f.read())
        self.version = content['version']
        self.layers.clear()
        layers = content['layers']
        for layer in layers:
            formated_layer = {}
            for pos, tile in layer['tiles'].items():
                pos = tuple(pos.split('|'))
                formated_layer[pos] = tile
