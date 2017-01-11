

from kivy.core.window import Window
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None
        self.board = TileMap()
        self.add_widget(self.board)
        Window.bind(on_key_down=self.on_key_down)

        self.actionbindings = {
            'move_left': lambda: self.player.move(x=-1),
            'move_right': lambda: self.player.move(x=1),
            'move_up': lambda: self.player.move(y=1),
            'move_down': lambda: self.player.move(y=-1),
        }

    def start(self, player):
        self.player = player
        player.view = self
        self.player.start()

    def on_key_down(self, keyboard, keycode, scancode, text, modifiers):
        try:
            action = self.keybindings[(keycode, tuple(modifiers))]
        except KeyError:
            print('key not bound:', (keycode, tuple(modifiers)))
            pass
        else:
            self.actionbindings[action]()
