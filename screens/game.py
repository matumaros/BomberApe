

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from views.tilemap import TileMap


class Game(Screen):
    Builder.load_file('screens/game.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = TileMap()
