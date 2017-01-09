

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
import yaml

from .tile import Tile


ATLAS_PATH = 'atlas://content/texturepacks/'


class TileMap(RelativeLayout):
    Builder.load_file('views/tilemap/tilemap.kv')

    def __init__(self, texture_pack='default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texture_pack = texture_pack
        self.bind(focused_coord=lambda wg, coord: self.on_focused_coord(coord))
        self.bind(
            selected_coord=lambda wg, coord: self.on_selected_coord(coord)
        )

    def coord_to_pos(self, coord):
        normx, normy = tuple(map(int, coord.split('|')))
        focus = tuple(map(int, self.focused_coord.split('|')))
        focx = focus[0] * self.scale
        focy = focus[1] * self.scale
        offx = self.center[0] - focx
        offy = self.center[1] - focy
        x = normx * self.scale + offx
        y = normy * self.scale + offy
        return x, y

    def update_tiles(self, tiles):
        for coord, ttype in tiles.items():
            try:
                tile = self.tiles[coord]
            except KeyError:
                pass
            else:
                self.remove_widget(tile)
            tile = Tile(
                source='{}{}/tiles/{}'.format(
                    ATLAS_PATH, self.texture_pack, ttype
                ),
                pos=self.coord_to_pos(coord),
                size=(self.scale, self.scale),
            )
            self.tiles[coord] = tile
            self.add_widget(tile)

    def on_center(self, wg, center):
        self.on_focused_coord('0|0')

    def on_selected_coord(self, coord):
        if not self.selected:
            self.selected = Tile(
                source='{}{}/tiles/select'.format(
                    ATLAS_PATH, self.texture_pack
                ),
                pos=self.coord_to_pos(coord),
                size=(self.scale, self.scale),
            )
            self.add_widget(self.selected)
        else:
            self.selected.pos = self.coord_to_pos(coord)

    def on_focused_coord(self, fcoord):
        for coord, tile in self.tiles.items():
            tile.pos = self.coord_to_pos(coord)
        self.selected.pos = self.coord_to_pos(self.selected_coord)
        self.selected.label.text = self.selected_coord

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
