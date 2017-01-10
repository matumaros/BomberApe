

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from views.tilemap import TileMap


class Game(Screen):
    Builder.load_file('screens/game.kv')

    keybindings = {
        (276, ()): 'move_left',  # left arrow
        (275, ()): 'move_right',  # right arrow
        (273, ()): 'move_up',  # up arrow
        (274, ()): 'move_down',  # down arrow
    }

    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player
        self.board = TileMap()

        self.actionbindings = {
            'move_left': lambda: self.player.move(x=-1),
            'move_right': lambda: self.player.move(x=1),
            'move_up': lambda: self.player.move(y=1),
            'move_down': lambda: self.player.move(y=-1),
        }

    def start(self, map_path):
        self.player.start(map_path)
