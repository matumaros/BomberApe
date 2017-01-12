
from uuid import uuid4

from kivy.lang import Builder

from controllers.player import Player
from controllers.game import Game as GameCtrl
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
        if self.parent.has_screen('game'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        game = Game(name='game')
        self.parent.add_widget(game)
        game_ctrl = GameCtrl()
        game_ctrl.load_map('content/maps/new.map')
        player = Player(uuid4(), game_ctrl)
        game_ctrl.players = {
            player.uid: player,
        }
        euid = uuid4()
        game_ctrl.spawn_entity('gorilla', euid, player.uid)
        game.start(player)
        self.parent.switch_to('game')

    def init_editor(self):
        if self.parent.has_screen('editor'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        editor = Editor(name='editor', map_path='content/maps/new.map')
        self.parent.add_widget(editor)
        self.parent.switch_to('editor')
