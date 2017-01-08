

from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
import yaml


class TileMap(FloatLayout):
    # Builder.load_file('tilemap/tilemap.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = None
        self.layers = []

    def load_map(self, name):
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
