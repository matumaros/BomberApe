

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from controllers.editor import EditorController
from views.tilemap import TileMap


class Editor(Screen):
    Builder.load_file('screens/editor.kv')

    def __init__(self, map_path='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = EditorController(self)
        self.board = TileMap()
        self.add_widget(self.board)
        Window.bind(on_key_down=self.on_key_down)
        self.keybindings = {  # ToDo: move to Editor scope (like Game)
            (103, ()): 'place_ground',  # g
            (105, ()): 'place_ice',  # i
            (115, ()): 'place_spawn',  # s
            (119, ()): 'place_wall',  # w
            (97, ()): 'place_water',  # a
            (98, ()): 'place_bridge',  # b
            (99, ()): 'place_crate',  # c
            (276, ()): 'select_left',  # left arrow
            (275, ()): 'select_right',  # right arrow
            (273, ()): 'select_up',  # up arrow
            (274, ()): 'select_down',  # down arrow
            (115, ('ctrl',)): 'save_map',  # s
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
            'place_ice': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='ice',
            ),
            'place_water': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='water',
            ),
            'place_bridge': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='bridge',
            ),
            'place_crate': lambda: self.controller.place_tile(
                coord=self.board.selected_coord,
                ttype='crate',
            ),
            'place_spawn': lambda: self.controller.place_spawn(
                coord=self.board.selected_coord,
            ),
            'select_left': lambda: self.move_selected(x=-1),
            'select_right': lambda: self.move_selected(x=1),
            'select_up': lambda: self.move_selected(y=1),
            'select_down': lambda: self.move_selected(y=-1),
            'save_map': self.controller.save,
        }

        self.board.bind(
            selected_coord=lambda wg, coord: self.update_focus(coord)
        )
        self.board.selected_coord = '0|0'
        if map_path:
            self.controller.load(map_path)

    def update_focus(self, coord):
        self.board.focused_coord = coord

    def move_selected(self, x=0, y=0):
        coord = self.board.selected_coord
        norm = coord.split('|')
        x, y = (x + int(norm[0]), y + int(norm[1]))
        self.board.selected_coord = '{x}|{y}'.format(x=x, y=y)

    def on_key_down(self, keyboard, keycode, scancode, text, modifiers):
        try:
            action = self.keybindings[(keycode, tuple(modifiers))]
        except KeyError:
            print('key not bound:', (keycode, tuple(modifiers)))
            pass
        else:
            self.actionbindings[action]()
