

from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import yaml


class TileMap(GridLayout):
    # Builder.load_file('world/world.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = None
        self.width = None
        self.height = None
        self.layers = []

    def load_map(self, name):
        self.clear_children()
        with open('content/maps/' + name, 'r') as f:
            content = yaml.load(f.read())
        self.version = content['version']
        self.width = content['width']
        self.height = content['height']
        self.layers.clear()
        layers = content['layers']
        for layer in layers:
            formated_layer = {}
            for pos, tile in layer['tiles'].items():
                pos = tuple(pos.split('|'))
                formated_layer[pos] = tile
