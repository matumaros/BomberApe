

from kivy.lang import Builder
from kivy.uix.image import Image


class Tile(Image):
    Builder.load_file('tilemap/tile.kv')
