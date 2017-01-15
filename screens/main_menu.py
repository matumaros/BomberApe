
from uuid import uuid4

from kivy.lang import Builder

from controllers.entities import ENTITIES
from controllers.game import Game as GameCtrl
from models.scenario import Scenario
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
        scenario = Scenario()
        scenario.map_path = 'content/maps/new.map'
        euid = uuid4()
        scenario.entities = {
            euid: ENTITIES['gorilla'](euid, (1, 1)),
        }

        if self.parent.has_screen('game'):
            game = self.parent.get_screen('game')
        else:
            game = Game(name='game')
            self.parent.add_widget(game)
        player = game.controller
        player.entity = euid
        self._ctrl = GameCtrl()
        self._ctrl.setup(
            scenario=scenario,
            players={
                player.uid: player,
            },
            assignments={
                player.uid: euid,
            }
        )
        self._ctrl.start()
        self.parent.switch_to('game')

    def init_editor(self):
        if self.parent.has_screen('editor'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        editor = Editor(name='editor', map_path='content/maps/new.map')
        self.parent.add_widget(editor)
        self.parent.switch_to('editor')
