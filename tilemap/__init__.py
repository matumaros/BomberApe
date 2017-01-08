

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
import yaml

from .tile import Tile


class TileMap(RelativeLayout):
    Builder.load_file('tilemap/tilemap.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(focused_pos=lambda wg, pos: self.on_focused_pos(pos))

    def coord_to_pos(self, coord):
        norm = tuple(map(int, coord.split('|')))
        x = norm[0] * self.scale + self.focused_pos[0]
        y = norm[1] * self.scale + self.focused_pos[1]
        return x, y

    def update_tiles(self, tiles):
        for coord, tile_type in tiles.items():
            try:
                tile = self.tiles[coord]
            except KeyError:
                pass
            else:
                self.remove_widget(tile)
            tile = Tile(
                source='atlas://atlases/tiles/{}'.format(tile_type),
                pos=self.coord_to_pos(coord),
                size=(self.scale, self.scale),
            )
            self.tiles[coord] = tile
            self.add_widget(tile)

    def on_focused_pos(self, fpos):
        for coord, tile in self.tiles.items():
            tile.pos = self.coord_to_pos(coord)

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
