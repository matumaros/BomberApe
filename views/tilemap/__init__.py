

from kivy.atlas import Atlas
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
import yaml

from .tile import Tile
from .entity import Entity


TEXPACK_PATH = 'atlas://content/texturepacks'
ENTITY_PATH = 'atlas://content/entities'


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
        normx, normy = tuple(map(float, coord.split('|')))
        focus = tuple(map(float, self.focused_coord.split('|')))
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
                source='{}/{}/tiles/{}'.format(
                    TEXPACK_PATH, self.texture_pack, ttype
                ),
                pos=self.coord_to_pos(coord),
                size=(self.scale, self.scale),
            )
            self.tiles[coord] = tile
            self.add_widget(tile)
        if self.selected:
            self.remove_widget(self.selected)
            self.add_widget(self.selected)

    def update_spawns(self, spawns):
        for coord, etype in spawns.items():
            try:
                spawn = self.spawns[coord]
            except KeyError:
                pass
            else:
                self.remove_widget(spawn)
            spawn = Tile(
                source='{}/{}/tiles/spawn'.format(
                    TEXPACK_PATH, self.texture_pack
                ),
                pos=self.coord_to_pos(coord),
                size=(self.scale, self.scale),
            )
            self.spawns[coord] = spawn
            spawn.label.text = etype
            self.add_widget(spawn)
        if self.selected:
            self.remove_widget(self.selected)
            self.add_widget(self.selected)

    def spawn_entity(self, coord, euid, skin, size=(1, 1)):
        size = (size[0] * self.scale, size[1] * self.scale)
        entity = Entity(
            source='{}/{}'.format(
                ENTITY_PATH, skin
            ),
            pos=self.coord_to_pos(coord),
            size=size,
            coord=coord,
        )
        # ToDo: somehow it doesn't set the texture, so it is set manually
        # figure out why that is, fix it and delete the next two lines
        atlas = Atlas('content/entities/entities.atlas')
        entity.texture = atlas[skin]
        self.entities[euid] = entity
        self.add_widget(entity)

    def move_entity(self, coord, euid):
        self.entities[euid].pos = self.coord_to_pos(coord)

    def on_center(self, wg, center):
        self.on_focused_coord(self.focused_coord)

    def on_selected_coord(self, coord):
        if not self.selected:
            self.selected = Tile(
                source='{}/{}/tiles/select'.format(
                    TEXPACK_PATH, self.texture_pack
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
        for coord, spawn in self.spawns.items():
            spawn.pos = self.coord_to_pos(coord)
        for entity in self.entities.values():
            entity.pos = self.coord_to_pos(entity.coord)
            self.remove_widget(entity)
            self.add_widget(entity)
        if self.selected and self.selected_coord:
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
