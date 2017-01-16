
from uuid import uuid4

from kivy.lang import Builder

from controllers.game import Game as GameCtrl
from models.scenario import Scenario
from models.tilemap import TileMap
from screens.screen import Screen
from screens.game import Game
from screens.editor import Editor


class MainMenu(Screen):
    Builder.load_file('screens/main_menu.kv')

    keybindings = {
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.actionbindings = {
        }

    def init_game(self):
        # Initialization
        scenario = Scenario()
        scenario.map_path = 'content/maps/new.map'
        tilemap = TileMap(scenario.map_path)
        ctrl = GameCtrl()

        # Game Setup
        euid = uuid4()
        scenario.entities = {
            euid: 'gorilla'
        }

        if self.parent.has_screen('game'):
            game = self.parent.get_screen('game')
        else:
            game = Game(name='game')
            self.parent.add_widget(game)
        player = game.controller
        player.entity = euid

        # Start
        ctrl.setup(
            scenario=scenario,
            tilemap=tilemap,
            players={
                player.uid: player,
            },
            assignments={
                player.uid: euid,
            }
        )
        ctrl.start()
        game._ctrl = ctrl
        self.parent.switch_to('game')

    def init_editor(self):
        if self.parent.has_screen('editor'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        editor = Editor(name='editor', map_path='content/maps/new.map')
        self.parent.add_widget(editor)
        self.parent.switch_to('editor')
