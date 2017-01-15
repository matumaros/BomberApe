

from uuid import uuid4

from kivy.lang import Builder

from screens.screen import Screen
from views.tilemap import TileMap
from controllers.player import Player


class Game(Screen):
    Builder.load_file('screens/game.kv')

    keybindings = {
        (276, ()): 'move_left',  # left arrow
        (275, ()): 'move_right',  # right arrow
        (273, ()): 'move_up',  # up arrow
        (274, ()): 'move_down',  # down arrow
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Player(uuid4(), self)
        self.board = TileMap()
        self.add_widget(self.board)
        self._ctrl = None  # Game controller

        self.actionbindings = {
            'move_left': lambda: self.controller.move(x=-1),
            'move_right': lambda: self.controller.move(x=1),
            'move_up': lambda: self.controller.move(y=1),
            'move_down': lambda: self.controller.move(y=-1),
        }
