
from uuid import uuid4

from kivy.lang import Builder

from controllers.player import Player
from controllers.server import Server
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
        server = Server()
        server.load_map('content/maps/new.map')
        player = Player(uuid4(), server)
        server.players = {
            player.uid: player,
        }
        euid = uuid4()
        server.spawn_entity('gorilla', euid, player.uid)
        game.start(player)
        self.parent.switch_to('game')

    def init_editor(self):
        if self.parent.has_screen('editor'):
            screen = self.parent.get_screen('game')
            self.parent.remove_widget(screen)
        editor = Editor(name='editor', map_path='content/maps/new.map')
        self.parent.add_widget(editor)
        self.parent.switch_to('editor')
