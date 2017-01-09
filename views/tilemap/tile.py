

from kivy.lang import Builder
from kivy.uix.image import Image


class Tile(Image):
    Builder.load_file('views/tilemap/tile.kv')

    def __init__(self, text='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label.text = text
