

from kivy.lang import Builder
from kivy.uix.image import Image


class Entity(Image):
    Builder.load_file('views/tilemap/entity.kv')

    def __init__(self, coord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coord = coord
