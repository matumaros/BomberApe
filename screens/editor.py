

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from tilemap import TileMap


class Editor(Screen):
    Builder.load_file('screens/editor.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = TileMap()
