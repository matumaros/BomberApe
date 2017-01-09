

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from controllers.editor import EditorController
from views.tilemap import TileMap


class Editor(Screen):
    Builder.load_file('screens/editor.kv')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = EditorController(self)
        self.board = TileMap()
        self.add_widget(self.board)
        Window.bind(on_key_down=self.on_key_down)
        self.keybindings = {
            103: 'place_ground',  # g
            119: 'place_wall',  # w
            276: 'select_left',  # left arrow
            275: 'select_right',  # right arrow
            273: 'select_up',  # up arrow
            274: 'select_down',  # down arrow
        }
        self.actionbindings = {
            'place_ground': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='ground',
            ),
            'place_wall': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='wall',
            ),
            'select_left': lambda: self.move_selected(x=-1),
            'select_right': lambda: self.move_selected(x=1),
            'select_up': lambda: self.move_selected(y=1),
            'select_down': lambda: self.move_selected(y=-1),
        }

        self.board.bind(
            selected_coord=lambda wg, coord: self.update_focus(coord)
        )
        self.board.selected_coord = '0|0'

    def update_focus(self, coord):
        self.board.focused_coord = coord

    def move_selected(self, x=0, y=0):
        coord = self.board.selected_coord
        norm = coord.split('|')
        x, y = (x + int(norm[0]), y + int(norm[1]))
        self.board.selected_coord = '{x}|{y}'.format(x=x, y=y)

    def on_key_down(self, keyboard, keycode, scancode, text, modifiers):
        try:
            action = self.keybindings[keycode]
        except KeyError:
            print('key not bound:', keycode)
            pass
        else:
            self.actionbindings[action]()
